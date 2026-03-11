# Jeroboam

The main application class.

## Jeroboam

```python
class Jeroboam(Flask)
```

A Flask subclass that adds request parsing, response validation, and OpenAPI documentation.

### Constructor

```python
Jeroboam(*args, **kwargs)
```

Takes the same parameters as `Flask`. See [Flask documentation](https://flask.palletsprojects.com/en/stable/api/#flask.Flask) for details.

On initialization, Jeroboam loads its configuration from `JeroboamConfig` (which reads environment variables) and merges it into `app.config`. Jeroboam-specific settings are configured via `app.config` after construction:

- `JEROBOAM_REGISTER_OPENAPI` (bool): Register OpenAPI endpoints. Default: `True`
- `JEROBOAM_REGISTER_ERROR_HANDLERS` (bool): Register validation error handlers. Default: `True`
- `JEROBOAM_OPENAPI_URL` (str): Path to interactive docs. Default: `/docs`
- `JEROBOAM_TITLE` (str): API title in OpenAPI schema. Default: `None`
- `JEROBOAM_VERSION` (str): API version. Default: `0.1.0`
- `JEROBOAM_DESCRIPTION` (str): API description. Default: `None`

### Methods

#### route

```python
def route(
    rule: str,
    **options
) -> Callable
```

Register a view function for a given URL rule. Works like Flask's `route()` decorator but adds request/response validation.

**Example:**

```python
@app.route("/items", methods=["GET"])
def list_items():
    return [{"id": 1, "name": "Item 1"}]
```

#### get, post, put, patch, delete, options, head

```python
def get(rule: str, **options) -> Callable
def post(rule: str, **options) -> Callable
def put(rule: str, **options) -> Callable
def patch(rule: str, **options) -> Callable
def delete(rule: str, **options) -> Callable
def options(rule: str, **options) -> Callable
def head(rule: str, **options) -> Callable
```

Shortcuts for HTTP methods. Each works like Flask's method decorators but with validation.

**Example:**

```python
@app.get("/wines/<int:wine_id>")
def get_wine(wine_id: int):
    return {"id": wine_id}

@app.post("/wines")
def create_wine(name: str, vintage: int):
    return {"name": name, "vintage": vintage}
```

#### add_url_rule

```python
def add_url_rule(
    rule: str,
    endpoint: str = None,
    view_func: Callable = None,
    **options
) -> None
```

Register a URL rule with a view function. Works like Flask's `add_url_rule()`.

### Properties

#### jeroboam_config

```python
@property
def jeroboam_config(self) -> dict
```

Returns Jeroboam-specific configuration.

---

## Blueprint

```python
class Blueprint(Flask.Blueprint)
```

A Blueprint subclass that adds request parsing and response validation.

Works exactly like Jeroboam but for organizing routes into modules. Use `blueprint.route()`, `blueprint.get()`, etc. the same way as Jeroboam.

**Example:**

```python
from flask_jeroboam import Blueprint

wines_bp = Blueprint("wines", __name__)

@wines_bp.get("/wines")
def list_wines():
    return []

app.register_blueprint(wines_bp)
```
