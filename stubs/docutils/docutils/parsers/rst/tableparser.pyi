"""
This module defines table parser classes,which parse plaintext-graphic tables
and produce a well-formed data structure suitable for building a CALS table.

:Classes:
    - `GridTableParser`: Parse fully-formed tables represented with a grid.
    - `SimpleTableParser`: Parse simple tables, delimited by top & bottom
      borders.

:Exception class: `TableMarkupError`

:Function:
    `update_dict_of_lists()`: Merge two dictionaries containing list values.
"""

from re import Pattern
from typing import ClassVar, Final
from typing_extensions import TypeAlias

from docutils import DataError
from docutils.statemachine import StringList

_Cell: TypeAlias = tuple[int, int, int, list[str]]
_Row: TypeAlias = list[_Cell | None]
_Colspecs: TypeAlias = list[int]

__docformat__: Final = "reStructuredText"

class TableMarkupError(DataError):
    """
    Raise if there is any problem with table markup.

    The keyword argument `offset` denotes the offset of the problem
    from the table's start line.
    """

    offset: int
    def __init__(self, *args, **kwargs) -> None: ...

class TableParser:
    """
    Abstract superclass for the common parts of the syntax-specific parsers.
    """

    head_body_separator_pat: ClassVar[Pattern[str] | None]
    double_width_pad_char: ClassVar[str]
    head_body_sep: int
    def parse(self, block: StringList) -> tuple[_Colspecs, list[_Row], list[_Row]]:
        """
        Analyze the text `block` and return a table data structure.

        Given a plaintext-graphic table in `block` (list of lines of text; no
        whitespace padding), parse the table, construct and return the data
        necessary to construct a CALS table or equivalent.

        Raise `TableMarkupError` if there is any problem with the markup.
        """

    def find_head_body_sep(self) -> None:
        """Look for a head/body row separator line; store the line index."""

class GridTableParser(TableParser):
    """
    Parse a grid table using `parse()`.

    Here's an example of a grid table::

        +------------------------+------------+----------+----------+
        | Header row, column 1   | Header 2   | Header 3 | Header 4 |
        +========================+============+==========+==========+
        | body row 1, column 1   | column 2   | column 3 | column 4 |
        +------------------------+------------+----------+----------+
        | body row 2             | Cells may span columns.          |
        +------------------------+------------+---------------------+
        | body row 3             | Cells may  | - Table cells       |
        +------------------------+ span rows. | - contain           |
        | body row 4             |            | - body elements.    |
        +------------------------+------------+---------------------+

    Intersections use '+', row separators use '-' (except for one optional
    head/body row separator, which uses '='), and column separators use '|'.

    Passing the above table to the `parse()` method will result in the
    following data structure::

        ([24, 12, 10, 10],
         [[(0, 0, 1, ['Header row, column 1']),
           (0, 0, 1, ['Header 2']),
           (0, 0, 1, ['Header 3']),
           (0, 0, 1, ['Header 4'])]],
         [[(0, 0, 3, ['body row 1, column 1']),
           (0, 0, 3, ['column 2']),
           (0, 0, 3, ['column 3']),
           (0, 0, 3, ['column 4'])],
          [(0, 0, 5, ['body row 2']),
           (0, 2, 5, ['Cells may span columns.']),
           None,
           None],
          [(0, 0, 7, ['body row 3']),
           (1, 0, 7, ['Cells may', 'span rows.', '']),
           (1, 1, 7, ['- Table cells', '- contain', '- body elements.']),
           None],
          [(0, 0, 9, ['body row 4']), None, None, None]])

    The first item is a list containing column widths (colspecs). The second
    item is a list of head rows, and the third is a list of body rows. Each
    row contains a list of cells. Each cell is either None (for a cell unused
    because of another cell's span), or a tuple. A cell tuple contains four
    items: the number of extra rows used by the cell in a vertical span
    (morerows); the number of extra columns used by the cell in a horizontal
    span (morecols); the line offset of the first line of the cell contents;
    and the cell contents, a list of lines of text.
    """

    head_body_separator_pat: ClassVar[Pattern[str]]
    block: StringList
    bottom: int
    right: int
    head_body_sep: int
    done: list[int]
    cells: list[_Cell]
    rowseps: dict[int, list[int]]
    colseps: dict[int, list[int]]
    def setup(self, block: StringList) -> None: ...
    def parse_table(self) -> None:
        """
        Start with a queue of upper-left corners, containing the upper-left
        corner of the table itself. Trace out one rectangular cell, remember
        it, and add its upper-right and lower-left corners to the queue of
        potential upper-left corners of further cells. Process the queue in
        top-to-bottom order, keeping track of how much of each text column has
        been seen.

        We'll end up knowing all the row and column boundaries, cell positions
        and their dimensions.
        """

    def mark_done(self, top: int, left: int, bottom: int, right: int) -> None:
        """For keeping track of how much of each text column has been seen."""

    def check_parse_complete(self) -> bool:
        """Each text column should have been completely seen."""

    def scan_cell(self, top: int, left: int) -> tuple[int, int, dict[int, list[int]], dict[int, list[int]]]:
        """Starting at the top-left corner, start tracing out a cell."""

    def scan_right(self, top: int, left: int) -> tuple[int, int, dict[int, list[int]], dict[int, list[int]]]:
        """
        Look for the top-right corner of the cell, and make note of all column
        boundaries ('+').
        """

    def scan_down(self, top: int, left: int, right: int) -> tuple[int, dict[int, list[int]], dict[int, list[int]]]:
        """
        Look for the bottom-right corner of the cell, making note of all row
        boundaries.
        """

    def scan_left(self, top: int, left: int, bottom: int, right: int) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
        """
        Noting column boundaries, look for the bottom-left corner of the cell.
        It must line up with the starting point.
        """

    def scan_up(self, top: int, left: int, bottom: int, right: int) -> dict[int, list[int]]:
        """
        Noting row boundaries, see if we can return to the starting point.
        """

    def structure_from_cells(self) -> tuple[_Colspecs, list[_Row], list[_Row]]:
        """
        From the data collected by `scan_cell()`, convert to the final data
        structure.
        """

