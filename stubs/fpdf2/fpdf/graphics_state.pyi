"""
Mixin class for managing a stack of graphics state variables.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from typing import Any, ClassVar, Final, Literal, TypedDict, type_check_only

from .drawing import DeviceGray, DeviceRGB
from .enums import TextMode
from .fonts import FontFace

@type_check_only
class _TextShaping(TypedDict):
    use_shaping_engine: bool
    features: dict[str, bool]
    direction: Literal["ltr", "rtl"]
    script: str | None
    language: str | None
    fragment_direction: Literal["L", "R"] | None
    paragraph_direction: Literal["L", "R"] | None

class GraphicsStateMixin:
    """Mixin class for managing a stack of graphics state variables.

    To the subclassing library and its users, the variables look like
    normal instance attributes. But by the magic of properties, we can
    push and pop levels as needed, and users will always see and modify
    just the current version.

    This class is mixed in by fpdf.FPDF(), and is not meant to be used
    directly by user code.
    """

    DEFAULT_DRAW_COLOR: ClassVar[DeviceGray]
    DEFAULT_FILL_COLOR: ClassVar[DeviceGray]
    DEFAULT_TEXT_COLOR: ClassVar[DeviceGray]
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def draw_color(self) -> DeviceGray | DeviceRGB: ...
    @draw_color.setter
    def draw_color(self, v: DeviceGray | DeviceRGB) -> None: ...
    @property
    def fill_color(self) -> DeviceGray | DeviceRGB: ...
    @fill_color.setter
    def fill_color(self, v: DeviceGray | DeviceRGB) -> None: ...
    @property
    def text_color(self) -> DeviceGray | DeviceRGB: ...
    @text_color.setter
    def text_color(self, v: DeviceGray | DeviceRGB) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, v: bool) -> None: ...
    @property
    def strikethrough(self) -> bool: ...
    @strikethrough.setter
    def strikethrough(self, v: bool) -> None: ...
    @property
    def font_style(self) -> str: ...
    @font_style.setter
    def font_style(self, v: str) -> None: ...
    @property
    def font_stretching(self) -> float: ...
    @font_stretching.setter
    def font_stretching(self, v: float) -> None: ...
    @property
    def char_spacing(self) -> float: ...
    @char_spacing.setter
    def char_spacing(self, v: float) -> None: ...
    @property
    def font_family(self) -> str: ...
    @font_family.setter
    def font_family(self, v: str) -> None: ...
    @property
    def font_size_pt(self) -> float: ...
    @font_size_pt.setter
    def font_size_pt(self, v: float) -> None: ...
    @property
    def font_size(self) -> float: ...
    @font_size.setter
    def font_size(self, v: float) -> None: ...
    @property
    def current_font(self) -> dict[str, Any]: ...
    @current_font.setter
    def current_font(self, v: dict[str, Any]) -> None: ...
    @property
    def current_font_is_set_on_page(self) -> bool: ...
    @current_font_is_set_on_page.setter
    def current_font_is_set_on_page(self, v: bool) -> None: ...
    @property
    def dash_pattern(self) -> dict[str, float]: ...
    @dash_pattern.setter
    def dash_pattern(self, v: dict[str, float]) -> None: ...
    @property
    def line_width(self) -> float: ...
    @line_width.setter
    def line_width(self, v: float) -> None: ...
    @property
    def text_mode(self) -> TextMode: ...
    @text_mode.setter
    def text_mode(self, v: int | str) -> None: ...
    @property
    def char_vpos(self):
        """
        Return vertical character position relative to line.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @char_vpos.setter
    def char_vpos(self, v) -> None: ...
    @property
    def sub_scale(self):
        """
        Return scale factor for subscript text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @sub_scale.setter
    def sub_scale(self, v) -> None: ...
    @property
    def sup_scale(self):
        """
        Return scale factor for superscript text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @sup_scale.setter
    def sup_scale(self, v) -> None: ...
    @property
    def nom_scale(self):
        """
        Return scale factor for nominator text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @nom_scale.setter
    def nom_scale(self, v) -> None: ...
    @property
    def denom_scale(self):
        """
        Return scale factor for denominator text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @denom_scale.setter
    def denom_scale(self, v) -> None: ...
    @property
    def sub_lift(self):
        """
        Return lift factor for subscript text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @sub_lift.setter
    def sub_lift(self, v) -> None: ...
    @property
    def sup_lift(self):
        """
        Return lift factor for superscript text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @sup_lift.setter
    def sup_lift(self, v) -> None: ...
    @property
    def nom_lift(self):
        """
        Return lift factor for nominator text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @nom_lift.setter
    def nom_lift(self, v) -> None: ...
    @property
    def denom_lift(self):
        """
        Return lift factor for denominator text.
        ([docs](../TextStyling.html#subscript-superscript-and-fractional-numbers))
        """

    @denom_lift.setter
    def denom_lift(self, v) -> None: ...
    @property
    def text_shaping(self) -> _TextShaping | None: ...
    @text_shaping.setter
    def text_shaping(self, v: _TextShaping | None) -> None: ...
    def font_face(self) -> FontFace:
        """
        Return a `fpdf.fonts.FontFace` instance
        representing a subset of properties of this GraphicsState.
        """

__pdoc__: Final[dict[str, bool]]
