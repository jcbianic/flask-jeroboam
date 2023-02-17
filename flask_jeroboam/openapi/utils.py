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
from pydantic.schema import get_model_name_map
from pydantic.schema import model_process_schema

from flask_jeroboam.openapi.models.openapi import Components
from flask_jeroboam.openapi.models.openapi import Info
from flask_jeroboam.openapi.models.openapi import Tag
from flask_jeroboam.rule import JeroboamRule
from flask_jeroboam.view import JeroboamView
from flask_jeroboam.view_params.parameters import BodyParameter
from flask_jeroboam.view_params.parameters import NonBodyParameter
from flask_jeroboam.view_params.solved import SolvedParameter

from .models.openapi import OpenAPI


if TYPE_CHECKING:  # pragma: no cover
    from flask_jeroboam.jeroboam import Jeroboam

REF_PREFIX = "#/components/schemas/"
METHODS_WITH_BODY = {"POST", "PUT", "PATCH", "DELETE"}
NO_BODY_STATUS_CODES = {"204", "205", "304"}

validation_error_definition = {
    "title": "ValidationError",
    "type": "object",
    "properties": {
        "loc": {
            "title": "Location",
            "type": "array",
            "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        },
        "msg": {"title": "Message", "type": "string"},
        "type": {"title": "Error Type", "type": "string"},
    },
    "required": ["loc", "msg", "type"],
}

validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "detail": {
            "title": "Detail",
            "type": "array",
            "items": {"$ref": f"{REF_PREFIX}ValidationError"},
        }
    },
}

status_code_ranges: Dict[str, str] = {
    "1XX": "Information",
    "2XX": "Success",
    "3XX": "Redirection",
    "4XX": "Client Error",
    "5XX": "Server Error",
    "DEFAULT": "Default Response",
}


