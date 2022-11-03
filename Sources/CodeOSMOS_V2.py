# -*- coding: utf-8 -*-
"""OSMOS Program's documentation.

Description
-----------
OSMOS allows you to performs actions on the controlBox.
For instance, generate a setup file of one or many controlBox
You can also test a connection to a controlBox or reset it. \n
The concept of OSMOS is based on the sequence diagram below:

.. image:: N:/ISAC/01_DOCUMENTS_EN_COURS/DOC_MS/OSMOS_V2/OSMOSSource/DiagramSeq.png


Libraries/Modules
-----------------
- os standard library (https://docs.python.org/3/library/os.html)
    - Access to files function.

- time standard library (https://docs.python.org/3/library/time.html)
    - Access various time-related functions.

- datetime standard library (https://docs.python.org/3/library/datetime.html)
    - Access basic date format functions.

- Regular expression (re) standard library
    (https://docs.python.org/3/library/datetime.html)

    - Access Regular Expression matching operations.

- gclib GALIL property library
    (https://www.galil.com/sw/pub/all/doc/gclib/html/python.html)

    - Access ControlBox communication functions.

- Tkinter standard library(https://docs.python.org/fr/3/library/tkinter.html)
    - Standard GUI function

Version
-------
- 1.0.0.0

Notes
-----
- Here is OSMOS_V2 concept explanation. It's main feature is to extract
  ControlBox setups: variables, microcode and parameters.
  To have it done, 3 main functions have been defined.
- OSMOS_V2 establishes connection to a ControlBox only once during all the
  setups extraction process. Just after it, the connection is closed.
- OSMOS_V2 has a GUI with objects like buttons, ComboBox, TextField for display
  and entry fields.
- In the ipEntry field, when entering the ip address, if the entered ip address
  doesn't respect spelling like xx.xx.xx.xx any action will not be
  possible and a message invites you to put a correct format of ip address.
- OSMOS_V2 has been modified since the previous version:
- First, the SI command return list of values like 0, 0, 0, 0, 0<0>
  In the current version, when we have list of values beginning with 0, we put
  only one zero (SI=0).
- Second, GA command position has been modified.  At the beginning, the
  command was at the end of the parameters part; that generates errors when
  uploading osmos file to a ControlBox. This is why it has been decided to
  order all the commands in the input file OSM_LIST_CDE.csv
- Third, there was error when uploading the microcode because it was in many
  lines. From now on, the microcode is put in one line (like in galil) and it
  works whithout any problem.

TODO
----
- The current version of OSMOS aims to extract setups from ControlBox
- It can be improved to also allow uploading setups files to ControlBox instead
  of going trought GalilSuite tool.

Author(s)
---------
- Created by M. Cerato on 06/17/2022.
- Modified by Sidibé on 07/18/2022.

Copyright (c) 2022 Cerato Workshop.  All rights reserved.

Members
-------
- Matthieu Cerato
- Moussa Sidibé
"""

import time
import datetime
import re
import gclib
import os
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as st


