"""Different types of responses for Flask."""
from flask.wrappers import Response


class HTMLResponse(Response):
    """HTML Response."""

    default_mimetype = "text/html"
    charset = "utf-8"
    direct_passthrough = False


class JSONResponse(Response):
    """JSON Response."""

    default_mimetype = "application/json"
    charset = "utf-8"
    direct_passthrough = False
