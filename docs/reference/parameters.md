# Request Parameters

Functions for declaring where parameters come from.

## Query

```python
def Query(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    pattern: str = None,
    examples: List[Any] = None,
    deprecated: bool = None,
    ...
) -> Any
```

Declares a query string parameter.

**Example:**

```python
@app.get("/items")
def list_items(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return []
```

---

## Body

```python
def Body(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    examples: List[Any] = None,
    deprecated: bool = None,
    ...
) -> Any
```

Declares a request body parameter.

**Example:**

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item = Body(...)):
    return item
```

---

## Path

```python
def Path(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    gt: float = None,
    ge: float = None,
    lt: float = None,
    le: float = None,
    min_length: int = None,
    max_length: int = None,
    pattern: str = None,
    examples: List[Any] = None,
    deprecated: bool = None,
    ...
) -> Any
```

Declares a path parameter. Usually implicit but can be made explicit.

**Example:**

```python
@app.get("/items/<int:item_id>")
def get_item(item_id: int = Path(..., gt=0)):
    return {"id": item_id}
```

---

## Header

```python
def Header(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    ...
) -> Any
```

Declares an HTTP header parameter.

**Example:**

```python
@app.get("/protected")
def get_protected(
    x_token: str = Header(...),
    x_user_id: int = Header(...)
):
    return {}
```

Headers with underscores are converted to hyphens in the HTTP request. `x_token` matches the `X-Token` header.

---

## Cookie

```python
def Cookie(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    ...
) -> Any
```

Declares a cookie parameter.

**Example:**

```python
@app.get("/profile")
def get_profile(session_id: str = Cookie(...)):
    return {}
```

---

## Form

```python
def Form(
    default: Any = ...,
    *,
    alias: str = None,
    title: str = None,
    description: str = None,
    ...
) -> Any
```

Declares a form field parameter (for `application/x-www-form-urlencoded` or `multipart/form-data`).

**Example:**

```python
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```
