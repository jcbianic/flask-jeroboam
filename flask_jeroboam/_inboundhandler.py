import inspect
import re
import typing as t
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union

from pydantic import BaseModel
from pydantic import create_model
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Undefined
from pydantic.schema import get_annotation_from_field_info
from typing_extensions import ParamSpec

from flask_jeroboam._utils import create_field
from flask_jeroboam._utils import get_typed_signature
from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.typing import JeroboamResponseReturnValue
from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.view_arguments.arguments import ArgumentLocation
from flask_jeroboam.view_arguments.arguments import BodyArgument
from flask_jeroboam.view_arguments.arguments import ViewArgument
from flask_jeroboam.view_arguments.arguments import get_argument_class
from flask_jeroboam.view_arguments.functions import Body
from flask_jeroboam.view_arguments.functions import File
from flask_jeroboam.view_arguments.functions import Form
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
        self.query_params: List[SolvedArgument] = []
        self.path_params: List[SolvedArgument] = []
        self.header_params: List[SolvedArgument] = []
        self.cookie_params: List[SolvedArgument] = []
        self.body_params: List[SolvedArgument] = []
        self.form_params: List[SolvedArgument] = []
        self.file_params: List[SolvedArgument] = []
        self.other_params: List[SolvedArgument] = []
        self.locations_to_visit: Set[ArgumentLocation] = set()
        self._solve_params(view_func)
        self._check_compliance()
        self._body_field: Optional[SolvedArgument] = None

    @staticmethod
    def _solve_default_params_location(
        main_http_verb: str,
    ) -> ArgumentLocation:
        """Return the default FieldInfo for the InboundHandler."""
        if main_http_verb in {"POST", "PUT"}:
            return ArgumentLocation.body
        elif main_http_verb == "GET":
            return ArgumentLocation.query
        else:
            return ArgumentLocation.path

    @property
    def parameters(self) -> List[SolvedArgument]:
        """Return all Parameters of the InboundHandler."""
        return (
            self.query_params
            + self.path_params
            + self.header_params
            + self.cookie_params
        )

    @property
    def body_arguments(self) -> List[SolvedArgument]:
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

    def body_field(self, name: Optional[str] = None) -> Optional[SolvedArgument]:
        """The Body Arguments are combined into a single Body Field."""
        if self._body_field is None and self.body_arguments and name:
            self._body_field = self._build_body_field(name)
        return self._body_field

    def _solve_body_field_info(self) -> BodyArgument:
        """Return the Body FieldInfo for the InboundHandler.

        Has unreachable branches. Single Arguments never reach this method.
        """
        body_field_info_kwargs: Dict[str, Any] = {"default": None}
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

    def _build_body_field(self, name: str) -> Optional[SolvedArgument]:
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
            and not getattr(field_info, "embed", None) is None
        ):
            if not issubclass(first_param.type_, BaseModel):
                first_param.embed = True
            return first_param
        model_name = f"{name}_request_body_as_model"
        BodyModel: Type[BaseModel] = create_model(model_name)  # noqa: N806
        any_embed = any(argument.embed for argument in self.body_arguments)
        any_required = any(argument.required for argument in self.body_arguments)
        for argument in self.body_arguments:
            argument.embed = any_embed
            BodyModel.__fields__[argument.name] = argument
        field_info = self._solve_body_field_info()
        field = create_field(
            name=BodyModel.__name__,
            type_=BodyModel,
            required=any_required,
            alias="body",
            field_info=field_info,
            class_validators={},
        )
        assert field  # noqa: S101
        return SolvedArgument.specialize(
            name=name,
            type_=field.type_,
            required=any_required,
            view_param=field_info,
        )

    def add_inbound_handling_to(
        self, view_func: JeroboamRouteCallable
    ) -> JeroboamRouteCallable:
        """It injects inbound parsed and validated data into the view function."""

        @wraps(view_func)
        def wrapper(*args, **kwargs) -> JeroboamResponseReturnValue:
            inbound_values, errors = self._parse_and_validate_inbound_data(**kwargs)
            if errors:
                raise InvalidRequest([errors])
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
                f"You have defined Form or File Parameters on a {self.main_http_verb}"
                "request. This is not supported by Flask:"
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
        force_location: Optional[ArgumentLocation] = None,
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
            view_param = param_class(param.default)

        default_value = self._solve_default_value(param, ignore_default)
        # Solving Required
        required: bool = default_value is Undefined or getattr(
            view_param, "required", False
        )
        annotation = param.annotation if param.annotation != param.empty else Any
        annotation = get_annotation_from_field_info(annotation, view_param, param_name)

        return SolvedArgument.specialize(
            name=param_name,
            type_=annotation,
            required=required,
            view_param=view_param,
        )

    def _solve_location(
        self,
        param_name: str,
        param: inspect.Parameter,
        force_location: Optional[ArgumentLocation] = None,
    ) -> ArgumentLocation:
        if param_name in self.path_param_names:
            return ArgumentLocation.path
        else:
            return getattr(
                param.default, "location", force_location or self.default_param_location
            )

    def _solve_default_value(
        self,
        param: inspect.Parameter,
        ignore_default: bool,
    ) -> Any:
        default_value: Any = getattr(param.default, "default", param.default)
        if default_value in {param.empty, Ellipsis} or ignore_default:
            default_value = Undefined
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

    def _parse_and_validate_inbound_data(
        self, **kwargs
    ) -> Tuple[Dict, Union[List, ErrorWrapper]]:
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
            values.update(body_value)
        return values, errors
