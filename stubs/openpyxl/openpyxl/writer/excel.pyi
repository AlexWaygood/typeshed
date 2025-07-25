from typing import Literal
from zipfile import ZipFile

from openpyxl import _ZipFileFileProtocol
from openpyxl.packaging.manifest import Manifest
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

class ExcelWriter:
    """Write a workbook object to an Excel file."""

    workbook: Workbook
    manifest: Manifest
    vba_modified: set[str | None]
    def __init__(self, workbook: Workbook, archive: ZipFile) -> None: ...
    def write_data(self) -> None: ...
    def write_worksheet(self, ws: Worksheet) -> None: ...
    def save(self) -> None:
        """Write data into the archive."""

def save_workbook(workbook: Workbook, filename: _ZipFileFileProtocol) -> Literal[True]:
    """Save the given workbook on the filesystem under the name filename.

    :param workbook: the workbook to save
    :type workbook: :class:`openpyxl.workbook.Workbook`

    :param filename: the path to which save the workbook
    :type filename: string

    :rtype: bool

    """
