"""Customized exceptions for the Flask-Jeroboam package.

They are small wrappers around werkzeug HTTP exceptions that customize
how the message is colllected and formatted.
"""
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type

from pydantic import BaseModel
from pydantic import ValidationError
from pydantic import create_model
from pydantic.error_wrappers import ErrorList
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import NotFound


if TYPE_CHECKING:  # pragma: no cover
    from flask_jeroboam.jeroboam import Jeroboam


RequestErrorModel: Type[BaseModel] = create_model("Request")


class RessourceNotFound(NotFound):
    """A slightly modified version of Werkzeug's RessourceNotFound Exception."""

    def __init__(
        self,
        msg: Optional[str] = None,
        ressource_name: Optional[str] = None,
        context: Optional[str] = None,
    ):
        self.msg = msg
        self.ressource_name = ressource_name
        self.context = context
        self.response = None

    def __str__(self) -> str:
        return f"RessourceNotFound: {self.message}"

    @property
    def message(self) -> str:
        """Either format message or pass the msg property."""
        if self.msg is None:
            return f"{self.ressource_name} not found : {self.context}."
        else:
            return self.msg

    def handle(self) -> Tuple[str, int]:
        """Handle the exception and return a message to the user."""
        return str(self), 404


class InvalidRequest(ValidationError, BadRequest):
    """A slightly modifiedversion of Werkzeug's BadRequest Exception."""

    def __init__(self, errors: Sequence[ErrorList], *, body: Any = None):
        self.body = body
        self.response = None
        super().__init__(errors, RequestErrorModel)

    def handle(self) -> Tuple[dict, int]:
        """Handle the exception and return a message to the user."""
        return {"detail": self.errors()}, 400


class ServerError(InternalServerError):
    """A slightly modifiedversion of Werkzeug's InternalServerError Exception."""

    def __init__(
        self, msg: str, error: Exception, trace: str, context: Optional[str] = None
    ):
        self.msg = msg
        self.error = error
        self.trace = trace
        self.context = context
        self.response = None

    def __str__(self) -> str:
        return f"InternalServerError: {self.msg}"

    def handle(self) -> Tuple[str, int]:
        """Handle the exception and return a message to the user."""
        return str(self), 500


class ResponseValidationError(ServerError):
    """When an error occurs on Outbound Validation."""

    def __str__(self) -> str:
        return f"InternalServerError: {self.msg}"


class JeroboamError(Exception):
    """Base Exception for Flask-Jeroboam."""

    pass


def handle_404(e):
    """Simple Hanlder for 404 errors."""
    return {"message": "Not Found"}, 404


def handle_500(e):
    """Simple Hanlder for 500 errors."""
    return {"message": "Internal Error"}, 500


def register_error_handlers(app: "Jeroboam"):
    """Register error handlers for the app."""
    app.register_error_handler(InvalidRequest, InvalidRequest.handle)
    app.register_error_handler(RessourceNotFound, RessourceNotFound.handle)
    app.register_error_handler(ServerError, ServerError.handle)
    app.register_error_handler(ResponseValidationError, ResponseValidationError.handle)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
