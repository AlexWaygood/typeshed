"""General tools which don't depend on other parts of Parsimonious"""

import ast
from typing import Any

class StrAndRepr:
    """Mix-in which gives the class the same __repr__ and __str__."""

def evaluate_string(string: str | ast.AST) -> Any:
    """Piggyback on Python's string support so we can have backslash escaping
        and niceties like
    ,       , etc.

        This also supports:
        1. b"strings", allowing grammars to parse bytestrings, in addition to str.
        2. r"strings" to simplify regexes.
    """

class Token(StrAndRepr):
    """A class to represent tokens, for use with TokenGrammars

    You will likely want to subclass this to hold additional information, like
    the characters that you lexed to create this token. Alternately, feel free
    to create your own class from scratch. The only contract is that tokens
    must have a ``type`` attr.

    """

    type: str
    def __init__(self, type: str) -> None: ...
