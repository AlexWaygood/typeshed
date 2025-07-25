from _typeshed import SupportsWrite
from array import array
from collections.abc import Callable, Sequence
from typing import Any, Final, Literal, overload

from .biffh import *
from .book import Book
from .formatting import XF
from .timemachine import *

OBJ_MSO_DEBUG: Final[int]

class MSODrawing(BaseObject): ...
class MSObj(BaseObject): ...
class MSTxo(BaseObject): ...

class Note(BaseObject):
    """
    Represents a user "comment" or "note".
    Note objects are accessible through :attr:`Sheet.cell_note_map`.

    .. versionadded:: 0.7.2
    """

    author: str
    col_hidden: int
    colx: int
    rich_text_runlist: list[tuple[str, int]] | None
    row_hidden: int
    rowx: int
    show: int
    text: str

class Hyperlink(BaseObject):
    """
    Contains the attributes of a hyperlink.
    Hyperlink objects are accessible through :attr:`Sheet.hyperlink_list`
    and :attr:`Sheet.hyperlink_map`.

    .. versionadded:: 0.7.2
    """

    frowx: int | None
    lrowx: int | None
    fcolx: int | None
    lcolx: int | None
    type: str | None
    url_or_path: bytes | str | None
    desc: str | None
    target: str | None
    textmark: str | None
    quicktip: str | None

def unpack_RK(rk_str: bytes) -> float: ...

cellty_from_fmtty: Final[dict[int, int]]
ctype_text: Final[dict[int, str]]

class Cell(BaseObject):
    """
    Contains the data for one cell.

    .. warning::
      You don't call this class yourself. You access :class:`Cell` objects
      via methods of the :class:`Sheet` object(s) that you found in the
      :class:`~xlrd.book.Book` object that was returned when you called
      :func:`~xlrd.open_workbook`

    Cell objects have three attributes: ``ctype`` is an int, ``value``
    (which depends on ``ctype``) and ``xf_index``.
    If ``formatting_info`` is not enabled when the workbook is opened,
    ``xf_index`` will be ``None``.

    The following table describes the types of cells and how their values
    are represented in Python.

    .. raw:: html

        <table border="1" cellpadding="7">
        <tr>
        <th>Type symbol</th>
        <th>Type number</th>
        <th>Python value</th>
        </tr>
        <tr>
        <td>XL_CELL_EMPTY</td>
        <td align="center">0</td>
        <td>empty string ''</td>
        </tr>
        <tr>
        <td>XL_CELL_TEXT</td>
        <td align="center">1</td>
        <td>a Unicode string</td>
        </tr>
        <tr>
        <td>XL_CELL_NUMBER</td>
        <td align="center">2</td>
        <td>float</td>
        </tr>
        <tr>
        <td>XL_CELL_DATE</td>
        <td align="center">3</td>
        <td>float</td>
        </tr>
        <tr>
        <td>XL_CELL_BOOLEAN</td>
        <td align="center">4</td>
        <td>int; 1 means TRUE, 0 means FALSE</td>
        </tr>
        <tr>
        <td>XL_CELL_ERROR</td>
        <td align="center">5</td>
        <td>int representing internal Excel codes; for a text representation,
        refer to the supplied dictionary error_text_from_code</td>
        </tr>
        <tr>
        <td>XL_CELL_BLANK</td>
        <td align="center">6</td>
        <td>empty string ''. Note: this type will appear only when
        open_workbook(..., formatting_info=True) is used.</td>
        </tr>
        </table>
    """

    ctype: int
    value: str
    xf_index: int | None
    def __init__(self, ctype: int, value: str, xf_index: int | None = None) -> None: ...

empty_cell: Final[Cell]

