from _typeshed import Incomplete, ReadableBuffer, StrPath, Unused
from collections.abc import Generator, Iterable
from typing import Protocol
from typing_extensions import TypeAlias

from openpyxl.cell import _CellOrMergedCell
from openpyxl.worksheet._write_only import WriteOnlyWorksheet
from openpyxl.worksheet.worksheet import Worksheet

# WorksheetWriter.read has an explicit BytesIO branch. Let's make sure this protocol is viable for BytesIO too.
class _SupportsCloseAndWrite(Protocol):
    def write(self, buffer: ReadableBuffer, /) -> Unused: ...
    def close(self) -> Unused: ...

# et_xmlfile.xmlfile accepts a str | _SupportsCloseAndWrite
# lxml.etree.xmlfile should accept a StrPath | _SupportsClose https://lxml.de/api/lxml.etree.xmlfile-class.html
_OutType: TypeAlias = _SupportsCloseAndWrite | StrPath

ALL_TEMP_FILES: list[str]

def create_temporary_file(suffix: str = "") -> str: ...

class WorksheetWriter:
    ws: Worksheet | WriteOnlyWorksheet
    out: _OutType
    xf: Generator[Incomplete | None, Incomplete, None]
    def __init__(self, ws: Worksheet | WriteOnlyWorksheet, out: _OutType | None = None) -> None: ...
    def write_properties(self) -> None: ...
    def write_dimensions(self) -> None:
        """
        Write worksheet size if known
        """

    def write_format(self) -> None: ...
    def write_views(self) -> None: ...
    def write_cols(self) -> None: ...
    def write_top(self) -> None:
        """
        Write all elements up to rows:
        properties
        dimensions
        views
        format
        cols
        """

    def rows(self) -> list[tuple[int, list[_CellOrMergedCell]]]:
        """Return all rows, and any cells that they contain"""

    def write_rows(self) -> None: ...
    def write_row(self, xf, row: Iterable[_CellOrMergedCell], row_idx) -> None: ...
    def write_protection(self) -> None: ...
    def write_scenarios(self) -> None: ...
    def write_filter(self) -> None: ...
    def write_sort(self) -> None:
        """
        As per discusion with the OOXML Working Group global sort state is not required.
        openpyxl never reads it from existing files
        """

    def write_merged_cells(self) -> None: ...
    def write_formatting(self) -> None: ...
    def write_validations(self) -> None: ...
    def write_hyperlinks(self) -> None: ...
    def write_print(self) -> None: ...
    def write_margins(self) -> None: ...
    def write_page(self) -> None: ...
    def write_header(self) -> None: ...
    def write_breaks(self) -> None: ...
    def write_drawings(self) -> None: ...
    def write_legacy(self) -> None:
        """
        Comments & VBA controls use VML and require an additional element
        that is no longer in the specification.
        """

    def write_tables(self) -> None: ...
    def get_stream(self) -> Generator[Incomplete | None, bool | None, None]: ...
    def write_tail(self) -> None:
        """
        Write all elements after the rows
        calc properties
        protection
        protected ranges #
        scenarios
        filters
        sorts # always ignored
        data consolidation #
        custom views #
        merged cells
        phonetic properties #
        conditional formatting
        data validation
        hyperlinks
        print options
        page margins
        page setup
        header
        row breaks
        col breaks
        custom properties #
        cell watches #
        ignored errors #
        smart tags #
        drawing
        drawingHF #
        background #
        OLE objects #
        controls #
        web publishing #
        tables
        """

    def write(self) -> None:
        """
        High level
        """

    def close(self) -> None:
        """
        Close the context manager
        """

    def read(self) -> bytes:
        """
        Close the context manager and return serialised XML
        """

    def cleanup(self) -> None:
        """
        Remove tempfile
        """
