import inspect
import re
import typing as t
from collections.abc import Callable
from functools import wraps
from typing import Any

from pydantic import BaseModel, create_model
from pydantic_core import PydanticUndefined
from typing_extensions import ParamSpec

from flask_jeroboam._utils import _lenient_issubclass, get_typed_signature
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.typing import JeroboamResponseReturnValue, JeroboamRouteCallable
from flask_jeroboam.view_arguments.arguments import (
    ArgumentLocation,
    BodyArgument,
    ViewArgument,
    get_argument_class,
)
from flask_jeroboam.view_arguments.functions import Body, File, Form
from flask_jeroboam.view_arguments.solved import SolvedArgument

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
R = t.TypeVar("R", bound=t.Any)
P = ParamSpec("P")
T = t.TypeVar("T", bound=t.Any)


pattern = r"(.*)\[(.+)\]$"


class InboundHandler:
    """The InboundHandler handles inbound data of a request.

    More precisely, it parses the incoming data, validates it, and injects it into the
    view function. It is also responsible for raising an InvalidRequest exception.
    The InboundHandler will only be called if the view function has type-annotated
    parameters.



    #TODO: Get Better at laying Out Levels of the Algorythm. Most Likely in the View
    # class.
    # And Moving away from the decorator scheme which feels obstrusive sometimes.
    """

    def __init__(self, view_func: Callable, main_http_verb: str, rule: str):
        self.main_http_verb = main_http_verb
        self.default_param_location = self._solve_default_params_location(
            main_http_verb
        )
        self.rule = rule
        self.path_param_names = set(re.findall(r"<(?:\w*:)?(\w*?)>", rule))
        self.query_params: list[SolvedArgument] = []
        self.path_params: list[SolvedArgument] = []
        self.header_params: list[SolvedArgument] = []
        self.cookie_params: list[SolvedArgument] = []
        self.body_params: list[SolvedArgument] = []
        self.form_params: list[SolvedArgument] = []
        self.file_params: list[SolvedArgument] = []
        self.other_params: list[SolvedArgument] = []
        self.locations_to_visit: set[ArgumentLocation] = set()
        self._solve_params(view_func)
        self._check_compliance()
        self._body_field: SolvedArgument | None = None

    @staticmethod
    def _solve_default_params_location(
        main_http_verb: str,
    ) -> ArgumentLocation:
        """Return the default FieldInfo for the InboundHandler."""
        if main_http_verb in {"POST", "PUT"}:
            return ArgumentLocation.body
        if main_http_verb == "GET":
            return ArgumentLocation.query
        return ArgumentLocation.path

    @property
    def parameters(self) -> list[SolvedArgument]:
        """Return all Parameters of the InboundHandler."""
        return (
            self.query_params
            + self.path_params
            + self.header_params
            + self.cookie_params
        )

    @property
    def body_arguments(self) -> list[SolvedArgument]:
        """Return all Body Arguments of the InboundHandler."""
        return self.body_params + self.form_params + self.file_params

    @property
    def is_valid(self) -> bool:
        """Check if the InboundHandler has any Configured Parameters."""
        return len(self.locations_to_visit) > 0

    @property
    def has_request_body(self) -> bool:
        """Check if the InboundHandler has any Configured Parameters."""
        return len(self.body_arguments) > 0

    def body_field(self, name: str | None = None) -> SolvedArgument | None:
        """The Body Arguments are combined into a single Body Field."""
        if self._body_field is None and self.body_arguments and name is not None:
            self._body_field = self._build_body_field(name)
        return self._body_field

    def _solve_body_field_info(self) -> BodyArgument:
        """Return the Body FieldInfo for the InboundHandler.

        Has unreachable branches. Single Arguments never reach this method.
        """
        body_field_info_kwargs: dict[str, Any] = {"default": None, "embed": False}
        if len(self.file_params) > 0:  # pragma: no cover
            body_field_info: Callable = File
        elif len(self.form_params) > 0:
            body_field_info = Form
        else:
            body_field_info = Body
            body_param_media_types = [
                f.field_info.media_type
                for f in self.body_arguments
                if isinstance(f.field_info, BodyArgument)
            ]
            if len(set(body_param_media_types)) == 1:  # pragma: no cover
                body_field_info_kwargs["media_type"] = body_param_media_types[0]
        return body_field_info(**body_field_info_kwargs)

    def _build_body_field(self, name: str) -> SolvedArgument | None:
        """Build the Body Field from the Body Arguments.

        TODO: refactor this method: inelegant.
        TODO: warn if multiple locations are used.
        TODO: embed should be set to True if multiple BaseModel are used.
        embed should only be used to build the body field.
        """
        first_param = self.body_arguments[0]
        field_info = first_param.field_info
        body_param_names_set = {param.name for param in self.body_arguments}
        if (
            len(body_param_names_set) == 1
            and getattr(field_info, "embed", None) is not None
        ):
            if not _lenient_issubclass(first_param.annotation, BaseModel):
                first_param.embed = True
            return first_param
        model_name = f"{name}_request_body_as_model"
        any_embed = any(argument.embed for argument in self.body_arguments)
        any_required = any(argument.required for argument in self.body_arguments)
        field_defs: dict[str, Any] = {}
        for argument in self.body_arguments:
            argument.embed = any_embed
            if argument.required:
                field_defs[argument.name] = (argument.annotation, ...)
            else:
                field_defs[argument.name] = (argument.annotation, argument.default)
        BodyModel: type[BaseModel] = create_model(model_name, **field_defs)  # noqa: N806
        body_field_info = self._solve_body_field_info()
        return SolvedArgument.specialize(
            name=name,
            annotation=BodyModel,
            required=any_required,
            view_param=body_field_info,
        )

    def add_inbound_handling_to(
        self, view_func: JeroboamRouteCallable
    ) -> JeroboamRouteCallable:
        """It injects inbound parsed and validated data into the view function."""

        @wraps(view_func)
        def wrapper(*args, **kwargs) -> JeroboamResponseReturnValue:
            inbound_values, errors = self._parse_and_validate_inbound_data(**kwargs)
            if errors:
                raise InvalidRequest(errors)
            return view_func(*args, **inbound_values)

        return wrapper

    def _check_compliance(self):
        """Will warn the user if their view function does something a bit off."""
        if len(self.form_params + self.file_params) > 0 and self.main_http_verb not in {
            "POST",
            "PUT",
            "PATCH",
        }:
            import warnings

            warnings.warn(
                f"You have defined Form or File Parameters on a {self.main_http_verb} "
                "request. This is not supported by Flask: "
                "https://flask.palletsprojects.com/en/2.2.x/api/#incoming-request-data",
                UserWarning,
                stacklevel=2,
            )

    def _solve_params(self, view_func: Callable):
        """Registering the Parameters of the View Function."""
        signature = get_typed_signature(view_func)
        for parameter_name, parameter in signature.parameters.items():
            solved_param = self._solve_view_function_parameter(
                param_name=parameter_name, param=parameter
            )
            # Check if Param is in Path (not needed for now)
            self._register_view_parameter(solved_param)

    def _solve_view_function_parameter(
        self,
        param_name: str,
        param: inspect.Parameter,
        force_location: ArgumentLocation | None = None,
        ignore_default: bool = False,
    ) -> SolvedArgument:
        """Analyse the param and its annotation to solve its configiration.

        At the end of this process, we want to know the following things:
        - What is its location?
        - What is its type/annotation?
        - Is it a scalar or a sequence?
        - Is it required and/or has a default value?
        # Split it into functions for each step.
        """
        solved_location = self._solve_location(param_name, param, force_location)
        # Get the ViewParam
        if isinstance(param.default, ViewArgument):
            view_param = param.default
        else:
            param_class = get_argument_class(solved_location)
            raw_default = param.default
            if raw_default is param.empty or raw_default is Ellipsis:
                raw_default = PydanticUndefined
            view_param = param_class(raw_default)

        default_value = self._solve_default_value(param, ignore_default)
        # Solving Required
        required: bool = default_value is PydanticUndefined
        annotation = param.annotation if param.annotation != param.empty else Any

        return SolvedArgument.specialize(
            name=param_name,
            annotation=annotation,
            required=required,
            view_param=view_param,
        )

    def _solve_location(
        self,
        param_name: str,
        param: inspect.Parameter,
        force_location: ArgumentLocation | None = None,
    ) -> ArgumentLocation:
        if param_name in self.path_param_names:
            return ArgumentLocation.path
        return getattr(
            param.default, "location", force_location or self.default_param_location
        )

    def _solve_default_value(
        self,
        param: inspect.Parameter,
        ignore_default: bool,
    ) -> Any:
        default_value: Any = getattr(param.default, "default", param.default)
        if (
            default_value in {param.empty, Ellipsis, PydanticUndefined}
            or ignore_default
        ):
            default_value = PydanticUndefined
        return default_value

    def _register_view_parameter(self, solved_parameter: SolvedArgument) -> None:
        """Registering the Solved View parameters for the View Function.

        The registration will put the params in the right list
        and add the location to the locations_to_visit set.
        """
        assert solved_parameter.location is not None  # noqa: S101
        self.locations_to_visit.add(solved_parameter.location)
        {
            ArgumentLocation.query: self.query_params,
            ArgumentLocation.path: self.path_params,
            ArgumentLocation.header: self.header_params,
            ArgumentLocation.body: self.body_params,
            ArgumentLocation.form: self.form_params,
            ArgumentLocation.cookie: self.cookie_params,
            ArgumentLocation.file: self.file_params,
        }.get(solved_parameter.location, self.other_params).append(solved_parameter)

    def _parse_and_validate_inbound_data(self, **kwargs) -> tuple[dict, list[dict]]:
        """Parse and Validate the request Inbound data."""
        errors = []
        values = {}
        for param in self.parameters:
            values_, errors_ = param.validate_request()
            errors.extend(errors_)
            values.update(values_)
        if body_field := self.body_field(self.rule):
            body_value, body_errors = body_field.validate_request()
            errors.extend(body_errors)
            if len(self.body_arguments) > 1:
                # Synthetic model wraps multiple params — unpack fields
                # back into individual kwargs for the view function.
                for model in body_value.values():
                    if isinstance(model, BaseModel):  # pragma: no branch
                        for field_name in type(model).model_fields:
                            values[field_name] = getattr(model, field_name)
            else:
                values.update(body_value)
        return values, errors
