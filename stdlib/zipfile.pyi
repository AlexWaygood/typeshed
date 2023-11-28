from collections.abc import Iterator
from io import TextIOWrapper
from typing import IO, overload
from typing_extensions import Literal, Self, TypeAlias

_DateTuple: TypeAlias = tuple[int, int, int, int, int, int]
_ReadWriteBinaryMode: TypeAlias = Literal["r", "w", "rb", "wb"]

date_time: _DateTuple

class Path:
    def __init__(self, root: str | IO[bytes]) -> None: ...
    @property
    def name(self) -> str: ...
    @overload
    def open(
        self,
        mode: Literal["r", "w"] = "r",
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        line_buffering: bool = ...,
        write_through: bool = ...,
        *,
        pwd: bytes | None = None,
    ) -> TextIOWrapper: ...
    @overload
    def open(self, mode: Literal["rb", "wb"], *, pwd: bytes | None = None) -> IO[bytes]: ...
    def iterdir(self) -> Iterator[Self]: ...
    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    def exists(self) -> bool: ...
    def read_text(
        self,
        encoding: str | None = ...,
        errors: str | None = ...,
        newline: str | None = ...,
        line_buffering: bool = ...,
        write_through: bool = ...,
    ) -> str: ...
    def read_bytes(self) -> bytes: ...
    def joinpath(self, *other: str) -> Path: ...
    def __truediv__(self, add: str) -> Path: ...
