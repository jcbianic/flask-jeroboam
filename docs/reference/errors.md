# Error Handling

Error responses and validation exceptions.

## Validation Errors

When request validation fails, Jeroboam returns a 422 Unprocessable Entity response with details about what failed.

### Format

```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "Input should be a valid integer",
      "type": "int_parsing"
    }
  ]
}
```

**Fields:**

- `loc` (array): Location of the error (e.g., `["query", "field_name"]`)
- `msg` (string): Human-readable error message
- `type` (string): Error type code (e.g., `"int_parsing"`, `"string_type"`, `"value_error"`)

### Common Error Types

- `"int_parsing"` - Expected an integer
- `"float_parsing"` - Expected a float
- `"string_type"` - Expected a string
- `"bool_parsing"` - Expected a boolean
- `"list_type"` - Expected a list
- `"dict_type"` - Expected a dict
- `"value_error"` - Value violates constraints (e.g., `gt=0`)
- `"greater_than"` - Value is not greater than minimum
- `"less_than"` - Value is not less than maximum
- `"string_too_short"` - String is shorter than `min_length`
- `"string_too_long"` - String is longer than `max_length`
- `"string_pattern_mismatch"` - String doesn't match `pattern`
- `"missing"` - Required field is missing

---

## Response Validation Errors

When response validation fails (only in development), Jeroboam raises an error before sending the response.

**Example error:**

```
ValidationError: 1 validation error for WineOut
vintage
  Field required (type=missing)
```

This indicates your function returned data missing the `vintage` field.

---

## Custom Error Handlers

Use Flask's `@app.errorhandler` to customize error responses.

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(422)
def handle_validation_error(e):
    return {
        "error": "Validation failed",
        "details": e.description
    }, 422
```

---

## Raising Validation Errors

For custom validation in your functions:

```python
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

@app.post("/items")
def create_item(item: Item):
    if item.price < 0:
        raise BadRequest("Price cannot be negative")
    return item
```

---

## HTTP Exceptions

Standard Flask HTTP exceptions work normally.

```python
from werkzeug.exceptions import NotFound, Forbidden

@app.get("/items/<int:item_id>")
def get_item(item_id: int):
    if item_id < 0:
        raise NotFound("Item not found")
    return {"id": item_id}
```

These return appropriate HTTP status codes (404, 403, etc.) without triggering Jeroboam's validation error formatting.

---

## OpenAPI Error Documentation

Document error responses in OpenAPI with custom error descriptions.

```python
@app.get(
    "/items",
    responses={
        404: {"description": "Item not found"},
        500: {"description": "Server error"}
    }
)
def get_item():
    return {}
```

This adds error responses to the `/docs` documentation.
