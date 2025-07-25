"""
HTML renderer

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete, SupportsKeysAndGetItem
from collections.abc import Callable, Iterable, Mapping
from html.parser import HTMLParser
from logging import Logger
from typing import ClassVar, Final, Literal
from typing_extensions import TypeAlias

from fpdf import FPDF

from .enums import TextEmphasis
from .fonts import FontFace
from .table import Row, Table

__author__: Final[str]
__copyright__: Final[str]

_OLType: TypeAlias = Literal["1", "a", "A", "I", "i"]

LOGGER: Logger
BULLET_WIN1252: Final[str]
DEGREE_WIN1252: Final[str]
HEADING_TAGS: Final[tuple[str, ...]]
DEFAULT_TAG_STYLES: Final[dict[str, FontFace]]
INLINE_TAGS: Final[tuple[str, ...]]
BLOCK_TAGS: Final[tuple[str, ...]]

COLOR_DICT: Final[dict[str, str]]

def color_as_decimal(color: str | None = "#000000") -> tuple[int, int, int] | None:
    """
    Convert a web color name to a (R, G, B) color tuple.
    cf. https://en.wikipedia.org/wiki/Web_colors#HTML_color_names
    """

def parse_css_style(style_attr: str) -> dict[str, str]:
    """Parse `style="..."` HTML attributes, and return a dict of key-value"""

class HTML2FPDF(HTMLParser):
    """Render basic HTML to FPDF"""

    HTML_UNCLOSED_TAGS: ClassVar[tuple[str, ...]]
    TABLE_LINE_HEIGHT: ClassVar[float]

    pdf: FPDF
    image_map: Callable[[str], str]
    ul_bullet_char: str
    li_prefix_color: tuple[int, int, int]
    warn_on_tags_not_matching: bool

    font_family: str
    font_size_pt: float
    font_emphasis: TextEmphasis
    font_color: tuple[int, int, int]

    style_stack: list[FontFace]
    h: float
    follows_trailing_space: bool
    follows_heading: bool
    href: str
    align: str
    indent: int
    line_height_stack: list[Incomplete]
    ol_type: list[_OLType]
    bullet: list[Incomplete]
    heading_level: Incomplete | None
    render_title_tag: bool
    table_line_separators: bool
    table: Table | None
    table_row: Row | None
    tr: dict[str, str] | None
    td_th: dict[str, str] | None
    tag_indents: dict[str, int]
    tag_styles: dict[str, FontFace]

    def __init__(
        self,
        pdf: FPDF,
        image_map: Callable[[str], str] | None = None,
        li_tag_indent: int | None = None,
        dd_tag_indent: int | None = None,
        table_line_separators: bool = False,
        ul_bullet_char: str = "\x95",
        li_prefix_color: tuple[int, int, int] = (190, 0, 0),
        heading_sizes: SupportsKeysAndGetItem[str, int] | Iterable[tuple[str, int]] | None = None,
        pre_code_font: str | None = None,
        warn_on_tags_not_matching: bool = True,
        tag_indents: dict[str, int] | None = None,
        tag_styles: Mapping[str, FontFace] | None = None,
        font_family: str = "times",
        render_title_tag: bool = False,
    ) -> None:
        """
        Args:
            pdf (FPDF): an instance of `fpdf.FPDF`
            image_map (function): an optional one-argument function that map `<img>` "src" to new image URLs
            li_tag_indent (int): [**DEPRECATED since v2.7.9**]
                numeric indentation of `<li>` elements - Set `tag_styles` instead
            dd_tag_indent (int): [**DEPRECATED since v2.7.9**]
                numeric indentation of `<dd>` elements - Set `tag_styles` instead
            table_line_separators (bool): enable horizontal line separators in `<table>`. Defaults to `False`.
            ul_bullet_char (str): bullet character preceding `<li>` items in `<ul>` lists.
                Can also be configured using the HTML `type` attribute of `<ul>` tags.
            li_prefix_color (tuple, str, fpdf.drawing.DeviceCMYK, fpdf.drawing.DeviceGray, fpdf.drawing.DeviceRGB): color for bullets
                or numbers preceding `<li>` tags. This applies to both `<ul>` & `<ol>` lists.
            heading_sizes (dict): [**DEPRECATED since v2.7.9**]
                font size per heading level names ("h1", "h2"...) - Set `tag_styles` instead
            pre_code_font (str): [**DEPRECATED since v2.7.9**]
                font to use for `<pre>` & `<code>` blocks - Set `tag_styles` instead
            warn_on_tags_not_matching (bool): control warnings production for unmatched HTML tags. Defaults to `True`.
            tag_indents (dict): [**DEPRECATED since v2.8.0**]
                mapping of HTML tag names to numeric values representing their horizontal left indentation. - Set `tag_styles` instead
            tag_styles (dict[str, fpdf.fonts.TextStyle]): mapping of HTML tag names to `fpdf.TextStyle` or `fpdf.FontFace` instances
            font_family (str): optional font family. Default to Times.
            render_title_tag (bool): Render the document <title> at the beginning of the PDF. Default to False.
        """

    def handle_data(self, data) -> None: ...
    def handle_starttag(self, tag, attrs) -> None: ...
    def handle_endtag(self, tag) -> None: ...
    def put_link(self, text) -> None:
        """Insert a hyperlink"""

    def render_toc(self, pdf, outline) -> None:
        """This method can be overridden by subclasses to customize the Table of Contents style."""

    def error(self, message: str) -> None: ...

def ul_prefix(ul_type: str) -> str: ...
def ol_prefix(ol_type: _OLType, index: int) -> str: ...

class HTMLMixin:
    """
    [**DEPRECATED since v2.6.0**]
    You can now directly use the `FPDF.write_html()` method
    """

    def __init__(self, *args, **kwargs) -> None: ...
