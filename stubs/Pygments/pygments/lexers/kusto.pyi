"""
pygments.lexers.kusto
~~~~~~~~~~~~~~~~~~~~~

Lexers for Kusto Query Language (KQL).

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Final

from ..lexer import RegexLexer

__all__ = ["KustoLexer"]

KUSTO_KEYWORDS: Final[list[str]]
KUSTO_PUNCTUATION: Final[list[str]]

class KustoLexer(RegexLexer):
    """For Kusto Query Language source code."""
