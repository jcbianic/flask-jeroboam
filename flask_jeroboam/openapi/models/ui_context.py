"""Models for OpenAPI 3.0.0."""

from typing import Optional

from pydantic import Field

from flask_jeroboam.models import OutboundModel


class SwaggerContextOut(OutboundModel):
    """Swagger Outbound Model."""

    title: Optional[str] = Field(
        default="Swagger UI", description="Title of the Swagger UI"
    )
    swagger_ui_url: Optional[str] = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4",
        description="The Base URL for all Swagger Ui Assets",
    )
    current_swagger_ui_parameters: Optional[dict] = Field(
        default={}, description="The current Swagger UI parameters"
    )
