# Alternatives & Comparison

Flask-Jeroboam exists in a space with several other libraries. This page gives you an honest comparison so you can pick the right tool for your situation.

## The Landscape

| Library        | Monthly Downloads | Approach                          | Pydantic       | Response Validation |
| -------------- | ----------------- | --------------------------------- | -------------- | ------------------- |
| flask-restx    | ~2.6M             | Class-based resources, Swagger UI | ❌ None        | ❌                  |
| flask-smorest  | ~1.3M             | Marshmallow-based, OpenAPI        | ❌ Marshmallow | ❌                  |
| flask-openapi3 | ~2.2M             | Named-model injection             | ✅ v2          | Opt-in              |
| apiflask       | ~227K             | Framework-level replacement       | Partial        | ❌                  |
| spectree       | ~252K             | Decorator-based validation        | ✅ v1+v2       | Opt-in              |
| flask-jeroboam | —                 | FastAPI-style per-parameter       | ✅ v2          | ✅ Default          |

---

## Flask-Jeroboam vs flask-openapi3

Flask-openapi3 is the closest functional alternative and worth understanding in depth before choosing between them.

### The Core Design Difference

The two libraries made opposite bets at the center of their parameter declaration API.

**flask-openapi3 uses reserved magic argument names.** You group all params of a given HTTP location into a single Pydantic model, then pass that model as a function argument whose _name_ tells the library where to look:

```python
# flask-openapi3
class BookQuery(BaseModel):
    page: int = 1
    per_page: int = 10

class BookBody(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(query: BookQuery, body: BookBody):
    # "query" and "body" are magic strings — the names drive location detection
    pass
```

**Flask-Jeroboam uses individual function parameters**, with location inferred from context (HTTP verb, route pattern) or declared explicitly per-parameter — the same pattern as FastAPI:

```python
# flask-jeroboam
@app.post("/books")
def create_book(page: int = 1, per_page: int = 10, title: str, author: str):
    # page, per_page → query (inferred: GET-style params)
    # title, author  → body (inferred: POST verb default)
    # No magic names, no wrapper models required
    pass
```

This is not just syntax sugar. The architectural choice has real consequences.

---

### Where Flask-Jeroboam Has a Structural Advantage

#### 1. Decorator and middleware composition

Flask-openapi3 validates requests by intercepting `**kwargs` at call time and treating everything as a path argument. This breaks any decorator that injects keyword arguments — authentication decorators, dependency injection frameworks, rate limiters. The result: unauthenticated requests return `422 Validation Error` instead of `401 Unauthorized` because validation runs before auth ([flask-openapi3 issue #111](https://github.com/luolingchun/flask-openapi3/issues/111), [#143](https://github.com/luolingchun/flask-openapi3/issues/143)).

Flask-Jeroboam resolves all parameter metadata at **registration time** (when the decorator runs), not at request time. The view function's signature is inspected once and a dedicated handler is built. Standard Flask decorators compose naturally.

#### 2. Response validation as a first-class feature

Flask-openapi3 was built for documentation generation; response validation was added later as an opt-in (`validate_response=True`). The implementation patches a flag onto the function object, and the PR that added it was immediately followed by an `AttributeError` bug ([#246](https://github.com/luolingchun/flask-openapi3/issues/246)).

Flask-Jeroboam has bidirectional validation from day one. The `OutboundHandler` is a peer to the `InboundHandler`, not an afterthought. Response validation is on by default — if your view returns data that doesn't match the declared `response_model`, you get a `ResponseValidationError` in development before it ever reaches a client.

#### 3. No Pydantic schema re-implementation

Flask-openapi3 re-implements Pydantic's schema traversal internally. This is the root cause of a recurring class of bugs: `@computed_field` properties disappearing from OpenAPI docs ([#139](https://github.com/luolingchun/flask-openapi3/issues/139)), tuples breaking after version bumps ([#183](https://github.com/luolingchun/flask-openapi3/issues/183)), field aliases stopping working for form data ([#182](https://github.com/luolingchun/flask-openapi3/issues/182)), and deprecation warnings from `Field(example=...)` ([#176](https://github.com/luolingchun/flask-openapi3/issues/176), [#177](https://github.com/luolingchun/flask-openapi3/issues/177)).

Flask-Jeroboam delegates schema generation to Pydantic's own `model_json_schema()` rather than reimplementing it. This class of bug cannot arise by design.

#### 4. Individual scalar parameters without wrapper models

In flask-openapi3, even a single query parameter requires wrapping in a `BaseModel`:

```python
# flask-openapi3 — you need a model for a single param
class PaginationQuery(BaseModel):
    page: int = 1

@app.get("/items")
def list_items(query: PaginationQuery):
    pass
```

In Flask-Jeroboam, individual scalars work directly:

```python
# flask-jeroboam — no wrapper needed
@app.get("/items")
def list_items(page: int = 1):
    pass
```

#### 5. HTTP-verb-based smart defaults

Flask-Jeroboam infers parameter location from the HTTP verb — `GET`/`HEAD`/`DELETE` default to query string; `POST`/`PUT`/`PATCH` default to request body. This removes the need to annotate most parameters explicitly, while still allowing overrides with `Query()`, `Body()`, `Header()`, etc.

---

### Where flask-openapi3 Has a Structural Advantage

**Pydantic v2 support.** Both libraries support Pydantic v2 natively. Flask-Jeroboam v0.2.0 completed a full migration to Pydantic v2 with no v1 compatibility layer.

**More documentation UI options.** Flask-openapi3 supports Swagger UI, ReDoc, RapiDoc, Scalar, and Elements. Flask-Jeroboam currently provides Swagger UI.

**Larger install base.** More users means more battle-testing, more Stack Overflow answers, and more likelihood your specific question has been asked before.

---

### Summary

Choose **flask-openapi3** if:

- You prefer explicit model-grouping over per-parameter declarations
- You need ReDoc, Scalar, or other UI options beyond Swagger

Choose **Flask-Jeroboam** if:

- You are familiar with FastAPI and want that exact parameter syntax
- You need response validation on by default, not opt-in
- You need clean decorator/middleware composition without validation ordering surprises
- You want Pydantic schema generation delegated to Pydantic itself, not re-implemented

---

## Flask-Jeroboam vs FastAPI

FastAPI is not a Flask extension — it is a separate framework built on Starlette/ASGI. Flask-Jeroboam is explicitly modelled after FastAPI's parameter syntax, so most FastAPI patterns transfer directly.

Choose **FastAPI** if:

- You are starting a new project with no Flask legacy
- You need native async/await throughout
- Performance from ASGI is a requirement

Choose **Flask-Jeroboam** if:

- You have an existing Flask codebase
- You depend on Flask-specific extensions (Flask-Login, Flask-Admin, Flask-SQLAlchemy, etc.)
- You use server-side rendering alongside your API
- You need WSGI deployment

---

## Flask-Jeroboam vs flask-smorest / flask-restx

These libraries are marshmallow-based (flask-smorest) or pre-type-hints in design (flask-restx). If your team is already using Pydantic for data modeling, the impedance mismatch with marshmallow schemas adds real overhead. Flask-Jeroboam lets you use the same Pydantic models for database layer, business logic, and API validation without translation.
