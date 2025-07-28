"""The compat module provides various Python 2 / Python 3
compatibility functions

"""

from abc import ABCMeta
from collections.abc import ItemsView, Mapping, ValuesView
from io import StringIO as StringIO
from re import Pattern
from typing import Any, Final, SupportsIndex, TypeVar
from typing_extensions import TypeGuard
from urllib.parse import parse_qs, quote, unquote, urlencode as urlencode, urlparse as urlparse

_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)

url_quote = quote
url_unquote = unquote
url_parse_qs = parse_qs

PY2: Final = False
PY3: Final = True
RE_NUM: Final[Pattern[str]]
ON_LINUX: Final[bool]
ON_OSX: Final[bool]
ON_WINDOWS: Final[bool]

class AbstractBase(metaclass=ABCMeta): ...

SOCKET_ERROR = OSError
SOL_TCP: Final[int]
basestring: Final[tuple[type[str]]]
str_or_bytes: Final[tuple[type[str], type[bytes]]]
xrange = range
unicode_type = str

def time_now() -> float:
    """
    Python 3 supports monotonic time
    """

def dictkeys(dct: Mapping[_KT, Any]) -> list[_KT]:
    """
    Returns a list of keys of dictionary

    dict.keys returns a view that works like .keys in Python 2
    *except* any modifications in the dictionary will be visible
    (and will cause errors if the view is being iterated over while
    it is modified).
    """

def dictvalues(dct: Mapping[Any, _VT_co]) -> list[_VT_co]:
    """
    Returns a list of values of a dictionary

    dict.values returns a view that works like .values in Python 2
    *except* any modifications in the dictionary will be visible
    (and will cause errors if the view is being iterated over while
    it is modified).
    """

def dict_iteritems(dct: Mapping[_KT, _VT_co]) -> ItemsView[_KT, _VT_co]:
    """
    Returns an iterator of items (key/value pairs) of a dictionary

    dict.items returns a view that works like .items in Python 2
    *except* any modifications in the dictionary will be visible
    (and will cause errors if the view is being iterated over while
    it is modified).
    """

def dict_itervalues(dct: Mapping[Any, _VT_co]) -> ValuesView[_VT_co]:
    """
    :param dict dct:
    :returns: an iterator of the values of a dictionary
    :rtype: iterator
    """

def byte(*args: SupportsIndex) -> bytes:
    """
    This is the same as Python 2 `chr(n)` for bytes in Python 3

    Returns a single byte `bytes` for the given int argument (we
    optimize it a bit here by passing the positional argument tuple
    directly to the bytes constructor.
    """

class long(int):
    """
    A marker class that signifies that the integer value should be
    serialized as `l` instead of `I`
    """

def canonical_str(value: object) -> str:
    """
    Return the canonical str value for the string.
    In both Python 3 and Python 2 this is str.
    """

def is_integer(value: object) -> TypeGuard[int]:
    """
    Is value an integer?
    """

def as_bytes(value: str | bytes) -> bytes:
    """
    Returns value as bytes
    """

def to_digit(value: str) -> int:
    """
    Returns value as in integer
    """

def get_linux_version(release_str: str) -> tuple[int, int, int]:
    """
    Gets linux version
    """

HAVE_SIGNAL: Final[bool]
EINTR_IS_EXPOSED: Final = False
LINUX_VERSION: tuple[int, int, int] | None
