How to serialize responses
==========================

Flask-Jeroboam validates and serializes your responses using Pydantic models. This ensures your API returns data in the expected format and catches bugs before they reach clients.

Simple response models
----------------------

Define what your endpoint returns using Pydantic models:

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        id: int
        name: str
        price: float

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        item = fetch_item_from_db(item_id)
        return item

Jeroboam validates that your return value matches ItemOut. If a field is missing, an error is raised in development.

Lists and collections
---------------------

Return lists by wrapping the model in a list type:

.. code-block:: python

    from typing import List

    @app.get("/items", response_model=List[ItemOut])
    def list_items():
        items = fetch_all_items()
        return items

Field aliases
-------------

Serialize with different names than your Python fields:

.. code-block:: python

    from pydantic import BaseModel, Field

    class ItemOut(BaseModel):
        id: int
        item_name: str = Field(..., alias="name")
        price_usd: float = Field(..., alias="price")

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

Response JSON will be ``{"name": "...", "price": ...}`` even though your Python code uses different names.

Excluding fields
----------------

Sometimes you fetch more data than you want to return:

.. code-block:: python

    class ItemOut(BaseModel):
        id: int
        name: str
        price: float

        class Config:
            # Only these fields are included in responses
            fields = {"id", "name", "price"}

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        # Internal model might have secret_key, password, etc.
        item = fetch_item_internal(item_id)
        return item  # Only id, name, price are returned

Nested responses
----------------

Use nested models for complex structures:

.. code-block:: python

    from typing import List

    class AuthorOut(BaseModel):
        id: int
        name: str

    class BookOut(BaseModel):
        id: int
        title: str
        author: AuthorOut

    @app.get("/books/<int:book_id>", response_model=BookOut)
    def get_book(book_id: int):
        book = fetch_book_with_author(book_id)
        return book

The response will include the nested author object, automatically serialized.

Optional responses
------------------

Endpoints can return None sometimes:

.. code-block:: python

    from typing import Optional

    @app.get("/items/<int:item_id>", response_model=Optional[ItemOut])
    def get_item_if_exists(item_id: int):
        item = fetch_item(item_id)
        return item  # Could be None

Returning None will serialize to ``null`` in JSON.

Type coercion
-------------

Pydantic coerces values to match the model:

.. code-block:: python

    class ItemOut(BaseModel):
        id: int
        quantity: int

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        # fetch_item returns quantities as strings "42"
        item = fetch_item(item_id)
        return item  # Pydantic coerces "42" to 42

Your code returns strings but the response contains integers.

Computed fields
---------------

Add fields that are calculated on the fly:

.. code-block:: python

    from pydantic import computed_field

    class ItemOut(BaseModel):
        name: str
        quantity: int
        price_each: float

        @computed_field
        @property
        def total_value(self) -> float:
            return self.quantity * self.price_each

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        item = fetch_item(item_id)
        return item

The response includes ``total_value`` even though it's not in the database. It's computed from quantity and price_each.

Custom serializers
------------------

Transform data during serialization:

.. code-block:: python

    from datetime import datetime
    from pydantic import BaseModel, field_serializer

    class EventOut(BaseModel):
        name: str
        created_at: datetime

        @field_serializer('created_at')
        def serialize_datetime(self, value: datetime):
            return value.isoformat()

    @app.get("/events/<int:event_id>", response_model=EventOut)
    def get_event(event_id: int):
        event = fetch_event(event_id)
        return event

Datetimes are serialized as ISO strings instead of the default format.
