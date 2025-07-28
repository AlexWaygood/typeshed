from _typeshed import Incomplete

from authlib.oauth2.rfc7009 import RevocationEndpoint

class JWTRevocationEndpoint(RevocationEndpoint):
    """JWTRevocationEndpoint inherits from `RFC7009`_
    :class:`~authlib.oauth2.rfc7009.RevocationEndpoint`.

    The JWT access tokens cannot be revoked.
    If the submitted token is a JWT access token, then revocation returns
    a `invalid_token_error`.

    :param issuer: The issuer identifier.

    :param \\\\*\\\\*kwargs: Other parameters are inherited from
        :class:`~authlib.oauth2.rfc7009.RevocationEndpoint`.

    Plain text access tokens and other kind of tokens such as refresh_tokens
    will be ignored by this endpoint and passed to the next revocation endpoint::

        class MyJWTAccessTokenRevocationEndpoint(JWTRevocationEndpoint):
            def get_jwks(self): ...


        # endpoint dedicated to JWT access token revokation
        authorization_server.register_endpoint(
            MyJWTAccessTokenRevocationEndpoint(
                issuer="https://authorization-server.example.org",
            )
        )

        # another endpoint dedicated to refresh token revokation
        authorization_server.register_endpoint(MyRefreshTokenRevocationEndpoint)

    .. _RFC7009: https://tools.ietf.org/html/rfc7009
    """

    issuer: Incomplete
    def __init__(self, issuer, server=None, *args, **kwargs) -> None: ...
    def authenticate_token(self, request, client) -> None:
        """ """

    def get_jwks(self) -> None:
        """Return the JWKs that will be used to check the JWT access token signature.
        Developers MUST re-implement this method::

            def get_jwks(self):
                return load_jwks("jwks.json")
        """
