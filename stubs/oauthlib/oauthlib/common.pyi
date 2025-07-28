"""
oauthlib.common
~~~~~~~~~~~~~~

This module provides data structures and utilities common
to all implementations of OAuth.
"""

import re
from _typeshed import Incomplete, SupportsLenAndGetItem
from collections.abc import Iterable, Mapping
from logging import Logger
from typing import Any, Final, Literal, TypeVar, overload
from typing_extensions import TypeAlias

_T = TypeVar("_T")
_V = TypeVar("_V")

_HTTPMethod: TypeAlias = Literal["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

UNICODE_ASCII_CHARACTER_SET: Final[str]
CLIENT_ID_CHARACTER_SET: Final[str]
SANITIZE_PATTERN: Final[re.Pattern[str]]
INVALID_HEX_PATTERN: Final[re.Pattern[str]]
always_safe: Final[str]
log: Logger

def quote(s: str | bytes, safe: bytes = b"/") -> str: ...
def unquote(s: str | bytes) -> str: ...
def urlencode(params: Iterable[tuple[str | bytes, str | bytes]]) -> str: ...
def encode_params_utf8(params: Iterable[tuple[str | bytes, str | bytes]]) -> list[tuple[bytes, bytes]]:
    """Ensures that all parameters in a list of 2-element tuples are encoded to
    bytestrings using UTF-8
    """

def decode_params_utf8(params: Iterable[tuple[str | bytes, str | bytes]]) -> list[tuple[str, str]]:
    """Ensures that all parameters in a list of 2-element tuples are decoded to
    unicode using UTF-8.
    """

urlencoded: Final[set[str]]

def urldecode(query: str | bytes) -> list[tuple[str, str]]:
    """Decode a query string in x-www-form-urlencoded format into a sequence
    of two-element tuples.

    Unlike urlparse.parse_qsl(..., strict_parsing=True) urldecode will enforce
    correct formatting of the query string by validation. If validation fails
    a ValueError will be raised. urllib.parse_qsl will only raise errors if
    any of name-value pairs omits the equals sign.
    """

def extract_params(raw: str | bytes | dict[str, str] | Iterable[tuple[str, str]]) -> list[tuple[str, str]] | None:
    """Extract parameters and return them as a list of 2-tuples.

    Will successfully extract parameters from urlencoded query strings,
    dicts, or lists of 2-tuples. Empty strings/dicts/lists will return an
    empty list of parameters. Any other input will result in a return
    value of None.
    """

def generate_nonce() -> str:
    """Generate pseudorandom nonce that is unlikely to repeat.

    Per `section 3.3`_ of the OAuth 1 RFC 5849 spec.
    Per `section 3.2.1`_ of the MAC Access Authentication spec.

    A random 64-bit number is appended to the epoch timestamp for both
    randomness and to decrease the likelihood of collisions.

    .. _`section 3.2.1`: https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01#section-3.2.1
    .. _`section 3.3`: https://tools.ietf.org/html/rfc5849#section-3.3
    """

def generate_timestamp() -> str:
    """Get seconds since epoch (UTC).

    Per `section 3.3`_ of the OAuth 1 RFC 5849 spec.
    Per `section 3.2.1`_ of the MAC Access Authentication spec.

    .. _`section 3.2.1`: https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-01#section-3.2.1
    .. _`section 3.3`: https://tools.ietf.org/html/rfc5849#section-3.3
    """

def generate_token(length: int = 30, chars: SupportsLenAndGetItem[str] = ...) -> str:
    """Generates a non-guessable OAuth token

    OAuth (1 and 2) does not specify the format of tokens except that they
    should be strings of random characters. Tokens should not be guessable
    and entropy when generating the random characters is important. Which is
    why SystemRandom is used instead of the default random.choice method.
    """

def generate_signed_token(private_pem: str, request: Request) -> str: ...
def verify_signed_token(public_pem, token): ...
def generate_client_id(length: int = 30, chars: SupportsLenAndGetItem[str] = ...) -> str:
    """Generates an OAuth client_id

    OAuth 2 specify the format of client_id in
    https://tools.ietf.org/html/rfc6749#appendix-A.
    """

def add_params_to_qs(query: str, params: dict[str, str] | Iterable[tuple[str, str]]) -> str:
    """Extend a query with a list of two-tuples."""

def add_params_to_uri(uri: str, params: dict[str, str] | Iterable[tuple[str, str]], fragment: bool = False) -> str:
    """Add a list of two-tuples to the uri query components."""

def safe_string_equals(a: str, b: str) -> bool:
    """Near-constant time string comparison.

    Used in order to avoid timing attacks on sensitive information such
    as secret keys during request verification (`rootLabs`_).

    .. _`rootLabs`: http://rdist.root.org/2010/01/07/timing-independent-array-comparison/

    """

@overload
def to_unicode(data: str | bytes, encoding: str = "UTF-8") -> str:
    """Convert a number of different types of objects to unicode."""

@overload
def to_unicode(data: Mapping[str, _V] | Mapping[bytes, _V], encoding: str = "UTF-8") -> dict[str, _V]: ...
@overload
def to_unicode(data: _T, encoding: str = "UTF-8") -> _T: ...

class CaseInsensitiveDict(dict[str, Incomplete]):
    """Basic case insensitive dict with strings only keys."""

    proxy: dict[str, str]
    def __init__(self, data: dict[str, Incomplete]) -> None: ...
    @overload
    def __contains__(self, k: str) -> bool: ...
    @overload
    def __contains__(self, k: object) -> bool: ...
    def __delitem__(self, k: str) -> None: ...
    def __getitem__(self, k: str): ...
    @overload
    def get(self, k: str, default: None = None) -> Incomplete | None: ...
    @overload
    def get(self, k: str, default): ...
    def __setitem__(self, k: str, v) -> None: ...
    def update(self, *args, **kwargs) -> None: ...

class Request:
    """A malleable representation of a signable HTTP request.

    Body argument may contain any data, but parameters will only be decoded if
    they are one of:

    * urlencoded query string
    * dict
    * list of 2-tuples

    Anything else will be treated as raw body data to be passed through
    unmolested.
    """

    uri: str
    http_method: _HTTPMethod
    headers: CaseInsensitiveDict
    body: str | dict[str, str] | list[tuple[str, str]] | None
    decoded_body: list[tuple[str, str]] | None
    oauth_params: list[str]
    validator_log: dict[str, Any]  # value type depends on the key
    def __init__(
        self,
        uri: str,
        http_method: _HTTPMethod = "GET",
        body: str | dict[str, str] | list[tuple[str, str]] | None = None,
        headers: Mapping[str, str] | None = None,
        encoding: str = "utf-8",
    ): ...
    def __getattr__(self, name: str) -> str | None: ...  # or raises AttributeError if attribute is not found
    @property
    def uri_query(self) -> str: ...
    @property
    def uri_query_params(self) -> list[tuple[str, str]]: ...
    @property
    def duplicate_params(self) -> list[str]: ...
