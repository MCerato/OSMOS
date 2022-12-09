# -*- coding: utf-8 -*-
"""Manage the bank file.

Description
-----------
Object from wich you can manage the file you're using in your BankApp.
For instance, create a file, rename it etc...

You can also get (read) the content and save a new content into it.

.. warning::
    You can't manipulate datas directly from/to the file.
    It is recommended to export the content of the file for treatment as
    a list of strings wich is easier to manipulate in python.

Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.

Version
-------
- 1.0.0.0

Notes
-----
- None.

TODO
----
- None.

Author(s)
---------
- Created by M. Cerato on 06/17/2022.
- Modified by xxx on xx/xx/xxxx.

Copyright (c) 2020 Cerato Workshop.  All rights reserved.

Members
-------
"""

# In[1]: imports

import os

# importing tkinter and tkinter.ttk
# and all their functions and classes
from tkinter import * 
from tkinter.ttk import *
  
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askdirectory
from tkinter import messagebox

from OSMOS import OSMOS

class App:
  
    def __init__(self):

# In[1]: General setup
        self.CBFile=os.path.dirname(__file__)+"\\OSM_LIST_CB.csv"
        self.CdeFile=os.path.dirname(__file__)+"\\OSM_LIST_CDE2.csv"
        self.osmos=OSMOS(self.CBFile, self.CdeFile)

# In[1]: root setup       
        self.root = Tk()
        self.root.title("OSMOS")
        # self.root.geometry('1024x768')
        self.root.resizable(height = None, width = None)

# In[1]: Menu bar setup  
        self.menubar = Menu(self.root)
        self.help_ = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label ='Help', menu = self.help_)
        self.help_.add_command(label = "User Guide", 
                               command = lambda:webbrowser.open(f"file://{self._FindLocalDocFiles()}" ))

# In[1]: widget setup
# ============= ROOT ============
# *************       
        self.WelcomeBtn = Button(self.root, text ='Hello', 
                            command=lambda:print("welcome!"))
        self.WelcomeBtn.grid(row = 0, column = 0, padx = 20)

# ============= SELECT FILES FRAME ============
# *************
        selectFileFrame = LabelFrame(self.root, text ='Infos')
        selectFileFrame.grid(row = 0, column = 1, rowspan = 2, pady = 10, 
                             padx = 10)

# *************
        self.lblFilePath = Label(selectFileFrame,
                              text = "CB File Path")
        self.lblFilePath.grid(row = 0, column = 0, pady = 10, padx = 10,
                              sticky = "W")

# *************
        self.lblFileName = Label(selectFileFrame,
                              text = "Command File Path")
        self.lblFileName.grid(row = 1, column = 0, pady = 10, padx = 10, sticky = "W")
# *************
        self.openFileBtn = Button(selectFileFrame, text ='import CB file', 
                             command=lambda:self.CBOpenFile())
        self.openFileBtn.grid(row = 0, column = 1, pady = 10, padx = 10)

# *************
        self.openFileBtn = Button(selectFileFrame, text ='import Command file', 
                             command=lambda:self.CdeOpenFile())
        self.openFileBtn.grid(row = 1, column = 1, pady = 10, padx = 10)

# *************

# ============= Configuration FRAME ============
# *************
        ConfigFrame = LabelFrame(self.root, text ='Configuration')
        ConfigFrame.grid(row = 0, column = 2, rowspan = 2, pady = 10,
                          padx = 10)

# *************
        self.lblNtwrk = Label(ConfigFrame,
                              text = "SOLEIL Network :")
        self.lblNtwrk.grid(row = 0, column = 0, pady = 10, padx = 0, 
                           sticky = "W")
# *************
        self.lblNtwrk = Label(ConfigFrame,
                              text = "IP Address")
        self.lblNtwrk.grid(row = 1, column = 0, pady = 10, padx = 0, 
                           sticky = "W")

# *************
        self.ntworksCbBx = Combobox(ConfigFrame, text ='networks',
                                    width = 15, textvariable = StringVar())         
        self.ntworksCbBx.grid(row = 0, column = 1, pady = 10, padx = 10)
        # Adding combobox drop down list
        self.ntworksCbBx['values'] = (self.osmos.GetAllNetworks())

# *************
        self.IPEntry = Entry(ConfigFrame, text ='User IP',
                                    width = 15, textvariable = StringVar())         
        self.IPEntry.grid(row = 1, column = 1, pady = 10, padx = 10)

# ============= COMMANDS FRAME ============
# *************
        CommandFrame = LabelFrame(self.root, text ='Commands')
        CommandFrame.grid(row = 0, column = 3, rowspan = 2, pady = 10,
                          padx = 10)

# *************
        self.StartBtn = Button(CommandFrame, text ='Start', 
                            command=lambda:self.Start())
        self.StartBtn.grid(row = 0, column = 0, pady = 10, padx = 10)

# *************
        self.StopBtn = Button(CommandFrame, text ='Stop', 
                            command=lambda:print("Stop"))
        self.StopBtn.grid(row = 1, column = 0, pady = 10, padx = 10)

# =============================================================================
# # *************
#         name_var=tk.StringVar()
#         IPEntry = Entry(CommandFrame,
#                         textvariable = name_var, font=('calibre',10,'normal'))
# =============================================================================
# In[1]: root Display
        self.root.config(menu = self.menubar)
        self.ntworksCbBx.current(30) 
        # Button(self.root, text="Quit", command=self.root.destroy).pack()
        self.root.mainloop()

# In[1]: Graphical File Manipulation (GUI Wrapper)    
    def CBOpenFile(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        self.CBUserFile = askopenfile(mode='r',
                                    filetypes=[('CSV Files', '*.csv'),
                                               ('Text Files', '*.txt'),
                                               ('Python Files', '*.py'),
                                               ('PDF Files', '*.pdf')])
        if self.CBUserFile:
            self.CBFile = self.CBUserFile.name
            print(f"{self.CBUserFile.name} loaded")

# In[1]: Graphical File Manipulation (GUI Wrapper)    
    def CdeOpenFile(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        self.CdeUserFile = askopenfile(mode='r',
                                    filetypes=[('CSV Files', '*.csv'),
                                               ('Text Files', '*.txt'),
                                               ('Python Files', '*.py'),
                                               ('PDF Files', '*.pdf')])
        if self.CdeUserFile:
            self.CdeFile = self.CdeUserFile.name
            print(f"{self.CdeUserFile.name} loaded")


# In[1]: Graphical File Manipulation (GUI Wrapper)    
    def Start(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        self.osmos = OSMOS(self.CBFile, self.CdeFile)
        if self.IPEntry.get():        
            self.osmos.OSMOSSeq(None, self.IPEntry.get())
        else:
            self.osmos.OSMOSSeq(self.ntworksCbBx.get(), None)           

# In[1]: Graphical File Manipulation (GUI Wrapper)    
    def Test(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """


        print(self.ntworksCbBx.get())

if __name__ == '__main__':      
    App()