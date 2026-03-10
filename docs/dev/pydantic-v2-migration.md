# Pydantic v2 Migration Plan

Pydantic v2 was released in June 2023. Migrating is the single highest-priority item for the project — it is a hard blocker for adoption in any modern Python project.

This document is the internal plan for executing that migration.

---

## Scope of Change

The migration touches almost every file in `flask_jeroboam/`. The overall scale is large because the library's core relies heavily on Pydantic v1 internals — `ModelField`, `ErrorWrapper`, `SHAPE_*` constants, `validate_model()` — that were removed without equivalents in v2.

A complete audit is below. Changes are grouped by difficulty and dependency order.

---

## Phase 0: Setup & Compatibility Strategy

**Decision: native v2, no compatibility shim.**

Pydantic ships a `pydantic.v1` compatibility module, but using it would mean we still can't accept user models built with v2 APIs (e.g. `model_config`, `@model_validator`). The goal is full v2 native support.

Steps:
- [ ] Add `pydantic>=2.0` to `pyproject.toml` (remove `<2.0` ceiling)
- [ ] Add `pydantic-settings>=2.0` as a dependency (replaces `pydantic.BaseSettings`)
- [ ] Update CI matrix to run tests against Pydantic v2 only
- [ ] Consider a v1 deprecation notice in `0.1.x` before the breaking `0.2.0` release

---

## Phase 1: Trivial Renames (Start Here)

These are mechanical find-and-replace changes. Do them first to reduce noise in later diffs.

| File | Change | v1 | v2 |
|---|---|---|---|
| `jeroboam.py` | Method rename | `.dict()` | `.model_dump()` |
| `_outboundhandler.py` | Method rename | `.json()` | `.model_dump_json()` |
| `_outboundhandler.py` | Method rename | `.dict()` | `.model_dump()` |
| `openapi/blueprint.py` | Method rename | `.dict()` | `.model_dump()` |
| `_config.py` | Class method rename | `.parse_obj()` | `.model_validate()` |
| `openapi/builder.py` | Class method rename | `.parse_obj()` | `.model_validate()` |
| `openapi/models/openapi.py` | Forward refs | `.update_forward_refs()` | `.model_rebuild()` |
| All files | `__fields__` access | `model.__fields__` | `model.model_fields` |
| `openapi/models/openapi.py` | Config classes (~20) | `class Config: extra = "allow"` | `model_config = ConfigDict(extra="allow")` |

**Estimated effort: 2–4 hours**

---

## Phase 2: Error Handling Restructure

These classes from `pydantic.error_wrappers` are fully removed in v2: `ErrorWrapper`, `ErrorList`, `MissingError`.

In v2, validation errors are represented as `pydantic_core.ValidationError` with a list of `InitErrorDetails`. The approach changes from building errors imperatively to catching `ValidationError` exceptions from `model_validate()` calls.

### `exceptions.py`
- Remove import of `ErrorList` from `pydantic.error_wrappers`
- `InvalidRequest.from_pydantic_validation_error()` currently takes an `ErrorList`; rewrite to accept `pydantic.ValidationError` directly and call `.errors()` on it

### `_inboundhandler.py`
- Remove `ErrorWrapper` and `MissingError` imports
- The error accumulation loop (collecting errors across multiple parameters) needs to collect raw error dicts instead of `ErrorWrapper` objects, then raise `pydantic.ValidationError` using `pydantic_core.InitErrorDetails`

### `view_arguments/solved.py`
- `MissingError` is used when a required parameter is absent; replace with raising `ValueError` or constructing a `pydantic_core.InitErrorDetails` directly

**Estimated effort: 6–10 hours**

---

## Phase 3: Configuration Pattern Migration

### `models.py` — `InboundModel` and `OutboundModel`

```python
# v1
class InboundModel(BaseModel):
    class Config:
        alias_generator = snake_case_to_camel
        allow_population_by_field_name = True

class OutboundModel(BaseModel):
    class Config:
        json_dumps = json_dumps_to_camel_case
```

```python
# v2
from pydantic import ConfigDict

class InboundModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=snake_case_to_camel,
        populate_by_name=True,  # replaces allow_population_by_field_name
    )

class OutboundModel(BaseModel):
    model_config = ConfigDict()
    # json_dumps is removed — use model_serializer or custom json encoder
    # For camelCase output: use alias_generator on the response side too,
    # or use model_dump(by_alias=True) in the outbound handler
```

