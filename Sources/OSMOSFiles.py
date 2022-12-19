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
    # Get default Files
    Project = "OSMOS"
    ProjectDir = os.path.dirname(__file__)

    while os.path.basename(ProjectDir) != Project:
        ProjectDir = os.path.dirname(ProjectDir)

    DefaultCBFile = ProjectDir + "\\Documentation\\Reference" + "\\OSM_LIST_CB.csv"
    DefaultCdeFile = ProjectDir + "\\Documentation\\Reference" + "\\OSM_LIST_CDE.csv"

    # ********************

    def __init__(self, listCB=DefaultCBFile, listCmd=DefaultCdeFile):

        listCB = csvf.CSV(listCB)
        listCde = csvf.CSV(listCmd)

        self.__CBDatas = listCB.GetColumnDatas()
        self.__networks = self.FileCleanup(self.__CBDatas["ssh aile"], '')
        self.__Ips = self.FileCleanup(self.__CBDatas["Adresse-IP"], '')
        self.__Names = self.FileCleanup(self.__CBDatas["Racine-nom-CVS"], '')
        # example (uncomment line below)
        # self.listOfCBToGet = self.CBFileNtwrkFilter("TEST")

        self.CdeDatas = listCde.GetColumnDatas()
        self.FWAvailable = self.FileCleanup(self.CdeDatas["Firmware"], '')
        self.syntaxGetParam = self.FileCleanup(self.CdeDatas["type-getparam"],
                                               '')
        self.param = self.FileCleanup(self.CdeDatas["parameter"], '')
        self.getParamFormat = self.FileCleanup(self.CdeDatas["get"], '')
        self.setParamFormat = self.FileCleanup(self.CdeDatas["set"], '')

        self.syntaxWriteBak = self.FileCleanup(self.CdeDatas["type-wrtbak"],
                                               '')
        self.writeBakFormat = self.FileCleanup(self.CdeDatas["write"], '')
        # self.writeFormattedParam("MT")
        # example (uncomment line below)
        # self.listOfCmdToGet = self.CdeFileCmdFilter("3")

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

        # In[1]: internal function for Class OSMOSGui

    def CBFileNtwrks(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        return self.__networks

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

    def CBFileGetName(self, IP):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        for index, ip in enumerate(self.__Ips):
            if ip == IP:
                CVSName = self.__Names[index]
                CVSName = CVSName.replace("_parameters", "")
                return CVSName

        return "NameNotFound"

        # In[1]: internal function for Class OSMOSGui

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
        for index, keyValue in enumerate(self.FWAvailable):
            if keyValue == key:
                parameters.append(self.param[index])
        return parameters

    def CdeFileParamList(self):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        return self.FileCleanup(self.CdeDatas["parameter"], '')

    def CdeFileReadWriteType(self, parameter):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        commandIndex = self.param.index(parameter)
        readType = self.syntaxGetParam[commandIndex]
        Writetype = self.syntaxWriteBak[commandIndex]

        return readType, Writetype

    def CdeFileGetFWAvail(self, parameter):
        """Extract the IPs according to the network input.

        :param network:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        commandIndex = self.param.index(parameter)
        WhichFW = self.FWAvailable[commandIndex].split(", ")

        return WhichFW

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
        if self.syntaxGetParam[commandIndex] == "Standard":
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

        elif self.syntaxGetParam[commandIndex] == "Unique":
            command = self.getParamFormat[commandIndex]

        elif self.syntaxGetParam[commandIndex] == "Message":
            command = self.getParamFormat[commandIndex]

        else:
            paramCommandFormat = self.getParamFormat[commandIndex]
            command = paramCommandFormat.replace("x", axis)

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

        if self.syntaxWriteBak[commandIndex] == "Sized":
            paramWriteFormat = self.writeBakFormat[commandIndex]
            paramList = paramWriteFormat.split(r"\n")
            paramList = paramList[:int(size)+1]
            paramWriteFormat = ""

            for elt in paramList:
                if elt != paramList[-1]:
                    paramWriteFormat = paramWriteFormat + elt + "\n"
                else:
                    paramWriteFormat = paramWriteFormat + elt
            paramWriteFormat = paramWriteFormat.replace("'", '"')
        
        else:
            paramWriteFormat = self.writeBakFormat[commandIndex]
            paramWriteFormat = paramWriteFormat.replace("'", '"')            

        return paramWriteFormat + "\n"

if __name__ == '__main__':
    osmosf = OSMOSFiles()
