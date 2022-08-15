import traceback
import typing as t
from functools import wraps
from typing import Callable
from typing import TypeVar

from flask import Response
from pydantic import BaseModel
from typing_extensions import ParamSpec

from .exceptions import ServerError


P = ParamSpec("P")
R = TypeVar("R")


def _prepare_response(result: BaseModel, status: int = 200) -> Response:
    """Wraps pydantic Serializer into flask Response Object."""
    try:
        return Response(result.json(), mimetype="application/json", status=status)
    except AttributeError as e:
        raise ServerError(
            msg="Internal server error",
            error=e,
            trace=traceback.format_exc(),
            context=f"Trying to jsonify result with value {result}.",
        ) from e


def serializer(response_model: t.Type[BaseModel], status_code: int = 200):
    """Parameterized decorator for view functions."""

    def serialize_decorator(
        func: Callable[P, t.Union[R, Response]]
    ) -> Callable[P, t.Union[R, Response]]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> t.Union[R, Response]:
            response = func(*args, **kwargs)
            if isinstance(response, dict):
                return _prepare_response(response_model(**response), status_code)
            elif isinstance(response, response_model):
                return _prepare_response(response, status_code)
            else:
                return response

        return inner

    return serialize_decorator
