# How Flask-Jeroboam Works Internally

Flask-Jeroboam sits between your view function and Flask's request/response cycle. When you decorate a function with `@app.get()`, Jeroboam wraps it with logic that inspects your function signature, extracts request data, validates it against your type hints, then validates the response before it leaves.

## The Three Stages of Request Handling

### 1. Registration Time (When the decorator runs)

When you write:

```python
@app.get("/wines/<int:wine_id>")
def get_wine(wine_id: int, include_notes: bool = False):
    ...
```

Jeroboam's `InboundHandler` runs immediately. It inspects your function's signature and builds a plan for how to handle requests. This is where the heavy lifting happens—it figures out that `wine_id` comes from the URL, that `include_notes` comes from query parameters, what types they should be, and what validations apply.

The key insight: we do expensive introspection once at registration, not on every request.

### 2. Request Time (When a request arrives)

A client hits your endpoint. Flask routes it, then Jeroboam's `JeroboamView` intercepts before your function runs. It:

1. Extracts data from the request (path parameters, query string, body, headers, cookies)
2. Passes it through the validation plan built at registration time
3. Calls your function with validated arguments
4. Catches the return value to validate the response

Your function sees clean, validated arguments. No defensive coding needed. If the request is invalid, Jeroboam returns a 422 error before your code runs.

### 3. Response Time (After your function returns)

Your function returns data. Jeroboam validates it against your response model, serializes it to JSON, and sends it back. If your function returns a wine missing a field, Jeroboam catches that in development and fails loudly.

This is a safety net—in production, misconfigured responses get caught early.

## Inside the Request Validator

Here's what happens in more detail when a request arrives.

### Gathering Data

Flask has already parsed the URL and extracted path parameters. Jeroboam adds:
- Query parameters (from `request.args`)
- Request body (from `request.get_json()`, using Pydantic's model validation)
- Headers (from `request.headers`)
- Cookies (from `request.cookies`)
- Path parameters (already parsed by Flask)

Each data source is kept separate—the plan built at registration time knows which parameter comes from where.

### The Validation Step

Here's where Pydantic enters. Jeroboam builds a temporary Pydantic model that has one field for each of your function parameters. For each source (query, body, headers), it creates a Pydantic model and validates the incoming data.

Why this approach? Pydantic is fast, thorough, and handles hundreds of edge cases we don't want to reinvent. We leverage it completely.

### Type Adaptation

Each parameter is wrapped in a `TypeAdapter`—Pydantic's tool for validating arbitrary types, not just BaseModel subclasses. This means you can accept lists, unions, literal strings, anything. Pydantic handles it.

## How Responses Are Validated

When you specify a `response_model`, Jeroboam doesn't let anything slip through.

```python
class WineOut(BaseModel):
    name: str
    vintage: int
    region: str = "Unknown"

@app.get("/wines/<int:wine_id>", response_model=WineOut)
def get_wine(wine_id: int):
    return {"name": "Château Lafite", "vintage": 2015}  # Missing region!
```

Your function returns a dict missing `region`. In development mode, Jeroboam throws an error. You see it immediately. In production, the response validation is still active by default, so misconfigured endpoints fail safely.

You can also return a list, nested structures, or any type your annotation supports:

```python
@app.get("/wines", response_model=List[WineOut])
def list_wines():
    ...
```

List validation uses Pydantic's `TypeAdapter` to handle the container and each element.

## The Registration Plan

At decoration time, Jeroboam builds a `SolvedArgument` for each parameter. This contains:

- Where the parameter comes from (query, body, path, header, cookie)
- The expected type and any validation constraints
- A Pydantic `TypeAdapter` ready to validate data
- Serialization metadata (field aliases, field exclusions, etc.)

This is precomputed. On every request, Jeroboam just runs the already-built validators. No signature introspection on each request.

## Why This Matters

The separation of registration time from request time gives Jeroboam several properties:

**Speed**: Expensive introspection happens once. Requests are fast.

**Clarity**: Your function signature is the source of truth. No separate schema files, no decorators on function parameters (unless you want them). Jeroboam reads your types and builds everything else.

**Safety**: Invalid requests are rejected before your code runs. Responses are checked. Bad data doesn't silently reach your business logic.

**Debugging**: Error messages are precise because Pydantic tells you exactly what failed and why. Not "bad request", but "field 'vintage' should be an integer, got 'abc'".

## Integration with Flask

Jeroboam subclasses Flask and Blueprint. When you use `Jeroboam(__name__)` instead of `Flask(__name__)`, you get the same Flask object with request parsing and response validation layered on top.

This means:
- Drop-in compatible with Flask middleware
- Works with Flask extensions
- Same `request` and `g` objects
- Decorators like `@app.before_request` work as expected

The wrapping happens at the view level—Flask's routing, middleware, and error handling are untouched.

## OpenAPI Generation

Jeroboam automatically generates OpenAPI specs and serves interactive documentation at `/docs`. How? By reading the information it already gathered at registration time.

Your function signature + type hints + response model + docstring + any explicit parameter descriptions = everything needed for OpenAPI. No separate schema definitions, no duplication.

The `/docs` endpoint reflects your actual API. Rename a parameter, and the docs update. Add a constraint to a Pydantic field, and the docs show it. This happens because Jeroboam is reading live from your code.

## A Note on Pydantic's Role

Pydantic handles the hard parts of validation: type coercion, constraint checking, nested model validation, discriminated unions, computed fields, serialization aliases, and much more.

Jeroboam sits on top, coordinating between Flask's request/response cycle and Pydantic's validation. You don't write validation code—your type hints and Pydantic models are the specification, and Pydantic enforces them automatically.
