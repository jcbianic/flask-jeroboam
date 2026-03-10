"""A Test Blueprint for testing mixed parameter locations.

Tests that path, query and body parameters are all resolved correctly
when used together in the same endpoint.
The corresponding tests are in tests/test_inbound_handler/test_mixed_parameters.py
"""

from pydantic import BaseModel

from flask_jeroboam import Blueprint, Query
from flask_jeroboam.view_arguments.functions import Body

router = Blueprint("mixed_router", __name__, tags=["Mixed"])


class ItemIn(BaseModel):
    name: str
    price: float


class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    q: str | None = None


@router.get("/mixed/<int:item_id>")
def get_item(item_id: int, q: str | None = None):
    """GET with path param (auto-detected) + optional query param."""
    return {"item_id": item_id, "q": q}


@router.put("/mixed/<int:item_id>", response_model=ItemOut)
def update_item(item_id: int, q: str | None = Query(None), item: ItemIn = Body()):
    """PUT with path param + explicit query param + required body.

    NOTE: q must use Query() explicitly — PUT's default location is body.
    Without Query(), q would be treated as a body field, not a query param.
    """
    return {"id": item_id, "name": item.name, "price": item.price, "q": q}
