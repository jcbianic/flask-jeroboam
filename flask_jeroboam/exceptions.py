"""Customized exceptions for the Flask-Jeroboam package.

They are small wrappers around werkzeug HTTP exceptions that customize
how the message is colllected and formatted.
"""
from typing import Optional
from typing import Tuple

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import NotFound


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


class InvalidRequest(BadRequest):
    """A slightly modifiedversion of Werkzeug's BadRequest Exception."""

    def __init__(self, msg: Optional[str]):
        self.msg = msg

    def __str__(self) -> str:
        return f"BadRequest: {self.msg}"

    def handle(self) -> Tuple[str, int]:
        """Handle the exception and return a message to the user."""
        return str(self), 400


class ServerError(InternalServerError):
    """A slightly modifiedversion of Werkzeug's InternalServerError Exception."""

    def __init__(
        self, msg: str, error: Exception, trace: str, context: Optional[str] = None
    ):
        self.msg = msg
        self.error = error
        self.trace = trace
        self.context = context

    def __str__(self) -> str:
        return f"InternalServerError: {self.msg}"

    def handle(self) -> Tuple[str, int]:
        """Handle the exception and return a message to the user."""
        return str(self), 500
