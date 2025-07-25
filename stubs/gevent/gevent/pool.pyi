"""
Managing greenlets in a group.

The :class:`Group` class in this module abstracts a group of running
greenlets. When a greenlet dies, it's automatically removed from the
group. All running greenlets in a group can be waited on with
:meth:`Group.join`, or all running greenlets can be killed with
:meth:`Group.kill`.

The :class:`Pool` class, which is a subclass of :class:`Group`,
provides a way to limit concurrency: its :meth:`spawn <Pool.spawn>`
method blocks if the number of greenlets in the pool has already
reached the limit, until there is a free slot.
"""

from collections.abc import Callable, Collection, Iterable, Iterator
from typing import Any, TypeVar, overload
from typing_extensions import ParamSpec

from gevent._imap import IMap, IMapUnordered
from gevent.greenlet import Greenlet
from gevent.queue import Full as QueueFull

__all__ = ["Group", "Pool", "PoolFull"]

_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_S = TypeVar("_S")
_P = ParamSpec("_P")

class GroupMappingMixin:
    def spawn(self, func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> Greenlet[_P, _T]:
        """
        A function that runs *func* with *args* and *kwargs*, potentially
        asynchronously. Return a value with a ``get`` method that blocks
        until the results of func are available, and a ``rawlink`` method
        that calls a callback when the results are available.

        If this object has an upper bound on how many asyncronously executing
        tasks can exist, this method may block until a slot becomes available.
        """
    # we would like to use ParamSpec for these, but since args and kwds are passed in as is
    # pyright will complain if we use _P.args/_P.kwargs, it appears to work on mypy though
    # we can probably get away with Sequence and Mapping instead of tuple and dict, but for
    # now we will be strict, just to be safe
    def apply_cb(
        self,
        func: Callable[..., _T],
        args: tuple[Any, ...] | None = None,
        kwds: dict[str, Any] | None = None,
        callback: Callable[[_T], object] | None = None,
    ) -> _T:
        """
        :meth:`apply` the given *func(\\*args, \\*\\*kwds)*, and, if a *callback* is given, run it with the
        results of *func* (unless an exception was raised.)

        The *callback* may be called synchronously or asynchronously. If called
        asynchronously, it will not be tracked by this group. (:class:`Group` and :class:`Pool`
        call it asynchronously in a new greenlet; :class:`~gevent.threadpool.ThreadPool` calls
        it synchronously in the current greenlet.)
        """
    # The ParamSpec of the spawned greenlet can differ from the one being passed in, but the return type will match
    def apply_async(
        self,
        func: Callable[..., _T],
        args: tuple[Any, ...] | None = None,
        kwds: dict[str, Any] | None = None,
        callback: Callable[[_T], object] | None = None,
    ) -> Greenlet[..., _T]:
        """
        A variant of the :meth:`apply` method which returns a :class:`~.Greenlet` object.

        When the returned greenlet gets to run, it *will* call :meth:`apply`,
        passing in *func*, *args* and *kwds*.

        If *callback* is specified, then it should be a callable which
        accepts a single argument. When the result becomes ready
        callback is applied to it (unless the call failed).

        This method will never block, even if this group is full (that is,
        even if :meth:`spawn` would block, this method will not).

        .. caution:: The returned greenlet may or may not be tracked
           as part of this group, so :meth:`joining <join>` this group is
           not a reliable way to wait for the results to be available or
           for the returned greenlet to run; instead, join the returned
           greenlet.

        .. tip:: Because :class:`~.ThreadPool` objects do not track greenlets, the returned
           greenlet will never be a part of it. To reduce overhead and improve performance,
           :class:`Group` and :class:`Pool` may choose to track the returned
           greenlet. These are implementation details that may change.
        """

    def apply(self, func: Callable[..., _T], args: tuple[Any, ...] | None = None, kwds: dict[str, Any] | None = None) -> _T:
        """
        Rough quivalent of the :func:`apply()` builtin function blocking until
        the result is ready and returning it.

        The ``func`` will *usually*, but not *always*, be run in a way
        that allows the current greenlet to switch out (for example,
        in a new greenlet or thread, depending on implementation). But
        if the current greenlet or thread is already one that was
        spawned by this pool, the pool may choose to immediately run
        the `func` synchronously.

        Any exception ``func`` raises will be propagated to the caller of ``apply`` (that is,
        this method will raise the exception that ``func`` raised).
        """

    def map(self, func: Callable[[_T], _S], iterable: Iterable[_T]) -> list[_S]:
        """Return a list made by applying the *func* to each element of
        the iterable.

        .. seealso:: :meth:`imap`
        """

    def map_cb(
        self, func: Callable[[_T], _S], iterable: Iterable[_T], callback: Callable[[list[_S]], object] | None = None
    ) -> list[_S]: ...
    def map_async(
        self, func: Callable[[_T], _S], iterable: Iterable[_T], callback: Callable[[list[_S]], object] | None = None
    ) -> Greenlet[..., list[_S]]:
        """
        A variant of the map() method which returns a Greenlet object that is executing
        the map function.

        If callback is specified then it should be a callable which accepts a
        single argument.
        """

    @overload
    def imap(self, func: Callable[[_T1], _S], iter1: Iterable[_T1], /, *, maxsize: int | None = None) -> IMap[[_T1], _S]:
        """
        imap(func, *iterables, maxsize=None) -> iterable

        An equivalent of :func:`itertools.imap`, operating in parallel.
        The *func* is applied to each element yielded from each
        iterable in *iterables* in turn, collecting the result.

        If this object has a bound on the number of active greenlets it can
        contain (such as :class:`Pool`), then at most that number of tasks will operate
        in parallel.

        :keyword int maxsize: If given and not-None, specifies the maximum number of
            finished results that will be allowed to accumulate awaiting the reader;
            more than that number of results will cause map function greenlets to begin
            to block. This is most useful if there is a great disparity in the speed of
            the mapping code and the consumer and the results consume a great deal of resources.

            .. note:: This is separate from any bound on the number of active parallel
               tasks, though they may have some interaction (for example, limiting the
               number of parallel tasks to the smallest bound).

            .. note:: Using a bound is slightly more computationally expensive than not using a bound.

            .. tip:: The :meth:`imap_unordered` method makes much better
                use of this parameter. Some additional, unspecified,
                number of objects may be required to be kept in memory
                to maintain order by this function.

        :return: An iterable object.

        .. versionchanged:: 1.1b3
            Added the *maxsize* keyword parameter.
        .. versionchanged:: 1.1a1
            Accept multiple *iterables* to iterate in parallel.
        """

    @overload
    def imap(
        self, func: Callable[[_T1, _T2], _S], iter1: Iterable[_T1], iter2: Iterable[_T2], /, *, maxsize: int | None = None
    ) -> IMap[[_T1, _T2], _S]: ...
    @overload
    def imap(
        self,
        func: Callable[[_T1, _T2, _T3], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMap[[_T1, _T2, _T3], _S]: ...
    @overload
    def imap(
        self,
        func: Callable[[_T1, _T2, _T3, _T4], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        iter4: Iterable[_T4],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMap[[_T1, _T2, _T3, _T4], _S]: ...
    @overload
    def imap(
        self,
        func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        iter4: Iterable[_T4],
        iter5: Iterable[_T5],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMap[[_T1, _T2, _T3, _T4, _T5], _S]: ...
    @overload
    def imap(
        self,
        func: Callable[_P, _S],
        iter1: Iterable[Any],
        iter2: Iterable[Any],
        iter3: Iterable[Any],
        iter4: Iterable[Any],
        iter5: Iterable[Any],
        iter6: Iterable[Any],
        /,
        *iterables: Iterable[Any],
        maxsize: int | None = None,
    ) -> IMap[_P, _S]: ...
    @overload
    def imap_unordered(
        self, func: Callable[[_T1], _S], iter1: Iterable[_T1], /, *, maxsize: int | None = None
    ) -> IMapUnordered[[_T1], _S]:
        """
        imap_unordered(func, *iterables, maxsize=None) -> iterable

        The same as :meth:`imap` except that the ordering of the results
        from the returned iterator should be considered in arbitrary
        order.

        This is lighter weight than :meth:`imap` and should be preferred if order
        doesn't matter.

        .. seealso:: :meth:`imap` for more details.
        """

    @overload
    def imap_unordered(
        self, func: Callable[[_T1, _T2], _S], iter1: Iterable[_T1], iter2: Iterable[_T2], /, *, maxsize: int | None = None
    ) -> IMapUnordered[[_T1, _T2], _S]: ...
    @overload
    def imap_unordered(
        self,
        func: Callable[[_T1, _T2, _T3], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMapUnordered[[_T1, _T2, _T3], _S]: ...
    @overload
    def imap_unordered(
        self,
        func: Callable[[_T1, _T2, _T3, _T4], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        iter4: Iterable[_T4],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMapUnordered[[_T1, _T2, _T3, _T4], _S]: ...
    @overload
    def imap_unordered(
        self,
        func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
        iter1: Iterable[_T1],
        iter2: Iterable[_T2],
        iter3: Iterable[_T3],
        iter4: Iterable[_T4],
        iter5: Iterable[_T5],
        /,
        *,
        maxsize: int | None = None,
    ) -> IMapUnordered[[_T1, _T2, _T3, _T4, _T5], _S]: ...
    @overload
    def imap_unordered(
        self,
        func: Callable[_P, _S],
        iter1: Iterable[Any],
        iter2: Iterable[Any],
        iter3: Iterable[Any],
        iter4: Iterable[Any],
        iter5: Iterable[Any],
        iter6: Iterable[Any],
        /,
        *iterables: Iterable[Any],
        maxsize: int | None = None,
    ) -> IMapUnordered[_P, _S]: ...

# TODO: Consider making these generic in Greenlet. The drawback would be, that it
#       wouldn't be possible to mix Greenlets with different return values/ParamSpecs
#       unless you bind Grenlet[..., object], but in that case all the spawn/apply/map
#       methods become less helpful, because the return types cannot be as specific...
#       We would need higher-kinded TypeVars if we wanted to give up neither
class Group(GroupMappingMixin):
    """
    Maintain a group of greenlets that are still running, without
    limiting their number.

    Links to each item and removes it upon notification.

    Groups can be iterated to discover what greenlets they are tracking,
    they can be tested to see if they contain a greenlet, and they know the
    number (len) of greenlets they are tracking. If they are not tracking any
    greenlets, they are False in a boolean context.

    .. attribute:: greenlet_class

        Either :class:`gevent.Greenlet` (the default) or a subclass.
        These are the type of
        object we will :meth:`spawn`. This can be
        changed on an instance or in a subclass.
    """

    greenlet_class: type[Greenlet[..., Any]]
    greenlets: set[Greenlet[..., Any]]
    dying: set[Greenlet[..., Any]]
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, grenlets: Collection[Greenlet[..., object]], /) -> None: ...
    def __len__(self) -> int:
        """
        Answer how many greenlets we are tracking. Note that if we are empty,
        we are False in a boolean context.
        """

    def __contains__(self, item: Greenlet[..., object]) -> bool:
        """
        Answer if we are tracking the given greenlet.
        """

    def __iter__(self) -> Iterator[Greenlet[..., object]]:
        """
        Iterate across all the greenlets we are tracking, in no particular order.
        """

    def add(self, greenlet: Greenlet[..., object]) -> None:
        """
        Begin tracking the *greenlet*.

        If this group is :meth:`full`, then this method may block
        until it is possible to track the greenlet.

        Typically the *greenlet* should **not** be started when
        it is added because if this object blocks in this method,
        then the *greenlet* may run to completion before it is tracked.
        """

    def discard(self, greenlet: Greenlet[..., object]) -> None:
        """
        Stop tracking the greenlet.
        """

    def start(self, greenlet: Greenlet[..., object]) -> None:
        """
        Add the **unstarted** *greenlet* to the collection of greenlets
        this group is monitoring, and then start it.
        """

    def join(self, timeout: float | None = None, raise_error: bool = False) -> bool:
        """
        Wait for this group to become empty *at least once*.

        If there are no greenlets in the group, returns immediately.

        .. note:: By the time the waiting code (the caller of this
           method) regains control, a greenlet may have been added to
           this group, and so this object may no longer be empty. (That
           is, ``group.join(); assert len(group) == 0`` is not
           guaranteed to hold.) This method only guarantees that the group
           reached a ``len`` of 0 at some point.

        :keyword bool raise_error: If True (*not* the default), if any
            greenlet that finished while the join was in progress raised
            an exception, that exception will be raised to the caller of
            this method. If multiple greenlets raised exceptions, which
            one gets re-raised is not determined. Only greenlets currently
            in the group when this method is called are guaranteed to
            be checked for exceptions.

        :return bool: A value indicating whether this group became empty.
           If the timeout is specified and the group did not become empty
           during that timeout, then this will be a false value. Otherwise
           it will be a true value.

        .. versionchanged:: 1.2a1
           Add the return value.
        """

    def kill(
        self, exception: type[BaseException] | BaseException = ..., block: bool = True, timeout: float | None = None
    ) -> None:
        """
        Kill all greenlets being tracked by this group.
        """

    def killone(
        self,
        greenlet: Greenlet[..., object],
        exception: type[BaseException] | BaseException = ...,
        block: bool = True,
        timeout: float | None = None,
    ) -> None:
        """
        If the given *greenlet* is running and being tracked by this group,
        kill it.
        """

    def full(self) -> bool:
        """
        Return a value indicating whether this group can track more greenlets.

        In this implementation, because there are no limits on the number of
        tracked greenlets, this will always return a ``False`` value.
        """

    def wait_available(self, timeout: float | None = None) -> int | None:
        """
        Block until it is possible to :meth:`spawn` a new greenlet.

        In this implementation, because there are no limits on the number
        of tracked greenlets, this will always return immediately.
        """

class PoolFull(QueueFull):
    """
    Raised when a Pool is full and an attempt was made to
    add a new greenlet to it in non-blocking mode.
    """

class Pool(Group):
    size: int | None
    def __init__(self, size: int | None = None, greenlet_class: type[Greenlet[..., object]] | None = None) -> None:
        """
        Create a new pool.

        A pool is like a group, but the maximum number of members
        is governed by the *size* parameter.

        :keyword int size: If given, this non-negative integer is the
            maximum count of active greenlets that will be allowed in
            this pool. A few values have special significance:

            * `None` (the default) places no limit on the number of
              greenlets. This is useful when you want to track, but not limit,
              greenlets. In general, a :class:`Group`
              may be a more efficient way to achieve the same effect, but some things
              need the additional abilities of this class (one example being the *spawn*
              parameter of :class:`gevent.baseserver.BaseServer` and
              its subclass :class:`gevent.pywsgi.WSGIServer`).

            * ``0`` creates a pool that can never have any active greenlets. Attempting
              to spawn in this pool will block forever. This is only useful
              if an application uses :meth:`wait_available` with a timeout and checks
              :meth:`free_count` before attempting to spawn.
        """

    def wait_available(self, timeout: float | None = None) -> int:
        """
        Wait until it's possible to spawn a greenlet in this pool.

        :param float timeout: If given, only wait the specified number
            of seconds.

        .. warning:: If the pool was initialized with a size of 0, this
           method will block forever unless a timeout is given.

        :return: A number indicating how many new greenlets can be put into
           the pool without blocking.

        .. versionchanged:: 1.1a3
            Added the ``timeout`` parameter.
        """

    def free_count(self) -> int:
        """
        Return a number indicating *approximately* how many more members
        can be added to this pool.
        """

    def start(self, greenlet: Greenlet[..., object], blocking: bool = True, timeout: float | None = None) -> None:
        """
        start(greenlet, blocking=True, timeout=None) -> None

        Add the **unstarted** *greenlet* to the collection of greenlets
        this group is monitoring and then start it.

        Parameters are as for :meth:`add`.
        """

    def add(self, greenlet: Greenlet[..., object], blocking: bool = True, timeout: float | None = None) -> None:
        """
        Begin tracking the given **unstarted** greenlet, possibly blocking
        until space is available.

        Usually you should call :meth:`start` to track and start the greenlet
        instead of using this lower-level method, or :meth:`spawn` to
        also create the greenlet.

        :keyword bool blocking: If True (the default), this function
            will block until the pool has space or a timeout occurs.  If
            False, this function will immediately raise a Timeout if the
            pool is currently full.
        :keyword float timeout: The maximum number of seconds this
            method will block, if ``blocking`` is True.  (Ignored if
            ``blocking`` is False.)
        :raises PoolFull: if either ``blocking`` is False and the pool
            was full, or if ``blocking`` is True and ``timeout`` was
            exceeded.

        ..  caution:: If the *greenlet* has already been started and
            *blocking* is true, then the greenlet may run to completion
            while the current greenlet blocks waiting to track it. This would
            enable higher concurrency than desired.

        ..  seealso:: :meth:`Group.add`

        ..  versionchanged:: 1.3.0 Added the ``blocking`` and
            ``timeout`` parameters.
        """
