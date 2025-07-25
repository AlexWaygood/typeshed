from _typeshed import Incomplete, SupportsItems
from collections.abc import Iterable
from dataclasses import dataclass
from io import BytesIO
from typing import Literal, overload

from PIL import Image

from .drawing import DeviceGray, DeviceRGB
from .enums import (
    Align,
    CellBordersLayout,
    TableBordersLayout,
    TableCellFillMode,
    TableHeadingsDisplay,
    TableSpan,
    VAlign,
    WrapMode,
)
from .fonts import FontFace
from .fpdf import FPDF
from .image_datastructures import _TextAlign
from .util import Padding

DEFAULT_HEADINGS_STYLE: FontFace

class Table:
    """
    Object that `fpdf.FPDF.table()` yields, used to build a table in the document.
    Detailed usage documentation: https://py-pdf.github.io/fpdf2/Tables.html
    """

    rows: list[Row]

    def __init__(
        self,
        fpdf: FPDF,
        rows: Iterable[str] = (),
        *,
        # Keep in sync with `fpdf.fpdf.FPDF.table`:
        align: str | _TextAlign = "CENTER",
        v_align: str | VAlign = "MIDDLE",
        borders_layout: str | TableBordersLayout = ...,
        cell_fill_color: int | tuple[Incomplete, ...] | DeviceGray | DeviceRGB | None = None,
        cell_fill_mode: str | TableCellFillMode = ...,
        col_widths: int | tuple[int, ...] | None = None,
        first_row_as_headings: bool = True,
        gutter_height: float = 0,
        gutter_width: float = 0,
        headings_style: FontFace = ...,
        line_height: int | None = None,
        markdown: bool = False,
        text_align: str | _TextAlign | tuple[str | _TextAlign, ...] = "JUSTIFY",
        width: int | None = None,
        wrapmode: WrapMode = ...,
        padding: float | Padding | None = None,
        outer_border_width: float | None = None,
        num_heading_rows: int = 1,
        repeat_headings: TableHeadingsDisplay | int = 1,
        min_row_height=None,
    ) -> None:
        """
        Args:
            fpdf (fpdf.FPDF): FPDF current instance
            rows: optional. Sequence of rows (iterable) of str to initiate the table cells with text content
            align (str, fpdf.enums.Align): optional, default to CENTER. Sets the table horizontal position relative to the page,
                when it's not using the full page width
            borders_layout (str, fpdf.enums.TableBordersLayout): optional, default to ALL. Control what cell borders are drawn
            cell_fill_color (float, tuple, fpdf.drawing.DeviceGray, fpdf.drawing.DeviceRGB): optional.
                Defines the cells background color
            cell_fill_mode (str, fpdf.enums.TableCellFillMode): optional. Defines which cells are filled with color in the background
            col_widths (float, tuple): optional. Sets column width. Can be a single number or a sequence of numbers.
                 When `col_widths` is a single number, it is interpreted as a fixed column width in document units.
                 When `col_widths` is provided as an array, the values are considered to be fractions of the full effective page width,
                 meaning that `col_widths=(1, 1, 2)` is strictly equivalent to `col_widths=(25, 25, 50)`.
            first_row_as_headings (bool): optional, default to True. If False, the first row of the table
                is not styled differently from the others
            gutter_height (float): optional vertical space between rows
            gutter_width (float): optional horizontal space between columns
            headings_style (fpdf.fonts.FontFace): optional, default to bold.
                Defines the visual style of the top headings row: size, color, emphasis...
            line_height (number): optional. Defines how much vertical space a line of text will occupy
            markdown (bool): optional, default to False. Enable markdown interpretation of cells textual content
            text_align (str, fpdf.enums.Align, tuple): optional, default to JUSTIFY. Control text alignment inside cells.
            v_align (str, fpdf.enums.VAlign): optional, default to CENTER. Control vertical alignment of cells content
            width (number): optional. Sets the table width
            wrapmode (fpdf.enums.WrapMode): "WORD" for word based line wrapping (default),
                "CHAR" for character based line wrapping.
            padding (number, tuple, Padding): optional. Sets the cell padding. Can be a single number or a sequence of numbers, default:0
                If padding for left and right ends up being non-zero then c_margin is ignored.
            outer_border_width (number): optional. Sets the width of the outer borders of the table.
                Only relevant when borders_layout is ALL or NO_HORIZONTAL_LINES. Otherwise, the border widths are controlled by FPDF.set_line_width()
            num_heading_rows (number): optional. Sets the number of heading rows, default value is 1. If this value is not 1,
                first_row_as_headings needs to be True if num_heading_rows>1 and False if num_heading_rows=0. For backwards compatibility,
                first_row_as_headings is used in case num_heading_rows is 1.
            repeat_headings (fpdf.enums.TableHeadingsDisplay): optional, indicates whether to print table headings on every page, default to 1.
        """

    def row(
        self, cells: Iterable[str] = (), style: FontFace | None = None, v_align: VAlign | str | None = None, min_height=None
    ) -> Row:
        """Adds a row to the table. Returns a `Row` object."""

    def render(self) -> None:
        """This is an internal method called by `fpdf.FPDF.table()` once the table is finished"""

    def get_cell_border(self, i: int, j: int, cell: Cell) -> str | Literal[0, 1]:
        """
        Defines which cell borders should be drawn.
        Returns a string containing some or all of the letters L/R/T/B,
        to be passed to `fpdf.FPDF.multi_cell()`.
        Can be overridden to customize this logic
        """

