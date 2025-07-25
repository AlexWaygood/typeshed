from _typeshed import Incomplete

from authlib.oauth2.rfc7662 import IntrospectionEndpoint

class JWTIntrospectionEndpoint(IntrospectionEndpoint):
    """JWTIntrospectionEndpoint inherits from :ref:`specs/rfc7662`
    :class:`~authlib.oauth2.rfc7662.IntrospectionEndpoint` and implements the machinery
    to automatically process the JWT access tokens.

    :param issuer: The issuer identifier for which tokens will be introspected.

    :param \\\\*\\\\*kwargs: Other parameters are inherited from
        :class:`~authlib.oauth2.rfc7662.introspection.IntrospectionEndpoint`.

    ::

        class MyJWTAccessTokenIntrospectionEndpoint(JWTIntrospectionEndpoint):
            def get_jwks(self): ...

            def get_username(self, user_id): ...


        # endpoint dedicated to JWT access token introspection
        authorization_server.register_endpoint(
            MyJWTAccessTokenIntrospectionEndpoint(
                issuer="https://authorization-server.example.org",
            )
        )

        # another endpoint dedicated to refresh token introspection
        authorization_server.register_endpoint(MyRefreshTokenIntrospectionEndpoint)

    """

    ENDPOINT_NAME: str
    issuer: Incomplete
    def __init__(self, issuer, server=None, *args, **kwargs) -> None: ...
    def create_endpoint_response(self, request):
        """ """

    def authenticate_token(self, request, client):
        """ """

    def create_introspection_payload(self, token): ...
    def get_jwks(self) -> None:
        """Return the JWKs that will be used to check the JWT access token signature.
        Developers MUST re-implement this method::

            def get_jwks(self):
                return load_jwks("jwks.json")
        """

    def get_username(self, user_id: str) -> str:
        """Returns an username from a user ID.
        Developers MAY re-implement this method::

            def get_username(self, user_id):
                return User.get(id=user_id).username
        """