class OSMOSGui(object):
    """ The class where necessary tkinter objects are defined to create the GUI

    :parameter master: the main support of the GUI
    :type master: object
    """

    def __init__(self, master):
        """
        Instanciate OSMOSGui class .
        """
        root.title('OSMOS - V2')
        root.geometry('1480x860')
        root.minsize(1480, 860)
        frame = tk.Frame(master)
        frame.config(bg='grey')
        frame.place(x=1, y=5, width=1915, height=1130)
        self.label = tk.Label(frame, text='Output OSMOS', width=20, font=15,
                              bg='green', fg='white')
        self.label.place(x=380, y=75)
        self.resoLabel = tk.Label(frame, text='Reseau: ')
        self.resoLabel.place(x=1, y=5)
        listeReso = ["RCM", "ODE", "SMIS", "AILES", "MARS", "PSICHE",
                     "PLEIADES", "DISCO", "DESIRS", "METROLOGIE", "PUMA",
                     "CRISTAL", "DEIMOS", "GALAXIES", "TEMPO", "SAMBA",
                     "HERMES", "PX1", "PX2", "SWING", "ANTARES", "ROCK",
                     "ANATOMIX", "NANOSCOPIUM", 'DIFFABS', "SEXTANTS",
                     "CASSIOPEE", "SIRIUS", "LUCIA", "SIXS"]
        self.choixReso = tk.ttk.Combobox(frame, values=listeReso)
        self.choixReso.place(x=60, y=5)
        self.modeLabel = tk.Label(frame, text='Mode')
        self.modeLabel.place(x=300, y=5)
        self.mode = ttk.Combobox(frame, values=['0 CB unique',
                                                '1 Liste de CB'])
        self.mode.current(1)
        self.mode.bind("<<ComboboxSelected>>", refreshGui)
        self.mode.place(x=350, y=5)
        self.ipAd = tk.Label(frame, text='@ IP : ', bd=3)
        self.ipAd.place(x=560, y=5)
        self.ipEntry = tk.Entry(frame, width=30, bd=3, state='disabled',
                                disabledbackground='ivory')
        self.ipEntry.place(x=600, y=5)
        self.label2 = tk.Label(frame, text='Nom Fichier Output', bd=3)
        self.label2.place(x=825, y=5)
        self.nomFichier = tk.Entry(frame, width=50, bd=3, state='disabled',
                                   disabledbackground='ivory')
        self.nomFichier.place(x=945, y=5)
        self.cbxEssai = ttk.Combobox(frame, values=['0 Retry', '1 Retry'])
        self.cbxEssai.current(0)
        self.cbxEssai.place(x=1300, y=5)
        self.btn = tk.Button(frame, text='Start', bg='green', fg='white',
                             command=lambda: main())
        self.btn.place(x=500, y=600)
        self.testCon = tk.Button(frame, text='Test Connection', fg='blue',
                                 command=lambda: __testConnexion(self))
        self.testCon.place(x=300, y=600)
        self.screen = st.ScrolledText(frame)
        # height is the number of lines and width is in pixel
        self.screen.place(x=3, y=120, height=450, width=960)
        self.screen.insert(tk.END, str('Welcome to OSMOS\n'))
        self.btn2 = tk.Button(frame, text='ResetCB',  bg='red',
                              command=lambda: resetCB())
        self.btn2.place(x=650, y=600)

        # In[1]: internal function for Class OSMOSGui
        def __getip(self):
            """Internal function for Class OSMOSGui.
            Intended to get the ip address entered by the user in the ipEntry
            field. Necessary in unique mode for getting output file,
            trying a connection or resetting a ControlBox.

            :return: None.
            """
            adress = self.ipEntry.get()
            sprint(adress)
            reso = self.choixReso.get()
            sprint(reso)

        def __testConnexion(self):
            if eval(gui.mode.get()[0]) == 1:
                tk.messagebox.showwarning('warning', 'Vous devez être en mode'
                                          + 'CB unique pour continuer')
                gui.ipEntry.delete(0, tk.END)
                gui.ipEntry.config(state='disabled')
            elif gui.ipEntry.get() == '':
                tk.messagebox.showwarning('warning', 'Veuillez saisir l\'@ ip')
                gui.ipEntry.config(state='normal')

            else:
                # The regex which oblige to respect a good format of ip address
                ipFormat = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                ip = gui.ipEntry.get()
                if not re.match(ipFormat, ip):
                    tk.messagebox.showwarning('warning', 'Le format de ' +
                                              'l\'adresse ip n\'est pas bon')
                else:
                    gui.screen.delete(0.0, tk.END)
                    g = etablirConnexion(ip)
                    g.GClose()


def refreshGui(self):
    """
    Function aiming the dynamic update of the GUI

    :return: None.
    """
    if eval(gui.mode.get()[0]) == 1:
        gui.ipEntry.config(state='disabled')
        gui.nomFichier.config(state='disabled')
    else:
        gui.ipEntry.config(state='normal')
        gui.nomFichier.config(state='normal')


def etablirConnexion(ip):
    """To connect to a ControlBox.

    :parameter ip: the address of the ControlBox we want to connect to.
    :type ip: str
    :return: the object g which allows to interact with the ControlBox.
    :rtype: object
    """
    try:
        g = gclib.py()
        g.GOpen(ip)
    except Exception as ex:
        sprint("Erreur: " + str(ex))

    if __isConnected(g) is True:
        sprint(f"connected to {ip}")
        # Returns all the informations about a device : ip address, firmware,
        # number of axis
        info = g.GInfo()
        info = re.split(" ", info)
        firmware = info[1]
        # return only the firmaware: DMC4183s56e-SER old version
        firmware = firmware[:-1]
    return g


def __isConnected(g):
    """Check if connection is established with the ControlBox.

    :param g: The object returned by etablirConnexion()
    :type g: object
    :return: True or False
    :rtype: boolean
    """
    try:
        # ping the device that ip address is given on the GUI or input file
        g.GCommand('IA?')
    except Exception:
        return False
    return True


def sprint(msg):
    """Allow to display informations on the GUI.

    :param msg: is the text to display.
    :type msg: str
    :return: None.
    """
    gui.screen.insert(tk.END, str(msg)+'\n')


