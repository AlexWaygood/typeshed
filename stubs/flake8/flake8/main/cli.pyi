"""Command-line implementation of flake8."""

from collections.abc import Sequence

def main(argv: Sequence[str] | None = None) -> int:
    """Execute the main bit of the application.

    This handles the creation of an instance of :class:`Application`, runs it,
    and then exits the application.

    :param argv:
        The arguments to be passed to the application for parsing.
    """
