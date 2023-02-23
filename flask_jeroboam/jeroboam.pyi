"""Stub File for Jeroboam."""
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from flask import Flask
from typing_extensions import TypeVar

from flask_jeroboam.openapi.models.openapi import OpenAPI
from flask_jeroboam.rule import JeroboamRule
from flask_jeroboam.scaffold import JeroboamScaffoldOverRide

R = TypeVar("R", bound=Any)
_sentinel = object()
current_app: Jeroboam

class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    query_string_key_transformer: Callable
    openapi: OpenAPI
    def rules(self) -> List[JeroboamRule]: ...
    def init_app(self, app: Optional["Jeroboam"] = None) -> None: ...
