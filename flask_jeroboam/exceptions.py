from typing import Any, Dict, Optional

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import NotFound


class RessourceNotFound(NotFound):
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
        if self.msg is None:
            return f"{self.ressource_name} not found : {self.context}."
        else:
            return self.msg


class InvalidRequest(BadRequest):
    def __init__(self, msg_to_user: str, context: Optional[str] = None):
        self.msg_to_user = msg_to_user
        self.context = context

    def __str__(self) -> str:
        return f"{self.msg_to_user}"


class ServerError(InternalServerError):
    def __init__(
        self, msg: str, error: Exception, trace: str, context: Optional[str] = None
    ):
        self.msg = msg
        self.error = error
        self.trace = trace
        self.context = context

    def __str__(self) -> str:
        return f"InternalServerError: {self.msg}"