The `json_dumps` config key is removed in v2. The camelCase output behavior of `OutboundModel` needs to be reimplemented — the cleanest v2 approach is to set an `alias_generator` on the output model and call `model_dump(by_alias=True)` in `OutboundHandler`.

### `_config.py` — `BaseSettings`

```python
# v1
from pydantic import BaseSettings

# v2
from pydantic_settings import BaseSettings  # separate package
```

**Estimated effort: 4–6 hours**

---

## Phase 4: `ViewArgument` Hierarchy Redesign

`ViewArgument` currently inherits from `pydantic.fields.FieldInfo`. In v2, `FieldInfo` is still present but its internals changed significantly, and the `Undefined` sentinel moved.

```python
# v1
from pydantic.fields import FieldInfo, Undefined

class ViewArgument(FieldInfo):
    location: ArgumentLocation
    ...
```

In v2, `FieldInfo` is less designed for subclassing. The recommended pattern for attaching custom metadata to fields is `Annotated` with a custom metadata class:

```python
# v2 approach
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefinedType, PydanticUndefined

class ViewArgumentMetadata:
    """Metadata attached via Annotated[] to carry location info."""
    def __init__(self, location: ArgumentLocation, **kwargs):
        self.location = location
        self.kwargs = kwargs
```

However, the `FieldInfo` subclassing approach *may* still work in v2 with adjustments — this needs to be prototyped before committing to a full rewrite. The `Undefined` sentinel is now at `pydantic_core.PydanticUndefined`.

**Estimated effort: 8–16 hours (prototype first)**

---

## Phase 5: `_utils.py` — The Hardest File

This file is the heart of the migration complexity. It uses:
- `ModelField` (removed in v2)
- `SHAPE_*` constants (removed in v2)
- `evaluate_forwardref()` (removed in v2)
- `lenient_issubclass()` (removed in v2)
- `BaseConfig` (removed in v2)

### `ModelField` replacement

`ModelField` was Pydantic v1's internal representation of a resolved field. In v2 this is replaced by the combination of `FieldInfo` + Python type annotations. The `create_field()` function in `_utils.py` that currently builds `ModelField` objects needs to be rewritten.

The `SolvedArgument` class in `view_arguments/solved.py` currently **inherits from `ModelField`**, which is the deepest coupling to v1 internals. This needs to become a composition-based design:

```python
# v1 — inheritance
class SolvedArgument(ModelField):
    ...

# v2 — composition
class SolvedArgument:
    field_info: FieldInfo
    annotation: type
    name: str
    location: ArgumentLocation
    ...
```

### `SHAPE_*` constants replacement

These constants identified whether a field held a scalar, list, set, etc. In v2, this information lives in the type annotation itself. Use `typing.get_args()` and `typing.get_origin()` to inspect:

```python
# v1
from pydantic.fields import SHAPE_LIST, SHAPE_SET

if field.shape in (SHAPE_LIST, SHAPE_SET):
    ...

# v2
import typing

origin = typing.get_origin(annotation)
if origin in (list, set):
    ...
```

### Utility function replacements

| v1 | v2 replacement |
|---|---|
| `evaluate_forwardref(ref, globalns, localns)` | `typing.get_type_hints()` on the containing class |
| `lenient_issubclass(cls, parent)` | `try/except TypeError` around `issubclass()` |
| `get_annotation_from_field_info(fi, name, model_name)` | `fi.annotation` attribute (exists in v2) |

**Estimated effort: 16–24 hours**

---

## Phase 6: `SolvedArgument` Redesign

`view_arguments/solved.py` is the request-side parameter extraction engine. It currently subclasses `ModelField` for each location type. Post-migration architecture:

```python
class SolvedArgument:
    """Resolved view parameter, ready to extract and validate at request time."""

    def __init__(self, name: str, annotation: type, field_info: FieldInfo, location: ArgumentLocation):
        self.name = name
        self.annotation = annotation
        self.field_info = field_info
        self.location = location
        self._configure_extractor()

    def _configure_extractor(self):
        origin = typing.get_origin(self.annotation)
        if hasattr(self.annotation, "model_fields"):
            self.extractor = self._extract_subfields
        elif origin in (list, set, tuple):
            self.extractor = self._extract_sequence
        else:
            self.extractor = self._extract_scalar
```

**Estimated effort: 12–16 hours**

