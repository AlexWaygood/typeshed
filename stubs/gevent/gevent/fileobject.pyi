"""
Wrappers to make file-like objects cooperative.

.. class:: FileObject(fobj, mode='r', buffering=-1, closefd=True, encoding=None, errors=None, newline=None)

    The main entry point to the file-like gevent-compatible behaviour. It
    will be defined to be the best available implementation.

    All the parameters are as for :func:`io.open`.

    :param fobj: Usually a file descriptor of a socket. Can also be
        another object with a ``fileno()`` method, or an object that can
        be passed to ``io.open()`` (e.g., a file system path). If the object
        is not a socket, the results will vary based on the platform and the
        type of object being opened.

        All supported versions of Python allow :class:`os.PathLike` objects.

    .. versionchanged:: 1.5
       Accept str and ``PathLike`` objects for *fobj* on all versions of Python.
    .. versionchanged:: 1.5
       Add *encoding*, *errors* and *newline* arguments.
    .. versionchanged:: 1.5
       Accept *closefd* and *buffering* instead of *close* and *bufsize* arguments.
       The latter remain for backwards compatibility.

There are two main implementations of ``FileObject``. On all systems,
there is :class:`FileObjectThread` which uses the built-in native
threadpool to avoid blocking the entire interpreter. On UNIX systems
(those that support the :mod:`fcntl` module), there is also
:class:`FileObjectPosix` which uses native non-blocking semantics.

A third class, :class:`FileObjectBlock`, is simply a wrapper that
executes everything synchronously (and so is not gevent-compatible).
It is provided for testing and debugging purposes.

All classes have the same signature; some may accept extra keyword arguments.

Configuration
=============

You may change the default value for ``FileObject`` using the
``GEVENT_FILE`` environment variable. Set it to ``posix``, ``thread``,
or ``block`` to choose from :class:`FileObjectPosix`,
:class:`FileObjectThread` and :class:`FileObjectBlock`, respectively.
You may also set it to the fully qualified class name of another
object that implements the file interface to use one of your own
objects.

.. note::

    The environment variable must be set at the time this module
    is first imported.

Classes
=======
"""

import sys
from typing import Any
from typing_extensions import TypeAlias

from gevent._fileobjectcommon import FileObjectBlock as FileObjectBlock, FileObjectThread as FileObjectThread

if sys.platform != "win32":
    import io
    from _typeshed import (
        FileDescriptorOrPath,
        OpenBinaryMode,
        OpenBinaryModeReading,
        OpenBinaryModeUpdating,
        OpenBinaryModeWriting,
        OpenTextMode,
    )
    from typing import IO, AnyStr, Literal, overload

    from gevent._fileobjectcommon import _IOT, FileObjectBase

    # this is implemented in _fileobjectposix and technically uses an undocumented subclass
    # of RawIOBase, but the interface is the same, so it doesn't seem worth it to add
    # annotations for it. _fileobjectcommon was barely worth it due to the common base class
    # of all three FileObject types
    class FileObjectPosix(FileObjectBase[_IOT, AnyStr]):
        """
        FileObjectPosix()

        A file-like object that operates on non-blocking files but
        provides a synchronous, cooperative interface.

        .. caution::
             This object is only effective wrapping files that can be used meaningfully
             with :func:`select.select` such as sockets and pipes.

             In general, on most platforms, operations on regular files
             (e.g., ``open('a_file.txt')``) are considered non-blocking
             already, even though they can take some time to complete as
             data is copied to the kernel and flushed to disk: this time
             is relatively bounded compared to sockets or pipes, though.
             A :func:`~os.read` or :func:`~os.write` call on such a file
             will still effectively block for some small period of time.
             Therefore, wrapping this class around a regular file is
             unlikely to make IO gevent-friendly: reading or writing large
             amounts of data could still block the event loop.

             If you'll be working with regular files and doing IO in large
             chunks, you may consider using
             :class:`~gevent.fileobject.FileObjectThread` or
             :func:`~gevent.os.tp_read` and :func:`~gevent.os.tp_write` to bypass this
             concern.

        .. tip::
             Although this object provides a :meth:`fileno` method and so
             can itself be passed to :func:`fcntl.fcntl`, setting the
             :data:`os.O_NONBLOCK` flag will have no effect (reads will
             still block the greenlet, although other greenlets can run).
             However, removing that flag *will cause this object to no
             longer be cooperative* (other greenlets will no longer run).

             You can use the internal ``fileio`` attribute of this object
             (a :class:`io.RawIOBase`) to perform non-blocking byte reads.
             Note, however, that once you begin directly using this
             attribute, the results from using methods of *this* object
             are undefined, especially in text mode. (See :issue:`222`.)

        .. versionchanged:: 1.1
           Now uses the :mod:`io` package internally. Under Python 2, previously
           used the undocumented class :class:`socket._fileobject`. This provides
           better file-like semantics (and portability to Python 3).
        .. versionchanged:: 1.2a1
           Document the ``fileio`` attribute for non-blocking reads.
        .. versionchanged:: 1.2a1

            A bufsize of 0 in write mode is no longer forced to be 1.
            Instead, the underlying buffer is flushed after every write
            operation to simulate a bufsize of 0. In gevent 1.0, a
            bufsize of 0 was flushed when a newline was written, while
            in gevent 1.1 it was flushed when more than one byte was
            written. Note that this may have performance impacts.
        .. versionchanged:: 1.3a1
            On Python 2, enabling universal newlines no longer forces unicode
            IO.
        .. versionchanged:: 1.5
           The default value for *mode* was changed from ``rb`` to ``r``. This is consistent
           with :func:`open`, :func:`io.open`, and :class:`~.FileObjectThread`, which is the
           default ``FileObject`` on some platforms.
        .. versionchanged:: 1.5
           Stop forcing buffering. Previously, given a ``buffering=0`` argument,
           *buffering* would be set to 1, and ``buffering=1`` would be forced to
           the default buffer size. This was a workaround for a long-standing concurrency
           issue. Now the *buffering* argument is interpreted as intended.
        """

        default_bufsize = io.DEFAULT_BUFFER_SIZE
        fileio: io.RawIOBase
        # Text mode: always binds a TextIOWrapper
        @overload
        def __init__(
            self: FileObjectPosix[io.TextIOWrapper, str],
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
            self: FileObjectPosix[io.FileIO, bytes],
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
            self: FileObjectPosix[io.FileIO, bytes],
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
            self: FileObjectPosix[io.BufferedRandom, bytes],
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
            self: FileObjectPosix[io.BufferedWriter, bytes],
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
            self: FileObjectPosix[io.BufferedReader, bytes],
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
            self: FileObjectPosix[IO[bytes], bytes],
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
            self: FileObjectPosix[IO[Any], Any],
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

    _FileObjectType: TypeAlias = type[FileObjectPosix[Any, Any] | FileObjectBlock[Any, Any] | FileObjectThread[Any, Any]]
    __all__ = ["FileObjectPosix", "FileObjectThread", "FileObjectBlock", "FileObject"]
else:
    _FileObjectType: TypeAlias = type[FileObjectBlock[Any, Any] | FileObjectThread[Any, Any]]
    __all__ = ["FileObjectThread", "FileObjectBlock", "FileObject"]

FileObject: _FileObjectType
