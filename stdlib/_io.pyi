import builtins
import codecs
import sys
from _typeshed import FileDescriptorOrPath, MaybeNone, ReadableBuffer, WriteableBuffer
from collections.abc import Callable, Iterable, Iterator
from io import BufferedIOBase, RawIOBase, TextIOBase, UnsupportedOperation as UnsupportedOperation
from os import _Opener
from types import TracebackType
from typing import IO, Any, BinaryIO, Final, Generic, Literal, Protocol, TextIO, TypeVar, overload, type_check_only
from typing_extensions import Self

_T = TypeVar("_T")

DEFAULT_BUFFER_SIZE: Final = 8192

open = builtins.open

def open_code(path: str) -> IO[bytes]: ...

BlockingIOError = builtins.BlockingIOError

class _IOBase:
    def __iter__(self) -> Iterator[bytes]: ...
    def __next__(self) -> bytes: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    read: Callable[..., Any]
    def readlines(self, hint: int = -1, /) -> list[bytes]: ...
    def seek(self, offset: int, whence: int = 0, /) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: int | None = None, /) -> int: ...
    def writable(self) -> bool: ...
    write: Callable[..., Any]
    def writelines(self, lines: Iterable[ReadableBuffer], /) -> None: ...
    def readline(self, size: int | None = -1, /) -> bytes: ...
    def __del__(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    def _checkClosed(self) -> None: ...  # undocumented

class _RawIOBase(_IOBase):
    def readall(self) -> bytes: ...
    # The following methods can return None if the file is in non-blocking mode
    # and no data is available.
    def readinto(self, buffer: WriteableBuffer, /) -> int | MaybeNone: ...
    def write(self, b: ReadableBuffer, /) -> int | MaybeNone: ...
    def read(self, size: int = -1, /) -> bytes | MaybeNone: ...

class _BufferedIOBase(_IOBase):
    def detach(self) -> RawIOBase: ...
    def readinto(self, buffer: WriteableBuffer, /) -> int: ...
    def write(self, buffer: ReadableBuffer, /) -> int: ...
    def readinto1(self, buffer: WriteableBuffer, /) -> int: ...
    def read(self, size: int | None = -1, /) -> bytes: ...
    def read1(self, size: int = -1, /) -> bytes: ...

class FileIO(RawIOBase, _RawIOBase, BinaryIO):  # type: ignore[misc]  # incompatible definitions of writelines in the base classes
    mode: str
    # The type of "name" equals the argument passed in to the constructor,
    # but that can make FileIO incompatible with other I/O types that assume
    # "name" is a str. In the future, making FileIO generic might help.
    name: Any
    def __init__(
        self, file: FileDescriptorOrPath, mode: str = "r", closefd: bool = True, opener: _Opener | None = None
    ) -> None: ...
    @property
    def closefd(self) -> bool: ...
    def seek(self, pos: int, whence: int = 0, /) -> int: ...
    def read(self, size: int | None = -1, /) -> bytes | MaybeNone: ...

class BytesIO(BufferedIOBase, _BufferedIOBase, BinaryIO):  # type: ignore[misc]  # incompatible definitions of methods in the base classes
    def __init__(self, initial_bytes: ReadableBuffer = b"") -> None: ...
    # BytesIO does not contain a "name" field. This workaround is necessary
    # to allow BytesIO sub-classes to add this field, as it is defined
    # as a read-only property on IO[].
    name: Any
    def getvalue(self) -> bytes: ...
    def getbuffer(self) -> memoryview: ...
    def read1(self, size: int | None = -1, /) -> bytes: ...
    def readlines(self, size: int | None = None, /) -> list[bytes]: ...
    def seek(self, pos: int, whence: int = 0, /) -> int: ...

class BufferedReader(BufferedIOBase, _BufferedIOBase, BinaryIO):  # type: ignore[misc]  # incompatible definitions of methods in the base classes
    raw: RawIOBase
    def __init__(self, raw: RawIOBase, buffer_size: int = 8192) -> None: ...
    def peek(self, size: int = 0, /) -> bytes: ...
    def seek(self, target: int, whence: int = 0, /) -> int: ...
    def truncate(self, pos: int | None = None, /) -> int: ...

class BufferedWriter(BufferedIOBase, _BufferedIOBase, BinaryIO):  # type: ignore[misc]  # incompatible definitions of writelines in the base classes
    raw: RawIOBase
    def __init__(self, raw: RawIOBase, buffer_size: int = 8192) -> None: ...
    def write(self, buffer: ReadableBuffer, /) -> int: ...
    def seek(self, target: int, whence: int = 0, /) -> int: ...
    def truncate(self, pos: int | None = None, /) -> int: ...

class BufferedRandom(BufferedIOBase, _BufferedIOBase, BinaryIO):  # type: ignore[misc]  # incompatible definitions of methods in the base classes
    mode: str
    name: Any
    raw: RawIOBase
    def __init__(self, raw: RawIOBase, buffer_size: int = 8192) -> None: ...
    def seek(self, target: int, whence: int = 0, /) -> int: ...  # stubtest needs this
    def peek(self, size: int = 0, /) -> bytes: ...
    def truncate(self, pos: int | None = None, /) -> int: ...

class BufferedRWPair(BufferedIOBase, _BufferedIOBase):
    def __init__(self, reader: RawIOBase, writer: RawIOBase, buffer_size: int = 8192, /) -> None: ...
    def peek(self, size: int = 0, /) -> bytes: ...

class _TextIOBase(_IOBase):
    encoding: str
    errors: str | None
    newlines: str | tuple[str, ...] | None
    def __iter__(self) -> Iterator[str]: ...  # type: ignore[override]
    def __next__(self) -> str: ...  # type: ignore[override]
    def detach(self) -> BinaryIO: ...
    def write(self, s: str, /) -> int: ...
    def writelines(self, lines: Iterable[str], /) -> None: ...  # type: ignore[override]
    def readline(self, size: int = -1, /) -> str: ...  # type: ignore[override]
    def readlines(self, hint: int = -1, /) -> list[str]: ...  # type: ignore[override]
    def read(self, size: int | None = -1, /) -> str: ...

@type_check_only
class _WrappedBuffer(Protocol):
    # "name" is wrapped by TextIOWrapper. Its type is inconsistent between
    # the various I/O types, see the comments on TextIOWrapper.name and
    # TextIO.name.
    @property
    def name(self) -> Any: ...
    @property
    def closed(self) -> bool: ...
    def read(self, size: int = ..., /) -> ReadableBuffer: ...
    # Optional: def read1(self, size: int, /) -> ReadableBuffer: ...
    def write(self, b: bytes, /) -> object: ...
    def flush(self) -> object: ...
    def close(self) -> object: ...
    def seekable(self) -> bool: ...
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def truncate(self, size: int, /) -> int: ...
    def fileno(self) -> int: ...
    def isatty(self) -> bool: ...
    # Optional: Only needs to be present if seekable() returns True.
    # def seek(self, offset: Literal[0], whence: Literal[2]) -> int: ...
    # def tell(self) -> int: ...

_BufferT_co = TypeVar("_BufferT_co", bound=_WrappedBuffer, default=_WrappedBuffer, covariant=True)

class TextIOWrapper(TextIOBase, _TextIOBase, TextIO, Generic[_BufferT_co]):  # type: ignore[misc]  # incompatible definitions of write in the base classes
    def __init__(
        self,
        buffer: _BufferT_co,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        line_buffering: bool = False,
        write_through: bool = False,
    ) -> None: ...
    # Equals the "buffer" argument passed in to the constructor.
    @property
    def buffer(self) -> _BufferT_co: ...  # type: ignore[override]
    @property
    def line_buffering(self) -> bool: ...
    @property
    def write_through(self) -> bool: ...
    def reconfigure(
        self,
        *,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        line_buffering: bool | None = None,
        write_through: bool | None = None,
    ) -> None: ...
    def readline(self, size: int = -1, /) -> str: ...  # type: ignore[override]
    # Equals the "buffer" argument passed in to the constructor.
    def detach(self) -> _BufferT_co: ...  # type: ignore[override]
    # TextIOWrapper's version of seek only supports a limited subset of
    # operations.
    def seek(self, cookie: int, whence: int = 0, /) -> int: ...
    def truncate(self, pos: int | None = None, /) -> int: ...

class StringIO(TextIOBase, _TextIOBase, TextIO):  # type: ignore[misc]  # incompatible definitions of write in the base classes
    def __init__(self, initial_value: str | None = "", newline: str | None = "\n") -> None: ...
    # StringIO does not contain a "name" field. This workaround is necessary
    # to allow StringIO sub-classes to add this field, as it is defined
    # as a read-only property on IO[].
    name: Any
    def getvalue(self) -> str: ...
    @property
    def line_buffering(self) -> bool: ...
    def seek(self, pos: int, whence: int = 0, /) -> int: ...
    def truncate(self, pos: int | None = None, /) -> int: ...

class IncrementalNewlineDecoder:
    def __init__(self, decoder: codecs.IncrementalDecoder | None, translate: bool, errors: str = "strict") -> None: ...
    def decode(self, input: ReadableBuffer | str, final: bool = False) -> str: ...
    @property
    def newlines(self) -> str | tuple[str, ...] | None: ...
    def getstate(self) -> tuple[bytes, int]: ...
    def reset(self) -> None: ...
    def setstate(self, state: tuple[bytes, int], /) -> None: ...

if sys.version_info >= (3, 10):
    @overload
    def text_encoding(encoding: None, stacklevel: int = 2, /) -> Literal["locale", "utf-8"]: ...
    @overload
    def text_encoding[_T](encoding: _T, stacklevel: int = 2, /) -> _T: ...
