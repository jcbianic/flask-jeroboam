"""Sphinx configuration."""
project = "flask-jeroboam"
author = "Jean-Christophe Bianic"
copyright = "2022, Jean-Christophe Bianic"
extensions = [
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
    "sphinx_multiversion",
]
autodoc_typehints = "description"
html_theme = "flask"
smv_tag_whitelist = r"^v\d+\.\d+.*$|latest"
smv_branch_whitelist = r"^(?main).*$"
smv_released_pattern = r"v.*"
smv_remote_whitelist = r"^(origin)$"
