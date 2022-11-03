# -*- coding: utf-8 -*-
"""Manage the file.

Description
-----------
Object from wich you can manage a file.
For instance, create a file, rename it etc...

.. note::
    This file doesn't manage **the content** of the file.
    To do this, we recommend using PDFFile, TXTFile or CSVFile wich gives
    access to specific methods.

.. warning::
    You can't manipulate datas directly from/to the file.
    It is recommended to export the content of the file for treatment as
    a list of strings wich is easier to manipulate in python.

Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    Access to files function.

Version
-------
- 0.0.0.1

Notes
-----
- Repository : https://github.com/MCerato/FileManagement

TODO
----
- None.

Author(s)
---------
- Created by M. Cerato on 09/25/2022.
- Modified by xxx on xx/xx/xxxx.

Copyright (c) 2020 Cerato Workshop.  All rights reserved.

Members
-------
- M. cerato
"""


# In[1]: imports
import os


class File:
    # In[1]: constructor & destructor

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
        """Instanciate class onto object."""
        
        self._path = None
        self._name = None
        self._size = None
        self._fileFormat = None
        print(f"creation of the File object associated with {self}")

    def __del__(self):
        """Destroying object.

        Mainly used to close file in case something went wrong
        """
        print(f"{self} deleted")

    def __repr__(self):
        """Display the object of the file."""
        if self.__IsAFileSelected():
            return f"{self.GetFileName()}, situated at {self.GetFilePath()}"
        else:
            return "No file selected"
            
        
# In[2]: Associate a file to object
    def CreateFile(self, userPath):
        """Create a new file. Select one if already exsiting.

        :param userPath:
            path to the file.
        :type userPath:
            str
        :return:
            the path and the name of the file
        :rtype:
            str, str.
        """
        try:
            with open(userPath, encoding="utf-8", mode="x"):              
                self.__UpdtFileInfos(userPath)
            return self.GetFilePath(), self.GetFileName()

        except FileExistsError:
            print("File already exists, file selected")
            print("")
            self.SelectFile(userPath)

        except FileNotFoundError:
            pass
        
        except PermissionError:
            print("File seems open somewhere else")

    def SelectFile(self, userPath):
        """Select an existing file
        
        :param userPath:
            path to the file.
        :type userPath:
            str
        :return:
            the path and the name of the file
        :rtype:
            str, str
        """
        if self.__DoesFileExist(userPath):
            try:
                with open(userPath, encoding="utf-8", mode="a"):
                    self.__UpdtFileInfos(userPath)            
                return self.GetFilePath(), self.GetFileName()

            except PermissionError:
                print("File seems open somewhere else")   
        else:
            print("This file doesn't exist")


# In[2]: Manipulate file
    def DeleteFile(self):
        """Delete the file pointed by the object.

        .. note::
            object is not associated with a file anymore.
            A new one has to be selected or created.
        """
        if self.__IsAFileSelected():
            print(self._name)
            os.remove(os.path.join(self.GetFilePath(), self.GetFileName()))
            self._path = None
            self._name = None
            self._size = None
            self._fileFormat = None

        print("file deleted")            

    def RenameFile(self, newName):
        """Rename the file pointed by the object.

        .. note::
            return None if no file selected
        
        :param newName:
            New name of the file.
        :type newName:
            str

        .. note::
            Change the name only if no file of this name exists
            
        .. warning::
            don't foget extention'
        """
        if self.__IsAFileSelected():
            
            try:
                os.rename(os.path.join(self.GetFilePath(), 
                                       self.GetFileName()),
                          os.path.join(self.GetFilePath(), 
                                       newName))
            except FileExistsError:
                print("This file already exists")

            self._name = newName
            
    def MoveFile(self, newPath):
        """Change the directory of the file

        :param newPath:
            New path of the file.
        :type newPath:
            str

        .. note::
            Move the file only if no other file of this name exists

        """
        if self.__IsAFileSelected():
            
            try:
                os.rename(os.path.join(self.GetFilePath(), 
                                       self.GetFileName()),
                          os.path.join(newPath, 
                                       self.GetFileName()))
            except FileExistsError:
                print("This file already exists")

            self._path = newPath
# In[4]: functions for file manipulation
    def GetFileSize(self):
        """Ask for the size of the file.

        .. note::
            return None if no file selected

        :return:
            The size of the file in Bytes
        :rtype:
            int
        """
        if self.__IsAFileSelected():
            return os.path.getsize(os.path.join(self.GetFilePath(),
                                                self.GetFileName()))

    def GetFileFormat(self):
        """Ask for the extention of the file.

        .. note::
            return None if no file selected

        :return:
            The extention of the file. For instance ``.txt``, ``.py``, ``.pdf``
        :rtype:
            str
        """
        if self.__IsAFileSelected():

            for inc, char in enumerate(os.path.join(self.GetFilePath(),
                                                    self.GetFileName())):
                if char == ".":
                    ext = os.path.join(self.GetFilePath(),
                                       self.GetFileName())[inc:]
            return ext

    def GetFilePath(self):
        """Ask for Path of the file

        .. note::
            return None if no file selected

        :return:
            absolute path containing the file (without file name)
        :rtype:
            str
        """
        if self.__IsAFileSelected():
            return self._path
        else:
            return None

    def GetFileName(self):
        """Name of the file pointed by the object.

        .. note::
            return None if no file selected

        :return:
             full name of the file if it exists (with extension)
             None if it doesn't exist
        :rtype:
            str or None
        """
        if self.__IsAFileSelected():
            return self._name
    
        else:
            return None

# In[4]: internal functions for file itself
    def __IsAFileSelected(self):
        """(local method) check if a file is associated with the object.

        :return:
            Return ``True`` or ``False``
        :rtype:
            bool
        """

        if self._path and self._name:
            return True
        else:
            return False

    def __DoesFileExist(self, userPath):
        """(local method) check if the file exists.

        :return:
            Return ``True`` or ``False``
        :rtype:
            bool
        """

        if os.path.exists(userPath):
            return True

        else:
            print("")
            print("The file you looking for doesn't exist")
            return False

    def __IsFileEmpty(self):
        """(local method) check if the file is empty.

        :return:
            Return ``True`` or ``False``.
        :rtype:
            bool
        """
        if self.__DoesFileExist() is True:
            if self.GetFileSize() != 0:
                isEmpty = False
            else:
                isEmpty = True
            return isEmpty

    def __UpdtFileInfos(self, userPath):
        """(local method) Get all Informations of the file."""
        self._path, self._name = os.path.split(userPath)
        self._size = self.GetFileSize()
        self._fileFormat = self.GetFileFormat()
        

# In[6]: Class properties

    path = property(GetFilePath)
    name = property(GetFileName)
    size = property(GetFileSize)
    fileFormat = property(GetFileFormat)