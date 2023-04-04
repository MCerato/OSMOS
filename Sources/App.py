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
import contextlib
import io
import time
import webbrowser
from threading import Thread

# importing tkinter and tkinter.ttk
# and all their functions and classes
import tkinter as tk
import tkinter.ttk as ttk

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askdirectory
# importing some widgets functions
# from class filedialog
from tkinter import scrolledtext

from OSMOS import OSMOS


class App:
    """Class representing the CSV file.

    :param userPath:
        where the CSV file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self):
        # In[1]: General setup
        self.project = "OSMOS"
        ProjectDir = os.path.dirname(__file__)

        while os.path.basename(ProjectDir) != self.project:
            ProjectDir = os.path.dirname(ProjectDir)

        self.CBFile = ProjectDir + "\\Documentation\\Reference"
        self.CBFile = self.CBFile + "\\OSM_LIST_CB.csv"
        self.CdeFile = ProjectDir + "\\Documentation\\Reference"
        self.CdeFile = self.CdeFile + "\\OSM_LIST_CDE.csv"

        self.bakDir = ProjectDir + "\\Sources"+"\\.bak\\"
        self.logDir = ProjectDir + "\\Sources"+"\\.log\\"

        self.osmos = OSMOS()
        self.seqRunning = False
        self.newContent = ""

    # In[1]: window setup
    # ============= ROOT ============
        self.root = tk.Tk()
        self.root.title("OSMOS")
        # self.root.geometry('1024x768')
        self.root.resizable(height=None, width=None)

    # In[1]: Menu bar setup
        self.menubar = tk.Menu(self.root)
        self.help_ = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.help_)
        self.help_.add_command(label="User Guide",
                               command = lambda:webbrowser.open(f"file://{self.__FindUserGuideFiles()}" ))
        self.help_.add_command(label="Developper Guide",
                               command = lambda:webbrowser.open(f"file://{self.__FindDevGuideFiles()}" ))
# In[1]: widget setup
# ============= SELECT CONFIG FILES FRAME ============
# *************
        selectFileFrame = ttk.LabelFrame(self.root, text='Select Config Files')
        selectFileFrame.grid(row=0, column=0, rowspan=2, pady=10, padx=10)

# *************
        self.filePathLbl = ttk.Label(selectFileFrame, text="CB File Path")
        self.filePathLbl.grid(row=0, column=0, pady=10, padx=10, sticky="W")

# *************
        self.FileNameLbl = ttk.Label(selectFileFrame, text="Command File Path")
        self.FileNameLbl.grid(row=1, column=0, pady=10, padx=10, sticky="W")

# *************
        self.openFileBtn = ttk.Button(selectFileFrame, text='import CB file',
                                      command=lambda: self.CBOpenFile())
        self.openFileBtn.grid(row=0, column=1, pady=10, padx=10)

# *************
        self.openFileBtn = ttk.Button(selectFileFrame,
                                      text='import Command file',
                                      command=lambda: self.CdeOpenFile())
        self.openFileBtn.grid(row=1, column=1, pady=10, padx=10)

# ============= SELECT .BAK .LOG DIRECTORIES FRAME ============
# *************
        selectDirFrame = ttk.LabelFrame(self.root, text='Select Directories')
        selectDirFrame.grid(row=0, column=1, rowspan=2, pady=10, padx=10)

# *************
        self.bakDirPathLbl = ttk.Label(selectDirFrame, text=".bak Path")
        self.bakDirPathLbl.grid(row=0, column=0, pady=10, padx=10, sticky="W")

# *************
        self.logDirLbl = ttk.Label(selectDirFrame, text=".log Path")
        self.logDirLbl.grid(row=1, column=0, pady=10, padx=10, sticky="W")

# *************
        self.openBakBtn = ttk.Button(selectDirFrame,
                                     text='import bak Directory',
                                     command=lambda: self.BakOpenDir())
        self.openBakBtn.grid(row=0, column=1, pady=10, padx=10)

# *************
        self.openLogBtn = ttk.Button(selectDirFrame,
                                     text='import log Directory',
                                     command=lambda: self.LogOpenDir())
        self.openLogBtn.grid(row=1, column=1, pady=10, padx=10)

# ============= CONFIGURATION FRAME ============
# *************
        configFrame = ttk.LabelFrame(self.root, text='Configuration')
        configFrame.grid(row=0, column=2, rowspan=2, pady=10, padx=10)

# *************
        self.ntwrkLbl = ttk.Label(configFrame, text="SOLEIL Network :")
        self.ntwrkLbl.grid(row=0, column=0, pady=10, padx=0, sticky="W")
# *************
        self.IPLbl = ttk.Label(configFrame, text="IP Address")
        self.IPLbl.grid(row=1, column=0, pady=10, padx=0, sticky="W")

# *************
        self.ntworksCbBx = ttk.Combobox(configFrame, text='networks',
                                        width=15, textvariable=tk.StringVar())
        self.ntworksCbBx.grid(row=0, column=1, pady=10, padx=10)

        # Adding combobox drop down list
        self.ntworksCbBx['values'] = (self.osmos.GetAllNetworks())
        last = self.osmos.GetAllNetworks()[-1]
        self.ntworksCbBx.current(self.osmos.GetAllNetworks().index(last))

# *************
        self.IPEntry = ttk.Entry(configFrame, text='User IP',
                                 width=15, textvariable=tk.StringVar())
        self.IPEntry.grid(row=1, column=1, pady=10, padx=10)

# ============= COMMANDS FRAME ============
# *************
        commandFrame = ttk.LabelFrame(self.root, text='Commands')
        commandFrame.grid(row=0, column=3, rowspan=2, pady=10, padx=10)

# *************
        self.startBtn = ttk.Button(commandFrame, text='Start',
                                   command=lambda: self.StartSeq())
        self.startBtn.grid(row=0, column=0, pady=10, padx=10)

# *************
        self.stopBtn = ttk.Button(commandFrame, text='Stop (WIP)',
                                  command=lambda: print("Stop"))
        self.stopBtn.grid(row=1, column=0, pady=10, padx=10)

# ============= OUTPUT FRAME ============
# *************
        outputFrame = ttk.LabelFrame(self.root, text='Output')
        outputFrame.grid(row=2, column=0, rowspan=2, columnspan=10, pady=10,
                         padx=10)

# *************
        self.outputTxt = scrolledtext.ScrolledText(outputFrame, height=10)
        self.outputTxt.grid(row=0, column=0, columnspan=10, pady=10, padx=10)
        self.outputTxt.configure(state='disabled')
        self.outputTxt.delete(0.0, tk.END)

# =========== PROGRESS FRAME ============
# *************
        progressFrame = ttk.LabelFrame(self.root, text='Sequence running')
        progressFrame.grid(row=6, column=0, rowspan=2, columnspan=4, pady=10,
                           padx=10, sticky="W")

# *************
        self.configProgress = ttk.Progressbar(progressFrame,
                                              orient=tk.HORIZONTAL,
                                              length=100, mode='indeterminate')
        self.configProgress.grid(row=0, column=0, rowspan=2, columnspan=4,
                                 pady=10, padx=10)

# In[1]: root Display
        self.root.config(menu=self.menubar)
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
    def BakOpenDir(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        self.bakUserDir = askdirectory()
        if self.bakUserDir:
            self.bakDir = self.bakUserDir + "/"
            print(f"new path : {self.bakUserDir} loaded")

# In[1]: Graphical File Manipulation (GUI Wrapper)
    def LogOpenDir(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        self.logUserDir = askdirectory()
        if self.logUserDir:
            self.logDir = self.logUserDir + "/"
            print(f"new path : {self.logUserDir} loaded")

# In[1]: Internal Methods
    def __FindUserGuideFiles(self):
        """Use to change the doc path according to the App run dir."""
        self.pathDocFiles = __file__
        self.pathDocFiles = self.pathDocFiles.replace("\\", "/")
        while os.path.basename(self.pathDocFiles) != self.project:
            self.pathDocFiles = os.path.dirname(self.pathDocFiles)

        self.pathDocFiles = self.pathDocFiles + "/Documentation/build/html/GuidesPages/UserGuide.html"
        return self.pathDocFiles

    def __FindDevGuideFiles(self):
        """Use to change the doc path according to the App run dir."""
        self.pathDocFiles = __file__
        self.pathDocFiles = self.pathDocFiles.replace("\\", "/")
        while os.path.basename(self.pathDocFiles) != self.project:
            self.pathDocFiles = os.path.dirname(self.pathDocFiles)

        self.pathDocFiles = self.pathDocFiles + "/Documentation/build/html/GuidesPages/DevGuide.html"
        return self.pathDocFiles

# In[1]: Graphical File Manipulation (GUI Wrapper)
    def StartSeq(self):
        """Take the empty lines off the column in the the file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """

        def __OsmSeq(self):
            """Take the empty lines off the column in the the file.

            :param contentToWrite:
                Line to read.
            :type contentToWrite:
                str, list

            .. warning::
                Works only on .CSV.
            """
            self.startBtn['state'] = tk.DISABLED
            self.seqRunning = True
            self.osmos.UpdateBakDir(self.bakDir)
            self.osmos.UpdateLogDir(self.logDir)
            self.osmos.UpdateCBFile(self.CBFile)
            self.osmos.UpdateCdeFile(self.CdeFile)
            # self.osmos = OSMOS(self.CBFile, self.CdeFile,
                               # self.bakDir, self.logDir)

            if self.IPEntry.get():
                self.osmos.OSMOSSeq(None, self.IPEntry.get())

            else:
                self.osmos.OSMOSSeq(self.ntworksCbBx.get(), None)

            self.seqRunning = False
            self.startBtn['state'] = tk.NORMAL

        def __DisplayPrint(self):
            """Take the empty lines off the column in the the file.

            :param contentToWrite:
                Line to read.
            :type contentToWrite:
                str, list

            .. warning::
                Works only on .CSV.
            """
            # os.system('cls' if os.name == 'nt' else 'clear\n')
            self.outputTxt.configure(state='normal')
            self.outputTxt.delete(0.0, tk.END)
            outputContainer = io.StringIO()
            self.seqRunning = True

            with contextlib.redirect_stdout(outputContainer):
                savedContent = outputContainer.getvalue()
                self.outputTxt.insert(tk.END, outputContainer.getvalue())

                while self.seqRunning:
                    if savedContent != outputContainer.getvalue():
                        oldContent = outputContainer.getvalue()
                        self.newContent = oldContent.replace(savedContent, "")
                        savedContent = outputContainer.getvalue()

                        self.outputTxt.insert(tk.END, self.newContent)
                        self.outputTxt.yview(tk.END)

                    time.sleep(0.05)
            self.outputTxt.configure(state='disabled')

        def __ProgressBar(self):
            """Take the empty lines off the column in the the file.

                Line to read.
            :type contentToWrite:
                str, list

            .. warning::
                Works only on .CSV.
            """
            iSave = 0
            i = iSave
            self.seqRunning = True
            progressSpeed = self.configProgress['length']/20
            self.configProgress['value'] = 0
            while self.seqRunning:
                if iSave == 0:
                    i += 1
                    self.configProgress['value'] = i*progressSpeed
                    if i > 99:
                        iSave == 1
                else:
                    i -= 1
                    self.configProgress['value'] = i*progressSpeed
                    if i < 1:
                        iSave == 0
                time.sleep(0.05)
            self.configProgress['value'] = 0

        Thread(target=__DisplayPrint, args=(self,)).start()
        Thread(target=__OsmSeq, args=(self,)).start()
        Thread(target=__ProgressBar, args=(self,)).start()

# In[1]: Graphical File Manipulation (GUI Wrapper)


if __name__ == '__main__':
    App()
