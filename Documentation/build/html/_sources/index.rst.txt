.. My Sphinx Example Project documentation master file, created by
   sphinx-quickstart on Thu Jun 11 16:43:50 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
 
Welcome to OSMOS Documentation!
===============================
 
Description
-----------
 
This documentation describe everything related to the software product : OSMOS.

OSMOS is a software designed to upload and save parameters, code and variables from
GALIL motion controllers referenced on synchrotron SOLEIL network.
 
Notes
-----
 
- This documentation has been redacted by people still learning how to use SPHINX framework. Be nice reading it!
- If information is missing or too much information is present... Keep quiet!
- You can contact ISAC Service at any moment if you don't understand how it works.
 
Modules
-------
 
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   FilePages/modules.rst
   CBPages/modules.rst
   GuidesPages/modules.rst
   Src/modules.rst 

..    modules
.. si non fonctionnel, le faire revenir derrière "content:" puis refaire entréex2 (+ tab si nécessaire)
 
.. ex:
   Directory1/modules.rst
   Directory2/modules.rst
   UserGuide.rst
 
.. Ces modules sont impératifs pour organiser la documentation en dossier.
 
Indices and tables
------------------
 
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`