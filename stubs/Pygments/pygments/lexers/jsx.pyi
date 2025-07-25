"""
pygments.lexers.jsx
~~~~~~~~~~~~~~~~~~~

Lexers for JSX (React) and TSX (TypeScript flavor).

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from .javascript import JavascriptLexer

__all__ = ["JsxLexer"]

class JsxLexer(JavascriptLexer):
    """For JavaScript Syntax Extension (JSX)."""
