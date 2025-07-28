from _typeshed import Incomplete, ReadableBuffer
from logging import Logger
from typing import IO, Any, ClassVar
from typing_extensions import Self, TypeAlias

Dataset: TypeAlias = Incomplete  # tablib.Dataset

logger: Logger

class Format:
    def get_title(self) -> type[Self]: ...
    def create_dataset(self, in_stream: str | bytes | IO[Any]) -> Dataset:
        """
        Create dataset from given string.
        """

    def export_data(self, dataset: Dataset, **kwargs: Any) -> Any:
        """
        Returns format representation for given dataset.
        """

    def is_binary(self) -> bool:
        """
        Returns if this format is binary.
        """

    def get_read_mode(self) -> str:
        """
        Returns mode for opening files.
        """

    def get_extension(self) -> str:
        """
        Returns extension for this format files.
        """

    def get_content_type(self) -> str: ...
    @classmethod
    def is_available(cls) -> bool: ...
    def can_import(self) -> bool: ...
    def can_export(self) -> bool: ...

class TablibFormat(Format):
    TABLIB_MODULE: ClassVar[str]
    CONTENT_TYPE: ClassVar[str]
    encoding: str | None
    def __init__(self, encoding: str | None = None) -> None: ...
    def get_format(self) -> type[Any]:
        """
        Import and returns tablib module.
        """

    def get_title(self) -> str: ...  # type: ignore[override]
    def create_dataset(self, in_stream: str | bytes | IO[Any], **kwargs: Any) -> Dataset: ...  # type: ignore[override]

class TextFormat(TablibFormat): ...

class CSV(TextFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> str: ...

class JSON(TextFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> str: ...

class YAML(TextFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> str: ...

class TSV(TextFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> str: ...

class ODS(TextFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> bytes: ...

class HTML(TextFormat): ...

class XLS(TablibFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> bytes: ...
    def create_dataset(self, in_stream: bytes) -> Dataset:  # type: ignore[override]
        """
        Create dataset from first sheet.
        """

class XLSX(TablibFormat):
    def export_data(self, dataset: Dataset, **kwargs: Any) -> bytes: ...
    def create_dataset(self, in_stream: ReadableBuffer) -> Dataset:  # type: ignore[override]
        """
        Create dataset from first sheet.
        """

DEFAULT_FORMATS: list[type[Format]]
BINARY_FORMATS: list[type[Format]]
