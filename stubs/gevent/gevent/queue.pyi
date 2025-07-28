"""
Synchronized queues.

The :mod:`gevent.queue` module implements multi-producer, multi-consumer queues
that work across greenlets, with the API similar to the classes found in the
standard :mod:`Queue` and :class:`multiprocessing <multiprocessing.Queue>` modules.

The classes in this module implement the iterator protocol. Iterating
over a queue means repeatedly calling :meth:`get <Queue.get>` until
:meth:`get <Queue.get>` returns ``StopIteration`` (specifically that
class, not an instance or subclass).

    >>> import gevent.queue
    >>> queue = gevent.queue.Queue()
    >>> queue.put(1)
    >>> queue.put(2)
    >>> queue.put(StopIteration)
    >>> for item in queue:
    ...    print(item)
    1
    2

.. versionchanged:: 1.0
       ``Queue(0)`` now means queue of infinite size, not a channel. A :exc:`DeprecationWarning`
       will be issued with this argument.

.. versionchanged:: 25.4.1
   :class:`Queue` was renamed to :class:`SimpleQueue`, while :class:`JoinableQueue` was
   renamed to :class:`Queue` (`JoinableQueue` remains a backwards compatible alias).
   This adds the ability to ``join()`` all queues, like the standard library.

   Previously ``SimpleQueue`` was an alias for the undocumented Python
   implementation ``queue._PySimpleQueue``; now it is gevent's own implementation.
   This ensures that it is cooperative even without monkey-patching.
"""

import sys
import types
from collections import deque
from collections.abc import Iterable

# technically it is using _PySimpleQueue, which has the same interface as SimpleQueue
from queue import Empty as Empty, Full as Full
from typing import Any, Generic, Literal, TypeVar, final, overload
from typing_extensions import Self

from gevent._waiter import Waiter
from gevent.hub import Hub

__all__ = ["Queue", "PriorityQueue", "LifoQueue", "SimpleQueue", "JoinableQueue", "Channel", "Empty", "Full", "ShutDown"]

if sys.version_info >= (3, 13):
    from queue import ShutDown as ShutDown
else:
    class ShutDown(Exception): ...

_T = TypeVar("_T")

