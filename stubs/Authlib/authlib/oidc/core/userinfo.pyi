from authlib.oauth2.rfc6749.authorization_server import AuthorizationServer
from authlib.oauth2.rfc6749.requests import OAuth2Request
from authlib.oauth2.rfc6749.resource_protector import ResourceProtector

from .claims import UserInfo

class UserInfoEndpoint:
    """OpenID Connect Core UserInfo Endpoint.

    This endpoint returns information about a given user, as a JSON payload or as a JWT.
    It must be subclassed and a few methods needs to be manually implemented::

        class UserInfoEndpoint(oidc.core.UserInfoEndpoint):
            def get_issuer(self):
                return "https://auth.example"

            def generate_user_info(self, user, scope):
                return UserInfo(
                    sub=user.id,
                    name=user.name,
                    ...
                ).filter(scope)

            def resolve_private_key(self):
                return server_private_jwk_set()

    It is also needed to pass a :class:`~authlib.oauth2.rfc6749.ResourceProtector` instance
    with a registered :class:`~authlib.oauth2.rfc6749.TokenValidator` at initialization,
    so the access to the endpoint can be restricter to valid token bearers::

        resource_protector = ResourceProtector()
        resource_protector.register_token_validator(BearerTokenValidator())
        server.register_endpoint(
            UserInfoEndpoint(resource_protector=resource_protector)
        )

    And then you can plug the endpoint to your application::

        @app.route("/oauth/userinfo", methods=["GET", "POST"])
        def userinfo():
            return server.create_endpoint_response("userinfo")

    """

    ENDPOINT_NAME: str
    server: AuthorizationServer | None
    resource_protector: ResourceProtector | None
    def __init__(
        self, server: AuthorizationServer | None = None, resource_protector: ResourceProtector | None = None
    ) -> None: ...
    def create_endpoint_request(self, request: OAuth2Request): ...
    def __call__(self, request: OAuth2Request) -> tuple[int, dict[str, str | None], list[tuple[str, str]]]: ...
    def generate_user_info(self, user, scope: str) -> UserInfo:
        """
        Generate a :class:`~authlib.oidc.core.UserInfo` object for an user::

            def generate_user_info(self, user, scope: str) -> UserInfo:
                return UserInfo(
                    given_name=user.given_name,
                    family_name=user.last_name,
                    email=user.email,
                    ...
                ).filter(scope)

        This method must be implemented by developers.
        """

    def get_issuer(self) -> str:
        """The OP's Issuer Identifier URL.

        The value is used to fill the ``iss`` claim that is mandatory in signed userinfo::

            def get_issuer(self) -> str:
                return "https://auth.example"

        This method must be implemented by developers to support JWT userinfo.
        """

    def resolve_private_key(self):
        """Return the server JSON Web Key Set.

        This is used to sign userinfo payloads::

            def resolve_private_key(self):
                return server_private_jwk_set()

        This method must be implemented by developers to support JWT userinfo signing.
        """