class Colinfo(BaseObject):
    """
    Width and default formatting information that applies to one or
    more columns in a sheet. Derived from ``COLINFO`` records.

    Here is the default hierarchy for width, according to the OOo docs:

      In BIFF3, if a ``COLINFO`` record is missing for a column,
      the width specified in the record ``DEFCOLWIDTH`` is used instead.

      In BIFF4-BIFF7, the width set in this ``COLINFO`` record is only used,
      if the corresponding bit for this column is cleared in the ``GCW``
      record, otherwise the column width set in the ``DEFCOLWIDTH`` record
      is used (the ``STANDARDWIDTH`` record is always ignored in this case [#f1]_).

      In BIFF8, if a ``COLINFO`` record is missing for a column,
      the width specified in the record ``STANDARDWIDTH`` is used.
      If this ``STANDARDWIDTH`` record is also missing,
      the column width of the record ``DEFCOLWIDTH`` is used instead.

    .. [#f1] The docs on the ``GCW`` record say this:

      If a bit is set, the corresponding column uses the width set in the
      ``STANDARDWIDTH`` record. If a bit is cleared, the corresponding column
      uses the width set in the ``COLINFO`` record for this column.

      If a bit is set, and the worksheet does not contain the ``STANDARDWIDTH``
      record, or if the bit is cleared, and the worksheet does not contain the
      ``COLINFO`` record, the ``DEFCOLWIDTH`` record of the worksheet will be
      used instead.

    xlrd goes with the GCW version of the story.
    Reference to the source may be useful: see
    :meth:`Sheet.computed_column_width`.

    .. versionadded:: 0.6.1
    """

    width: int
    xf_index: int
    hidden: int
    bit1_flag: int
    outline_level: int
    collapsed: int

class Rowinfo(BaseObject):
    """
    Height and default formatting information that applies to a row in a sheet.
    Derived from ``ROW`` records.

    .. versionadded:: 0.6.1
    """

    height: int | None
    has_default_height: int | None
    outline_level: int | None
    outline_group_starts_ends: int | None
    hidden: int | None
    height_mismatch: int | None
    has_default_xf_index: int | None
    xf_index: int | None
    additional_space_above: int | None
    additional_space_below: int | None
    def __init__(self) -> None: ...
    def __getstate__(self) -> tuple[int | None, ...]: ...
    def __setstate__(self, state: tuple[int | None, ...]) -> None: ...

