import sys
from _typeshed import SupportsWrite
from typing import Final

from . import timemachine as timemachine
from .biffh import (
    XL_CELL_BLANK as XL_CELL_BLANK,
    XL_CELL_BOOLEAN as XL_CELL_BOOLEAN,
    XL_CELL_DATE as XL_CELL_DATE,
    XL_CELL_EMPTY as XL_CELL_EMPTY,
    XL_CELL_ERROR as XL_CELL_ERROR,
    XL_CELL_NUMBER as XL_CELL_NUMBER,
    XL_CELL_TEXT as XL_CELL_TEXT,
    biff_text_from_num as biff_text_from_num,
    error_text_from_code as error_text_from_code,
)
from .book import Book as Book, colname as colname, open_workbook_xls as open_workbook_xls
from .formula import *
from .info import __VERSION__ as __VERSION__, __version__ as __version__
from .sheet import empty_cell as empty_cell
from .xldate import XLDateError as XLDateError, xldate_as_datetime as xldate_as_datetime, xldate_as_tuple as xldate_as_tuple

FILE_FORMAT_DESCRIPTIONS: Final[dict[str, str]]
ZIP_SIGNATURE: Final[bytes]
PEEK_SIZE: Final[int]

def inspect_format(path: str | None = None, content: bytes | None = None) -> str | None:
    """
    Inspect the content at the supplied path or the :class:`bytes` content provided
    and return the file's type as a :class:`str`, or ``None`` if it cannot
    be determined.

    :param path:
      A :class:`string <str>` path containing the content to inspect.
      ``~`` will be expanded.

    :param content:
      The :class:`bytes` content to inspect.

    :returns:
       A :class:`str`, or ``None`` if the format cannot be determined.
       The return value can always be looked up in :data:`FILE_FORMAT_DESCRIPTIONS`
       to return a human-readable description of the format found.
    """

def open_workbook(
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
) -> Book:
    """
    Open a spreadsheet file for data extraction.

    :param filename: The path to the spreadsheet file to be opened.

    :param logfile: An open file to which messages and diagnostics are written.

    :param verbosity: Increases the volume of trace material written to the
                      logfile.

    :param use_mmap:

      Whether to use the mmap module is determined heuristically.
      Use this arg to override the result.

      Current heuristic: mmap is used if it exists.

    :param file_contents:

      A string or an :class:`mmap.mmap` object or some other behave-alike
      object. If ``file_contents`` is supplied, ``filename`` will not be used,
      except (possibly) in messages.

    :param encoding_override:

      Used to overcome missing or bad codepage information
      in older-version files. See :doc:`unicode`.

    :param formatting_info:

      The default is ``False``, which saves memory.
      In this case, "Blank" cells, which are those with their own formatting
      information but no data, are treated as empty by ignoring the file's
      ``BLANK`` and ``MULBLANK`` records.
      This cuts off any bottom or right "margin" of rows of empty or blank
      cells.
      Only :meth:`~xlrd.sheet.Sheet.cell_value` and
      :meth:`~xlrd.sheet.Sheet.cell_type` are available.

      When ``True``, formatting information will be read from the spreadsheet
      file. This provides all cells, including empty and blank cells.
      Formatting information is available for each cell.

      Note that this will raise a NotImplementedError when used with an
      xlsx file.

    :param on_demand:

      Governs whether sheets are all loaded initially or when demanded
      by the caller. See :doc:`on_demand`.

    :param ragged_rows:

      The default of ``False`` means all rows are padded out with empty cells so
      that all rows have the same size as found in
      :attr:`~xlrd.sheet.Sheet.ncols`.

      ``True`` means that there are no empty cells at the ends of rows.
      This can result in substantial memory savings if rows are of widely
      varying sizes. See also the :meth:`~xlrd.sheet.Sheet.row_len` method.


    :param ignore_workbook_corruption:

      This option allows to read corrupted workbooks.
      When ``False`` you may face CompDocError: Workbook corruption.
      When ``True`` that exception will be ignored.

    :returns: An instance of the :class:`~xlrd.book.Book` class.
    """

def dump(filename: str, outfile: SupportsWrite[str] = sys.stdout, unnumbered: bool = False) -> None:
    """
    For debugging: dump an XLS file's BIFF records in char & hex.

    :param filename: The path to the file to be dumped.
    :param outfile: An open file, to which the dump is written.
    :param unnumbered: If true, omit offsets (for meaningful diffs).
    """

def count_records(filename: str, outfile: SupportsWrite[str] = sys.stdout) -> None:
    """
    For debugging and analysis: summarise the file's BIFF records.
    ie: produce a sorted file of ``(record_name, count)``.

    :param filename: The path to the file to be summarised.
    :param outfile: An open file, to which the summary is written.
    """
