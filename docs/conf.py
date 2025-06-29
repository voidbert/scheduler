# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

project = 'scheduler'
copyright = '2025, Humberto Gomes'
author = 'Humberto Gomes'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints'
]

add_module_names = False

autodoc_inherit_docstrings = False
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

html_css_files = ['custom.css']
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'

sys.path.insert(0, os.path.abspath(".."))
