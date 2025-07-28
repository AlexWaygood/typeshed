"""Checker Manager and Checker classes."""

import argparse
import tokenize
from _typeshed import Incomplete
from collections.abc import Sequence
from logging import Logger
from typing import Any
from typing_extensions import TypeAlias

from .plugins.finder import Checkers, LoadedPlugin
from .processor import _LogicalMapping
from .style_guide import StyleGuideManager

Results: TypeAlias = list[tuple[str, int, int, str, str | None]]

LOG: Logger
SERIAL_RETRY_ERRNOS: Incomplete

class Manager:
    """Manage the parallelism and checker instances for each plugin and file.

    This class will be responsible for the following:

    - Determining the parallelism of Flake8, e.g.:

      * Do we use :mod:`multiprocessing` or is it unavailable?

      * Do we automatically decide on the number of jobs to use or did the
        user provide that?

    - Falling back to a serial way of processing files if we run into an
      OSError related to :mod:`multiprocessing`

    - Organizing the results of each checker so we can group the output
      together and make our output deterministic.
    """

    style_guide: Incomplete
    options: Incomplete
    plugins: Incomplete
    jobs: Incomplete
    statistics: Incomplete
    exclude: Incomplete
    argv: Incomplete
    results: Incomplete
    def __init__(self, style_guide: StyleGuideManager, plugins: Checkers, argv: Sequence[str]) -> None:
        """Initialize our Manager instance."""

    def report(self) -> tuple[int, int]:
        """Report all of the errors found in the managed file checkers.

        This iterates over each of the checkers and reports the errors sorted
        by line number.

        :returns:
            A tuple of the total results found and the results reported.
        """

    def run_parallel(self) -> None:
        """Run the checkers in parallel."""

    def run_serial(self) -> None:
        """Run the checkers in serial."""

    def run(self) -> None:
        """Run all the checkers.

        This will intelligently decide whether to run the checks in parallel
        or whether to run them in serial.

        If running the checks in parallel causes a problem (e.g.,
        :issue:`117`) this also implements fallback to serial processing.
        """
    filenames: Incomplete
    def start(self) -> None:
        """Start checking files.

        :param paths:
            Path names to check. This is passed directly to
            :meth:`~Manager.make_checkers`.
        """

    def stop(self) -> None:
        """Stop checking files."""

class FileChecker:
    """Manage running checks for a file and aggregate the results."""

    options: Incomplete
    filename: Incomplete
    plugins: Incomplete
    results: Incomplete
    statistics: Incomplete
    processor: Incomplete
    display_name: Incomplete
    should_process: bool
    def __init__(self, *, filename: str, plugins: Checkers, options: argparse.Namespace) -> None:
        """Initialize our file checker."""

    def report(self, error_code: str | None, line_number: int, column: int, text: str) -> str:
        """Report an error by storing it in the results list."""

    def run_check(self, plugin: LoadedPlugin, **arguments: Any) -> Any:
        """Run the check in a single plugin."""

    def run_ast_checks(self) -> None:
        """Run all checks expecting an abstract syntax tree."""

    def run_logical_checks(self) -> None:
        """Run all checks expecting a logical line."""

    def run_physical_checks(self, physical_line: str) -> None:
        """Run all checks for a given physical line.

        A single physical check may return multiple errors.
        """

    def process_tokens(self) -> None:
        """Process tokens and trigger checks.

        Instead of using this directly, you should use
        :meth:`flake8.checker.FileChecker.run_checks`.
        """

    def run_checks(self) -> tuple[str, Results, dict[str, int]]:
        """Run checks against the file."""

    def handle_newline(self, token_type: int) -> None:
        """Handle the logic when encountering a newline token."""

    def check_physical_eol(self, token: tokenize.TokenInfo, prev_physical: str) -> None:
        """Run physical checks if and only if it is at the end of the line."""

def find_offset(offset: int, mapping: _LogicalMapping) -> tuple[int, int]:
    """Find the offset tuple for a single offset."""