def _get_openapi_operation_parameters(
    *,
    all_route_params: Sequence[ModelField],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> List[Dict[str, Any]]:
    parameters = []
    for param in all_route_params:
        field_info = param.field_info
        field_info = cast(NonBodyParameter, field_info)
        if getattr(param, "include_in_schema", True) is False:
            continue
        parameter = _compact_dict(
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


def _compact_dict(
    sparse_dict: Dict[str, Any], keep: Optional[set] = None
) -> Dict[str, Any]:
    keep = keep or set()
    return {key: value for key, value in sparse_dict.items() if value or key in keep}


def _smart_update(key: str, new_value: Any, orginal: Dict[str, Any]):
    if new_value:
        orginal.setdefault(key, {}).update(new_value)


def _generate_operation_summary(*, rule: JeroboamRule, method: str) -> str:
    return rule.summary or rule.endpoint.replace("_", " ").title().split(".")[-1]


def _get_openapi_operation_metadata(
    *, rule: JeroboamRule, method: str, operation_ids: Set[str]
) -> Dict[str, Any]:
    operation_id = rule.operation_id or rule.unique_id or rule.endpoint
    if operation_id in operation_ids:
        message = (
            f"Duplicate Operation ID {operation_id} for function " + f"{rule.endpoint}"
        )
        warnings.warn(message, UserWarning, stacklevel=2)
    operation_ids.add(operation_id)
    operation: Dict[str, Any] = _compact_dict(
        {
            "tags": rule.tags,
            "description": rule.description,
            "summary": _generate_operation_summary(rule=rule, method=method),
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
    body_schema, _, _ = field_schema(
        body_field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
    )
    field_info = cast(BodyParameter, body_field.field_info)
    request_media_type = field_info.media_type
    request_body_oai: Dict[str, Any] = {}
    if required := body_field.required:
        request_body_oai["required"] = required
    request_media_content: Dict[str, Any] = {"schema": body_schema}
    request_body_oai["content"] = {request_media_type: request_media_content}
    return request_body_oai


def _add_responses(
    operation,
    model_name_map,
    jeroboam_view,
):
    definitions: Dict[str, Any] = {}
    status_code = str(jeroboam_view.outbound_handler.latent_status_code)
    current_response_class = jeroboam_view.outbound_handler.response_class
    route_response_media_type: Optional[str] = current_response_class.default_mimetype
    description = jeroboam_view.outbound_handler.response_description
    response_field = jeroboam_view.outbound_handler.response_field

    operation.setdefault("responses", {}).setdefault(status_code, {})[
        "description"
    ] = description

    if route_response_media_type and status_code not in NO_BODY_STATUS_CODES:
        response_schema = {"type": "string"}
        if response_field:
            response_schema, _, _ = field_schema(
                response_field,
                model_name_map=model_name_map,
                ref_prefix=REF_PREFIX,
            )
        else:
            response_schema = {}
        operation.setdefault("responses", {}).setdefault(status_code, {}).setdefault(
            "content", {}
        ).setdefault(route_response_media_type, {})["schema"] = response_schema

    http400 = str(400)  # TODO: possibilité de configurer le status code
    if jeroboam_view.inbound_handler.is_valid and all(
        status not in operation["responses"] for status in {http400, "4XX", "default"}
    ):
        operation["responses"][http400] = {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {"$ref": f"{REF_PREFIX}HTTPValidationError"}
                }
            },
        }
        definitions.update(
            {
                "ValidationError": validation_error_definition,
                "HTTPValidationError": validation_error_response_definition,
            }
        )
    return operation, definitions


def _build_openapi_path_item(
    *,
    rule: JeroboamRule,
    jeroboam_view: JeroboamView,
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
    jeroboam_views: List[Optional[JeroboamView]], rules: List[JeroboamRule]
):
    params: List[Union[ModelField, SolvedParameter]] = []
    for jeroboam_view, rule in zip(jeroboam_views, rules):
        if jeroboam_view is None or jeroboam_view.include_in_openapi is False:
            continue
        params.extend(jeroboam_view.inbound_handler.parameters or [])
        if jeroboam_view.outbound_handler.response_field:
            params.append(jeroboam_view.outbound_handler.response_field)
        body_field = jeroboam_view.inbound_handler.body_field(rule.unique_id)
        if body_field is not None:
            params.append(body_field)
    return get_flat_models_from_fields(params, known_models=set())


def build_openapi(
    *,
    app: "Jeroboam",
    rules: List[JeroboamRule],
    tags: Optional[List[Dict[str, Any]]] = None,
) -> OpenAPI:
    """Generate an OpenAPI schema for the given routes.

    TODO: Gérer les securitySchemes.
    Credits: Refactoring of FastApi's get_openapi.
    """
    # Meta
    openapi_version = app.config.get("JEROBOAM_OPENAPI_VERSION", "3.0.2")
    info = Info.parse_obj(
        {
            "title": app.config.get("JEROBOAM_TITLE", app.name),
            "version": app.config.get("JEROBOAM_VERSION", "0.1.0"),
            "description": app.config.get("JEROBOAM_DESCRIPTION", None),
            "terms_of_service": app.config.get("JEROBOAM_TERMS_OF_SERVICE", None),
            "contact": app.config.get("JEROBOAM_CONTACT", None),
            "license": app.config.get("JEROBOAM_LICENCE_INFO", None),
        }
    )
    servers = app.config.get("JEROBOAM_SERVERS", None)

    # Préparation
    paths: Dict[str, Dict[str, Any]] = {}
    components: Dict[str, Dict[str, Any]] = {}
    operation_ids: Set[str] = set()

    # Les jerobomas views, probablement à déléguer à l'app
    jeroboam_views: List[Optional[JeroboamView]] = [
        getattr(app.view_functions[rule.endpoint], "__jeroboam_view__", None)
        for rule in rules
    ]

    # On créer des objects intermédiaires
    flat_models = _get_flat_models_from_jeroboam_views(jeroboam_views, rules)
    model_name_map = get_model_name_map(flat_models)
    definitions = _get_model_definitions(
        flat_models=flat_models, model_name_map=model_name_map
    )

    # On itères sur les rules and views pour récuperr les Paths Items et Définitions.
    for rule, jeroboam_view in zip(rules, jeroboam_views):
        if rule.include_in_openapi is False or jeroboam_view is None:
            continue
        path_dict, security_schemes, path_definitions = _build_openapi_path_item(
            rule=rule,
            jeroboam_view=jeroboam_view,
            model_name_map=model_name_map,
            operation_ids=operation_ids,
        )
        _smart_update(rule.openapi_path, path_dict, paths)
        # TODO: ici il faut être capable de récupérer les securitySchemes
        _smart_update("security_schemes", security_schemes, components)
        definitions.update(path_definitions or {})

    # On package le tout.
    return OpenAPI(
        openapi=openapi_version,
        info=info,
        servers=servers,
        paths=paths,
        tags=[Tag(**tag) for tag in tags or []],
        components=Components(schemas={k: definitions[k] for k in sorted(definitions)}),
    )
