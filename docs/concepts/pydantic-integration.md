# Why and How We Use Pydantic

Pydantic is the backbone of Flask-Jeroboam. Understanding how we use it helps explain design choices and what's possible.

## What Pydantic Does

Pydantic validates Python objects against a schema. You define a model with fields and types:

```python
from pydantic import BaseModel

class Wine(BaseModel):
    name: str
    vintage: int
    region: str = "Unknown"
```

Then you validate data:

```python
wine = Wine(**{"name": "Château Lafite", "vintage": "2015"})
# Pydantic coerces "2015" to 2015
# wine.vintage is now an int
```

If data is invalid, Pydantic raises an error with details about what failed.

That's the core insight: Pydantic turns validation into a declarative problem. You describe what you want (type hints), and Pydantic enforces it.

## Why This Matters for Request Validation

Flask gives you raw request data as strings and dicts:

```python
# request.args is {"page": "1", "limit": "10"}
# request.get_json() is {"name": "Château Lafite", "vintage": "2015"}
```

Everything is a string or nested dict. No types. No validation.

Your function signature says what you need:

```python
def list_wines(page: int = 1, limit: int = 10):
    ...
```

Jeroboam bridges this gap. It uses Pydantic to:
1. Build a validation model from your function signature
2. Extract and validate request data
3. Pass validated arguments to your function

You don't write validation code. Pydantic handles the mapping.

## Why TypeAdapter

In Pydantic v2, `TypeAdapter` is the tool for validating arbitrary types without BaseModel:

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(int)
result = adapter.validate_python("42")  # 42
```

Jeroboam uses TypeAdapter for every parameter. Why? Because function parameters can be anything:

```python
def get_user(user_id: int):
    # Simple type
    ...

def search(tags: List[str] = Query(...)):
    # Complex type
    ...

def process(config: Dict[str, Any] = Body(...)):
    # Nested dict
    ...
```

BaseModel only works for classes. TypeAdapter works for any type—scalars, lists, unions, custom classes. That's the flexibility Jeroboam provides.

## Why FieldInfo

Pydantic v2's `FieldInfo` is the metadata object that describes constraints on a field:

```python
from pydantic import Field

page: int = Field(1, ge=1, le=100)
```

That `Field(...)` call returns a `FieldInfo` object with information about defaults, constraints, descriptions, aliases, etc.

Jeroboam's `Query`, `Body`, `Header`, etc. are subclasses of `FieldInfo`. When you write:

```python
page: int = Query(1, ge=1)
```

You're providing Pydantic metadata that describes this parameter. Jeroboam reads that metadata and builds validation rules from it.

The benefit: you use Pydantic's constraint system directly. `Field(ge=1, le=100)` means "greater than or equal to 1, less than or equal to 100." The same syntax works in response models, body parameters, query parameters—everywhere.

## Validation at Registration vs. Request Time

Here's where the design gets interesting. Jeroboam does validation work at two times:

### Registration Time (when you decorate the function)

```python
@app.get("/wines")
def list_wines(page: int = 1):
    ...
```

Jeroboam inspects your signature immediately. It:
- Reads the type hint (`int`)
- Reads any metadata (`Field(...)`, `Query(...)`, etc.)
- Builds a Pydantic `TypeAdapter` for that parameter
- Stores this in a `SolvedArgument` (a pre-built validation plan)

This is expensive work, but it happens once.

### Request Time (when a request arrives)

The request comes in. Jeroboam:
1. Extracts the parameter from the appropriate source (query, body, headers)
2. Runs the pre-built TypeAdapter
3. Passes the validated value to your function

This is fast because the heavy lifting is done.

The insight: validate once at registration, use many times at request time.

## How Pydantic Handles Request Bodies

When you accept a Pydantic model in your request:

```python
class WineCreate(BaseModel):
    name: str
    price: float

@app.post("/wines")
def create_wine(wine: WineCreate):
    ...