def resetCB():
    """Allow the reset of the CB wich ip address is entered on the GUI.

    :return: None
    :rtype: None
    """
    ip = gui.ipEntry.get()
    if ip == '':
        # show a pop up if any ip address is not entered
        tk.messagebox.showwarning('warning', 'Veuillez saisir l\'adresse ip de'
                                  + ' la CB !')
        gui.ipEntry.config(state='normal')

    else:
        ip = gui.ipEntry.get()
        gui.screen.delete(0.0, tk.END)

        # The regex which oblige to respect a good format of ip address
        ipFormat = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        if not re.match(ipFormat, ip):
            tk.messagebox.showwarning('warning', 'Le format de l\'adresse ip '
                                      + 'n\'est pas bon')
        else:
            g = etablirConnexion(ip)
            cmd = 'RS'              # command for reset
            try:
                res = g.GCommand(cmd)
                sprint(res)
            except Exception as ex:
                sprint(ex)
                g.GClose()


def fichierLog(reso, pathBis):
    """Is in charge of creating a file which records all events that happen
    during OSMOS run.

    :param pathBis: the path leading to output files directory
    :param reso: the name of the concerned network.
    :type reso: str
    :type pathBis: str
    :return: the file name
    :rtype: str
    """
    global logFile  # One log file per run.
    # get today's date
    today = datetime.date.today()
    # create a full date
    dat = today.strftime("%Y-%m-%d_") + time.strftime("%H-%M-%S")
    # create the logFile
    logFile = open(pathBis + "OSMOS-Log-" + reso + '_' + dat + ".txt", "a+")
    name = "log File: " + dat + ".txt"
    return name


def getMicrocode(g, device, pathBis):
    """Download the microcode of the controlBox in variable
     before putting it in a temporary file.

    :param g: the object got above from etablirConnexion(ip)
    :type g: object
    :param device: name of the ControlBox
    :type device: str
    :param pathBis: path leading to the directory where the ouput files
     will be created.
    :type pathBis: str
    :return: None
    """
    day = datetime.date.today().strftime('%Y-%m-%d')
    if __isConnected(g) is True:
        info = g.GInfo()
        info = re.split(' ', info)
        info = info[0]
        info = re.split(',', info)
        IP = info[0]
        logFile.write('\nConnection to the CB ' + str(IP) + ' is Ok')
        try:
            ucode = open(pathBis + day + '_microcode.txt', 'w')
            sprint('Chargement du microcode ...')
            logFile.write('\nChargement du microcode')
            # Avoid any impact of the previous quotation mark on the ucode
            mcode = g.GProgramUpload()
            mcode = mcode.replace("\r\n", "\\r\\n")
            ucode.write('\n[Program]\n')
            ucode.write('Program=\"')
            ucode.write(mcode)
            sprint('  chargement du µcode ok')
            logFile.write('\n  chargement du microcode ok')

        except Exception as ex:
            sprint('Echec de chargement du µcode ' + device + '\rError : '
                   + str(ex))
            logFile.write('\n  Echec de chargement du code ' + device
                          + '\rError : '+str(ex))
            return 1
        ucode.close()
    else:
        logFile.write('\nConnection to the CB not established')
        sprint('\nConnection to the CB not established')


