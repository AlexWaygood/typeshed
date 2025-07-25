"""
Tables are created by passing the constructor a tuple of column widths, a tuple of row heights and the data in
row order. Drawing of the table can be controlled by using a TableStyle instance. This allows control of the
color and weight of the lines (if any), and the font, alignment and padding of the text.

None values in the sequence of row heights or column widths, mean that the corresponding rows
or columns should be automatically sized.

All the cell values should be convertible to strings; embedded newline '\\n' characters
cause the value to wrap (ie are like a traditional linefeed).

See the test output from running this module as a script for a discussion of the method for constructing
tables and table styles.
"""

from _typeshed import Incomplete
from abc import abstractmethod
from collections.abc import Collection, Iterable, Sequence
from typing import Any, Literal, overload
from typing_extensions import TypeAlias, Unpack

from reportlab.lib.colors import Color
from reportlab.lib.styles import PropertySet
from reportlab.lib.utils import _UNSET_
from reportlab.platypus.flowables import Flowable, _HAlignment, _VAlignment

__all__ = ("Table", "TableStyle", "CellStyle", "LongTable")

_Color: TypeAlias = Color | list[float] | tuple[float, float, float, float] | tuple[float, float, float] | str | int
# TODO: consider creating a tagged union of all the possible commands, although
#       this would restrict us to passing cmds to TableStyle.__init__ in a tuple
#       since a list would not be able to be inferred correctly
#       All commands are a tuple with a str opcode as the first element, followed
#       by the arguments for that command. Most commands start with two positions
#       indicating the cell-range affected by the command, the only exception is
#       the ROUNDEDCORNERS command which applies to the whole table always.
_SpecialRow: TypeAlias = Literal["splitfirst", "splitlast", "inrowsplitstart", "inrowsplitend"]
_TableSectionCommand: TypeAlias = tuple[str, tuple[int | _SpecialRow, int], tuple[int, int], Unpack[tuple[Any, ...]]]
_CornerRadii: TypeAlias = tuple[float, float, float, float] | list[float]
_RoundedCornersTableCommand: TypeAlias = tuple[Literal["ROUNDEDCORNERS"], _CornerRadii | None]
_TableCommand: TypeAlias = _TableSectionCommand | _RoundedCornersTableCommand

class CellStyle(PropertySet):
    name: str
    fontname: str
    fontsize: float
    leading: float
    leftPadding: float
    rightPadding: float
    topPadding: float
    bottomPadding: float
    firstLineIndent: float
    color: _Color
    alignment: Literal["LEFT", "CENTER", "CENTRE", "RIGHT", "DECIMAL"]
    background: _Color
    valign: Literal["TOP", "MIDDLE", "BOTTOM"]
    href: str | None
    direction: str | None
    shaping: Incomplete | None
    destination: Incomplete | None
    def __init__(self, name: str, parent: CellStyle | None = None) -> None: ...
    def copy(self, result: CellStyle | None = None) -> CellStyle: ...

class TableStyle:
    # TODO: Add TypedDict for Table properties that can be set through the style
    def __init__(self, cmds: Iterable[_TableCommand] | None = None, parent: TableStyle | None = None, **kw) -> None: ...
    @overload
    def add(self, *cmd: Unpack[_TableSectionCommand]) -> None: ...
    @overload
    def add(self, *cmd: Unpack[_RoundedCornersTableCommand]) -> None: ...
    def getCommands(self) -> list[_TableCommand]: ...

class Table(Flowable):
    ident: str | None
    repeatRows: int
    repeatCols: int
    splitByRow: int
    splitInRow: int
    spaceBefore: float
    spaceAfter: float
    def __init__(
        self,
        # NOTE: Technically only list or tuple works but lack of covariance
        #       on list makes this too annoying
        data: Sequence[list[Any] | tuple[Any, ...]],
        colWidths: Sequence[float | str | None] | float | str | None = None,
        rowHeights: Sequence[float | None] | float | None = None,
        style: TableStyle | Iterable[_TableCommand] | None = None,
        # docs say list/tuple, but the implementation allows any collection
        repeatRows: int | Collection[int] = 0,
        repeatCols: int | Collection[int] = 0,
        splitByRow: int = 1,
        splitInRow: int = 0,
        emptyTableAction: Literal["error", "indicate", "ignore"] | None = None,
        ident: str | None = None,
        hAlign: _HAlignment | None = None,
        vAlign: _VAlignment | None = None,
        normalizedData: int = 0,
        cellStyles: Sequence[Sequence[CellStyle]] | None = None,
        rowSplitRange: tuple[int, int] | None = None,
        spaceBefore: float | None = None,
        spaceAfter: float | None = None,
        longTableOptimize=None,
        minRowHeights: Sequence[float] | None = None,
        cornerRadii: _CornerRadii | _UNSET_ | None = ...,
        renderCB: TableRenderCB | None = None,
    ) -> None: ...
    def identity(self, maxLen: int | None = 30) -> str:
        """Identify our selves as well as possible"""

    def normalizeData(self, data: Iterable[Iterable[Any]]) -> list[list[Any]]:
        """Takes a block of input data (list of lists etc.) and
        - coerces unicode strings to non-unicode UTF8
        - coerces nulls to ''
        -

        """

    def minWidth(self) -> float: ...
    def setStyle(self, tblstyle: TableStyle | Iterable[_TableCommand]) -> None: ...
    def normCellRange(self, sc: int, ec: int, sr: int, er: int) -> tuple[int, int, int, int]:
        """ensure cell range ends are with the table bounds"""

    def onSplit(self, T: Table, byRow: int = 1) -> None:
        """
        This method will be called when the Table is split.
        Special purpose tables can override to do special stuff.
        """

    def draw(self) -> None: ...

class LongTable(Table):
    """Henning von Bargen's changes will be active"""

class TableRenderCB:
    """table render callback abstract base klass to be called in Table.draw"""

    def __call__(self, T: Table, cmd: str, *args: Any) -> None: ...
    @abstractmethod
    def startTable(self, T: Table) -> None: ...
    @abstractmethod
    def startBG(self, T: Table) -> None: ...
    @abstractmethod
    def endBG(self, T: Table) -> None: ...
    @abstractmethod
    def startRow(self, T: Table, rowNo: int) -> None: ...
    @abstractmethod
    def startCell(
        self, T: Table, rowNo: int, colNo: int, cellval: Any, cellstyle: CellStyle, pos: tuple[int, int], size: tuple[int, int]
    ) -> None: ...
    @abstractmethod
    def endCell(self, T: Table) -> None: ...
    @abstractmethod
    def endRow(self, T: Table) -> None: ...
    @abstractmethod
    def startLines(self, T: Table) -> None: ...
    @abstractmethod
    def endLines(self, T: Table) -> None: ...
    @abstractmethod
    def endTable(self, T: Table) -> None: ...
