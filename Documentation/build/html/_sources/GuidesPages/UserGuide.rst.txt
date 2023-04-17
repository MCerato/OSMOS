"""""""""""""""""""""
OSMOS UserGuide (WIP)
"""""""""""""""""""""

WELCOME HERE! This documentation intend to show you how to use the OSMOS software 

.. _1. Description:

==============
1. Description
==============

OSMOS is a tool wich can communicate with the GALIL controllers of SOLEIL, 
extract the parameters/variables/microcode and write the into a ``.bak`` file

This file is parsed according to GALIL format allowing to upload those settings
into the controller

A ``.log`` file is generated indicatig if everything went right during the download

The user can configure the software through 2 ``.csv`` files wich are described below

.. _2. Software presentation:

========================
2. Software presentation
========================

How FileManagement has been designed is represented by the software architecture below:

.. image:: ./OSMOS_window.PNG
   :width: 600
   :align: center

The software is splitted in 5 main parts:

- "Select config Files", where you can shange  ``.csv`` file if you need
- "Select Directories", where you can choose a different location to save the ``.bak`` and ``.log`` files.
- "Configuration", where you choose wich network to save or you can enter a specific IP adress of a ControlBox
    .. note:: Whatever the network, IP Address is treated in priority.
        Keep it empty to treat the network of you choosing 

- "commands", where you can start the sequence.
    .. note:: As noted, the stop button is not implemented. It will come in a futur update.

- "Output", where you can have information during the sequence.

.. _3. Select the configuration Files:

=================================
3. Select the configuration Files
=================================

If you want, you can select the configurations files. These files consist on
2 ``.csv`` files called:

- *OSM_LIST_CB.csv* wich represent roughly the parameters available in a ControlBox
- *OSM_LIST_CDE.csv* wich list all controlbox in SOLEIL according to their network and physical locations

.. image:: ./OSMOS_window_config.PNG
   :width: 600
   :align: center

.. note:: choosing new files is not mandatory. If they are not manually given,
    OSMOS will take the default files located in *"OSMOS/Documentation/Reference"*

.. danger:: Never delete the reference files! OSMOS may crash instantly as 
    it doesn't have any reference to use!
    
To select new files you may just click on *"import CB file"* button 
or *"import Command file"* button and choose your new file

.. hint:: You can try it out with the path given in the picture below:
    ``OSMOS/Test/altern_CB_Path``
    ``OSMOS/Test/altern_Cde_Path``

.. image:: ./change_csv_file.PNG
   :width: 600
   :align: center

.. warning:: Be careful on wich file you load. CB file and command file can't be swapped.
    This can result in crash or non-functioning behavior as it won't find the informations it needs
    inside the document.
    


..  memo for tables
.. =========================== ================================
.. IP Adress Type              Description                     
.. =========================== ================================
.. Default IP Adress           Maintenance Adress 172.168.0.200
.. Custom IP adress            any Standard PBR adress
.. =========================== ================================

.. +--------+--------+--------+
.. | Time   | Number | Value  |
.. +========+========+========+
.. | 12:00  | 42     | 2      |
.. +--------+--------+--------+
.. | 23:00  | 23     | 4      |
.. +--------+--------+--------+

.. _4. Select where the files will be saved:

=======================================
4. Select where the files will be saved
=======================================

You can, if you want, change the directory in wich directories the ``.bak`` and ``.log`` are saved.

To select new directories you may just click on *"import .bak directory"* button 
or *"import .log directory"* button and choose your new directories

.. image:: ./OSMOS_window_save_dir.PNG
   :width: 600
   :align: center

.. note:: These files can be put in the same directory or not. 
    Directory management is automatic.

.. image:: ./change_directory.PNG
   :width: 600
   :align: center
   
If a IP adress is given, no networtk directory will be created inside the path chosen as 
it is disabled in this case (see :ref:`5. Network and/or IP address` )

.. note:: No information will be given to the user when changing the directory
    but it will be given to a developper through the standard output (interpreter).
    
.. important:: Changing the directory is not mandatory. There is defaults paths wich are:
    ``OSMOS/Sources/.bak`` and ``OSMOS/Sources/.log``

.. _5. Network and/or IP address:

============================
5. Network and/or IP address
============================

By default, ad with the current "CB file", the default network is "ISAC".
If a network is added in the file after ISAC then, this network will be the default one.

.. image:: ./OSMOS_window_IP_network.PNG
   :width: 600
   :align: center

.. note:: This drop-down menu can't be empty. It will amways have the value of the last network
    in the file
    
As said previously, the text field "IP adress" has priority. If this field is not empty
then, OSMOS will get the informations of this specific Controlbox and will ignore the network.

.. warning:: IP address text field is not yet protected if a wrong format is written.
    the requiered format is ``xxx.xxx.xxx.xxx``. I.e : ``172.16.3.65``.

.. image:: ./OSMOS_window_choose_network.PNG
   :width: 600
   :align: center

===================
6. How to use OSMOS
===================

-------------------------------
1. How to configure the CB File
-------------------------------

--------------------------------
2. How to configure the Cde File
--------------------------------

-----------------
3. Network and IP
-----------------

-----------------------------
4. When everything goes right
-----------------------------

.bak content
------------

.log content
------------

===========================
5. Troubleshooting and help
===========================



.. Below is a memo on How to put special parts in the documentation 
    Just take the first ".." off

.. .. note:: example in line 1 

    in line 2

.. .. caution:: example in line 1
    
    in line 2

.. .. warning:: example in line 1
    
    in line 2

.. .. important:: example in line 1
    
    in line 2

.. .. attention:: example in line 1
    
    in line 2

.. .. tip:: example in line 1
    
    in line 2

.. .. hint:: example in line 1
    
    in line 2

.. ..  code-block:: python

    plop = 1