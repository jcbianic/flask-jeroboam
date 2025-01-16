"""A Test Blueprint for testing Form Params.

The corresponding test can be found in tests/test_inbound/test_form
"""

from flask_jeroboam import Blueprint
from flask_jeroboam import Form
from tests.app_test.models.inbound import SimpleModelIn


router = Blueprint("form_params_router", __name__, tags=["Form"])


@router.post("/form/base_model")
def post_base_model_in_form(form_payload: SimpleModelIn = Form(embed=False)):
    """POST Form Parameter as pydantic BaseModel."""
    return form_payload.json()


@router.post("/form/primitives_in_form")
def post_primitives_in_form(name: str = Form("John"), age: int = Form(34)):
    """POST Form Parameter as pydantic BaseModel."""
    return {"name": name, "age": age}
