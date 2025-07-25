"""Module containing shims around Flake8 2.x behaviour.

Previously, users would import :func:`get_style_guide` from ``flake8.engine``.
In 3.0 we no longer have an "engine" module but we maintain the API from it.
"""

import argparse
from _typeshed import Unused
from typing import Any

from ..formatting import base as formatter
from ..main import application as app

__all__ = ("get_style_guide",)

class Report:
    """Public facing object that mimic's Flake8 2.0's API.

    .. note::

        There are important changes in how this object behaves compared to
        the object provided in Flake8 2.x.

    .. warning::

        This should not be instantiated by users.

    .. versionchanged:: 3.0.0
    """

    def __init__(self, application: app.Application) -> None:
        """Initialize the Report for the user.

        .. warning:: This should not be instantiated by users.
        """

    @property
    def total_errors(self) -> int:
        """Return the total number of errors."""

    def get_statistics(self, violation: str) -> list[str]:
        """Get the list of occurrences of a violation.

        :returns:
            List of occurrences of a violation formatted as:
            {Count} {Error Code} {Message}, e.g.,
            ``8 E531 Some error message about the error``
        """

class StyleGuide:
    """Public facing object that mimic's Flake8 2.0's StyleGuide.

    .. note::

        There are important changes in how this object behaves compared to
        the StyleGuide object provided in Flake8 2.x.

    .. warning::

        This object should not be instantiated directly by users.

    .. versionchanged:: 3.0.0
    """

    def __init__(self, application: app.Application) -> None:
        """Initialize our StyleGuide."""

    @property
    def options(self) -> argparse.Namespace:
        """Return application's options.

        An instance of :class:`argparse.Namespace` containing parsed options.
        """

    @property
    def paths(self) -> list[str]:
        """Return the extra arguments passed as paths."""

    def check_files(self, paths: list[str] | None = None) -> Report:
        """Run collected checks on the files provided.

        This will check the files passed in and return a :class:`Report`
        instance.

        :param paths:
            List of filenames (or paths) to check.
        :returns:
            Object that mimic's Flake8 2.0's Reporter class.
        """

    def excluded(self, filename: str, parent: str | None = None) -> bool:
        """Determine if a file is excluded.

        :param filename:
            Path to the file to check if it is excluded.
        :param parent:
            Name of the parent directory containing the file.
        :returns:
            True if the filename is excluded, False otherwise.
        """

    def init_report(self, reporter: type[formatter.BaseFormatter] | None = None) -> None:
        """Set up a formatter for this run of Flake8."""

    def input_file(self, filename: str, lines: Unused = None, expected: Unused = None, line_offset: Unused = 0) -> Report:
        """Run collected checks on a single file.

        This will check the file passed in and return a :class:`Report`
        instance.

        :param filename:
            The path to the file to check.
        :param lines:
            Ignored since Flake8 3.0.
        :param expected:
            Ignored since Flake8 3.0.
        :param line_offset:
            Ignored since Flake8 3.0.
        :returns:
            Object that mimic's Flake8 2.0's Reporter class.
        """

def get_style_guide(**kwargs: Any) -> StyleGuide:
    """Provision a StyleGuide for use.

    :param \\*\\*kwargs:
        Keyword arguments that provide some options for the StyleGuide.
    :returns:
        An initialized StyleGuide
    """
