from collections.abc import Generator
from zipfile import ZipFile

from openpyxl.packaging.relationship import Relationship, RelationshipList
from openpyxl.packaging.workbook import ChildSheet, PivotCache
from openpyxl.pivot.cache import CacheDefinition
from openpyxl.workbook import Workbook

class WorkbookParser:
    archive: ZipFile
    workbook_part_name: str
    wb: Workbook
    keep_links: bool
    sheets: list[ChildSheet]
    def __init__(self, archive: ZipFile, workbook_part_name: str, keep_links: bool = True) -> None: ...
    @property
    def rels(self) -> RelationshipList: ...
    # Errors if "parse" is never called.
    caches: list[PivotCache]
    def parse(self) -> None: ...
    def find_sheets(self) -> Generator[tuple[ChildSheet, Relationship], None, None]:
        """
        Find all sheets in the workbook and return the link to the source file.

        Older XLSM files sometimes contain invalid sheet elements.
        Warn user when these are removed.
        """

    def assign_names(self) -> None:
        """
        Bind defined names and other definitions to worksheets or the workbook
        """

    @property
    def pivot_caches(self) -> dict[int, CacheDefinition]:
        """
        Get PivotCache objects
        """