def getVariables(g, device, pathBis):
    """Downloads the variables in a temporary file before formatting them.

    :param device: it's the CVS name of the concerned ControlBox
    :param g: the object returned by etablirConnexion
    :param pathBis: the path leading to the directory where the output files
     will be created.
    :return: None
    :rtype: None
    """
    day = datetime.date.today().strftime('%Y-%m-%d')
    if __isConnected(g) is True:
        info = g.GInfo()
        info = re.split(' ', info)
        info = info[0]
        info = re.split(',', info)
        IP = info[0]
        logFile.write('\nConnection to CB ' + str(IP) + ' stays established')

        # Create the variable's file
        listDeVariable = open(pathBis + day + "_variable.txt", "w")
        logFile.write("\nRécupération des variables")
        sprint('Récupération des variables...')
        # LV is the command to print the list of the variables except arrays
        flag = 0
        try:
            variable = g.GCommand("LV")
        except Exception as ex:
            logFile.write('\n  Erreur commande LV : ' + str(ex))
            sprint('  Erreur commande LV : ' + str(ex))
            flag = 1
            # return 1
        # nomFichier = "listDevariable_" + day + ".txt"
        # One, because no return in the last line
        nombDeVariable = 1 + variable.count("\n")
        listDeVariable.write('[Data]\n')
        # Write down the number of variables at the beginning of the file
        listDeVariable.write("Variable\\size=" + str(nombDeVariable))
        # Put the data in list format
        variableSplite = variable.split()
        # getting the variables
        for i in range(nombDeVariable):
            if i == 0:
                temp = variableSplite[0]
                # Return just the name of the variable
                nomVariab = temp[:-1]
                valeur = variableSplite[i+1]
                listDeVariable.write('\nVariable' + '\\' + str(i + 1) + '\\' +
                                     'Name=' + nomVariab + '\nVariable' + '\\'
                                     + str(i+1) + '\\' + 'Value='
                                     + str(valeur))
            else:
                temp = variableSplite[i*2]
                nomVariab = temp[:-1]
                valeur = variableSplite[(i*2)+1]
                listDeVariable.write('\nVariable' + '\\' + str(i+1) + '\\' +
                                     'Name=' + nomVariab + '\nVariable' + '\\'
                                     + str(i+1) + '\\' + 'Value='
                                     + str(valeur))
        if flag == 0:
            logFile.write('\n  Chargement des variables de type variable ok')
            sprint('  Chargement des variables de type variable ok')
        # Récuperation des variables tableau
        try:
            # LA is the galil command to get the list of array variables
            tableau = g.GCommand('LA')
        except Exception as ex:
            logFile.write('Erreur commande LA : ' + str(ex))
            sprint('   Erreur commande LA : ' + str(ex))
            return 1

        nombDeTableau = 1 + tableau.count("\n")
        # Write the number of arrays in the file
        listDeVariable.write("\nArray\\size=" + str(nombDeTableau))
        tableauSplite = tableau.split("\n")
        for i in range(len(tableauSplite)):
            temp = tableauSplite[i]
            # Regex to split the length of the array and it's name
            temp = re.split("\\[", temp)
            nomTableau = temp[0]
            tailleTab = temp[1].split("]")
            # Get the length of each array: after a reset the CB must be
            # loaded otherwise this line returns error (list out of range)
            tailleTab = tailleTab[0]
            x = int(tailleTab) - 1
            try:
                # LA is the galil command to get the contents of the arrays
                # given as parameter
                cmd = 'QU ' + nomTableau + '[], 0,' + str(x) + ', 1'
                valArray = g.GCommand(cmd)
                listDeVariable.write('\nArray' + '\\' + str(i + 1) + '\\'
                                     + 'Name=' + nomTableau + '\nArray' + '\\'
                                     + str(i + 1) + '\\' + 'Size='
                                     + str(tailleTab) + '\nArray' + '\\'
                                     + str(i + 1) + '\\' + 'Value=' + valArray)
            except Exception as ex:
                logFile.write('\n  Echec de récupération du contenu des Array.'
                              + ' Error: ' + str(ex))
                sprint('     Echec de récupération du contenu des Array.'
                       + ' Error: ' + str(ex))
                return 1
        logFile.write('\n  Chargement des array ok')
        sprint('  Chargement des array ok')


def get_feat_cb(g):
    """Define the binary code corresponding to the version of the CB which we
    want to extract parameters.

    :param g: the object return by etablirConnexion(ip)
    :type g: object
    :return: feat_CB which is a result of a boolean operation.
    :rtype: int
    """
    path = './'
    conf = open(path + 'HW_SW_conf.csv')
    HW = {}
    SW = {}
    for i in conf.readlines():
        x = (i.split(';'))
        if x[0] == 'HW':
            HW[x[1]] = x[2]
        if x[0] == 'SW':
            SW[x[1]] = x[2]

    if __isConnected(g) is True:
        mot = g.GInfo().split(',')
        sprint(mot)
        # Get hardware elements in the word DMC. (e.g 4183)
        hw = mot[1][4:8]
        # Get the software part in the word DMC. (e.g 56g)
        sw = mot[1][9:]
        bin_sw = bin(0)   # bin_sw equal binairy value of (0b0)
        bin_hw = bin(0)

        try:
            bin_hw = bin(eval(HW[hw]))
        except Exception as ex:
            print('ERREUR HW ' + str(ex))

        try:
            bin_sw = bin(eval(SW[sw]))    # Binairy conbvert of  SW[sw] value
        except Exception as ex:
            print('ERREUR SW ' + str(ex))
        # Logical operation OR
        sprint("feat CBBBBBBBBB "
               + str((bin(int(bin_sw, 2) | int(bin_hw, 2)))))
        # Returns a binary value of feat_CB
        return bin(int(bin_sw, 2) | int(bin_hw, 2))


