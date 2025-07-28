from _typeshed import ConvertibleToInt, Incomplete
from typing import ClassVar, Literal, Protocol
from typing_extensions import TypeAlias

from openpyxl.descriptors.base import (
    Alias,
    Bool,
    Convertible,
    Integer,
    NoneSet,
    String,
    _ConvertibleToBool,
    _ConvertibleToMultiCellRange,
)
from openpyxl.descriptors.nested import NestedText
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.worksheet.cell_range import CellRange, MultiCellRange
from openpyxl.xml.functions import Element

_DataValidationType: TypeAlias = Literal["whole", "decimal", "list", "date", "time", "textLength", "custom"]
_DataValidationErrorStyle: TypeAlias = Literal["stop", "warning", "information"]
_DataValidationImeMode: TypeAlias = Literal[
    "noControl",
    "off",
    "on",
    "disabled",
    "hiragana",
    "fullKatakana",
    "halfKatakana",
    "fullAlpha",
    "halfAlpha",
    "fullHangul",
    "halfHangul",
]
_DataValidationOperator: TypeAlias = Literal[
    "between", "notBetween", "equal", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"
]

class _HasCoordinate(Protocol):
    coordinate: str | CellRange

def collapse_cell_addresses(cells, input_ranges=()):
    """Collapse a collection of cell co-ordinates down into an optimal
    range or collection of ranges.

    E.g. Cells A1, A2, A3, B1, B2 and B3 should have the data-validation
    object applied, attempt to collapse down to a single range, A1:B3.

    Currently only collapsing contiguous vertical ranges (i.e. above
    example results in A1:A3 B1:B3).
    """

def expand_cell_ranges(range_string):
    """
    Expand cell ranges to a sequence of addresses.
    Reverse of collapse_cell_addresses
    Eg. converts "A1:A2 B1:B2" to (A1, A2, B1, B2)
    """

class DataValidation(Serialisable):
    tagname: ClassVar[str]
    sqref: Convertible[MultiCellRange, Literal[False]]
    cells: Alias
    ranges: Alias
    showDropDown: Bool[Literal[True]]
    hide_drop_down: Alias
    showInputMessage: Bool[Literal[True]]
    showErrorMessage: Bool[Literal[True]]
    allowBlank: Bool[Literal[True]]
    allow_blank: Alias
    errorTitle: String[Literal[True]]
    error: String[Literal[True]]
    promptTitle: String[Literal[True]]
    prompt: String[Literal[True]]
    formula1: NestedText[str, Literal[True]]
    formula2: NestedText[str, Literal[True]]
    type: NoneSet[_DataValidationType]
    errorStyle: NoneSet[_DataValidationErrorStyle]
    imeMode: NoneSet[_DataValidationImeMode]
    operator: NoneSet[_DataValidationOperator]
    validation_type: Alias
    def __init__(
        self,
        type: _DataValidationType | Literal["none"] | None = None,
        formula1: object = None,
        formula2: object = None,
        showErrorMessage: _ConvertibleToBool | None = False,
        showInputMessage: _ConvertibleToBool | None = False,
        showDropDown: _ConvertibleToBool | None = False,
        allowBlank: _ConvertibleToBool = False,
        sqref: _ConvertibleToMultiCellRange = (),
        promptTitle: str | None = None,
        errorStyle: _DataValidationErrorStyle | Literal["none"] | None = None,
        error: str | None = None,
        prompt: str | None = None,
        errorTitle: str | None = None,
        imeMode: _DataValidationImeMode | Literal["none"] | None = None,
        operator: _DataValidationOperator | Literal["none"] | None = None,
        allow_blank: _ConvertibleToBool | None = None,
    ) -> None: ...
    def add(self, cell) -> None:
        """Adds a cell or cell coordinate to this validator"""

    def __contains__(self, cell: _HasCoordinate | str | CellRange) -> bool: ...

class DataValidationList(Serialisable):
    tagname: ClassVar[str]
    disablePrompts: Bool[Literal[True]]
    xWindow: Integer[Literal[True]]
    yWindow: Integer[Literal[True]]
    dataValidation: Incomplete
    __elements__: ClassVar[tuple[str, ...]]
    __attrs__: ClassVar[tuple[str, ...]]
    def __init__(
        self,
        disablePrompts: _ConvertibleToBool | None = None,
        xWindow: ConvertibleToInt | None = None,
        yWindow: ConvertibleToInt | None = None,
        count=None,
        dataValidation=(),
    ) -> None: ...
    @property
    def count(self) -> int: ...
    def __len__(self) -> int: ...
    def append(self, dv) -> None: ...
    def to_tree(self, tagname: str | None = None) -> Element:  # type: ignore[override]
        """
        Need to skip validations that have no cell ranges
        """
