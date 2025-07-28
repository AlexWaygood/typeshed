"""Capture C-level FD output on pipes

Use `wurlitzer.pipes` or `wurlitzer.sys_pipes` as context managers.
"""

__all__ = ["STDOUT", "PIPE", "Wurlitzer", "pipes", "sys_pipes", "sys_pipes_forever", "stop_sys_pipes"]

import contextlib
import io
import logging
from _typeshed import SupportsWrite
from contextlib import _GeneratorContextManager
from threading import Thread
from types import TracebackType
from typing import Any, Final, Literal, Protocol, TextIO, TypeVar, overload
from typing_extensions import Self, TypeAlias

STDOUT: Final = 2
PIPE: Final = 3
_STDOUT: TypeAlias = Literal[2]
_PIPE: TypeAlias = Literal[3]
_T_contra = TypeVar("_T_contra", contravariant=True)
_StreamOutT = TypeVar("_StreamOutT", bound=_Stream[str] | _Stream[bytes])
_StreamErrT = TypeVar("_StreamErrT", bound=_Stream[str] | _Stream[bytes])

class _Stream(SupportsWrite[_T_contra], Protocol):
    def seek(self, offset: int, whence: int = ..., /) -> int: ...

# Alias for IPython.core.interactiveshell.InteractiveShell.
# N.B. Even if we added ipython to the stub-uploader allowlist,
# we wouldn't be able to declare a dependency on ipython here,
# since `wurlitzer` does not declare a dependency on `ipython` at runtime
_InteractiveShell: TypeAlias = Any

class Wurlitzer:
    """Class for Capturing Process-level FD output via dup2

    Typically used via `wurlitzer.pipes`
    """

    flush_interval: float
    encoding: str | None
    thread: Thread | None
    handle: tuple[
        _LogPipe | SupportsWrite[str] | SupportsWrite[bytes] | None, _LogPipe | SupportsWrite[str] | SupportsWrite[bytes] | None
    ]

    def __init__(
        self,
        stdout: SupportsWrite[str] | SupportsWrite[bytes] | logging.Logger | None = None,
        stderr: _STDOUT | SupportsWrite[str] | SupportsWrite[bytes] | logging.Logger | None = None,
        encoding: str | None = ...,
        bufsize: int | None = ...,
    ) -> None:
        """
        Parameters
        ----------
        stdout: stream or None
            The stream for forwarding stdout.
        stderr = stream or None
            The stream for forwarding stderr.
        encoding: str or None
            The encoding to use, if streams should be interpreted as text.
        bufsize: int or None
            Set pipe buffer size using fcntl F_SETPIPE_SZ (linux only)
            default: use /proc/sys/fs/pipe-max-size up to a max of 1MB
            if 0, will do nothing.
        """

    def __enter__(
        self,
    ) -> tuple[
        _LogPipe | SupportsWrite[str] | SupportsWrite[bytes] | None, _LogPipe | SupportsWrite[str] | SupportsWrite[bytes] | None
    ]: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...

def dup2(a: int, b: int, timeout: float = 3) -> int:
    """Like os.dup2, but retry on EBUSY"""

def sys_pipes(encoding: str = ..., bufsize: int | None = None) -> contextlib._GeneratorContextManager[tuple[TextIO, TextIO]]:
    """Redirect C-level stdout/stderr to sys.stdout/stderr

    This is useful of sys.sdout/stderr are already being forwarded somewhere,
    e.g. in a Jupyter kernel.

    DO NOT USE THIS if sys.stdout and sys.stderr are not already being forwarded.
    """

# stubtest does not support overloaded context managers, hence the _GeneratorContextManager[Foo] return types.
@overload
def pipes(
    stdout: _PIPE, stderr: _STDOUT, encoding: None, bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.BytesIO, None]]:
    """Capture C-level stdout/stderr in a context manager.

    The return value for the context manager is (stdout, stderr).

    Args:

    stdout (optional, default: PIPE): None or PIPE or Writable or Logger
    stderr (optional, default: PIPE): None or PIPE or STDOUT or Writable or Logger
    encoding (optional): probably 'utf-8'
    bufsize (optional): set explicit buffer size if the default doesn't work

    .. versionadded:: 3.1
        Accept Logger objects for stdout/stderr.
        If a Logger is specified, each line will produce a log message.
        stdout messages will be at INFO level, stderr messages at ERROR level.

    .. versionchanged:: 3.0

        when using `PIPE` (default), the type of captured output
        is `io.StringIO/BytesIO` instead of an OS pipe.
        This eliminates max buffer size issues (and hang when output exceeds 65536 bytes),
        but also means the buffer cannot be read with `.read()` methods
        until after the context exits.

    Examples
    --------

    >>> with pipes() as (stdout, stderr):
    ...     printf("C-level stdout")
    ... output = stdout.read()
    """

