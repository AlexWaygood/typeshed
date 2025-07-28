from collections.abc import Container, Iterable, Mapping
from typing import Any

from .backends.base import Key

def sign(
    payload: bytes | Mapping[str, Any],
    # Internally it's passed down to jwk.construct(), which explicitly checks for
    # key as dict instance, instead of a Mapping
    key: str | bytes | dict[str, Any] | Key,
    headers: Mapping[str, Any] | None = None,
    algorithm: str = "HS256",
) -> str:
    """Signs a claims set and returns a JWS string.

    Args:
        payload (str or dict): A string to sign
        key (str or dict): The key to use for signing the claim set. Can be
            individual JWK or JWK set.
        headers (dict, optional): A set of headers that will be added to
            the default headers.  Any headers that are added as additional
            headers will override the default headers.
        algorithm (str, optional): The algorithm to use for signing the
            the claims.  Defaults to HS256.

    Returns:
        str: The string representation of the header, claims, and signature.

    Raises:
        JWSError: If there is an error signing the token.

    Examples:

        >>> jws.sign({'a': 'b'}, 'secret', algorithm='HS256')
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'

    """

def verify(
    token: str | bytes,
    key: str | bytes | Mapping[str, Any] | Key | Iterable[str],
    # Callers of this function, like jwt.decode(), and functions called internally,
    # like jws._verify_signature(), use and accept algorithms=None
    algorithms: str | Container[str] | None,
    verify: bool = True,
) -> bytes:
    """Verifies a JWS string's signature.

    Args:
        token (str): A signed JWS to be verified.
        key (str or dict): A key to attempt to verify the payload with. Can be
            individual JWK or JWK set.
        algorithms (str or list): Valid algorithms that should be used to verify the JWS.

    Returns:
        str: The str representation of the payload, assuming the signature is valid.

    Raises:
        JWSError: If there is an exception verifying a token.

    Examples:

        >>> token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        >>> jws.verify(token, 'secret', algorithms='HS256')

    """

def get_unverified_header(token: str | bytes) -> dict[str, Any]:
    """Returns the decoded headers without verification of any kind.

    Args:
        token (str): A signed JWS to decode the headers from.

    Returns:
        dict: The dict representation of the token headers.

    Raises:
        JWSError: If there is an exception decoding the token.
    """

def get_unverified_headers(token: str | bytes) -> dict[str, Any]:
    """Returns the decoded headers without verification of any kind.

    This is simply a wrapper of get_unverified_header() for backwards
    compatibility.

    Args:
        token (str): A signed JWS to decode the headers from.

    Returns:
        dict: The dict representation of the token headers.

    Raises:
        JWSError: If there is an exception decoding the token.
    """

def get_unverified_claims(token: str | bytes) -> bytes:
    """Returns the decoded claims without verification of any kind.

    Args:
        token (str): A signed JWS to decode the headers from.

    Returns:
        str: The str representation of the token claims.

    Raises:
        JWSError: If there is an exception decoding the token.
    """
