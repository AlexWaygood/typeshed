import sys
from _typeshed import SupportsWrite
from collections.abc import Iterator
from types import TracebackType
from typing import Final, Literal
from typing_extensions import Self

from .biffh import *
from .formatting import XF, Font, Format
from .formula import *
from .sheet import Cell, Sheet
from .timemachine import *

empty_cell: Final[Cell]
MY_EOF: Final[int]
SUPBOOK_UNK: Final[int]
SUPBOOK_INTERNAL: Final[int]
SUPBOOK_EXTERNAL: Final[int]
SUPBOOK_ADDIN: Final[int]
SUPBOOK_DDEOLE: Final[int]
SUPPORTED_VERSIONS: Final[tuple[int, ...]]
builtin_name_from_code: Final[dict[str, str]]
code_from_builtin_name: Final[dict[str, str]]

def open_workbook_xls(
    filename: str | None = None,
    logfile: SupportsWrite[str] = sys.stdout,
    verbosity: int = 0,
    use_mmap: bool = True,
    file_contents: bytes | None = None,
    encoding_override: str | None = None,
    formatting_info: bool = False,
    on_demand: bool = False,
    ragged_rows: bool = False,
    ignore_workbook_corruption: bool = False,
) -> Book: ...

class Name(BaseObject):
    """
    Information relating to a named reference, formula, macro, etc.

    .. note::

      Name information is **not** extracted from files older than
      Excel 5.0 (``Book.biff_version < 50``)
    """

    _repr_these: list[str]
    book: Book | None = None
    hidden: Literal[0, 1]
    func: Literal[0, 1]
    vbasic: Literal[0, 1]
    macro: Literal[0, 1]
    complex: Literal[0, 1]
    builtin: Literal[0, 1]
    funcgroup: Literal[0, 1]
    binary: Literal[0, 1]
    name_index: int
    name: str
    raw_formula: bytes
    scope: Literal[-1, -2, -3, 0]
    result: Operand | None
    def cell(self) -> Cell:
        """
        This is a convenience method for the frequent use case where the name
        refers to a single cell.

        :returns: An instance of the :class:`~xlrd.sheet.Cell` class.

        :raises xlrd.biffh.XLRDError:
          The name is not a constant absolute reference
          to a single cell.
        """

    def area2d(self, clipped: bool = True) -> tuple[Sheet, int, int, int, int]:
        """
        This is a convenience method for the use case where the name
        refers to one rectangular area in one worksheet.

        :param clipped:
          If ``True``, the default, the returned rectangle is clipped
          to fit in ``(0, sheet.nrows, 0, sheet.ncols)``.
          it is guaranteed that ``0 <= rowxlo <= rowxhi <= sheet.nrows`` and
          that the number of usable rows in the area (which may be zero) is
          ``rowxhi - rowxlo``; likewise for columns.

        :returns: a tuple ``(sheet_object, rowxlo, rowxhi, colxlo, colxhi)``.

        :raises xlrd.biffh.XLRDError:
           The name is not a constant absolute reference
           to a single area in a single sheet.
        """

