"""Pydantic v1 compatibility bridge.

This module re-exports removed pydantic v1 internals via the pydantic.v1
compatibility shim that ships with pydantic v2. Each symbol here is a
migration TODO — subsequent phases will replace them with native v2 equivalents.

Phase 2: DONE — ErrorWrapper/MissingError/ErrorList removed from public transport.
         ErrorWrapper still used internally in solved.py (removed in Phase 6).
Phase 3: DONE — Config classes migrated to ConfigDict.
Phase 4: Undefined — deferred, coupled to Phase 6 ViewArgument/SolvedArgument rewrite.
Phase 5: PARTIAL — evaluate_forwardref and lenient_issubclass replaced with local
         impls; SHAPE_SINGLETON removed. Remaining: ModelField, SHAPE_* removed in Phase 6.
Phase 6: ModelField, V1FieldInfo, SHAPE_*, ErrorWrapper, Undefined — all removed
         when SolvedArgument/ViewArgument are rewritten.
Phase 7: validate_model (already replaced in outbound handler).
Phase 8: get_model_name_map, field_schema, get_flat_models_from_fields,
         model_process_schema, get_annotation_from_field_info
"""

# --- Phase 2: ErrorWrapper still needed internally by solved.py until Phase 6 ---
from pydantic.v1.error_wrappers import ErrorWrapper  # noqa: F401

# --- Phase 3: Config ---
from pydantic.v1 import BaseConfig  # noqa: F401

# --- Phase 4: Undefined sentinel ---
from pydantic.v1.fields import Undefined  # noqa: F401

# --- Phase 5: ModelField and shape constants (ModelField removed in Phase 6) ---
from pydantic.v1.fields import (  # noqa: F401
    SHAPE_FROZENSET,
    SHAPE_LIST,
    SHAPE_SEQUENCE,
    SHAPE_SET,
    SHAPE_TUPLE,
    SHAPE_TUPLE_ELLIPSIS,
    FieldInfo as V1FieldInfo,
    ModelField,
)

# --- Phase 7: validate_model ---
from pydantic.v1 import validate_model  # noqa: F401

# --- Phase 8: OpenAPI schema generation ---
from pydantic.v1.schema import (  # noqa: F401
    field_schema,
    get_annotation_from_field_info,
    get_flat_models_from_fields,
    get_model_name_map,
    model_process_schema,
)
