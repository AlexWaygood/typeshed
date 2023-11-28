import sys
from _typeshed import SizedBuffer, StrPath
from collections.abc import Callable, Iterable, Iterator
from io import TextIOWrapper
from typing import IO, Protocol, overload
from typing_extensions import Literal, Self, TypeAlias

_DateTuple: TypeAlias = tuple[int, int, int, int, int, int]
_ReadWriteMode: TypeAlias = Literal["r", "w"]
_ReadWriteBinaryMode: TypeAlias = Literal["r", "w", "rb", "wb"]
_ZipFileMode: TypeAlias = Literal["r", "w", "x", "a"]

class _ZipStream(Protocol):
    def read(self, __n: int) -> bytes: ...
    # The following methods are optional:
    # def seekable(self) -> bool: ...
    # def tell(self) -> int: ...
    # def seek(self, __n: int) -> object: ...

class _Writer(Protocol):
    def write(self, __s: str) -> object: ...

class ZipFile:
    if sys.version_info >= (3, 11):
        @overload
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: Literal["r"] = "r",
            compression: int = 0,
            allowZip64: bool = True,
            compresslevel: int | None = None,
            *,
            strict_timestamps: bool = True,
            metadata_encoding: str | None,
        ) -> None: ...
        @overload
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = "r",
            compression: int = 0,
            allowZip64: bool = True,
            compresslevel: int | None = None,
            *,
            strict_timestamps: bool = True,
            metadata_encoding: None = None,
        ) -> None: ...
    elif sys.version_info >= (3, 8):
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = "r",
            compression: int = 0,
            allowZip64: bool = True,
            compresslevel: int | None = None,
            *,
            strict_timestamps: bool = True,
        ) -> None: ...
    else:
        def __init__(
            self,
            file: StrPath | IO[bytes],
            mode: _ZipFileMode = "r",
            compression: int = 0,
            allowZip64: bool = True,
            compresslevel: int | None = None,
        ) -> None: ...

class ZipInfo:
    date_time: _DateTuple
    def __init__(self, filename: str = "NoName", date_time: _DateTuple = (1980, 1, 1, 0, 0, 0)) -> None: ...
    if sys.version_info >= (3, 8):
        @classmethod
        def from_file(cls, filename: StrPath, arcname: StrPath | None = None, *, strict_timestamps: bool = True) -> Self: ...
    else:
        @classmethod
        def from_file(cls, filename: StrPath, arcname: StrPath | None = None) -> Self: ...

if sys.version_info >= (3, 8):
    class Path:
        def __init__(self, root: ZipFile | StrPath | IO[bytes], at: str = "") -> None: ...
        @property
        def name(self) -> str: ...
        if sys.version_info >= (3, 11):
            @property
            def suffix(self) -> str: ...
            @property
            def suffixes(self) -> list[str]: ...
            @property
            def stem(self) -> str: ...

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
        if sys.version_info >= (3, 12):
            def glob(self, pattern: str) -> Iterator[Self]: ...
            def rglob(self, pattern: str) -> Iterator[Self]: ...
            def is_symlink(self) -> Literal[False]: ...
            def relative_to(self, other: Path, *extra: StrPath) -> str: ...
            def match(self, path_pattern: str) -> bool: ...
            def __eq__(self, other: object) -> bool: ...
            def __hash__(self) -> int: ...

        def __truediv__(self, add: StrPath) -> Path: ...
