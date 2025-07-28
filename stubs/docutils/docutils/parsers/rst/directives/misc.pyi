"""Miscellaneous directives."""

from _typeshed import StrPath
from pathlib import Path
from re import Match, Pattern
from typing import ClassVar, Final

from docutils.parsers.rst import Directive
from docutils.parsers.rst.states import SpecializedBody

__docformat__: Final = "reStructuredText"

def adapt_path(path: str, source: StrPath = "", root_prefix: StrPath = "/") -> str: ...

class Include(Directive):
    """
    Include content read from a separate source file.

    Content may be parsed by the parser, or included as a literal
    block.  The encoding of the included file can be specified.  Only
    a part of the given file argument may be included by specifying
    start and end line or text to match before and/or after the text
    to be used.

    https://docutils.sourceforge.io/docs/ref/rst/directives.html#including-an-external-document-fragment
    """

    standard_include_path: Path

class Raw(Directive):
    """
    Pass through content unchanged

    Content is included in output based on type argument

    Content may be included inline (content section of directive) or
    imported from a file or url.
    """

class Replace(Directive): ...

class Unicode(Directive):
    """
    Convert Unicode character codes (numbers) to characters.  Codes may be
    decimal numbers, hexadecimal numbers (prefixed by ``0x``, ``x``, ``\\x``,
    ``U+``, ``u``, or ``\\u``; e.g. ``U+262E``), or XML-style numeric character
    entities (e.g. ``&#x262E;``).  Text following ".." is a comment and is
    ignored.  Spaces are ignored, and any other text remains as-is.
    """

    comment_pattern: Pattern[str]

class Class(Directive):
    """
    Set a "class" attribute on the directive content or the next element.
    When applied to the next element, a "pending" element is inserted, and a
    transform does the work later.
    """

class Role(Directive):
    argument_pattern: Pattern[str]

class DefaultRole(Directive):
    """Set the default interpreted text role."""

class Title(Directive): ...

class MetaBody(SpecializedBody):
    def field_marker(  # type: ignore[override]
        self, match: Match[str], context: list[str], next_state: str | None
    ) -> tuple[list[str], str | None, list[str]]:
        """Meta element."""

    def parsemeta(self, match: Match[str]): ...

class Meta(Directive):
    SMkwargs: ClassVar[dict[str, tuple[MetaBody]]]

class Date(Directive): ...

class TestDirective(Directive):
    """This directive is useful only for testing purposes."""
