"""
Low-level operating system functions from :mod:`os`.

Cooperative I/O
===============

This module provides cooperative versions of :func:`os.read` and
:func:`os.write`. These functions are *not* monkey-patched; you
must explicitly call them or monkey patch them yourself.

POSIX functions
---------------

On POSIX, non-blocking IO is available.

- :func:`nb_read`
- :func:`nb_write`
- :func:`make_nonblocking`

All Platforms
-------------

On non-POSIX platforms (e.g., Windows), non-blocking IO is not
available. On those platforms (and on POSIX), cooperative IO can
be done with the threadpool.

- :func:`tp_read`
- :func:`tp_write`

Child Processes
===============

The functions :func:`fork` and (on POSIX) :func:`forkpty` and :func:`waitpid` can be used
to manage child processes.

.. warning::

   Forking a process that uses greenlets does not eliminate all non-running
   greenlets. Any that were scheduled in the hub of the forking thread in the parent
   remain scheduled in the child; compare this to how normal threads operate. (This behaviour
   may change is a subsequent major release.)
"""

import os
import sys
from _typeshed import FileDescriptor, ReadableBuffer
from collections.abc import Callable
from typing import Literal

from gevent._types import _ChildWatcher, _Loop

def tp_read(fd: FileDescriptor, n: int) -> bytes:
    """Read up to *n* bytes from file descriptor *fd*. Return a string
    containing the bytes read. If end-of-file is reached, an empty string
    is returned.

    Reading is done using the threadpool.
    """

def tp_write(fd: FileDescriptor, buf: ReadableBuffer) -> int:
    """Write bytes from buffer *buf* to file descriptor *fd*. Return the
    number of bytes written.

    Writing is done using the threadpool.
    """

if sys.platform != "win32":
    def make_nonblocking(fd: FileDescriptor) -> Literal[True] | None:
        """Put the file descriptor *fd* into non-blocking mode if
        possible.

        :return: A boolean value that evaluates to True if successful.
        """

    def nb_read(fd: FileDescriptor, n: int) -> bytes:
        """
        Read up to *n* bytes from file descriptor *fd*. Return a
        byte string containing the bytes read, which may be shorter than
        *n*. If end-of-file is reached, an empty string is returned.

        The descriptor must be in non-blocking mode.
        """

    def nb_write(fd: FileDescriptor, buf: ReadableBuffer) -> int:
        """
        Write some number of bytes from buffer *buf* to file
        descriptor *fd*. Return the number of bytes written, which may
        be less than the length of *buf*.

        The file descriptor must be in non-blocking mode.
        """
    fork = os.fork
    forkpty = os.forkpty
    def fork_gevent() -> int:
        """
        Forks the process using :func:`os.fork` and prepares the
        child process to continue using gevent before returning.

        .. note::

            The PID returned by this function may not be waitable with
            either the original :func:`os.waitpid` or this module's
            :func:`waitpid` and it may not generate SIGCHLD signals if
            libev child watchers are or ever have been in use. For
            example, the :mod:`gevent.subprocess` module uses libev
            child watchers (which parts of gevent use libev child
            watchers is subject to change at any time). Most
            applications should use :func:`fork_and_watch`, which is
            monkey-patched as the default replacement for
            :func:`os.fork` and implements the ``fork`` function of
            this module by default, unless the environment variable
            ``GEVENT_NOWAITPID`` is defined before this module is
            imported.

        .. versionadded:: 1.1b2
        """

    def forkpty_gevent() -> tuple[int, int]:
        """
        Forks the process using :func:`os.forkpty` and prepares the
        child process to continue using gevent before returning.

        Returns a tuple (pid, master_fd). The `master_fd` is *not* put into
        non-blocking mode.

        Availability: Some Unix systems.

        .. seealso:: This function has the same limitations as :func:`fork_gevent`.

        .. versionadded:: 1.1b5
        """
    waitpid = os.waitpid
    def fork_and_watch(
        callback: Callable[[_ChildWatcher], object] | None = None,
        loop: _Loop | None = None,
        ref: bool = False,
        fork: Callable[[], int] = ...,
    ) -> int:
        """
        Fork a child process and start a child watcher for it in the parent process.

        This call cooperates with :func:`waitpid` to enable cooperatively waiting
        for children to finish. When monkey-patching, these functions are patched in as
        :func:`os.fork` and :func:`os.waitpid`, respectively.

        In the child process, this function calls :func:`gevent.hub.reinit` before returning.

        Availability: POSIX.

        :keyword callback: If given, a callable that will be called with the child watcher
            when the child finishes.
        :keyword loop: The loop to start the watcher in. Defaults to the
            loop of the current hub.
        :keyword fork: The fork function. Defaults to :func:`the one defined in this
            module <gevent.os.fork_gevent>` (which automatically calls :func:`gevent.hub.reinit`).
            Pass the builtin :func:`os.fork` function if you do not need to
            initialize gevent in the child process.

        .. versionadded:: 1.1b1
        .. seealso::
            :func:`gevent.monkey.get_original` To access the builtin :func:`os.fork`.
        """

    def forkpty_and_watch(
        callback: Callable[[_ChildWatcher], object] | None = None,
        loop: _Loop | None = None,
        ref: bool = False,
        forkpty: Callable[[], tuple[int, int]] = ...,
    ) -> tuple[int, int]:
        """
        Like :func:`fork_and_watch`, except using :func:`forkpty_gevent`.

        Availability: Some Unix systems.

        .. versionadded:: 1.1b5
        """
    posix_spawn = os.posix_spawn
    posix_spawnp = os.posix_spawnp
