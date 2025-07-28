"""Contains the Violation error class used internally."""

from logging import Logger
from typing import NamedTuple

LOG: Logger

class Violation(NamedTuple):
    """Class representing a violation reported by Flake8."""

    code: str
    filename: str
    line_number: int
    column_number: int
    text: str
    physical_line: str | None
    def is_inline_ignored(self, disable_noqa: bool) -> bool:
        """Determine if a comment has been added to ignore this line.

        :param disable_noqa:
            Whether or not users have provided ``--disable-noqa``.
        :returns:
            True if error is ignored in-line, False otherwise.
        """
