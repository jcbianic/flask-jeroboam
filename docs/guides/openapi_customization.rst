How to customize API documentation
===================================

Flask-Jeroboam generates OpenAPI documentation automatically, but you can customize it to match your needs.

Adding descriptions
-------------------

Use docstrings to describe your endpoints:

.. code-block:: python

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        """
        Retrieve a single item by ID.

        Returns the item with all its details.
        """
        return fetch_item(item_id)

This docstring appears in the OpenAPI docs as the endpoint description.

Documenting parameters
----------------------

Add descriptions to parameters using Field:

.. code-block:: python

    from pydantic import Field

    class ItemFilter(BaseModel):
        page: int = Field(1, ge=1, description="Page number, starting from 1")
        limit: int = Field(10, ge=1, le=100, description="Max items per page")

    @app.get("/items")
    def list_items(filter: ItemFilter):
        return search_items(filter)

Parameters now appear in docs with descriptions and validation rules.

Response descriptions
---------------------

Document what your response contains:

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        """An item in the catalog."""
        id: int
        name: str = Field(..., description="The item's display name")
        price: float = Field(..., description="Price in USD")

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

The model docstring and field descriptions appear in the response schema.

Customizing endpoints
---------------------

Use additional decorator arguments to customize OpenAPI metadata:

.. code-block:: python

    @app.get(
        "/items",
        summary="List all items",
        tags=["items"]
    )
    def list_items():
        """Get a paginated list of all items in the catalog."""
        return fetch_all_items()

The summary is short; the docstring provides detail. Tags organize endpoints in the UI.

Grouping endpoints with tags
----------------------------

Use tags to organize related endpoints:

.. code-block:: python

    @app.get("/items", tags=["items"])
    def list_items():
        """List items."""
        return fetch_all_items()

    @app.post("/items", tags=["items"])
    def create_item(item: ItemCreate):
        """Create a new item."""
        return create_new_item(item)

    @app.get("/orders", tags=["orders"])
    def list_orders():
        """List orders."""
        return fetch_all_orders()

In the Swagger UI, endpoints are grouped under their tags.

Hiding endpoints from docs
--------------------------

Some endpoints might not be public. Exclude them:

.. code-block:: python

    @app.get("/internal/health")
    def health_check():
        """Check if the service is running."""
        return {"status": "ok"}

Endpoints are included by default. To hide one, use OpenAPI configuration.

Documenting errors
------------------

Describe what errors clients might receive:

.. code-block:: python

    from werkzeug.exceptions import NotFound

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int):
        """
        Retrieve an item by ID.

        Raises:
            404: Item not found
        """
        item = fetch_item(item_id)
        if not item:
            raise NotFound("Item not found")
        return item

Document your error cases so clients know what to expect.

Authentication in docs
----------------------

Mark endpoints that require authentication:

.. code-block:: python

    @app.get("/me")
    def get_current_user(authorization: str = Header(...)):
        """
        Get the current user's profile.

        Requires: Bearer token in Authorization header
        """
        user = verify_token(authorization)
        return user

The Authorization header appears in the docs as required.

Examples in docs
----------------

Show example requests and responses:

.. code-block:: python

    from pydantic import BaseModel

    class ItemOut(BaseModel):
        """An item."""
        id: int
        name: str
        price: float

        class Config:
            json_schema_extra = {
                "example": {
                    "id": 1,
                    "name": "Widget",
                    "price": 9.99
                }
            }

    @app.get("/items/<int:item_id>", response_model=ItemOut)
    def get_item(item_id: int):
        return fetch_item(item_id)

The example appears in the OpenAPI schema, visible in interactive docs.

Deprecating endpoints
---------------------

Mark endpoints that should no longer be used:

.. code-block:: python

    @app.get("/old-endpoint", deprecated=True)
    def old_endpoint():
        """
        This endpoint is deprecated.

        Use /new-endpoint instead.
        """
        return fetch_data()

Deprecated endpoints are visually marked in the Swagger UI.
