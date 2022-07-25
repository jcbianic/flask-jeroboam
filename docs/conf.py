"""Sphinx configuration."""
project = "flask-jeroboam"
author = "Jean-Christophe Bianic"
copyright = "2022, Jean-Christophe Bianic"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
