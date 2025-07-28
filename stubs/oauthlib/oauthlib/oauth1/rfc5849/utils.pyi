"""
oauthlib.utils
~~~~~~~~~~~~~~

This module contains utility methods used by various parts of the OAuth
spec.
"""

from collections.abc import Callable, Iterable
from typing import Any, Final, TypeVar

_T = TypeVar("_T")

UNICODE_ASCII_CHARACTER_SET: Final[str]

def filter_params(
    target: Callable[[dict[str, Any] | Iterable[tuple[str, Any]], _T], object],
) -> Callable[[list[str], _T], object]:
    """Decorator which filters params to remove non-oauth_* parameters

    Assumes the decorated method takes a params dict or list of tuples as its
    first argument.
    """

def filter_oauth_params(params: dict[str, Any] | Iterable[tuple[str, Any]]) -> list[str]:  # we don't care about second (Any) part
    """Removes all non oauth parameters from a dict or a list of params."""

def escape(u: str) -> str:
    """Escape a unicode string in an OAuth-compatible fashion.

    Per `section 3.6`_ of the spec.

    .. _`section 3.6`: https://tools.ietf.org/html/rfc5849#section-3.6

    """

def unescape(u: str) -> str: ...
def parse_keqv_list(l: list[str]) -> dict[str, str]:
    """A unicode-safe version of urllib2.parse_keqv_list"""

def parse_http_list(u: str) -> list[str]:
    """A unicode-safe version of urllib2.parse_http_list"""

def parse_authorization_header(authorization_header: str) -> list[tuple[str, str]]:
    """Parse an OAuth authorization header into a list of 2-tuples"""
