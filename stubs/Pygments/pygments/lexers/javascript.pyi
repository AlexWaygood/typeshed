"""
pygments.lexers.javascript
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lexers for JavaScript and related languages.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from collections.abc import Iterator
from typing import Final

from ..lexer import Lexer, RegexLexer
from ..token import _TokenType

__all__ = [
    "JavascriptLexer",
    "KalLexer",
    "LiveScriptLexer",
    "DartLexer",
    "TypeScriptLexer",
    "LassoLexer",
    "ObjectiveJLexer",
    "CoffeeScriptLexer",
    "MaskLexer",
    "EarlGreyLexer",
    "JuttleLexer",
    "NodeConsoleLexer",
]

JS_IDENT_START: Final[str]
JS_IDENT_PART: Final[str]
JS_IDENT: Final[str]

class JavascriptLexer(RegexLexer):
    """
    For JavaScript source code.
    """

class TypeScriptLexer(JavascriptLexer):
    """
    For TypeScript source code.
    """

class KalLexer(RegexLexer):
    """
    For Kal source code.
    """

class LiveScriptLexer(RegexLexer):
    """
    For LiveScript source code.
    """

class DartLexer(RegexLexer):
    """
    For Dart source code.
    """

class LassoLexer(RegexLexer):
    """
    For Lasso source code, covering both Lasso 9
    syntax and LassoScript for Lasso 8.6 and earlier. For Lasso embedded in
    HTML, use the `LassoHtmlLexer`.

    Additional options accepted:

    `builtinshighlighting`
        If given and ``True``, highlight builtin types, traits, methods, and
        members (default: ``True``).
    `requiredelimiters`
        If given and ``True``, only highlight code between delimiters as Lasso
        (default: ``False``).
    """

    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...  # type: ignore[override]

class ObjectiveJLexer(RegexLexer):
    """
    For Objective-J source code with preprocessor directives.
    """

class CoffeeScriptLexer(RegexLexer):
    """
    For CoffeeScript source code.
    """

class MaskLexer(RegexLexer):
    """
    For Mask markup.
    """

class EarlGreyLexer(RegexLexer):
    """
    For Earl-Grey source code.

    .. versionadded: 2.1
    """

class JuttleLexer(RegexLexer):
    """
    For Juttle source code.
    """

class NodeConsoleLexer(Lexer):
    """
    For parsing within an interactive Node.js REPL, such as:

    .. sourcecode:: nodejsrepl

        > let a = 3
        undefined
        > a
        3
        > let b = '4'
        undefined
        > b
        '4'
        > b == a
        false

    .. versionadded: 2.10
    """
