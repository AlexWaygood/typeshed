"""
Module for formatting information.
"""

from collections.abc import Callable
from typing import Final, Literal

from .biffh import BaseObject
from .book import Book
from .timemachine import *

DEBUG: Final[int]
excel_default_palette_b5: Final[tuple[tuple[int, int, int], ...]]
excel_default_palette_b2: Final[tuple[tuple[int, int, int], ...]]
excel_default_palette_b8: Final[tuple[tuple[int, int, int], ...]]
default_palette: Final[dict[int, tuple[tuple[int, int, int], ...]]]
built_in_style_names: Final[list[str]]

def initialise_colour_map(book: Book) -> None: ...
def nearest_colour_index(
    colour_map: dict[int, tuple[int, int, int] | None], rgb: tuple[int, int, int] | None, debug: int = 0
) -> int:
    """
    General purpose function. Uses Euclidean distance.
    So far used only for pre-BIFF8 ``WINDOW2`` record.
    Doesn't have to be fast.
    Doesn't have to be fancy.
    """

class EqNeAttrs:
    """
    This mixin class exists solely so that :class:`Format`, :class:`Font`, and
    :class:`XF` objects can be compared by value of their attributes.
    """

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Font(BaseObject, EqNeAttrs):
    """
    An Excel "font" contains the details of not only what is normally
    considered a font, but also several other display attributes.
    Items correspond to those in the Excel UI's Format -> Cells -> Font tab.

    .. versionadded:: 0.6.1
    """

    bold: Literal[0, 1]
    character_set: int
    colour_index: int
    escapement: Literal[0, 1, 2]
    family: Literal[0, 1, 2, 3, 4, 5]
    font_index: int
    height: int
    italic: Literal[0, 1]
    name: str
    struck_out: Literal[0, 1]
    underline_type: Literal[0, 1, 33, 34]
    underlined: Literal[0, 1]
    weight: int
    outline: Literal[0, 1]
    shadow: Literal[0, 1]

def handle_efont(book: Book, data: bytes) -> None: ...
def handle_font(book: Book, data: bytes) -> None: ...

class Format(BaseObject, EqNeAttrs):
    """
    "Number format" information from a ``FORMAT`` record.

    .. versionadded:: 0.6.1
    """

    format_key: int
    type: int
    format_str: str
    def __init__(self, format_key: int, ty: int, format_str: str) -> None: ...

std_format_strings: dict[int, str]
fmt_code_ranges: list[tuple[int, int, int]]
std_format_code_types: dict[int, int]
date_char_dict: dict[str, Literal[5]]
skip_char_dict: dict[str, Literal[1]]
num_char_dict: dict[str, Literal[5]]
non_date_formats: dict[str, Literal[1]]
fmt_bracketed_sub: Callable[[str, str], str]

def is_date_format_string(book: Book, fmt: str) -> bool: ...
def handle_format(self: Book, data: bytes, rectype: int = 1054) -> None: ...
def handle_palette(book: Book, data: bytes) -> None: ...
def palette_epilogue(book: Book) -> None: ...
def handle_style(book: Book, data: bytes) -> None: ...
def check_colour_indexes_in_obj(book: Book, obj: object, orig_index: int) -> None: ...
def fill_in_standard_formats(book: Book) -> None: ...
def handle_xf(self: Book, data: bytes) -> None: ...
def xf_epilogue(self: Book) -> None: ...
def initialise_book(book: Book) -> None: ...

class XFBorder(BaseObject, EqNeAttrs):
    """
    A collection of the border-related attributes of an ``XF`` record.
    Items correspond to those in the Excel UI's Format -> Cells -> Border tab.

    An explanations of "colour index" is given in :ref:`palette`.

    There are five line style attributes; possible values and the
    associated meanings are::

      0 = No line,
      1 = Thin,
      2 = Medium,
      3 = Dashed,
      4 = Dotted,
      5 = Thick,
      6 = Double,
      7 = Hair,
      8 = Medium dashed,
      9 = Thin dash-dotted,
      10 = Medium dash-dotted,
      11 = Thin dash-dot-dotted,
      12 = Medium dash-dot-dotted,
      13 = Slanted medium dash-dotted.

    The line styles 8 to 13 appear in BIFF8 files (Excel 97 and later) only.
    For pictures of the line styles, refer to OOo docs s3.10 (p22)
    "Line Styles for Cell Borders (BIFF3-BIFF8)".</p>

    .. versionadded:: 0.6.1
    """

    top_colour_index: int
    bottom_colour_index: int
    left_colour_index: int
    right_colour_index: int
    diag_colour_index: int
    top_line_style: int
    bottom_line_style: int
    left_line_style: int
    right_line_style: int
    diag_line_style: int
    diag_down: Literal[0, 1]
    diag_up: Literal[0, 1]

class XFBackground(BaseObject, EqNeAttrs):
    """
    A collection of the background-related attributes of an ``XF`` record.
    Items correspond to those in the Excel UI's Format -> Cells -> Patterns tab.

    An explanations of "colour index" is given in :ref:`palette`.

    .. versionadded:: 0.6.1
    """

    fill_pattern: int
    background_colour_index: int
    pattern_colour_index: int

class XFAlignment(BaseObject, EqNeAttrs):
    """
    A collection of the alignment and similar attributes of an ``XF`` record.
    Items correspond to those in the Excel UI's Format -> Cells -> Alignment tab.

    .. versionadded:: 0.6.1
    """

    hor_align: int
    vert_align: int
    rotation: int
    text_wrapped: Literal[0, 1]
    indent_level: int
    shrink_to_fit: Literal[0, 1]
    text_direction: Literal[0, 1, 2]

class XFProtection(BaseObject, EqNeAttrs):
    """
    A collection of the protection-related attributes of an ``XF`` record.
    Items correspond to those in the Excel UI's Format -> Cells -> Protection tab.
    Note the OOo docs include the "cell or style" bit in this bundle of
    attributes. This is incorrect; the bit is used in determining which bundles
    to use.

    .. versionadded:: 0.6.1
    """

    cell_locked: Literal[0, 1]
    formula_hidden: Literal[0, 1]

class XF(BaseObject):
    """
    eXtended Formatting information for cells, rows, columns and styles.

    Each of the 6 flags below describes the validity of
    a specific group of attributes.

    In cell XFs:

    - ``flag==0`` means the attributes of the parent style ``XF`` are
      used, (but only if the attributes are valid there);

    - ``flag==1`` means the attributes of this ``XF`` are used.

    In style XFs:

    - ``flag==0`` means the attribute setting is valid;
    - ``flag==1`` means the attribute should be ignored.

    .. note::
      the API provides both "raw" XFs and "computed" XFs. In the latter case,
      cell XFs have had the above inheritance mechanism applied.

    .. versionadded:: 0.6.1
    """

    is_style: Literal[0, 1]
    parent_style_index: int
    xf_index: int
    font_index: int
    format_key: int
    protection: XFProtection | None
    background: XFBackground | None
    alignment: XFAlignment | None
    border: XFBorder | None