class Sheet(BaseObject):
    """
    Contains the data for one worksheet.

    In the cell access functions, ``rowx`` is a row index, counting from
    zero, and ``colx`` is a column index, counting from zero.
    Negative values for row/column indexes and slice positions are supported in
    the expected fashion.

    For information about cell types and cell values, refer to the documentation
    of the :class:`Cell` class.

    .. warning::

      You don't instantiate this class yourself. You access :class:`Sheet`
      objects via the :class:`~xlrd.book.Book` object that
      was returned when you called :func:`xlrd.open_workbook`.
    """

    name: str
    book: Book | None
    nrows: int
    ncols: int
    colinfo_map: dict[int, Colinfo]
    rowinfo_map: dict[int, Rowinfo]
    col_label_ranges: list[tuple[int, int, int, int]]
    row_label_ranges: list[tuple[int, int, int, int]]
    merged_cells: list[tuple[int, int, int, int]]
    rich_text_runlist_map: dict[tuple[int, int], list[tuple[int, int]]]
    defcolwidth: float | None
    standardwidth: float | None
    default_row_height: int | None
    default_row_height_mismatch: int | None
    default_row_hidden: int | None
    default_additional_space_above: int | None
    default_additional_space_below: int | None
    visibility: Literal[0, 1, 2]
    gcw: tuple[int, ...]
    hyperlink_list: list[Hyperlink]
    hyperlink_map: dict[tuple[int, int], Hyperlink]
    cell_note_map: dict[tuple[int, int], Note]
    vert_split_pos: int
    horz_split_pos: int
    horz_split_first_visible: int
    vert_split_first_visible: int
    split_active_pane: int
    has_pane_record: int
    horizontal_page_breaks: list[tuple[int, int, int]]
    vertical_page_breaks: list[tuple[int, int, int]]
    biff_version: int
    logfile: SupportsWrite[str]
    bt: array[int]
    bf: array[int]
    number: int
    verbosity: int
    formatting_info: bool
    ragged_rows: bool
    put_cell: Callable[[int, int, int | None, str, int | None], None]
    first_visible_rowx: int
    first_visible_colx: int
    gridline_colour_index: int
    gridline_colour_rgb: tuple[int, int, int] | None
    cooked_page_break_preview_mag_factor: int
    cooked_normal_view_mag_factor: int
    cached_page_break_preview_mag_factor: int
    cached_normal_view_mag_factor: int
    scl_mag_factor: int | None
    utter_max_rows: int
    utter_max_cols: int
    def __init__(self, book: Book, position: int, name: str, number: int) -> None: ...
    def cell(self, rowx: int, colx: int) -> Cell:
        """
        :class:`Cell` object in the given row and column.
        """

    def cell_value(self, rowx: int, colx: int) -> str:
        """Value of the cell in the given row and column."""

    def cell_type(self, rowx: int, colx: int) -> int:
        """
        Type of the cell in the given row and column.

        Refer to the documentation of the :class:`Cell` class.
        """

    def cell_xf_index(self, rowx: int, colx: int) -> int:
        """
        XF index of the cell in the given row and column.
        This is an index into :attr:`~xlrd.book.Book.xf_list`.

        .. versionadded:: 0.6.1
        """

    def row_len(self, rowx: int) -> int:
        """
        Returns the effective number of cells in the given row. For use with
        ``open_workbook(ragged_rows=True)`` which is likely to produce rows
        with fewer than :attr:`~Sheet.ncols` cells.

        .. versionadded:: 0.7.2
        """

    def row(self, rowx: int) -> list[Cell]:
        """
        Returns a sequence of the :class:`Cell` objects in the given row.
        """

    @overload
    def __getitem__(self, item: int) -> list[Cell]:
        """
        Takes either rowindex or (rowindex, colindex) as an index,
        and returns either row or cell respectively.
        """

    @overload
    def __getitem__(self, item: tuple[int, int]) -> Cell: ...
    def get_rows(self) -> tuple[list[Cell], ...]:
        """Returns a generator for iterating through each row."""
    __iter__ = get_rows
    def row_types(self, rowx: int, start_colx: int = 0, end_colx: int | None = None) -> Sequence[int]:
        """
        Returns a slice of the types of the cells in the given row.
        """

    def row_values(self, rowx: int, start_colx: int = 0, end_colx: int | None = None) -> Sequence[str]:
        """
        Returns a slice of the values of the cells in the given row.
        """

    def row_slice(self, rowx: int, start_colx: int = 0, end_colx: int | None = None) -> list[Cell]:
        """
        Returns a slice of the :class:`Cell` objects in the given row.
        """

    def col_slice(self, colx: int, start_rowx: int = 0, end_rowx: int | None = None) -> list[Cell]:
        """
        Returns a slice of the :class:`Cell` objects in the given column.
        """

    def col_values(self, colx: int, start_rowx: int = 0, end_rowx: int | None = None) -> list[str]:
        """
        Returns a slice of the values of the cells in the given column.
        """

    def col_types(self, colx: int, start_rowx: int = 0, end_rowx: int | None = None) -> list[int]:
        """
        Returns a slice of the types of the cells in the given column.
        """
    col = col_slice
    def tidy_dimensions(self) -> None: ...
    def put_cell_ragged(self, rowx: int, colx: int, ctype: int | None, value: str, xf_index: int | None) -> None: ...
    def put_cell_unragged(self, rowx: int, colx: int, ctype: int | None, value: str, xf_index: int | None) -> None: ...
    def read(self, bk: Book) -> Literal[1]: ...
    def string_record_contents(self, data: bytes) -> str | None: ...
    def update_cooked_mag_factors(self) -> None: ...
    def fixed_BIFF2_xfindex(self, cell_attr: bytes, rowx: int, colx: int, true_xfx: int | None = None) -> int: ...
    def insert_new_BIFF20_xf(self, cell_attr: bytes, style: int = 0) -> int: ...
    def fake_XF_from_BIFF20_cell_attr(self, cell_attr: bytes, style: int = 0) -> XF: ...
    def req_fmt_info(self) -> None: ...
    def computed_column_width(self, colx: int) -> float:
        """
        Determine column display width.

        :param colx:
          Index of the queried column, range 0 to 255.
          Note that it is possible to find out the width that will be used to
          display columns with no cell information e.g. column IV (colx=255).

        :return:
          The column width that will be used for displaying
          the given column by Excel, in units of 1/256th of the width of a
          standard character (the digit zero in the first font).

        .. versionadded:: 0.6.1
        """

    def handle_hlink(self, data: bytes) -> None: ...
    def handle_quicktip(self, data: bytes) -> None: ...
    def handle_msodrawingetc(self, recid: Any, data_len: int, data: bytes) -> None: ...
    def handle_obj(self, data: bytes) -> MSObj | None: ...
    def handle_note(self, data: bytes, txos: dict[int, MSTxo]) -> None: ...
    def handle_txo(self, data: bytes) -> MSTxo | None: ...
    def handle_feat11(self, data: bytes) -> None: ...
