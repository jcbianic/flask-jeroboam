"""Testing path operations."""

import pytest

response_not_valid_bool = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be a valid boolean, unable to interpret input",
            "type": "bool_parsing",
        }
    ]
}

response_not_valid_int = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "type": "int_parsing",
        }
    ]
}

response_not_valid_float = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be a valid number, unable to parse string as a number",
            "type": "float_parsing",
        }
    ]
}

response_at_least_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "String should have at least 3 characters",
            "type": "string_too_short",
            "ctx": {"min_length": 3},
        }
    ]
}


response_at_least_2 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "String should have at least 2 characters",
            "type": "string_too_short",
            "ctx": {"min_length": 2},
        }
    ]
}


response_maximum_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "String should have at most 3 characters",
            "type": "string_too_long",
            "ctx": {"max_length": 3},
        }
    ]
}


response_greater_than_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be greater than 3",
            "type": "greater_than",
            "ctx": {"gt": 3.0},
        }
    ]
}


response_greater_than_0 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be greater than 0",
            "type": "greater_than",
            "ctx": {"gt": 0.0},
        }
    ]
}


response_greater_than_1 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be greater than 1",
            "type": "greater_than",
            "ctx": {"gt": 1.0},
        }
    ]
}


response_greater_than_equal_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be greater than or equal to 3",
            "type": "greater_than_equal",
            "ctx": {"ge": 3.0},
        }
    ]
}


response_less_than_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be less than 3",
            "type": "less_than",
            "ctx": {"lt": 3.0},
        }
    ]
}


response_less_than_0 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be less than 0",
            "type": "less_than",
            "ctx": {"lt": 0.0},
        }
    ]
}


response_less_than_equal_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "Input should be less than or equal to 3",
            "type": "less_than_equal",
            "ctx": {"le": 3.0},
        }
    ]
}


valid_foobar_str = {"item_id": "foobar"}
valid_42_str = {"item_id": "42"}
valid_true_str = {"item_id": "True"}
valid_true_bool = {"item_id": True}
valid_false_bool = {"item_id": False}
valid_42_int = {"item_id": 42}
valid_42_5_float = {"item_id": 42.5}


def _valid(x):
    return {"item_id": x}


not_found = {"message": "Not Found"}


