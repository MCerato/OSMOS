# -*- coding: utf-8 -*-
"""Manage the CSV file.

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


class CSV(fw.File):
    # In[1]: constructor & destructor
    """Class representing the CSV file.

    :param userPath:
        where the CSV file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self, userPath):
        fw.File.__init__(self)

        self.CreateFile(userPath)

        if self.GetFileFormat() != ".csv":
            print("wrong file format")
            print(f"This is a {self.GetFileFormat()}")
            print("")

    def __del__(self):
        """Destroying object.

        Mainly used to close file in case something went wrong
        """
        # print(f"object {self} deleted")

    def __repr__(self):
        """Display the object of the file."""
        return f"csv file : {self.GetFileName()}"

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
        content = ""
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(), self.GetFileName()),
                      mode='r', encoding="utf-8") as file:
                for line in file.readlines():
                    content += line
            return content
        else:
            return None

    def GetLinesContent(self):
        """Return the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='r', encoding="utf-8") as file:
                content = file.readlines()
            return content
        else:
            return None

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
        if self.GetFileFormat() == ".csv":
            if line > 0 and line <= len(self.GetLinesContent()):

                with open(os.path.join(self.GetFilePath(),
                                       self.GetFileName()),
                          mode='r', encoding="utf-8") as file:
                    for i in range(line):
                        content = file.readline()
                return content
            else:
                print("line doesn't exist")
        else:
            return None

    def AddContent(self, contentToWrite):
        """Append content into a txt file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list
        """
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='a', encoding="utf-8") as file:
                if contentToWrite[len(contentToWrite)-1:] == "\n":
                    file.writelines(contentToWrite)
                else:
                    file.writelines(contentToWrite + "\n")

    def ReplaceContent(self, contentToWrite):
        """Erase previous content and write new content into a txt file.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list
        """
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='w', encoding="utf-8") as file:
                file.writelines(contentToWrite)

    def EraseContent(self):
        """Erase content of a txt file."""
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='w', encoding="utf-8") as file:
                file.writelines("")

    def GetColumnDatas(self):
        """Extract Datas as colomn in a dictionnary form.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        for example:
        =========================== ================================
        Header1                     Header 2
        =========================== ================================
        Data11                      Data21
        Data12                      Data22
        =========================== ================================

        It gives a dictionnary as :
        dic = {Header1:[Data11, Data12], Header2:[Data21, Data22]}

        .. warning::
            Worksd only on .CSV. As said, separators HAVE TO be ";"
        """
        columnSortedDict = {}
        if self.GetFileFormat() == ".csv":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()),
                      mode='r', encoding="utf-8") as file:
                contentFile = file.readlines()
                header = contentFile[0]
                corpus = contentFile[1:]

                for index, text in enumerate(header.split(";")):
                    listValues = []
                    for val in corpus:
                        listValues.append(val.split(";")[index])
                    columnSortedDict[text] = listValues

        return columnSortedDict

    def ChangeSep(self, oldSepFormat, newSepFormat):
        """Extract Datas as colomn in a dictionnary form.

        :param contentToWrite:
            Line to read.
        :type contentToWrite:
            str, list

        .. warning::
            Works only on .CSV.
        """
        newContent = []
        if self.GetFileFormat() == ".csv":
            oldContent = self.GetLinesContent()

            for line in oldContent:
                modifLine = line.replace(oldSepFormat, newSepFormat)
                newContent.append(modifLine)

            self.ReplaceContent(newContent)

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

if __name__ == '__main__':
    csvf = CSV("D:/Temp_pro/OSMOS/Sources/OSM_LIST_CDE.csv")
    plop = csvf.GetColumnDatas()