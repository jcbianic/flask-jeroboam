# Jeroboam

The main application class.

## Jeroboam

```python
class Jeroboam(Flask)
```

A Flask subclass that adds request parsing, response validation, and OpenAPI documentation.

### Constructor

```python
Jeroboam(
    import_name: str,
    static_url_path: str = "/static",
    static_folder: str = "static",
    static_host: str = None,
    host_matching: bool = False,
    subdomain_matching: bool = False,
    template_folder: str = "templates",
    instance_path: str = None,
    instance_relative_config: bool = False,
    root_path: str = None,
    openapi_enabled: bool = True,
    openapi_url_prefix: str = "/",
    docs_url: str = "/docs"
)
```

**Parameters:**

- `import_name` (str): The module name for the application
- `openapi_enabled` (bool): Whether to generate OpenAPI docs. Default: `True`
- `openapi_url_prefix` (str): URL prefix for OpenAPI endpoints. Default: `/`
- `docs_url` (str): Path to interactive docs. Default: `/docs`

All other parameters are inherited from Flask.

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
