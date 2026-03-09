"""Pydantic v1 compatibility bridge.

This module re-exports removed pydantic v1 internals via the pydantic.v1
compatibility shim that ships with pydantic v2. Each symbol here is a
migration TODO — subsequent phases will replace them with native v2 equivalents.

Phase 2: DONE — ErrorWrapper removed (was used by solved.py, removed in Phase 6).
Phase 3: DONE — Config classes migrated to ConfigDict.
Phase 4: DONE — Undefined removed; replaced by PydanticUndefined from pydantic_core.
Phase 5: DONE — SHAPE_* constants removed (were used by SolvedArgument, removed in Phase 6).
Phase 6: DONE — ErrorWrapper, Undefined, SHAPE_* cleaned up. ModelField and V1FieldInfo
         retained for the OpenAPI response_field property in _outboundhandler.py (Phase 8).
Phase 7: DONE — validate_model removed (already replaced in outbound handler).
Phase 8: get_model_name_map, field_schema, get_flat_models_from_fields,
         model_process_schema, get_annotation_from_field_info
"""

# --- Phase 6 remnant: still needed by _outboundhandler.py response_field property ---
from pydantic.v1 import BaseConfig  # noqa: F401
from pydantic.v1.fields import (  # noqa: F401
    FieldInfo as V1FieldInfo,
    ModelField,
)

# --- Phase 8: OpenAPI schema generation ---
from pydantic.v1.schema import (  # noqa: F401
    field_schema,
    get_annotation_from_field_info,
    get_flat_models_from_fields,
    get_model_name_map,
    model_process_schema,
)
