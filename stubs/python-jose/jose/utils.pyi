from collections.abc import Callable, Iterable
from datetime import timedelta
from hashlib import _Hash
from typing import Any

def long_to_bytes(n: int, blocksize: int | None = 0) -> bytes: ...
def long_to_base64(data: int, size: int | None = 0) -> bytes: ...
def int_arr_to_long(arr: Iterable[Any]) -> int: ...
def base64_to_long(data: str | bytes) -> int: ...
def calculate_at_hash(access_token: str, hash_alg: Callable[[bytes], _Hash]) -> str:
    """Helper method for calculating an access token
    hash, as described in http://openid.net/specs/openid-connect-core-1_0.html#CodeIDToken

    Its value is the base64url encoding of the left-most half of the hash of the octets
    of the ASCII representation of the access_token value, where the hash algorithm
    used is the hash algorithm used in the alg Header Parameter of the ID Token's JOSE
    Header. For instance, if the alg is RS256, hash the access_token value with SHA-256,
    then take the left-most 128 bits and base64url encode them. The at_hash value is a
    case sensitive string.

    Args:
        access_token (str): An access token string.
        hash_alg (callable): A callable returning a hash object, e.g. hashlib.sha256

    """

def base64url_decode(input: bytes) -> bytes:
    """Helper method to base64url_decode a string.

    Args:
        input (bytes): A base64url_encoded string (bytes) to decode.

    """

def base64url_encode(input: bytes) -> bytes:
    """Helper method to base64url_encode a string.

    Args:
        input (bytes): A base64url_encoded string (bytes) to encode.

    """

def timedelta_total_seconds(delta: timedelta) -> int:
    """Helper method to determine the total number of seconds
    from a timedelta.

    Args:
        delta (timedelta): A timedelta to convert to seconds.
    """

def ensure_binary(s: str | bytes) -> bytes:
    """Coerce **s** to bytes."""

def is_pem_format(key: bytes) -> bool: ...
def is_ssh_key(key: bytes) -> bool: ...
