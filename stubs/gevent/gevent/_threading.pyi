"""
A small selection of primitives that always work with
native threads. This has very limited utility and is
targeted only for the use of gevent's threadpool.
"""

from _thread import LockType, allocate_lock as Lock
from typing import Generic, NewType, TypeVar

__all__ = ["Lock", "Queue", "EmptyTimeout"]

_T = TypeVar("_T")
_Cookie = NewType("_Cookie", LockType)

class EmptyTimeout(Exception):
    """Raised from :meth:`Queue.get` if no item is available in the timeout."""

class Queue(Generic[_T]):
    """
    Create a queue object.

    The queue is always infinite size.
    """

    unfinished_tasks: int
    def __init__(self) -> None: ...
    def task_done(self) -> None:
        """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """

    def qsize(self) -> int:
        """Return the approximate size of the queue (not reliable!)."""

    def empty(self) -> bool:
        """Return True if the queue is empty, False otherwise (not reliable!)."""

    def full(self) -> bool:
        """Return True if the queue is full, False otherwise (not reliable!)."""

    def put(self, item: _T) -> None:
        """Put an item into the queue."""

    def get(self, cookie: _Cookie, timeout: int = -1) -> _T:
        """
        Remove and return an item from the queue.

        If *timeout* is given, and is not -1, then we will
        attempt to wait for only that many seconds to get an item.
        If those seconds elapse and no item has become available,
        raises :class:`EmptyTimeout`.
        """

    def allocate_cookie(self) -> _Cookie:
        """
        Create and return the *cookie* to pass to `get()`.

        Each thread that will use `get` needs a distinct cookie.
        """

    def kill(self) -> None:
        """
        Call to destroy this object.

        Use this when it's not possible to safely drain the queue, e.g.,
        after a fork when the locks are in an uncertain state.
        """
