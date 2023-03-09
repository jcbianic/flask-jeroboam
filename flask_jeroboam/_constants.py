from enum import Enum
from typing import Dict


class MethodEnum(str, Enum):
    """List of HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


REF_PREFIX = "#/components/schemas/"
METHODS_WITH_BODY = {"POST", "PUT", "PATCH", "DELETE"}
NO_BODY_STATUS_CODES = {"204", "205", "304"}

VALIDATION_ERROR_DEFINITION = {
    "title": "ValidationError",
    "type": "object",
    "properties": {
        "loc": {
            "title": "Location",
            "type": "array",
            "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        },
        "msg": {"title": "Message", "type": "string"},
        "type": {"title": "Error Type", "type": "string"},
    },
    "required": ["loc", "msg", "type"],
}

VALIDATION_ERROR_RESPONSE_DEFINITION = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "detail": {
            "title": "Detail",
            "type": "array",
            "items": {"$ref": f"{REF_PREFIX}ValidationError"},
        }
    },
}

status_code_ranges: Dict[str, str] = {
    "1XX": "Information",
    "2XX": "Success",
    "3XX": "Redirection",
    "4XX": "Client Error",
    "5XX": "Server Error",
    "DEFAULT": "Default Response",
}


METHODS_DEFAULT_STATUS_CODE = {
    "GET": 200,
    "HEAD": 200,
    "POST": 201,
    "PUT": 201,
    "DELETE": 204,
    "CONNECT": 200,
    "OPTIONS": 200,
    "TRACE": 200,
    "PATCH": 200,
}

NO_BODY_STATUS_CODES = {"204", "205", "304"}
