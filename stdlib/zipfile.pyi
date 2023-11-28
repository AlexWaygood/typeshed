import sys
from _typeshed import StrPath
from collections.abc import Iterator
from io import TextIOWrapper
from typing import IO, overload
from typing_extensions import Literal, Self, TypeAlias

_DateTuple: TypeAlias = tuple[int, int, int, int, int, int]
_ReadWriteBinaryMode: TypeAlias = Literal["r", "w", "rb", "wb"]

class ZipFile: ...

class ZipInfo:
    date_time: _DateTuple

class Path:
    def __init__(self, root: ZipFile | StrPath | IO[bytes], at: str = "") -> None: ...
    @property
    def name(self) -> str: ...

    if sys.version_info >= (3, 9):
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
    else:
        def open(
            self, mode: _ReadWriteBinaryMode = "r", pwd: bytes | None = None, *, force_zip64: bool = False
        ) -> IO[bytes]: ...

    if sys.version_info >= (3, 10):
        def iterdir(self) -> Iterator[Self]: ...
    else:
        def iterdir(self) -> Iterator[Path]: ...

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
    if sys.version_info >= (3, 10):
        def joinpath(self, *other: StrPath) -> Path: ...
    else:
        def joinpath(self, add: StrPath) -> Path: ...  # undocumented

    def __truediv__(self, add: StrPath) -> Path: ...
