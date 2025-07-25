"""Workbook is the top-level container for all document information."""

from _typeshed import Incomplete, Unused
from collections.abc import Iterator
from datetime import datetime
from typing import Any, Final, type_check_only
from typing_extensions import TypeAlias, deprecated
from zipfile import ZipFile

from openpyxl import _Decodable, _ZipFileFileWriteProtocol
from openpyxl.chartsheet.chartsheet import Chartsheet
from openpyxl.styles.named_styles import NamedStyle
from openpyxl.utils.indexed_list import IndexedList
from openpyxl.workbook.child import _WorkbookChild
from openpyxl.worksheet._read_only import ReadOnlyWorksheet
from openpyxl.worksheet._write_only import WriteOnlyWorksheet
from openpyxl.worksheet.worksheet import Worksheet

_WorkbookWorksheet: TypeAlias = Worksheet | WriteOnlyWorksheet | ReadOnlyWorksheet
_WorkbookSheet: TypeAlias = _WorkbookWorksheet | Chartsheet

# The type of worksheets in a workbook are the same as the aliases above.
# However, because Worksheet adds a lots of attributes that other _WorkbookChild subclasses
# don't have (ReadOnlyWorksheet doesn't even inherit from it), this ends up being too
# disruptive to the typical usage of openpyxl where sheets are just Worksheets.
# Using Any may just lose too much type information and duck-typing
# from Worksheet works great here. Allowing instance type check, even if direct
# type comparison might be wrong.
@type_check_only
class _WorksheetLike(  # type: ignore[misc] # Incompatible definitions, favor Worksheet
    Worksheet, WriteOnlyWorksheet, ReadOnlyWorksheet
): ...

@type_check_only
class _WorksheetOrChartsheetLike(  # type: ignore[misc] # Incompatible definitions, favor Worksheet
    Chartsheet, _WorksheetLike
): ...

INTEGER_TYPES: Final[tuple[type[int]]]

class Workbook:
    """Workbook is the container for all other parts of the document."""

    template: bool
    path: str
    defined_names: Incomplete
    properties: Incomplete
    security: Incomplete
    shared_strings: IndexedList[str]
    loaded_theme: Incomplete
    vba_archive: ZipFile | None
    is_template: bool
    code_name: Incomplete
    encoding: str
    iso_dates: Incomplete
    rels: Incomplete
    calculation: Incomplete
    views: Incomplete
    # Useful as a reference of what "sheets" can be for other types
    # ExcelReader can add ReadOnlyWorksheet in read_only mode.
    # _sheets: list[_WorksheetOrChartsheetLike]
    def __init__(self, write_only: bool = False, iso_dates: bool = False) -> None: ...
    @property
    def epoch(self) -> datetime: ...
    @epoch.setter
    def epoch(self, value: datetime) -> None: ...
    @property
    def read_only(self) -> bool: ...
    @property
    def data_only(self) -> bool: ...
    @property
    def write_only(self) -> bool: ...
    @property
    def excel_base_date(self) -> datetime: ...
    @property
    def active(self) -> _WorksheetOrChartsheetLike | None:
        """Get the currently active sheet or None

        :type: :class:`openpyxl.worksheet.worksheet.Worksheet`
        """

    @active.setter
    def active(self, value: Worksheet | Chartsheet | int) -> None: ...
    # read_only workbook cannot call this method
    # Could be generic based on write_only
    def create_sheet(
        self, title: str | _Decodable | None = None, index: int | None = None
    ) -> Any:  # AnyOf[WriteOnlyWorksheet, Worksheet]
        """Create a worksheet (at an optional index).

        :param title: optional title of the sheet
        :type title: str
        :param index: optional position at which the sheet will be inserted
        :type index: int

        """

    def move_sheet(self, sheet: Worksheet | str, offset: int = 0) -> None:
        """
        Move a sheet or sheetname
        """

    def remove(self, worksheet: _WorkbookSheet) -> None:
        """Remove `worksheet` from this workbook."""

    @deprecated("Use wb.remove(worksheet) or del wb[sheetname]")
    def remove_sheet(self, worksheet: _WorkbookSheet) -> None:
        """Remove `worksheet` from this workbook."""

    def create_chartsheet(self, title: str | _Decodable | None = None, index: int | None = None) -> Chartsheet: ...
    @deprecated("Use wb[sheetname]")
    def get_sheet_by_name(self, name: str) -> _WorksheetOrChartsheetLike:
        """Returns a worksheet by its name.

        :param name: the name of the worksheet to look for
        :type name: string

        """

    def __contains__(self, key: str) -> bool: ...
    def index(self, worksheet: _WorkbookWorksheet) -> int:
        """Return the index of a worksheet."""

    @deprecated("Use wb.index(worksheet)")
    def get_index(self, worksheet: _WorkbookWorksheet) -> int:
        """Return the index of the worksheet."""

    def __getitem__(self, key: str) -> _WorksheetOrChartsheetLike:
        """Returns a worksheet by its name.

        :param name: the name of the worksheet to look for
        :type name: string

        """

    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[_WorksheetLike]: ...
    @deprecated("Use wb.sheetnames")
    def get_sheet_names(self) -> list[str]: ...
    @property
    def worksheets(self) -> list[_WorksheetLike]:
        """A list of sheets in this workbook

        :type: list of :class:`openpyxl.worksheet.worksheet.Worksheet`
        """

    @property
    def chartsheets(self) -> list[Chartsheet]:
        """A list of Chartsheets in this workbook

        :type: list of :class:`openpyxl.chartsheet.chartsheet.Chartsheet`
        """

    @property
    def sheetnames(self) -> list[str]:
        """Returns the list of the names of worksheets in this workbook.

        Names are returned in the worksheets order.

        :type: list of strings

        """

    @deprecated("Assign scoped named ranges directly to worksheets or global ones to the workbook. Deprecated in 3.1")
    def create_named_range(
        self,
        name: str,
        worksheet: _WorkbookChild | ReadOnlyWorksheet | None = None,
        value: str | Incomplete | None = None,
        scope: Unused = None,
    ) -> None:
        """Create a new named_range on a worksheet"""

    def add_named_style(self, style: NamedStyle) -> None:
        """
        Add a named style
        """

    @property
    def named_styles(self) -> list[str]:
        """
        List available named styles
        """

    @property
    def mime_type(self) -> str:
        """
        The mime type is determined by whether a workbook is a template or
        not and whether it contains macros or not. Excel requires the file
        extension to match but openpyxl does not enforce this.

        """

    def save(self, filename: _ZipFileFileWriteProtocol) -> None:
        """Save the current workbook under the given `filename`.
        Use this function instead of using an `ExcelWriter`.

        .. warning::
            When creating your workbook using `write_only` set to True,
            you will only be able to call this function once. Subsequent attempts to
            modify or save the file will raise an :class:`openpyxl.shared.exc.WorkbookAlreadySaved` exception.
        """

    @property
    def style_names(self) -> list[str]:
        """
        List of named styles
        """
    # A write_only and read_only workbooks can't use this method as it requires both reading and writing.
    # On an implementation level, a WorksheetCopy is created from the call to self.create_sheet,
    # but WorksheetCopy only works with Worksheet.
    def copy_worksheet(self, from_worksheet: Worksheet) -> Worksheet:
        """Copy an existing worksheet in the current workbook

        .. warning::
            This function cannot copy worksheets between workbooks.
            worksheets can only be copied within the workbook that they belong

        :param from_worksheet: the worksheet to be copied from
        :return: copy of the initial worksheet
        """

    def close(self) -> None:
        """
        Close workbook file if open. Only affects read-only and write-only modes.
        """
