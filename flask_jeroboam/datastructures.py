"""DataStructures.

Credits: this module is essentially a for of FastAPI's datastructures.py module.
"""

from collections.abc import Callable, Iterable
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from werkzeug.datastructures import FileStorage


class UploadFile(FileStorage):
    """A wrapper around werkzeug.datastructures.FileStorage.

    Credits: Adaptation of FastAPI's UploadFile.
    """

    @classmethod
    def __get_validators__(cls: type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        """Pydantic v1 compat validator (used by pydantic.v1 ModelField shim)."""
        yield cls.validate

    @classmethod
    def validate(cls: type["FileStorage"], v: Any) -> Any:
        """Validate the value."""
        if not isinstance(v, FileStorage):
            raise ValueError(f"Expected FileStorage, received: {type(v)}")
        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Pydantic v2 schema."""
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: Any, handler: Any) -> dict[str, Any]:
        return {"type": "string", "format": "binary"}