class Row:
    """Object that `Table.row()` yields, used to build a row in a table"""

    cells: list[Cell]
    style: FontFace
    v_align: VAlign | None
    min_height: Incomplete | None
    def __init__(
        self, table: Table, style: FontFace | None = None, v_align: VAlign | str | None = None, min_height=None
    ) -> None: ...
    @property
    def cols_count(self) -> int: ...
    @property
    def max_rowspan(self) -> int: ...
    def convert_spans(self, active_rowspans: SupportsItems[int, int]) -> tuple[dict[int, int], list[int]]: ...
    @overload
    def cell(
        self,
        text: str = "",
        align: str | Align | None = None,
        v_align: str | VAlign | None = None,
        style: FontFace | None = None,
        img: str | Image.Image | BytesIO | None = None,
        img_fill_width: bool = False,
        colspan: int = 1,
        rowspan: int = 1,
        padding: tuple[float, ...] | None = None,
        link: str | int | None = None,
        border: CellBordersLayout | int = ...,
    ) -> str:
        """
        Adds a cell to the row.

        Args:
            text (str): string content, can contain several lines.
                In that case, the row height will grow proportionally.
            align (str, fpdf.enums.Align): optional text alignment.
            v_align (str, fpdf.enums.VAlign): optional vertical text alignment.
            style (fpdf.fonts.FontFace): optional text style.
            img: optional. Either a string representing a file path to an image,
                an URL to an image, an io.BytesIO, or a instance of `PIL.Image.Image`.
            img_fill_width (bool): optional, defaults to False. Indicates to render the image
                using the full width of the current table column.
            colspan (int): optional number of columns this cell should span.
            rowspan (int): optional number of rows this cell should span.
            padding (tuple): optional padding (left, top, right, bottom) for the cell.
            link (str, int): optional link, either an URL or an integer returned by `FPDF.add_link`, defining an internal link to a page
            border (fpdf.enums.CellBordersLayout): optional cell borders, defaults to `CellBordersLayout.INHERIT`

        """

    @overload
    def cell(
        self,
        text: TableSpan,
        align: str | Align | None = None,
        v_align: str | VAlign | None = None,
        style: FontFace | None = None,
        img: str | Image.Image | BytesIO | None = None,
        img_fill_width: bool = False,
        colspan: int = 1,
        rowspan: int = 1,
        padding: tuple[float, ...] | None = None,
        link: str | int | None = None,
        border: CellBordersLayout | int = ...,
    ) -> TableSpan: ...

@dataclass
class Cell:
    """Internal representation of a table cell"""

    text: str
    align: str | Align | None
    v_align: str | VAlign | None
    style: FontFace | None
    img: str | None
    img_fill_width: bool
    colspan: int
    rowspan: int
    padding: int | tuple[float, ...] | None
    link: str | int | None
    border: CellBordersLayout | None

    def write(self, text, align=None): ...

@dataclass(frozen=True)
class RowLayoutInfo:
    """RowLayoutInfo(height: float, pagebreak_height: float, rendered_heights: dict, merged_heights: list)"""

    height: int
    pagebreak_height: float
    rendered_heights: dict[Incomplete, Incomplete]
    merged_heights: list[Incomplete]

@dataclass(frozen=True)
class RowSpanLayoutInfo:
    """RowSpanLayoutInfo(column: int, start: int, length: int, contents_height: float)"""

    column: int
    start: int
    length: int
    contents_height: float

    def row_range(self) -> range: ...

def draw_box_borders(pdf: FPDF, x1, y1, x2, y2, border: str | Literal[0, 1], fill_color=None) -> None:
    """Draws a box using the provided style - private helper used by table for drawing the cell and table borders.
    Difference between this and rect() is that border can be defined as "L,R,T,B" to draw only some of the four borders;
    compatible with get_border(i,k)

    See Also: rect()
    """
