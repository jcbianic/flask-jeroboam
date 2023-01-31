import inspect
import re
import typing as t
from enum import Enum
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import Undefined
from pydantic.schema import get_annotation_from_field_info
from typing_extensions import ParamSpec

from flask_jeroboam.exceptions import InvalidRequest
from flask_jeroboam.typing import JeroboamResponseReturnValue
from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.view_params import ParamLocation
from flask_jeroboam.view_params import SolvedParameter
from flask_jeroboam.view_params import ViewParameter
from flask_jeroboam.view_params.parameters import get_parameter_class

from .utils import get_typed_signature


F = t.TypeVar("F", bound=t.Callable[..., t.Any])
R = t.TypeVar("R", bound=t.Any)
P = ParamSpec("P")
T = t.TypeVar("T", bound=t.Any)


class MethodEnum(str, Enum):
    """List of HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


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
        self.path_param_names = set(re.findall("<(?:.*:)?(.*?)>", rule))
        self.query_params: List[SolvedParameter] = []
        self.path_params: List[SolvedParameter] = []
        self.header_params: List[SolvedParameter] = []
        self.cookie_params: List[SolvedParameter] = []
        self.body_params: List[SolvedParameter] = []
        self.form_params: List[SolvedParameter] = []
        self.file_params: List[SolvedParameter] = []
        self.other_params: List[SolvedParameter] = []
        self.locations_to_visit: Set[ParamLocation] = set()
        self._solve_params(view_func)
        self._check_compliance()

    @staticmethod
    def _solve_default_params_location(
        main_http_verb: str,
    ) -> ParamLocation:
        """Return the default FieldInfo for the InboundHandler."""
        if main_http_verb in {"POST", "PUT"}:
            return ParamLocation.body
        elif main_http_verb == "GET":
            return ParamLocation.query
        else:
            return ParamLocation.path

    @property
    def is_valid(self) -> bool:
        """Check if the InboundHandler has any Configured Parameters."""
        return len(self.locations_to_visit) > 0

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
                f"You have defined Form or File Parameters on a "
                f"{self.main_http_verb} request. "
                "This is not supported by Flask:"
                "https://flask.palletsprojects.com/en/2.2.x/api/#incoming-request-data",
                UserWarning,
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
        force_location: Optional[ParamLocation] = None,
        ignore_default: bool = False,
    ) -> SolvedParameter:
        """Analyse the param and its annotation to solve its configiration.

        At the end of this process, we want to know the following things:
        - What is its location?
        - What is its type/annotation?
        - Is it a scalar or a sequence?
        - Is it required and/or has a default value?
        """
        # Solving Location
        if param_name in self.path_param_names:
            solved_location = ParamLocation.path
        else:
            solved_location = getattr(
                param.default, "location", force_location or self.default_param_location
            )
        # Get the ViewParam
        if isinstance(param.default, ViewParameter):
            view_param = param.default
        else:
            param_class = get_parameter_class(solved_location)
            view_param = param_class(default=param.default)

        # Solving Default Value
        default_value: Any = getattr(param.default, "default", param.default)
        if default_value == param.empty or ignore_default:
            default_value = Undefined

        # Solving Required
        required: bool = default_value is Undefined

        annotation = param.annotation if param.annotation != param.empty else Any
        annotation = get_annotation_from_field_info(annotation, view_param, param_name)

        return SolvedParameter(
            name=param_name,
            type_=annotation,
            required=required,
            view_param=view_param,
        )

    def _register_view_parameter(self, solved_parameter: SolvedParameter) -> None:
        """Registering the Solved View parameters for the View Function.

        The registration will put the params in the right list
        and add the location to the locations_to_visit set.
        """
        assert solved_parameter.location is not None  # noqa: S101
        self.locations_to_visit.add(solved_parameter.location)
        {
            ParamLocation.query: self.query_params,
            ParamLocation.path: self.path_params,
            ParamLocation.header: self.header_params,
            ParamLocation.body: self.body_params,
            ParamLocation.form: self.form_params,
            ParamLocation.cookie: self.cookie_params,
            ParamLocation.file: self.file_params,
        }.get(solved_parameter.location, self.other_params).append(solved_parameter)

    def _parse_and_validate_inbound_data(
        self, **kwargs
    ) -> Tuple[Dict, Union[List, ErrorWrapper]]:
        """Parse and Validate the request Inbound data."""
        errors = []
        values = {}
        for location in self.locations_to_visit:
            params = {
                ParamLocation.query: self.query_params,
                ParamLocation.path: self.path_params,
                ParamLocation.header: self.header_params,
                ParamLocation.body: self.body_params,
                ParamLocation.form: self.form_params,
                ParamLocation.cookie: self.cookie_params,
                ParamLocation.file: self.file_params,
            }.get(location, [])
            for param in params:
                values_, errors_ = param.validate_request()
                errors.extend(errors_)
                values.update(values_)
        return values, errors