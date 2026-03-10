from pydantic import Field
from pydantic_settings import BaseSettings

from flask_jeroboam.openapi.models.openapi import Server


class JeroboamConfig(BaseSettings):
    """Jeroboam Config."""

    JEROBOAM_REGISTER_OPENAPI: bool | None = Field(default=True)

    JEROBOAM_TITLE: str | None = Field(None)
    JEROBOAM_VERSION: str | None = Field("0.1.0")
    JEROBOAM_DESCRIPTION: str | None = Field(None)
    JEROBOAM_TERMS_OF_SERVICE: str | None = Field(None)
    JEROBOAM_CONTACT: str | None = Field(None)
    JEROBOAM_LICENCE_INFO: str | None = Field(None)
    JEROBOAM_OPENAPI_VERSION: str | None = Field("3.0.2")
    JEROBOAM_SERVERS: list[Server] | None = Field([])
    JEROBOAM_OPENAPI_URL: str | None = Field(default="/docs")

    JEROBOAM_REGISTER_ERROR_HANDLERS: bool | None = Field(default=True)

    @classmethod
    def load(cls) -> "JeroboamConfig":
        """Load config."""
        return cls.model_validate({})
