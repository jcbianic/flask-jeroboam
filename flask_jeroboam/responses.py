"""Custom responses for Flask-Jeroboam."""
from flask import Response


class JeroboamResponse(Response):
    """Base class for all Jeroboam responses."""

    default_status_code = 200


class JSONResponse(JeroboamResponse):
    """Subclassing Flask Response for JSON responses."""

    default_mimetype = "application/json"


class HTMLResponse(JeroboamResponse):
    """Subclassing Flask Response for HTML responses."""

    default_mimetype = "text/html"
