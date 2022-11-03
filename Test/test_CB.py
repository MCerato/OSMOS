# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 12:41:05 2022

@author: CERATO
"""

# connect :
#     - modifier l'adresse ip
#     - récupérer l'adresse ip

import os
import sys
from Controlbox import ControlBox
from File import CSVFile
import pytest

class Test_CB:

    wrongIP = "172.16.3.800"
    validIP = "172.16.3.65"
    CB = ControlBox.ControlBox()

# =============================================================================
#     def setup_method(self):
#         self.CB.Connect(self.validIP)
# =============================================================================

    def test_connection_nok(self):
        assert self.CB.Connect(self.wrongIP) is False

    def test_connection_ok(self):
        assert self.CB.Connect(self.validIP) is True

    def test_GetMicrocode(self):
        self.CB.Connect(self.validIP)
        assert isinstance(self.CB.GetMicrocode(), str) is True

    def test_GetVariable(self):
        self.CB.Connect(self.validIP)
        assert self.CB.GetVariable("Cmd[0]") == "0.0000"

    def test_GetParameter(self):
        self.CB.Connect(self.validIP)
        assert self.CB.GetParameter("IA?") == "172, 16, 3, 65"

    def test_setParameter(self):
        self.CB.Connect(self.validIP)
        value = self.CB.GetParameter("CEA=?")
        print(value)
        self.CB.SetParameter("CEA=4")
        assert self.CB.GetParameter("CEA=?") == "4"      
        self.CB.SetParameter("CEA=6")
        assert self.CB.GetParameter("CEA=?") == "6"
        self.CB.SetParameter("CEA=" + value)
        
    def test_GetCBVersion(self):
        print(self.CB.GetCBVersion())
        assert self.CB.GetCBVersion() == "DMC4183s56g"
        