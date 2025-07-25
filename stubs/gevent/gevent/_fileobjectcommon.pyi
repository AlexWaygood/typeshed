"""
gevent internals.
"""

import io
from _typeshed import (
    FileDescriptorOrPath,
    OpenBinaryMode,
    OpenBinaryModeReading,
    OpenBinaryModeUpdating,
    OpenBinaryModeWriting,
    OpenTextMode,
    ReadableBuffer,
)
from types import TracebackType
from typing import IO, Any, AnyStr, ClassVar, Generic, Literal, TypeVar, overload
from typing_extensions import Self

from gevent.lock import DummySemaphore, Semaphore
from gevent.threadpool import ThreadPool

_IOT = TypeVar("_IOT", bound=IO[Any])

class cancel_wait_ex(IOError):
    def __init__(self) -> None: ...

class FileObjectClosed(IOError):
    def __init__(self) -> None: ...

class FlushingBufferedWriter(io.BufferedWriter): ...

class WriteallMixin:
    def writeall(self, b: ReadableBuffer, /) -> int:
        """
        Similar to :meth:`socket.socket.sendall`, ensures that all the contents of
        *value* have been written (though not necessarily flushed) before returning.

        Returns the length of *value*.

        .. versionadded:: 20.12.0
        """

class FileIO(io.FileIO):
    """A subclass that we can dynamically assign __class__ for."""

class WriteIsWriteallMixin(WriteallMixin):
    def write(self, b: ReadableBuffer, /) -> int: ...

class WriteallFileIO(WriteIsWriteallMixin, io.FileIO): ...  # type: ignore[misc]

class OpenDescriptor(Generic[_IOT]):
    """
    Interprets the arguments to `open`. Internal use only.

    Originally based on code in the stdlib's _pyio.py (Python implementation of
    the :mod:`io` module), but modified for gevent:

    - Native strings are returned on Python 2 when neither
      'b' nor 't' are in the mode string and no encoding is specified.
    - Universal newlines work in that mode.
    - Allows externally unbuffered text IO.

    :keyword bool atomic_write: If true, then if the opened, wrapped, stream
        is unbuffered (meaning that ``write`` can produce short writes and the return
        value needs to be checked), then the implementation will be adjusted so that
        ``write`` behaves like Python 2 on a built-in file object and writes the
        entire value. Only set this on Python 2; the only intended user is
        :class:`gevent.subprocess.Popen`.
    """

    default_buffer_size: ClassVar[int]
    fileio_mode: str
    mode: str
    creating: bool
    reading: bool
    writing: bool
    appending: bool
    updating: bool
    text: bool
    binary: bool
    can_write: bool
    can_read: bool
    native: bool
    universal: bool
    buffering: int
    encoding: str | None
    errors: str | None
    newline: bool
    closefd: bool
    atomic_write: bool
    # we could add all the necessary overloads here too, but since this is internal API
    # I don't think it makes sense to do that
    def __init__(
        self,
        fobj: FileDescriptorOrPath,
        mode: str = "r",
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...
    def is_fd(self) -> bool: ...
    def opened(self) -> _IOT:
        """
        Return the :meth:`wrapped` file object.
        """

    def opened_raw(self) -> FileIO: ...
    @staticmethod
    def is_buffered(stream: object) -> bool: ...
    @classmethod
    def buffer_size_for_stream(cls, stream: object) -> int: ...

class FileObjectBase(Generic[_IOT, AnyStr]):
    """
    Internal base class to ensure a level of consistency
    between :class:`~.FileObjectPosix`, :class:`~.FileObjectThread`
    and :class:`~.FileObjectBlock`.
    """

    def __init__(
        self: FileObjectBase[_IOT, AnyStr], descriptor: OpenDescriptor[_IOT]  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    ) -> None: ...
    io: _IOT
    @property
    def closed(self) -> bool:
        """True if the file is closed"""

    def close(self) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None, /) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> AnyStr: ...
    def __bool__(self) -> bool: ...
    next = __next__

