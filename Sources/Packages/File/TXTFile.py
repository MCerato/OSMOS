# -*- coding: utf-8 -*-
"""Manage the PDF file.

Description
-----------
Object inherited from FileWrapper class and containing specific method
to extract Data.

unlike FileWrapper, this Class has to be associated with a file wich has
``.txt`` format

You can also get (read) the content and write, erase or replace a content.

.. warning::
    It is not recommended to manipulate datas directly from/to the file.
    It is recommended to import the content of the file for treatment as
    a list of strings wich is easier to manipulate in python and then
    write it back to the file.

Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.
- FileWrapper library (:file:FileWrapper.html)
    - Access to files function.

Version
-------
- 1.0.0.0

Notes
-----
- None

TODO
----
- None.

Author(s)
---------
- Created by M. Cerato on 10/04/2022.
- Modified by xxx on xx/xx/xxxx.

Copyright (c) 2020 Cerato Workshop.  All rights reserved.

Members
-------
- M. Cerato
"""

# In[1]: imports
import os
from Packages.File import FileWrapper as fw


class TXT(fw.File):
    # In[1]: constructor & destructor
    """Class representing the TXT file.

    :param userPath:
        where the TXT file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self, userPath):
        fw.File.__init__(self)

        self.CreateFile(userPath)  # link the file to the object

        if self.GetFileFormat() != ".txt":
            print("Warning : ")
            print(f"This is a {self.GetFileFormat()}")
            print("")

    def __del__(self):
        """Destroying object.

        Mainly used to close file in case something went wrong
        """
        # print(f"{self} deleted")

    def __repr__(self):
        """Display the object of the file."""
        return f"txt file : {self.GetFileName()}"

# In[3]: Content of the file
    def GetAllContent(self):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """

        with open(os.path.join(self.GetFilePath(), self.GetFileName()),
                  mode='r', encoding="utf-8") as file:
            try:
                content = file.read()

            except Exception as ex:
                print("content unreadable")
                print("May be a wrong format")
                return None
            
        return content


    def GetLinesContent(self):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        with open(os.path.join(self.GetFilePath(),
                               self.GetFileName()),
                  mode='r', encoding="utf-8") as file:
            try:
                content = file.readlines()
            except Exception as ex:
                print("content unreadable")
                print("May be a wrong format")
                return None
                
        return content


    def GetLineContent(self, line):
        """Give the specific line of the file.

        :param line:
            Line to read.
        :type line:
            int
        :return:
            Return the line as a string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed

        .. note::
            return an empty string if the line is out of bound or empty.
        """
        if line > 0 and line <= len(self.GetLinesContent()):

            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='r', encoding="utf-8") as file:
                for i in range(line):
                    try:
                        content = file.readline()
                    except Exception as ex:
                        print("content unreadable")
                        print("May be a wrong format")
                        return None
                    
                return content
        else:
            print("line doesn't exist")

    def AddContent(self, contentToWrite):
        """Append content into a txt file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list
        """
        with open(os.path.join(self.GetFilePath(),
                               self.GetFileName()),
                  mode='a', encoding="utf-8") as file:
            try:
                if contentToWrite[len(contentToWrite)-1:] == "\n":
                    file.writelines(contentToWrite)

                else:
                    file.writelines(contentToWrite + "\n")

            except Exception as ex:
                print("content nonwritable")
                print("May be a wrong format")

    def ReplaceContent(self, contentToWrite):
        """Erase previous content and write new content into a txt file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list
        """
        with open(os.path.join(self.GetFilePath(),
                               self.GetFileName()),
                  mode='w', encoding="utf-8") as file:
            try:
                file.writelines(contentToWrite)

            except Exception as ex:
                print("content non writable")
                print("May be a wrong format")

    def EraseContent(self):
        """Erase content of a txt file."""
        with open(os.path.join(self.GetFilePath(),
                               self.GetFileName()),
                  mode='w', encoding="utf-8") as file:
            try:
                file.writelines("")
            except Exception as ex:
                print("content can't be erased/ write")
                print("May be a wrong format")

# In[5]: internal functions for file content itself
    def __IsFileEmpty(self):
        """(local method) check if the file is empty.

        :return:
            Return ``True`` or ``False``
        :rtype:
            bool
        """
        if self.GetFileSize() != 0:
            isEmpty = False
        else:
            isEmpty = True
        return isEmpty
