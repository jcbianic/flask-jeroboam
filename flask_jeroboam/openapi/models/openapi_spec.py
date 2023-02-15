"""OpenAPI Specification models.

Credits: A fork of FASTAPI's openapi/models.py
"""
from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from pydantic import AnyUrl
from pydantic import Field

from flask_jeroboam.logger import logger
from flask_jeroboam.models import OutboundModel


try:
    import email_validator
    from pydantic import EmailStr  # type: ignore
except ImportError:  # pragma: no cover

    class EmailStr(str):  # type: ignore
        @classmethod
        def __get_validators__(cls) -> Iterable[Callable[..., Any]]:
            yield cls.validate

        @classmethod
        def validate(cls, v: Any) -> str:
            """Raises a warning if email-validator is not installed."""
            logger.warning(
                "email-validator not installed, email fields will be treated as str.\n"
                "To install, run: poetry add pydantic[email-validator]"
            )
            return str(v)


class Contact(OutboundModel):
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[EmailStr] = None

    class Config:
        extra = "allow"


class License(OutboundModel):
    name: str
    url: Optional[AnyUrl] = None

    class Config:
        extra = "allow"


class Info(OutboundModel):
    title: str
    description: Optional[str] = None
    terms_of_service: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None
    version: str

    class Config:
        extra = "allow"


class ServerVariable(OutboundModel):
    enum: Optional[List[str]] = None
    default: str
    description: Optional[str] = None

    class Config:
        extra = "allow"


class Server(OutboundModel):
    url: Union[AnyUrl, str]
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariable]] = None

    class Config:
        extra = "allow"


class Reference(OutboundModel):
    ref: str = Field(alias="$ref")


class Discriminator(OutboundModel):
    property_name: str
    mapping: Optional[Dict[str, str]] = None


class XML(OutboundModel):
    name: Optional[str] = None
    namespace: Optional[str] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = None
    wrapped: Optional[bool] = None

    class Config:
        extra = "allow"


class ExternalDocumentation(OutboundModel):
    description: Optional[str] = None
    url: AnyUrl

    class Config:
        extra = "allow"


class Schema(OutboundModel):
    ref: Optional[str] = Field(default=None, alias="$ref")
    title: Optional[str] = None
    multiple_of: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    max_length: Optional[int] = Field(default=None, gte=0)
    min_length: Optional[int] = Field(default=None, gte=0)
    pattern: Optional[str] = None
    max_items: Optional[int] = Field(default=None, gte=0)
    min_items: Optional[int] = Field(default=None, gte=0)
    unique_items: Optional[bool] = None
    max_properties: Optional[int] = Field(default=None, gte=0)
    min_properties: Optional[int] = Field(default=None, gte=0)
    required: Optional[List[str]] = None
    enum: Optional[List[Any]] = None
    type: Optional[str] = None
    all_of: Optional[List["Schema"]] = None
    one_of: Optional[List["Schema"]] = None
    any_of: Optional[List["Schema"]] = None
    not_: Optional["Schema"] = Field(default=None, alias="not")
    items: Optional[Union["Schema", List["Schema"]]] = None
    properties: Optional[Dict[str, "Schema"]] = None
    additional_properties: Optional[Union["Schema", Reference, bool]] = None
    description: Optional[str] = None
    format: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = None
    discriminator: Optional[Discriminator] = None
    read_only: Optional[bool] = None
    write_only: Optional[bool] = None
    xml: Optional[XML] = None
    external_docs: Optional[ExternalDocumentation] = None
    example: Optional[Any] = None
    deprecated: Optional[bool] = None

    class Config:
        extra: str = "allow"


