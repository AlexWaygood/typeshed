from collections.abc import Container, Iterable, Mapping, MutableMapping
from datetime import timezone
from typing import Any

from .backends.base import Key

UTC: timezone

def encode(
    claims: MutableMapping[str, Any],
    # Internally it calls jws.sign() that expects a key dict instance instead of Mapping
    key: str | bytes | dict[str, Any] | Key,
    algorithm: str = "HS256",
    headers: Mapping[str, Any] | None = None,
    access_token: str | None = None,
) -> str:
    """Encodes a claims set and returns a JWT string.

    JWTs are JWS signed objects with a few reserved claims.

    Args:
        claims (dict): A claims set to sign
        key (str or dict): The key to use for signing the claim set. Can be
            individual JWK or JWK set.
        algorithm (str, optional): The algorithm to use for signing the
            the claims.  Defaults to HS256.
        headers (dict, optional): A set of headers that will be added to
            the default headers.  Any headers that are added as additional
            headers will override the default headers.
        access_token (str, optional): If present, the 'at_hash' claim will
            be calculated and added to the claims present in the 'claims'
            parameter.

    Returns:
        str: The string representation of the header, claims, and signature.

    Raises:
        JWTError: If there is an error encoding the claims.

    Examples:

        >>> jwt.encode({'a': 'b'}, 'secret', algorithm='HS256')
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'

    """

def decode(
    token: str | bytes,
    key: str | bytes | Mapping[str, Any] | Key | Iterable[str],
    algorithms: str | Container[str] | None = None,
    options: Mapping[str, Any] | None = None,
    audience: str | None = None,
    issuer: str | Iterable[str] | None = None,
    subject: str | None = None,
    access_token: str | None = None,
) -> dict[str, Any]:
    """Verifies a JWT string's signature and validates reserved claims.

    Args:
        token (str): A signed JWS to be verified.
        key (str or iterable): A key to attempt to verify the payload with.
            This can be simple string with an individual key (e.g. "a1234"),
            a tuple or list of keys (e.g. ("a1234...", "b3579"),
            a JSON string, (e.g. '["a1234", "b3579"]'),
            a dict with the 'keys' key that gives a tuple or list of keys (e.g {'keys': [...]} ) or
            a dict or JSON string for a JWK set as defined by RFC 7517 (e.g.
                {'keys': [{'kty': 'oct', 'k': 'YTEyMzQ'}, {'kty': 'oct', 'k':'YjM1Nzk'}]} or
                '{"keys": [{"kty":"oct","k":"YTEyMzQ"},{"kty":"oct","k":"YjM1Nzk"}]}'
            ) in which case the keys must be base64 url safe encoded (with optional padding).
        algorithms (str or list): Valid algorithms that should be used to verify the JWS.
        audience (str): The intended audience of the token.  If the "aud" claim is
            included in the claim set, then the audience must be included and must equal
            the provided claim.
        issuer (str or iterable): Acceptable value(s) for the issuer of the token.
            If the "iss" claim is included in the claim set, then the issuer must be
            given and the claim in the token must be among the acceptable values.
        subject (str): The subject of the token.  If the "sub" claim is
            included in the claim set, then the subject must be included and must equal
            the provided claim.
        access_token (str): An access token string. If the "at_hash" claim is included in the
            claim set, then the access_token must be included, and it must match
            the "at_hash" claim.
        options (dict): A dictionary of options for skipping validation steps.

            defaults = {
                'verify_signature': True,
                'verify_aud': True,
                'verify_iat': True,
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iss': True,
                'verify_sub': True,
                'verify_jti': True,
                'verify_at_hash': True,
                'require_aud': False,
                'require_iat': False,
                'require_exp': False,
                'require_nbf': False,
                'require_iss': False,
                'require_sub': False,
                'require_jti': False,
                'require_at_hash': False,
                'leeway': 0,
            }

    Returns:
        dict: The dict representation of the claims set, assuming the signature is valid
            and all requested data validation passes.

    Raises:
        JWTError: If the signature is invalid in any way.
        ExpiredSignatureError: If the signature has expired.
        JWTClaimsError: If any claim is invalid in any way.

    Examples:

        >>> payload = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8'
        >>> jwt.decode(payload, 'secret', algorithms='HS256')

    """

def get_unverified_header(token: str | bytes) -> dict[str, Any]:
    """Returns the decoded headers without verification of any kind.

    Args:
        token (str): A signed JWT to decode the headers from.

    Returns:
        dict: The dict representation of the token headers.

    Raises:
        JWTError: If there is an exception decoding the token.
    """

def get_unverified_headers(token: str | bytes) -> dict[str, Any]:
    """Returns the decoded headers without verification of any kind.

    This is simply a wrapper of get_unverified_header() for backwards
    compatibility.

    Args:
        token (str): A signed JWT to decode the headers from.

    Returns:
        dict: The dict representation of the token headers.

    Raises:
        JWTError: If there is an exception decoding the token.
    """

def get_unverified_claims(token: str | bytes) -> dict[str, Any]:
    """Returns the decoded claims without verification of any kind.

    Args:
        token (str): A signed JWT to decode the headers from.

    Returns:
        dict: The dict representation of the token claims.

    Raises:
        JWTError: If there is an exception decoding the token.
    """
