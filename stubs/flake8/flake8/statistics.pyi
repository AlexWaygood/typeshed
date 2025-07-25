"""Statistic collection logic for Flake8."""

from collections.abc import Generator
from typing import NamedTuple

from .violation import Violation

class Statistics:
    """Manager of aggregated statistics for a run of Flake8."""

    def __init__(self) -> None:
        """Initialize the underlying dictionary for our statistics."""

    def error_codes(self) -> list[str]:
        """Return all unique error codes stored.

        :returns:
            Sorted list of error codes.
        """

    def record(self, error: Violation) -> None:
        """Add the fact that the error was seen in the file.

        :param error:
            The Violation instance containing the information about the
            violation.
        """

    def statistics_for(self, prefix: str, filename: str | None = None) -> Generator[Statistic, None, None]:
        """Generate statistics for the prefix and filename.

        If you have a :class:`Statistics` object that has recorded errors,
        you can generate the statistics for a prefix (e.g., ``E``, ``E1``,
        ``W50``, ``W503``) with the optional filter of a filename as well.

        .. code-block:: python

            >>> stats = Statistics()
            >>> stats.statistics_for('E12',
                                     filename='src/flake8/statistics.py')
            <generator ...>
            >>> stats.statistics_for('W')
            <generator ...>

        :param prefix:
            The error class or specific error code to find statistics for.
        :param filename:
            (Optional) The filename to further filter results by.
        :returns:
            Generator of instances of :class:`Statistic`
        """

class Key(NamedTuple):
    """Simple key structure for the Statistics dictionary.

    To make things clearer, easier to read, and more understandable, we use a
    namedtuple here for all Keys in the underlying dictionary for the
    Statistics object.
    """

    filename: str
    code: str
    @classmethod
    def create_from(cls, error: Violation) -> Key:
        """Create a Key from :class:`flake8.violation.Violation`."""

    def matches(self, prefix: str, filename: str | None) -> bool:
        """Determine if this key matches some constraints.

        :param prefix:
            The error code prefix that this key's error code should start with.
        :param filename:
            The filename that we potentially want to match on. This can be
            None to only match on error prefix.
        :returns:
            True if the Key's code starts with the prefix and either filename
            is None, or the Key's filename matches the value passed in.
        """

class Statistic:
    """Simple wrapper around the logic of each statistic.

    Instead of maintaining a simple but potentially hard to reason about
    tuple, we create a class which has attributes and a couple
    convenience methods on it.
    """

    error_code: str
    filename: str
    message: str
    count: int
    def __init__(self, error_code: str, filename: str, message: str, count: int) -> None:
        """Initialize our Statistic."""

    @classmethod
    def create_from(cls, error: Violation) -> Statistic:
        """Create a Statistic from a :class:`flake8.violation.Violation`."""

    def increment(self) -> None:
        """Increment the number of times we've seen this error in this file."""