def getParameters(g, device, pathBis):
    """Download and format the parameters in a temporary file.

    :param g: object returned by etablirConnexion(ip)
    :param device: the root name of the controlBox
    :param pathBis: output files directory
    :type g: object
    :type device: str
    :type pathBis: str
    :return: None
    :rtype: None
    """
    today = datetime.date.today()
    day = today.strftime('%Y-%m-%d')
    path = './'   # the current working directory where input files are saved
    if __isConnected(g) is True:
        sprint('Récupération des paramètres')
        info = []
        info = g.GInfo()
        firmware = re.split(" ", info)
        serialNum = firmware[2] + '.0000'
        firmware = firmware[1]
        firmware = firmware[:-1]           # Get the firmware
        axis = firmware[5]                 # same thing for getting axis number
        if firmware[5:7] == '82':
            deviceName = firmware[0:5] + 'x3'       # Get the device name
        else:
            deviceName = firmware[0:5] + 'x' + firmware[6]

        listeDeCommande = open(path + "OSM_LIST_CDE.csv")
        fichierParam = open(pathBis + day + '_parametre.txt', 'w')
        logFile.write('\nConnection to the CB stays established')
        logFile.write('\nChargement des paramètres\n')

        fichierParam.write("[SystemInfo]\nFirmware=" + firmware + '\nSerial='
                           + serialNum + '\nDevice=' + deviceName + '\nAxis='
                           + axis + '\n\n[Configuration]\n' + 'EO=False\n')
        axe = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        feat_cb = get_feat_cb(g)
        li = listeDeCommande.readlines()
        flag = 0   # Variable which checks if any problem occurs in the process
        for commande in li[1:]:
            # Convert data into list format
            ligne = (commande.replace('\n', '').split(';'))
            # Get the key param form input file
            kp = ligne[0]
            kp = int(kp)
            # Convert the binary value of feat_cb into  integer
            val2 = int(feat_cb, 2)
            # Logical operation between key-param and val2
            feat_et_key = (kp & val2)

            if feat_et_key != 0:
                # It's a mark of comment, so nothing to transform
                if ligne[1] == '0':
                    if ligne[2].find('firmware') != -1:
                        firm = ligne[3]
                        fichierParam.write(firm.replace('%VAR', firmware))
                        fichierParam.write('\n')

                    elif ligne[2].find('date') != -1:
                        tempDate = ligne[3]
                        fichierParam.write(tempDate.replace("%DATE", day))
                        fichierParam.write('\n')
                    # Below we have the code which formats the output data like
                    # galil output
                    elif ligne[3].find('MO') != -1:
                        fichierParam.write(ligne[3] + '\\' + 'size=1' + '\n')
                        res = ligne[3] + '\\1' + '\\Cmd=MO' + '\\r' + '\n'
                        fichierParam.write(res)

                    elif ligne[3].find('VF') != -1:
                        fichierParam.write('VF=' + ligne[3] + '\\r' + '\n')

                    elif ligne[3].find('PF') != -1:
                        fichierParam.write('PF=' + ligne[3] + '\\r' + '\n')
                    # Omit leading zero : it's a new command of galil
                    elif ligne[3].find('LZ') != -1:
                        fichierParam.write('LZ=' + ligne[3] + '\\r' + '\n')
                    else:
                        fichierParam.write(ligne[3])
                        fichierParam.write('\n')

                elif ligne[1] == '1':
                    # Delete if necessary, whitespace near a command
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()

                    if ligne[2] == 'MT':
                        fichierParam.write(ligne[2] + '\\' + 'size=' +
                                           str(len(axe)) + '\n')
                        for i in range(len(axe)):
                            cmd = ligne[2] + axe[i] + '=?'
                            try:
                                resCommande = g.GCommand(cmd)
                                res = (ligne[2] + '\\' + str(i+1) + '\\'
                                       + 'Cmd=' + '\"' + ligne[2] + axe[i] +
                                       '=' + resCommande + '\\r' + '\"')
                                fichierParam.write(res)
                                fichierParam.write('\n')

                            except Exception as ex:
                                logFile.write('Error' + device + ' ' + str(cmd)
                                              + ' ' + str(ex) + '\n')
                                sprint(ex)
                                flag = 1
                    else:
                        # write with the same format the returned data in only
                        # one line
                        res = ligne[2] + '=' + '\"'
                        for a in axe:
                            cmd = ligne[2] + a + '=?'
                            try:
                                # The variable resCommande stores the result of
                                # the command
                                resCommande = g.GCommand(cmd)
                                # It's the line to write in parameters file
                                res = (res + ligne[2] + a + '=' + resCommande
                                       + '\\r')
                            except Exception as ex:
                                logFile.write('Error ' + device + ' '
                                              + str(cmd) + ' ' + str(ex)
                                              + '\n')
                                sprint(ex)
                                flag = 1
                        fichierParam.write(res)
                        fichierParam.write('\"')
                        fichierParam.write('\n')

                elif ligne[1] == '2':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    else:
                        pass
                    cmd = ligne[2] + '?'
                    try:
                        resCommande = g.GCommand(cmd)
                        # Put strings like IA in cote
                        if resCommande.find(',') != -1:
                            res = (ligne[2] + '=' + '\"' + ligne[2] + ' '
                                   + resCommande + '\\r' + '\"')
                            fichierParam.write(res)
                            fichierParam.write('\n')
                        else:
                            res = (ligne[2] + '=' + ligne[2] + ' '
                                   + resCommande + '\\r')
                            fichierParam.write(res)
                            fichierParam.write('\n')
                    except Exception as ex:
                        logFile.write('\nError ' + device + ' ' + str(cmd)
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '3':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    cmd = 'MG_' + ligne[2]
                    try:
                        retour = g.GCommand(cmd)
                        res = ligne[2] + '=' + ligne[2] + ' ' + retour + '\\r'
                        fichierParam.write(res)
                        fichierParam.write('\n')
                    except Exception as ex:
                        logFile.write('Error' + device + ' ' + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '4':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    cmd = 'MG_' + ligne[2]
                    try:
                        retour = g.GCommand(cmd)
                        # [:-1] to delete the number(CN instead of CN0, CN1)
                        res = (ligne[2] + '=' + ligne[2][:-1] + ' ' + retour
                               + '\\r')
                        fichierParam.write(res)
                        fichierParam.write('\n')
                    except Exception as ex:
                        logFile.write('Error' + device + ' ' + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '5':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    cmd = 'MG_' + ligne[2]
                    try:
                        resCommande = g.GCommand(cmd)
                        res = (ligne[2] + '=' + '\"' + ligne[2][:-1] + ' ,'
                               + resCommande + '\\r' + '\"')
                        fichierParam.write(res)
                        fichierParam.write('\n')
                    except Exception as ex:
                        logFile.write('Error ' + device + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '6':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    cmd = 'MG_' + ligne[2]
                    try:
                        retour = g.GCommand(cmd)
                        res = (ligne[2] + '=' + '\"' + ligne[2][:-1] + ' ,,'
                               + retour + '\\r' + '\"')
                        fichierParam.write(res)
                        fichierParam.write('\n')
                    except Exception as ex:
                        logFile.write('Error ' + device + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '7':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    cmd = 'MG_' + ligne[2]
                    try:
                        resCommande = g.GCommand(cmd)
                        res = (ligne[2] + '=' + '\"' + ligne[2][:-1] + ' ,,,'
                               + resCommande + '\\r' + '\"')
                        fichierParam.write(res)
                        fichierParam.write('\n')

                    except Exception as ex:
                        logFile.write('Error ' + device + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)
                        flag = 1

                elif ligne[1] == '8':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    else:
                        pass
                    cmd = 'MG_' + ligne[2]
                    try:
                        resCommande = g.GCommand(cmd)
                        res = (ligne[2] + '=' + '\"' + ligne[2][:-1] + ' ,,,,'
                               + resCommande + '\\r' + '\"')
                        fichierParam.write(res)
                        fichierParam.write('\n')
                    except Exception as ex:
                        flag = 1
                        logFile.write('Error ' + device + str(cmd) + ' '
                                      + str(ex) + '\n')
                        sprint(ex)

                elif ligne[1] == '10':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    res = ligne[2] + '=' + '\"'
                    for a in axe:
                        try:
                            cmd = ligne[2] + a + '=?'
                            resCommande = g.GCommand(cmd)
                            # to avoid being out of 79 characters
                            rc = resCommande
                            if rc[0] == '0':
                                resCommande = '0\\r'
                            if rc == '0, 0, 0, 0, 0, 0' or rc == '0,0,0,0,0,0':
                                resCommande = '0\\r'
                            res = res + ligne[2] + a + '=' + resCommande
                        except Exception as ex:
                            flag = 1
                            logFile.write('Error ' + device + ' ' + str(cmd)
                                          + ' ' + str(ex) + '\n')
                            sprint(ex)
                    fichierParam.write(res)
                    fichierParam.write('\"')
                    fichierParam.write('\n')

                elif ligne[1] == '11':
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                        res = ligne[2] + '=' + '\"'
                    for a in axe:
                        try:
                            cmd = ligne[2] + a + '=?'
                            rc = g.GCommand(cmd)
                            if rc[0] == '0':
                                resCommande = '0\\r'
                            if rc == '0, 0, 0, 0, 0' or rc == '0,0,0,0':
                                resCommande = '0\\r'
                            res = res + ligne[2] + a + '=' + resCommande
                        except Exception as ex:
                            logFile.write('Error ' + device + ' ' + str(cmd)
                                          + ' ' + str(ex) + '\n')
                            sprint(ex)
                            flag = 1
                    fichierParam.write(res)
                    fichierParam.write('\"')
                    fichierParam.write('\n')

                elif ligne[1] == '12':
                    size = 0    # number of GA command result != 0
                    listRes = []
                    listAxeRes = []   # list of axis where the the gear is != 0
                    if ligne[2].find(' ') != -1:
                        ligne[2] = ligne[2].rstrip()
                    for a in axe:
                        cmd = ligne[2] + a + '=?'
                        try:
                            resCommande = g.GCommand(cmd)
                        except Exception as ex:
                            logFile.write('Error ' + device + str(cmd) + ' '
                                          + str(ex) + '\n')
                            sprint(ex)
                            flag = 1
                        if resCommande[0] != '0':
                            size += 1
                            listRes.append(resCommande)
                            listAxeRes.append(a)
                        else:
                            pass
                    fichierParam.write(ligne[2] + '\\size' + '='
                                       + str(size) + '\n')
                    for i in range(len(listRes)):
                        res = (ligne[2] + '\\' + str(i) + '\\'
                               + 'Cmd=' + '\"' + ligne[2] + listAxeRes[i] +
                               '=' + str(listRes[i]) + '\\r' + '\"')
                        fichierParam.write(res)
                        fichierParam.write('\n')
        if flag == 0:
            logFile.write('  chargement des paramètres ok\n\n')
            sprint('  chargement des paramètres ok')


def creerFichierOutput(pathBis, device):
    """Aim to merge to one output file the 3 temporary files above containing
    the microcode, the parameters and the variables.

    :param pathBis: the  path to output files directory
    :param device: the Concerned ControlBox
    :type pathBis: str
    :type device: str
    :return: None
    :rtype: None
    """
    day = datetime.date.today().strftime('%Y-%m-%d')
    dat = (datetime.date.today().strftime('%Y-%m-%d_')
           + time.strftime('%H-%M-%S'))
    # Opens file already created for variables and sends its data in a
    # temporary variable via the read method
    # Check if temporary file exists before (i.e setups have been extracted)
    flag = 1
    if os.path.isfile(pathBis + day + '_variable.txt'):
        flag = 0
    if os.path.isfile(pathBis + day + '_parametre.txt'):
        flag = 0
    if os.path.isfile(pathBis + day + '_microcode.txt'):
        flag = 0

    if flag == 0:
        with open(pathBis + day + '_variable.txt') as fp:
            data1 = fp.read()
        with open(pathBis + day + '_parametre.txt') as fp:
            # Its purpose likes the previous line
            data = fp.read()
        with open(pathBis + day + '_microcode.txt') as fp:
            data2 = fp.read()

        # Create the output file .bak  and write down all the data
        with open(pathBis + device + '.bak', 'w') as fp:
            data = data + '\n'
            data += data1
            data = data + '\n'
            data += data2
            fp.write('\"')
            fp.write('Log File: OSMOS-Log_' + dat + '.txt"\n\n')
            fp.write(data)
            # To close the quotation marks after the microcode in order to have
            # the same format with galilsuite output
            fp.write('\"')
        # Delete the files which the data has just been written in the output
        # file
        os.remove(pathBis + day + '_variable.txt')
        os.remove(pathBis + day + '_parametre.txt')
        os.remove(pathBis + day + '_microcode.txt')


def getListeCB():
    """Read the input file containing the list of CB.

    :return: None
    """
    global fichCB
    # Its the current working directory where file liste of CB is stored
    path = './'
    fichCB = open(path + 'OSM_LIST_CB.csv')


def main():
    """Its the entry of the program.
    All necessary values (variables or functions parameters) are given here to
    allow run OSMOS.
    User has to select all required parameters(network, operating mode,
    the retry, etc.) to run a task.

    :return: None
    """
    global fichCB
    path = './'    # Current working directory containing the input files
    gui.screen.delete(0.0, tk.END)   # Clean the display before every new task
    # Get the selected operating mode: 1 is multiple mode (default mode)
    if eval(gui.mode.get()[0]) == 1:
        gui.ipEntry.delete(0, tk.END)
        gui.ipEntry.config(state='disabled')
        gui.nomFichier.config(state='disabled')
        if gui.choixReso.get() == '':
            # Shows a warning if any network is not selected
            tk.messagebox.showwarning('warning', 'Veuillez choisir votre'
                                      + ' réseau de travail')
        else:
            reso = gui.choixReso.get()
            sprint(reso)
            way = (path + 'OSMOS_' + reso + '_'
                   + datetime.date.today().strftime('%Y-%m-%d_')
                   + time.strftime('%H-%M'))
            # List made from the batch of CB contained in the input file
            listeCB = []
            getListeCB()
            for line in fichCB.readlines():
                listeCB.append({'Reseau': line.split(';')[0],
                                'Device': line.split(';')[1],
                                'IPadress': line.split(';')[2],
                                'nomRacineCVS': line.split(';')[3]})

            # Creates the directory for output files
            try:
                os.makedirs(way)
            except Exception as ex:
                sprint(ex)
            pathBis = way + '/'                    # The path for output files
            fichierLog(reso, pathBis)
            logFile.write('Répertoire des fichiers ouput : ' + pathBis)
            logFile.write('\n\nLecture de la liste des CB..\n')
            sprint('Lecture de la liste des CB ...')
            # The number of retry selected on the GUI which allows the process
            # to retry in case of data extracting problem
            essai = eval(gui.cbxEssai.get()[0])
            i = 0
            # The number that the process retries when a failure occurs
            while i <= int(essai):
                i += 1
                sprint('Essai ' + str(essai+1))
                logFile.write('\nEssai ' + str(essai+1) + ':\n')
                for CB in listeCB:
                    # Checks if the network matches with the one in the input
                    # file listCB; otherwise the network is ignored
                    if str(CB['Reseau']) != 'ssh aile':  # to ignore the title
                        if str(CB['Reseau']) == reso:
                            ip = str(CB['IPadress'])
                            # Do not use the 1st line of the input file(title)
                            if ip != 'Adresse-IP':
                                # delete empty columns in the input file
                                if ip != '':
                                    # the CVS root name of the device
                                    device = str(CB['nomRacineCVS'])
                                    logFile.write('\n')
                                    logFile.write(device)
                                    sprint('\n')  # Make the display more clear
                                    sprint(device)
                                    g = etablirConnexion(ip)
                                    getMicrocode(g, device, pathBis)
                                    getVariables(g, device, pathBis)
                                    getParameters(g, device, pathBis)
                                    creerFichierOutput(pathBis, device)
                            g.GClose()
            logFile.close()
            fichCB.close()
            sprint('\n\n\t\t\t ---  End of task !   ---')

    # The another selected operating mode : 0 is unique CB (optional mode)
    else:
        gui.ipEntry.config(state='normal')
        gui.nomFichier.config(state='normal')
        # The regex which oblige to respect a good format of ip address
        ipFormat = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

        ipSaisi = gui.ipEntry.get()
        if ipSaisi == '':
            # Shows a pop up if any ip address has not been entered
            tk.messagebox.showwarning('warning', 'Veuillez saisir'
                                      + ' l\'adresse ip de la CB !')

        elif not re.match(ipFormat, ipSaisi):
            tk.messagebox.showwarning('warning', 'Le format de l\'adresse ip '
                                      + 'n\'est pas bon')

        else:
            ip = gui.ipEntry.get()
            if gui.nomFichier.get() == '':
                tk.messagebox.showwarning('warning', 'Saisissez le nom du'
                                          + 'fichier output !')
            else:
                reso = gui.nomFichier.get()
                way = (path + 'OSMOS_' + reso + '_'
                       + datetime.date.today().strftime('%Y-%m-%d_')
                       + time.strftime('%H-%M'))
                try:
                    os.makedirs(way)   # Creates the directory for output files
                except Exception as ex:
                    sprint(ex)
                pathBis = way + '/'
                fichierLog(reso, pathBis)
                logFile.write('Répertoire des fichiers ouput : ' + pathBis)
                # The number of retry selected on the GUI which allows the
                # process to retry in case of data extracting problem
                essai = eval(gui.cbxEssai.get()[0])
                i = 0
                # The number that the process retries when a failure occurs
                while i <= int(essai):
                    i += 1
                    sprint('Essai ' + str(essai+1))
                    logFile.write('\n\nEssai ' + str(essai+1) + ':\n')
                    g = etablirConnexion(ip)
                    device = reso
                    getMicrocode(g, device, pathBis)
                    getVariables(g, device, pathBis)
                    getParameters(g, device, pathBis)
                    creerFichierOutput(pathBis, device)
                    sprint('\n\t\t\t ---  End of task !   ---')
                    logFile.write('\n\t\t\t ---  End of task !   ---')
                    logFile.close()
                g.GClose()


if __name__ == '__main__':
    root = tk.Tk()
    gui = OSMOSGui(root)
    root.mainloop()
