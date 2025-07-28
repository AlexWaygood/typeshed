"""
pygments.lexers.vip
~~~~~~~~~~~~~~~~~~~

Lexers for Visual Prolog & Grammar files.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import ClassVar

from ..lexer import RegexLexer

__all__ = ["VisualPrologLexer", "VisualPrologGrammarLexer"]

class VisualPrologBaseLexer(RegexLexer):
    minorendkw: ClassVar[tuple[str, ...]]
    minorkwexp: ClassVar[tuple[str, ...]]
    dockw: ClassVar[tuple[str, ...]]

class VisualPrologLexer(VisualPrologBaseLexer):
    """Lexer for VisualProlog"""

    majorkw: ClassVar[tuple[str, ...]]
    minorkw: ClassVar[tuple[str, ...]]
    directivekw: ClassVar[tuple[str, ...]]

class VisualPrologGrammarLexer(VisualPrologBaseLexer):
    """Lexer for VisualProlog grammar"""

    majorkw: ClassVar[tuple[str, ...]]
    directivekw: ClassVar[tuple[str, ...]]
