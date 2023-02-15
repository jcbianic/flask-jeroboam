"""The Blueprint for the OpenAPI UI."""
from flask import current_app
from flask import render_template

from flask_jeroboam.jeroboam import JeroboamBlueprint
from flask_jeroboam.openapi.models.openapi_spec import OpenAPI
from flask_jeroboam.responses import HTMLResponse

from .models.ui_context import SwaggerContextOut


router = JeroboamBlueprint(
    "openapi_docs",
    __name__,
    template_folder="templates",
    static_folder="different_name",
    include_in_openapi=False,
)


@router.get("/docs", include_in_openapi=False)
def get_swagger_html():
    """Serving the Swagger UI HTML."""
    context = SwaggerContextOut(
        title=current_app.config.get("JEROBOAM_TITLE", "Jeroboam App")
    )
    return HTMLResponse(render_template("swagger-ui.jinja", **context.dict()))


@router.get("/openapi.json", response_model=OpenAPI, include_in_openapi=False)
def get_openapi_json():
    """Serving OpenAPI JSON."""
    return current_app.openapi()