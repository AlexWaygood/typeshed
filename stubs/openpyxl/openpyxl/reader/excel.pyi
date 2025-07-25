"""Read an xlsx file into Python"""

from typing import Final, Literal
from typing_extensions import TypeAlias
from zipfile import ZipFile

from openpyxl import _ZipFileFileProtocol
from openpyxl.chartsheet.chartsheet import Chartsheet
from openpyxl.packaging.manifest import Manifest
from openpyxl.packaging.relationship import Relationship
from openpyxl.reader.workbook import WorkbookParser
from openpyxl.workbook import Workbook

_SupportedFormats: TypeAlias = Literal[".xlsx", ".xlsm", ".xltx", ".xltm"]
SUPPORTED_FORMATS: Final[tuple[_SupportedFormats, ...]]

class ExcelReader:
    """
    Read an Excel package and dispatch the contents to the relevant modules
    """

    archive: ZipFile
    valid_files: list[str]
    read_only: bool
    keep_vba: bool
    data_only: bool
    keep_links: bool
    rich_text: bool
    shared_strings: list[str]
    package: Manifest  # defined after call to read_manifest()
    parser: WorkbookParser  # defined after call to read_workbook()
    wb: Workbook  # defined after call to read_workbook()

    def __init__(
        self,
        fn: _ZipFileFileProtocol,
        read_only: bool = False,
        keep_vba: bool = False,
        data_only: bool = False,
        keep_links: bool = True,
        rich_text: bool = False,
    ) -> None: ...
    def read_manifest(self) -> None: ...
    def read_strings(self) -> None: ...
    def read_workbook(self) -> None: ...
    def read_properties(self) -> None: ...
    def read_custom(self) -> None: ...
    def read_theme(self) -> None: ...
    def read_chartsheet(self, sheet: Chartsheet, rel: Relationship) -> None: ...
    def read_worksheets(self) -> None: ...
    def read(self) -> None: ...

def load_workbook(
    filename: _ZipFileFileProtocol,
    read_only: bool = False,
    keep_vba: bool = False,
    data_only: bool = False,
    keep_links: bool = True,
    rich_text: bool = False,
) -> Workbook:
    """Open the given filename and return the workbook

    :param filename: the path to open or a file-like object
    :type filename: string or a file-like object open in binary mode c.f., :class:`zipfile.ZipFile`

    :param read_only: optimised for reading, content cannot be edited
    :type read_only: bool

    :param keep_vba: preserve vba content (this does NOT mean you can use it)
    :type keep_vba: bool

    :param data_only: controls whether cells with formulae have either the formula (default) or the value stored the last time Excel read the sheet
    :type data_only: bool

    :param keep_links: whether links to external workbooks should be preserved. The default is True
    :type keep_links: bool

    :param rich_text: if set to True openpyxl will preserve any rich text formatting in cells. The default is False
    :type rich_text: bool

    :rtype: :class:`openpyxl.workbook.Workbook`

    .. note::

        When using lazy load, all worksheets will be :class:`openpyxl.worksheet.iter_worksheet.IterableWorksheet`
        and the returned workbook will be read-only.

    """
