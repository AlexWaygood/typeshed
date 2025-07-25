from collections.abc import Callable, Collection, Mapping
from typing import overload
from typing_extensions import TypeAlias, deprecated

from authlib.oauth2 import JsonRequest, OAuth2Error, OAuth2Request
from authlib.oauth2.rfc6749 import BaseGrant, ClientMixin
from authlib.oauth2.rfc6750 import BearerTokenGenerator

from .hooks import Hookable

_ServerResponse: TypeAlias = tuple[int, str, list[tuple[str, str]]]

class AuthorizationServer(Hookable):
    """Authorization server that handles Authorization Endpoint and Token
    Endpoint.

    :param scopes_supported: A list of supported scopes by this authorization server.
    """

    scopes_supported: Collection[str] | None
    def __init__(self, scopes_supported: Collection[str] | None = None) -> None: ...
    def query_client(self, client_id: str) -> ClientMixin:
        """Query OAuth client by client_id. The client model class MUST
        implement the methods described by
        :class:`~authlib.oauth2.rfc6749.ClientMixin`.
        """

    def save_token(self, token: dict[str, str | int], request: OAuth2Request) -> None:
        """Define function to save the generated token into database."""

    def generate_token(
        self,
        grant_type: str,
        client: ClientMixin,
        user=None,
        scope: str | None = None,
        expires_in: int | None = None,
        include_refresh_token: bool = True,
    ) -> dict[str, str | int]:
        """Generate the token dict.

        :param grant_type: current requested grant_type.
        :param client: the client that making the request.
        :param user: current authorized user.
        :param expires_in: if provided, use this value as expires_in.
        :param scope: current requested scope.
        :param include_refresh_token: should refresh_token be included.
        :return: Token dict
        """

    def register_token_generator(self, grant_type: str, func: BearerTokenGenerator) -> None:
        """Register a function as token generator for the given ``grant_type``.
        Developers MUST register a default token generator with a special
        ``grant_type=default``::

            def generate_bearer_token(
                grant_type,
                client,
                user=None,
                scope=None,
                expires_in=None,
                include_refresh_token=True,
            ):
                token = {"token_type": "Bearer", "access_token": ...}
                if include_refresh_token:
                    token["refresh_token"] = ...
                ...
                return token


            authorization_server.register_token_generator(
                "default", generate_bearer_token
            )

        If you register a generator for a certain grant type, that generator will only works
        for the given grant type::

            authorization_server.register_token_generator(
                "client_credentials",
                generate_bearer_token,
            )

        :param grant_type: string name of the grant type
        :param func: a function to generate token
        """

    def authenticate_client(self, request: OAuth2Request, methods: Collection[str], endpoint: str = "token") -> ClientMixin:
        """Authenticate client via HTTP request information with the given
        methods, such as ``client_secret_basic``, ``client_secret_post``.
        """

    def register_client_auth_method(self, method, func) -> None:
        """Add more client auth method. The default methods are:

        * none: The client is a public client and does not have a client secret
        * client_secret_post: The client uses the HTTP POST parameters
        * client_secret_basic: The client uses HTTP Basic

        :param method: Name of the Auth method
        :param func: Function to authenticate the client

        The auth method accept two parameters: ``query_client`` and ``request``,
        an example for this method::

            def authenticate_client_via_custom(query_client, request):
                client_id = request.headers["X-Client-Id"]
                client = query_client(client_id)
                do_some_validation(client)
                return client


            authorization_server.register_client_auth_method(
                "custom", authenticate_client_via_custom
            )
        """

    def register_extension(self, extension) -> None: ...
    def get_error_uri(self, request, error) -> None:
        """Return a URI for the given error, framework may implement this method."""

    def send_signal(self, name, *args: object, **kwargs: object) -> None:
        """Framework integration can re-implement this method to support
        signal system.
        """

    def create_oauth2_request(self, request) -> OAuth2Request:
        """This method MUST be implemented in framework integrations. It is
        used to create an OAuth2Request instance.

        :param request: the "request" instance in framework
        :return: OAuth2Request instance
        """

    def create_json_request(self, request) -> JsonRequest:
        """This method MUST be implemented in framework integrations. It is
        used to create an HttpRequest instance.

        :param request: the "request" instance in framework
        :return: HttpRequest instance
        """

    def handle_response(self, status: int, body: Mapping[str, object], headers: Mapping[str, str]) -> object:
        """Return HTTP response. Framework MUST implement this function."""

    def validate_requested_scope(self, scope: str) -> None:
        """Validate if requested scope is supported by Authorization Server.
        Developers CAN re-write this method to meet your needs.
        """

    def register_grant(
        self, grant_cls: type[BaseGrant], extensions: Collection[Callable[[BaseGrant], None]] | None = None
    ) -> None:
        """Register a grant class into the endpoint registry. Developers
        can implement the grants in ``authlib.oauth2.rfc6749.grants`` and
        register with this method::

            class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
                def authenticate_user(self, credential):
                    # ...

            authorization_server.register_grant(AuthorizationCodeGrant)

        :param grant_cls: a grant class.
        :param extensions: extensions for the grant class.
        """

    def register_endpoint(self, endpoint) -> None:
        """Add extra endpoint to authorization server. e.g.
        RevocationEndpoint::

            authorization_server.register_endpoint(RevocationEndpoint)

        :param endpoint_cls: A endpoint class or instance.
        """

    def get_authorization_grant(self, request: OAuth2Request) -> BaseGrant: ...
    def get_consent_grant(self, request=None, end_user=None):
        """Validate current HTTP request for authorization page. This page
        is designed for resource owner to grant or deny the authorization.
        """

    def get_token_grant(self, request: OAuth2Request) -> BaseGrant:
        """Find the token grant for current request.

        :param request: OAuth2Request instance.
        :return: grant instance
        """

    def create_endpoint_response(self, name, request=None):
        """Validate endpoint request and create endpoint response.

        :param name: Endpoint name
        :param request: HTTP request instance.
        :return: Response
        """

    @overload
    @deprecated("The 'grant' parameter will become mandatory.")
    def create_authorization_response(self, request=None, grant_user=None) -> object: ...
    @overload
    def create_authorization_response(self, request=None, grant_user=None, grant=None) -> object: ...
    def create_token_response(self, request=None) -> _ServerResponse:
        """Validate token request and create token response.

        :param request: HTTP request instance
        """

    def handle_error_response(self, request: OAuth2Request, error: OAuth2Error) -> object: ...
