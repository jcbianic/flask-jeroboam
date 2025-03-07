"""A Test Blueprint for testing Cookie Params.

The corresponding test can be found in tests/test_inbound/test_cookie
"""

from flask_jeroboam import Blueprint
from flask_jeroboam import Cookie


router = Blueprint("cookies_params_router", __name__, tags=["Cookies"])


@router.get("/cookie/int")
def get_cookie_as_int(cookie: int = Cookie()):
    return {"cookie": cookie}


@router.get("/cookie/str")
def get_cookie_as_str(cookie: str = Cookie()):
    return {"cookie": cookie}
