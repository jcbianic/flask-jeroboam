# Response Configuration

Decorators and parameters for response handling.

## response_model

```python
response_model: Type[BaseModel] = None
```

Declares the response model for a route. Validates and serializes responses.

**Example:**

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    price: float

@app.get("/items", response_model=List[Item])
def list_items():
    return [
        {"id": 1, "name": "Item 1", "price": 9.99},
        {"id": 2, "name": "Item 2", "price": 19.99}
    ]
```

---

## status_code

```python
status_code: int = None
```

Sets the HTTP status code for successful responses.

**Example:**

```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return item
```

---

## response_description

```python
response_description: str = None
```

Sets the description of the response in OpenAPI documentation.

**Example:**

```python
@app.get("/items", response_description="List of all items")
def list_items():
    return []
```

---

## validate_response

```python
validate_response: bool = True
```

Enables or disables response validation. Default is `True`.

**Example:**

```python
@app.get("/fast", validate_response=False)
def fast_endpoint():
    # Response is not validated
    return {"data": "..."}
```

Disable this only if you're sure about response correctness and need to skip validation overhead.

---

## Configuring Response Serialization

Use Pydantic's model configuration to control serialization.

### by_alias

```python
class Item(BaseModel):
    internal_id: int = Field(alias="id")

    model_config = ConfigDict(by_alias=True)
```

Serializes fields using their aliases.

### exclude_none

```python
class Item(BaseModel):
    name: str
    description: str = None

    model_config = ConfigDict(exclude_none=True)
```

Excludes fields with `None` values from the response.

### exclude_unset

```python
class Item(BaseModel):
    name: str
    description: str = "Default"

    model_config = ConfigDict(exclude_unset=True)
```

Excludes fields that were not explicitly set.

---

## Field Serialization

Control how individual fields serialize.

### alias

```python
from pydantic import Field

class Item(BaseModel):
    internal_id: int = Field(alias="id")
```

Uses a different name in the JSON response.

### serialization_alias

```python
from pydantic import Field

class Item(BaseModel):
    internal_id: int = Field(
        validation_alias="internalId",
        serialization_alias="id"
    )
```

Uses different names for validation and serialization.

### field_serializer

```python
from pydantic import field_serializer

class Item(BaseModel):
    price: float

    @field_serializer('price')
    def serialize_price(self, value: float) -> str:
        return f"${value:.2f}"
```

Custom serialization logic for a field.
