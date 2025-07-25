"""Worksheet is the 2nd-level container in Excel."""

from _typeshed import ConvertibleToInt, Incomplete
from collections.abc import Generator, Iterable, Iterator
from types import GeneratorType
from typing import Any, Final, Literal, NoReturn, overload
from typing_extensions import deprecated

from openpyxl import _Decodable, _VisibilityType
from openpyxl.cell import _AnyCellValue, _CellGetValue, _CellOrMergedCell, _CellSetValue
from openpyxl.cell.cell import Cell
from openpyxl.chart._chart import ChartBase
from openpyxl.drawing.image import Image
from openpyxl.formatting.formatting import ConditionalFormattingList
from openpyxl.workbook.child import _WorkbookChild
from openpyxl.workbook.defined_name import DefinedNameDict
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.cell_range import CellRange, MultiCellRange
from openpyxl.worksheet.datavalidation import DataValidation, DataValidationList
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder, RowDimension, SheetFormatProperties
from openpyxl.worksheet.filters import AutoFilter
from openpyxl.worksheet.page import PageMargins, PrintOptions, PrintPageSetup
from openpyxl.worksheet.pagebreak import ColBreak, RowBreak
from openpyxl.worksheet.properties import WorksheetProperties
from openpyxl.worksheet.protection import SheetProtection
from openpyxl.worksheet.scenario import ScenarioList
from openpyxl.worksheet.table import Table, TableList
from openpyxl.worksheet.views import SheetView, SheetViewList

