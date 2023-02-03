import pytest


not_a_valid_int = {
    "detail": [
        {
            "loc": ["header", "Test-Header"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


def _valid(x):
    return {"header": x}


@pytest.mark.parametrize(
    "url,header_value,expected_status,expected_response",
    [
        ("/headers/str", {"test-header": "foobar"}, 200, _valid("foobar")),
        ("/headers/int", {"test-header": "123"}, 200, _valid(123)),
        ("/headers/int", {"test-header": "not_a_valid_int"}, 400, not_a_valid_int),
    ],
)
def test_get_headers(client, url, header_value, expected_status, expected_response):
    """Test Cookie Parameter with GET method.


    TODO: Allow Configuration of the returned Status Code.
    """
    response = client.get(url, headers=header_value)
    assert response.status_code == expected_status
    assert response.json == expected_response