@overload
def pipes(
    stdout: _PIPE, stderr: _PIPE, encoding: None, bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.BytesIO, io.BytesIO]]: ...
@overload
def pipes(
    stdout: _PIPE, stderr: _StreamErrT, encoding: None, bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.BytesIO, _StreamErrT]]: ...
@overload
def pipes(
    stdout: _PIPE, stderr: _STDOUT, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.StringIO, None]]: ...
@overload
def pipes(
    stdout: _PIPE, stderr: _PIPE, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.StringIO, io.StringIO]]: ...
@overload
def pipes(
    stdout: _PIPE, stderr: _StreamErrT, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.StringIO, _StreamErrT]]: ...
@overload
def pipes(
    stdout: _PIPE, stderr: logging.Logger, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[io.StringIO, _LogPipe]]: ...
@overload
def pipes(
    stdout: logging.Logger, stderr: _STDOUT, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_LogPipe, None]]: ...
@overload
def pipes(
    stdout: logging.Logger, stderr: _PIPE, encoding: None, bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_LogPipe, io.BytesIO]]: ...
@overload
def pipes(
    stdout: logging.Logger, stderr: _PIPE, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_LogPipe, io.StringIO]]: ...
@overload
def pipes(
    stdout: logging.Logger, stderr: _StreamErrT, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_LogPipe, _StreamErrT]]: ...
@overload
def pipes(
    stdout: logging.Logger, stderr: logging.Logger, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_LogPipe, _LogPipe]]: ...
@overload
def pipes(
    stdout: _StreamOutT, stderr: _STDOUT, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_StreamOutT, None]]: ...
@overload
def pipes(
    stdout: _StreamOutT, stderr: _PIPE, encoding: None, bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_StreamOutT, io.BytesIO]]: ...
@overload
def pipes(
    stdout: _StreamOutT, stderr: _PIPE, encoding: str = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_StreamOutT, io.StringIO]]: ...
@overload
def pipes(
    stdout: _StreamOutT, stderr: _StreamErrT, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_StreamOutT, _StreamErrT]]: ...
@overload
def pipes(
    stdout: _StreamOutT, stderr: logging.Logger, encoding: str | None = ..., bufsize: int | None = None
) -> _GeneratorContextManager[tuple[_StreamOutT, _LogPipe]]: ...
@overload
def pipes(
    stdout: _PIPE | logging.Logger | _StreamOutT = 3,
    stderr: _STDOUT | _PIPE | logging.Logger | _StreamErrT = 3,
    encoding: str | None = ...,
    bufsize: int | None = None,
) -> _GeneratorContextManager[
    tuple[io.BytesIO | io.StringIO | _StreamOutT | _LogPipe, io.BytesIO | io.StringIO | _StreamErrT | _LogPipe | None]
]: ...

class _LogPipe(io.BufferedWriter):
    """Writeable that writes lines to a Logger object as they arrive from captured pipes"""

    logger: logging.Logger
    stream_name: str
    level: int
    def __init__(self, logger: logging.Logger, stream_name: str, level: int = 20) -> None: ...
    def write(self, chunk: str) -> None:  # type: ignore[override]
        """Given chunk, split into lines

        Log each line as a discrete message

        If it ends with a partial line, save it until the next one
        """

    def flush(self) -> None:
        """Write buffer as a last message if there is one"""

    def __enter__(self) -> Self: ...
    def __exit__(self, *exc_info: object) -> None: ...

def sys_pipes_forever(encoding: str = ..., bufsize: int | None = None) -> None:
    """Redirect all C output to sys.stdout/err

    This is not a context manager; it turns on C-forwarding permanently.
    """

def stop_sys_pipes() -> None:
    """Stop permanent redirection started by sys_pipes_forever"""

def load_ipython_extension(ip: _InteractiveShell) -> None:
    """Register me as an IPython extension

    Captures all C output during execution and forwards to sys.

    Does nothing on terminal IPython.

    Use: %load_ext wurlitzer
    """

def unload_ipython_extension(ip: _InteractiveShell) -> None:
    """Unload me as an IPython extension

    Use: %unload_ext wurlitzer
    """
