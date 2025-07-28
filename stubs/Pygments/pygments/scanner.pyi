"""
pygments.scanner
~~~~~~~~~~~~~~~~

This library implements a regex based scanner. Some languages
like Pascal are easy to parse but have some keywords that
depend on the context. Because of this it's impossible to lex
that just by using a regular expression lexer like the
`RegexLexer`.

Have a look at the `DelphiLexer` to get an idea of how to use
this scanner.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any

class EndOfText(RuntimeError):
    """
    Raise if end of text is reached and the user
    tried to call a match function.
    """

class Scanner:
    """
    Simple scanner

    All method patterns are regular expression strings (not
    compiled expressions!)
    """

    data: Any
    data_length: Any
    start_pos: int
    pos: int
    flags: Any
    last: Any
    match: Any
    def __init__(self, text, flags: int = 0) -> None:
        """
        :param text:    The text which should be scanned
        :param flags:   default regular expression flags
        """

    @property
    def eos(self):
        """`True` if the scanner reached the end of text."""

    def check(self, pattern):
        """
        Apply `pattern` on the current position and return
        the match object. (Doesn't touch pos). Use this for
        lookahead.
        """

    def test(self, pattern):
        """Apply a pattern on the current position and check
        if it patches. Doesn't touch pos.
        """

    def scan(self, pattern):
        """
        Scan the text for the given pattern and update pos/match
        and related fields. The return value is a boolean that
        indicates if the pattern matched. The matched value is
        stored on the instance as ``match``, the last value is
        stored as ``last``. ``start_pos`` is the position of the
        pointer before the pattern was matched, ``pos`` is the
        end position.
        """

    def get_char(self) -> None:
        """Scan exactly one char."""
