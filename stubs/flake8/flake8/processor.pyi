"""Module containing our file processor that tokenizes a file for checks."""

from _typeshed import Incomplete
from argparse import Namespace
from ast import AST
from collections.abc import Generator
from logging import Logger
from tokenize import TokenInfo
from typing import Any, Final
from typing_extensions import TypeAlias

from .plugins.finder import LoadedPlugin

LOG: Logger
NEWLINE: Final[frozenset[int]]
SKIP_TOKENS: Final[frozenset[int]]

_LogicalMapping: TypeAlias = list[tuple[int, tuple[int, int]]]
_Logical: TypeAlias = tuple[list[str], list[str], _LogicalMapping]

class FileProcessor:
    """Processes a file and holds state.

    This processes a file by generating tokens, logical and physical lines,
    and AST trees. This also provides a way of passing state about the file
    to checks expecting that state. Any public attribute on this object can
    be requested by a plugin. The known public attributes are:

    - :attr:`blank_before`
    - :attr:`blank_lines`
    - :attr:`checker_state`
    - :attr:`indent_char`
    - :attr:`indent_level`
    - :attr:`line_number`
    - :attr:`logical_line`
    - :attr:`max_line_length`
    - :attr:`max_doc_length`
    - :attr:`multiline`
    - :attr:`noqa`
    - :attr:`previous_indent_level`
    - :attr:`previous_logical`
    - :attr:`previous_unindented_logical_line`
    - :attr:`tokens`
    - :attr:`file_tokens`
    - :attr:`total_lines`
    - :attr:`verbose`
    """

    noqa: bool
    options: Incomplete
    filename: Incomplete
    lines: Incomplete
    blank_before: int
    blank_lines: int
    checker_state: Incomplete
    hang_closing: Incomplete
    indent_char: Incomplete
    indent_level: int
    indent_size: Incomplete
    line_number: int
    logical_line: str
    max_line_length: Incomplete
    max_doc_length: Incomplete
    multiline: bool
    previous_indent_level: int
    previous_logical: str
    previous_unindented_logical_line: str
    tokens: Incomplete
    total_lines: Incomplete
    verbose: Incomplete
    statistics: Incomplete
    def __init__(self, filename: str, options: Namespace, lines: list[str] | None = None) -> None:
        """Initialize our file processor.

        :param filename: Name of the file to process
        """

    @property
    def file_tokens(self) -> list[TokenInfo]:
        """Return the complete set of tokens for a file."""

    def tstring_start(self, lineno: int) -> None:
        """Signal the beginning of an tstring."""

    def fstring_start(self, lineno: int) -> None:
        """Signal the beginning of an fstring."""

    def multiline_string(self, token: TokenInfo) -> Generator[str, None, None]:
        """Iterate through the lines of a multiline string."""

    def reset_blank_before(self) -> None:
        """Reset the blank_before attribute to zero."""

    def delete_first_token(self) -> None:
        """Delete the first token in the list of tokens."""

    def visited_new_blank_line(self) -> None:
        """Note that we visited a new blank line."""

    def update_state(self, mapping: _LogicalMapping) -> None:
        """Update the indent level based on the logical line mapping."""

    def update_checker_state_for(self, plugin: LoadedPlugin) -> None:
        """Update the checker_state attribute for the plugin."""

    def next_logical_line(self) -> None:
        """Record the previous logical line.

        This also resets the tokens list and the blank_lines count.
        """

    def build_logical_line_tokens(self) -> _Logical:
        """Build the mapping, comments, and logical line lists."""

    def build_ast(self) -> AST:
        """Build an abstract syntax tree from the list of lines."""

    def build_logical_line(self) -> tuple[str, str, _LogicalMapping]:
        """Build a logical line from the current tokens list."""

    def keyword_arguments_for(self, parameters: dict[str, bool], arguments: dict[str, Any]) -> dict[str, Any]:
        """Generate the keyword arguments for a list of parameters."""

    def generate_tokens(self) -> Generator[TokenInfo, None, None]:
        """Tokenize the file and yield the tokens."""

    def noqa_line_for(self, line_number: int) -> str | None:
        """Retrieve the line which will be used to determine noqa."""

    def next_line(self) -> str:
        """Get the next line from the list."""

    def read_lines(self) -> list[str]:
        """Read the lines for this file checker."""

    def read_lines_from_filename(self) -> list[str]:
        """Read the lines for a file."""

    def read_lines_from_stdin(self) -> list[str]:
        """Read the lines from standard in."""

    def should_ignore_file(self) -> bool:
        """Check if ``flake8: noqa`` is in the file to be ignored.

        :returns:
            True if a line matches :attr:`defaults.NOQA_FILE`,
            otherwise False
        """

    def strip_utf_bom(self) -> None:
        """Strip the UTF bom from the lines of the file."""

def is_eol_token(token: TokenInfo) -> bool:
    """Check if the token is an end-of-line token."""

def is_multiline_string(token: TokenInfo) -> bool:
    """Check if this is a multiline string."""

def token_is_newline(token: TokenInfo) -> bool:
    """Check if the token type is a newline token type."""

def count_parentheses(current_parentheses_count: int, token_text: str) -> int:
    """Count the number of parentheses."""

def expand_indent(line: str) -> int:
    """Return the amount of indentation.

    Tabs are expanded to the next multiple of 8.

    >>> expand_indent('    ')
    4
    >>> expand_indent('\\t')
    8
    >>> expand_indent('       \\t')
    8
    >>> expand_indent('        \\t')
    16
    """

def mutate_string(text: str) -> str:
    """Replace contents with 'xxx' to prevent syntax matching.

    >>> mutate_string('"abc"')
    '"xxx"'
    >>> mutate_string("'''abc'''")
    "'''xxx'''"
    >>> mutate_string("r'abc'")
    "r'xxx'"
    """
