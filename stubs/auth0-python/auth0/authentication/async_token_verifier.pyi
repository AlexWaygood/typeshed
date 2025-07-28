"""Token Verifier module"""

from _typeshed import Incomplete

from .token_verifier import AsymmetricSignatureVerifier, JwksFetcher, TokenVerifier

class AsyncAsymmetricSignatureVerifier(AsymmetricSignatureVerifier):
    """Async verifier for RSA signatures, which rely on public key certificates.

    Args:
        jwks_url (str): The url where the JWK set is located.
        algorithm (str, optional): The expected signing algorithm. Defaults to "RS256".
    """

    def __init__(self, jwks_url: str, algorithm: str = "RS256") -> None: ...
    def set_session(self, session) -> None:
        """Set Client Session to improve performance by reusing session.

        Args:
            session (aiohttp.ClientSession): The client session which should be closed
                manually or within context manager.
        """

class AsyncJwksFetcher(JwksFetcher):
    """Class that async fetches and holds a JSON web key set.
    This class makes use of an in-memory cache. For it to work properly, define this instance once and re-use it.

    Args:
        jwks_url (str): The url where the JWK set is located.
        cache_ttl (str, optional): The lifetime of the JWK set cache in seconds. Defaults to 600 seconds.
    """

    def __init__(self, *args, **kwargs) -> None: ...
    def set_session(self, session) -> None:
        """Set Client Session to improve performance by reusing session.

        Args:
            session (aiohttp.ClientSession): The client session which should be closed
                manually or within context manager.
        """

    async def get_key(self, key_id: str):
        """Obtains the JWK associated with the given key id.

        Args:
            key_id (str): The id of the key to fetch.

        Returns:
            the JWK associated with the given key id.

        Raises:
            TokenValidationError: when a key with that id cannot be found
        """

class AsyncTokenVerifier(TokenVerifier):
    """Class that verifies ID tokens following the steps defined in the OpenID Connect spec.
    An OpenID Connect ID token is not meant to be consumed until it's verified.

    Args:
        signature_verifier (AsyncAsymmetricSignatureVerifier): The instance that knows how to verify the signature.
        issuer (str): The expected issuer claim value.
        audience (str): The expected audience claim value.
        leeway (int, optional): The clock skew to accept when verifying date related claims in seconds.
        Defaults to 60 seconds.
    """

    iss: str
    aud: str
    leeway: int
    def __init__(
        self, signature_verifier: AsyncAsymmetricSignatureVerifier, issuer: str, audience: str, leeway: int = 0
    ) -> None: ...
    def set_session(self, session) -> None:
        """Set Client Session to improve performance by reusing session.

        Args:
            session (aiohttp.ClientSession): The client session which should be closed
                manually or within context manager.
        """

    async def verify(  # type: ignore[override] # Differs from supertype
        self, token: str, nonce: str | None = None, max_age: int | None = None, organization: str | None = None
    ) -> dict[str, Incomplete]:
        """Attempts to verify the given ID token, following the steps defined in the OpenID Connect spec.

        Args:
            token (str): The JWT to verify.
            nonce (str, optional): The nonce value sent during authentication.
            max_age (int, optional): The max_age value sent during authentication.
            organization (str, optional): The expected organization ID (org_id) or organization name (org_name) claim value. This should be specified
            when logging in to an organization.

        Returns:
            the decoded payload from the token

        Raises:
            TokenValidationError: when the token cannot be decoded, the token signing algorithm is not the expected one,
            the token signature is invalid or the token has a claim missing or with unexpected value.
        """
