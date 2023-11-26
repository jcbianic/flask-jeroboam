import pytest

from flask_jeroboam import Form
from flask_jeroboam.jeroboam import Jeroboam


def test_form_param_on_get_raise_warning():
    """A warning is raised when a Form parameter is used on a GET view.

    GIVEN a GET view with a Form parameter
    WHEN registering the view
    THEN a warning is raised
    """
    with pytest.warns(UserWarning):
        app = Jeroboam(__name__)

        def form_on_get(not_allowed: str = Form(...)):
            return "OK"

        app.get("/form_on_get")(form_on_get)
