import traceback
import typing as t
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from flask import Response
from pydantic import BaseModel
from typing_extensions import ParamSpec

from .exceptions import ServerError


P = ParamSpec("P")
R = TypeVar("R")
B = TypeVar("B", bound=BaseModel)


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


class Serializer:
    """The Serializer is responsible for serializing the response data."""

    def __init__(
        self,
        view_function: Callable,
        options: Dict[str, Any],
    ):
        self.view_function = view_function
        self.options = options
        self.status_code = options.get("status_code", 200)
        self.response_model = options.get("response_model", None)
        self.response_class = options.get("response_class", Response)
        if self.response_model is not None:
            self.processor = self._make_response
        else:
            self.processor = lambda x: x

    def is_body_allowed(self) -> bool:
        """Check if Body is allowed for the status code."""
        if self.status_code is None:
            return True
        current_status_code = int(self.status_code)
        return not (current_status_code < 200 or current_status_code in {204, 304})

    def _make_response(self, value: Union[Type, Dict]) -> Any:
        """Convert the value to json."""
        if self.response_model is None:
            return value
        if isinstance(value, self.response_model):
            response = self.response_class(value.dict())
        elif isinstance(value, dict):
            parsed_result = self.response_model(**value)
            response = self.response_class(parsed_result.dict())
        if not self.is_body_allowed():
            response.data = b""
        return response

    def __call__(self, raw_result: Any):
        """Add the serialization behavior to the endpoint."""
        return self._make_response(raw_result)
