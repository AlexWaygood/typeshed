"""Write worksheets to xml representations in an optimized way"""

from collections.abc import Iterable

from openpyxl import _Decodable
from openpyxl.cell.cell import Cell
from openpyxl.workbook.child import _WorkbookChild
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.table import TableList
from openpyxl.worksheet.views import SheetView
from openpyxl.worksheet.worksheet import Worksheet

class WriteOnlyWorksheet(_WorkbookChild):
    """
    Streaming worksheet. Optimised to reduce memory by writing rows just in
    time.
    Cells can be styled and have comments Styles for rows and columns
    must be applied before writing cells
    """

    mime_type = Worksheet.mime_type
    add_chart = Worksheet.add_chart
    add_image = Worksheet.add_image
    add_table = Worksheet.add_table

    # Same properties as Worksheet
    # https://github.com/python/mypy/issues/6700
    @property
    def tables(self) -> TableList: ...
    @property
    def print_titles(self) -> str: ...
    @property
    def print_title_cols(self) -> str | None:
        """Columns to be printed at the left side of every page (ex: 'A:C')"""

    @print_title_cols.setter
    def print_title_cols(self, cols: str | None) -> None: ...
    @property
    def print_title_rows(self) -> str | None:
        """Rows to be printed at the top of every page (ex: '1:3')"""

    @print_title_rows.setter
    def print_title_rows(self, rows: str | None) -> None: ...
    @property
    def freeze_panes(self) -> str | None: ...
    @freeze_panes.setter
    def freeze_panes(self, topLeftCell: str | Cell | None = ...) -> None: ...
    @property
    def print_area(self) -> str:
        """
        The print area for the worksheet, or None if not set. To set, supply a range
        like 'A1:D4' or a list of ranges.
        """

    @print_area.setter
    def print_area(self, value: str | Iterable[str] | None) -> None: ...
    @property
    def sheet_view(self) -> SheetView: ...
    def __init__(self, parent: Workbook | None, title: str | _Decodable | None) -> None: ...
    @property
    def closed(self) -> bool: ...
    def close(self) -> None: ...
    def append(self, row) -> None:
        """
        :param row: iterable containing values to append
        :type row: iterable
        """
