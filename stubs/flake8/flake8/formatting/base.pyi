"""The base class and interface for all formatting plugins."""

import argparse
from _typeshed import Incomplete

from ..statistics import Statistics
from ..violation import Violation as Violation

class BaseFormatter:
    """Class defining the formatter interface.

    .. attribute:: options

        The options parsed from both configuration files and the command-line.

    .. attribute:: filename

        If specified by the user, the path to store the results of the run.

    .. attribute:: output_fd

        Initialized when the :meth:`start` is called. This will be a file
        object opened for writing.

    .. attribute:: newline

        The string to add to the end of a line. This is only used when the
        output filename has been specified.
    """

    options: Incomplete
    filename: Incomplete
    output_fd: Incomplete
    newline: str
    color: Incomplete
    def __init__(self, options: argparse.Namespace) -> None:
        """Initialize with the options parsed from config and cli.

        This also calls a hook, :meth:`after_init`, so subclasses do not need
        to call super to call this method.

        :param options:
            User specified configuration parsed from both configuration files
            and the command-line interface.
        """

    def after_init(self) -> None:
        """Initialize the formatter further."""

    def beginning(self, filename: str) -> None:
        """Notify the formatter that we're starting to process a file.

        :param filename:
            The name of the file that Flake8 is beginning to report results
            from.
        """

    def finished(self, filename: str) -> None:
        """Notify the formatter that we've finished processing a file.

        :param filename:
            The name of the file that Flake8 has finished reporting results
            from.
        """

    def start(self) -> None:
        """Prepare the formatter to receive input.

        This defaults to initializing :attr:`output_fd` if :attr:`filename`
        """

    def handle(self, error: Violation) -> None:
        """Handle an error reported by Flake8.

        This defaults to calling :meth:`format`, :meth:`show_source`, and
        then :meth:`write`. To extend how errors are handled, override this
        method.

        :param error:
            This will be an instance of
            :class:`~flake8.violation.Violation`.
        """

    def format(self, error: Violation) -> str | None:
        """Format an error reported by Flake8.

        This method **must** be implemented by subclasses.

        :param error:
            This will be an instance of
            :class:`~flake8.violation.Violation`.
        :returns:
            The formatted error string.
        """

    def show_statistics(self, statistics: Statistics) -> None:
        """Format and print the statistics."""

    def show_benchmarks(self, benchmarks: list[tuple[str, float]]) -> None:
        """Format and print the benchmarks."""

    def show_source(self, error: Violation) -> str | None:
        """Show the physical line generating the error.

        This also adds an indicator for the particular part of the line that
        is reported as generating the problem.

        :param error:
            This will be an instance of
            :class:`~flake8.violation.Violation`.
        :returns:
            The formatted error string if the user wants to show the source.
            If the user does not want to show the source, this will return
            ``None``.
        """

    def write(self, line: str | None, source: str | None) -> None:
        """Write the line either to the output file or stdout.

        This handles deciding whether to write to a file or print to standard
        out for subclasses. Override this if you want behaviour that differs
        from the default.

        :param line:
            The formatted string to print or write.
        :param source:
            The source code that has been formatted and associated with the
            line of output.
        """

    def _write(self, output: str) -> None:
        """Handle logic of whether to use an output file or print()."""

    def stop(self) -> None:
        """Clean up after reporting is finished."""
