"""
pygments.formatters.other
~~~~~~~~~~~~~~~~~~~~~~~~~

Other formatters: NullFormatter, RawTokenFormatter.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class NullFormatter(Formatter[_T]):
    """
    Output the text unchanged without any formatting.
    """

    name: str
    aliases: Any
    filenames: Any
    def format(self, tokensource, outfile) -> None: ...

class RawTokenFormatter(Formatter[bytes]):
    """
    Format tokens as a raw representation for storing token streams.

    The format is ``tokentype<TAB>repr(tokenstring)\\n``. The output can later
    be converted to a token stream with the `RawTokenLexer`, described in the
    :doc:`lexer list <lexers>`.

    Only two options are accepted:

    `compress`
        If set to ``'gz'`` or ``'bz2'``, compress the output with the given
        compression algorithm after encoding (default: ``''``).
    `error_color`
        If set to a color name, highlight error tokens using that color.  If
        set but with no value, defaults to ``'red'``.

        .. versionadded:: 0.11

    """

    name: str
    aliases: Any
    filenames: Any
    unicodeoutput: bool
    encoding: str
    compress: Any
    error_color: Any
    def format(self, tokensource, outfile) -> None: ...

class TestcaseFormatter(Formatter[_T]):
    """
    Format tokens as appropriate for a new testcase.

    .. versionadded:: 2.0
    """

    name: str
    aliases: Any
    def format(self, tokensource, outfile) -> None: ...
