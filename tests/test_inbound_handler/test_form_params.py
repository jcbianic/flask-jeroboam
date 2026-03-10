from flask.testing import FlaskClient


def test_valid_payload_in_data_is_injected(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with a BaseModel FormParam
    WHEN hit with valid form data
    THEN the parsed input is injected into the view function.
    """
    response = client.post("/form/base_model", data={"page": 1, "type": "item"})

    assert response.json == {"page": 1, "type": "item"}
    assert response.status_code == 201


def test_single_primitive_form_param_is_injected(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with a single primitive Form param (embed=True)
    WHEN hit with valid form data
    THEN the parsed value is injected into the view function.
    """
    response = client.post("/form/single_primitive", data={"name": "Alice"})

    assert response.json == {"name": "Alice"}
    assert response.status_code == 201


def test_single_primitive_form_param_uses_default(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with a single primitive Form param with default
    WHEN hit without providing that field
    THEN the default value is used.
    """
    response = client.post("/form/single_primitive", data={})

    assert response.json == {"name": "John"}
    assert response.status_code == 201


def test_multiple_primitive_form_params_are_injected(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with multiple primitive Form params
    WHEN hit with valid form data
    THEN each value is injected as an individual kwarg.
    """
    response = client.post(
        "/form/primitives_in_form", data={"name": "Alice", "age": 25}
    )

    assert response.status_code == 201
    assert response.json == {"name": "Alice", "age": 25}


def test_multiple_primitive_form_params_use_defaults(
    client: FlaskClient,
):
    """GIVEN a POST endpoint with multiple primitive Form params with defaults
    WHEN hit without providing those fields
    THEN the default values are used.
    """
    response = client.post("/form/primitives_in_form", data={})

    assert response.status_code == 201
    assert response.json == {"name": "John", "age": 34}
