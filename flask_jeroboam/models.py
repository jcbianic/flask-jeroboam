"""Model Helpers."""

import json
import re
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict


def snake_case_to_camel(string: str) -> str:
    """Convert snake_case_string to aCamelCaseString."""
    camel_case = string.title().replace("_", "")
    return camel_case[0].lower() + camel_case[1:]


pattern = re.compile(r"(?<!^)(?=[A-Z])")


def convert_dict_keys_to(obj: dict | list, convert_function: Callable) -> dict | list:
    """Convert all keys of a dict to a given format."""
    if isinstance(obj, list):
        return [
            convert_dict_keys_to(e, convert_function) if isinstance(e, dict) else e
            for e in obj
        ]
    return {
        convert_function(key): (
            convert_dict_keys_to(value, convert_function)
            if isinstance(value, (dict, list))
            else value
        )
        for key, value in obj.items()
    }


def underscore_to_camel(key: str) -> str:
    """Convert snake_case_string to aCamelCaseString."""
    under_pat = re.compile(r"_([a-z])")
    return under_pat.sub(lambda x: x.group(1).upper(), key)


def json_dumps_to_camel_case(*args, **kwargs):
    """Convert to JSON + convert keys to camelCase."""
    args = (convert_dict_keys_to(args[0], underscore_to_camel),) + args[1:]
    return json.dumps(*args, **kwargs)


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
