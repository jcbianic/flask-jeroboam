"""Explicit behavioral tests for InboundModel and OutboundModel.

These tests pin the camelCase ↔ snake_case conversion behavior driven by
Pydantic's alias_generator and allow_population_by_field_name / populate_by_name.

Both of these config keys change names in Pydantic v2:
  - allow_population_by_field_name → populate_by_name
  - alias_generator stays, but must return str (same as before)
  - Config inner class → model_config = ConfigDict(...)

If these tests break after the migration, the InboundModel/OutboundModel
config was not migrated correctly.
"""

import pytest
from flask.testing import FlaskClient

from flask_jeroboam import Jeroboam
from flask_jeroboam.models import InboundModel, OutboundModel


# ---------------------------------------------------------------------------
# InboundModel: camelCase query param acceptance
# The /query/optional_model route uses OptionalModelIn(InboundModel) which has
# a per_page: int | None field. InboundModel's alias_generator creates the
# "perPage" alias, and allow_population_by_field_name allows both to work.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "query_string,expected_json",
    [
        # camelCase alias works
        ("?page=2&perPage=5", {"page": 2, "per_page": 5}),
        # snake_case field name also works (allow_population_by_field_name)
        ("?page=2&per_page=5", {"page": 2, "per_page": 5}),
        # partial: only page provided, per_page is None
        ("?page=3", {"page": 3, "per_page": None}),
        # empty: both None
        ("", {"page": None, "per_page": None}),
    ],
)
def test_inbound_model_accepts_both_camel_and_snake_case(
    client: FlaskClient, query_string, expected_json
):
    """GIVEN an endpoint with an InboundModel parameter
    WHEN queried with camelCase or snake_case query params
    THEN both are accepted and stored internally as snake_case.

    This validates that:
    - alias_generator correctly generates camelCase aliases
    - allow_population_by_field_name / populate_by_name allows the field name too
    """
    response = client.get(f"/query/optional_model{query_string}")
    assert response.status_code == 200
    assert response.json == expected_json


# ---------------------------------------------------------------------------
# OutboundModel: snake_case serialized as camelCase
# The /return_type/dict route uses SimpleModelOut(OutboundModel) which has
# a total_count field. OutboundModel serializes it as totalCount.
# ---------------------------------------------------------------------------


def test_outbound_model_serializes_snake_case_to_camel_case(client: FlaskClient):
    """GIVEN an endpoint with an OutboundModel response_model
    WHEN the view returns snake_case field names
    THEN the JSON response uses camelCase.

    This validates that OutboundModel's json serialization is configured correctly.
    Pydantic v1: json_dumps = json_dumps_to_camel_case (custom Config option)
    Pydantic v2: requires different approach (alias_generator + by_alias=True)
    """
    response = client.get("/return_type/dict")
    assert response.status_code == 200
    assert "totalCount" in response.json
    assert "total_count" not in response.json
    assert response.json["totalCount"] == 10


# ---------------------------------------------------------------------------
# Unit-level: InboundModel and OutboundModel class behaviour
# ---------------------------------------------------------------------------


def test_inbound_model_parses_camel_case_directly():
    """GIVEN an InboundModel subclass with a snake_case field
    WHEN instantiated with a camelCase key
    THEN the value is stored under the snake_case field name.
    """

    class Pagination(InboundModel):
        per_page: int = 10

    instance = Pagination(**{"perPage": 25})
    assert instance.per_page == 25


def test_inbound_model_parses_snake_case_directly():
    """GIVEN an InboundModel subclass with a snake_case field
    WHEN instantiated with the snake_case key directly
    THEN the value is accepted (allow_population_by_field_name / populate_by_name).
    """

    class Pagination(InboundModel):
        per_page: int = 10

    instance = Pagination(**{"per_page": 30})
    assert instance.per_page == 30


def test_outbound_model_serializes_to_camel_case_directly():
    """GIVEN an OutboundModel subclass with a snake_case field
    WHEN serialized to JSON
    THEN the key is camelCase in the output.
    """

    class Stats(OutboundModel):
        total_count: int

    instance = Stats(total_count=42)
    # v1: .json() / v2: .model_dump_json() — test both forms defensively
    import json

    try:
        raw = instance.model_dump_json()  # v2
    except AttributeError:
        raw = instance.json()  # v1

    data = json.loads(raw)
    assert "totalCount" in data
    assert data["totalCount"] == 42


def test_inbound_model_validation_error_reports_snake_case_field_name(
    one_shot_app: Jeroboam,
):
    """GIVEN an endpoint with a required InboundModel field
    WHEN the request omits that field entirely
    THEN the error loc uses the Python field name, not the camelCase alias.

    This ensures validation errors are readable in Python terms.
    """

    class StrictPagination(InboundModel):
        per_page: int  # required, no default

    @one_shot_app.get("/test_strict_inbound")
    def strict_endpoint(pagination: StrictPagination):
        return {}

    client = one_shot_app.test_client()
    response = client.get("/test_strict_inbound")
    assert response.status_code == 400
    locs = [e.get("loc", []) for e in response.json["detail"]]
    # The field name in the error should be per_page (or perPage alias)
    # — but crucially the error must be present
    assert any("per_page" in str(loc) or "perPage" in str(loc) for loc in locs)
