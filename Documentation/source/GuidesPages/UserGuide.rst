OSMOS UserGuide (WIP)
==============================

WELCOME HERE! This documentation intend to show you how to use the OSMOS software 

Description
-----------

OSMOS is a tool wich can communicate with the GALIL controllers of SOLEIL, 
extract the parameters/variables/microcode and write the into a ``.bak`` file

This file is parsed according to GALIL format allowing to upload those settings
into the controller

A ``.log`` file is generated indicatig if everything went right during the download

The user can configure the software through 2 ``.csv`` files wich are described below

Software presentation
---------------------

How FileManagement has been designed is represented by the software architecture below:

.. image:: ./software_architecture.PNG

Select the configuration Files
------------------------------

It exists 2 type of connections to a Powerbrick. You can connect through the "maintenance port".
This ethernet port exists on every PowerBrick and always has the same adress.

The other way allows you to enter an IP adress manually.

.. attention:: Be careful on wich you are able to connect or not.
	The software doesn't check what device is on the network. He is pretty simple.

=========================== ================================
IP Adress Type              Description                     
=========================== ================================
Default IP Adress           Maintenance Adress 172.168.0.200
Custom IP adress            any Standard PBR adress
=========================== ================================

Select where the files will be saved
------------------------------------

The Download feature allows you to extract setups (in folders form or in files form) of a Power Birck. 
You'll have to select what setup you want to download. It goes from "usrflash" for the most recent parameters
to "usrflash.5" for the oldest.

.. note:: Choosing a path to download is not implemented yet. The files downloaded are put where the script is run.

You can then, press on the green button *"Download"*.

Network and/or IP adress
------------------------

How to get help
---------------

How To Upload
---------------

.. The second feature is the upload. If you need to send data to a Power Brick, it's the convenient feature.

.. Secondly, move on the blue button  "Upload" just below the Download button. Select, the remote directory where you'll 
.. send the data (folder or files).
.. Thirdly, you must enter the path (absolute path) to the folder you want to send.

.. Finally, press on the button "Upload" and look at log on your request in the display below.  

.. note:: example in line 1 

    in line 2

.. caution:: example in line 1
    
    in line 2

.. warning:: example in line 1
    
    in line 2

.. important:: example in line 1
    
    in line 2

.. important:: example in line 1
    
    in line 2

.. attention:: example in line 1
    
    in line 2

.. tip:: example in line 1
    
    in line 2

..  code-block:: python

    plop = 1