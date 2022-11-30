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

from File import CSVFile as csvf

class OSMOSFiles:
    """Class representing the CSV file.

    :param userPath:
        where the CSV file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self, listCB="D:/Temp_pro/OSMOS/Sources/OSM_LIST_CB.csv",
                 listCmd="D:/Temp_pro/OSMOS/Sources/OSM_LIST_CDE2.csv"):

        listCB = csvf.CSV(listCB)
        listCde = csvf.CSV(listCmd)

        self.__CBDatas = listCB.GetColumnDatas()
        self.__networks = self.FileCleanup(self.__CBDatas["ssh aile"], '')
        self.__Ips = self.FileCleanup(self.__CBDatas["Adresse-IP"], '')

        # example (uncomment line below)
        # self.listOfCBToGet = self.CBFileNtwrkFilter("TEST")

        self.CdeDatas = listCde.GetColumnDatas()
        self.keyParam = self.FileCleanup(self.CdeDatas["key-param"], '')
        self.syntaxParam = self.FileCleanup(self.CdeDatas["syntax-param"], '')
        self.param = self.FileCleanup(self.CdeDatas["keyword"], '')
        self.getParamFormat = self.FileCleanup(self.CdeDatas["get"], '')
        self.setParamFormat = self.FileCleanup(self.CdeDatas["set"], '')

        self.syntaxWriteBak = self.FileCleanup(self.CdeDatas["syntax-bak"], '')
        self.writeBakFormat = self.FileCleanup(self.CdeDatas["write"], '')
        plop = print(self.writeBakFormat[0])
        self.writeFormattedParam("MT")
        # example (uncomment line below)
        # self.listOfCmdToGet = self.CdeFileCmdFilter("3")

# =============================================================================
#         print(self.param)  # all parameters
#         print(self.CdeFileCmdFilter("3"))  # parameters according to the values of key
#         print(self.CBFileNtwrkFilter("TEST"))
#         print(self.GetFormattedCmd("MT", "B"))
#         print(self.GetFormattedCmd("IA"))
#         print(self.GetFormattedCmd("IA", "B"))  # B is ignored
#         print(self.SetFormattedCmd("MT", "1", "B"))
#         print(self.SetFormattedCmd("MT", "2", "B"))
# =============================================================================

    def FileCleanup(self, listToClean, strToclean):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        listCleaned = listToClean.copy()
        for element in listToClean:
            if element == strToclean:
                listCleaned.remove(element)
        return listCleaned

    def CBFileNtwrkFilter(self, network):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        networkIPs = []
        for index, net in enumerate(self.__networks):
            if net == network:
                networkIPs.append(self.__Ips[index])
        return networkIPs

    def CdeFileCmdFilter(self, key):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        parameters = []
        for index, keyValue in enumerate(self.keyParam):
            if keyValue == key:
                parameters.append(self.param[index])
        return parameters

    def GetFormattedCmd(self, commandToGet, axis="A"):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        commandIndex = self.param.index(commandToGet)
        if self.syntaxParam[commandIndex] == "1":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

        elif self.syntaxParam[commandIndex] == "2":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "3":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "4":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "5":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "6":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "7":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "8":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxParam[commandIndex] == "9":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("i", "0")

        elif self.syntaxParam[commandIndex] == "10":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

        elif self.syntaxParam[commandIndex] == "11":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

        else:
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

        return command

    def SetFormattedCmd(self, commandToSet, valueToGive, axis="A"):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        commandIndex = self.param.index(commandToSet)

        if self.syntaxParam[commandIndex] == "1":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)
            command = command.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "2":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "3":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "4":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "5":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "6":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "7":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "8":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "9":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("i", "0")
            command = command.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "10":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)
            command = command.replace("v", valueToGive)

        elif self.syntaxParam[commandIndex] == "11":
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)
            command = command.replace("v", valueToGive)

        else:
            paramCommandFormat = self.setParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)
            command = command.replace("v", valueToGive)

        return command

    def writeFormattedParam(self, paramTolook, size = "0", ):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        commandIndex = self.param.index(paramTolook)
        print(commandIndex)
        print(size)
        print(self.syntaxWriteBak)
        if self.syntaxWriteBak[commandIndex] == "1":
            if size == "4":
                paramWriteFormat = self.writeBakFormat[commandIndex]
            else:
                paramWriteFormat = self.writeBakFormat[commandIndex]
                tempFormat = paramWriteFormat.split("\\n")
                print(paramWriteFormat)
                print(tempFormat)     
                print(tempFormat[0])

        if self.syntaxWriteBak == "3":
            paramWriteFormat = self.writeBakFormat[commandIndex]

        return paramWriteFormat

# =============================================================================
#         if self.syntaxParam[commandIndex] == "1":
#             paramCommandFormat = self.getParamFormat[commandIndex]
#             command = paramCommandFormat.replace("x", axis)
# 
#         elif self.syntaxParam[commandIndex] == "2":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "3":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "4":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "5":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "6":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "7":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "8":
#             command = self.getParamFormat[commandIndex]
# 
#         elif self.syntaxParam[commandIndex] == "9":
#             paramCommandFormat = self.getParamFormat[commandIndex]
#             command = paramCommandFormat.replace("i", "0")
# 
#         elif self.syntaxParam[commandIndex] == "10":
#             paramCommandFormat = self.getParamFormat[commandIndex]
#             command = paramCommandFormat.replace("x", axis)
# 
#         elif self.syntaxParam[commandIndex] == "11":
#             paramCommandFormat = self.getParamFormat[commandIndex]
#             command = paramCommandFormat.replace("x", axis)
# 
#         else:
#             paramCommandFormat = self.getParamFormat[commandIndex]
#             command = paramCommandFormat.replace("x", axis)
# 
#         return command
# =============================================================================

if __name__ == '__main__':
    osmosf = OSMOSFiles()
