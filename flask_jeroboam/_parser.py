import json
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


def parser(method: MethodEnum):
    """Parametrize Decorator for parsing request data."""

    def parser_decorator(func: t.Callable[P, R]) -> t.Callable[P, R]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if method == MethodEnum.GET:
                location = request.args
            elif method == MethodEnum.POST:
                data = dict(request.form)
                if request.content_type == "application/json":
                    data.update(json.loads(request.data))
                else:
                    data.update(dict(request.data))
                location = data
            else:
                location = {}
            for arg_name, arg_type in func.__annotations__.items():
                if issubclass(arg_type, BaseModel):
                    kwargs[arg_name] = _parse_input(arg_type, **location)
            return func(*args, **kwargs)

        return wrapper

    return parser_decorator
