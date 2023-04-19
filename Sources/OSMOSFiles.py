# -*- coding: utf-8 -*-
"""Manage The OSMOS Files CB and Command (.csv).

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
- CSVFile library (:file:../FilePages/CSVFile.html)
    - Access to a CSV wrapper File management.

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
- Implement Tests according to Official tests protocol (TDD)

Author(s)
---------
- Created by M. Cerato on 10/05/2022.
- Modified by M. Cerato on 10/12/2022.

Copyright (c) 2022 Cerato Workshop.  All rights reserved.

Members
-------
"""
import os
from Packages.File import CSVFile as csvf


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
        Should be : ``OSMOS/Sources/.bak``
    :type DefaultCBFile:
        str
    :attr DefaultCdeFile:
        Path where default GALIL commands File is situated
        Should be : ``OSMOS/Sources/.log``
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

    def __init__(self, pathCB=DefaultCBFile, pathCmd=DefaultCdeFile):

        self.listCB = csvf.CSV(pathCB)
        self.listCde = csvf.CSV(pathCmd)

        self.CBDatas = self.listCB.GetColumnDatas()
        self.networks = self.FileCleanup(self.CBDatas["network"], '')
        self.Ips = self.FileCleanup(self.CBDatas["Adresse-IP"], '')
        self.Names = self.FileCleanup(self.CBDatas["Racine-nom-CVS"], '')

        self.CdeDatas = self.listCde.GetColumnDatas()
        self.FWAvailable = self.FileCleanup(self.CdeDatas["Firmware"], '')
        self.syntaxGetParam = self.FileCleanup(self.CdeDatas["type-getparam"],
                                               '')
        self.param = self.FileCleanup(self.CdeDatas["parameter"], '')
        self.getParamFormat = self.FileCleanup(self.CdeDatas["get"], '')
        self.setParamFormat = self.FileCleanup(self.CdeDatas["set"], '')

        self.syntaxWriteBak = self.FileCleanup(self.CdeDatas["type-wrtbak"],
                                               '')
        self.writeBakFormat = self.FileCleanup(self.CdeDatas["write"], '')

    def FileCleanup(self, listToClean, strToClean):
        """Take ``strToClean`` off the ``listToClean``.

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

    def UpdateCBFile(self, newPath):
        """Link this  objet to an other csv file.

        It updates all of his attributes too.

        :param newPath:
            path of the new file to be associated with
        :type newPath:
            str
        """
        self.listCB = csvf.CSV(newPath)
        self.CBDatas = self.listCB.GetColumnDatas()
        self.networks = self.FileCleanup(self.CBDatas["network"], '')
        self.Ips = self.FileCleanup(self.CBDatas["Adresse-IP"], '')
        self.Names = self.FileCleanup(self.CBDatas["Racine-nom-CVS"], '')
        print(f"new file : {newPath}")

    def UpdateCdeFile(self, newPath):
        """Link this object to an other csv file.

        It updates all of his attributes too.

        :param newPath:
            path of the new file to be associated with
        :type newPath:
            str
        """
        self.listCde = csvf.CSV(newPath)
        self.CdeDatas = self.listCde.GetColumnDatas()
        self.FWAvailable = self.FileCleanup(self.CdeDatas["Firmware"], '')
        self.syntaxGetParam = self.FileCleanup(self.CdeDatas["type-getparam"],
                                               '')
        self.param = self.FileCleanup(self.CdeDatas["parameter"], '')
        self.getParamFormat = self.FileCleanup(self.CdeDatas["get"], '')
        self.setParamFormat = self.FileCleanup(self.CdeDatas["set"], '')

        self.syntaxWriteBak = self.FileCleanup(self.CdeDatas["type-wrtbak"],
                                               '')
        self.writeBakFormat = self.FileCleanup(self.CdeDatas["write"], '')
        print(f"new file : {newPath}")
        # In[1]: internal function for Class OSMOSGui

    def CBFileNtwrks(self):
        """Give The list of network ("network" column from the CB file).

        example : ``rcm`` or ``ISAC``

        :return:
            Return a list of networks
        :rtype:
            list
        """
        return self.networks

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
        for index, net in enumerate(self.networks):
            if net == network:
                networkIPs.append(self.Ips[index])
        return networkIPs

    def CBFileGetName(self, IP):
        """Give the name of the ControlBox Associated to the given IP.

        .. important::
            ``IP`` should be xxxx.xxxx.xxxx.xxxx format (not GALIL format)

        :param IP:
            form "RCM", "TEMPO", etc...
        :type network:
            str

        .. warning::
            Works only on .CSV.

        .. warning::
            IP can be ``None``! It will just be ignored in the .csv list
        """
        for index, ip in enumerate(self.Ips):
            if ip == IP:
                CVSName = self.Names[index]
                return CVSName

        return None  # "NameNotFound"

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

        .. note::
            empty lines are automatically removed.

        :return:
            Return a list of GALIL parameters
        :rtype:
            list
        """
        return self.FileCleanup(self.CdeDatas["parameter"], '')

    def CdeFileReadWriteType(self, parameter):
        """Give the *""How to read"* and *"How to Write"* of a GALIL parameter.

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
            the size that should be writed into .bak, but only if necessary.
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

    # Default CB and Cde file
    print(osmosf.CBFileNtwrks())
    print(osmosf.CdeFileParamList())
    print("")

    # Alternative CB and Cde file
    osmosf.UpdateCBFile("D:/Temp_pro/OSMOS/Test/altern_CB_Path/OSM_LIST_CB.csv")
    osmosf.UpdateCdeFile("D:/Temp_pro/OSMOS/Test/altern_Cde_Path/OSM_LIST_CDE.csv")
    print(osmosf.CBFileNtwrks())
    print(osmosf.CdeFileParamList())
