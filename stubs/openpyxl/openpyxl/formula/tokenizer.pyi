"""
This module contains a tokenizer for Excel formulae.

The tokenizer is based on the Javascript tokenizer found at
http://ewbi.blogs.com/develops/2004/12/excel_formula_p.html written by Eric
Bachtal
"""

from _typeshed import Incomplete
from re import Pattern
from typing import Final, Literal
from typing_extensions import TypeAlias

_TokenTypesNotOperand: TypeAlias = Literal[
    "LITERAL", "FUNC", "ARRAY", "PAREN", "SEP", "OPERATOR-PREFIX", "OPERATOR-INFIX", "OPERATOR-POSTFIX", "WHITE-SPACE"
]
_TokenTypes: TypeAlias = Literal["OPERAND", _TokenTypesNotOperand]
_TokenOperandSubtypes: TypeAlias = Literal["TEXT", "NUMBER", "LOGICAL", "ERROR", "RANGE"]
_TokenSubtypes: TypeAlias = Literal["", _TokenOperandSubtypes, "OPEN", "CLOSE", "ARG", "ROW"]

class TokenizerError(Exception):
    """Base class for all Tokenizer errors."""

class Tokenizer:
    """
    A tokenizer for Excel worksheet formulae.

    Converts a str string representing an Excel formula (in A1 notation)
    into a sequence of `Token` objects.

    `formula`: The str string to tokenize

    Tokenizer defines a method `._parse()` to parse the formula into tokens,
    which can then be accessed through the `.items` attribute.

    """

    SN_RE: Final[Pattern[str]]
    WSPACE_RE: Final[Pattern[str]]
    STRING_REGEXES: Final[dict[str, Pattern[str]]]
    ERROR_CODES: Final[tuple[str, ...]]
    TOKEN_ENDERS: Final = ",;}) +-*/^&=><%"
    formula: Incomplete
    items: Incomplete
    token_stack: Incomplete
    offset: int
    token: Incomplete
    def __init__(self, formula) -> None: ...
    def check_scientific_notation(self):
        """
        Consumes a + or - character if part of a number in sci. notation.

        Returns True if the character was consumed and self.offset was
        updated, False otherwise.

        """

    def assert_empty_token(self, can_follow=()) -> None:
        """
        Ensure that there's no token currently being parsed.

        Or if there is a token being parsed, it must end with a character in
        can_follow.

        If there are unconsumed token contents, it means we hit an unexpected
        token transition. In this case, we raise a TokenizerError

        """

    def save_token(self) -> None:
        """If there's a token being parsed, add it to the item list."""

    def render(self):
        """Convert the parsed tokens back to a string."""

class Token:
    """
    A token in an Excel formula.

    Tokens have three attributes:

    * `value`: The string value parsed that led to this token
    * `type`: A string identifying the type of token
    * `subtype`: A string identifying subtype of the token (optional, and
                 defaults to "")

    """

    LITERAL: Final = "LITERAL"
    OPERAND: Final = "OPERAND"
    FUNC: Final = "FUNC"
    ARRAY: Final = "ARRAY"
    PAREN: Final = "PAREN"
    SEP: Final = "SEP"
    OP_PRE: Final = "OPERATOR-PREFIX"
    OP_IN: Final = "OPERATOR-INFIX"
    OP_POST: Final = "OPERATOR-POSTFIX"
    WSPACE: Final = "WHITE-SPACE"
    value: Incomplete
    type: _TokenTypes
    subtype: _TokenSubtypes
    def __init__(self, value, type_: _TokenTypes, subtype: _TokenSubtypes = "") -> None: ...
    TEXT: Final = "TEXT"
    NUMBER: Final = "NUMBER"
    LOGICAL: Final = "LOGICAL"
    ERROR: Final = "ERROR"
    RANGE: Final = "RANGE"
    @classmethod
    def make_operand(cls, value):
        """Create an operand token."""
    OPEN: Final = "OPEN"
    CLOSE: Final = "CLOSE"
    @classmethod
    def make_subexp(cls, value, func: bool = False):
        """
        Create a subexpression token.

        `value`: The value of the token
        `func`: If True, force the token to be of type FUNC

        """

    def get_closer(self):
        """Return a closing token that matches this token's type."""
    ARG: Final = "ARG"
    ROW: Final = "ROW"
    @classmethod
    def make_separator(cls, value):
        """Create a separator token"""
