# Design Philosophy

Flask-Jeroboam exists because we believed Flask needed a better way to handle request validation and response serialization without abandoning Flask's simplicity.

## The Problem We Solved

Flask gives you raw request data. You write code to validate it, transform it, coerce types, handle errors. The same dance, repeated across every endpoint. Developers either skip validation ("it's just for my internal API"), reinvent it per project, or layer on a framework like FastAPI.

But switching to FastAPI means leaving Flask's ecosystem. You lose Flask extensions, middleware patterns, existing code. Starting fresh is expensive.

Jeroboam asked: what if you could have Flask's flexibility with automatic validation built in? Not as a framework replacement, but as a natural extension of Flask itself.

## Why Type Hints, Not Schemas

Many frameworks (marshmallow, jsonschema) separate your schema from your code:

```python
# Schema defined separately
schema = ItemSchema()

# Function knows nothing about it
def create_item(data):
    item = schema.load(data)
    ...
```

Jeroboam makes your function signature the schema:

```python
def create_item(name: str, price: float = Field(..., gt=0)):
    ...
```

Why? Your signature already describes what you expect. Making it the source of truth means:

- No duplication (one place to update when requirements change)
- IDE support (your editor understands the types)
- Documentation (the signature is self-documenting)
- Less boilerplate (one annotation instead of field definitions in two places)

This is the same philosophy FastAPI uses. Jeroboam brings it to Flask.

## Why Pydantic

Pydantic does validation well. It handles type coercion, nested models, discriminated unions, computed fields, custom validators—dozens of edge cases we don't want to reinvent.

Pydantic v2 is fast and has good error messages. Rather than building yet another validation library, we integrated Pydantic as the core validation engine.

This is a deliberate tradeoff. Jeroboam brings Pydantic as a hard dependency. If you're already using it (and most modern Flask projects are), you get Jeroboam for free. If you're not, you pick up one dependency.

## Why Automatic Documentation

OpenAPI specs are useful but tedious to maintain. Teams write specs, then code drifts from the spec. Or the spec is never updated.

Jeroboam generates OpenAPI from your code. Rename a parameter, update the docs. Add a constraint, the docs show it. The docs can't be out of date because they're generated from what's actually running.

This is automatic, not optional. Every Jeroboam app gets documentation at `/docs` by default. Not because we love OpenAPI, but because generated docs that stay in sync are more valuable than manual docs that get stale.

## Compared to Alternatives

### FastAPI

FastAPI does what Jeroboam does but as a full framework. Pros: complete solution, excellent docs, large ecosystem. Cons: if you want to stay on Flask, you're out of luck. FastAPI isn't a Flask layer—it's a replacement.

Jeroboam is for teams who chose Flask and want its flexibility but also want validation and docs.

### flask-openapi3

Very similar positioning to Jeroboam. Also brings type hints and automatic OpenAPI to Flask. The main difference: we went with Pydantic models as the primary interface, while flask-openapi3 uses OpenAPI-first schemas.

Both are solid choices. The difference is philosophical—do you want your code to be Pydantic-centric or OpenAPI-centric?

### flask-restx

Older, marshmallow-based. Class-based views and decorators. Still popular, but heavier and less aligned with modern Python practices (type hints, dataclasses, Pydantic).

### Marshmallow

Tried-and-true, heavily used. But separate from your function signature, and requires manual schema definitions.

## What We Didn't Do

### No Magic Decorators on Parameters

Some frameworks require decorators on every parameter:

```python
def get_wines(
    page: int = Query(...),
    vintage: int = Query(...)
):
    ...
```

Jeroboam makes decorators optional. Undecorated parameters follow sensible defaults:
- GET requests: query parameters
- POST/PUT: body fields
- Path parameters: auto-detected from the URL

You can use decorators for clarity or to override defaults, but you don't need them for simple cases.

### No Custom Serialization Language

Some frameworks invent custom serialization syntax. Jeroboam uses Pydantic's field serializers, which are just Python methods:

```python
class WineOut(BaseModel):
    name: str
    vintage: int

    @field_serializer('vintage')
    def serialize_vintage(self, value):
        return f"Year {value}"
```

This is Python, not a DSL. If you know Python, you can read and write it.

### No Abandonment of Flask Conventions

Jeroboam is a Flask app. You use `@app.get()`, `request`, `g`, Flask middleware—all normal Flask. Nothing proprietary.

This means:
- Flask extensions work
- Your Flask knowledge transfers
- Migrating to or from Jeroboam is a refactoring, not a rewrite

## The Tradeoffs

Jeroboam trades simplicity in some areas for clarity in others.

**We added:** Pydantic as a dependency (small, fast, widely used)

**We removed:** Manual validation code in most functions

**We made implicit:** Type-to-location mapping (GET params are queries, POST params are body)

**We made explicit:** When you need to override (use `Query()`, `Body()`, etc.)

## Future Direction

Jeroboam aims to stay focused. We're not trying to be a full framework. We're trying to be the best way to add validation and documentation to Flask without changing Flask itself.

Where we might go:
- Better async support (Flask's story here is still evolving)
- Streaming response support
- GraphQL schema generation (maybe)

Where we won't go:
- Authentication/authorization (Flask extensions like Flask-Login exist)
- Database integration (use SQLAlchemy, Alembic—Flask is framework-agnostic)
- Full framework features (routing, middleware, templating—Flask does these)

Jeroboam is a layer on Flask, not a replacement for Flask.