class SimpleTableParser(TableParser):
    """
    Parse a simple table using `parse()`.

    Here's an example of a simple table::

        =====  =====
        col 1  col 2
        =====  =====
        1      Second column of row 1.
        2      Second column of row 2.
               Second line of paragraph.
        3      - Second column of row 3.

               - Second item in bullet
                 list (row 3, column 2).
        4 is a span
        ------------
        5
        =====  =====

    Top and bottom borders use '=', column span underlines use '-', column
    separation is indicated with spaces.

    Passing the above table to the `parse()` method will result in the
    following data structure, whose interpretation is the same as for
    `GridTableParser`::

        ([5, 25],
         [[(0, 0, 1, ['col 1']),
           (0, 0, 1, ['col 2'])]],
         [[(0, 0, 3, ['1']),
           (0, 0, 3, ['Second column of row 1.'])],
          [(0, 0, 4, ['2']),
           (0, 0, 4, ['Second column of row 2.',
                      'Second line of paragraph.'])],
          [(0, 0, 6, ['3']),
           (0, 0, 6, ['- Second column of row 3.',
                      '',
                      '- Second item in bullet',
                      '  list (row 3, column 2).'])],
          [(0, 1, 10, ['4 is a span'])],
          [(0, 0, 12, ['5']),
           (0, 0, 12, [''])]])
    """

    head_body_separator_pat: ClassVar[Pattern[str]]
    span_pat: ClassVar[Pattern[str]]
    block: StringList
    head_body_sep: int
    columns: list[tuple[int, int]]
    border_end: int
    table: tuple[list[int], list[_Row], list[_Row]]
    done: list[int]
    rowseps: dict[int, tuple[int]]
    colseps: dict[int, tuple[int]]
    def setup(self, block: StringList) -> None: ...
    def parse_table(self) -> None:
        """
        First determine the column boundaries from the top border, then
        process rows.  Each row may consist of multiple lines; accumulate
        lines until a row is complete.  Call `self.parse_row` to finish the
        job.
        """

    def parse_columns(self, line: str, offset: int) -> list[tuple[int, int]]:
        """
        Given a column span underline, return a list of (begin, end) pairs.
        """

    def init_row(self, colspec: list[tuple[int, int]], offset: int) -> list[_Cell]: ...
    def parse_row(self, lines: list[str], start: int, spanline: tuple[str, int] | None = None) -> None:
        """
        Given the text `lines` of a row, parse it and append to `self.table`.

        The row is parsed according to the current column spec (either
        `spanline` if provided or `self.columns`).  For each column, extract
        text from each line, and check for text in column margins.  Finally,
        adjust for insignificant whitespace.
        """

    def check_columns(self, lines: list[str], first_line: int, columns: list[tuple[int, int]]) -> None:
        """
        Check for text in column margins and text overflow in the last column.
        Raise TableMarkupError if anything but whitespace is in column margins.
        Adjust the end value for the last column if there is text overflow.
        """

    def structure_from_cells(self) -> tuple[_Colspecs, list[_Row], list[_Row]]: ...

def update_dict_of_lists(master: dict[int, list[int]], newdata: dict[int, list[int]]) -> None:
    """
    Extend the list values of `master` with those from `newdata`.

    Both parameters must be dictionaries containing list values.
    """
