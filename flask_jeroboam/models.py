"""Model Helpers."""
import json
import re
from typing import Callable
from typing import Union

from pydantic import BaseModel


def snake_case_to_camel(string: str) -> str:
    """Convert snake_case_string to aCamelCaseString."""
    camel_case = string.title().replace("_", "")
    return camel_case[0].lower() + camel_case[1:]


pattern = re.compile(r"(?<!^)(?=[A-Z])")


def convert_dict_keys_to(obj: Union[dict, list], convert_function: Callable) -> dict:
    """Convert all keys of a dict to a given format."""
    if isinstance(obj, list):
        return [
            convert_dict_keys_to(e, convert_function) if isinstance(e, dict) else e
            for e in obj
        ]
    new_object = {}
    for key, value in obj.items():
        new_object[convert_function(key)] = (
            convert_dict_keys_to(value, convert_function)
            if isinstance(value, dict) or isinstance(value, list)
            else value
        )
    return new_object


def underscore_to_camel(key: str) -> str:
    """Convert snake_case_string to aCamelCaseString."""
    under_pat = re.compile(r"_([a-z])")
    return under_pat.sub(lambda x: x.group(1).upper(), key)


def camel_case_to_snake(string: str) -> str:
    """Convert aCamelCaseString to snake_case_string."""
    return pattern.sub("_", string).lower()


def json_dumps_to_camel_case(*args, **kwargs):
    """Convert to JSON + convert keys to camelCase."""
    args = (convert_dict_keys_to(args[0], underscore_to_camel),) + args[1:]
    return json.dumps(*args, **kwargs)


class Parser(BaseModel):
    """Basic configuration for parsing Requests."""

    class Config:
        alias_generator = snake_case_to_camel
        allow_population_by_field_name = True


class Serializer(BaseModel):
    """Basic Configiration for serializing Responses."""

    class Config:
        json_dumps = json_dumps_to_camel_case
