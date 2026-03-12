How to validate request data
============================

Flask-Jeroboam validates incoming requests automatically based on your function signatures and Pydantic models. This guide shows common patterns for validating different types of request data.

Simple scalar parameters
------------------------

For single values, use type hints directly on function arguments:

.. code-block:: python

    @app.get("/items")
    def get_items(page: int = 1, limit: int = 10):
        # page and limit are automatically validated as integers
        return fetch_items(page, limit)

Try passing invalid values to see automatic error responses:

.. code-block:: bash

    $ curl "http://localhost:5000/items?page=abc"
    {"detail":[{"loc":["query","page"],"msg":"Input should be a valid integer","type":"int_parsing"}]}

Query vs body parameters
------------------------

By default, GET requests use query parameters and POST requests use body parameters. If you need to mix them, be explicit:

.. code-block:: python

    from flask_jeroboam import Query, Body

    @app.post("/items")
    def create_item(
        # Query parameter (explicit)
        category: str = Query(...),
        # Body parameters (implicit for POST)
        name: str = Body(...),
        description: str = Body(...)
    ):
        return {"name": name, "description": description, "category": category}

Using Pydantic models
---------------------

For complex structures, use Pydantic models. This adds schema validation:

.. code-block:: python

    from pydantic import BaseModel, Field

    class ItemCreate(BaseModel):
        name: str
        description: str = None
        price: float = Field(..., gt=0)  # Must be greater than 0

    @app.post("/items")
    def create_item(item: ItemCreate):
        # item is validated and provides IDE autocomplete
        return {"created": item.name}

Field constraints
-----------------

Add validation rules directly in your model:

.. code-block:: python

    from pydantic import Field, EmailStr

    class UserCreate(BaseModel):
        email: EmailStr  # Automatically validated as email
        age: int = Field(..., ge=18, le=120)  # 18-120 range
        username: str = Field(..., min_length=3, max_length=20)
        bio: str = Field("", max_length=500)

Try creating a user with invalid data:

.. code-block:: bash

    $ curl -X POST http://localhost:5000/users \
      -H "Content-Type: application/json" \
      -d '{"email": "not-an-email", "age": 15}'
    {"detail":[{"loc":["body","email"],"msg":"value is not a valid email address"},{"loc":["body","age"],"msg":"Input should be greater than or equal to 18"}]}

Path parameters
---------------

Path parameters are detected automatically from the URL rule. No extra work needed:

.. code-block:: python

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        # item_id is automatically validated and injected
        return fetch_item(item_id)

Headers and cookies
-------------------

Validate custom headers or cookies the same way:

.. code-block:: python

    from flask_jeroboam import Header, Cookie

    @app.get("/protected")
    def get_protected(
        x_token: str = Header(...),
        session_id: str = Cookie(...)
    ):
        # Both validated automatically
        return {"token": x_token}

Conditional validation
----------------------

Use Pydantic's validators to add custom logic:

.. code-block:: python

    from pydantic import BaseModel, field_validator

    class EventCreate(BaseModel):
        name: str
        start_date: str
        end_date: str

        @field_validator('end_date')
        @classmethod
        def end_after_start(cls, v, info):
            if info.data.get('start_date') and v < info.data.get('start_date'):
                raise ValueError('end_date must be after start_date')
            return v

This ensures end_date is always after start_date, even if both dates are individually valid.

Optional fields
---------------

Make fields optional by using None as default:

.. code-block:: python

    from typing import Optional

    class ItemFilter(BaseModel):
        category: Optional[str] = None
        min_price: Optional[float] = None
        max_price: Optional[float] = None

    @app.get("/items")
    def search_items(filter: ItemFilter):
        # All fields are optional
        return search(filter)
