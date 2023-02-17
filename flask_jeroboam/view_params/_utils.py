from functools import partial
from typing import Optional
from typing import Type

from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic.fields import ModelField

from flask_jeroboam.exceptions import JeroboamError


def create_field(
    *,
    name: str,
    type_: Type[BaseModel],
    required: bool,
    alias: str,
    field_info: FieldInfo,
    class_validators: dict,
) -> Optional[ModelField]:
    """Create a pydantic ModelField from a model class.

    TODO: Change the Link in the warning
    """
    class_validators = class_validators or {}
    field_info = field_info or FieldInfo()
    model_config = getattr(type_, "__config__", BaseConfig)

    derived_field = partial(
        ModelField,
        name=name,
        type_=type_,
        class_validators=class_validators,
        default=None,
        model_config=model_config,
        alias=alias,
        required=required,
    )

    try:
        return derived_field(field_info=field_info)
    except RuntimeError:
        raise JeroboamError(
            "Invalid args for response field! Hint: "
            f"check that {type_} is a valid"
            " Pydantic field type."
            "If you are using a return type annotation that "
            "is not a valid Pydantic "
            "field (e.g. Union[Response, dict, None]) you can"
            " disable generating the "
            "response model from the type annotation with the"
            "path operation decorator "
            "parameter response_model=None. Read more: "
            "https://fastapi.tiangolo.com/tutorial/response-model/"
        ) from None
