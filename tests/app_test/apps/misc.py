"""A Test Blueprint for testing Misc Behavior."""

from flask_jeroboam import Blueprint
from flask_jeroboam.exceptions import RessourceNotFound
from flask_jeroboam.exceptions import ServerError


router = Blueprint("misc_router", __name__, tags=["Misc"])


@router.get("/invalid_request")
def get_invalid_request(missing_param: int):
    return {"missing_param": missing_param}


@router.get("/ressource_not_found")
def get_ressource_not_found():
    raise RessourceNotFound(ressource_name="TestRessource", context=f"with id {id}")


@router.get("/generic_ressource")
def get_generic_ressource_not_found():
    raise RessourceNotFound(msg="My Message")


@router.get("/server_error")
def get_a_server_error():
    raise ServerError(msg="My Message", error=Exception(), trace="FakeTrace")


@router.delete("/delete")
def delete():
    return {}
