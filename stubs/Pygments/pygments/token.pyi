"""
pygments.token
~~~~~~~~~~~~~~

Basic token types and the standard tokens.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from collections.abc import Mapping
from typing import Any
from typing_extensions import Self

class _TokenType(tuple[str, ...]):
    parent: _TokenType | None
    def split(self) -> list[_TokenType]: ...
    subtypes: set[_TokenType]
    def __contains__(self, val: _TokenType) -> bool: ...  # type: ignore[override]
    def __getattr__(self, name: str) -> _TokenType: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: Any) -> Self: ...

Token: _TokenType
Text: _TokenType
Whitespace: _TokenType
Escape: _TokenType
Error: _TokenType
Other: _TokenType
Keyword: _TokenType
Name: _TokenType
Literal: _TokenType
String: _TokenType
Number: _TokenType
Punctuation: _TokenType
Operator: _TokenType
Comment: _TokenType
Generic: _TokenType

def is_token_subtype(ttype, other):
    """
    Return True if ``ttype`` is a subtype of ``other``.

    exists for backwards compatibility. use ``ttype in other`` now.
    """

def string_to_tokentype(s):
    """
    Convert a string into a token type::

        >>> string_to_token('String.Double')
        Token.Literal.String.Double
        >>> string_to_token('Token.Literal.Number')
        Token.Literal.Number
        >>> string_to_token('')
        Token

    Tokens that are already tokens are returned unchanged:

        >>> string_to_token(String)
        Token.Literal.String
    """

# dict, but shouldn't be mutated
STANDARD_TYPES: Mapping[_TokenType, str]
