# -*- coding: utf-8 -*-
"""Test the class FileWrapper.

Description
-----------
Sequence of tests for FileWrapper methods.

.. warning::
    Test non exhaustive (WIP - learning on tests methods)

.. note::
    add waiting time when files are created

Libraries/Modules
-----------------
- sys standard library (https://docs.python.org/3/library/sys.html)
    - Access to functions interacting with interpreter.
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.
- time standard library (https://docs.python.org/2/library/time.html)
    - Access to time-related functions.
- PDFFile library (:file:FileWrapper.html)
    - Access to files functions.

Version
-------
- 1.0.0.0

Notes
-----
- None

TODO
----
- Implement Tests according to Official tests protocol

Author(s)
---------
- Created by M. Cerato on 10/05/2022.
- Modified by xxx on xx/xx/xxxx.

Copyright (c) 2022 Cerato Workshop.  All rights reserved.

Members
-------
"""
import os
import time
from Controlbox import ControlBox
from File import TXTFile as txtf
import OSMOSFiles


class OSMOS:
    """Class representing the CSV file.

    :param userPath:
        where the CSV file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self, network=None, ipAdress=None):

        self.listOfCBToGet = []

        srcDirectory = os.path.dirname(__file__)
        print(srcDirectory)
        CBFile = srcDirectory + "\\OSM_LIST_CB.csv"
        CdeFile = srcDirectory + "\\OSM_LIST_CDE2.csv"

        self.osmosf = OSMOSFiles.OSMOSFiles(CBFile, CdeFile)
        # print(self.osmosf.CdeDatas)
        self.CB = ControlBox.ControlBox()

        self.network = network

        if self.network is None and ipAdress is not None:
            self.listOfCBToGet.append(ipAdress)

        elif self.network is None and ipAdress is None:
            self.listOfCBToGet = self.osmosf.CBFileNtwrkFilter(self.network)

        elif self.network is not None and ipAdress is not None:
            self.listOfCBToGet.append(ipAdress)

        else:
            self.listOfCBToGet = self.osmosf.CBFileNtwrkFilter("TEST")

        self.axis = ["A", "B", "C", "D", "E", "F", "G", "H"]

        # sequence
        for ip in self.listOfCBToGet:
            self.CB.Connect(ip)
            bakFolder = os.path.dirname(__file__) + "\\.bak\\"
            bakName = self.GenerateFileName()
            bakFullName = bakFolder + bakName
            bakFile = txtf.TXT(bakFullName)
            bakFile.EraseContent()

            bakFile.AddContent(self.SystemInfo())
            bakFile.AddContent(self.Configuration())
            bakFile.AddContent(self.Data())
            bakFile.AddContent(self.Program())
            self.CB.Disconnect()
            bakFile.RenameFile(bakFullName.replace(".txt", ".bak"))
        # end of sequence

# =============================================================================
#     def CBconnection(self, ip):
#         self.CB.Connect(ip)
# =============================================================================

    def SystemInfo(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        firmware = "Firmware=" + self.CB.GetFWVersion() + "\n"
        serial = "Serial=" + self.CB.GetSerial() + "\n"
        device = "Device=" + self.CB.GetFWVersion()[:7].replace("8", "x")
        device = device + "\n"
        axisNb = "Axis=" + self.CB.GetFWVersion()[5] + "\n"

        systemInfo = "[SystemInfo]\n" + firmware + serial
        systemInfo = systemInfo + device + axisNb
        systemInfo = systemInfo + "\n"
        return systemInfo

    def Configuration(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
# ******************************** init ***************************************
        echo = "EO=false" + "\n"
        firmware = "REM Source Firmware = " + self.CB.GetFWVersion() + "\n"
        setupCmd = "REM Setup Command" + "\n"
        rc = "RC 0" + "\n"
        motOFF = "MO\\size=1\n" + "MO\\1\\Cmd=MO" + "\\r" + "\n"
        stop = "ST" + "\n"
        specialConf = "REM special configuration" + "\n"
        variableFormat = "VF=VF " + self.CB.GetParameter("VF?") + "\\r" + "\n"
        positionFormat = "PF=PF " + self.CB.GetParameter("PF?") + "\\r" + "\n"
        ommitLeading0 = "LZ=LZ 1\\r" + "\n"
        rem = "REM" + "\n"
        motEncsetup = "REM motor encoder setup" + "\n"

        config = "[Configuration]\n" + echo + firmware + setupCmd + rc
        config = config + motOFF + stop + specialConf + variableFormat
        config = config + positionFormat + ommitLeading0 + rem + motEncsetup

# ********************************* MT ****************************************
        mt = "MT\\"
        mtCmd = ""

        for index, element in enumerate(self.axis):
            cmd = self.osmosf.GetFormattedCmd("MT", element)
            ans = self.CB.GetParameter(cmd)
            cmdAns = cmd.replace("?", ans)
            mtCmd = mtCmd + mt + str(index+1) + "\\Cmd=\"" + cmdAns + "\\r\""
            mtCmd = mtCmd + "\n"

        mtSize = mt + "size=" + self.CB.GetFWVersion()[5] + "\n"
        config = config + mtSize
        config = config + mtCmd

# ********************************* GA ****************************************
        ga = "GA\\"
        gaCmd = ""
        gaSizeNb = 0

        for index, element in enumerate(self.axis):
            cmd = self.osmosf.GetFormattedCmd("GA", element)
            ans = self.CB.GetParameter(cmd)
            if ans != "0":
                gaSizeNb += 1
                cmdAns = cmd.replace("?", ans)
                gaCmd = gaCmd + ga + str(gaSizeNb-1)
                gaCmd = gaCmd + "\\Cmd=\"" + cmdAns + "\\r\""
                gaCmd = gaCmd + "\n"

        gaSize = ga + "size=" + str(gaSizeNb)
        config = config + gaSize + "\n"
        config = config + gaCmd

# *****************************************************************************
        config = config + self.__GetStdParameters("CE")
        config = config + self.__GetStdParameters("AF")
        config = config + self.__GetStdParameters("DV")
        config = config + self.__GetStdParameters("FL")
        config = config + self.__GetStdParameters("BL")
        config = config + self.__GetStdParameters("CL")


# ********************************* SI ****************************************
        config = config + self.__GetStdParameters("SI")
        config = config + self.__GetStdParameters("DB")
        print(config)
        config = config + self.__GetStdParameters("DS")
        config = config + self.__GetStdParameters("KD")
        config = config + self.__GetStdParameters("KI")
        config = config + self.__GetStdParameters("KP")
        config = config + self.__GetStdParameters("K3")
        config = config + self.__GetStdParameters("K2")
        config = config + self.__GetStdParameters("K1")
        config = config + self.__GetStdParameters("ZN")
        config = config + self.__GetStdParameters("ZP")
        config = config + self.__GetStdParameters("CP")
        config = config + self.__GetStdParameters("CT")
        config = config + self.__GetStdParameters("IL")
        config = config + self.__GetStdParameters("TK")
        config = config + self.__GetStdParameters("TL")
        config = config + self.__GetStdParameters("OF")
        config = config + self.__GetStdParameters("FA")
        config = config + self.__GetStdParameters("FV")
        config = config + self.__GetStdParameters("PL")
        config = config + self.__GetStdParameters("IT")
        config = config + self.__GetStdParameters("NB")
        config = config + self.__GetStdParameters("NF")
        config = config + self.__GetStdParameters("NZ")
        config = config + self.__GetStdParameters("AC")
        config = config + self.__GetStdParameters("DC")
        config = config + self.__GetStdParameters("SP")
        config = config + self.__GetStdParameters("GD")
        config = config + self.__GetStdParameters("GM")
        config = config + self.__GetStdParameters("GR")
        config = config + self.__GetStdParameters("OE")
        config = config + self.__GetStdParameters("ER")
        config = config + self.__GetStdParameters("TW")
        config = config + self.__GetStdParameters("BW")
        config = config + self.__GetStdParameters("KS")
        config = config + self.__GetStdParameters("YA")
        config = config + self.__GetStdParameters("YB")
        config = config + self.__GetStdParameters("YC")
        config = config + self.__GetUniqueParameters("IA")
        config = config + self.__GetMessageParameters("TM")
        config = config + self.__GetUniqueParameters("MW")
        config = config + self.__GetMessageParameters("CW")
        config = config + self.__GetMessageParameters("CN0")
        config = config + self.__GetMessageParameters("CN1")
        config = config + self.__GetMessageParameters("CN2")
        config = config + self.__GetMessageParameters("CN3")
        config = config + self.__GetMessageParameters("CN4")
        config = config + "\n"

        return config

    def Data(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
# ***************************** Variables *************************************
        variables = self.CB.GetAllVariables()
        varSize = len(variables)

        varData = ""
        variableInit = "Variable\\"
        for varNb, var in enumerate(variables):
            nameValue = var.split("= ")
            varName = nameValue[0]
            varValue = nameValue[1]

            varData = varData + variableInit
            varData = varData + str(varNb+1) + "\\Name=" + varName + "\n"
            varData = varData + variableInit
            varData = varData + str(varNb+1) + "\\Value=" + varValue + "\n"

        data = "[Data]\n"
        data = data + variableInit + "size=" + str(varSize) + "\n"
        data = data + varData

# ****************************** Arrays ***************************************
        arrays = self.CB.GetAllArrays()
        arrNb = len(arrays)

        arrData = ""
        arrInit = "Array\\"

        for arrNumber, array in enumerate(arrays):
            nameLen = array.split("[")
            arrName = nameLen[0]

            arrLen = nameLen[1].split("]")
            arrLen = arrLen[0]

            arrData = arrData + arrInit
            arrData = arrData + str(arrNumber+1) + "\\Name=" + arrName + "\n"
            arrData = arrData + arrInit
            arrData = arrData + str(arrNumber+1) + "\\Size=" + arrLen + "\n"

            ansData = ""
            for i in range(int(arrLen)):
                req = arrName + "[" + str(i) + "]"
                ans = self.CB.GetVariable(req)

                if i != int(arrLen)-1:
                    ansData = ansData + ans + ", "

                else:
                    ansData = ansData + ans
            arrData = arrData + arrInit
            arrData = arrData + str(arrNumber+1) + "\\Value=" + ansData + "\n"

        # print(arrData)
        data = data + arrInit + "size=" + str(arrNb) + "\n"
        data = data + arrData

        data = data + "\n"
        return data

    def Program(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        programInit = "Program=\""
        program = "[Program]\n"
        mcode = self.CB.GetMicrocode().replace("\r\n", "\\n")
        program = program + programInit + mcode + "\""
        return program

    def GenerateFileName(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        fullTime = time.gmtime()
        year = str(fullTime.tm_year)
        month = str(fullTime.tm_mon)
        day = str(fullTime.tm_mday)
        hour = str(fullTime.tm_hour)
        minute = str(fullTime.tm_min)
        second = str(fullTime.tm_sec)

        if self.network is not None:
            name = "OSMOS_" + self.network + "_IP_"
        else:
            name = "OSMOS_" + "_IP_"
        name = name + year + month + day + hour + minute + second + ".txt"

        return name

    def __GetStdParameters(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        init = param + "=\""
        outputStr = ""
        for index, element in enumerate(self.axis):
            cmd = self.osmosf.GetFormattedCmd(param, element)
            ans = self.CB.GetParameter(cmd)
            cmdAns = cmd.replace("?", ans)
            outputStr = outputStr + cmdAns + "\\r"
            if (index+1) == len(self.axis):
                outputStr = outputStr + "\"" + "\n"
        output = init + outputStr
        return output

    def __GetUniqueParameters(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        if param == "MW":
            init = param + "="
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = cmd.replace("?", ans)
            outputStr = cmdAns + "\\r" + "\n"
            output = init + outputStr
            return output
        else:
            init = param + "=\""
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = cmd.replace("?", ans)
            outputStr = cmdAns + "\\r\"" + "\n"
            output = init + outputStr
            return output

    def __GetMessageParameters(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        if param == "CN0":
            init = param + "="
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param[:2] + " " + ans
            outputStr = cmdAns + "\\r" + "\n"
            output = init + outputStr
            return output

        elif param == "CN1":
            init = param + "=\""
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param[:2] + " ," + ans
            outputStr = cmdAns + "\\r\"" + "\n"
            output = init + outputStr
            return output

        elif param == "CN2":
            init = param + "=\""
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param[:2] + " ,," + ans
            outputStr = cmdAns + "\\r\"" + "\n"
            output = init + outputStr
            return output

        elif param == "CN3":
            init = param + "=\""
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param[:2] + " ,,," + ans
            outputStr = cmdAns + "\\r\"" + "\n"
            output = init + outputStr
            return output

        elif param == "CN4":
            init = param + "=\""
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param[:2] + " ,,,," + ans
            outputStr = cmdAns + "\\r\"" + "\n"
            output = init + outputStr
            return output

        else:
            init = param + "="
            outputStr = ""
            cmd = self.osmosf.GetFormattedCmd(param)
            ans = self.CB.GetParameter(cmd)
            cmdAns = param + " " + ans
            outputStr = cmdAns + "\\r" + "\n"
            output = init + outputStr
            return output


if __name__ == '__main__':
    # osmos = OSMOS(network=None, ipAdress="172.16.3.65")
    osmos = OSMOS(network="TEST", ipAdress=None)
    # print(osmos.SystemInfo())
    # print(osmos.Configuration())
    # print(osmos.Data())
    # print(osmos.Program())

    # osmos = OSMOSSeq("RCM")
