"""Utlility functions for creating the OpenAPI doc.

Credits: This is a Fork of FastAPI's openapi/utils.py
"""

import warnings
from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    cast,
)

from pydantic import BaseModel

from flask_jeroboam._constants import (
    NO_BODY_STATUS_CODES,
    REF_PREFIX,
    VALIDATION_ERROR_DEFINITION,
    VALIDATION_ERROR_RESPONSE_DEFINITION,
)
from flask_jeroboam._utils import (
    _lenient_issubclass,
    _set_nested_defaults,
    _throw_away_falthy_values,
)
from flask_jeroboam.view_arguments.arguments import BodyArgument, ParameterArgument

if TYPE_CHECKING:  # pragma: no cover
    from flask_jeroboam.rule import JeroboamRule
    from flask_jeroboam.view import JeroboamView
    from flask_jeroboam.view_arguments.solved import SolvedArgument


def _unwrap_optional_annotation(annotation: Any) -> Any:
    """Return the inner type if annotation is Optional[X], else return it unchanged."""
    import types as _types
    from typing import Union, get_args, get_origin

    origin = get_origin(annotation)
    is_union = origin is Union
    if not is_union and hasattr(_types, "UnionType"):
        is_union = isinstance(annotation, _types.UnionType)
    if is_union:
        non_none = [a for a in get_args(annotation) if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return annotation


def _get_param_schema(param: "SolvedArgument") -> dict[str, Any]:
    from pydantic import TypeAdapter

    # For Optional[X] (union with None), use just the inner type for schema generation
    # so that we get {"type": "integer"} rather than {"anyOf": [...]}
    inner_annotation = _unwrap_optional_annotation(param.annotation)
    if inner_annotation is not param.annotation:
        schema = TypeAdapter(inner_annotation).json_schema(
            ref_template=REF_PREFIX + "{model}"
        )
    else:
        schema = param._type_adapter.json_schema(ref_template=REF_PREFIX + "{model}")
    # Remove "default": None from schema — None defaults are implicit in optional params
    if schema.get("default") is None:
        schema.pop("default", None)
    schema.setdefault("title", param.alias.replace("_", " ").title())
    return schema


def _get_openapi_operation_parameters(
    *,
    all_route_params: "Sequence[SolvedArgument]",
) -> list[dict[str, Any]]:
    parameters = []
    for param in all_route_params:
        field_info = param.field_info
        field_info = cast(ParameterArgument, field_info)
        if getattr(param, "include_in_schema", True) is False:
            continue
        parameter = _throw_away_falthy_values(
            {
                "name": param.alias,
                "in": field_info.location.value,
                "required": param.required,
                "schema": _get_param_schema(param),
                "deprecated": field_info.deprecated,
                "description": field_info.description,
            },
            keep={"name", "in", "required"},
        )
        parameters.append(parameter)
    return parameters


def _get_openapi_operation_metadata(
    *, rule: "JeroboamRule", method: str, operation_ids: set[str]
) -> dict[str, Any]:
    operation_id = rule.operation_id or rule.unique_id or rule.endpoint
    if operation_id in operation_ids:
        message = (
            f"Duplicate Operation ID {operation_id} for function " + f"{rule.endpoint}"
        )
        warnings.warn(message, UserWarning, stacklevel=2)
    operation_ids.add(operation_id)
    operation: dict[str, Any] = _throw_away_falthy_values(
        {
            "tags": rule.tags,
            "description": rule.description,
            "summary": rule.summary,
            "deprecated": rule.deprecated,
            "operationId": operation_id,
        }
    )
    return operation


def _get_openapi_operation_request_body(
    *,
    body_field: "SolvedArgument | None",
) -> dict[str, Any] | None:
    if body_field is None:  # pragma: no cover
        return None
    annotation = body_field.annotation
    field_info = cast(BodyArgument, body_field.field_info)
    request_media_type = field_info.media_type

    is_synthetic = _lenient_issubclass(
        annotation, BaseModel
    ) and annotation.__name__.endswith("request_body_as_model")
    if is_synthetic:
        body_schema = cast(type[BaseModel], annotation).model_json_schema(
            ref_template=REF_PREFIX + "{model}"
        )
        body_schema.pop("$defs", None)
    elif _lenient_issubclass(annotation, BaseModel):
        body_schema = {"$ref": f"{REF_PREFIX}{annotation.__name__}"}
    else:
        body_schema = body_field._type_adapter.json_schema(
            ref_template=REF_PREFIX + "{model}"
        )

    request_body_oai: dict[str, Any] = {}
    if body_field.required:
        request_body_oai["required"] = True
    request_body_oai["content"] = {request_media_type: {"schema": body_schema}}
    return request_body_oai


def _get_response_schema(
    response_model: type | None,
) -> dict[str, Any]:
    if response_model is None:
        return {}
    if _lenient_issubclass(response_model, BaseModel):
        return {"$ref": f"{REF_PREFIX}{response_model.__name__}"}
    return {}  # pragma: no cover


def _add_responses(
    operation,
    jeroboam_view,
):
    definitions: dict[str, Any] = {}
    status_code = str(jeroboam_view.outbound_handler.latent_status_code)
    current_response_class = jeroboam_view.outbound_handler.response_class
    route_response_media_type: str | None = current_response_class.default_mimetype

    _set_nested_defaults(
        original_dict=operation,
        keys=["responses", status_code],
        last_key="description",
        new_value=jeroboam_view.outbound_handler.response_description,
    )

    if route_response_media_type and status_code not in NO_BODY_STATUS_CODES:
        _set_nested_defaults(
            original_dict=operation,
            keys=["responses", status_code, "content", route_response_media_type],
            last_key="schema",
            new_value=_get_response_schema(
                jeroboam_view.outbound_handler.response_model,
            ),
        )

    # TODO: possibilité de configurer le status code
    if jeroboam_view.inbound_handler.is_valid and all(
        status not in operation["responses"] for status in {"400", "4XX", "default"}
    ):
        operation["responses"]["400"] = {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {"$ref": f"{REF_PREFIX}HTTPValidationError"}
                }
            },
        }
        definitions.update(
            {
                "ValidationError": VALIDATION_ERROR_DEFINITION,
                "HTTPValidationError": VALIDATION_ERROR_RESPONSE_DEFINITION,
            }
        )
    return operation, definitions


