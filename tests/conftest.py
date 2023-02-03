"""Defining Fixtures for the Test Suite."""
import pytest

from flask_jeroboam import Jeroboam

from .app_test.application_factory import create_test_app


@pytest.fixture
def app() -> Jeroboam:
    """The Jeroboam Test App."""
    return create_test_app()


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
