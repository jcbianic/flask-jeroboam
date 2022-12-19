import json
import typing as t
from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict

from flask import request
from pydantic import BaseModel
from typing_extensions import ParamSpec

from flask_jeroboam.exceptions import InvalidRequest


F = t.TypeVar("F", bound=t.Callable[..., t.Any])
R = t.TypeVar("R", bound=t.Any)
P = ParamSpec("P")


class MethodEnum(str, Enum):
    """List of HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


def _parse_input(model: t.Type[BaseModel], **kwargs: ParamSpec) -> BaseModel:
    try:
        return model(**kwargs)
    except ValueError as e:
        raise InvalidRequest(msg_to_user=str(e), context=str(kwargs)) from e


class Parser:
    """The Parser is responsible for parsing incoming request data."""

    def __init__(
        self,
        view_function: Callable,
        options: Dict[str, Any],
    ):
        self.view_function = view_function
        self.options = options
        self.get_inbound: Callable = lambda: {}
        methods = options.get("methods", [])
        if MethodEnum.GET in methods:
            self.get_inbound = self._from_get
        elif MethodEnum.POST in methods:
            self.get_inbound = self._from_post

    def _from_get(self):
        inbound = request.args
        return inbound

    def _from_post(self):
        inbound = dict(request.form)
        if request.content_type == "application/json":
            inbound.update(json.loads(request.data))
        else:
            inbound.update(dict(request.data))
        return inbound

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Inject InboundData into the view function."""
        inbound = self.get_inbound()
        for arg_name, arg_type in self.view_function.__annotations__.items():
            if issubclass(arg_type, BaseModel):
                kwargs[arg_name] = _parse_input(arg_type, **inbound)
        return self.view_function(*args, **kwargs)
