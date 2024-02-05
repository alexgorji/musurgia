# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from pathlib import Path
import sys

sys.path.insert(0, Path(__file__).parents[1].resolve().as_posix())

project = 'musurgia'
copyright = '2023, A. Gorji'
author = 'A. Gorji'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosummary',
              'sphinx.ext.autosectionlabel',
              'sphinx.ext.doctest',
              'sphinx.ext.todo',
              'sphinx_copybutton'
              ]

# templates_path = ['_templates']
# exclude_patterns = []

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']
autodoc_member_order = 'groupwise'

html_theme_options = {
    "collapse_navigation": True
}
todo_include_todos = True
