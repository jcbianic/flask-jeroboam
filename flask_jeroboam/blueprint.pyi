"""Flask-Jeroboam Blueprint.

Subclasses the Flask Blueprint.
Can be used as a drop in replacement of any Flask's Blueprint.
"""
import os
from typing import List
from typing import Optional
from typing import Union

from flask import Blueprint as FlaskBlueprint

from flask_jeroboam.scaffold import JeroboamScaffoldOverRide

_sentinel = object()

class Blueprint(JeroboamScaffoldOverRide, FlaskBlueprint):  # type:ignore
    def __init__(
        self,
        name: str,
        import_name: str,
        static_folder: Optional[Union[str, os.PathLike]] = None,
        static_url_path: Optional[str] = None,
        template_folder: Optional[Union[str, os.PathLike]] = None,
        url_prefix: Optional[str] = None,
        subdomain: Optional[str] = None,
        url_defaults: Optional[dict] = None,
        root_path: Optional[str] = None,
        cli_group: Optional[str] = _sentinel,  # type: ignore
        tags: Optional[List[str]] = None,
        include_in_openapi: bool = True,
    ) -> None: ...
