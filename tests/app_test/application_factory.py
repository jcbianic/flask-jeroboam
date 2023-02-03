"""Jeroboam Test App factory."""
import os

from flask_jeroboam import Jeroboam
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import ResponseValidationError
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError

from .apps.body import router as body_router
from .apps.cookies import router as cookies_router
from .apps.file import router as file_router
from .apps.form import router as form_router
from .apps.header import router as header_router
from .apps.misc import router as misc_router
from .apps.outbound import router as outbound_router
from .apps.path import router as path_router
from .apps.query import router as query_router


def create_test_app():
    """Jeroboam test app factory."""
    app = Jeroboam("jeroboam_test", root_path=os.path.dirname(__file__))
    app.config.update(
        TESTING=True,
    )
    # TODO: Add it by default with CONFIG OPT-OUT

    def handle_404(e):
        return {"message": "Not Found"}, 404

    app.register_error_handler(InvalidRequest, InvalidRequest.handle)
    app.register_error_handler(RessourceNotFound, RessourceNotFound.handle)
    app.register_error_handler(ServerError, ServerError.handle)
    app.register_error_handler(ResponseValidationError, ResponseValidationError.handle)
    app.register_error_handler(404, handle_404)

    @app.route("/api_route")
    def non_operation():
        return {"message": "Hello World"}

    @app.get("/text")
    def get_text():
        return "Hello World"

    # register blueprints.
    app.register_blueprint(body_router)
    app.register_blueprint(cookies_router)
    app.register_blueprint(file_router)
    app.register_blueprint(form_router)
    app.register_blueprint(header_router)
    app.register_blueprint(path_router)
    app.register_blueprint(query_router)
    app.register_blueprint(misc_router)
    app.register_blueprint(outbound_router)

    return app
