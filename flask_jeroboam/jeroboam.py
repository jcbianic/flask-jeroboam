"""The Flask Object with augmented functionality around route registration.

Here we overide the route method of the Flask object to use our custom implementation.
This allow us to introduce new functionality to the route registration process.

TODO: A probably better way to override it is to override the url_rule_class
with a custom JeroboamRule Object
"""
from typing import Any
from typing import Callable
from typing import Optional

from flask import Flask
from typing_extensions import TypeVar

from flask_jeroboam._config import JeroboamConfig
from flask_jeroboam.exceptions import register_error_handlers
from flask_jeroboam.openapi.blueprint import register_open_api_blueprint
from flask_jeroboam.openapi.builder import build_openapi
from flask_jeroboam.openapi.models.openapi import OpenAPI
from flask_jeroboam.responses import JSONResponse
from flask_jeroboam.rule import JeroboamRule
from flask_jeroboam.scaffold import JeroboamScaffoldOverRide


R = TypeVar("R", bound=Any)


class Jeroboam(JeroboamScaffoldOverRide, Flask):  # type:ignore
    """A Flask Object with extra functionalities.

    The route method is overriden by a custom flask_jeroboam
    route decorator.
    """

    response_class = JSONResponse

    url_rule_class = JeroboamRule

    query_string_key_transformer: Optional[Callable] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self.config.update(JeroboamConfig.load().dict())
        self._openapi: Optional[OpenAPI] = None

    def init_app(self, app: Optional["Jeroboam"] = None) -> None:
        """Setup is performed after app has received all its configuration."""
        if self.config["JEROBOAM_REGISTER_ERROR_HANDLERS"]:
            register_error_handlers(self)  # type: ignore
        if self.config["JEROBOAM_REGISTER_OPENAPI"]:
            register_open_api_blueprint(self)  # type: ignore

    @property
    def openapi(self) -> OpenAPI:
        """Get the OpenApi object."""
        if self._openapi is None:
            self._openapi = build_openapi(
                app=self,  # type: ignore
                rules=list(self.url_map.iter_rules()),  # type: ignore
                tags=[],
            )
        return self._openapi
