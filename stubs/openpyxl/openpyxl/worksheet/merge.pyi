from _typeshed import Incomplete, Unused
from typing import ClassVar

from openpyxl.cell import _CellOrMergedCell
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.worksheet.worksheet import Worksheet

from .cell_range import CellRange

class MergeCell(CellRange):
    tagname: ClassVar[str]
    # Same as CellRange.coord
    # https://github.com/python/mypy/issues/6700
    @property
    def ref(self) -> str:
        """
        Excel-style representation of the range
        """
    __attrs__: ClassVar[tuple[str, ...]]
    def __init__(self, ref=None) -> None: ...
    def __copy__(self): ...

class MergeCells(Serialisable):
    tagname: ClassVar[str]
    # Overwritten by property below
    # count: Integer
    mergeCell: Incomplete
    __elements__: ClassVar[tuple[str, ...]]
    __attrs__: ClassVar[tuple[str, ...]]
    def __init__(self, count: Unused = None, mergeCell=()) -> None: ...
    @property
    def count(self) -> int: ...

class MergedCellRange(CellRange):
    """
    MergedCellRange stores the border information of a merged cell in the top
    left cell of the merged cell.
    The remaining cells in the merged cell are stored as MergedCell objects and
    get their border information from the upper left cell.
    """

    ws: Worksheet
    start_cell: _CellOrMergedCell
    def __init__(self, worksheet: Worksheet, coord) -> None: ...
    def format(self) -> None:
        """
        Each cell of the merged cell is created as MergedCell if it does not
        already exist.

        The MergedCells at the edge of the merged cell gets its borders from
        the upper left cell.

         - The top MergedCells get the top border from the top left cell.
         - The bottom MergedCells get the bottom border from the top left cell.
         - The left MergedCells get the left border from the top left cell.
         - The right MergedCells get the right border from the top left cell.
        """

    def __contains__(self, coord: str) -> bool: ...
    def __copy__(self): ...
