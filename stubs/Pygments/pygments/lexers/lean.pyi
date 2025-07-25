"""
pygments.lexers.lean
~~~~~~~~~~~~~~~~~~~~

Lexers for the Lean theorem prover.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from ..lexer import RegexLexer

__all__ = ["Lean3Lexer"]

class Lean3Lexer(RegexLexer):
    """
    For the Lean 3 theorem prover.
    """

LeanLexer = Lean3Lexer
