"""Models for OpenAPI 3.0.0."""

from typing import Optional

from pydantic import Field

from flask_jeroboam import OutboundModel


class SwaggerContextOut(OutboundModel):
    """Swagger Outbound Model."""

    title: str = Field("Swagger UI", description="Title of the Swagger UI")
    swagger_ui_url: Optional[str] = Field(
        default="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4",
        description="The Base URL for all swagger ui Assets",
    )
    current_swagger_ui_parameters: Optional[dict] = Field(
        default={}, description="The current Swagger UI parameters"
    )


class RedocOut(OutboundModel):
    """Swagger Outbound Model."""

    redoc: str
