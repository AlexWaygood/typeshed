"""
pygments.lexers.prql
~~~~~~~~~~~~~~~~~~~~

Lexer for the PRQL query language.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from typing import ClassVar

from ..lexer import RegexLexer

__all__ = ["PrqlLexer"]

class PrqlLexer(RegexLexer):
    """
    For PRQL source code.

    grammar: https://github.com/PRQL/prql/tree/main/grammars
    """

    builtinTypes: ClassVar[Incomplete]
    def innerstring_rules(ttype) -> list[tuple[str, Incomplete]]: ...
    def fstring_rules(ttype) -> list[tuple[str, Incomplete]]: ...
