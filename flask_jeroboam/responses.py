"""A few wrappers arount Responses."""

from typing import Any

from flask import Response as BaseResponse


class Response(BaseResponse):
    """Flask Response Object with a render method."""

    charset = "utf-8"

    def render(self, content: Any) -> Any:
        """Default render method. Not Sure to use it in Flask Context"""
        if content is None:
            return b""
        if isinstance(content, bytes):
            return content
        return content.encode(self.charset)


class HTMLResponse(Response):
    """Response class for HTML."""

    default_mimetype = "text/html"


class JSONResponse(Response):
    """Response class for JSON."""

    default_mimetype = "application/json"


class FileResponse(Response):
    """Response class for files."""

    default_mimetype = "application/octet-stream"


class PlainTextResponse(Response):
    """Response class for plain text."""

    default_mimetype = "text/plain"


class RedirectResponse(Response):
    """Response class for redirects."""

    default_mimetype = "text/html"


class StreamingResponse(Response):
    """Response class for streaming."""

    default_mimetype = "text/html"


class CustomJSONResponse(JSONResponse):
    """Response class for UJSON."""

    def render(self, content: Any) -> bytes:
        """Overirde render method to use Custom JSON Module.

        Example:
        def render(self, content: Any) -> bytes:
           return ujson.dumps(content, ensure)
        def render(self, content: Any) -> bytes:
           return orjson.dumps(content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY)
        """
        raise NotImplementedError(
            "You must override render() with a custom JSON encoder."
        )
