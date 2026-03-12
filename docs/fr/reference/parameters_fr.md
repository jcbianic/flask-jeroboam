# Paramètres de requête

Fonctions pour déclarer d'où proviennent les paramètres.

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

Déclare un paramètre de chaîne de requête.

**Exemple :**

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

Déclare un paramètre de corps de requête.

**Exemple :**

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

Déclare un paramètre de chemin. Généralement implicite mais peut être rendu explicite.

**Exemple :**

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

Déclare un paramètre d'en-tête HTTP.

**Exemple :**

```python
@app.get("/protected")
def get_protected(
    x_token: str = Header(...),
    x_user_id: int = Header(...)
):
    return {}
```

Les en-têtes avec des traits de soulignement sont convertis en tirets dans la requête HTTP. `x_token` correspond à l'en-tête `X-Token`.

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

Déclare un paramètre de cookie.

**Exemple :**

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

Déclare un paramètre de champ de formulaire (pour `application/x-www-form-urlencoded` ou `multipart/form-data`).

**Exemple :**

```python
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```
