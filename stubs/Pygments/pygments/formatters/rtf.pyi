"""
pygments.formatters.rtf
~~~~~~~~~~~~~~~~~~~~~~~

A formatter that generates RTF files.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class RtfFormatter(Formatter[_T]):
    """
    Format tokens as RTF markup. This formatter automatically outputs full RTF
    documents with color information and other useful stuff. Perfect for Copy and
    Paste into Microsoft(R) Word(R) documents.

    Please note that ``encoding`` and ``outencoding`` options are ignored.
    The RTF format is ASCII natively, but handles unicode characters correctly
    thanks to escape sequences.

    .. versionadded:: 0.6

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `fontface`
        The used font family, for example ``Bitstream Vera Sans``. Defaults to
        some generic font which is supposed to have fixed width.

    `fontsize`
        Size of the font used. Size is specified in half points. The
        default is 24 half-points, giving a size 12 font.

        .. versionadded:: 2.0

    `linenos`
        Turn on line numbering (default: ``False``).

        .. versionadded:: 2.18

    `lineno_fontsize`
        Font size for line numbers. Size is specified in half points
        (default: `fontsize`).

        .. versionadded:: 2.18

    `lineno_padding`
        Number of spaces between the (inline) line numbers and the
        source code (default: ``2``).

        .. versionadded:: 2.18

    `linenostart`
        The line number for the first line (default: ``1``).

        .. versionadded:: 2.18

    `linenostep`
        If set to a number n > 1, only every nth line number is printed.

        .. versionadded:: 2.18

    `lineno_color`
        Color for line numbers specified as a hex triplet, e.g. ``'5e5e5e'``.
        Defaults to the style's line number color if it is a hex triplet,
        otherwise ansi bright black.

        .. versionadded:: 2.18

    `hl_lines`
        Specify a list of lines to be highlighted, as line numbers separated by
        spaces, e.g. ``'3 7 8'``. The line numbers are relative to the input
        (i.e. the first line is line 1) unless `hl_linenostart` is set.

        .. versionadded:: 2.18

    `hl_color`
        Color for highlighting the lines specified in `hl_lines`, specified as
        a hex triplet (default: style's `highlight_color`).

        .. versionadded:: 2.18

    `hl_linenostart`
        If set to ``True`` line numbers in `hl_lines` are specified
        relative to `linenostart` (default ``False``).

        .. versionadded:: 2.18
    """

    name: str
    aliases: Any
    filenames: Any
    fontface: Any
    fontsize: Any
    def format_unencoded(self, tokensource, outfile) -> None: ...
