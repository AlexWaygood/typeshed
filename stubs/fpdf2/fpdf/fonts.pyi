"""
Font-related classes & constants.
Includes the definition of the character widths of all PDF standard fonts.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

import dataclasses
from _typeshed import Incomplete, Unused
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from logging import Logger
from typing import Final, overload
from typing_extensions import Self, deprecated

from ._fonttools_shims import _TTFont
from .drawing import DeviceGray, DeviceRGB, Number
from .enums import Align, TextEmphasis
from .syntax import PDFObject

LOGGER: Logger

# Only defined if harfbuzz is installed.
class HarfBuzzFont(Incomplete):  # derives from uharfbuzz.Font
    def __deepcopy__(self, _memo: object) -> Self: ...

@dataclass
class FontFace:
    """
    Represent basic font styling properties.
    This is a subset of `fpdf.graphics_state.GraphicsStateMixin` properties.
    """

    family: str | None
    emphasis: TextEmphasis | None
    size_pt: int | None
    color: DeviceGray | DeviceRGB | None
    fill_color: DeviceGray | DeviceRGB | None

    def __init__(
        self,
        family: str | None = None,
        emphasis=None,
        size_pt: int | None = None,
        color: int | tuple[Number, Number, Number] | DeviceGray | DeviceRGB | None = None,
        fill_color: int | tuple[Number, Number, Number] | DeviceGray | DeviceRGB | None = None,
    ) -> None: ...

    replace = dataclasses.replace

    @overload
    @staticmethod
    def combine(default_style: None, override_style: None) -> None:  # type: ignore[misc]
        """
        Create a combined FontFace with all the supplied features of the two styles. When both
        the default and override styles provide a feature, prefer the override style.
        Override specified FontFace style features
        Override this FontFace's values with the values of `other`.
        Values of `other` that are None in this FontFace will be kept unchanged.
        """

    @overload
    @staticmethod
    def combine(default_style: FontFace | None, override_style: FontFace | None) -> FontFace: ...

class TextStyle(FontFace):
    """
    Subclass of `FontFace` that allows to specify vertical & horizontal spacing
    """

    t_margin: int
    l_margin: int | Align
    b_margin: int
    def __init__(
        self,
        font_family: str | None = None,
        font_style: str | None = None,
        font_size_pt: int | None = None,
        color: int | tuple[int, int, int] | None = None,
        fill_color: int | tuple[int, int, int] | None = None,
        underline: bool = False,
        t_margin: int | None = None,
        l_margin: int | Align | str | None = None,
        b_margin: int | None = None,
    ): ...
    def replace(  # type: ignore[override]
        self,
        /,
        font_family: str | None = None,
        emphasis: TextEmphasis | None = None,
        font_size_pt: int | None = None,
        color: int | tuple[int, int, int] | None = None,
        fill_color: int | tuple[int, int, int] | None = None,
        t_margin: int | None = None,
        l_margin: int | None = None,
        b_margin: int | None = None,
    ) -> TextStyle:
        """
        Create a new TextStyle instance, with new values for some attributes.
        Same as `dataclasses.replace()`
        """

@deprecated("fpdf.TitleStyle is deprecated since 2.7.10. It has been replaced by fpdf.TextStyle.")
class TitleStyle(TextStyle): ...

__pdoc__: Final[dict[str, bool]]

class CoreFont:
    i: int
    type: str
    name: str
    up: int
    ut: int
    sp: int
    ss: int
    cw: int
    fontkey: str
    emphasis: TextEmphasis
    def __init__(self, fpdf, fontkey: str, style: int) -> None: ...
    def get_text_width(self, text: str, font_size_pt: int, _: Unused) -> float: ...
    def encode_text(self, text: str) -> str: ...

class TTFFont:
    i: int
    type: str
    ttffile: Incomplete
    fontkey: str
    ttfont: _TTFont
    scale: float
    desc: PDFFontDescriptor
    cw: defaultdict[str, int]
    cmap: Incomplete
    glyph_ids: dict[Incomplete, Incomplete]
    missing_glyphs: list[Incomplete]
    name: str
    up: int
    ut: int
    sp: int
    ss: int
    emphasis: TextEmphasis
    subset: SubsetMap
    hbfont: HarfBuzzFont | None  # Not always defined.
    def __init__(self, fpdf, font_file_path, fontkey: str, style: int) -> None: ...
    def close(self) -> None: ...
    def get_text_width(self, text: str, font_size_pt: int, text_shaping_params): ...
    def shaped_text_width(self, text: str, font_size_pt: int, text_shaping_params):
        """
        When texts are shaped, the length of a string is not always the sum of all individual character widths
        This method will invoke harfbuzz to perform the text shaping and return the sum of "x_advance"
        and "x_offset" for each glyph. This method works for "left to right" or "right to left" texts.
        """

    def perform_harfbuzz_shaping(self, text: str, font_size_pt: int, text_shaping_params):
        """
        This method invokes Harfbuzz to perform text shaping of the input string
        """

    def encode_text(self, text: str) -> str: ...
    def shape_text(self, text: str, font_size_pt: int, text_shaping_params):
        """
        This method will invoke harfbuzz for text shaping, include the mapping code
        of the glyphs on the subset and map input characters to the cluster codes
        """

class PDFFontDescriptor(PDFObject):
    type: Incomplete
    ascent: Incomplete
    descent: Incomplete
    cap_height: Incomplete
    flags: Incomplete
    font_b_box: Incomplete
    italic_angle: Incomplete
    stem_v: Incomplete
    missing_width: Incomplete
    font_name: Incomplete
    def __init__(self, ascent, descent, cap_height, flags, font_b_box, italic_angle, stem_v, missing_width) -> None: ...

@dataclass(order=True)
class Glyph:
    """
    This represents one glyph on the font
    Unicode is a tuple because ligatures or character substitution
    can map a sequence of unicode characters to a single glyph
    """

    glyph_id: int
    unicode: tuple[Incomplete, ...]
    glyph_name: str
    glyph_width: int
    def __hash__(self) -> int: ...

class SubsetMap:
    """
    Holds a mapping of used characters and their position in the font's subset

    Characters that must be mapped on their actual unicode must be part of the
    `identities` list during object instantiation. These non-negative values should
    only appear once in the list. `pick()` can be used to get the characters
    corresponding position in the subset. If it's not yet part of the object, a new
    position is acquired automatically. This implementation always tries to return
    the lowest possible representation.
    """

    font: TTFFont
    def __init__(self, font: TTFFont) -> None: ...
    def __len__(self) -> int: ...
    def items(self) -> Generator[Incomplete, None, None]: ...
    def pick(self, unicode: int): ...
    def pick_glyph(self, glyph): ...
    def get_glyph(self, glyph=None, unicode=None, glyph_name=None, glyph_width=None) -> Glyph: ...
    def get_all_glyph_names(self): ...

CORE_FONTS: dict[str, str]
COURIER_FONT: dict[str, int]
CORE_FONTS_CHARWIDTHS: dict[str, dict[str, int]]
