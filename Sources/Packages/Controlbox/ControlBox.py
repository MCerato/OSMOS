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

import gclib


class ControlBox:
    """Class representing the file.

    :param path:
        where the file is.
        Path should be absolute with format ``C:/file1/file2/sourcefile``
    :type path:
        str
    :param name:
        Name of the file. For instance ``plop.txt``
    :type name:
        str
    :param size:
        size of the file in bytes
    :type size:
        int
    :param fileFormat:
        extention of the file. for Instance, ``.txt``
    :type fileFormat:
        int
    """

    def __init__(self):
        self.g = gclib.py()

    def __del__(self):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected():
            print("disconnected")
            self.g.GClose()

    def Connect(self, ip):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        try:
            self.g.GOpen(ip)
            print(f"connected to {ip}")
            return True
        except gclib.GclibError:
            print(f"couldn't connect to {ip}")
            return False

    def Disconnect(self):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        self.g.GCommand("IHT =>-3")
        self.g.GClose()
        if self.__IsConnected() is True:
            print("Disconnection failed")
            return False
        else:
            print("Disconnected")
            return True

    def Reset(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            savedIP = self.GetIp()
            self.g.GCommand("RS")
            # try to connect until it does connect or timeout
            # self.g.Connect(savedIP)

    def GetMicrocode(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GProgramUpload()

    def SetMicrocode(self, code):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GProgramDownload(code)

    def GetVariable(self, galilVar):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GCommand(galilVar + "=?")

    def GetAllVariables(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            rawVariables = self.g.GCommand("LV")
            variables = rawVariables.split("\r\n")
            return variables
            
    def GetAllArrays(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            rawArrays = self.g.GCommand("LA")
            arrays = rawArrays.split("\r\n")
            return arrays            

    def GetParameter(self, command):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            if command[-1:] == "?":
                return self.g.GCommand(command)

            elif command[:3] == "MG_":
                return self.g.GCommand(command)

            else:
                print(f"the command {command} is not a query")

    def SetParameter(self, command):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GCommand(command)

    def GetIp(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GCommand("IA?")

    def GetFWVersion(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GInfo().split(", ")[1]

    def GetSerial(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.__IsConnected() is True:
            return self.g.GInfo().split(", ")[2] + ".0000"

    def __IsConnected(self):
        """Return the entire file.

        :param userPath:
            where the TXT file is.
            Path should be, preferably, absolute with format :
            ``C:/file1/file2/sourcefile``
        :type userPath:
            str
        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        try:
            self.g.GCommand("IA?")
            return True
        except gclib.GclibError:
            return False
