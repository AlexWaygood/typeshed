from logging import Logger
from typing import Final

ASSERTION_TYPE: Final[str]
log: Logger

class JWTBearerClientAssertion:
    """Implementation of Using JWTs for Client Authentication, which is
    defined by RFC7523.
    """

    CLIENT_ASSERTION_TYPE: Final[str]
    CLIENT_AUTH_METHOD: Final[str]
    token_url: str
    leeway: int
    def __init__(self, token_url: str, validate_jti: bool = True, leeway: int = 60) -> None: ...
    def __call__(self, query_client, request): ...
    def create_claims_options(self):
        """Create a claims_options for verify JWT payload claims. Developers
        MAY overwrite this method to create a more strict options.
        """

    def process_assertion_claims(self, assertion, resolve_key):
        """Extract JWT payload claims from request "assertion", per
        `Section 3.1`_.

        :param assertion: assertion string value in the request
        :param resolve_key: function to resolve the sign key
        :return: JWTClaims
        :raise: InvalidClientError

        .. _`Section 3.1`: https://tools.ietf.org/html/rfc7523#section-3.1
        """

    def authenticate_client(self, client): ...
    def create_resolve_key_func(self, query_client, request): ...
    def validate_jti(self, claims, jti) -> None:
        """Validate if the given ``jti`` value is used before. Developers
        MUST implement this method::

            def validate_jti(self, claims, jti):
                key = "jti:{}-{}".format(claims["sub"], jti)
                if redis.get(key):
                    return False
                redis.set(key, 1, ex=3600)
                return True
        """

    def resolve_client_public_key(self, client, headers) -> None:
        """Resolve the client public key for verifying the JWT signature.
        A client may have many public keys, in this case, we can retrieve it
        via ``kid`` value in headers. Developers MUST implement this method::

            def resolve_client_public_key(self, client, headers):
                return client.public_key
        """
