"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.

TODO: A probably better way to override it is to override the url_rule_class
with a custom JeroboamRule Object
"""
import os
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

from flask import Blueprint as FlaskBlueprint
from flask import Flask
from typing_extensions import TypeVar

from flask_jeroboam.openapi.models.openapi import OpenAPI
from flask_jeroboam.rule import JeroboamRule
from flask_jeroboam.typing import JeroboamRouteCallable

R = TypeVar("R", bound=Any)
_sentinel = object()

class JeroboamScaffoldOverRide:
    def route(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def get(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def post(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def put(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def delete(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def patch(
        self, rule: str, **options: Any
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...
    def _method_route(
        self,
        method: str,
        rule: str,
        options: dict,
    ) -> Callable[[JeroboamRouteCallable], JeroboamRouteCallable]: ...

class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    query_string_key_transformer: Callable
    open_api: OpenAPI
    def rules(self) -> List[JeroboamRule]: ...

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
