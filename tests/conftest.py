"""Configuration File for pytest."""
import os

import pytest

from flask_jeroboam import APIBlueprint
from flask_jeroboam import Jeroboam
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError


@pytest.fixture
def app() -> Jeroboam:
    """A Basic Jeroboam Test App."""
    app = Jeroboam("jeroboam_test", root_path=os.path.dirname(__file__))
    app.config.update(
        TESTING=True,
        SECRET_KEY="RandomSecretKey",
    )
    app.register_error_handler(InvalidRequest, InvalidRequest.handle)
    app.register_error_handler(RessourceNotFound, RessourceNotFound.handle)
    app.register_error_handler(ServerError, ServerError.handle)
    return app


@pytest.fixture
def blueprint() -> APIBlueprint:
    """A Basic Jeroboam Test App."""
    return APIBlueprint("TestBluePrint", __name__)


@pytest.fixture
def app_ctx(app: Jeroboam):
    """Application Context from the Test App."""
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def request_context(app: Jeroboam):
    """Request Context from the Test App."""
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app: Jeroboam):
    """Test Client from the Test App."""
    return app.test_client()
