"""
Collection of utilities used within the package and also available for client code
"""

from collections.abc import Generator
from re import Pattern
from typing import Final
from typing_extensions import TypeAlias

# "1:1" | "A1:A1" | "A:A"
_RangeBoundariesTuple: TypeAlias = tuple[None, int, None, int] | tuple[int, int, int, int] | tuple[int, None, int, None]

COORD_RE: Final[Pattern[str]]
COL_RANGE: Final = "[A-Z]{1,3}:[A-Z]{1,3}:"
ROW_RANGE: Final = r"\d+:\d+:"
RANGE_EXPR: Final[str]
ABSOLUTE_RE: Final[Pattern[str]]
SHEET_TITLE: Final[str]
SHEETRANGE_RE: Final[Pattern[str]]

def get_column_interval(start: str | int, end: str | int) -> list[str]:
    """
    Given the start and end columns, return all the columns in the series.

    The start and end columns can be either column letters or 1-based
    indexes.
    """

def coordinate_from_string(coord_string: str) -> tuple[str, int]:
    """Convert a coordinate string like 'B12' to a tuple ('B', 12)"""

def absolute_coordinate(coord_string: str) -> str:
    """Convert a coordinate to an absolute coordinate string (B12 -> $B$12)"""

def get_column_letter(col_idx: int) -> str:
    """
    Convert decimal column position to its ASCII (base 26) form.

    Because column indices are 1-based, strides are actually pow(26, n) + 26
    Hence, a correction is applied between pow(26, n) and pow(26, 2) + 26 to
    prevent and additional column letter being prepended

    "A" == 1 == pow(26, 0)
    "Z" == 26 == pow(26, 0) + 26 // decimal equivalent 10
    "AA" == 27 == pow(26, 1) + 1
    "ZZ" == 702 == pow(26, 2) + 26 // decimal equivalent 100
    """

def column_index_from_string(col: str) -> int:
    """
    Convert ASCII column name (base 26) to decimal with 1-based index

    Characters represent descending multiples of powers of 26

    "AFZ" == 26 * pow(26, 0) + 6 * pow(26, 1) + 1 * pow(26, 2)
    """

def range_boundaries(range_string: str) -> _RangeBoundariesTuple:
    """
    Convert a range string into a tuple of boundaries:
    (min_col, min_row, max_col, max_row)
    Cell coordinates will be converted into a range with the cell at both end
    """

def rows_from_range(range_string: str) -> Generator[tuple[str, ...], None, None]:
    """
    Get individual addresses for every cell in a range.
    Yields one row at a time.
    """

def cols_from_range(range_string: str) -> Generator[tuple[str, ...], None, None]:
    """
    Get individual addresses for every cell in a range.
    Yields one row at a time.
    """

def coordinate_to_tuple(coordinate: str) -> tuple[int, int]:
    """
    Convert an Excel style coordinate to (row, column) tuple
    """

def range_to_tuple(range_string: str) -> tuple[str, _RangeBoundariesTuple]:
    """
    Convert a worksheet range to the sheetname and maximum and minimum
    coordinate indices
    """

def quote_sheetname(sheetname: str) -> str:
    """
    Add quotes around sheetnames if they contain spaces.
    """