class SimpleQueue(Generic[_T]):
    """SimpleQueue(maxsize=None, items=(), _warn_depth=2)

    Create a queue object with a given maximum size.

    If *maxsize* is less than or equal to zero or ``None``, the queue
    size is infinite.

    Queues have a ``len`` equal to the number of items in them (the :meth:`qsize`),
    but in a boolean context they are always True.

    .. versionchanged:: 1.1b3
       Queues now support :func:`len`; it behaves the same as :meth:`qsize`.
    .. versionchanged:: 1.1b3
       Multiple greenlets that block on a call to :meth:`put` for a full queue
       will now be awakened to put their items into the queue in the order in which
       they arrived. Likewise, multiple greenlets that block on a call to :meth:`get` for
       an empty queue will now receive items in the order in which they blocked. An
       implementation quirk under CPython *usually* ensured this was roughly the case
       previously anyway, but that wasn't the case for PyPy.
    .. versionchanged:: 24.10.1
       Implement the ``shutdown`` methods from Python 3.13.
    .. versionchanged:: 25.4.1
       Renamed from ``Queue`` to ``SimpleQueue`` to better match the standard library.
       While this class no longer has a ``shutdown`` method, the new ``Queue`` class
       (previously ``JoinableQueue``) continues to have it.
    .. versionchanged:: 25.4.2
       Make this class subscriptable.
    """

    @property
    def hub(self) -> Hub: ...  # readonly in Cython
    @property
    def queue(self) -> deque[_T]: ...  # readonly in Cython
    maxsize: int | None
    is_shutdown: bool

    @classmethod
    def __class_getitem__(cls, item: Any, /) -> types.GenericAlias:
        """Represent a PEP 585 generic type

        E.g. for t = list[int], t.__origin__ is list and t.__args__ is (int,).
        """

    @overload
    def __init__(self, maxsize: int | None = None) -> None: ...
    @overload
    def __init__(self, maxsize: int | None, items: Iterable[_T]) -> None: ...
    @overload
    def __init__(self, maxsize: int | None = None, *, items: Iterable[_T]) -> None: ...
    def copy(self) -> Self:
        """SimpleQueue.copy(self)"""

    def empty(self) -> bool:
        """SimpleQueue.empty(self) -> bool
        Return ``True`` if the queue is empty, ``False`` otherwise.
        """

    def full(self) -> bool:
        """SimpleQueue.full(self) -> bool
        Return ``True`` if the queue is full, ``False`` otherwise.

                ``Queue(None)`` is never full.
        """

    def get(self, block: bool = True, timeout: float | None = None) -> _T:
        """SimpleQueue.get(self, block=True, timeout=None)

        Remove and return an item from the queue.

        If optional args *block* is true and *timeout* is ``None`` (the default),
        block if necessary until an item is available. If *timeout* is a positive number,
        it blocks at most *timeout* seconds and raises the :class:`Empty` exception
        if no item was available within that time. Otherwise (*block* is false), return
        an item if one is immediately available, else raise the :class:`Empty` exception
        (*timeout* is ignored in that case).
        """

    def get_nowait(self) -> _T:
        """SimpleQueue.get_nowait(self)
        Remove and return an item from the queue without blocking.

                Only get an item if one is immediately available. Otherwise
                raise the :class:`Empty` exception.
        """

    def peek(self, block: bool = True, timeout: float | None = None) -> _T:
        """SimpleQueue.peek(self, block=True, timeout=None)
        Return an item from the queue without removing it.

                If optional args *block* is true and *timeout* is ``None`` (the default),
                block if necessary until an item is available. If *timeout* is a positive number,
                it blocks at most *timeout* seconds and raises the :class:`Empty` exception
                if no item was available within that time. Otherwise (*block* is false), return
                an item if one is immediately available, else raise the :class:`Empty` exception
                (*timeout* is ignored in that case).
        """

    def peek_nowait(self) -> _T:
        """SimpleQueue.peek_nowait(self)
        Return an item from the queue without blocking.

                Only return an item if one is immediately available. Otherwise
                raise the :class:`Empty` exception.
        """

    def put(self, item: _T, block: bool = True, timeout: float | None = None) -> None:
        """SimpleQueue.put(self, item, block=True, timeout=None)

        Put an item into the queue.

        If optional arg *block* is true and *timeout* is ``None`` (the default),
        block if necessary until a free slot is available. If *timeout* is
        a positive number, it blocks at most *timeout* seconds and raises
        the :class:`Full` exception if no free slot was available within that time.
        Otherwise (*block* is false), put an item on the queue if a free slot
        is immediately available, else raise the :class:`Full` exception (*timeout*
        is ignored in that case).

        ... versionchanged:: 24.10.1
           Now raises a ``ValueError`` for a negative *timeout* in the cases
           that CPython does.
        """

    def put_nowait(self, item: _T) -> None:
        """SimpleQueue.put_nowait(self, item)
        Put an item into the queue without blocking.

                Only enqueue the item if a free slot is immediately available.
                Otherwise raise the :class:`Full` exception.
        """

    def qsize(self) -> int:
        """SimpleQueue.qsize(self) -> Py_ssize_t
        Return the size of the queue.
        """

    def __bool__(self) -> bool:
        """True if self else False"""

    def __iter__(self) -> Self:
        """Implement iter(self)."""

    def __len__(self) -> int:
        """
        Return the size of the queue. This is the same as :meth:`qsize`.

        .. versionadded: 1.1b3

            Previously, getting len() of a queue would raise a TypeError.
        """

    def __next__(self) -> _T: ...
    next = __next__

