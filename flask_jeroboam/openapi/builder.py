"""Main builder function for OPENAPI schema."""
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

from pydantic.schema import get_model_name_map

from flask_jeroboam._utils import _memoized_update_if_value
from flask_jeroboam.openapi._utils import _build_openapi_path_item
from flask_jeroboam.openapi._utils import _get_flat_models_from_jeroboam_views
from flask_jeroboam.openapi._utils import _get_model_definitions
from flask_jeroboam.openapi.models.openapi import Components
from flask_jeroboam.openapi.models.openapi import Info
from flask_jeroboam.openapi.models.openapi import OpenAPI
from flask_jeroboam.openapi.models.openapi import Tag


if TYPE_CHECKING:  # pragma: no cover
    from flask_jeroboam.jeroboam import Jeroboam
    from flask_jeroboam.rule import JeroboamRule
    from flask_jeroboam.view import JeroboamView


def build_openapi(
    *,
    app: "Jeroboam",
    rules: List["JeroboamRule"],
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
            "title": app.config.get("JEROBOAM_TITLE", None) or app.name,
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
    jeroboam_views: List[Optional["JeroboamView"]] = [
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
        _memoized_update_if_value(rule.openapi_path, path_dict, paths)
        # TODO: ici il faut être capable de récupérer les securitySchemes
        _memoized_update_if_value("security_schemes", security_schemes, components)
        definitions.update(path_definitions or {})

    definitions = {
        k: definitions[k]
        for k in sorted(definitions)
        if not k.endswith("request_body_as_model")
    }
    # On package le tout.
    return OpenAPI(
        openapi=openapi_version,
        info=info,
        servers=servers,
        paths=paths,
        tags=[Tag(**tag) for tag in tags or []],
        components=Components(schemas=definitions),
    )
