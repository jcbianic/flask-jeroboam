"""Defining Fixtures for the Test Suite."""

import pytest
from flask.testing import FlaskClient

from flask_jeroboam import Jeroboam
from tests.app_test.app import create_test_app


@pytest.fixture(scope="session")
def app() -> Jeroboam:
    """The Jeroboam Test App."""
    return create_test_app()


@pytest.fixture(scope="function")
def one_shot_app() -> Jeroboam:
    """The Jeroboam Test App."""
    return create_test_app()


@pytest.fixture(scope="function")
def one_shot_client(one_shot_app: Jeroboam) -> FlaskClient:
    """The Jeroboam Test App."""
    return one_shot_app.test_client()


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
def client(app: Jeroboam) -> FlaskClient:
    """Test Client from the Test App."""
    return app.test_client()
