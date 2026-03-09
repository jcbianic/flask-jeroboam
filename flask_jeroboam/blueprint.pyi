"""Flask-Jeroboam Blueprint.

Subclasses the Flask Blueprint.
Can be used as a drop in replacement of any Flask's Blueprint.
"""

import os

from flask import Blueprint as FlaskBlueprint

from flask_jeroboam.scaffold import JeroboamScaffoldOverRide

_sentinel = object()

class Blueprint(JeroboamScaffoldOverRide, FlaskBlueprint):  # type:ignore
    def __init__(
        self,
        name: str,
        import_name: str,
        static_folder: str | os.PathLike | None = None,
        static_url_path: str | None = None,
        template_folder: str | os.PathLike | None = None,
        url_prefix: str | None = None,
        subdomain: str | None = None,
        url_defaults: dict | None = None,
        root_path: str | None = None,
        cli_group: str | None = _sentinel,  # type: ignore
        tags: list[str] | None = None,
        include_in_openapi: bool = True,
    ) -> None: ...
