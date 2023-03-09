"""Utlility functions for creating the OpenAPI doc.

Credits: This is a Fork of FastAPI's openapi/utils.py
"""
import warnings
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union
from typing import cast

from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.schema import field_schema
from pydantic.schema import get_flat_models_from_fields
from pydantic.schema import model_process_schema

from flask_jeroboam._constants import NO_BODY_STATUS_CODES
from flask_jeroboam._constants import REF_PREFIX
from flask_jeroboam._constants import VALIDATION_ERROR_DEFINITION
from flask_jeroboam._constants import VALIDATION_ERROR_RESPONSE_DEFINITION
from flask_jeroboam._utils import _append_truthy
from flask_jeroboam._utils import _set_nested_defaults
from flask_jeroboam._utils import _throw_away_falthy_values
from flask_jeroboam.view_arguments.arguments import BodyArgument
from flask_jeroboam.view_arguments.arguments import ParameterArgument


if TYPE_CHECKING:  # pragma: no cover
    from flask_jeroboam.rule import JeroboamRule
    from flask_jeroboam.view import JeroboamView
    from flask_jeroboam.view_arguments.solved import SolvedArgument


def _get_openapi_operation_parameters(
    *,
    all_route_params: Sequence[ModelField],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> List[Dict[str, Any]]:
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
                "schema": field_schema(
                    cast(ModelField, param),
                    model_name_map=model_name_map,
                    ref_prefix=REF_PREFIX,
                )[0],
                "deprecated": field_info.deprecated,
                "description": field_info.description,
            },
            keep={"name", "in", "required"},
        )
        parameters.append(parameter)
    return parameters


def _get_openapi_operation_metadata(
    *, rule: "JeroboamRule", method: str, operation_ids: Set[str]
) -> Dict[str, Any]:
    operation_id = rule.operation_id or rule.unique_id or rule.endpoint
    if operation_id in operation_ids:
        message = (
            f"Duplicate Operation ID {operation_id} for function " + f"{rule.endpoint}"
        )
        warnings.warn(message, UserWarning, stacklevel=2)
    operation_ids.add(operation_id)
    operation: Dict[str, Any] = _throw_away_falthy_values(
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
    body_field: Optional[ModelField],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> Optional[Dict[str, Any]]:
    assert body_field  # noqa: S101
    # TODO: something is broken here.
    body_schema, body_definition, _ = field_schema(
        body_field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
    )
    field_info = cast(BodyArgument, body_field.field_info)
    request_media_type = field_info.media_type
    request_body_oai: Dict[str, Any] = {}
    if required := body_field.required:
        request_body_oai["required"] = required
    if body_schema.get("$ref", "").endswith("request_body_as_model"):
        request_media_content: Dict[str, Any] = {
            "schema": body_definition[body_schema.get("$ref", "").split("/")[-1]]
        }
    else:
        request_media_content = {"schema": body_schema}
    request_body_oai["content"] = {request_media_type: request_media_content}
    return request_body_oai


def _get_response_schema(
    response_field: Optional[ModelField], model_name_map
) -> Dict[str, Any]:
    response_schema = {"type": "string"}
    if response_field:
        response_schema, _, _ = field_schema(
            response_field,
            model_name_map=model_name_map,
            ref_prefix=REF_PREFIX,
        )
    else:
        response_schema = {}
    return response_schema


def _add_responses(
    operation,
    model_name_map,
    jeroboam_view,
):
    definitions: Dict[str, Any] = {}
    status_code = str(jeroboam_view.outbound_handler.latent_status_code)
    current_response_class = jeroboam_view.outbound_handler.response_class
    route_response_media_type: Optional[str] = current_response_class.default_mimetype

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
                jeroboam_view.outbound_handler.response_field,
                model_name_map=model_name_map,
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
    model_name_map,
    operation_ids: Set[str],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Build OpenApi path from our rule Object.

    TODO: Gérer les Callbacks ?
    """
    operation = _get_openapi_operation_metadata(
        rule=rule, method=jeroboam_view.main_method, operation_ids=operation_ids
    )

    # On gère les paramètres
    if parameters := _get_openapi_operation_parameters(
        all_route_params=jeroboam_view.parameters, model_name_map=model_name_map
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
            model_name_map=model_name_map,
        )

    operation, definitions = _add_responses(
        operation,
        model_name_map,
        jeroboam_view,
    )
    operation.update(rule.openapi_extra or {})
    return {jeroboam_view.main_method: operation}, {}, definitions


def _get_model_definitions(
    *,
    flat_models: Set[Union[Type[BaseModel], Type[Enum]]],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> Dict[str, Any]:
    definitions: Dict[str, Dict[str, Any]] = {}
    for model in flat_models:
        m_schema, m_definitions, _ = model_process_schema(
            model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )
        definitions.update(m_definitions)
        model_name = model_name_map[model]
        if "description" in m_schema:
            m_schema["description"] = m_schema["description"].split("\f")[0]
        definitions[model_name] = m_schema
    return definitions


def _get_flat_models_from_jeroboam_views(
    jeroboam_views: List[Optional["JeroboamView"]], rules: List["JeroboamRule"]
):
    params: List[Union[ModelField, "SolvedArgument"]] = []
    for jeroboam_view, rule in zip(jeroboam_views, rules):
        if getattr(jeroboam_view, "include_in_openapi", False) is False:
            continue
        assert jeroboam_view is not None  # noqa: S101
        params.extend(jeroboam_view.inbound_handler.parameters or [])
        _append_truthy(params, jeroboam_view.outbound_handler.response_field)
        _append_truthy(params, jeroboam_view.inbound_handler.body_field(rule.unique_id))
    return get_flat_models_from_fields(params, known_models=set())