class FileObjectBlock(FileObjectBase[_IOT, AnyStr]):
    """
    FileObjectBlock()

    A simple synchronous wrapper around a file object.

    Adds no concurrency or gevent compatibility.
    """

    # Text mode: always binds a TextIOWrapper
    @overload
    def __init__(
        self: FileObjectBlock[io.TextIOWrapper, str],
        fobj: FileDescriptorOrPath,
        mode: OpenTextMode = "r",
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...

    # Unbuffered binary mode: binds a FileIO
    @overload
    def __init__(
        self: FileObjectBlock[io.FileIO, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: Literal[0],
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[0] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectBlock[io.FileIO, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: Literal[0] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        *,
        buffering: Literal[0],
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...

    # Buffering is on: return BufferedRandom, BufferedReader, or BufferedWriter
    @overload
    def __init__(
        self: FileObjectBlock[io.BufferedRandom, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeUpdating,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectBlock[io.BufferedWriter, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeWriting,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectBlock[io.BufferedReader, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeReading,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...

    # Buffering cannot be determined: fall back to BinaryIO
    @overload
    def __init__(
        self: FileObjectBlock[IO[bytes], bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...

    # Fallback if mode is not specified
    @overload
    def __init__(
        self: FileObjectBlock[IO[Any], Any],
        fobj: FileDescriptorOrPath,
        mode: str,
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
    ) -> None: ...

class FileObjectThread(FileObjectBase[_IOT, AnyStr]):
    """
    FileObjectThread()

    A file-like object wrapping another file-like object, performing all blocking
    operations on that object in a background thread.

    .. caution::
        Attempting to change the threadpool or lock of an existing FileObjectThread
        has undefined consequences.

    .. versionchanged:: 1.1b1
       The file object is closed using the threadpool. Note that whether or
       not this action is synchronous or asynchronous is not documented.
    """

    threadpool: ThreadPool
    lock: Semaphore | DummySemaphore
    # Text mode: always binds a TextIOWrapper
    @overload
    def __init__(
        self: FileObjectThread[io.TextIOWrapper, str],
        fobj: FileDescriptorOrPath,
        mode: OpenTextMode = "r",
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None:
        """
        :keyword bool lock: If True (the default) then all operations will
           be performed one-by-one. Note that this does not guarantee that, if using
           this file object from multiple threads/greenlets, operations will be performed
           in any particular order, only that no two operations will be attempted at the
           same time. You can also pass your own :class:`gevent.lock.Semaphore` to synchronize
           file operations with an external resource.
        :keyword bool closefd: If True (the default) then when this object is closed,
           the underlying object is closed as well. If *fobj* is a path, then
           *closefd* must be True.
        """
    # Unbuffered binary mode: binds a FileIO
    @overload
    def __init__(
        self: FileObjectThread[io.FileIO, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: Literal[0],
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[0] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectThread[io.FileIO, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: Literal[0] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        *,
        buffering: Literal[0],
        closefd: bool | None = None,
        atomic_write: bool = False,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...

    # Buffering is on: return BufferedRandom, BufferedReader, or BufferedWriter
    @overload
    def __init__(
        self: FileObjectThread[io.BufferedRandom, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeUpdating,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectThread[io.BufferedWriter, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeWriting,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self: FileObjectThread[io.BufferedReader, bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryModeReading,
        bufsize: Literal[-1, 1] | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: Literal[-1, 1] | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...

    # Buffering cannot be determined: fall back to BinaryIO
    @overload
    def __init__(
        self: FileObjectThread[IO[bytes], bytes],
        fobj: FileDescriptorOrPath,
        mode: OpenBinaryMode,
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...

    # Fallback if mode is not specified
    @overload
    def __init__(
        self: FileObjectThread[IO[Any], Any],
        fobj: FileDescriptorOrPath,
        mode: str,
        bufsize: int | None = None,
        close: bool | None = None,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        buffering: int | None = None,
        closefd: bool | None = None,
        atomic_write: bool = False,
        *,
        lock: bool = True,
        threadpool: ThreadPool | None = None,
    ) -> None: ...
