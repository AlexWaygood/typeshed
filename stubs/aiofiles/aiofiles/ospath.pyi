"""Async executor versions of file functions from the os.path module."""

from _typeshed import FileDescriptorOrPath
from asyncio.events import AbstractEventLoop
from collections.abc import Awaitable, Callable
from concurrent.futures import Executor
from os import PathLike
from typing import AnyStr, TypeVar

_R = TypeVar("_R")

def wrap(func: Callable[..., _R]) -> Callable[..., Awaitable[_R]]: ...
async def exists(path: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> bool:
    """Test whether a path exists.  Returns False for broken symbolic links"""

async def isfile(path: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> bool:
    """Test whether a path is a regular file"""

async def isdir(s: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> bool:
    """Return true if the pathname refers to an existing directory."""

async def islink(path: FileDescriptorOrPath) -> bool:
    """Test whether a path is a symbolic link"""

async def ismount(path: FileDescriptorOrPath) -> bool:
    """Test whether a path is a mount point"""

async def getsize(
    filename: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> int:
    """Return the size of a file, reported by os.stat()."""

async def getmtime(
    filename: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> float:
    """Return the last modification time of a file, reported by os.stat()."""

async def getatime(
    filename: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> float:
    """Return the last access time of a file, reported by os.stat()."""

async def getctime(
    filename: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> float:
    """Return the metadata change time of a file, reported by os.stat()."""

async def samefile(
    f1: FileDescriptorOrPath, f2: FileDescriptorOrPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> bool:
    """Test whether two pathnames reference the same actual file or directory

    This is determined by the device number and i-node number and
    raises an exception if an os.stat() call on either pathname fails.
    """

async def sameopenfile(fp1: int, fp2: int, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> bool:
    """Test whether two open file objects reference the same file"""

async def abspath(path: PathLike[AnyStr] | AnyStr) -> AnyStr:
    """Return an absolute path."""
