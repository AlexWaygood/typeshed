"""
pygments.formatters.terminal256
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Formatter for 256-color terminal output with ANSI sequences.

RGB-to-XTERM color conversion routines adapted from xterm256-conv
tool (http://frexx.de/xterm-256-notes/data/xterm256-conv2.tar.bz2)
by Wolfgang Frisch.

Formatter version 1.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class EscapeSequence:
    fg: Any
    bg: Any
    bold: Any
    underline: Any
    italic: Any
    def __init__(self, fg=None, bg=None, bold: bool = False, underline: bool = False, italic: bool = False) -> None: ...
    def escape(self, attrs): ...
    def color_string(self): ...
    def true_color_string(self): ...
    def reset_string(self): ...

class Terminal256Formatter(Formatter[_T]):
    """
    Format tokens with ANSI color sequences, for output in a 256-color
    terminal or console.  Like in `TerminalFormatter` color sequences
    are terminated at newlines, so that paging the output works correctly.

    The formatter takes colors from a style defined by the `style` option
    and converts them to nearest ANSI 256-color escape sequences. Bold and
    underline attributes from the style are preserved (and displayed).

    .. versionadded:: 0.9

    .. versionchanged:: 2.2
       If the used style defines foreground colors in the form ``#ansi*``, then
       `Terminal256Formatter` will map these to non extended foreground color.
       See :ref:`AnsiTerminalStyle` for more information.

    .. versionchanged:: 2.4
       The ANSI color names have been updated with names that are easier to
       understand and align with colornames of other projects and terminals.
       See :ref:`this table <new-ansi-color-names>` for more information.


    Options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `linenos`
        Set to ``True`` to have line numbers on the terminal output as well
        (default: ``False`` = no line numbers).
    """

    name: str
    aliases: Any
    filenames: Any
    xterm_colors: Any
    best_match: Any
    style_string: Any
    usebold: Any
    useunderline: Any
    useitalic: Any
    linenos: Any
    def format(self, tokensource, outfile): ...
    def format_unencoded(self, tokensource, outfile) -> None: ...

class TerminalTrueColorFormatter(Terminal256Formatter[_T]):
    """
    Format tokens with ANSI color sequences, for output in a true-color
    terminal or console.  Like in `TerminalFormatter` color sequences
    are terminated at newlines, so that paging the output works correctly.

    .. versionadded:: 2.1

    Options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).
    """

    name: str
    aliases: Any
    filenames: Any
