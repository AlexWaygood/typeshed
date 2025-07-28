"""Default formatting class for Flake8."""

from _typeshed import Incomplete

from ..violation import Violation
from .base import BaseFormatter

COLORS: dict[str, str]
COLORS_OFF: dict[str, str]

class SimpleFormatter(BaseFormatter):
    """Simple abstraction for Default and Pylint formatter commonality.

    Sub-classes of this need to define an ``error_format`` attribute in order
    to succeed. The ``format`` method relies on that attribute and expects the
    ``error_format`` string to use the old-style formatting strings with named
    parameters:

    * code
    * text
    * path
    * row
    * col

    """

    error_format: str
    def format(self, error: Violation) -> str | None:
        """Format and write error out.

        If an output filename is specified, write formatted errors to that
        file. Otherwise, print the formatted error to standard out.
        """

class Default(SimpleFormatter):
    """Default formatter for Flake8.

    This also handles backwards compatibility for people specifying a custom
    format string.
    """

    error_format: str
    def after_init(self) -> None:
        """Check for a custom format string."""

class Pylint(SimpleFormatter):
    """Pylint formatter for Flake8."""

    error_format: str

class FilenameOnly(SimpleFormatter):
    """Only print filenames, e.g., flake8 -q."""

    error_format: str
    filenames_already_printed: Incomplete
    def after_init(self) -> None:
        """Initialize our set of filenames."""

    def show_source(self, error: Violation) -> str | None:
        """Do not include the source code."""

    def format(self, error: Violation) -> str | None:
        """Ensure we only print each error once."""

class Nothing(BaseFormatter):
    """Print absolutely nothing."""

    def format(self, error: Violation) -> str | None:
        """Do nothing."""

    def show_source(self, error: Violation) -> str | None:
        """Do not print the source."""