class Book(BaseObject):
    """
    Contents of a "workbook".

    .. warning::

      You should not instantiate this class yourself. You use the :class:`Book`
      object that was returned when you called :func:`~xlrd.open_workbook`.
    """

    nsheets: int
    datemode: Literal[0, 1]
    biff_version: int
    name_obj_list: list[Name]
    codepage: int | None
    encoding: str | None
    countries: tuple[int, int]
    user_name: str
    font_list: list[Font]
    xf_list: list[XF]
    format_list: list[Format]
    format_map: dict[int, Format]
    style_name_map: dict[str, tuple[int, int]]
    colour_map: dict[int, tuple[int, int, int] | None]
    palette_record: list[tuple[int, int, int]]
    load_time_stage_1: float
    load_time_stage_2: float
    def sheets(self) -> list[Sheet]:
        """
        :returns: A list of all sheets in the book.

        All sheets not already loaded will be loaded.
        """

    def sheet_by_index(self, sheetx: int) -> Sheet:
        """
        :param sheetx: Sheet index in ``range(nsheets)``
        :returns: A :class:`~xlrd.sheet.Sheet`.
        """

    def __iter__(self) -> Iterator[Sheet]:
        """
        Makes iteration through sheets of a book a little more straightforward.
        Don't free resources after use since it can be called like `list(book)`
        """

    def sheet_by_name(self, sheet_name: str) -> Sheet:
        """
        :param sheet_name: Name of the sheet required.
        :returns: A :class:`~xlrd.sheet.Sheet`.
        """

    def __getitem__(self, item: int | str) -> Sheet:
        """
        Allow indexing with sheet name or index.
        :param item: Name or index of sheet enquired upon
        :return: :class:`~xlrd.sheet.Sheet`.
        """

    def sheet_names(self) -> list[str]:
        """
        :returns:
          A list of the names of all the worksheets in the workbook file.
          This information is available even when no sheets have yet been
          loaded.
        """

    def sheet_loaded(self, sheet_name_or_index: int | str) -> bool:
        """
        :param sheet_name_or_index: Name or index of sheet enquired upon
        :returns: ``True`` if sheet is loaded, ``False`` otherwise.

        .. versionadded:: 0.7.1
        """

    def unload_sheet(self, sheet_name_or_index: int | str) -> None:
        """
        :param sheet_name_or_index: Name or index of sheet to be unloaded.

        .. versionadded:: 0.7.1
        """
    mem: bytes | None = None
    filestr: bytes | None = None
    def release_resources(self) -> None:
        """
        This method has a dual purpose. You can call it to release
        memory-consuming objects and (possibly) a memory-mapped file
        (:class:`mmap.mmap` object) when you have finished loading sheets in
        ``on_demand`` mode, but still require the :class:`Book` object to
        examine the loaded sheets. It is also called automatically (a) when
        :func:`~xlrd.open_workbook`
        raises an exception and (b) if you are using a ``with`` statement, when
        the ``with`` block is exited. Calling this method multiple times on the
        same object has no ill effect.
        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    name_and_scope_map: dict[tuple[str, int], Name]
    name_map: dict[str, list[Name]]
    raw_user_name: bool
    builtinfmtcount: int
    addin_func_names: list[str]
    def __init__(self) -> None: ...
    logfile: SupportsWrite[str]
    verbosity: int
    use_mmap: bool
    encoding_override: str | None
    formatting_info: bool
    on_demand: bool
    ragged_rows: bool
    stream_len: int
    base: int
    def biff2_8_load(
        self,
        filename: str | None = None,
        file_contents: bytes | None = None,
        logfile: SupportsWrite[str] = sys.stdout,
        verbosity: int = 0,
        use_mmap: bool = True,
        encoding_override: str | None = None,
        formatting_info: bool = False,
        on_demand: bool = False,
        ragged_rows: bool = False,
        ignore_workbook_corruption: bool = False,
    ) -> None: ...
    xfcount: int
    actualfmtcount: int
    def initialise_format_info(self) -> None: ...
    def get2bytes(self) -> int: ...
    def get_record_parts(self) -> tuple[int, int, bytes]: ...
    def get_record_parts_conditional(self, reqd_record: int) -> tuple[int | None, int, bytes]: ...
    def get_sheet(self, sh_number: int, update_pos: bool = True) -> Sheet: ...
    def get_sheets(self) -> None: ...
    def fake_globals_get_sheet(self) -> None: ...
    def handle_boundsheet(self, data: bytes) -> None: ...
    def handle_builtinfmtcount(self, data: bytes) -> None: ...
    def derive_encoding(self) -> str: ...
    def handle_codepage(self, data: bytes) -> None: ...
    def handle_country(self, data: bytes) -> None: ...
    def handle_datemode(self, data: bytes) -> None: ...
    def handle_externname(self, data: bytes) -> None: ...
    def handle_externsheet(self, data: bytes) -> None: ...
    def handle_filepass(self, data: bytes) -> None: ...
    def handle_name(self, data: bytes) -> None: ...
    def names_epilogue(self) -> None: ...
    def handle_obj(self, data: bytes) -> None: ...
    def handle_supbook(self, data: bytes) -> None: ...
    def handle_sheethdr(self, data: bytes) -> None: ...
    def handle_sheetsoffset(self, data: bytes) -> None: ...
    def handle_sst(self, data: bytes) -> None: ...
    def handle_writeaccess(self, data: bytes) -> None: ...
    def parse_globals(self) -> None: ...
    def read(self, pos: int, length: int) -> bytes: ...
    def getbof(self, rqd_stream: int) -> int | None: ...

# Helper functions
def expand_cell_address(inrow: int, incol: int) -> tuple[int, int, int, int]: ...
def display_cell_address(rowx: int, colx: int, relrow: int, relcol: int) -> str: ...
def unpack_SST_table(datatab: list[bytes], nstrings: int) -> tuple[list[str], dict[int, list[tuple[int, int]]]]:
    """Return list of strings"""
