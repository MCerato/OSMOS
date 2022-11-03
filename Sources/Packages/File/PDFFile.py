# -*- coding: utf-8 -*-
"""Manage the PDF file.

Description
-----------
Object inherited from FileWrapper class and containing specific method
to extract Data.

unlike FileWrapper, this Class has to be associated with a file wich has
``.pdf`` format

You can also get (read) the content.

.. warning::
    You can't manipulate datas directly from/to the file.
    It is recommended to export the content of the file for treatment as
    a list of strings wich is easier to manipulate in python.

This file has largely been inspired by this tutorial:
https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/

Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.
- PyPDF2 library (https://pypdf2.readthedocs.io/en/latest/)
    - Access to PDF Manipulation functions.
- FileWrapper library (:file:FileWrapper.html)
    - Access to files function.

Version
-------
- 1.0.0.0

Notes
-----
This suggest that the PDF file has been build correctly and, is not a
picture of a file.

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
from PyPDF2 import PdfFileReader
from File import FileWrapper as fw


class PDF(fw.File):
    # In[1]: constructor & destructor
    """Class representing the PDF file.

    :param userPath:
        where the PDF file is.
        Path should be, preferably, absolute with format :
        ``C:/file1/file2/sourcefile``
    :type userPath:
        str
    """

    def __init__(self, userPath):
        """Instanciate class onto object."""
        fw.File.__init__(self)
        self.CreateFile(userPath)  # link the PDF to the object

        if self.GetFileFormat() != ".pdf":
            print("wrong file format")
            print(f"This is a {self.GetFileFormat()}")
            print("")

    def __del__(self):
        """Destroying object.

        Mainly used to close file in case something went wrong
        """
        print(f"object {self} deleted")

    def __repr__(self):
        """Display the object of the file."""
        return f"pdf file : {self.GetFileName()}"

# In[3]: Content of the file
    def GetAllContent(self):
        """Read the entire file.

        :return:
            Return the entire content of the file as one big string
        :rtype:
            str

        .. note::
            Should displays the carriage return + line feed
        """
        if self.GetFileFormat() == ".pdf":
            return self.__RawTextExtraction()
        else:
            return None

    def GetLinesContent(self):
        """Read the entire file.

        :return:
            Return the entire content of the file line by line
        :rtype:
            str

        .. note::
            displays the carriage return + line feed
        """
        if self.GetFileFormat() == ".pdf":
            return self.__RawTextExtraction().splitlines()
        else:
            return None

    def GetLineContent(self, line):
        """Read a specific line of the file.

        .. note::
            line start at 1

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
        if self.GetFileFormat() == ".pdf":
            if line > 0 and line <= len(self.GetLinesContent()):
                return self.__RawTextExtraction().splitlines()[line-1]
            else:
                print("line doesn't exist")
        else:
            return None

    def GetMetaPDF(self):
        """Return the MetaDatas of the file such as Author or date of creation.

        :return:
            Return a dictionnary containing the keys :
                - /Title
                - /Author
                - /Subject
                - /Producer
                - /CreationDate (format:yyyymmddhhmmss)
        :rtype:
            dict


        """
        if self.GetFileFormat() == ".pdf":
            with open(os.path.join(self.GetFilePath(),
                                   self.GetFileName()), 'rb') as file:
                pdf = PdfFileReader(file)
                meta = pdf.getDocumentInfo()
            return meta
        else:
            return None

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

    def __RawTextExtraction(self):
        """(local method) Prepare and extract datas from PDF.

        :return:
            Return ``True`` or ``False``
        :rtype:
            bool
        """
        text = ""
        with open(os.path.join(self.GetFilePath(),
                               self.GetFileName()), 'rb') as file:
            pdf = PdfFileReader(file)
            # get the first page
            for pageNumber in range(pdf.numPages):
                page = pdf.getPage(pageNumber)
                # print(page)
                # print('Page type: {}'.format(str(type(page))))
                text += page.extractText()

            return text
