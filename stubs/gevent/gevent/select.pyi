"""
Waiting for I/O completion.
"""

import sys
from _typeshed import FileDescriptorLike
from collections.abc import Iterable
from select import error as error
from typing import Any

def select(
    rlist: Iterable[Any], wlist: Iterable[Any], xlist: Iterable[Any], timeout: float | None = None
) -> tuple[list[Any], list[Any], list[Any]]:
    """An implementation of :obj:`select.select` that blocks only the current greenlet.

    .. caution:: *xlist* is ignored.

    .. versionchanged:: 1.2a1
       Raise a :exc:`ValueError` if timeout is negative. This matches Python 3's
       behaviour (Python 2 would raise a ``select.error``). Previously gevent had
       undefined behaviour.
    .. versionchanged:: 1.2a1
       Raise an exception if any of the file descriptors are invalid.
    """

if sys.platform != "win32":
    __all__ = ["error", "poll", "select"]
else:
    __all__ = ["error", "select"]

class poll:
    """
    An implementation of :obj:`select.poll` that blocks only the current greenlet.

    With only one exception, the interface is the same as the standard library interface.

    .. caution:: ``POLLPRI`` data is not supported.

    .. versionadded:: 1.1b1
    .. versionchanged:: 1.5
       This is now always defined, regardless of whether the standard library
       defines :func:`select.poll` or not. Note that it may have different performance
       characteristics.
    """

    def register(self, fd: FileDescriptorLike, eventmask: int = ...) -> None:
        """
        Register a file descriptor *fd* with the polling object.

        Future calls to the :meth:`poll`` method will then check
        whether the file descriptor has any pending I/O events. *fd* can
        be either an integer, or an object with a ``fileno()`` method that
        returns an integer. File objects implement ``fileno()``, so they
        can also be used as the argument (but remember that regular
        files are usually always ready).

        *eventmask* is an optional bitmask describing the type of events
        you want to check for, and can be a combination of the
        constants ``POLLIN``, and ``POLLOUT`` (``POLLPRI`` is not supported).
        """

    def modify(self, fd: FileDescriptorLike, eventmask: int) -> None:
        """
        Change the set of events being watched on *fd*.
        """

    def poll(self, timeout: float | None = None) -> list[tuple[int, int]]:
        """
        poll the registered fds.

        .. versionchanged:: 1.2a1
           File descriptors that are closed are reported with POLLNVAL.

        .. versionchanged:: 1.3a2
           Under libuv, interpret *timeout* values less than 0 the same as *None*,
           i.e., block. This was always the case with libev.
        """

    def unregister(self, fd: FileDescriptorLike) -> None:
        """
        Unregister the *fd*.

        .. versionchanged:: 1.2a1
           Raise a `KeyError` if *fd* was not registered, like the standard
           library. Previously gevent did nothing.
        """
