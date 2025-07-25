from _typeshed import Incomplete, Unused
from collections.abc import Iterator
from typing import ClassVar, Literal

from openpyxl.descriptors.base import Alias, Bool, Convertible, _ConvertibleToBool, _ConvertibleToMultiCellRange
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.worksheet.cell_range import CellRange, MultiCellRange

class ConditionalFormatting(Serialisable):
    tagname: ClassVar[str]
    sqref: Convertible[MultiCellRange, Literal[False]]
    cells: Alias
    pivot: Bool[Literal[True]]
    cfRule: Incomplete
    rules: Alias
    def __init__(
        self, sqref: _ConvertibleToMultiCellRange = (), pivot: _ConvertibleToBool | None = None, cfRule=(), extLst: Unused = None
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __contains__(self, coord: str | CellRange) -> bool:
        """
        Check whether a certain cell is affected by the formatting
        """

class ConditionalFormattingList:
    """Conditional formatting rules."""

    max_priority: int
    def __init__(self) -> None: ...
    def add(self, range_string, cfRule) -> None:
        """Add a rule such as ColorScaleRule, FormulaRule or CellIsRule

        The priority will be added automatically.
        """

    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[ConditionalFormatting]: ...
    def __getitem__(self, key):
        """
        Get the rules for a cell range
        """

    def __delitem__(self, key) -> None: ...
    def __setitem__(self, key, rule) -> None:
        """
        Add a rule for a cell range
        """
