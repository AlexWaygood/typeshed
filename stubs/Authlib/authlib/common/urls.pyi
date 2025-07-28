"""authlib.util.urls.
~~~~~~~~~~~~~~~~~

Wrapper functions for URL encoding and decoding.
"""

from re import Pattern
from typing import Final
from typing_extensions import TypeAlias

always_safe: Final[str]
urlencoded: Final[set[str]]
INVALID_HEX_PATTERN: Final[Pattern[str]]

_ExplodedQueryString: TypeAlias = list[tuple[str, str]]

def url_encode(params: _ExplodedQueryString) -> str: ...
def url_decode(query: str) -> _ExplodedQueryString:
    """Decode a query string in x-www-form-urlencoded format into a sequence
    of two-element tuples.

    Unlike urlparse.parse_qsl(..., strict_parsing=True) urldecode will enforce
    correct formatting of the query string by validation. If validation fails
    a ValueError will be raised. urllib.parse_qsl will only raise errors if
    any of name-value pairs omits the equals sign.
    """

def add_params_to_qs(query: str, params: _ExplodedQueryString) -> str:
    """Extend a query with a list of two-tuples."""

def add_params_to_uri(uri: str, params: _ExplodedQueryString, fragment: bool = False):
    """Add a list of two-tuples to the uri query components."""

def quote(s: str, safe: bytes = b"/") -> str: ...
def unquote(s: str) -> str: ...
def quote_url(s: str) -> str: ...
def extract_params(raw: dict[str, str] | _ExplodedQueryString) -> _ExplodedQueryString:
    """Extract parameters and return them as a list of 2-tuples.

    Will successfully extract parameters from urlencoded query strings,
    dicts, or lists of 2-tuples. Empty strings/dicts/lists will return an
    empty list of parameters. Any other input will result in a return
    value of None.
    """

def is_valid_url(url: str, fragments_allowed: bool = True) -> bool: ...
