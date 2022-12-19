import json
import re
import typing as t
from enum import Enum
from functools import wraps

from flask import request
from pydantic import BaseModel
from typing_extensions import ParamSpec

from flask_jeroboam.exceptions import InvalidRequest


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


def _parse_input(model: t.Type[BaseModel], **kwargs: ParamSpec) -> BaseModel:
    try:
        return model(**kwargs)
    except ValueError as e:
        raise InvalidRequest(msg_to_user=str(e), context=str(kwargs)) from e


def _rename_keys(location: dict, pattern: str) -> dict:
    renamings = []
    for key, value in location.items():
        match = re.match(pattern, key)
        if len(value) == 1 and match is None:
            location[key] = value[0]
        elif match is not None:
            new_key = match.group(1) + "[]"
            new_value = {match.group(2): value[0]}
            renamings.append((key, new_key, new_value))
    for key, new_key, new_value in renamings:
        if new_key not in location:
            location[new_key] = [new_value]
        else:
            location[new_key].extend(new_value)
        del location[key]
    return location


def parser(
    method: MethodEnum, rule: str
) -> t.Callable[[t.Callable[..., R]], t.Callable[..., R]]:
    """Parametrize Decorator for parsing request data."""

    def parser_decorator(func: t.Callable[..., R]) -> t.Callable[..., R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if method == MethodEnum.GET:
                location = dict(request.args.lists())
                location = _rename_keys(location, pattern)
            elif method == MethodEnum.POST:
                location = dict(request.form)
                location.update(dict(json.loads(request.data)))
            else:
                location = {}
            for arg_name, arg_type in func.__annotations__.items():
                if issubclass(arg_type, BaseModel):
                    kwargs[arg_name] = _parse_input(arg_type, **location)
            return func(*args, **kwargs)

        return wrapper

    return parser_decorator
