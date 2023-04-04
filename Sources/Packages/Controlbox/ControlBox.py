# -*- coding: utf-8 -*-
"""Wrap the GALIL gclib library.

Description
-----------
Allow to connect and communicate with a specific GALIL board.
The board is identified through its IP address.

.. warning::
    The IP address of the board has to be fixed previously.
    (parameter DH should be 0)


Libraries/Modules
-----------------
- gclib library (https://www.galil.com/sw/pub/all/doc/gclib/html/python.html)
    - provided by GALIL to communicate with ther product

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
from Packages.Controlbox import gclib


class ControlBox:
    """Class representing the device to connect or connected to.

    :attr g:
        g is the object wich represent a connection.
    :type g:
        gclib
    """

    def __init__(self):
        self.g = gclib.py()

    def __del__(self):
        """Close connection.

        .. note::
            If previously connected, close connection before delete
        """
        if self.__IsConnected():
            self.Disconnect()

    def Connect(self, ip):
        """Connect to a ControlBox.

        :param ip:
            should be a standard IP addresse (ex : 172.20.24.65)
        :type ip:
            str
        :return:
            Return the **connection** State.
        :rtype:
            Bool
        """
        try:
            self.g.GOpen(ip)
            print(f"connected to {ip}")
            return True
        except gclib.GclibError:
            print(f"couldn't connect to {ip}")
            return False

    def Disconnect(self):
        """Disconnect from a ControlBox.

        :return:
            Return the **disconnection** State.
        :rtype:
            bool
        """
        try:
            # close UDP and TCP if used of surrent connection (not others)
            self.g.GCommand("IHS =>-3")
            print("Disconnection failed")
            return False

        except gclib.GclibError:
            self.g.GClose()
            print("Disconnected")
            return True

    def Reset(self):
        """Restart the Controller (ControlBox).

        .. warning::
            This function is disabled for now (need to create a timeout)
        """
# =============================================================================
#         if self.__IsConnected() is True:
#             savedIP = self.GetIp()
#             self.g.GCommand("RS")
#             # try to connect until it does connect or timeout
#             self.g.Connect(savedIP)
# =============================================================================
        pass

    def GetMicrocode(self):
        r"""Return the microcode from the controller.

        :return:
            Return the entire microcode with special characters
        :rtype:
            str

        .. note::
            displays the carriage return + line feed as ``\n``
        """
        if self.__IsConnected() is True:
            return self.g.GProgramUpload()

    def SetMicrocode(self, code):
        """Download the microcode into the controller."""
        if self.__IsConnected() is True:
            self.g.GProgramDownload(code)

    def GetVariable(self, galilVar):
        """Get the value of a variable.

        :param galilVar:
            should be an existing variable of galil script (ex : McRevSpe)
        :type galilVar:
            str
        :return:
            the value
        :rtype:
            str

        .. warning::
            If the variable doesn't exist, the controller create the variable
            and gives a zero value.
        """
        if self.__IsConnected() is True:
            return self.g.GCommand(galilVar + "=?")

    def GetAllVariables(self):
        """Get the value of all variables.

        :return:
            a list of all variables name and their value
        :rtype:
            list
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
        """
        if self.__IsConnected() is True:
            rawArrays = self.g.GCommand("LA")
            arrays = rawArrays.split("\r\n")
            return arrays

    def GetParameter(self, command):
        """Return the value of a parameter.

        :param command:
            should be an existing parameter coupled to his axis if necessary.
            (ex : SPA=?, IA ? or MG_CN0)
        :type command:
            str
        :return:
            The result from the ControlBox
        :rtype:
            str
        """
        if self.__IsConnected() is True:
            if command[-1:] == "?":
                return self.g.GCommand(command)

            elif command[:3] == "MG_":
                return self.g.GCommand(command)

            else:
                print(f"the command {command} is not a query")

    def SetParameter(self, command):
        """Return the value of a parameter.

        :param command:
            should be an existing parameter coupled to his axis if necessary.
            (ex : SPA=value, IA value)
        :type command:
            str
        """
        if self.__IsConnected() is True:
            self.g.GCommand(command)

    def GetIp(self):
        """Get the IP of the controller. If not connected, return None.

        :return:
            Return the IP in GALIL format
        :rtype:
            str, None

        .. note::
            Separator at GALIL is ``,`` so it should return something like:
            ``xxxx, xxxx, xxxx, xxxx``
        """
        if self.__IsConnected() is True:
            return self.g.GCommand("IA?")
        else:
            return None

    def GetFWVersion(self):
        """Return the Firmware of the product.

        :return:
            Return the Firmware of the controller. (ex : DMC4183s56b-SER)
        :rtype:
            str
        """
        if self.__IsConnected() is True:
            return self.g.GInfo().split(", ")[1]

    def GetSerial(self):
        """Get the serial number of the product.

        :return:
            Return the S.N of the controller. (ex : 15953.0000)
        :rtype:
            str
        """
        if self.__IsConnected() is True:
            return self.g.GInfo().split(", ")[2] + ".0000"

    def __IsConnected(self):
        """Control the connexion State.

        :return:
            ``True`` if the soft is connected to the controller
            ``False`` otherwise
        :rtype:
            bool
        """
        try:
            self.g.GCommand("IA?")
            return True
        except gclib.GclibError:
            return False


if __name__ == '__main__':
    cb = ControlBox()  # instance of ControlBox
    print(cb.Connect("172.16.3.65"))  # connect to an existing controlbox
    print(cb.GetIp())  # ask for anything
    print(cb.Disconnect())
    print(cb.Connect("172.16.3.88"))  # connect to an non existing controlbox
