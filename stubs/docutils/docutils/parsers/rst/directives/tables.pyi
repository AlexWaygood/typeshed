"""
Directives for table elements.
"""

import csv
from _typeshed import Incomplete
from collections.abc import Callable
from typing import ClassVar, Final

from docutils.parsers.rst import Directive

__docformat__: Final = "reStructuredText"

def align(argument): ...

class Table(Directive):
    """
    Generic table base class.
    """

    option_spec: ClassVar[dict[str, Callable[[str], str | list[str]]]]
    def make_title(self): ...
    def check_table_dimensions(self, rows, header_rows, stub_columns) -> None: ...
    def set_table_width(self, table_node) -> None: ...
    @property
    def widths(self): ...
    def get_column_widths(self, n_cols): ...
    def extend_short_rows_with_empty_cells(self, columns, parts) -> None: ...

class RSTTable(Table):
    """
    Class for the `"table" directive`__ for formal tables using rST syntax.

    __ https://docutils.sourceforge.io/docs/ref/rst/directives.html
    """

    def run(self): ...

class CSVTable(Table):
    class DocutilsDialect(csv.Dialect):
        """CSV dialect for `csv_table` directive."""

        delimiter: str
        quotechar: str
        doublequote: bool
        skipinitialspace: bool
        strict: bool
        lineterminator: str
        quoting: Incomplete
        escapechar: Incomplete
        def __init__(self, options) -> None: ...

    class HeaderDialect(csv.Dialect):
        """
        CSV dialect used for the "header" option data.

        Deprecated. Will be removed in Docutils 0.22.
        """

        delimiter: str
        quotechar: str
        escapechar: str
        doublequote: bool
        skipinitialspace: bool
        strict: bool
        lineterminator: str
        quoting: Incomplete
        def __init__(self) -> None: ...

    @staticmethod
    def check_requirements() -> None: ...
    def process_header_option(self): ...
    def run(self): ...
    def get_csv_data(self):
        """
        Get CSV data from the directive content, from an external
        file, or from a URL reference.
        """

    @staticmethod
    def decode_from_csv(s): ...
    @staticmethod
    def encode_for_csv(s): ...
    def parse_csv_data_into_rows(self, csv_data, dialect, source): ...

class ListTable(Table):
    """
    Implement tables whose data is encoded as a uniform two-level bullet list.
    For further ideas, see
    https://docutils.sourceforge.io/docs/dev/rst/alternatives.html#list-driven-tables
    """

    def run(self): ...
    def check_list_content(self, node): ...
    def build_table_from_list(self, table_data, col_widths, header_rows, stub_columns): ...
