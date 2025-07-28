from _typeshed import Incomplete
from collections import OrderedDict
from collections.abc import Iterator
from functools import cached_property
from typing import Any, ClassVar, Literal
from typing_extensions import TypeAlias

from django.core.exceptions import ValidationError
from django.db.models import Model

Dataset: TypeAlias = Incomplete  # tablib.Dataset

class Error:
    """
    Base class representing an Error arising from error during data import.
    """

    error: Exception
    row: dict[str, Any]
    number: int | None
    def __init__(self, error: Exception, row: dict[str, Any] | None = None, number: int | None = None) -> None:
        """
        :param error: Instance of an Exception class.
        :param row: The row as a dict of fields and values (optional).
        :param number: The row number (optional).
        """

    @cached_property
    def traceback(self) -> str: ...

_ImportType: TypeAlias = Literal["update", "new", "delete", "skip", "error", "invalid"]

class RowResult:
    """Container for values relating to a row import."""

    IMPORT_TYPE_UPDATE: ClassVar[Literal["update"]]
    IMPORT_TYPE_NEW: ClassVar[Literal["new"]]
    IMPORT_TYPE_DELETE: ClassVar[Literal["delete"]]
    IMPORT_TYPE_SKIP: ClassVar[Literal["skip"]]
    IMPORT_TYPE_ERROR: ClassVar[Literal["error"]]
    IMPORT_TYPE_INVALID: ClassVar[Literal["invalid"]]
    valid_import_types: frozenset[_ImportType]
    errors: list[Error]
    validation_error: ValidationError | None
    diff: list[str] | None
    import_type: _ImportType
    row_values: dict[str, Any]
    object_id: Any | None
    object_repr: str | None
    instance: Model
    original: Model
    def __init__(self) -> None: ...
    def add_instance_info(self, instance: Model) -> None: ...
    def is_update(self) -> bool:
        """
        :return: ``True`` if import type is 'update', otherwise ``False``.
        """

    def is_new(self) -> bool:
        """
        :return: ``True`` if import type is 'new', otherwise ``False``.
        """

    def is_delete(self) -> bool:
        """
        :return: ``True`` if import type is 'delete', otherwise ``False``.
        """

    def is_skip(self) -> bool:
        """
        :return: ``True`` if import type is 'skip', otherwise ``False``.
        """

    def is_error(self) -> bool:
        """
        :return: ``True`` if import type is 'error', otherwise ``False``.
        """

    def is_invalid(self) -> bool:
        """
        :return: ``True`` if import type is 'invalid', otherwise ``False``.
        """

    def is_valid(self) -> bool:
        """
        :return: ``True`` if import type is not 'error' or 'invalid', otherwise
          ``False``.
        """

class ErrorRow:
    """A row that resulted in one or more errors being raised during import."""

    number: int
    errors: list[Error]
    def __init__(self, number: int, errors: list[Error]) -> None: ...

class InvalidRow:
    """A row that resulted in one or more ``ValidationError``
    being raised during import.
    """

    number: int
    error: ValidationError
    values: tuple[Any, ...]
    error_dict: dict[str, list[str]]
    def __init__(self, number: int, validation_error: ValidationError, values: tuple[Any, ...]) -> None: ...
    @property
    def field_specific_errors(self) -> dict[str, list[str]]:
        """Returns a dictionary of field-specific validation errors for this row."""

    @property
    def non_field_specific_errors(self) -> list[str]:
        """Returns a list of non field-specific validation errors for this row."""

    @property
    def error_count(self) -> int:
        """Returns the total number of validation errors for this row."""

class Result:
    base_errors: list[Error]
    diff_headers: list[str]
    rows: list[RowResult]
    invalid_rows: list[InvalidRow]
    error_rows: list[ErrorRow]
    failed_dataset: Dataset
    totals: OrderedDict[_ImportType, int]
    total_rows: int
    def __init__(self) -> None: ...
    def valid_rows(self) -> list[RowResult]: ...
    def append_row_result(self, row_result: RowResult) -> None: ...
    def append_base_error(self, error: Error) -> None: ...
    def add_dataset_headers(self, headers: list[str] | None) -> None: ...
    def append_failed_row(self, row: dict[str, Any], error: Exception) -> None: ...
    def append_invalid_row(self, number: int, row: dict[str, Any], validation_error: ValidationError) -> None: ...
    def append_error_row(self, number: int, row: dict[str, Any], errors: list[Error]) -> None: ...
    def increment_row_result_total(self, row_result: RowResult) -> None: ...
    def row_errors(self) -> list[tuple[int, Any]]: ...
    def has_errors(self) -> bool:
        """Returns a boolean indicating whether the import process resulted in
        any critical (non-validation) errors for this result.
        """

    def has_validation_errors(self) -> bool:
        """Returns a boolean indicating whether the import process resulted in
        any validation errors for this result.
        """

    def __iter__(self) -> Iterator[RowResult]: ...
