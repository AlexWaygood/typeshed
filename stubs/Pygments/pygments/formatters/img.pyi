"""
pygments.formatters.img
~~~~~~~~~~~~~~~~~~~~~~~

Formatter for Pixmap output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class PilNotAvailable(ImportError):
    """When Python imaging library is not available"""

class FontNotFound(Exception):
    """When there are no usable fonts specified"""

class FontManager:
    """
    Manages a set of fonts: normal, italic, bold, etc...
    """

    font_name: Any
    font_size: Any
    fonts: Any
    encoding: Any
    variable: bool
    def __init__(self, font_name, font_size: int = 14) -> None: ...
    def get_char_size(self):
        """
        Get the character size.
        """

    def get_text_size(self, text):
        """
        Get the text size (width, height).
        """

    def get_font(self, bold, oblique):
        """
        Get the font based on bold and italic flags.
        """

    def get_style(self, style):
        """
        Get the specified style of the font if it is a variable font.
        If not found, return the normal font.
        """

class ImageFormatter(Formatter[_T]):
    """
    Create a PNG image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 0.10

    Additional options accepted:

    `image_format`
        An image format to output to that is recognised by PIL, these include:

        * "PNG" (default)
        * "JPEG"
        * "BMP"
        * "GIF"

    `line_pad`
        The extra spacing (in pixels) between each line of text.

        Default: 2

    `font_name`
        The font name to be used as the base font from which others, such as
        bold and italic fonts will be generated.  This really should be a
        monospace font to look sane.
        If a filename or a file-like object is specified, the user must
        provide different styles of the font.

        Default: "Courier New" on Windows, "Menlo" on Mac OS, and
                 "DejaVu Sans Mono" on \\*nix

    `font_size`
        The font size in points to be used.

        Default: 14

    `image_pad`
        The padding, in pixels to be used at each edge of the resulting image.

        Default: 10

    `line_numbers`
        Whether line numbers should be shown: True/False

        Default: True

    `line_number_start`
        The line number of the first line.

        Default: 1

    `line_number_step`
        The step used when printing line numbers.

        Default: 1

    `line_number_bg`
        The background colour (in "#123456" format) of the line number bar, or
        None to use the style background color.

        Default: "#eed"

    `line_number_fg`
        The text color of the line numbers (in "#123456"-like format).

        Default: "#886"

    `line_number_chars`
        The number of columns of line numbers allowable in the line number
        margin.

        Default: 2

    `line_number_bold`
        Whether line numbers will be bold: True/False

        Default: False

    `line_number_italic`
        Whether line numbers will be italicized: True/False

        Default: False

    `line_number_separator`
        Whether a line will be drawn between the line number area and the
        source code area: True/False

        Default: True

    `line_number_pad`
        The horizontal padding (in pixels) between the line number margin, and
        the source code area.

        Default: 6

    `hl_lines`
        Specify a list of lines to be highlighted.

        .. versionadded:: 1.2

        Default: empty list

    `hl_color`
        Specify the color for highlighting lines.

        .. versionadded:: 1.2

        Default: highlight color of the selected style
    """

    name: str
    aliases: Any
    filenames: Any
    unicodeoutput: bool
    default_image_format: str
    encoding: str
    styles: Any
    background_color: str
    image_format: Any
    image_pad: Any
    line_pad: Any
    fonts: Any
    line_number_fg: Any
    line_number_bg: Any
    line_number_chars: Any
    line_number_bold: Any
    line_number_italic: Any
    line_number_pad: Any
    line_numbers: Any
    line_number_separator: Any
    line_number_step: Any
    line_number_start: Any
    line_number_width: Any
    hl_lines: Any
    hl_color: Any
    drawables: Any
    def get_style_defs(self, arg: str = "") -> None: ...
    def format(self, tokensource, outfile) -> None:
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """

class GifImageFormatter(ImageFormatter[_T]):
    """
    Create a GIF image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """

    name: str
    aliases: Any
    filenames: Any
    default_image_format: str

class JpgImageFormatter(ImageFormatter[_T]):
    """
    Create a JPEG image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """

    name: str
    aliases: Any
    filenames: Any
    default_image_format: str

class BmpImageFormatter(ImageFormatter[_T]):
    """
    Create a bitmap image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """

    name: str
    aliases: Any
    filenames: Any
    default_image_format: str
