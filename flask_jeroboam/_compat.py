"""Pydantic v1 compatibility bridge.

This module re-exports removed pydantic v1 internals via the pydantic.v1
compatibility shim that ships with pydantic v2. Each symbol here is a
migration TODO — subsequent phases will replace them with native v2 equivalents.

Phase 2: DONE — ErrorWrapper/MissingError/ErrorList removed from public transport.
         ErrorWrapper still used internally in solved.py (removed in Phase 6).
Phase 3: BaseConfig (replaced by model_config = ConfigDict(...))
Phase 4: Undefined (replaced by pydantic_core.PydanticUndefined)
Phase 5: ModelField, SHAPE_*, create_field, evaluate_forwardref, lenient_issubclass
Phase 7: validate_model (replaced by model.model_validate())
Phase 8: get_model_name_map, field_schema, get_flat_models_from_fields,
         model_process_schema, get_annotation_from_field_info
"""

# --- Phase 2: ErrorWrapper still needed internally by solved.py until Phase 6 ---
from pydantic.v1.error_wrappers import ErrorWrapper  # noqa: F401

# --- Phase 3: Config ---
from pydantic.v1 import BaseConfig  # noqa: F401

# --- Phase 4: Undefined sentinel ---
from pydantic.v1.fields import Undefined  # noqa: F401

# --- Phase 5: ModelField and shape constants ---
from pydantic.v1.fields import (  # noqa: F401
    SHAPE_FROZENSET,
    SHAPE_LIST,
    SHAPE_SEQUENCE,
    SHAPE_SET,
    SHAPE_SINGLETON,
    SHAPE_TUPLE,
    SHAPE_TUPLE_ELLIPSIS,
    FieldInfo as V1FieldInfo,
    ModelField,
)
from pydantic.v1.typing import evaluate_forwardref  # noqa: F401
from pydantic.v1.utils import lenient_issubclass  # noqa: F401

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
