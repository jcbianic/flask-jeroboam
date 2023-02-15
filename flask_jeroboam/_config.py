from typing import List
from typing import Optional

from pydantic import BaseSettings
from pydantic import Field

from flask_jeroboam.openapi.models.openapi_spec import Server


class JeroboamConfig(BaseSettings):
    """Jeroboam Config."""

    JEROBOAM_TITLE: Optional[str] = Field(None)
    JEROBOAM_VERSION: Optional[str] = Field("0.1.0")
    JEROBOAM_DESCRIPTION: Optional[str] = Field(None)
    JEROBOAM_TERMS_OF_SERVICE: Optional[str] = Field(None)
    JEROBOAM_CONTACT: Optional[str] = Field(None)
    JEROBOAM_LICENCE_INFO: Optional[str] = Field(None)
    JEROBOAM_OPENAPI_VERSION: Optional[str] = Field("3.0.2")
    JEROBOAM_SERVERS: Optional[List[Server]] = Field([])
    JEROBOAM_OPENAPI_DISABLED: Optional[bool] = Field(default=False)
    JEROBOAM_OPENAPI_URL: Optional[str] = Field(default="/docs")

    @classmethod
    def load(cls) -> "JeroboamConfig":
        """Load config."""
        return cls.parse_obj({})
