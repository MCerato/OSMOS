# -*- coding: utf-8 -*-
"""Manage The OSMOS Files CB and Command (not .bak and .log).

Description
-----------
Allow to treat and format the .csv files where are ControlBox informations and
GALIL Command Informations

.. note::
    add waiting time when files are created

Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.
- CSVFile Personal library
    (https://github.com/MCerato/FileManagement/tree/main/Sources/Packages/File)
    - Access to a personal CSV wrapper File management.

.. note::
    CSVFile has lightly been modified for the purpose of OSMOS.
    Mainly indications and differents ``print``

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
- Modified by M. Cerato on 10/12/2022.

Copyright (c) 2022 Cerato Workshop.  All rights reserved.

Members
-------
"""
import os
from File import CSVFile as csvf


class OSMOSFiles:
    """Class managing OSMOS project configuration Files.

    :attr Project:
        Should be the Project directory name (ex : OSMOS in this case)
    :type Project:
        str
    :attr ProjectDir:
        automatic detection of the path according to the name project
    :type ProjectDir:
        str
    :attr DefaultCBFile:
        Path where default ControlBox File is situated
    :type DefaultCBFile:
        str
    :attr DefaultCdeFile:
        Path where default GALIL commands File is situated
    :type DefaultCdeFile:
        str
    """

    # Get default Files
    Project = "OSMOS"
    ProjectDir = os.path.dirname(__file__)

    while os.path.basename(ProjectDir) != Project:
        ProjectDir = os.path.dirname(ProjectDir)

    DefaultCBFile = ProjectDir + "\\Documentation\\Reference"
    DefaultCBFile = DefaultCBFile + "\\OSM_LIST_CB.csv"

    DefaultCdeFile = ProjectDir + "\\Documentation\\Reference"
    DefaultCdeFile = DefaultCdeFile + "\\OSM_LIST_CDE.csv"

    # ********************

    def __init__(self, listCB=DefaultCBFile, listCmd=DefaultCdeFile):

        listCB = csvf.CSV(listCB)
        listCde = csvf.CSV(listCmd)

        self.__CBDatas = listCB.GetColumnDatas()
        self.__networks = self.FileCleanup(self.__CBDatas["ssh aile"], '')
        self.__Ips = self.FileCleanup(self.__CBDatas["Adresse-IP"], '')
        self.__Names = self.FileCleanup(self.__CBDatas["Racine-nom-CVS"], '')
        # example (uncomment line below)
        # self.listOfCBToGet = self.CBFileNtwrkFilter("ISAC")

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

    def FileCleanup(self, listToClean, strToClean):
        """Take ``strToClean`` from the ``listToClean``.

        .. note::
            Mainly used here to clean the empty lines from the files.

        :param listToClean:
            Can be any list
        :type listToClean:
            list
        :param strToClean:
            Any Character. Can be empty character too.
        :type strToClean:
            str
        :return:
            Return a list without ``strToClean``
        :rtype:
            list
        """
        listCleaned = listToClean.copy()
        for element in listToClean:
            if element == strToClean:
                listCleaned.remove(element)
        return listCleaned

        # In[1]: internal function for Class OSMOSGui

    def CBFileNtwrks(self):
        """Give The list of network ("ssh-Ailes") column from the CB file.

        :return:
            Return a list of networks
        :rtype:
            list
        """
        return self.__networks

    def CBFileNtwrkFilter(self, network):
        """Extract the IPs according to the network input.

        :param network:
            SOLEIL network onto the form "RCM", "TEMPO", etc...
        :type network:
            str
        :return:
            Return a list of IP's
        :rtype:
            list
        """
        networkIPs = []
        for index, net in enumerate(self.__networks):
            if net == network:
                networkIPs.append(self.__Ips[index])
        return networkIPs

    def CBFileGetName(self, IP):
        """Give the name of the ControlBox Associated to the given IP.

        .. note::
            ``IP`` should be xxxx.xxxx.xxxx.xxxx format (not GALIL format)

        :param IP:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.
        """
        for index, ip in enumerate(self.__Ips):
            if ip == IP:
                CVSName = self.__Names[index]
                return CVSName

        return "NameNotFound"

        # In[1]: internal function for Class OSMOSGui

    def CdeFileCmdFilter(self, FW):
        """Return a list of GALIL parameters according to the firmware given.

        :param FW:
            GALIL Firmware (ex: DMC4183s56f or DMC2182s87j)
        :type FW:
            str

        :return:
            Return a list of GALIL parameters
        :rtype:
            list
        """
        parameters = []
        for index, FWValue in enumerate(self.FWAvailable):
            if FWValue == FW:
                parameters.append(self.param[index])
        return parameters

    def CdeFileParamList(self):
        """Return the entire list of paramters in the file.

        :return:
            Return a list of GALIL parameters
        :rtype:
            list
        """
        return self.FileCleanup(self.CdeDatas["parameter"], '')

    def CdeFileReadWriteType(self, parameter):
        """Give the "How to read" and "How to Write" of a GALIL parameter.

        This parameter has to be present in the Command file.
        :param parameter:
            GALIL parameter (ex: SP or AC or DC)
        :type parameter:
            str

        :return readType:
            Return the way to read the parameter from the controller
        :rtype:
            list

        :return readType:
            Return the way to write the parameter into the .bak file
        :rtype:
            list

        """
        commandIndex = self.param.index(parameter)
        readType = self.syntaxGetParam[commandIndex]
        writeType = self.syntaxWriteBak[commandIndex]

        return readType, writeType

    def CdeFileGetFWAvail(self, parameter):
        """Return the available GALIL firmwares for a GALIL parameter given.

        :param parameter:
            GALIL parameter (ex: SP or AC or DC)
        :type parameter:
            str

        :return:
            Return the list of available firmwares
        :rtype:
            list

        """
        commandIndex = self.param.index(parameter)
        WhichFW = self.FWAvailable[commandIndex].split(", ")

        return WhichFW

    def GetFormattedCmd(self, commandToGet, axis="A"):
        """Return the formatted way to read a parameter.

        (ex: parameter is SP and axis is B then, it returns SPB=?)

        .. note::
            This is according to the way to read the parameter. i.e: IA doesn't
            have any axis then it will return "IA ?"

        :param commandToGet:
            GALIL parameter (ex: SP or AC or DC)
        :type commandToGet:
            str

        :param axis:
            GALIL axis from "A" to "H"
        :type axis:
            str

        :return:
            the formatted reading string
        :rtype:
            str
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

    def writeFormattedParam(self, paramTolook, size="0", ):
        """Return the formatted way to write a parameter into .bak file.

        .. note::
            This is according to the command file ``OSM_LIST_CDE``.

        sometimes, the number of parameters to write depends on his "size"
        except for some size hardcoded by GALIL, this parameter is automaticaly
        calculated

        :param paramTolook:
            GALIL parameter (ex: SP or AC or DC)
        :type commandToGet:
            str

        :param size:
            the size tha should be writed into .bak, but only if necessary.
        :type size:
            str

        :return:
            the formatted writing string
        :rtype:
            str
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
