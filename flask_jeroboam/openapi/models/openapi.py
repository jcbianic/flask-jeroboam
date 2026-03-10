"""OpenAPI Specification models.

Credits: A fork of FASTAPI's openapi/models.py
"""

from enum import Enum
from typing import Any, Optional, Union

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from flask_jeroboam._logger import logger

try:  # pragma: no cover
    import email_validator  # type: ignore
    from pydantic import EmailStr  # type: ignore

    assert email_validator  # noqa: S101
except ImportError:  # pragma: no cover
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import core_schema as _core_schema

    class EmailStr(str):  # type: ignore
        """An empty EmailStr to warn users if email-validator is not installed."""

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
        ) -> Any:
            return _core_schema.no_info_plain_validator_function(cls.validate)

        @classmethod
        def validate(cls, v: Any) -> str:
            """Raises a warning if email-validator is not installed."""
            logger.warning(
                "email-validator not installed, email fields will be treated as str.\n"
                "To install, run: pip install pydantic[email]"
            )
            return str(v)


class Contact(BaseModel):
    name: str | None = None
    url: AnyUrl | None = None
    email: EmailStr | None = None

    model_config = ConfigDict(extra="allow")


class License(BaseModel):
    name: str
    url: AnyUrl | None = None

    model_config = ConfigDict(extra="allow")


class Info(BaseModel):
    title: str
    description: str | None = None
    terms_of_service: str | None = Field(None, alias="termsOfService")
    contact: Contact | None = None
    license: License | None = None
    version: str

    model_config = ConfigDict(extra="allow")


class ServerVariable(BaseModel):
    enum: list[str] | None = None
    default: str
    description: str | None = None

    model_config = ConfigDict(extra="allow")


class Server(BaseModel):
    url: AnyUrl | str
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None

    model_config = ConfigDict(extra="allow")


class Reference(BaseModel):
    ref: str = Field(alias="$ref")


class Discriminator(BaseModel):
    property_name: str
    mapping: dict[str, str] | None = None


class XML(BaseModel):
    name: str | None = None
    namespace: str | None = None
    prefix: str | None = None
    attribute: bool | None = None
    wrapped: bool | None = None

    model_config = ConfigDict(extra="allow")


class ExternalDocumentation(BaseModel):
    description: str | None = None
    url: AnyUrl

    model_config = ConfigDict(extra="allow")


class Schema(BaseModel):
    ref: str | None = Field(default=None, alias="$ref")
    title: str | None = None
    multiple_of: float | None = Field(None, alias="multipleOf")
    maximum: float | None = None
    exclusive_maximum: float | None = Field(None, alias="exclusiveMaximum")
    minimum: float | None = None
    exclusive_minimum: float | None = Field(None, alias="exclusiveMinimum")
    max_length: int | None = Field(default=None, ge=0, alias="maxLength")
    min_length: int | None = Field(default=None, ge=0, alias="minLength")
    pattern: str | None = None
    max_items: int | None = Field(default=None, ge=0, alias="maxItems")
    min_items: int | None = Field(default=None, ge=0, alias="minItems")
    unique_items: bool | None = Field(None, alias="uniqueItems")
    max_properties: int | None = Field(default=None, ge=0, alias="maxProperties")
    min_properties: int | None = Field(default=None, ge=0, alias="minProperties")
    required: list[str] | None = None
    enum: list[Any] | None = None
    type: str | None = None
    all_of: list["Schema"] | None = Field(None, alias="allOf")
    one_of: list["Schema"] | None = Field(None, alias="oneOf")
    any_of: list["Schema"] | None = Field(None, alias="anyOf")
    not_: Optional["Schema"] = Field(default=None, alias="not")
    items: Union["Schema", list["Schema"]] | None = None
    properties: dict[str, "Schema"] | None = None
    additional_properties: Union["Schema", Reference, bool] | None = Field(
        None, alias="additionalProperties"
    )
    description: str | None = None
    format: str | None = None
    default: Any | None = None
    nullable: bool | None = None
    discriminator: Discriminator | None = None
    read_only: bool | None = Field(None, alias="readOnly")
    write_only: bool | None = Field(None, alias="writeOnly")
    xml: XML | None = None
    external_docs: ExternalDocumentation | None = Field(None, alias="externalDocs")
    example: Any | None = None
    deprecated: bool | None = None

    model_config = ConfigDict(extra="allow")


class Example(BaseModel):
    summary: str | None = None
    description: str | None = None
    value: Any | None = None
    external_value: AnyUrl | None = Field(None, alias="externalValue")

    model_config = ConfigDict(extra="allow")


