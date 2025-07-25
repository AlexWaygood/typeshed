"""Python comes with a many great data structures, from :class:`dict`
to :class:`collections.deque`, and no shortage of serviceable
algorithm implementations, from :func:`sorted` to :mod:`bisect`. But
priority queues are curiously relegated to an example documented in
:mod:`heapq`. Even there, the approach presented is not full-featured
and object-oriented. There is a built-in priority queue,
:class:`Queue.PriorityQueue`, but in addition to its austere API, it
carries the double-edged sword of threadsafety, making it fine for
multi-threaded, multi-consumer applications, but high-overhead for
cooperative/single-threaded use cases.

The ``queueutils`` module currently provides two Queue
implementations: :class:`HeapPriorityQueue`, based on a heap, and
:class:`SortedPriorityQueue`, based on a sorted list. Both use a
unified API based on :class:`BasePriorityQueue` to facilitate testing
the slightly different performance characteristics on various
application use cases.

>>> pq = PriorityQueue()
>>> pq.add('low priority task', 0)
>>> pq.add('high priority task', 2)
>>> pq.add('medium priority task 1', 1)
>>> pq.add('medium priority task 2', 1)
>>> len(pq)
4
>>> pq.pop()
'high priority task'
>>> pq.peek()
'medium priority task 1'
>>> len(pq)
3

"""

from typing_extensions import TypeAlias

class BasePriorityQueue:
    """The abstract base class for the other PriorityQueues in this
    module. Override the ``_backend_type`` class attribute, as well as
    the :meth:`_push_entry` and :meth:`_pop_entry` staticmethods for
    custom subclass behavior. (Don't forget to use
    :func:`staticmethod`).

    Args:
        priority_key (callable): A function that takes *priority* as
            passed in by :meth:`add` and returns a real number
            representing the effective priority.

    """

    def __init__(self, **kw) -> None: ...
    def add(self, task, priority: int | None = None) -> None:
        """
        Add a task to the queue, or change the *task*'s priority if *task*
        is already in the queue. *task* can be any hashable object,
        and *priority* defaults to ``0``. Higher values representing
        higher priority, but this behavior can be controlled by
        setting *priority_key* in the constructor.
        """

    def remove(self, task) -> None:
        """Remove a task from the priority queue. Raises :exc:`KeyError` if
        the *task* is absent.
        """

    def peek(self, default=...):
        """Read the next value in the queue without removing it. Returns
        *default* on an empty queue, or raises :exc:`KeyError` if
        *default* is not set.
        """

    def pop(self, default=...):
        """Remove and return the next value in the queue. Returns *default* on
        an empty queue, or raises :exc:`KeyError` if *default* is not
        set.
        """

    def __len__(self) -> int:
        """Return the number of tasks in the queue."""

class HeapPriorityQueue(BasePriorityQueue):
    """A priority queue inherited from :class:`BasePriorityQueue`,
    backed by a list and based on the :func:`heapq.heappop` and
    :func:`heapq.heappush` functions in the built-in :mod:`heapq`
    module.
    """

class SortedPriorityQueue(BasePriorityQueue):
    """A priority queue inherited from :class:`BasePriorityQueue`, based
    on the :func:`bisect.insort` approach for in-order insertion into
    a sorted list.
    """

PriorityQueue: TypeAlias = SortedPriorityQueue

__all__ = ["PriorityQueue", "BasePriorityQueue", "HeapPriorityQueue", "SortedPriorityQueue"]
