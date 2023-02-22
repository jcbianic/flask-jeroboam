"""Jeroboam Test App factory."""
import os

from toml import load as load_toml  # type: ignore

from flask_jeroboam import Jeroboam
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import ResponseValidationError
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError
from flask_jeroboam.openapi.blueprint import router as openapi_router
from tests.app_test.apps.body import router as body_router
from tests.app_test.apps.cookies import router as cookies_router
from tests.app_test.apps.file import router as file_router
from tests.app_test.apps.form import router as form_router
from tests.app_test.apps.header import router as header_router
from tests.app_test.apps.misc import router as misc_router
from tests.app_test.apps.openapi import router as openapi_test_router
from tests.app_test.apps.outbound import router as outbound_router
from tests.app_test.apps.path import router as path_router
from tests.app_test.apps.query import router as query_router


def create_test_app():
    """Jeroboam test app factory."""
    app = Jeroboam("jeroboam_test", root_path=os.path.dirname(__file__))
    app.config.update(
        TESTING=True,
    )
    app.config.from_file("openapi.toml", load=load_toml)

    # TODO: Add it by default with CONFIG OPT-OUT

    def handle_404(e):
        return {"message": "Not Found"}, 404

    app.register_error_handler(InvalidRequest, InvalidRequest.handle)
    app.register_error_handler(RessourceNotFound, RessourceNotFound.handle)
    app.register_error_handler(ServerError, ServerError.handle)
    app.register_error_handler(ResponseValidationError, ResponseValidationError.handle)
    app.register_error_handler(404, handle_404)

    @app.route("/api_route", tags=["Base"])
    def non_operation():
        return {"message": "Hello World"}

    @app.get("/text", tags=["Base"])
    def get_text():
        return "Hello World"

    def non_decorated_route():
        return {"message": "Hello World"}

    app.add_url_rule("/non_decorated_route", view_func=non_decorated_route)

    app.register_blueprint(body_router)
    app.register_blueprint(cookies_router)
    app.register_blueprint(file_router)
    app.register_blueprint(form_router)
    app.register_blueprint(header_router)
    app.register_blueprint(path_router)
    app.register_blueprint(query_router)
    app.register_blueprint(misc_router)
    app.register_blueprint(outbound_router)
    app.register_blueprint(openapi_router)
    app.register_blueprint(openapi_test_router)

    return app