---

## Phase 7: `validate_model()` Replacement in `_outboundhandler.py`

```python
# v1
from pydantic import validate_model

values, _, error = validate_model(self.response_model, outbound_data)
if error:
    raise ResponseValidationError(...)
return self.response_model(**values).json()
```

```python
# v2
try:
    instance = self.response_model.model_validate(outbound_data)
except pydantic.ValidationError as error:
    raise ResponseValidationError(...) from error
return instance.model_dump_json()
```

**Estimated effort: 2–3 hours**

---

## Phase 8: OpenAPI Schema Generation Rewrite

`openapi/_utils.py` is the second-hardest file. It imports and calls:
- `field_schema()` — removed in v2
- `get_flat_models_from_fields()` — removed in v2
- `model_process_schema()` — removed in v2
- `ModelField` — removed in v2

From `openapi/builder.py`:
- `get_model_name_map()` — removed in v2

**v2 replacement strategy:** Use `model_json_schema()` directly and let Pydantic generate the full JSON Schema. Then post-process the output to fit the OpenAPI 3.x spec format (handling `$defs`, `$ref` resolution, etc.).

```python
# v2 approach
schema = MyModel.model_json_schema(mode="serialization")
# schema is a complete JSON Schema dict
# $defs contains all referenced sub-schemas
```

This is a significant rewrite. The key insight: Pydantic v2's `model_json_schema()` is much more complete than v1's `schema()` — it handles forward references, recursive models, and `$defs` correctly out of the box. Much of the custom logic in `_utils.py` exists to work around v1 limitations that simply don't exist in v2.

**Estimated effort: 16–24 hours** (but may be less than expected because v2 handles more automatically)

---

## Phase 9: `datastructures.py` — Custom Type Validators

```python
# v1 — __get_validators__ protocol
class UploadFile:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", format="binary")
```

```python
# v2 — Annotated with GetCoreSchemaHandler
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class UploadFile:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "format": "binary"}
```

**Estimated effort: 2–4 hours**

---

## Execution Order

```
Phase 1  →  Phase 2  →  Phase 3
                ↓
           Phase 4 (prototype)
                ↓
    Phase 5 + Phase 6 (parallel, tightly coupled)
                ↓
           Phase 7  →  Phase 8
                ↓
           Phase 9
```

---

## Total Effort Estimate

| Phase | Scope | Estimated Hours |
|---|---|---|
| 0 — Setup | pyproject.toml, CI | 1 |
| 1 — Trivial renames | Mechanical replacements | 2–4 |
| 2 — Error handling | ErrorWrapper, ErrorList, MissingError | 6–10 |
| 3 — Config migration | InboundModel, OutboundModel, BaseSettings | 4–6 |
| 4 — ViewArgument redesign | FieldInfo subclassing, Undefined | 8–16 |
| 5 — `_utils.py` rewrite | ModelField, SHAPE_*, utilities | 16–24 |
| 6 — SolvedArgument redesign | Composition-based redesign | 12–16 |
| 7 — validate_model() | Outbound handler | 2–3 |
| 8 — OpenAPI schema rewrite | field_schema, get_flat_models | 16–24 |
| 9 — datastructures.py | Custom type validators | 2–4 |
| **Total** | | **69–108 hours** |

This is 2–3 weeks of focused engineering work. Phases 5, 6, and 8 are the critical path.

---

## Testing Strategy

- The existing 100% coverage requirement is the safety net — keep it
- Add Pydantic v2 to the nox test matrix early (Phase 0) so failures surface immediately
- Phases 1–3 should keep existing tests green; use them as a regression check
- Phases 4–6 will break tests; write new tests alongside the redesign
- Add a `tests/test_pydantic_v2/` suite specifically for v2-only features (`model_config`, `@model_validator`, `@computed_field`) that v1 users couldn't use

---

## Breaking Changes for Users

This migration will be a **breaking change** for any user who passes `InboundModel` or `OutboundModel` subclasses with v1-style `Config` inner classes. Communicate clearly:

- `0.1.x` — last versions supporting Pydantic v1
- `0.2.0` — Pydantic v2 only, breaking change release
- Write a user-facing migration guide alongside this internal plan

The user-facing migration guide should cover: replacing `class Config:` with `model_config = ConfigDict(...)`, replacing `.dict()` with `.model_dump()`, and any changes to `InboundModel`/`OutboundModel` behavior.
