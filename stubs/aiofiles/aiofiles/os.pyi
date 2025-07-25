"""Async executor versions of file functions from the os module."""

import sys
from _typeshed import BytesPath, FileDescriptorOrPath, GenericPath, ReadableBuffer, StrOrBytesPath, StrPath
from asyncio.events import AbstractEventLoop
from collections.abc import Sequence
from concurrent.futures import Executor
from os import _ScandirIterator, stat_result
from typing import AnyStr, overload

from aiofiles import ospath
from aiofiles.ospath import wrap as wrap

__all__ = [
    "path",
    "stat",
    "rename",
    "renames",
    "replace",
    "remove",
    "unlink",
    "mkdir",
    "makedirs",
    "rmdir",
    "removedirs",
    "link",
    "symlink",
    "readlink",
    "listdir",
    "scandir",
    "access",
    "wrap",
    "getcwd",
]

if sys.platform != "win32":
    __all__ += ["statvfs", "sendfile"]

path = ospath

async def stat(
    path: FileDescriptorOrPath,
    *,
    dir_fd: int | None = None,
    follow_symlinks: bool = True,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> stat_result:
    """Perform a stat system call on the given path.

      path
        Path to be examined; can be string, bytes, a path-like object or
        open-file-descriptor int.
      dir_fd
        If not None, it should be a file descriptor open to a directory,
        and path should be a relative string; path will then be relative to
        that directory.
      follow_symlinks
        If False, and the last element of the path is a symbolic link,
        stat will examine the symbolic link itself instead of the file
        the link points to.

    dir_fd and follow_symlinks may not be implemented
      on your platform.  If they are unavailable, using them will raise a
      NotImplementedError.

    It's an error to use dir_fd or follow_symlinks when specifying path as
      an open file descriptor.
    """

async def rename(
    src: StrOrBytesPath,
    dst: StrOrBytesPath,
    *,
    src_dir_fd: int | None = None,
    dst_dir_fd: int | None = None,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """Rename a file or directory.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    src_dir_fd and dst_dir_fd, may not be implemented on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """

async def renames(
    old: StrOrBytesPath, new: StrOrBytesPath, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> None:
    """renames(old, new)

    Super-rename; create directories as necessary and delete any left
    empty.  Works like rename, except creation of any intermediate
    directories needed to make the new pathname good is attempted
    first.  After the rename, directories corresponding to rightmost
    path segments of the old name will be pruned until either the
    whole path is consumed or a nonempty directory is found.

    Note: this function can fail with the new directory structure made
    if you lack permissions needed to unlink the leaf directory or
    file.

    """

async def replace(
    src: StrOrBytesPath,
    dst: StrOrBytesPath,
    *,
    src_dir_fd: int | None = None,
    dst_dir_fd: int | None = None,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """Rename a file or directory, overwriting the destination.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    src_dir_fd and dst_dir_fd, may not be implemented on your platform.
      If they are unavailable, using them will raise a NotImplementedError.
    """

async def remove(
    path: StrOrBytesPath, *, dir_fd: int | None = None, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> None:
    """Remove a file (same as unlink()).

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """

async def unlink(
    path: StrOrBytesPath, *, dir_fd: int | None = ..., loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> None:
    """Remove a file (same as remove()).

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """

async def mkdir(
    path: StrOrBytesPath,
    mode: int = 511,
    *,
    dir_fd: int | None = None,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """Create a directory.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.

    The mode argument is ignored on Windows. Where it is used, the current umask
    value is first masked out.
    """

async def makedirs(
    name: StrOrBytesPath,
    mode: int = 511,
    exist_ok: bool = False,
    *,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """makedirs(name [, mode=0o777][, exist_ok=False])

    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.

    """

async def link(
    src: StrOrBytesPath,
    dst: StrOrBytesPath,
    *,
    src_dir_fd: int | None = ...,
    dst_dir_fd: int | None = ...,
    follow_symlinks: bool = ...,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """Create a hard link to a file.

    If either src_dir_fd or dst_dir_fd is not None, it should be a file
      descriptor open to a directory, and the respective path string (src or dst)
      should be relative; the path will then be relative to that directory.
    If follow_symlinks is False, and the last element of src is a symbolic
      link, link will create a link to the symbolic link itself instead of the
      file the link points to.
    src_dir_fd, dst_dir_fd, and follow_symlinks may not be implemented on your
      platform.  If they are unavailable, using them will raise a
      NotImplementedError.
    """

async def symlink(
    src: StrOrBytesPath,
    dst: StrOrBytesPath,
    target_is_directory: bool = ...,
    *,
    dir_fd: int | None = ...,
    loop: AbstractEventLoop | None = ...,
    executor: Executor | None = ...,
) -> None:
    """Create a symbolic link pointing to src named dst.

    target_is_directory is required on Windows if the target is to be
      interpreted as a directory.  (On Windows, symlink requires
      Windows 6.0 or greater, and raises a NotImplementedError otherwise.)
      target_is_directory is ignored on non-Windows platforms.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """

async def readlink(
    path: AnyStr, *, dir_fd: int | None = ..., loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> AnyStr:
    """Return a string representing the path to which the symbolic link points.

    If dir_fd is not None, it should be a file descriptor open to a directory,
    and path should be relative; path will then be relative to that directory.

    dir_fd may not be implemented on your platform.  If it is unavailable,
    using it will raise a NotImplementedError.
    """

async def rmdir(
    path: StrOrBytesPath, *, dir_fd: int | None = None, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> None:
    """Remove a directory.

    If dir_fd is not None, it should be a file descriptor open to a directory,
      and path should be relative; path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
      If it is unavailable, using it will raise a NotImplementedError.
    """

async def removedirs(name: StrOrBytesPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> None:
    """removedirs(name)

    Super-rmdir; remove a leaf directory and all empty intermediate
    ones.  Works like rmdir except that, if the leaf directory is
    successfully removed, directories corresponding to rightmost path
    segments will be pruned away until either the whole path is
    consumed or an error occurs.  Errors during this latter phase are
    ignored -- they generally mean that a directory was not empty.

    """

@overload
async def scandir(
    path: None = None, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> _ScandirIterator[str]:
    """Return an iterator of DirEntry objects for given path.

    path can be specified as either str, bytes, or a path-like object.  If path
    is bytes, the names of yielded DirEntry objects will also be bytes; in
    all other circumstances they will be str.

    If path is None, uses the path='.'.
    """

@overload
async def scandir(
    path: int, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> _ScandirIterator[str]: ...
@overload
async def scandir(
    path: GenericPath[AnyStr], *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...
) -> _ScandirIterator[AnyStr]: ...
@overload
async def listdir(path: StrPath | None, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> list[str]:
    """Return a list containing the names of the files in the directory.

path can be specified as either str, bytes, or a path-like object.  If path is bytes,
  the filenames returned will also be bytes; in all other circumstances
  the filenames returned will be str.
If path is None, uses the path='.'.
On some platforms, path may also be specified as an open file descriptor;\\
  the file descriptor must refer to a directory.
  If this functionality is unavailable, using it raises NotImplementedError.

The list is in arbitrary order.  It does not include the special
entries '.' and '..' even if they are present in the directory.
"""

@overload
async def listdir(path: BytesPath, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> list[bytes]: ...
@overload
async def listdir(path: int, *, loop: AbstractEventLoop | None = ..., executor: Executor | None = ...) -> list[str]: ...
async def access(
    path: FileDescriptorOrPath, mode: int, *, dir_fd: int | None = None, effective_ids: bool = False, follow_symlinks: bool = True
) -> bool:
    """Use the real uid/gid to test for access to a path.

      path
        Path to be tested; can be string, bytes, or a path-like object.
      mode
        Operating-system mode bitfield.  Can be F_OK to test existence,
        or the inclusive-OR of R_OK, W_OK, and X_OK.
      dir_fd
        If not None, it should be a file descriptor open to a directory,
        and path should be relative; path will then be relative to that
        directory.
      effective_ids
        If True, access will use the effective uid/gid instead of
        the real uid/gid.
      follow_symlinks
        If False, and the last element of the path is a symbolic link,
        access will examine the symbolic link itself instead of the file
        the link points to.

    dir_fd, effective_ids, and follow_symlinks may not be implemented
      on your platform.  If they are unavailable, using them will raise a
      NotImplementedError.

    Note that most operations will use the effective uid/gid, therefore this
      routine can be used in a suid/sgid environment to test if the invoking user
      has the specified access to the path.
    """

async def getcwd() -> str:
    """Return a unicode string representing the current working directory."""

if sys.platform != "win32":
    from os import statvfs_result

    @overload
    async def sendfile(
        out_fd: int,
        in_fd: int,
        offset: int | None,
        count: int,
        *,
        loop: AbstractEventLoop | None = ...,
        executor: Executor | None = ...,
    ) -> int:
        """Copy count bytes from file descriptor in_fd to file descriptor out_fd."""

    @overload
    async def sendfile(
        out_fd: int,
        in_fd: int,
        offset: int,
        count: int,
        headers: Sequence[ReadableBuffer] = ...,
        trailers: Sequence[ReadableBuffer] = ...,
        flags: int = ...,
        *,
        loop: AbstractEventLoop | None = ...,
        executor: Executor | None = ...,
    ) -> int: ...  # FreeBSD and Mac OS X only
    async def statvfs(path: FileDescriptorOrPath) -> statvfs_result:  # Unix only
        """Perform a statvfs system call on the given path.

        path may always be specified as a string.
        On some platforms, path may also be specified as an open file descriptor.
          If this functionality is unavailable, using it raises an exception.
        """
