import traceback
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TypeVar

from flask import Response
from flask.globals import current_app
from pydantic import BaseModel
from typing_extensions import ParamSpec

from .exceptions import ServerError
from .typing import JeroboamResponseReturnValue
from .typing import JeroboamRouteCallable
from .typing import ResponseModel


# from .typing import TypedParams
# from .utils import get_typed_return_annotation


P = ParamSpec("P")
R = TypeVar("R")


class Serializer:
    """A Serializer Class for Flask-Jeroboam."""

    def __init__(self, func: Callable, options: Dict[str, Any]):
        self.response_model = self.get_response_model(func, options)

    def get_response_model(
        self, func: Callable, options: Dict[str, Any]
    ) -> Optional[ResponseModel]:
        """Extract the Response Model from view function.

        It takes it either explicitly from the options
        or from return type of the view function if it is
        a pydantic BaseModel.
        """
        response_model = options.pop("response_model", None)
        """if response_model is None:
            return_annotation = get_typed_return_annotation(func)
            if issubclass(return_annotation, BaseModel):
                response_model = return_annotation """
        return response_model

    def __bool__(self) -> bool:
        """Return True if the Serializer has a Response Model."""
        return bool(self.response_model)

    def _prepare_response(self, result: BaseModel, status: int = 200) -> Response:
        """Wraps simple Response initialisation."""
        return Response(result.json(), status=status, mimetype="application/json")

    def __call__(
        self, func: JeroboamRouteCallable, status_code: int
    ) -> JeroboamRouteCallable:
        """Return a view funcion."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> JeroboamResponseReturnValue:
            response = current_app.ensure_sync(func)(*args, **kwargs)
            if self.response_model is None:  # pragma: no cover
                return response
            elif isinstance(response, dict):
                try:
                    validated_response = self.response_model(**response)
                except ValueError as e:
                    raise ServerError(
                        msg="Internal server error",
                        error=e,
                        trace=traceback.format_exc(),
                        context=f"Trying to validate result with value {response}.",
                    ) from e
                return self._prepare_response(validated_response, status_code)
            elif isinstance(response, self.response_model):
                return self._prepare_response(response, status_code)
            else:
                return response

        return wrapper
