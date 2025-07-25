"""
pygments.formatters
~~~~~~~~~~~~~~~~~~~

Pygments formatters.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from collections.abc import Generator
from typing import Any

from ..formatter import Formatter
from .bbcode import BBCodeFormatter as BBCodeFormatter
from .html import HtmlFormatter as HtmlFormatter
from .img import (
    BmpImageFormatter as BmpImageFormatter,
    GifImageFormatter as GifImageFormatter,
    ImageFormatter as ImageFormatter,
    JpgImageFormatter as JpgImageFormatter,
)
from .irc import IRCFormatter as IRCFormatter
from .latex import LatexFormatter as LatexFormatter
from .other import NullFormatter as NullFormatter, RawTokenFormatter as RawTokenFormatter, TestcaseFormatter as TestcaseFormatter
from .pangomarkup import PangoMarkupFormatter as PangoMarkupFormatter
from .rtf import RtfFormatter as RtfFormatter
from .svg import SvgFormatter as SvgFormatter
from .terminal import TerminalFormatter as TerminalFormatter
from .terminal256 import Terminal256Formatter as Terminal256Formatter, TerminalTrueColorFormatter as TerminalTrueColorFormatter

def get_all_formatters() -> Generator[type[Formatter[Any]], None, None]:
    """Return a generator for all formatter classes."""

def get_formatter_by_name(_alias, **options):
    """
    Return an instance of a :class:`.Formatter` subclass that has `alias` in its
    aliases list. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter with that
    alias is found.
    """

def load_formatter_from_file(filename, formattername: str = "CustomFormatter", **options):
    """
    Return a `Formatter` subclass instance loaded from the provided file, relative
    to the current directory.

    The file is expected to contain a Formatter class named ``formattername``
    (by default, CustomFormatter). Users should be very careful with the input, because
    this method is equivalent to running ``eval()`` on the input file. The formatter is
    given the `options` at its instantiation.

    :exc:`pygments.util.ClassNotFound` is raised if there are any errors loading
    the formatter.

    .. versionadded:: 2.2
    """

def get_formatter_for_filename(fn, **options):
    """
    Return a :class:`.Formatter` subclass instance that has a filename pattern
    matching `fn`. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter for that filename
    is found.
    """
