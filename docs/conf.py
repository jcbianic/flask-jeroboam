"""Configuration for Generating Docs."""

# import packaging.version
from pallets_sphinx_themes import ProjectLink  # type: ignore
from pallets_sphinx_themes import get_version  # type: ignore


# Project --------------------------------------------------------------

project = "Flask-Jeroboam"
copyright = "2022, Jean-Christophe Bianic"
author = "Jean-Christophe Bianic"
release, version = get_version("Flask-Jeroboam")

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx_click",
    "myst_parser",
    "sphinx_multiversion",
    "sphinx_tabs.tabs",
    "sphinx_copybutton",
]
autodoc_typehints = "description"

smv_tag_whitelist = r"^v\d+\.\d+.*$|latest"
smv_branch_whitelist = r"^(?main).*$"
smv_released_pattern = r"v.*"
smv_remote_whitelist = r"^(origin)$"

# HTML -----------------------------------------------------------------

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/flask-jeroboam/"),
        ProjectLink("Source Code", "https://github.com/jcbianic/flask-jeroboam"),
        ProjectLink(
            "Issue Tracker", "https://github.com/jcbianic/flask-jeroboam/issues/"
        ),
    ]
}
# html_sidebars = {
#     "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
#     "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
# }
# singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]
html_favicon = "_static/img/jeroboam_icon.png"
html_logo = "_static/img/jeroboam_logo_with_text.png"
html_title = f"Flask-Jeroboam Documentation ({version})"
html_show_sourcelink = False


# CopyButton -----------------------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True


# MISCELLANEOUS -------------------------------------------------------------

autosectionlabel_prefix_document = True
