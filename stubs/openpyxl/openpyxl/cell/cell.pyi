"""Manage individual cells in a spreadsheet.

The Cell class is required to know its value and type, display options,
and any other features of an Excel cell.  Utilities for referencing
cells using Excel's 'A1' column/row nomenclature are also provided.

"""

from _typeshed import ReadableBuffer
from datetime import datetime
from re import Pattern
from typing import Final, Literal, overload

from openpyxl.cell import _CellGetValue, _CellOrMergedCell, _CellSetValue, _TimeTypes
from openpyxl.comments.comments import Comment
from openpyxl.compat.numbers import NUMERIC_TYPES as NUMERIC_TYPES  # cell numeric types
from openpyxl.styles.cell_style import StyleArray
from openpyxl.styles.styleable import StyleableObject
from openpyxl.workbook.child import _WorkbookChild
from openpyxl.worksheet._read_only import ReadOnlyWorksheet
from openpyxl.worksheet.hyperlink import Hyperlink

__docformat__: Final = "restructuredtext en"
TIME_TYPES: Final[tuple[type, ...]]
TIME_FORMATS: Final[dict[type[_TimeTypes], str]]
STRING_TYPES: Final[tuple[type, ...]]
KNOWN_TYPES: Final[tuple[type, ...]]

ILLEGAL_CHARACTERS_RE: Final[Pattern[str]]
ERROR_CODES: Final[tuple[str, ...]]

TYPE_STRING: Final = "s"
TYPE_FORMULA: Final = "f"
TYPE_NUMERIC: Final = "n"
TYPE_BOOL: Final = "b"
TYPE_NULL: Final = "n"
TYPE_INLINE: Final = "inlineStr"
TYPE_ERROR: Final = "e"
TYPE_FORMULA_CACHE_STRING: Final = "str"

VALID_TYPES: Final[tuple[str, ...]]

def get_type(t: type, value: object) -> Literal["n", "s", "d", "f"] | None: ...
def get_time_format(t: _TimeTypes) -> str: ...

class Cell(StyleableObject):
    """Describes cell associated properties.

    Properties of interest include style, type, value, and address.

    """

    row: int
    column: int
    data_type: str
    # row and column are never meant to be None and would lead to errors
    def __init__(
        self,
        worksheet: _WorkbookChild | ReadOnlyWorksheet,
        row: int,
        column: int,
        value: _CellSetValue = None,
        style_array: StyleArray | None = None,
    ) -> None: ...
    @property
    def coordinate(self) -> str:
        """This cell's coordinate (ex. 'A5')"""

    @property
    def col_idx(self) -> int:
        """The numerical index of the column"""

    @property
    def column_letter(self) -> str: ...
    @property
    def encoding(self) -> str: ...
    @property
    def base_date(self) -> datetime: ...
    @overload
    def check_string(self, value: None) -> None:
        """Check string coding, length, and line break character"""

    @overload
    def check_string(self, value: str | ReadableBuffer) -> str: ...
    def check_error(self, value: object) -> str:
        """Tries to convert Error" else N/A"""

    @property
    def value(self) -> _CellGetValue:
        """Get or set the value held in the cell.

        :type: depends on the value (string, float, int or
            :class:`datetime.datetime`)
        """

    @value.setter
    def value(self, value: _CellSetValue) -> None: ...
    @property
    def internal_value(self) -> _CellGetValue:
        """Always returns the value for excel."""

    @property
    def hyperlink(self) -> Hyperlink | None:
        """Return the hyperlink target or an empty string"""

    @hyperlink.setter
    def hyperlink(self, val: Hyperlink | str | None) -> None: ...
    @property
    def is_date(self) -> bool:
        """True if the value is formatted as a date

        :type: bool
        """

    def offset(self, row: int = 0, column: int = 0) -> _CellOrMergedCell:
        """Returns a cell location relative to this cell.

        :param row: number of rows to offset
        :type row: int

        :param column: number of columns to offset
        :type column: int

        :rtype: :class:`openpyxl.cell.Cell`
        """

    @property
    def comment(self) -> Comment | None:
        """Returns the comment associated with this cell

        :type: :class:`openpyxl.comments.Comment`
        """

    @comment.setter
    def comment(self, value: Comment | None) -> None: ...

class MergedCell(StyleableObject):
    """
    Describes the properties of a cell in a merged cell and helps to
    display the borders of the merged cell.

    The value of a MergedCell is always None.
    """

    data_type: str
    comment: Comment | None
    hyperlink: Hyperlink | None
    row: int | None
    column: int | None
    def __init__(
        self, worksheet: _WorkbookChild | ReadOnlyWorksheet, row: int | None = None, column: int | None = None
    ) -> None: ...
    # Same as Cell.coordinate
    # https://github.com/python/mypy/issues/6700
    @property
    def coordinate(self) -> str:
        """This cell's coordinate (ex. 'A5')"""
    # The value of a MergedCell is always None.
    value: None

def WriteOnlyCell(ws: _WorkbookChild | ReadOnlyWorksheet, value: str | float | datetime | None = None) -> Cell: ...
