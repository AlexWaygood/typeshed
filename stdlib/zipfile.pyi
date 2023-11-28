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
    filename: str | None
    debug: int
    comment: bytes
    filelist: list[ZipInfo]
    fp: IO[bytes] | None
    NameToInfo: dict[str, ZipInfo]
    start_dir: int  # undocumented
    compression: int  # undocumented
    compresslevel: int | None  # undocumented
    mode: _ZipFileMode  # undocumented
    pwd: bytes | None  # undocumented
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

    def close(self) -> None: ...
    def getinfo(self, name: str) -> ZipInfo: ...
    def infolist(self) -> list[ZipInfo]: ...
    def namelist(self) -> list[str]: ...
    def open(
        self, name: str | ZipInfo, mode: _ReadWriteMode = "r", pwd: bytes | None = None, *, force_zip64: bool = False
    ) -> IO[bytes]: ...
    def extract(self, member: str | ZipInfo, path: StrPath | None = None, pwd: bytes | None = None) -> str: ...
    def extractall(
        self, path: StrPath | None = None, members: Iterable[str | ZipInfo] | None = None, pwd: bytes | None = None
    ) -> None: ...
    def printdir(self, file: _Writer | None = None) -> None: ...
    def setpassword(self, pwd: bytes) -> None: ...
    def read(self, name: str | ZipInfo, pwd: bytes | None = None) -> bytes: ...
    def testzip(self) -> str | None: ...
    def write(
        self,
        filename: StrPath,
        arcname: StrPath | None = None,
        compress_type: int | None = None,
        compresslevel: int | None = None,
    ) -> None: ...
    def writestr(
        self,
        zinfo_or_arcname: str | ZipInfo,
        data: SizedBuffer | str,
        compress_type: int | None = None,
        compresslevel: int | None = None,
    ) -> None: ...
    if sys.version_info >= (3, 11):
        def mkdir(self, zinfo_or_directory_name: str | ZipInfo, mode: int = 0o777) -> None: ...

    def __del__(self) -> None: ...

class PyZipFile(ZipFile):
    def __init__(
        self, file: str | IO[bytes], mode: _ZipFileMode = "r", compression: int = 0, allowZip64: bool = True, optimize: int = -1
    ) -> None: ...
    def writepy(self, pathname: str, basename: str = "", filterfunc: Callable[[str], bool] | None = None) -> None: ...

class ZipInfo:
    filename: str
    date_time: _DateTuple
    compress_type: int
    comment: bytes
    extra: bytes
    create_system: int
    create_version: int
    extract_version: int
    reserved: int
    flag_bits: int
    volume: int
    internal_attr: int
    external_attr: int
    header_offset: int
    CRC: int
    compress_size: int
    file_size: int
    orig_filename: str  # undocumented
    def __init__(self, filename: str = "NoName", date_time: _DateTuple = (1980, 1, 1, 0, 0, 0)) -> None: ...
    if sys.version_info >= (3, 8):
        @classmethod
        def from_file(cls, filename: StrPath, arcname: StrPath | None = None, *, strict_timestamps: bool = True) -> Self: ...
    else:
        @classmethod
        def from_file(cls, filename: StrPath, arcname: StrPath | None = None) -> Self: ...

    def is_dir(self) -> bool: ...
    def FileHeader(self, zip64: bool | None = None) -> bytes: ...

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
