import json
import re
import typing as t
from enum import Enum
from functools import wraps
from typing import Callable
from typing import List
from typing import Type

from flask import request
from flask.globals import current_app
from pydantic import BaseModel
from typing_extensions import ParamSpec

from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.typing import JeroboamResponseReturnValue
from flask_jeroboam.typing import JeroboamRouteCallable

from .utils import get_typed_signature


F = t.TypeVar("F", bound=t.Callable[..., t.Any])
R = t.TypeVar("R", bound=t.Any)
P = ParamSpec("P")
T = t.TypeVar("T", bound=t.Any)


class MethodEnum(str, Enum):
    """List of HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


pattern = r"(.*)\[(.+)\]$"


class InboundHandler:
    """The InboundHandler handles inbound data of a request.

    More precisely, it parses the incoming data, validates it, and injects it into the
    view function. It is also responsible for raising an InvalidRequest exception.
    The InboundHandler will only be called if the view function has type-annotated
    parameters.
    """

    def __init__(self, view_func: Callable, methods: List[str], rule: str):
        self.typed_params = get_typed_signature(view_func)
        self.methods = methods
        self.rule = rule

    def __bool__(self) -> bool:
        return bool(self.typed_params.parameters)

    def __call__(self, func: JeroboamRouteCallable) -> JeroboamRouteCallable:
        """It injects inbound parsed and validated data into the view function."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> JeroboamResponseReturnValue:
            location = self._parse_incoming_request_data()
            kwargs = self._validate_inbound_data(location, kwargs)
            return current_app.ensure_sync(func)(*args, **kwargs)

        return wrapper

    def _parse_incoming_request_data(self) -> dict:
        """Getting the Data out of the Request Object."""
        if MethodEnum.GET in self.methods:
            location = dict(request.args.lists())
            location = self._rename_query_params_keys(location, pattern)
        elif MethodEnum.POST in self.methods:
            location = dict(request.form.lists())
            location = self._rename_query_params_keys(location, pattern)
            if request.data:
                # TODO: on.3.8.drop location |= dict(json.loads(request.data))
                location.update(dict(json.loads(request.data)))
            # TODO: on.3.8.drop location |= dict(request.files)  # type: ignore
            location.update(dict(request.files))  # type: ignore
        else:  # pragma: no cover
            # TODO: Statement cannot be reached at this point.
            location = {}
        return location

    def _validate_inbound_data(self, location, kwargs) -> dict:
        """Getting the Data out of the Request Object."""
        for arg_name, typed_param in self.typed_params.parameters.items():
            if getattr(typed_param.annotation, "__origin__", None) == t.Union:
                kwargs[arg_name] = self._validate_input(
                    typed_param.annotation.__args__[0], **location
                )
            elif issubclass(typed_param.annotation, BaseModel):
                kwargs[arg_name] = self._validate_input(
                    typed_param.annotation, **location
                )
            elif arg_name not in self.rule:
                kwargs[arg_name] = self._simple_validate_input(
                    typed_param.annotation, location, arg_name
                )
        return kwargs

    def _validate_input(self, model: Type[BaseModel], **kwargs: ParamSpec) -> BaseModel:
        try:
            return model(**kwargs)
        except ValueError as e:
            raise InvalidRequest(msg=str(e)) from e

    def _simple_validate_input(self, type_: T, payload: dict, key: str) -> T:
        try:
            return type_(payload.get(key, None))
        except ValueError as e:
            raise InvalidRequest(msg=str(e)) from e

    def _rename_query_params_keys(self, inbound_dict: dict, pattern: str) -> dict:
        """Rename keys in a dictionary."""
        renamings = []
        for key, value in inbound_dict.items():
            match = re.match(pattern, key)
            if len(value) == 1 and match is None:
                inbound_dict[key] = value[0]
            elif match is not None:
                new_key = f"{match[1]}[]"
                new_value = {match[2]: value[0]}
                renamings.append((key, new_key, new_value))
        for key, new_key, new_value in renamings:
            if new_key not in inbound_dict:
                inbound_dict[new_key] = [new_value]
            else:
                inbound_dict[new_key].append(new_value)
            del inbound_dict[key]
        return inbound_dict
