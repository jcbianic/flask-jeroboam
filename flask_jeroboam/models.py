"""Model Helpers."""

from pydantic import BaseModel, ConfigDict


def snake_case_to_camel(string: str) -> str:
    """Convert snake_case_string to aCamelCaseString."""
    camel_case = string.title().replace("_", "")
    return camel_case[0].lower() + camel_case[1:]


class InboundModel(BaseModel):
    """Basic configuration for parsing Requests."""

    model_config = ConfigDict(
        alias_generator=snake_case_to_camel,
        populate_by_name=True,
    )


class OutboundModel(BaseModel):
    """Basic configuration for serializing Responses."""

    model_config = ConfigDict(
        alias_generator=snake_case_to_camel,
        populate_by_name=True,
    )

    def model_dump_json(self, **kwargs) -> str:
        """Serialize to JSON with camelCase keys by default."""
        kwargs.setdefault("by_alias", True)
        return super().model_dump_json(**kwargs)
