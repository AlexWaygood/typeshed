from typing import Any

class ImportExportError(Exception):
    """A generic exception for all others to extend."""

class FieldError(ImportExportError):
    """Raised when a field encounters an error."""

class WidgetError(ImportExportError):
    """Raised when there is a misconfiguration with a Widget."""

class ImportError(ImportExportError):
    error: Exception
    number: int | None
    row: dict[str, Any] | None
    def __init__(self, error: Exception, number: int | None = None, row: dict[str, Any] | None = None) -> None:
        """A wrapper for errors thrown from the import process.

        :param error: The underlying error that occurred.
        :param number: The row number of the row containing the error (if obtainable).
        :param row: The row containing the error (if obtainable).
        """