@pytest.mark.parametrize(
    "url,expected_status,expected_response",
    [
        ("/path/foobar", 200, valid_foobar_str),
        ("/path/str/foobar", 200, valid_foobar_str),
        ("/path/str/42", 200, valid_42_str),
        ("/path/str/True", 200, valid_true_str),
        ("/path/int/foobar", 400, response_not_valid_int),
        ("/path/int/True", 400, response_not_valid_int),
        ("/path/int/42", 200, valid_42_int),
        ("/path/int/42.5", 400, response_not_valid_int),
        ("/path/float/foobar", 400, response_not_valid_float),
        ("/path/float/True", 400, response_not_valid_float),
        ("/path/float/42", 200, _valid(42.0)),
        ("/path/float/42.5", 200, valid_42_5_float),
        ("/path/bool/foobar", 400, response_not_valid_bool),
        ("/path/bool/True", 200, valid_true_bool),
        ("/path/bool/42", 400, response_not_valid_bool),
        ("/path/bool/42.5", 400, response_not_valid_bool),
        ("/path/bool/1", 200, valid_true_bool),
        ("/path/bool/0", 200, valid_false_bool),
        ("/path/bool/true", 200, valid_true_bool),
        ("/path/bool/False", 200, valid_false_bool),
        ("/path/bool/false", 200, valid_false_bool),
        ("/path/param/foo", 200, _valid("foo")),
        ("/path/param-required/foo", 200, _valid("foo")),
        ("/path/param-minlength/foo", 200, _valid("foo")),
        ("/path/param-minlength/fo", 400, response_at_least_3),
        ("/path/param-maxlength/foo", 200, _valid("foo")),
        ("/path/param-maxlength/foobar", 400, response_maximum_3),
        ("/path/param-min_maxlength/foo", 200, _valid("foo")),
        ("/path/param-min_maxlength/foobar", 400, response_maximum_3),
        ("/path/param-min_maxlength/f", 400, response_at_least_2),
        ("/path/param-gt/42", 200, valid_42_int),
        ("/path/param-gt/2", 400, response_greater_than_3),
        ("/path/param-gt0/0.05", 200, _valid(0.05)),
        ("/path/param-gt0/0", 400, response_greater_than_0),
        ("/path/param-ge/42", 200, valid_42_int),
        ("/path/param-ge/3", 200, _valid(3)),
        ("/path/param-ge/2", 400, response_greater_than_equal_3),
        ("/path/param-lt/42", 400, response_less_than_3),
        ("/path/param-lt/2", 200, _valid(2)),
        ("/path/param-lt0/-1", 200, _valid(-1)),
        ("/path/param-lt0/0", 400, response_less_than_0),
        ("/path/param-le/42", 400, response_less_than_equal_3),
        ("/path/param-le/3", 200, _valid(3)),
        ("/path/param-le/2", 200, _valid(2)),
        ("/path/param-lt-gt/2", 200, _valid(2)),
        ("/path/param-lt-gt/4", 400, response_less_than_3),
        ("/path/param-lt-gt/0", 400, response_greater_than_1),
        ("/path/param-le-ge/2", 200, _valid(2)),
        ("/path/param-le-ge/1", 200, _valid(1)),
        ("/path/param-le-ge/3", 200, _valid(3)),
        ("/path/param-le-ge/4", 400, response_less_than_equal_3),
        ("/path/param-lt-int/2", 200, _valid(2)),
        ("/path/param-lt-int/42", 400, response_less_than_3),
        ("/path/param-lt-int/2.7", 400, response_not_valid_int),
        ("/path/param-gt-int/42", 200, valid_42_int),
        ("/path/param-gt-int/2", 400, response_greater_than_3),
        ("/path/param-gt-int/2.7", 400, response_not_valid_int),
        ("/path/param-le-int/42", 400, response_less_than_equal_3),
        ("/path/param-le-int/3", 200, _valid(3)),
        ("/path/param-le-int/2", 200, _valid(2)),
        ("/path/param-le-int/2.7", 400, response_not_valid_int),
        ("/path/param-ge-int/42", 200, valid_42_int),
        ("/path/param-ge-int/3", 200, _valid(3)),
        ("/path/param-ge-int/2", 400, response_greater_than_equal_3),
        ("/path/param-ge-int/2.7", 400, response_not_valid_int),
        ("/path/param-lt-gt-int/2", 200, _valid(2)),
        ("/path/param-lt-gt-int/4", 400, response_less_than_3),
        ("/path/param-lt-gt-int/0", 400, response_greater_than_1),
        ("/path/param-lt-gt-int/2.7", 400, response_not_valid_int),
        ("/path/param-le-ge-int/2", 200, _valid(2)),
        ("/path/param-le-ge-int/1", 200, _valid(1)),
        ("/path/param-le-ge-int/3", 200, _valid(3)),
        ("/path/param-le-ge-int/4", 400, response_less_than_equal_3),
        ("/path/param-le-ge-int/2.7", 400, response_not_valid_int),
    ],
)
def test_get_path(client, url, expected_status, expected_response):
    """Test Path Operation with GET method.


    TODO: Allow Configuration of the returned Status Code.
    """
    response = client.get(url)
    assert response.status_code == expected_status
    assert response.json == expected_response


