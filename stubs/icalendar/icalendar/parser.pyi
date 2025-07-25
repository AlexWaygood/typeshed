"""This module parses and generates contentlines as defined in RFC 5545
(iCalendar), but will probably work for other MIME types with similar syntax.
Eg. RFC 2426 (vCard)

It is stupid in the sense that it treats the content purely as strings. No type
conversion is attempted.
"""

from _collections_abc import dict_keys
from _typeshed import Incomplete
from collections.abc import Iterable
from re import Pattern
from typing import AnyStr, ClassVar, Final, overload
from typing_extensions import Self

from .caselessdict import CaselessDict
from .parser_tools import ICAL_TYPE

__all__ = [
    "Contentline",
    "Contentlines",
    "FOLD",
    "NAME",
    "NEWLINE",
    "Parameters",
    "QUNSAFE_CHAR",
    "QUOTABLE",
    "UNSAFE_CHAR",
    "dquote",
    "escape_char",
    "escape_string",
    "foldline",
    "param_value",
    "q_join",
    "q_split",
    "rfc_6868_escape",
    "rfc_6868_unescape",
    "uFOLD",
    "unescape_char",
    "unescape_list_or_string",
    "unescape_string",
    "validate_param_value",
    "validate_token",
]

def escape_char(text: str) -> str:
    """Format value according to iCalendar TEXT escaping rules."""

def unescape_char(text: AnyStr) -> AnyStr: ...
def foldline(line: str, limit: int = 75, fold_sep: str = "\r\n ") -> str:
    """Make a string folded as defined in RFC5545
    Lines of text SHOULD NOT be longer than 75 octets, excluding the line
    break.  Long content lines SHOULD be split into a multiple line
    representations using a line "folding" technique.  That is, a long
    line can be split between any two characters by inserting a CRLF
    immediately followed by a single linear white-space character (i.e.,
    SPACE or HTAB).
    """

def param_value(value: str | list[str] | tuple[str, ...] | Incomplete, always_quote: bool = False) -> str:
    """Returns a parameter value."""

NAME: Final[Pattern[str]]
UNSAFE_CHAR: Final[Pattern[str]]
QUNSAFE_CHAR: Final[Pattern[str]]
FOLD: Final[Pattern[bytes]]
uFOLD: Final[Pattern[str]]
NEWLINE: Final[Pattern[str]]

def validate_token(name: str) -> None: ...
def validate_param_value(value: str, quoted: bool = True) -> None: ...

QUOTABLE: Final[Pattern[str]]

def dquote(val: str, always_quote: bool = False) -> str:
    """Enclose parameter values containing [,;:] in double quotes."""

def q_split(st: str, sep: str = ",", maxsplit: int = -1) -> list[str]:
    """Splits a string on char, taking double (q)uotes into considderation."""

def q_join(lst: Iterable[str], sep: str = ",", always_quote: bool = False) -> str:
    """Joins a list on sep, quoting strings with QUOTABLE chars."""

class Parameters(CaselessDict[str]):
    """Parser and generator of Property parameter strings. It knows nothing of
    datatypes. Its main concern is textual structure.
    """

    always_quoted: ClassVar[tuple[str, ...]]
    quote_also: ClassVar[dict[str, str]]
    def params(self) -> dict_keys[str, str]:
        """In RFC 5545 keys are called parameters, so this is to be consitent
        with the naming conventions.
        """

    def to_ical(self, sorted: bool = True) -> bytes: ...
    @classmethod
    def from_ical(cls, st: str, strict: bool = False) -> Self:
        """Parses the parameter format from ical text format."""

def escape_string(val: str) -> str: ...
def unescape_string(val: str) -> str: ...

RFC_6868_UNESCAPE_REGEX: Final[Pattern[str]]

def rfc_6868_unescape(param_value: str) -> str:
    """Take care of :rfc:`6868` unescaping.

    - ^^ -> ^
    - ^n -> system specific newline
    - ^' -> "
    - ^ with others stay intact
    """

RFC_6868_ESCAPE_REGEX: Final[Pattern[str]]

def rfc_6868_escape(param_value: str) -> str:
    """Take care of :rfc:`6868` escaping.

    - ^ -> ^^
    - " -> ^'
    - newline -> ^n
    """

@overload
def unescape_list_or_string(val: list[str]) -> list[str]: ...
@overload
def unescape_list_or_string(val: str) -> str: ...

class Contentline(str):
    """A content line is basically a string that can be folded and parsed into
    parts.
    """

    strict: bool
    def __new__(cls, value: str | bytes, strict: bool = False, encoding: str = ...) -> Self: ...
    @classmethod
    def from_parts(cls, name: ICAL_TYPE, params: Parameters, values, sorted: bool = True) -> Self:
        """Turn a parts into a content line."""

    def parts(self) -> tuple[str, Parameters, str]:
        """Split the content line up into (name, parameters, values) parts."""

    @classmethod
    def from_ical(cls, ical: str | bytes, strict: bool = False) -> Self:
        """Unfold the content lines in an iCalendar into long content lines."""

    def to_ical(self) -> bytes:
        """Long content lines are folded so they are less than 75 characters
        wide.
        """

class Contentlines(list[Contentline]):
    """I assume that iCalendar files generally are a few kilobytes in size.
    Then this should be efficient. for Huge files, an iterator should probably
    be used instead.
    """

    def to_ical(self) -> bytes:
        """Simply join self."""

    @classmethod
    def from_ical(cls, st: str | bytes) -> Self:
        """Parses a string into content lines."""
