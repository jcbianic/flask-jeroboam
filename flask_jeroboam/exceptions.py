"""Customized exceptions for the Flask-Jeroboam package.

They are small wrappers around werkzeug HTTP exceptions that customize
how the message is colllected and formatted.
"""
from typing import Optional

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


class InvalidRequest(BadRequest):
    """A slightly modifiedversion of Werkzeug's BadRequest Exception."""

    def __init__(self, msg_to_user: str, context: Optional[str] = None):
        self.msg_to_user = msg_to_user
        self.context = context

    def __str__(self) -> str:
        return f"BadRequest: {self.msg_to_user}"


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
