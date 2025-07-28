"""Token Verifier module"""

from _typeshed import Incomplete
from typing import ClassVar

class SignatureVerifier:
    """Abstract class that will verify a given JSON web token's signature
    using the key fetched internally given its key id.

    Args:
        algorithm (str): The expected signing algorithm (e.g. RS256).
    """

    DISABLE_JWT_CHECKS: ClassVar[dict[str, bool]]
    def __init__(self, algorithm: str) -> None: ...
    async def verify_signature(self, token: str) -> dict[str, Incomplete]:
        """Verifies the signature of the given JSON web token.

        Args:
            token (str): The JWT to get its signature verified.

        Raises:
            TokenValidationError: if the token cannot be decoded, the algorithm is invalid
            or the token's signature doesn't match the calculated one.
        """

class SymmetricSignatureVerifier(SignatureVerifier):
    """Verifier for HMAC signatures, which rely on shared secrets.

    Args:
        shared_secret (str): The shared secret used to decode the token.
        algorithm (str, optional): The expected signing algorithm. Defaults to "HS256".
    """

    def __init__(self, shared_secret: str, algorithm: str = "HS256") -> None: ...

class JwksFetcher:
    """Class that fetches and holds a JSON web key set.
    This class makes use of an in-memory cache. For it to work properly, define this instance once and re-use it.

    Args:
        jwks_url (str): The url where the JWK set is located.
        cache_ttl (str, optional): The lifetime of the JWK set cache in seconds. Defaults to 600 seconds.
    """

    CACHE_TTL: ClassVar[int]
    def __init__(self, jwks_url: str, cache_ttl: int = ...) -> None: ...
    def get_key(self, key_id: str):
        """Obtains the JWK associated with the given key id.

        Args:
            key_id (str): The id of the key to fetch.

        Returns:
            the JWK associated with the given key id.

        Raises:
            TokenValidationError: when a key with that id cannot be found
        """

class AsymmetricSignatureVerifier(SignatureVerifier):
    """Verifier for RSA signatures, which rely on public key certificates.

    Args:
        jwks_url (str): The url where the JWK set is located.
        algorithm (str, optional): The expected signing algorithm. Defaults to "RS256".
        cache_ttl (int, optional): The lifetime of the JWK set cache in seconds. Defaults to 600 seconds.
    """

    def __init__(self, jwks_url: str, algorithm: str = "RS256", cache_ttl: int = ...) -> None: ...

class TokenVerifier:
    """Class that verifies ID tokens following the steps defined in the OpenID Connect spec.
    An OpenID Connect ID token is not meant to be consumed until it's verified.

    Args:
        signature_verifier (SignatureVerifier): The instance that knows how to verify the signature.
        issuer (str): The expected issuer claim value.
        audience (str): The expected audience claim value.
        leeway (int, optional): The clock skew to accept when verifying date related claims in seconds.
        Defaults to 60 seconds.
    """

    iss: str
    aud: str
    leeway: int
    def __init__(self, signature_verifier: SignatureVerifier, issuer: str, audience: str, leeway: int = 0) -> None: ...
    def verify(
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