class Example(OutboundModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    external_value: Optional[AnyUrl] = None

    class Config:
        extra = "allow"


class ParameterInType(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Encoding(OutboundModel):
    content_type: Optional[str] = None
    headers: Optional[Dict[str, Union["Header", Reference]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None

    class Config:
        extra = "allow"


class MediaType(OutboundModel):
    schema_: Optional[Union[Schema, Reference]] = Field(default=None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None

    class Config:
        extra = "allow"


class ParameterBase(OutboundModel):
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    # Serialization rules for simple scenarios
    style: Optional[str] = None
    explode: Optional[bool] = None
    allow_reserved: Optional[bool] = None
    schema_: Optional[Union[Schema, Reference]] = Field(default=None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    # Serialization rules for more complex scenarios
    content: Optional[Dict[str, MediaType]] = None

    class Config:
        extra = "allow"


class Parameter(ParameterBase):
    name: str
    in_: ParameterInType = Field(alias="in")


class Header(ParameterBase):
    pass


class RequestBody(OutboundModel):
    description: Optional[str] = None
    content: Dict[str, MediaType]
    required: Optional[bool] = None

    class Config:
        extra = "allow"


class Link(OutboundModel):
    operation_ref: Optional[str] = None
    operation_id: Optional[str] = None
    parameters: Optional[Dict[str, Union[Any, str]]] = None
    request_body: Optional[Union[Any, str]] = None
    description: Optional[str] = None
    server: Optional[Server] = None

    class Config:
        extra = "allow"


class Response(OutboundModel):
    description: str
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None

    class Config:
        extra = "allow"


class Operation(OutboundModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    external_docs: Optional[ExternalDocumentation] = None
    operation_id: Optional[str] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    request_body: Optional[Union[RequestBody, Reference]] = None
    # Using Any for Specification Extensions
    responses: Dict[str, Union[Response, Any]]
    callbacks: Optional[Dict[str, Union[Dict[str, "PathItem"], Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    servers: Optional[List[Server]] = None

    class Config:
        extra = "allow"


class PathItem(OutboundModel):
    ref: Optional[str] = Field(default=None, alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None

    class Config:
        extra = "allow"


class SecuritySchemeType(Enum):
    api_key = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    open_id_connect = "openIdConnect"


class SecurityBase(OutboundModel):
    type_: SecuritySchemeType = Field(alias="type")
    description: Optional[str] = None

    class Config:
        extra = "allow"


class APIKeyIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


class APIKey(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.api_key, alias="type")
    in_: APIKeyIn = Field(alias="in")
    name: str


class HTTPBase(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.http, alias="type")
    scheme: str


class HTTPBearer(HTTPBase):
    scheme = "bearer"
    bearer_format: Optional[str] = None


class OAuthFlow(OutboundModel):
    refresh_url: Optional[str] = None
    scopes: Dict[str, str] = {}

    class Config:
        extra = "allow"


class OAuthFlowImplicit(OAuthFlow):
    authorization_url: str


class OAuthFlowPassword(OAuthFlow):
    token_url: str


class OAuthFlowClientCredentials(OAuthFlow):
    token_url: str


class OAuthFlowAuthorizationCode(OAuthFlow):
    authorization_url: str
    token_url: str


class OAuthFlows(OutboundModel):
    implicit: Optional[OAuthFlowImplicit] = None
    password: Optional[OAuthFlowPassword] = None
    client_credentials: Optional[OAuthFlowClientCredentials] = None
    authorization_code: Optional[OAuthFlowAuthorizationCode] = None

    class Config:
        extra = "allow"


class OAuth2(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.oauth2, alias="type")
    flows: OAuthFlows


class OpenIdConnect(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.open_id_connect, alias="type")
    open_id_connect_url: str


SecurityScheme = Union[APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer]


class Components(OutboundModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    request_bodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    security_schemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    # Using Any for Specification Extensions
    callbacks: Optional[Dict[str, Union[Dict[str, PathItem], Reference, Any]]] = None

    class Config:
        extra = "allow"


class Tag(OutboundModel):
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocumentation] = None

    class Config:
        extra = "allow"


class OpenAPI(OutboundModel):
    openapi: str
    info: Info
    servers: Optional[List[Server]] = None
    # Using Any for Specification Extensions
    paths: Dict[str, Union[PathItem, Any]]
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    external_docs: Optional[ExternalDocumentation] = None

    class Config:
        extra = "allow"


Schema.update_forward_refs()
Operation.update_forward_refs()
Encoding.update_forward_refs()
