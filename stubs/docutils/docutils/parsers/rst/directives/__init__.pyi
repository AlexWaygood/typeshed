"""
This package contains directive implementation modules.
"""

from collections.abc import Callable, Container, Iterable, Sequence
from re import Pattern
from typing import Final, Literal

from docutils.languages import _LanguageModule
from docutils.nodes import document, system_message
from docutils.parsers import Parser
from docutils.parsers.rst import Directive

__docformat__: Final = "reStructuredText"

def register_directive(name: str, directive: type[Directive]) -> None:
    """
    Register a nonstandard application-defined directive function.
    Language lookups are not needed for such functions.
    """

def directive(
    directive_name: str, language_module: _LanguageModule, document: document
) -> tuple[type[Directive] | None, list[system_message]]:
    """
    Locate and return a directive function from its language-dependent name.
    If not found in the current language, check English.  Return None if the
    named directive cannot be found.
    """

def flag(argument: str | None) -> None:
    """
    Check for a valid flag option (no argument) and return ``None``.
    (Directive option conversion function.)

    Raise ``ValueError`` if an argument is found.
    """

def unchanged_required(argument: str) -> str:
    """
    Return the argument text, unchanged.
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """

def unchanged(argument: str | None) -> str:
    """
    Return the argument text, unchanged.
    (Directive option conversion function.)

    No argument implies empty string ("").
    """

def path(argument: str) -> str:
    """
    Return the path argument unwrapped (with newlines removed).
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """

def uri(argument: str) -> str:
    """
    Return the URI argument with unescaped whitespace removed.
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """

def nonnegative_int(argument: str) -> int:
    """
    Check for a nonnegative integer argument; raise ``ValueError`` if not.
    (Directive option conversion function.)
    """

def percentage(argument: str) -> int:
    """
    Check for an integer percentage value with optional percent sign.
    (Directive option conversion function.)
    """

length_units: Final[list[str]]

def get_measure(argument: str, units: Iterable[str]) -> str:
    """
    Check for a positive argument of one of the units and return a
    normalized string of the form "<value><unit>" (without space in
    between).
    (Directive option conversion function.)

    To be called from directive option conversion functions.
    """

def length_or_unitless(argument: str) -> str: ...
def length_or_percentage_or_unitless(argument: str, default: str = "") -> str:
    """
    Return normalized string of a length or percentage unit.
    (Directive option conversion function.)

    Add <default> if there is no unit. Raise ValueError if the argument is not
    a positive measure of one of the valid CSS units (or without unit).

    >>> length_or_percentage_or_unitless('3 pt')
    '3pt'
    >>> length_or_percentage_or_unitless('3%', 'em')
    '3%'
    >>> length_or_percentage_or_unitless('3')
    '3'
    >>> length_or_percentage_or_unitless('3', 'px')
    '3px'
    """

def class_option(argument: str) -> list[str]:
    """
    Convert the argument into a list of ID-compatible strings and return it.
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """

unicode_pattern: Final[Pattern[str]]

def unicode_code(code: str) -> str:
    """
    Convert a Unicode character code to a Unicode character.
    (Directive option conversion function.)

    Codes may be decimal numbers, hexadecimal numbers (prefixed by ``0x``,
    ``x``, ``\\x``, ``U+``, ``u``, or ``\\u``; e.g. ``U+262E``), or XML-style
    numeric character entities (e.g. ``&#x262E;``).  Other text remains as-is.

    Raise ValueError for illegal Unicode code values.
    """

def single_char_or_unicode(argument: str) -> str:
    """
    A single character is returned as-is.  Unicode character codes are
    converted as in `unicode_code`.  (Directive option conversion function.)
    """

def single_char_or_whitespace_or_unicode(argument: str | Literal["tab", "space"]) -> str:  # noqa: Y051
    """
    As with `single_char_or_unicode`, but "tab" and "space" are also supported.
    (Directive option conversion function.)
    """

def positive_int(argument: str) -> int:
    """
    Converts the argument into an integer.  Raises ValueError for negative,
    zero, or non-integer values.  (Directive option conversion function.)
    """

def positive_int_list(argument: str) -> list[int]:
    """
    Converts a space- or comma-separated list of values into a Python list
    of integers.
    (Directive option conversion function.)

    Raises ValueError for non-positive-integer values.
    """

def encoding(argument: str) -> str:
    """
    Verifies the encoding argument by lookup.
    (Directive option conversion function.)

    Raises ValueError for unknown encodings.
    """

def choice(argument: str, values: Sequence[str]) -> str:
    """
    Directive option utility function, supplied to enable options whose
    argument must be a member of a finite set of possible values (must be
    lower case).  A custom conversion function must be written to use it.  For
    example::

        from docutils.parsers.rst import directives

        def yesno(argument):
            return directives.choice(argument, ('yes', 'no'))

    Raise ``ValueError`` if no argument is found or if the argument's value is
    not valid (not an entry in the supplied list).
    """

def format_values(values: Sequence[object]) -> str: ...
def value_or(values: Container[str], other: Callable[[str], str]) -> Callable[[str], str]:
    """
    Directive option conversion function.

    The argument can be any of `values` or `argument_type`.
    """

def parser_name(argument: str | None) -> type[Parser] | None:
    """
    Return a docutils parser whose name matches the argument.
    (Directive option conversion function.)

    Return `None`, if the argument evaluates to `False`.
    Raise `ValueError` if importing the parser module fails.
    """
