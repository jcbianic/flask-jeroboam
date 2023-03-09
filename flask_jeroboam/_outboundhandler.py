import dataclasses
import traceback
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from flask import Response
from flask.globals import current_app
from pydantic import BaseConfig
from pydantic import BaseModel
from pydantic import create_model
from pydantic import validate_model
from pydantic.fields import FieldInfo
from typing_extensions import ParamSpec

from flask_jeroboam._constants import METHODS_DEFAULT_STATUS_CODE
from flask_jeroboam._constants import NO_BODY_STATUS_CODES
from flask_jeroboam._utils import create_field
from flask_jeroboam._utils import get_typed_return_annotation
from flask_jeroboam.exceptions import ResponseValidationError
from flask_jeroboam.responses import JSONResponse
from flask_jeroboam.typing import HeadersValue
from flask_jeroboam.typing import JeroboamBodyType
from flask_jeroboam.typing import JeroboamResponseReturnValue
from flask_jeroboam.typing import JeroboamRouteCallable
from flask_jeroboam.typing import ResponseModel
from flask_jeroboam.typing import Union


# from flask_jeroboam.typing import TypedParams
# from flask_jeroboam.utils import get_typed_return_annotation


P = ParamSpec("P")
R = TypeVar("R")


class OutboundHandler:
    """The OutboundHandler handles outbound data of a request.

    More precisely, it prepare the content of the response, serializes it,
    determines the status code and form a proper Response object.

    The OutboundHandler will always be called if the view function
    returns without raising exception. Although if it receive an already
    well formed Response object, it will just return it.
    It's main purpose and public method is to add_outbound_handling_to
    """

    def __init__(
        self,
        view_func: Callable,
        configured_status_code: Optional[int],
        main_http_verb: str,
        options: Dict[str, Any],
        response_class: Type = JSONResponse,
    ):
        self.response_model = self._solve_response_model(view_func, options)
        self.configured_status_code = configured_status_code
        self.method_default_status_code = self._solve_default_status_code_by_http_verb(
            main_http_verb, configured_status_code
        )
        self.response_class = response_class
        self.response_description = options.pop(
            "response_description", "Successful Response"
        )

    @property
    def latent_status_code(self) -> int:
        """The status code that will be used if no status code is provided."""
        return self._solve_status_code(None)

    @property
    def response_field(self):
        """The response_model as model field."""
        if self.response_model is None:
            return None
        class_validators = getattr(self.response_model, "__validators__", {})
        field_info = getattr(self.response_model, "field_info", FieldInfo())
        model_config = getattr(self.response_model, "__config__", BaseConfig)
        return create_field(
            name=self.response_model.__name__,
            type_=self.response_model,
            class_validators=class_validators,
            required=True,
            model_config=model_config,
            field_info=field_info,
        )

    def add_outbound_handling_to(
        self, view_func: JeroboamRouteCallable
    ) -> JeroboamRouteCallable:
        """Add outbound handling to a view funcion."""

        @wraps(view_func)
        def outbound_handling(*args: Any, **kwargs: Any) -> JeroboamResponseReturnValue:
            """Coordinating the outbound data handling.

            It starts by executing the view_func with the given args and kwargs.
            At this point, the inbound handling has already parsed, validated
            and injected the incoming data in agrs and kwargs, provided it was
            configured to do so.
            If the initial response is already a well-formed Response object,
            it is returned as is.
            If not, it solve status code, serialize the content and finally
            build a Response object with it.
            It may raise a ValidationError if the outgoing data is not valid.

            Credits: this algorithm and subalgorithms are inspired by FastAPI.
            """
            initial_return_value = current_app.ensure_sync(view_func)(*args, **kwargs)
            if issubclass(initial_return_value.__class__, Response):
                return initial_return_value
            (
                returned_body,
                returned_status_code,
                headers,
            ) = self._unpack_view_function_return_value(initial_return_value)
            solved_status_code = self._solve_status_code(returned_status_code)
            if self._status_code_forbids_body(solved_status_code):
                return self._build_response(
                    status_code=solved_status_code, headers=headers
                )
            if self.response_model is None:
                return returned_body, solved_status_code, headers
            content = self._serialize_content(returned_body)
            return self._build_response(content, solved_status_code, headers=headers)

        return outbound_handling

    def _unpack_view_function_return_value(
        self, initial_return_value: JeroboamResponseReturnValue
    ) -> Tuple[JeroboamBodyType, Optional[int], Optional[HeadersValue]]:
        """Unpack the return value of the view function.

        Flask support various shapes of return values in their view function.
        We accomodate for theses shapes, but force them into a body/status_code
        /headers tuple.
        """
        if isinstance(initial_return_value, tuple):
            if len(initial_return_value) == 3:
                return initial_return_value  # type: ignore
            elif len(initial_return_value) == 2:
                if isinstance(initial_return_value[1], int):
                    return (
                        initial_return_value[0],
                        initial_return_value[1],  # type:ignore
                        {},
                    )
                else:
                    return (
                        initial_return_value[0],
                        None,
                        initial_return_value[1],  # type:ignore
                    )
            else:
                raise TypeError(
                    "The view function did not return a valid response tuple."
                    " The tuple must have the form (body, status, headers),"
                    " (body, status), or (body, headers)."
                )
        return initial_return_value, None, None  # type: ignore

    def _solve_response_model(
        self, view_func: Callable, options: Dict[str, Any]
    ) -> Optional[ResponseModel]:
        """Extract the Response Model from view function.

        The reponse_model must be a subclass of pydantic.BaseModel
        or a list of a of pydantic.BaseModel. Otherwise a type Error will be raised.
        It can be set in the options or a as return type annotation of the view
        function.
        The first one will take prescedence over the latter.
        Thus, to turn off registering a reponse_model, even when your
        view_function has a return annotation, set it to None.
        ..implementation details VS FastAPI:
            * Creating a model with root seems to do the trick. No need to generate
              a model_field from the response_model ?
            * Cloning the response_field doesn't seem to be necessary either
              to filter out unwanted data.
        """
        response_model: Optional[Type] = options.pop(
            "response_model", get_typed_return_annotation(view_func)
        )
        if response_model is None:
            return None

        if getattr(response_model, "__origin__", None) == list:
            field: Type = response_model.__args__[0]
            response_model = create_model(
                f"{field.__name__}AsList",
                __root__=(List[field], ...),  # type: ignore[valid-type]
            )
        assert response_model is not None  # noqa: S101
        if not issubclass(response_model, BaseModel):
            raise TypeError(
                "The response model must be a subclass of pydantic.BaseModel."
            )
        return response_model

    def _solve_default_status_code_by_http_verb(
        self, http_verb: str, configured_status_code: Optional[int]
    ) -> Optional[int]:
        """Determines sensible default status code depending for the main HTTP VERB.

        TODO: Add a CONFIGURATION OPTION for this.
        """
        method_status_code = METHODS_DEFAULT_STATUS_CODE.get(http_verb, None)
        if method_status_code is None and configured_status_code is None:
            import warnings

            warnings.warn(
                f"No sensible default status code for verb {http_verb}."
                "Maybe it's a exotic one. Make sure to set the status_code"
                "in the options and if you think we should add it, please fill"
                "an issue.",
                UserWarning,
                stacklevel=2,
            )
        return method_status_code

    def _solve_status_code(self, returned_status_code: Optional[int]) -> int:
        """Solve the status code from this Response.

        In order of priority:
        - the status code returned by the view function
        - the status code set in the options
        - the default status code for the main HTTP verb
        - the default status code for the ResponseClass


        TODO: Warning if conflict ?
        """
        candidates = [
            candidate
            for candidate in [
                returned_status_code,
                self.configured_status_code,
                self.method_default_status_code,
                self.response_class.default_status_code,
            ]
            if candidate is not None
        ]
        return candidates[0]

    def _serialize_content(self, content: JeroboamBodyType) -> Any:
        """Serialize the content of the response.

        # TODO: Algo de Sérialisation du Content de la Réponse.
        # Called only when we have a response_model
        # Sinon prepare_content qui renvoie un dict (option pour l'orm_mode)
        # On valide le dict avec le response_model et on collecte les erreurs
        # de validation
        # Option pour Couroutine or note
        # On raise un ValueError avec toutes les erreurs pas seulement la première.
        # on json_encode avec des options

        TODO: Ability to render_template ?
        TODO: Gestions des CoRoutine ?
        TODO: Plus d'options pour le passage en JSON ?
        TODO: Determine if we need by_alias, exclude_unset,
        exclude_defaults, exclude_none options ?
        """
        assert self.response_model is not None  # noqa: S101
        outbound_data: dict = self._adapt_datastructure_of(content)  # type: ignore
        values, _, error = validate_model(self.response_model, outbound_data)
        if error:
            raise ResponseValidationError(
                "A validation", error, traceback.format_exc()
            ) from error
        return self.response_model(**values).json()

    def _adapt_datastructure_of(
        self, content: JeroboamBodyType
    ) -> Union[Dict, List[Any]]:
        """Prepare the content of the response.

        It basically accomodate for different datastructures and convert
        them to a dict.

        TODO: Do we support the ORM Mode ?$
        TODO: Better Name ?
        """
        if isinstance(content, dict):
            return content
        elif isinstance(content, BaseModel):
            return content.dict()
        elif isinstance(content, list):
            return {
                "__root__": [self._adapt_datastructure_of(item) for item in content]
            }
        elif dataclasses.is_dataclass(content):
            return dataclasses.asdict(content)

        raise ValueError("Content must be a list, a dict, a dataclass, or a BaseModel.")

    def _build_response(
        self,
        content: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[HeadersValue] = None,
    ) -> Response:
        """Make a Response Object from content and status code, and passed_headers."""
        # Do we replace with a check on content is None ?
        if content is None:
            return self.response_class(status=status_code, headers=headers)
        return self.response_class(content, status=status_code, headers=headers)

    def _status_code_forbids_body(self, status_code: int) -> bool:
        """Check if the status code allows a body.

        Credits: Inspired by FastAPI.
        """
        return status_code < 200 or str(status_code) in NO_BODY_STATUS_CODES
