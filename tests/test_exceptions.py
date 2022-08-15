import pytest
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError

def test_invalid_request():
    e = InvalidRequest("User Message", context="Here's my Context")
    assert e.code == 400
    assert str(e) == "User Message"
    assert e.context == "Here's my Context"
        

def test_invalid_request_without_context():
    e = InvalidRequest("User Message")
    assert e.code == 400
    assert str(e) == "User Message"
    assert e.context is None


def test_ressource_not_found():
    e = RessourceNotFound("User Message")
    assert e.code == 404
    assert str(e) == "RessourceNotFound: User Message"


def test_ressource_not_found_with_formatted_context():
    e = RessourceNotFound(ressource_name="TestRessource", context="This is my Context")
    assert e.code == 404
    assert str(e) == "RessourceNotFound: TestRessource not found : This is my Context."


def test_internal_server_error():
    original_error = Exception("Original Error")
    e = ServerError("User Message", original_error, "Trace")
    assert e.code == 500
    assert str(e) == "InternalServerError: User Message"
    assert e.error == original_error
    assert e.trace == "Trace"