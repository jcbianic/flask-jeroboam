"""Jeroboam Test App factory."""
import os

from toml import load as load_toml  # type: ignore

from flask_jeroboam import Jeroboam
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
    app.register_blueprint(openapi_test_router)

    app.init_app()

    return app
