"""Lexical analysis of formal languages (i.e. code) using Pygments."""

from collections.abc import Generator, Iterable
from typing import Literal
from typing_extensions import TypeAlias

from docutils import ApplicationError

_TokenNames: TypeAlias = Literal["long", "short", "none"]

with_pygments: bool
unstyled_tokens: list[str]

class LexerError(ApplicationError): ...

class Lexer:
    """Parse `code` lines and yield "classified" tokens.

    Arguments

      code       -- string of source code to parse,
      language   -- formal language the code is written in,
      tokennames -- either 'long', 'short', or 'none' (see below).

    Merge subsequent tokens of the same token-type.

    Iterating over an instance yields the tokens as ``(tokentype, value)``
    tuples. The value of `tokennames` configures the naming of the tokentype:

      'long':  downcased full token type name,
      'short': short name defined by pygments.token.STANDARD_TYPES
               (= class argument used in pygments html output),
      'none':  skip lexical analysis.
    """

    code: str
    language: str
    tokennames: _TokenNames
    lexer: Lexer | None
    def __init__(self, code: str, language: str, tokennames: _TokenNames = "short") -> None:
        """
        Set up a lexical analyzer for `code` in `language`.
        """

    def merge(self, tokens: Iterable[tuple[_TokenNames, str]]) -> Generator[tuple[_TokenNames, str]]:
        """Merge subsequent tokens of same token-type.

        Also strip the final newline (added by pygments).
        """

    def __iter__(self) -> Generator[tuple[list[str], str]]:
        """Parse self.code and yield "classified" tokens."""

class NumberLines:
    """Insert linenumber-tokens at the start of every code line.

    Arguments

       tokens    -- iterable of ``(classes, value)`` tuples
       startline -- first line number
       endline   -- last line number

    Iterating over an instance yields the tokens with a
    ``(['ln'], '<the line number>')`` token added for every code line.
    Multi-line tokens are split.
    """

    tokens: Iterable[tuple[list[str], str]]
    startline: int
    fmt_str: str
    def __init__(self, tokens: Iterable[tuple[list[str], str]], startline: int, endline: int) -> None: ...
    def __iter__(self) -> Generator[tuple[list[str], str]]: ...
