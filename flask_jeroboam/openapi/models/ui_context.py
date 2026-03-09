"""Models for OpenAPI 3.0.0."""

from pydantic import Field

from flask_jeroboam.models import OutboundModel


class SwaggerContextOut(OutboundModel):
    """Swagger Outbound Model."""

    title: str | None = Field(
        default="Swagger UI", description="Title of the Swagger UI"
    )
    swagger_ui_url: str | None = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4",
        description="The Base URL for all Swagger Ui Assets",
    )
    current_swagger_ui_parameters: dict | None = Field(
        default={}, description="The current Swagger UI parameters"
    )
