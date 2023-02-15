"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.

TODO: A probably better way to override it is to override the url_rule_class
with a custom JeroboamRule Object
"""
import os
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from flask import Blueprint as FlaskBlueprint
from flask import Flask
from typing_extensions import TypeVar

from .jeroboam import JeroboamScaffoldOverRide

R = TypeVar("R", bound=Any)
_sentinel = object()

class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    ...

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

def current_app() -> Jeroboam: ...
