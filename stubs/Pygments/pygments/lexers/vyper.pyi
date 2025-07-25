"""
pygments.lexers.vyper
~~~~~~~~~~~~~~~~~~~~~

Lexer for the Vyper Smart Contract language.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from ..lexer import RegexLexer

__all__ = ["VyperLexer"]

class VyperLexer(RegexLexer):
    """For the Vyper smart contract language."""
