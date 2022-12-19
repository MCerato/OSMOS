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
from File import TXTFile as txtf
from Controlbox import ControlBox
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
    # Get default Files
    Project = "OSMOS"
    ProjectDir = os.path.dirname(__file__)

    while os.path.basename(ProjectDir) != Project:
        ProjectDir = os.path.dirname(ProjectDir)

    DefaultCBFile = ProjectDir + "\\Documentation\\Reference" + "\\OSM_LIST_CB.csv"
    DefaultCdeFile = ProjectDir + "\\Documentation\\Reference" + "\\OSM_LIST_CDE.csv"
    DefaultbakFolder = ProjectDir + "\\Sources"+"\\.bak\\"
    DefaultlogFolder = ProjectDir + "\\Sources"+"\\.log\\"

    def __init__(self, CBFile=DefaultCBFile, CdeFile=DefaultCdeFile, 
                 bakFolder=DefaultbakFolder,logFolder=DefaultlogFolder):

        self.CBFile = CBFile
        self.CdeFile = CdeFile
        self.bakFolder = bakFolder
        self.logFolder = logFolder
        self.osmosf = OSMOSFiles.OSMOSFiles(self.CBFile, self.CdeFile)
 
        self.listOfCBToGet = []

        
        srcDirectory = os.path.dirname(__file__)        
        print(srcDirectory)

        # print(self.osmosf.CdeDatas)
        self.CB = ControlBox.ControlBox()

        self.axis = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.vectors = ["S", "T"]
        self.vectorSpeed = ["N", "M"]

    def OSMOSSeq(self, network="TEST", userIP=None):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