```

Jeroboam doesn't pass the raw request JSON to your function. It:
1. Extracts the JSON body
2. Passes it to Pydantic's `WineCreate.model_validate(data)`
3. Pydantic validates and returns a `WineCreate` instance
4. Passes that instance to your function

Your function receives a fully validated object with properties like `wine.name` and `wine.price`.

## How Pydantic Handles Multiple Parameters

You can mix simple parameters with Pydantic models:

```python
@app.post("/wines")
def create_wine(
    wine: WineCreate,
    skip_notification: bool = Query(False)
):
    ...
```

Jeroboam builds a temporary Pydantic model that has both `wine` (a nested WineCreate model) and `skip_notification` (a boolean from the query string). Then it aggregates the data from both sources and validates everything together.

This is why Jeroboam can handle complex scenarios without custom code.

## Response Validation with Pydantic

On the way out, your function returns data. Jeroboam validates it:

```python
class WineOut(BaseModel):
    name: str
    vintage: int

@app.get("/wines/<int:wine_id>", response_model=WineOut)
def get_wine(wine_id: int):
    return {"name": "Château Lafite", "vintage": 2015}
```

Jeroboam calls `WineOut.model_validate(response_data)`. If validation fails, it raises an error (in development mode, loudly).

This catches bugs where your function returns data that doesn't match the schema. In production, you can turn this off if you're confident (though we don't recommend it).

## Serialization Aliases

Pydantic models can have different field names in Python vs. JSON:

```python
class WineOut(BaseModel):
    name: str
    total_reviews: int = Field(alias="totalReviews")

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        ser_by_alias=True
    )
```

Your function works with `wine.total_reviews`. JSON responses use `totalReviews`. Pydantic handles the mapping automatically.

## Custom Validators

Pydantic supports custom validation logic:

```python
class EventCreate(BaseModel):
    start_date: date
    end_date: date

    @field_validator('end_date')
    @classmethod
    def end_after_start(cls, v, info):
        if v <= info.data.get('start_date'):
            raise ValueError('end_date must be after start_date')
        return v
```

Jeroboam runs these validators. Cross-field validation, conditional validation, anything Pydantic supports.

## Computed Fields

Pydantic can generate fields from other fields:

```python
class Person(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

When serializing to JSON, `full_name` appears in the output without being a stored field. Jeroboam respects this in response models.

## The Cost

Pydantic validation has overhead. For simple endpoints with few parameters, it's negligible. For high-throughput APIs, you notice it.

Jeroboam mitigates this by doing validation registration once, not per-request. But the cost is still there.

If you need extreme performance on a specific endpoint, you can disable response validation:

```python
@app.get("/fast", validate_response=False)
def fast_endpoint():
    ...
```

You lose safety, but gain speed.

## Why Not a Different Validation Library

Some alternatives:

- **Marshmallow**: Heavier, slower, mature but older patterns
- **Cerberus**: Simpler but less powerful
- **Custom regex/logic**: Error-prone, hard to maintain

Pydantic is fast, thorough, and has become the standard in modern Python web frameworks. Using it means:
- Most developers are familiar with it
- Documentation and examples exist
- Performance is good
- Integration with other tools (SQLAlchemy, dataclasses) is seamless

## The v2 Migration

Jeroboam was built on Pydantic v1. Pydantic v2 changed significantly—faster, more accurate validation, better type handling.

Jeroboam v0.2.0 targets Pydantic v2. This involved:
- Updating validators (`@validator` → `@field_validator`)
- Using TypeAdapter instead of custom validation wrappers
- Adopting v2's FieldInfo patterns

The benefit: Jeroboam now uses modern Pydantic. The cost: if you're on Pydantic v1, you need to upgrade.

## Conclusion

Pydantic is not a requirement for using Flask. You can use Flask without it. But Jeroboam requires it because Pydantic does validation so well. Rather than reinventing validation, we integrated with the tool that does it best.

If you've used Pydantic elsewhere (FastAPI, SQLModel, many web frameworks), Jeroboam's use of it will feel natural.