def _build_openapi_path_item(
    *,
    rule: "JeroboamRule",
    jeroboam_view: "JeroboamView",
    operation_ids: set[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Build OpenApi path from our rule Object.

    TODO: Gérer les Callbacks ?
    """
    operation = _get_openapi_operation_metadata(
        rule=rule, method=jeroboam_view.main_method, operation_ids=operation_ids
    )

    # On gère les paramètres
    if parameters := _get_openapi_operation_parameters(
        all_route_params=jeroboam_view.parameters,
    ):
        all_parameters = {(param["in"], param["name"]): param for param in parameters}
        required_parameters = {
            (param["in"], param["name"]): param
            for param in parameters
            if param.get("required")
        }
        # Make sure required definitions of the same parameter take precedence
        # over non-required definitions
        all_parameters.update(required_parameters)
        operation["parameters"] = list(all_parameters.values())
    # On gère le request Body
    if jeroboam_view.has_request_body:
        operation["request_body"] = _get_openapi_operation_request_body(
            body_field=jeroboam_view.inbound_handler.body_field(rule.unique_id),
        )

    operation, definitions = _add_responses(
        operation,
        jeroboam_view,
    )
    operation.update(rule.openapi_extra or {})
    return {jeroboam_view.main_method: operation}, {}, definitions


def _get_model_definitions(
    *,
    flat_models: set,
) -> dict[str, Any]:
    definitions: dict[str, Any] = {}
    for model in flat_models:
        m_schema = model.model_json_schema(ref_template=REF_PREFIX + "{model}")
        nested = m_schema.pop("$defs", {})
        definitions.update(nested)
        if "description" in m_schema:
            m_schema["description"] = m_schema["description"].split("\f")[0]
        definitions[model.__name__] = m_schema
    return definitions


def _get_flat_models_from_jeroboam_views(
    jeroboam_views: list[Optional["JeroboamView"]], rules: list["JeroboamRule"]
):
    models: set = set()
    for jeroboam_view, rule in zip(jeroboam_views, rules):
        if jeroboam_view is None:
            continue
        if not getattr(jeroboam_view, "include_in_openapi", True):
            continue
        response_model = jeroboam_view.outbound_handler.response_model
        if response_model is not None:
            models.add(response_model)
        body_field = jeroboam_view.inbound_handler.body_field(rule.unique_id)
        if body_field is not None and _lenient_issubclass(
            body_field.annotation, BaseModel
        ):
            if not body_field.annotation.__name__.endswith("request_body_as_model"):
                models.add(body_field.annotation)
    return models