class Worksheet(_WorkbookChild):
    """Represents a worksheet.

    Do not create worksheets yourself,
    use :func:`openpyxl.workbook.Workbook.create_sheet` instead

    """

    mime_type: str
    BREAK_NONE: Final = 0
    BREAK_ROW: Final = 1
    BREAK_COLUMN: Final = 2

    SHEETSTATE_VISIBLE: Final = "visible"
    SHEETSTATE_HIDDEN: Final = "hidden"
    SHEETSTATE_VERYHIDDEN: Final = "veryHidden"

    PAPERSIZE_LETTER: Final = "1"
    PAPERSIZE_LETTER_SMALL: Final = "2"
    PAPERSIZE_TABLOID: Final = "3"
    PAPERSIZE_LEDGER: Final = "4"
    PAPERSIZE_LEGAL: Final = "5"
    PAPERSIZE_STATEMENT: Final = "6"
    PAPERSIZE_EXECUTIVE: Final = "7"
    PAPERSIZE_A3: Final = "8"
    PAPERSIZE_A4: Final = "9"
    PAPERSIZE_A4_SMALL: Final = "10"
    PAPERSIZE_A5: Final = "11"

    ORIENTATION_PORTRAIT: Final = "portrait"
    ORIENTATION_LANDSCAPE: Final = "landscape"

    _cells: dict[tuple[int, int], _CellOrMergedCell]  # private but very useful to understand typing
    row_dimensions: DimensionHolder[int, RowDimension]
    column_dimensions: DimensionHolder[str, ColumnDimension]
    row_breaks: RowBreak
    col_breaks: ColBreak
    merged_cells: MultiCellRange
    data_validations: DataValidationList
    sheet_state: _VisibilityType
    page_setup: PrintPageSetup
    print_options: PrintOptions
    page_margins: PageMargins
    views: SheetViewList
    protection: SheetProtection
    defined_names: DefinedNameDict
    auto_filter: AutoFilter
    conditional_formatting: ConditionalFormattingList
    legacy_drawing: Incomplete | None
    sheet_properties: WorksheetProperties
    sheet_format: SheetFormatProperties
    scenarios: ScenarioList

    def __init__(self, parent: Workbook | None, title: str | _Decodable | None = None) -> None: ...
    @property
    def sheet_view(self) -> SheetView: ...
    @property
    def selected_cell(self) -> str | None: ...
    @property
    def active_cell(self) -> str | None: ...
    @property
    def array_formulae(self) -> dict[str, str]:
        """Returns a dictionary of cells with array formulae and the cells in array"""

    @property
    def show_gridlines(self) -> bool | None: ...
    @property
    def freeze_panes(self) -> str | None: ...
    @freeze_panes.setter
    def freeze_panes(self, topLeftCell: str | Cell | None = None) -> None: ...
    # A MergedCell value should be kept to None
    @overload
    def cell(self, row: int, column: int, value: None = None) -> _CellOrMergedCell:
        """
        Returns a cell object based on the given coordinates.

        Usage: cell(row=15, column=1, value=5)

        Calling `cell` creates cells in memory when they
        are first accessed.

        :param row: row index of the cell (e.g. 4)
        :type row: int

        :param column: column index of the cell (e.g. 3)
        :type column: int

        :param value: value of the cell (e.g. 5)
        :type value: numeric or time or string or bool or none

        :rtype: openpyxl.cell.cell.Cell
        """

    @overload
    def cell(self, row: int, column: int, value: _CellSetValue = None) -> Cell: ...
    # An int is necessarily a row selection
    @overload
    def __getitem__(self, key: int) -> tuple[_CellOrMergedCell, ...]:
        """Convenience access by Excel style coordinates

        The key can be a single cell coordinate 'A1', a range of cells 'A1:D25',
        individual rows or columns 'A', 4 or ranges of rows or columns 'A:D',
        4:10.

        Single cells will always be created if they do not exist.

        Returns either a single cell or a tuple of rows or columns.
        """
    # A slice is necessarily a row or rows, even if targetting a single cell
    @overload
    def __getitem__(self, key: slice) -> tuple[Any, ...]: ...  # tuple[AnyOf[_CellOrMergedCell, tuple[_CellOrMergedCell, ...]]]
    # A str could be an individual cell, row, column or full range
    @overload
    def __getitem__(
        self, key: str
    ) -> Any: ...  # AnyOf[_CellOrMergedCell, tuple[_CellOrMergedCell, ...], tuple[tuple[_CellOrMergedCell, ...], ...]]
    def __setitem__(self, key: str, value: _CellSetValue) -> None: ...
    def __iter__(self) -> Iterator[tuple[_CellOrMergedCell, ...]]: ...
    def __delitem__(self, key: str) -> None: ...
    @property
    def min_row(self) -> int:
        """The minimum row index containing data (1-based)

        :type: int
        """

    @property
    def max_row(self) -> int:
        """The maximum row index containing data (1-based)

        :type: int
        """

    @property
    def min_column(self) -> int:
        """The minimum column index containing data (1-based)

        :type: int
        """

    @property
    def max_column(self) -> int:
        """The maximum column index containing data (1-based)

        :type: int
        """

    def calculate_dimension(self) -> str:
        """Return the minimum bounding range for all cells containing data (ex. 'A1:M24')

        :rtype: string
        """

    @property
    def dimensions(self) -> str:
        """Returns the result of :func:`calculate_dimension`"""

    @overload
    def iter_rows(
        self, min_row: int | None, max_row: int | None, min_col: int | None, max_col: int | None, values_only: Literal[True]
    ) -> Generator[tuple[_CellGetValue, ...], None, None]:
        """
        Produces cells from the worksheet, by row. Specify the iteration range
        using indices of rows and columns.

        If no indices are specified the range starts at A1.

        If no cells are in the worksheet an empty tuple will be returned.

        :param min_col: smallest column index (1-based index)
        :type min_col: int

        :param min_row: smallest row index (1-based index)
        :type min_row: int

        :param max_col: largest column index (1-based index)
        :type max_col: int

        :param max_row: largest row index (1-based index)
        :type max_row: int

        :param values_only: whether only cell values should be returned
        :type values_only: bool

        :rtype: generator
        """

    @overload
    def iter_rows(
        self,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
        *,
        values_only: Literal[True],
    ) -> Generator[tuple[_CellGetValue, ...], None, None]: ...
    @overload
    def iter_rows(
        self,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
        values_only: Literal[False] = False,
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None]: ...
    @overload
    def iter_rows(
        self, min_row: int | None, max_row: int | None, min_col: int | None, max_col: int | None, values_only: bool
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None] | Generator[tuple[_CellGetValue, ...], None, None]: ...
    @overload
    def iter_rows(
        self,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
        *,
        values_only: bool,
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None] | Generator[tuple[_CellGetValue, ...], None, None]: ...
    @property
    def rows(self) -> Generator[tuple[_CellOrMergedCell, ...], None, None]:
        """Produces all cells in the worksheet, by row (see :func:`iter_rows`)

        :type: generator
        """

    @property
    def values(self) -> Generator[tuple[_CellGetValue, ...]]:
        """Produces all cell values in the worksheet, by row

        :type: generator
        """

    @overload
    def iter_cols(
        self, min_col: int | None, max_col: int | None, min_row: int | None, max_row: int | None, values_only: Literal[True]
    ) -> Generator[tuple[_CellGetValue, ...], None, None]:
        """
        Produces cells from the worksheet, by column. Specify the iteration range
        using indices of rows and columns.

        If no indices are specified the range starts at A1.

        If no cells are in the worksheet an empty tuple will be returned.

        :param min_col: smallest column index (1-based index)
        :type min_col: int

        :param min_row: smallest row index (1-based index)
        :type min_row: int

        :param max_col: largest column index (1-based index)
        :type max_col: int

        :param max_row: largest row index (1-based index)
        :type max_row: int

        :param values_only: whether only cell values should be returned
        :type values_only: bool

        :rtype: generator
        """

    @overload
    def iter_cols(
        self,
        min_col: int | None = None,
        max_col: int | None = None,
        min_row: int | None = None,
        max_row: int | None = None,
        *,
        values_only: Literal[True],
    ) -> Generator[tuple[_CellGetValue, ...], None, None]: ...
    @overload
    def iter_cols(
        self,
        min_col: int | None = None,
        max_col: int | None = None,
        min_row: int | None = None,
        max_row: int | None = None,
        values_only: Literal[False] = False,
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None]: ...
    @overload
    def iter_cols(
        self, min_col: int | None, max_col: int | None, min_row: int | None, max_row: int | None, values_only: bool
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None] | Generator[tuple[_CellGetValue, ...], None, None]: ...
    @overload
    def iter_cols(
        self,
        min_col: int | None = None,
        max_col: int | None = None,
        min_row: int | None = None,
        max_row: int | None = None,
        *,
        values_only: bool,
    ) -> Generator[tuple[_CellOrMergedCell, ...], None, None] | Generator[tuple[_CellGetValue, ...], None, None]: ...
    @property
    def columns(self) -> Generator[tuple[_CellOrMergedCell, ...], None, None]:
        """Produces all cells in the worksheet, by column  (see :func:`iter_cols`)"""

    @property
    def column_groups(self) -> list[str]:
        """
        Return a list of column ranges where more than one column
        """

    def set_printer_settings(
        self, paper_size: int | None, orientation: Literal["default", "portrait", "landscape"] | None
    ) -> None:
        """Set printer settings"""

    def add_data_validation(self, data_validation: DataValidation) -> None:
        """Add a data-validation object to the sheet.  The data-validation
        object defines the type of data-validation to be applied and the
        cell or range of cells it should apply to.
        """

    def add_chart(self, chart: ChartBase, anchor: str | None = None) -> None:
        """
        Add a chart to the sheet
        Optionally provide a cell for the top-left anchor
        """

    def add_image(self, img: Image, anchor: str | None = None) -> None:
        """
        Add an image to the sheet.
        Optionally provide a cell for the top-left anchor
        """

    def add_table(self, table: Table) -> None:
        """
        Check for duplicate name in definedNames and other worksheet tables
        before adding table.
        """

    @property
    def tables(self) -> TableList: ...
    def add_pivot(self, pivot) -> None: ...
    # Same overload as CellRange.__init__
    @overload
    def merge_cells(
        self, range_string: str, start_row: None = None, start_column: None = None, end_row: None = None, end_column: None = None
    ) -> None:
        """Set merge on a cell range.  Range is a cell range (e.g. A1:E1)"""

    @overload
    def merge_cells(
        self,
        range_string: None = None,
        *,
        start_row: ConvertibleToInt,
        start_column: ConvertibleToInt,
        end_row: ConvertibleToInt,
        end_column: ConvertibleToInt,
    ) -> None: ...
    @overload
    def merge_cells(
        self,
        range_string: None,
        start_row: ConvertibleToInt,
        start_column: ConvertibleToInt,
        end_row: ConvertibleToInt,
        end_column: ConvertibleToInt,
    ) -> None: ...
    # Will always raise: TypeError: 'set' object is not subscriptable
    @property
    @deprecated("Use ws.merged_cells.ranges")
    def merged_cell_ranges(self) -> NoReturn:
        """Return a copy of cell ranges

        .. note::
            Deprecated: Use ws.merged_cells.ranges
        """

    def unmerge_cells(
        self,
        range_string: str | None = None,
        start_row: int | None = None,
        start_column: int | None = None,
        end_row: int | None = None,
        end_column: int | None = None,
    ) -> None:
        """Remove merge on a cell range.  Range is a cell range (e.g. A1:E1)"""

    def append(
        self,
        iterable: (
            list[_AnyCellValue]
            | tuple[_CellOrMergedCell | _CellGetValue, ...]
            | range
            | GeneratorType[_CellOrMergedCell | _CellGetValue, object, object]
            | dict[int | str, _AnyCellValue]
        ),
    ) -> None:
        """Appends a group of values at the bottom of the current sheet.

        * If it's a list: all values are added in order, starting from the first column
        * If it's a dict: values are assigned to the columns indicated by the keys (numbers or letters)

        :param iterable: list, range or generator, or dict containing values to append
        :type iterable: list|tuple|range|generator or dict

        Usage:

        * append(['This is A1', 'This is B1', 'This is C1'])
        * **or** append({'A' : 'This is A1', 'C' : 'This is C1'})
        * **or** append({1 : 'This is A1', 3 : 'This is C1'})

        :raise: TypeError when iterable is neither a list/tuple nor a dict

        """

    def insert_rows(self, idx: int, amount: int = 1) -> None:
        """
        Insert row or rows before row==idx
        """

    def insert_cols(self, idx: int, amount: int = 1) -> None:
        """
        Insert column or columns before col==idx
        """

    def delete_rows(self, idx: int, amount: int = 1) -> None:
        """
        Delete row or rows from row==idx
        """

    def delete_cols(self, idx: int, amount: int = 1) -> None:
        """
        Delete column or columns from col==idx
        """

    def move_range(self, cell_range: CellRange | str, rows: int = 0, cols: int = 0, translate: bool = False) -> None:
        """
        Move a cell range by the number of rows and/or columns:
        down if rows > 0 and up if rows < 0
        right if cols > 0 and left if cols < 0
        Existing cells will be overwritten.
        Formulae and references will not be updated.
        """

    @property
    def print_title_rows(self) -> str | None:
        """Rows to be printed at the top of every page (ex: '1:3')"""

    @print_title_rows.setter
    def print_title_rows(self, rows: str | None) -> None: ...
    @property
    def print_title_cols(self) -> str | None:
        """Columns to be printed at the left side of every page (ex: 'A:C')"""

    @print_title_cols.setter
    def print_title_cols(self, cols: str | None) -> None: ...
    @property
    def print_titles(self) -> str: ...
    @property
    def print_area(self) -> str:
        """
        The print area for the worksheet, or None if not set. To set, supply a range
        like 'A1:D4' or a list of ranges.
        """

    @print_area.setter
    def print_area(self, value: str | Iterable[str] | None) -> None: ...