@pytest.mark.parametrize(
    "url,expected_status,expected_response",
    [
        ("/path/with_converter/foobar", 200, valid_foobar_str),
        ("/path/with_converter/str/foobar", 200, valid_foobar_str),
        ("/path/with_converter/str/42", 200, valid_42_str),
        ("/path/with_converter/str/True", 200, _valid("True")),
        ("/path/with_converter/int/42", 200, valid_42_int),
        ("/path/with_converter/float/42.5", 200, valid_42_5_float),
        ("/path/with_converter/param/foo", 200, _valid("foo")),
        ("/path/with_converter/param-required/foo", 200, _valid("foo")),
        ("/path/with_converter/param-minlength/foo", 200, _valid("foo")),
        ("/path/with_converter/param-minlength/fo", 400, response_at_least_3),
        ("/path/with_converter/param-maxlength/foo", 200, _valid("foo")),
        ("/path/with_converter/param-maxlength/foobar", 400, response_maximum_3),
        ("/path/with_converter/param-min_maxlength/foo", 200, _valid("foo")),
        ("/path/with_converter/param-min_maxlength/foobar", 400, response_maximum_3),
        ("/path/with_converter/param-min_maxlength/f", 400, response_at_least_2),
        ("/path/with_converter/param-gt/42.0", 200, _valid(42.0)),
        ("/path/with_converter/param-gt/2.0", 400, response_greater_than_3),
        ("/path/with_converter/param-gt0/0.05", 200, _valid(0.05)),
        ("/path/with_converter/param-gt0/0.0", 400, response_greater_than_0),
        ("/path/with_converter/param-ge/42.0", 200, _valid(42.0)),
        ("/path/with_converter/param-ge/3.0", 200, _valid(3.0)),
        ("/path/with_converter/param-ge/2.0", 400, response_greater_than_equal_3),
        ("/path/with_converter/param-lt/42.0", 400, response_less_than_3),
        ("/path/with_converter/param-lt/2.0", 200, _valid(2.0)),
        ("/path/with_converter/param-lt0/-1.0", 200, _valid(-1)),
        ("/path/with_converter/param-lt0/0.0", 400, response_less_than_0),
        ("/path/with_converter/param-le/42.0", 400, response_less_than_equal_3),
        ("/path/with_converter/param-le/3.0", 200, _valid(3)),
        ("/path/with_converter/param-le/2.0", 200, _valid(2)),
        ("/path/with_converter/param-lt-gt/2.0", 200, _valid(2)),
        ("/path/with_converter/param-lt-gt/4.0", 400, response_less_than_3),
        ("/path/with_converter/param-lt-gt/0.0", 400, response_greater_than_1),
        ("/path/with_converter/param-le-ge/2.0", 200, _valid(2)),
        ("/path/with_converter/param-le-ge/1.0", 200, _valid(1)),
        ("/path/with_converter/param-le-ge/3.0", 200, _valid(3)),
        ("/path/with_converter/param-le-ge/4.0", 400, response_less_than_equal_3),
        ("/path/with_converter/param-lt-int/2", 200, _valid(2)),
        ("/path/with_converter/param-lt-int/42", 400, response_less_than_3),
        ("/path/with_converter/param-gt-int/42", 200, _valid(42)),
        ("/path/with_converter/param-gt-int/2", 400, response_greater_than_3),
        ("/path/with_converter/param-le-int/42", 400, response_less_than_equal_3),
        ("/path/with_converter/param-le-int/3", 200, _valid(3)),
        ("/path/with_converter/param-le-int/2", 200, _valid(2)),
        ("/path/with_converter/param-ge-int/42", 200, valid_42_int),
        ("/path/with_converter/param-ge-int/3", 200, _valid(3)),
        ("/path/with_converter/param-ge-int/2", 400, response_greater_than_equal_3),
        ("/path/with_converter/param-lt-gt-int/2", 200, _valid(2)),
        ("/path/with_converter/param-lt-gt-int/4", 400, response_less_than_3),
        ("/path/with_converter/param-lt-gt-int/0", 400, response_greater_than_1),
        ("/path/with_converter/param-le-ge-int/2", 200, _valid(2)),
        ("/path/with_converter/param-le-ge-int/1", 200, _valid(1)),
        ("/path/with_converter/param-le-ge-int/3", 200, _valid(3)),
        ("/path/with_converter/param-le-ge-int/4", 400, response_less_than_equal_3),
    ],
)
def test_get_path_with_converter(client, url, expected_status, expected_response):
    """Test Path Operation with GET method.


    TODO: Allow Configuration of the returned Status Code.
    """
    response = client.get(url)
    assert response.json == expected_response
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "url,expected_status,expected_response",
    [
        ("/path/with_converter/int/foobar", 404, not_found),
        ("/path/with_converter/int/True", 404, not_found),
        ("/path/with_converter/int/42.5", 404, not_found),
        ("/path/with_converter/float/foobar", 404, not_found),
        ("/path/with_converter/float/True", 404, not_found),
        ("/path/with_converter/float/42", 404, not_found),
        ("/path/with_converter/param-le-int/2.7", 404, not_found),
        ("/path/with_converter/param-ge-int/2.7", 404, not_found),
        ("/path/with_converter/param-le-ge-int/2.7", 404, not_found),
    ],
)
def test_path_converter_error_override_jeroboam_validation(
    client, url, expected_status, expected_response
):
    """Test Url Converter Overides PathParams Validation.

    GIVEN a Path Parameter with both Path (Jeroboam) and Converter (Flask) validation
    WHEN the url is called with a value that does not match the converter
    THEN the converter error is returned (404), not the Jeroboam one (400)
    """
    response = client.get(url)
    assert response.json == expected_response
    assert response.status_code == expected_status