class Queue(SimpleQueue[_T]):
    """Queue(maxsize=None, items=(), unfinished_tasks=None)

    A subclass of :class:`SimpleQueue` that additionally has
    :meth:`task_done` and :meth:`join` methods.

    .. versionchanged:: 25.4.1
       Renamed from ``JoinablQueue`` to simply ``Queue`` to better
       match the capability of the standard library :class:`queue.Queue`.
    """

    @property
    def unfinished_tasks(self) -> int: ...  # readonly in Cython
    @overload
    def __init__(self, maxsize: int | None = None, *, unfinished_tasks: int | None = None) -> None:
        """

        .. versionchanged:: 1.1a1
           If *unfinished_tasks* is not given, then all the given *items*
           (if any) will be considered unfinished.

        """

    @overload
    def __init__(self, maxsize: int | None, items: Iterable[_T], unfinished_tasks: int | None = None) -> None: ...
    @overload
    def __init__(self, maxsize: int | None = None, *, items: Iterable[_T], unfinished_tasks: int | None = None) -> None: ...
    def join(self, timeout: float | None = None) -> bool:
        """Queue.join(self, timeout=None)

        Block until all items in the queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the queue.
        The count goes down whenever a consumer thread calls :meth:`task_done` to indicate
        that the item was retrieved and all work on it is complete. When the count of
        unfinished tasks drops to zero, :meth:`join` unblocks.

        :param float timeout: If not ``None``, then wait no more than this time in seconds
            for all tasks to finish.
        :return: ``True`` if all tasks have finished; if ``timeout`` was given and expired before
            all tasks finished, ``False``.

        .. versionchanged:: 1.1a1
           Add the *timeout* parameter.
        """

    def task_done(self) -> None:
        """Queue.task_done(self)
        Indicate that a formerly enqueued task is complete. Used by queue consumer threads.
                For each :meth:`get <Queue.get>` used to fetch a task, a subsequent call to
                :meth:`task_done` tells the queue that the processing on the task is complete.

                If a :meth:`join` is currently blocking, it will resume when all items have been processed
                (meaning that a :meth:`task_done` call was received for every item that had been
                :meth:`put <Queue.put>` into the queue).

                Raises a :exc:`ValueError` if called more times than there were items placed in the queue.
        """

    def shutdown(self, immediate: bool = False) -> None:
        """Queue.shutdown(self, immediate=False)

        "Shut-down the queue, making queue gets and puts raise
        `ShutDown`.

        By default, gets will only raise once the queue is empty. Set
        *immediate* to True to make gets raise immediately instead.

        All blocked callers of `put` and `get` will be unblocked.

        In joinable queues, if *immediate*, a task is marked as done
        for each item remaining in the queue, which may unblock
        callers of `join`.
        """

JoinableQueue = Queue

@final
class UnboundQueue(Queue[_T]):
    """UnboundQueue(maxsize=None, items=())"""

    @overload
    def __init__(self, maxsize: None = None) -> None: ...
    @overload
    def __init__(self, maxsize: None, items: Iterable[_T]) -> None: ...
    @overload
    def __init__(self, maxsize: None = None, *, items: Iterable[_T]) -> None: ...

class PriorityQueue(Queue[_T]):
    """A subclass of :class:`Queue` that retrieves entries in priority order (lowest first).

    Entries are typically tuples of the form: ``(priority number, data)``.

    .. versionchanged:: 1.2a1
       Any *items* given to the constructor will now be passed through
       :func:`heapq.heapify` to ensure the invariants of this class hold.
       Previously it was just assumed that they were already a heap.
    """

class LifoQueue(Queue[_T]):
    """
    A subclass of :class:`JoinableQueue` that retrieves most recently added entries first.

    .. versionchanged:: 24.10.1
       Now extends :class:`JoinableQueue` instead of just :class:`Queue`.

    """

class Channel(Generic[_T]):
    """Channel(maxsize=1)

    A queue-like object that can only hold one item at a
    time.

    This is commonly used as a synchronization primitive,
    and is implemented efficiently for this use-case.

    .. versionchanged:: 25.4.2
       Make this class subscriptable.
    """

    @property
    def getters(self) -> deque[Waiter[Any]]: ...  # readonly in Cython
    @property
    def putters(self) -> deque[tuple[_T, Waiter[Any]]]: ...  # readonly in Cython
    @property
    def hub(self) -> Hub: ...  # readonly in Cython
    def __init__(self, maxsize: Literal[1] = 1) -> None: ...
    @classmethod
    def __class_getitem__(cls, item: Any, /) -> types.GenericAlias:
        """Represent a PEP 585 generic type

        E.g. for t = list[int], t.__origin__ is list and t.__args__ is (int,).
        """

    @property
    def balance(self) -> int: ...
    def qsize(self) -> Literal[0]:
        """Channel.qsize(self)"""

    def empty(self) -> Literal[True]:
        """Channel.empty(self)"""

    def full(self) -> Literal[True]:
        """Channel.full(self)"""

    def put(self, item: _T, block: bool = True, timeout: float | None = None) -> None:
        """Channel.put(self, item, block=True, timeout=None)"""

    def put_nowait(self, item: _T) -> None:
        """Channel.put_nowait(self, item)"""

    def get(self, block: bool = True, timeout: float | None = None) -> _T:
        """Channel.get(self, block=True, timeout=None)"""

    def get_nowait(self) -> _T:
        """Channel.get_nowait(self)"""

    def __iter__(self) -> Self:
        """Implement iter(self)."""

    def __next__(self) -> _T: ...
    next = __next__
