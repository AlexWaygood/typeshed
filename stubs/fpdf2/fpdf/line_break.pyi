"""
Routines for organizing lines and larger blocks of text, with manual and
automatic line wrapping.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from typing import Final, NamedTuple
from uuid import UUID

from .enums import Align, TextDirection, WrapMode

SOFT_HYPHEN: Final[str]
HYPHEN: Final[str]
SPACE: Final[str]
BREAKING_SPACE_SYMBOLS: Final[list[str]]
BREAKING_SPACE_SYMBOLS_STR: Final[str]
NBSP: Final[str]
NEWLINE: Final[str]
FORM_FEED: Final[str]

class Fragment:
    """
    A fragment of text with font/size/style and other associated information.
    """

    characters: list[str]
    graphics_state: dict[str, Incomplete]
    k: float
    url: str | None
    def __init__(
        self, characters: list[str] | str, graphics_state: dict[str, Incomplete], k: float, link: str | int | None = None
    ) -> None: ...
    @property
    def font(self): ...
    @font.setter
    def font(self, v) -> None: ...
    @property
    def is_ttf_font(self): ...
    @property
    def font_style(self): ...
    @property
    def font_family(self): ...
    @property
    def font_size_pt(self): ...
    @property
    def font_size(self): ...
    @property
    def font_stretching(self): ...
    @property
    def char_spacing(self): ...
    @property
    def text_mode(self): ...
    @property
    def underline(self) -> bool: ...
    @property
    def strikethrough(self) -> bool: ...
    @property
    def draw_color(self): ...
    @property
    def fill_color(self): ...
    @property
    def text_color(self): ...
    @property
    def line_width(self): ...
    @property
    def char_vpos(self): ...
    @property
    def lift(self): ...
    @property
    def string(self) -> str: ...
    @property
    def width(self) -> float: ...
    @property
    def text_shaping_parameters(self): ...
    @property
    def paragraph_direction(self) -> TextDirection: ...
    @property
    def fragment_direction(self) -> TextDirection: ...
    def trim(self, index: int) -> None: ...
    def __eq__(self, other: Fragment) -> bool: ...  # type: ignore[override]
    def get_width(self, start: int = 0, end: int | None = None, chars: str | None = None, initial_cs: bool = True) -> float:
        """
        Return the width of the string with the given font/size/style/etc.

        Args:
            start (int): Index of the start character. Default start of fragment.
            end (int): Index of the end character. Default end of fragment.
            chars (str): Specific text to get the width for (not necessarily the
                same as the contents of the fragment). If given, this takes
                precedence over the start/end arguments.
        """

    def has_same_style(self, other: Fragment) -> bool:
        """Returns if 2 fragments are equivalent other than the characters/string"""

    def get_character_width(self, character: str, print_sh: bool = False, initial_cs: bool = True):
        """
        Return the width of a single character out of the stored text.
        """

    def render_pdf_text(self, frag_ws, current_ws, word_spacing, adjust_x, adjust_y, h): ...
    def render_pdf_text_ttf(self, frag_ws, word_spacing): ...
    def render_with_text_shaping(self, pos_x: float, pos_y: float, h: float, word_spacing: float) -> str: ...
    def render_pdf_text_core(self, frag_ws, current_ws): ...

class TotalPagesSubstitutionFragment(Fragment):
    """
    A special type of text fragment that represents a placeholder for the total number of pages
    in a PDF document.

    A placeholder will be generated during the initial content rendering phase of a PDF document.
    This placeholder is later replaced by the total number of pages in the document when the final
    output is being produced.
    """

    uuid: UUID
    def get_placeholder_string(self) -> str:
        """
        This method returns a placeholder string containing a universally unique identifier (UUID4),
        ensuring that the placeholder is distinct and does not conflict with other placeholders
        within the document.
        """

    def render_text_substitution(self, replacement_text: str) -> str:
        """
        This method is invoked at the output phase. It calls `render_pdf_text()` from the superclass
        to render the fragment with the preserved rendering state (stored in `_render_args` and `_render_kwargs`)
        and insert the final text in place of the placeholder.
        """

class TextLine(NamedTuple):
    """TextLine(fragments, text_width, number_of_spaces, align, height, max_width, trailing_nl, trailing_form_feed, indent)"""

    fragments: tuple[Fragment, ...]
    text_width: float
    number_of_spaces: int
    align: Align
    height: float
    max_width: float
    trailing_nl: bool = False
    trailing_form_feed: bool = False
    indent: float = 0
    def get_ordered_fragments(self) -> tuple[Fragment, ...]: ...

class SpaceHint(NamedTuple):
    """SpaceHint(original_fragment_index, original_character_index, current_line_fragment_index, current_line_character_index, line_width, number_of_spaces)"""

    original_fragment_index: int
    original_character_index: int
    current_line_fragment_index: int
    current_line_character_index: int
    line_width: float
    number_of_spaces: int

class HyphenHint(NamedTuple):
    """HyphenHint(original_fragment_index, original_character_index, current_line_fragment_index, current_line_character_index, line_width, number_of_spaces, curchar, curchar_width, graphics_state, k)"""

    original_fragment_index: int
    original_character_index: int
    current_line_fragment_index: int
    current_line_character_index: int
    line_width: float
    number_of_spaces: int
    curchar: str
    curchar_width: float
    graphics_state: dict[str, Incomplete]
    k: float

class CurrentLine:
    max_width: float
    print_sh: bool
    indent: float
    fragments: list[Fragment]
    height: int
    number_of_spaces: int
    space_break_hint: Incomplete
    hyphen_break_hint: Incomplete
    def __init__(self, max_width: float, print_sh: bool = False, indent: float = 0) -> None:
        """
        Per-line text fragment management for use by MultiLineBreak.
            Args:
                print_sh (bool): If true, a soft-hyphen will be rendered
                    normally, instead of triggering a line break. Default: False
        """

    @property
    def width(self) -> float: ...
    def add_character(
        self,
        character: str,
        character_width: float,
        original_fragment: Fragment,
        original_fragment_index: int,
        original_character_index: int,
        height: float,
        url: str | None = None,
    ) -> None: ...
    def trim_trailing_spaces(self) -> None: ...
    def manual_break(self, align: Align, trailing_nl: bool = False, trailing_form_feed: bool = False) -> TextLine: ...
    def automatic_break_possible(self) -> bool: ...
    def automatic_break(self, align: Align) -> tuple[Incomplete, Incomplete, TextLine]: ...

class MultiLineBreak:
    fragments: Sequence[Fragment]
    get_width: float
    margins: Sequence[float]
    align: Align
    print_sh: bool
    wrapmode: WrapMode
    line_height: float
    skip_leading_spaces: bool
    fragment_index: int
    character_index: int
    idx_last_forced_break: int | None
    first_line_indent: float
    def __init__(
        self,
        fragments: Sequence[Fragment],
        max_width: float | Callable[[float], float],
        margins: Sequence[float],
        align: Align = ...,
        print_sh: bool = False,
        wrapmode: WrapMode = ...,
        line_height: float = 1.0,
        skip_leading_spaces: bool = False,
        first_line_indent: float = 0,
    ) -> None:
        """Accept text as Fragments, to be split into individual lines depending
        on line width and text height.
        Args:
            fragments: A sequence of Fragment()s containing text.
            max_width: Either a fixed width as float or a callback function
                get_width(height). If a function, it gets called with the largest
                height encountered on the current line, and must return the
                applicable width for the line with the given height at the current
                vertical position. The height is relevant in those cases where the
                lateral boundaries of the enclosing TextRegion() are not vertical.
            margins (sequence of floats): The extra clearance that may apply at the beginning
                and/or end of a line (usually either FPDF.c_margin or 0.0 for each side).
            align (Align): The horizontal alignment of the current text block.
            print_sh (bool): If True, a soft-hyphen will be rendered
                normally, instead of triggering a line break. Default: False
            wrapmode (WrapMode): Selects word or character based wrapping.
            line_height (float, optional): A multiplier relative to the font
                size changing the vertical space occupied by a line of text. Default 1.0.
            skip_leading_spaces (bool, optional): On each line, any space characters
                at the beginning will be skipped. Default value: False.
            first_line_indent (float, optional): left spacing before first line of text in paragraph.
        """

    def get_line(self) -> TextLine: ...
