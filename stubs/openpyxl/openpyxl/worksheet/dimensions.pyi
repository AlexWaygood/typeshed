from _typeshed import ConvertibleToFloat, ConvertibleToInt, Unused
from collections.abc import Callable, Iterator
from typing import ClassVar, Literal, TypeVar
from typing_extensions import Self

from openpyxl.descriptors import Strict
from openpyxl.descriptors.base import Alias, Bool, Float, Integer, String, _ConvertibleToBool
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.styles.styleable import StyleableObject
from openpyxl.utils.bound_dictionary import BoundDictionary
from openpyxl.utils.cell import _RangeBoundariesTuple
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.xml.functions import Element

_DimKeyT = TypeVar("_DimKeyT", bound=str | int)
_DimT = TypeVar("_DimT", bound=Dimension)

class Dimension(Strict, StyleableObject):
    """Information about the display properties of a row or column."""

    __fields__: ClassVar[tuple[str, ...]]

    index: Integer[Literal[False]]
    hidden: Bool[Literal[False]]
    outlineLevel: Integer[Literal[True]]
    outline_level: Alias
    collapsed: Bool[Literal[False]]
    style: Alias  # type: ignore[assignment]

    # Dimensions are only meant to be used on Worksheet objects
    parent: Worksheet

    def __init__(
        self,
        index: ConvertibleToInt,
        hidden: _ConvertibleToBool,
        outlineLevel: ConvertibleToInt | None,
        collapsed: _ConvertibleToBool,
        worksheet: Worksheet,
        visible: Unused = True,
        style=None,
    ) -> None: ...
    def __iter__(self) -> Iterator[tuple[str, str]]: ...
    def __copy__(self) -> Self: ...

class RowDimension(Dimension):
    """Information about the display properties of a row."""

    r: Alias
    s: Alias
    ht: Float[Literal[True]]
    height: Alias
    thickBot: Bool[Literal[False]]
    thickTop: Bool[Literal[False]]
    def __init__(
        self,
        worksheet: Worksheet,
        index: int = 0,
        ht: ConvertibleToFloat | None = None,
        customHeight: Unused = None,
        s=None,
        customFormat: Unused = None,
        hidden: _ConvertibleToBool = None,
        outlineLevel: ConvertibleToInt | None = 0,
        outline_level: ConvertibleToInt | None = None,
        collapsed: _ConvertibleToBool = None,
        visible=None,
        height=None,
        r=None,
        spans: Unused = None,
        thickBot: _ConvertibleToBool = None,
        thickTop: _ConvertibleToBool = None,
        **kw: Unused,
    ) -> None: ...
    @property
    def customFormat(self) -> bool:
        """Always true if there is a style for the row"""

    @property
    def customHeight(self) -> bool:
        """Always true if there is a height for the row"""

class ColumnDimension(Dimension):
    """Information about the display properties of a column."""

    width: Float[Literal[False]]
    bestFit: Bool[Literal[False]]
    auto_size: Alias
    index: String[Literal[False]]  # type: ignore[assignment]
    min: Integer[Literal[True]]
    max: Integer[Literal[True]]
    collapsed: Bool[Literal[False]]

    def __init__(
        self,
        worksheet: Worksheet,
        index: str = "A",
        width: ConvertibleToFloat = 13,
        bestFit: _ConvertibleToBool = False,
        hidden: _ConvertibleToBool = False,
        outlineLevel: ConvertibleToInt | None = 0,
        outline_level: ConvertibleToInt | None = None,
        collapsed: _ConvertibleToBool = False,
        style=None,
        min: ConvertibleToInt | None = None,
        max: ConvertibleToInt | None = None,
        customWidth: Unused = False,
        visible: bool | None = None,
        auto_size: _ConvertibleToBool | None = None,
    ) -> None: ...
    @property
    def customWidth(self) -> bool:
        """Always true if there is a width for the column"""

    def reindex(self) -> None:
        """
        Set boundaries for column definition
        """

    @property
    def range(self) -> str:
        """Return the range of cells actually covered"""

    def to_tree(self) -> Element | None: ...

class DimensionHolder(BoundDictionary[_DimKeyT, _DimT]):
    """
    Allow columns to be grouped
    """

    worksheet: Worksheet
    max_outline: int | None
    default_factory: Callable[[], _DimT] | None

    def __init__(
        self, worksheet: Worksheet, reference: str = "index", default_factory: Callable[[], _DimT] | None = None
    ) -> None: ...
    def group(self, start: _DimKeyT, end: _DimKeyT | None = None, outline_level: int = 1, hidden: bool = False) -> None:
        """allow grouping a range of consecutive rows or columns together

        :param start: first row or column to be grouped (mandatory)
        :param end: last row or column to be grouped (optional, default to start)
        :param outline_level: outline level
        :param hidden: should the group be hidden on workbook open or not
        """

    def to_tree(self) -> Element | None: ...

class SheetFormatProperties(Serialisable):
    tagname: ClassVar[str]
    baseColWidth: Integer[Literal[True]]
    defaultColWidth: Float[Literal[True]]
    defaultRowHeight: Float[Literal[False]]
    customHeight: Bool[Literal[True]]
    zeroHeight: Bool[Literal[True]]
    thickTop: Bool[Literal[True]]
    thickBottom: Bool[Literal[True]]
    outlineLevelRow: Integer[Literal[True]]
    outlineLevelCol: Integer[Literal[True]]
    def __init__(
        self,
        baseColWidth: ConvertibleToInt | None = 8,
        defaultColWidth: ConvertibleToFloat | None = None,
        defaultRowHeight: ConvertibleToFloat = 15,
        customHeight: _ConvertibleToBool | None = None,
        zeroHeight: _ConvertibleToBool | None = None,
        thickTop: _ConvertibleToBool | None = None,
        thickBottom: _ConvertibleToBool | None = None,
        outlineLevelRow: ConvertibleToInt | None = None,
        outlineLevelCol: ConvertibleToInt | None = None,
    ) -> None: ...

class SheetDimension(Serialisable):
    tagname: ClassVar[str]
    ref: String[Literal[False]]
    def __init__(self, ref: str) -> None: ...
    @property
    def boundaries(self) -> _RangeBoundariesTuple: ...
