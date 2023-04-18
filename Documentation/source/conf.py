 # Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))

# --- insert python file to documentation project -----------------------------
Project = "OSMOS"
ProjectDir = os.path.dirname(__file__)

while os.path.basename(ProjectDir) != Project:
    ProjectDir = os.path.dirname(ProjectDir)

# ======== Sources files =================
sourcesPath = ProjectDir + "\\Sources"
sys.path.insert(0, sourcesPath)  # chemin absolu des fichiers source
sys.setrecursionlimit(1500)

# ======== File management package =================
sourcesPath = ProjectDir + "\\Sources\\Packages\\File"
sys.path.insert(0, sourcesPath)  # chemin absolu des fichiers source
sys.setrecursionlimit(1500)

# ======== ControlBox package =================
sourcesPath = ProjectDir + "\\Sources\\Packages\\ControlBox"
sys.path.insert(0, sourcesPath)  # chemin absolu des fichiers source
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------

project = 'OSMOS'
copyright = '2022, M.Cerato'
author = 'M.Cerato'

# The full version, including alpha/beta/rc tags

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Document __init__, __repr__, __del__ and __str__ methods
def skip(app, what, name, obj, would_skip, options):
    if name in ("__init__", "__repr__", "__str__", "__del__"):
        return False
    return would_skip
 
def setup(app):
    app.connect("autodoc-skip-member", skip)

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_static_path = ['_static']
html_logo = './_static/logo_150px_no_bg.png'
html_title = ""
html_favicon = './_static/logo_150px_no_bg.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']