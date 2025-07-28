"""Write the workbook global settings to the archive."""

from _typeshed import Incomplete

from openpyxl.workbook.workbook import Workbook

def get_active_sheet(wb: Workbook) -> int | None:
    """
    Return the index of the active sheet.
    If the sheet set to active is hidden return the next visible sheet or None
    """

class WorkbookWriter:
    wb: Workbook
    rels: Incomplete
    package: Incomplete
    def __init__(self, wb: Workbook) -> None: ...
    def write_properties(self) -> None: ...
    def write_worksheets(self) -> None: ...
    def write_refs(self) -> None: ...
    def write_names(self) -> None: ...
    def write_pivots(self) -> None: ...
    def write_views(self) -> None: ...
    def write(self):
        """Write the core workbook xml."""

    def write_rels(self):
        """Write the workbook relationships xml."""

    def write_root_rels(self):
        """Write the package relationships"""