# =============================================================================
#         self.network = network
#         self.userIP = userIP
# =============================================================================

        if userIP:
            print(userIP)
            self.listOfCBToGet.append(userIP)
            logName = self.__GenerateFileName(None, userIP)
        else:
            if network:
                print(network)
                self.listOfCBToGet = self.osmosf.CBFileNtwrkFilter(network)
                logName = self.__GenerateFileName(network, None)
            else:
                print("nothing to work on!")
                return None

        parametersList = self.osmosf.CdeFileParamList()

        # ----------------- log File Preparation ----------------------
        self.logFolder = os.path.dirname(__file__) + "\\.log\\"
        logFullName = self.logFolder + logName
        self.logFile = txtf.TXT(logFullName)
        self.logFile.EraseContent()
        
        self.logFile.AddContent(f" SOLEIL network : {network}")
        # sequence
        for ip in self.listOfCBToGet:

            # ----------------- bak File Preparation ----------------------
            self.bakFolder = os.path.dirname(__file__) + "\\.bak\\"
            bakName = self.__GenerateFileName(network, ip)
            bakFullName = self.bakFolder + bakName

            connected = self.CB.Connect(ip)

            if connected:
                bakFile = txtf.TXT(bakFullName)
                bakFile.EraseContent()
                self.logFile.AddContent("------------------------------------")
                self.logFile.AddContent(f"connected to {ip}")

                # -------------------- system Info Part -----------------------
                try:
                    print("System Info : run...")
                    bakFile.AddContent(self.__SystemInfo())
                    self.logFile.AddContent("System ok")
                    print("System Info : Done")

                except Exception as ex:
                    self.logFile.AddContent("Getting System Info Failed")
                    self.logFile.AddContent(f"due to : {ex}")

                # -------------------- Parameters Part ------------------------
                try:
                    print("Parameters : run...")
                    bakFile.AddContent(self.__Configuration(parametersList))
                    self.logFile.AddContent("parameters ok")
                    print("Parameters : Done")

                except Exception as ex:
                    self.logFile.AddContent("Getting configuration Failed")
                    self.logFile.AddContent(f"error : {ex}")

                # -------------------- Variables Part -------------------------
                try:
                    print("Variables : run...")
                    bakFile.AddContent(self.__Data())
                    self.logFile.AddContent("Variables ok")
                    print("Variables : Done")

                except Exception as ex:
                    self.logFile.AddContent("Getting Datas (variables) Failed")
                    self.logFile.AddContent(f"error : {ex}")
                    print("Variables : Done")

                # -------------------- Microcode Part -------------------------
                try:
                    print("Microcode : run...")
                    bakFile.AddContent(self.__Program())
                    self.logFile.AddContent("Microcode ok")
                    print("Microcode : Done")

                except Exception as ex:
                    self.logFile.AddContent("Getting Microcode Failed")
                    self.logFile.AddContent(f"error : {ex}")
                self.CB.Disconnect()

                self.logFile.AddContent(f"disconnected from {ip}\n\n")

                bakFile.RenameFile(bakFullName.replace(".txt", ".bak"))
            # end of sequence
            else:
                self.logFile.AddContent("------------------------------------")
                self.logFile.AddContent(f"couldn't connect to {ip}\n\n")
        
            # ----------------------- Format Files ----------------------------
        print("End of work")
        self.logFile.RenameFile(logFullName.replace(".txt", ".log"))
        time.sleep(0.2)

    def GetAllNetworks(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        networksList = []
        for network in self.osmosf.CBFileNtwrks():               
            if networksList.count(network)<1:
                networksList.append(network)
        return networksList
    
    def GetAllParameters(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        return self.osmosf.CdeFileParamList()
           
    def __SystemInfo(self):
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

        self.logFile.AddContent(f"firmware : {firmware}")
        self.logFile.AddContent(f"serial : {serial}")
        return systemInfo

    def __Configuration(self, parametersList):
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
        motOFF = "MO\\size=1\n" + "MO\\1\\Cmd=MO" + "\\r" + "\n"
        variableFormat = "VF=VF " + self.CB.GetParameter("VF?") + "\\r" + "\n"
        positionFormat = "PF=PF " + self.CB.GetParameter("PF?") + "\\r" + "\n"
        ommitLeading0 = "LZ=LZ 1\\r" + "\n"

        config = "[Configuration]\n" + echo
        config = config + variableFormat
        config = config + positionFormat + ommitLeading0

        for param in parametersList:
            if self.__DoesFWExists(param):
                # print(param)
                config = config + self.__ParamTrt(param)

        config = config + motOFF + "\n"
        # print(config)
        return config

    def __Data(self):
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

    def __Program(self):
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

        # In[1]: internal function for Class OSMOSGui
    def __GenerateFileName(self, network = None, ip = None):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        CVSName = self.osmosf.CBFileGetName(ip)

        fullTime = time.gmtime()
        year = str(fullTime.tm_year)
        month = str(fullTime.tm_mon)
        day = str(fullTime.tm_mday)
        hour = str(fullTime.tm_hour)
        minute = str(fullTime.tm_min)
        second = str(fullTime.tm_sec)

        if ip is not None and network is not None:
            name = "OSMOS_" + "_" + CVSName
            name = name + "_" + year + month + day
            name = name + "_" + hour + minute + second
            name = name + ".txt"

        elif ip is not None and network is None:

            name = "OSMOS_" + ip
            name = name + "_" + year + month + day
            name = name + "_" + hour + minute + second
            name = name + ".txt"

        elif ip is None and network is not None:
            name = "OSMOS_" + network
            name = name + "_" + year + month + day
            name = name + "_" + hour + minute + second
            name = name + ".txt"
        else:
            print("nothing to work on!")

        return name

    def __ParamTrt(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        howToRead, howToWrite = self.osmosf.CdeFileReadWriteType(param)

        if howToRead == "Standard":
            resultFromCB = self.__StdRead(param)

        elif howToRead == "Unique":
            resultFromCB = self.__UniqueRead(param)

        elif howToRead == "Message":
            resultFromCB = self.__MessageRead(param)

        elif howToRead == "Vector":
            resultFromCB = self.__VectorRead(param)

        else:
            resultFromCB = None
            # error

        if howToWrite == "Standard":
            result = self.__StdWrite(param, resultFromCB)

        elif howToWrite == "Sized":
            result = self.__SizedWrite(param, resultFromCB)

        elif howToWrite == "Special":
            result = self.__SpecialWrite(param, resultFromCB)

        elif howToWrite == "Unique":
            result = self.__UniqueWrite(param, resultFromCB)

        elif howToWrite == "Vector":
            result = self.__VectorWrite(param, resultFromCB)

        else:
            print("plop2")
            # error

        return result

        # In[1]: internal function for Class OSMOSGui
    def __StdRead(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        answers = []
        for axisValue in self.axis:
            cmd = self.osmosf.GetFormattedCmd(param, axisValue)
            ans = self.CB.GetParameter(cmd)
            answers.append(ans)

        return answers

    def __StdWrite(self, param, answerFromCB):
        output = self.osmosf.writeFormattedParam(param)

        for index, axisValue in enumerate(self.axis):
            output = output.replace(param + axisValue + "=v", 
                                    param + axisValue + "=" + answerFromCB[index])

        return output

        # In[1]: internal function for Class OSMOSGui
    def __UniqueRead(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        cmd = self.osmosf.GetFormattedCmd(param)
        ans = [self.CB.GetParameter(cmd)]

        return ans

    def __UniqueWrite(self, param, answerFromCB):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        output = self.osmosf.writeFormattedParam(param)
        answerFromCB[0] = answerFromCB[0].replace(", ", ",")
        output = output.replace("v", answerFromCB[0])

        return output

        # In[1]: internal function for Class OSMOSGui
    def __MessageRead(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        cmd = self.osmosf.GetFormattedCmd(param)
        ans = [self.CB.GetParameter(cmd)]
        return ans

        # In[1]: internal function for Class OSMOSGui
    def __SizedWrite(self, param, resultFromCB):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        Size = 0
        output = self.osmosf.writeFormattedParam(param, "1")
        if param != "BA":
            for value in resultFromCB:
                if value != "0":
                    Size += 1

            output = self.osmosf.writeFormattedParam(param, Size)
            output = output.replace("size=v", "size=" + str(Size))

        if param != "BA":
            nb = 0
            for index, axisValue in enumerate(self.axis):
                ans = resultFromCB[index]
                if ans != "0":
                    nb += 1
                    output = output.replace(param + "\\" + str(nb) + "\\Cmd=\"" + param + "x=v",
                                            param + "\\" + str(nb) + "\\Cmd=\"" + param + axisValue + "=" + ans)

        return output

        # In[1]: internal function for Class OSMOSGui
    def __SpecialWrite(self, param, resultFromCB):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        output = self.osmosf.writeFormattedParam(param)

        if resultFromCB[0].count(",") == 5:
            for index, axisValue in enumerate(self.axis):
                ansListed = resultFromCB[index].split(", ")
                a = ansListed[0] + ","
                b = ansListed[1] + ","
                c = ansListed[2] + ","
                d = ansListed[3] + "<"
                e = ansListed[4] + ">"
                f = ansListed[5]

                output = output.replace(param + axisValue + "=a,b,c,d<e>f",
                                        param +  axisValue + "=" + a + b + c + d + e + f)

        if resultFromCB[0].count(",") == 4:
            for index, axisValue in enumerate(self.axis):
                ansListed = resultFromCB[index].split(", ")
                a = ansListed[0] + ","
                b = ansListed[1] + ","
                c = ansListed[2] + ","
                d = ansListed[3] + "<"
                e = ansListed[4]

                output = output.replace(param + axisValue + "=a,b,c,d<e",
                                        param +  axisValue + "=" + a + b + c + d + e)

        return output
        # output = self.osmosf.writeFormattedParam(param, Size)

        # In[1]: internal function for Class OSMOSGui
    def __VectorRead(self, param):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        if param[-1] == "I":
            answers = []
            for axisValue in self.vectorSpeed:
                cmd = self.osmosf.GetFormattedCmd(param, axisValue)
                ans = self.CB.GetParameter(cmd)            
                answers.append(ans)

        else:
            answers = []
            for axisValue in self.vectors:
                cmd = self.osmosf.GetFormattedCmd(param, axisValue)
                ans = self.CB.GetParameter(cmd)
                answers.append(ans)
        return answers

    def __VectorWrite(self, param, resultFromCB):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """

        if param[-1] == "I":
            output = self.osmosf.writeFormattedParam(param)
            param = param[:2]
            for index, axisValue in enumerate(self.vectorSpeed):
                output = output.replace(param + axisValue + "=v",
                                        param + axisValue + "=" + resultFromCB[index])

        else:
            output = self.osmosf.writeFormattedParam(param)

            for index, axisValue in enumerate(self.vectors):
                output = output.replace(param + axisValue + "=v",
                                        param + axisValue + "=" + resultFromCB[index])

        return output

    def __DoesFWExists(self, parameter):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        firmwares = self.osmosf.CdeFileGetFWAvail(parameter)
        firmware = self.CB.GetFWVersion()
        for FW in firmwares:
            if FW == firmware:
                return True

        return False


if __name__ == '__main__':
    # osmos = OSMOS(network=None, ipAdress="172.16.3.65")
    osmos = OSMOS()
    # osmos.OSMOSSeq(network="TEST", userIP=None)
    osmos.OSMOSSeq(network=None, userIP="172.16.3.88")
