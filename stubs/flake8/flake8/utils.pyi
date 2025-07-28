"""Utility methods for flake8."""

import logging
from collections.abc import Sequence
from re import Pattern
from typing import Final, NamedTuple

COMMA_SEPARATED_LIST_RE: Final[Pattern[str]]
LOCAL_PLUGIN_LIST_RE: Final[Pattern[str]]
NORMALIZE_PACKAGE_NAME_RE: Final[Pattern[str]]

def parse_comma_separated_list(value: str, regexp: Pattern[str] = ...) -> list[str]:
    """Parse a comma-separated list.

    :param value:
        String to be parsed and normalized.
    :param regexp:
        Compiled regular expression used to split the value when it is a
        string.
    :returns:
        List of values with whitespace stripped.
    """

class _Token(NamedTuple):
    """_Token(tp, src)"""

    tp: str
    src: str

def parse_files_to_codes_mapping(value_: Sequence[str] | str) -> list[tuple[str, list[str]]]:
    """Parse a files-to-codes mapping.

    A files-to-codes mapping a sequence of values specified as
    `filenames list:codes list ...`.  Each of the lists may be separated by
    either comma or whitespace tokens.

    :param value: String to be parsed and normalized.
    """

def normalize_paths(paths: Sequence[str], parent: str = ".") -> list[str]:
    """Normalize a list of paths relative to a parent directory.

    :returns:
        The normalized paths.
    """

def normalize_path(path: str, parent: str = ".") -> str:
    """Normalize a single-path.

    :returns:
        The normalized path.
    """

def stdin_get_value() -> str:
    """Get and cache it so plugins can use it."""

def stdin_get_lines() -> list[str]:
    """Return lines of stdin split according to file splitting."""

def is_using_stdin(paths: list[str]) -> bool:
    """Determine if we're going to read from stdin.

    :param paths:
        The paths that we're going to check.
    :returns:
        True if stdin (-) is in the path, otherwise False
    """

def fnmatch(filename: str, patterns: Sequence[str]) -> bool:
    """Wrap :func:`fnmatch.fnmatch` to add some functionality.

    :param filename:
        Name of the file we're trying to match.
    :param patterns:
        Patterns we're using to try to match the filename.
    :param default:
        The default value if patterns is empty
    :returns:
        True if a pattern matches the filename, False if it doesn't.
        ``True`` if patterns is empty.
    """

def matches_filename(path: str, patterns: Sequence[str], log_message: str, logger: logging.Logger) -> bool:
    """Use fnmatch to discern if a path exists in patterns.

    :param path:
        The path to the file under question
    :param patterns:
        The patterns to match the path against.
    :param log_message:
        The message used for logging purposes.
    :returns:
        True if path matches patterns, False otherwise
    """

def get_python_version() -> str:
    """Find and format the python implementation and version.

    :returns:
        Implementation name, version, and platform as a string.
    """

def normalize_pypi_name(s: str) -> str:
    """Normalize a distribution name according to PEP 503."""
