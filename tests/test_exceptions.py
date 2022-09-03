"""Testing Exceptions."""
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError


def test_invalid_request():
    """GIVEN an InvalidRequest exception
    WHEN I create an exception with a message and a context
    THEN I get the message while the context isa saved for logging
    """
    e = InvalidRequest("User Message", context="Here's my Context")
    assert e.code == 400
    assert str(e) == "BadRequest: User Message"
    assert e.context == "Here's my Context"


def test_invalid_request_without_context():
    """GIVEN an InvalidRequest exception
    WHEN I create an exception with only a mesage
    THEN the context is None
    """
    e = InvalidRequest("User Message")
    assert e.code == 400
    assert str(e) == "BadRequest: User Message"
    assert e.context is None


def test_ressource_not_found():
    """GIVEN an RessourceNotFound exceptione
    WHEN I create an exception with a mesage
    THEN I get a formatted string representation
    """
    e = RessourceNotFound("User Message")
    assert e.code == 404
    assert str(e) == "RessourceNotFound: User Message"


def test_ressource_not_found_with_formatted_context():
    """GIVEN an RessourceNotFound exception
    WHEN I create an exception with a ressource_name and a context
    THEN I get a extra-formatted string representation
    """
    e = RessourceNotFound(ressource_name="TestRessource", context="This is my Context")
    assert e.code == 404
    assert str(e) == "RessourceNotFound: TestRessource not found : This is my Context."


def test_internal_server_error():
    """GIVEN an ServerError exception
    WHEN I create an exception with a exception and a trace
    THEN I get acces to original error information
    """
    original_error = Exception("Original Error")
    e = ServerError("User Message", original_error, "Trace")
    assert e.code == 500
    assert str(e) == "InternalServerError: User Message"
    assert e.error == original_error
    assert e.trace == "Trace"
