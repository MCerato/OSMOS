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

# connect :
#     - modifier l'adresse ip
#     - récupérer l'adresse ip

from Controlbox import ControlBox
import pytest


class Test_CB:
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
    wrongIP = "172.16.3.800"
    validIP = "172.16.3.65"
    CB = ControlBox.ControlBox()

# =============================================================================
#     def setup_method(self):
#         self.CB.Connect(self.validIP)
# =============================================================================

    def test_connection_nok(self):
        assert self.CB.Connect(self.wrongIP) is False
        self.CB.Disconnect()

    def test_connection_ok(self):
        assert self.CB.Connect(self.validIP) is True
        self.CB.Disconnect()

    def test_Disconnect(self):
        assert self.CB.Disconnect() is True

    def test_GetMicrocode(self):
        self.CB.Connect(self.validIP)
        assert isinstance(self.CB.GetMicrocode(), str) is True
        self.CB.Disconnect()

    def test_GetVariable(self):
        self.CB.Connect(self.validIP)
        assert self.CB.GetVariable("Cmd[0]") == "0.0000"
        self.CB.Disconnect()

    def test_GetParameter(self):
        self.CB.Connect(self.validIP)
        assert self.CB.GetParameter("IA?") == "172, 16, 3, 65"
        self.CB.Disconnect()

    def test_setParameter(self):
        self.CB.Connect(self.validIP)
        value = self.CB.GetParameter("CEA=?")
        self.CB.SetParameter("CEA=4")
        assert self.CB.GetParameter("CEA=?") == "4"
        self.CB.SetParameter("CEA=6")
        assert self.CB.GetParameter("CEA=?") == "6"
        self.CB.SetParameter("CEA=" + value)
        self.CB.Disconnect()

    def test_GetFWVersion(self):
        self.CB.Connect(self.validIP)
        print(self.CB.GetFWVersion())
        assert self.CB.GetFWVersion() == "DMC4183s56g"
        self.CB.Disconnect()

    def test_GetSerial(self):
        self.CB.Connect(self.validIP)
        print(self.CB.GetSerial())
        assert self.CB.GetSerial() == "15953.0000"
        self.CB.Disconnect()