class ParameterInType(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Encoding(BaseModel):
    content_type: str | None = Field(None, alias="contentType")
    headers: dict[str, Union["Header", Reference]] | None = None
    style: str | None = None
    explode: bool | None = None
    allow_reserved: bool | None = Field(None, alias="allowReserved")

    model_config = ConfigDict(extra="allow")


class MediaType(BaseModel):
    schema_: Schema | Reference | None = Field(default=None, alias="schema")
    example: Any | None = None
    examples: dict[str, Example | Reference] | None = None
    encoding: dict[str, Encoding] | None = None

    model_config = ConfigDict(extra="allow")


class ParameterBase(BaseModel):
    description: str | None = None
    required: bool | None = None
    deprecated: bool | None = None
    # Serialization rules for simple scenarios
    style: str | None = None
    explode: bool | None = None
    allow_reserved: bool | None = Field(None, alias="allowReserved")
    schema_: Schema | Reference | None = Field(default=None, alias="schema")
    example: Any | None = None
    examples: dict[str, Example | Reference] | None = None
    # Serialization rules for more complex scenarios
    content: dict[str, MediaType] | None = None

    model_config = ConfigDict(extra="allow")


class Parameter(ParameterBase):
    name: str
    in_: ParameterInType = Field(alias="in")


class Header(ParameterBase):
    pass


class RequestBody(BaseModel):
    description: str | None = None
    content: dict[str, MediaType]
    required: bool | None = None

    model_config = ConfigDict(extra="allow")


class Link(BaseModel):
    operation_ref: str | None = Field(None, alias="operationRef")
    operation_id: str | None = Field(None, alias="operationId")
    parameters: dict[str, Any | str] | None = None
    request_body: Any | str | None = Field(None, alias="requestBody")
    description: str | None = None
    server: Server | None = None

    model_config = ConfigDict(extra="allow")


class Response(BaseModel):
    description: str
    headers: dict[str, Header | Reference] | None = None
    content: dict[str, MediaType] | None = None
    links: dict[str, Link | Reference] | None = None

    model_config = ConfigDict(extra="allow")


class Operation(BaseModel):
    tags: list[str] | None = None
    summary: str | None = None
    description: str | None = None
    external_docs: ExternalDocumentation | None = Field(None, alias="externalDocs")
    operation_id: str | None = Field(None, alias="operationId")
    parameters: list[Parameter | Reference] | None = None
    request_body: RequestBody | Reference | None = Field(None, alias="requestBody")
    # Using Any for Specification Extensions
    responses: dict[str, Response | Any]
    callbacks: dict[str, dict[str, "PathItem"] | Reference] | None = None
    deprecated: bool | None = None
    security: list[dict[str, list[str]]] | None = None
    servers: list[Server] | None = None

    model_config = ConfigDict(extra="allow")


class PathItem(BaseModel):
    ref: str | None = Field(default=None, alias="$ref")
    summary: str | None = None
    description: str | None = None
    get: Operation | None = None
    put: Operation | None = None
    post: Operation | None = None
    delete: Operation | None = None
    options: Operation | None = None
    head: Operation | None = None
    patch: Operation | None = None
    trace: Operation | None = None
    servers: list[Server] | None = None
    parameters: list[Parameter | Reference] | None = None

    model_config = ConfigDict(extra="allow")


class SecuritySchemeType(Enum):
    api_key = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    open_id_connect = "openIdConnect"


class SecurityBase(BaseModel):
    type_: SecuritySchemeType = Field(alias="type")
    description: str | None = None

    model_config = ConfigDict(extra="allow")


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
    scheme: str = "bearer"
    bearer_format: str | None = Field(None, alias="bearerFormat")


class OAuthFlow(BaseModel):
    refresh_url: str | None = Field(None, alias="refreshUrl")
    scopes: dict[str, str] = {}

    model_config = ConfigDict(extra="allow")


class OAuthFlowImplicit(OAuthFlow):
    authorization_url: str = Field(..., alias="authorizationUrl")


class OAuthFlowPassword(OAuthFlow):
    token_url: str = Field(..., alias="tokenUrl")


class OAuthFlowClientCredentials(OAuthFlow):
    token_url: str = Field(..., alias="tokenUrl")


class OAuthFlowAuthorizationCode(OAuthFlow):
    authorization_url: str = Field(..., alias="authorizationUrl")
    token_url: str = Field(..., alias="tokenUrl")


class OAuthFlows(BaseModel):
    implicit: OAuthFlowImplicit | None = None
    password: OAuthFlowPassword | None = None
    client_credentials: OAuthFlowClientCredentials | None = Field(
        None, alias="clientCredentials"
    )
    authorization_code: OAuthFlowAuthorizationCode | None = Field(
        None, alias="authorizationCode"
    )

    model_config = ConfigDict(extra="allow")


class OAuth2(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.oauth2, alias="type")
    flows: OAuthFlows


class OpenIdConnect(SecurityBase):
    type_: SecuritySchemeType = Field(SecuritySchemeType.open_id_connect, alias="type")
    open_id_connect_url: str = Field(..., alias="openIdConnectUrl")


SecurityScheme = APIKey | HTTPBase | OAuth2 | OpenIdConnect | HTTPBearer


class Components(BaseModel):
    schemas: dict[str, Schema | Reference] | None = None
    responses: dict[str, Response | Reference] | None = None
    parameters: dict[str, Parameter | Reference] | None = None
    examples: dict[str, Example | Reference] | None = None
    request_bodies: dict[str, RequestBody | Reference] | None = Field(
        default=None, alias="requestBodies"
    )
    headers: dict[str, Header | Reference] | None = None
    security_schemes: dict[str, SecurityScheme | Reference] | None = Field(
        default=None, alias="securitySchemes"
    )
    links: dict[str, Link | Reference] | None = None
    # Using Any for Specification Extensions
    callbacks: dict[str, dict[str, PathItem] | Reference | Any] | None = None

    model_config = ConfigDict(extra="allow")


class Tag(BaseModel):
    name: str
    description: str | None = None
    external_docs: ExternalDocumentation | None = Field(None, alias="externalDocs")

    model_config = ConfigDict(extra="allow")


class OpenAPI(BaseModel):
    openapi: str
    info: Info
    servers: list[Server] | None = None
    # Using Any for Specification Extensions
    paths: dict[str, PathItem | Any]
    components: Components | None = None
    security: list[dict[str, list[str]]] | None = None
    tags: list[Tag] | None = None
    external_docs: ExternalDocumentation | None = Field(
        default=None, alias="externalDocs"
    )

    model_config = ConfigDict(extra="allow")


Schema.model_rebuild()
Operation.model_rebuild()
Encoding.model_rebuild()
