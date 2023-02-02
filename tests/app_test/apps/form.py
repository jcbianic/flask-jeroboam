"""A Test Blueprint for testing Form Params.

The corresponding test can be found in tests/test_inbound/test_form
"""
from flask_jeroboam import Form
from flask_jeroboam import JeroboamBlueprint
from tests.app_test.models.inbound import SimpleModelIn


router = JeroboamBlueprint("form_params_router", __name__)


@router.post("/form/base_model")
def post_base_model_in_form(payload: SimpleModelIn = Form()):
    """POST Form Parameter as pydantic BaseModel."""
    return payload.json()
