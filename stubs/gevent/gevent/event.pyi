"""Basic synchronization primitives: Event and AsyncResult"""

from types import TracebackType
from typing import Generic, Literal, Protocol, TypeVar, overload
from typing_extensions import TypeAlias

from gevent._abstract_linkable import AbstractLinkable

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
# gevent generally allows the tracebock to be omitted, it can also fail to serialize
# in which case it will be None as well.
_ExcInfo: TypeAlias = tuple[type[BaseException], BaseException, TracebackType | None]
_OptExcInfo: TypeAlias = _ExcInfo | tuple[None, None, None]

class _ValueSource(Protocol[_T_co]):
    def successful(self) -> bool: ...
    @property
    def value(self) -> _T_co | None: ...
    @property
    def exception(self) -> BaseException | None: ...

class Event(AbstractLinkable):
    """Event()

    A synchronization primitive that allows one greenlet to wake up
    one or more others. It has the same interface as
    :class:`threading.Event` but works across greenlets.

    .. important::
       This object is for communicating among greenlets within the
       same thread *only*! Do not try to use it to communicate across threads.

    An event object manages an internal flag that can be set to true
    with the :meth:`set` method and reset to false with the
    :meth:`clear` method. The :meth:`wait` method blocks until the
    flag is true; as soon as the flag is set to true, all greenlets
    that are currently blocked in a call to :meth:`wait` will be scheduled
    to awaken.

    Note that the flag may be cleared and set many times before
    any individual greenlet runs; all the greenlet can know for sure is that the
    flag was set *at least once* while it was waiting.
    If the greenlet cares whether the flag is still
    set, it must check with :meth:`ready` and possibly call back into
    :meth:`wait` again.

    .. note::

        The exact order and timing in which waiting greenlets are awakened is not determined.

        Once the event is set, other greenlets may run before any waiting greenlets
        are awakened.

        While the code here will awaken greenlets in the order in which they
        waited, each such greenlet that runs may in turn cause other greenlets
        to run.

        These details may change in the future.

    .. versionchanged:: 1.5a3

        Waiting greenlets are now awakened in
        the order in which they waited.

    .. versionchanged:: 1.5a3

        The low-level ``rawlink`` method (most users won't use this) now
        automatically unlinks waiters before calling them.

    .. versionchanged:: 20.5.1

        Callers to ``wait`` that find the event already set will now run
        after any other waiters that had to block. See :issue:`1520`.
    """

    def __init__(self) -> None: ...
    def is_set(self) -> bool:
        """Event.is_set(self)
        Return true if and only if the internal flag is true.
        """

    def isSet(self) -> bool:
        """Event.isSet(self)"""

    def ready(self) -> bool:
        """Event.ready(self) -> bool"""

    def set(self) -> None:
        """Event.set(self)

        Set the internal flag to true.

        All greenlets waiting for it to become true are awakened in
        some order at some time in the future. Greenlets that call
        :meth:`wait` once the flag is true will not block at all
        (until :meth:`clear` is called).
        """

    def clear(self) -> None:
        """Event.clear(self)

        Reset the internal flag to false.

        Subsequently, threads calling :meth:`wait` will block until
        :meth:`set` is called to set the internal flag to true again.
        """

    @overload
    def wait(self, timeout: None = None) -> Literal[True]:
        """Event.wait(self, timeout=None)

        Block until this object is :meth:`ready`.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread (greenlet) calls :meth:`set` to set the flag to true,
        or until the optional *timeout* expires.

        When the *timeout* argument is present and not ``None``, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        :return: This method returns true if and only if the internal flag has been set to
            true, either before the wait call or after the wait starts, so it will
            always return ``True`` except if a timeout is given and the operation
            times out.

        .. versionchanged:: 1.1
            The return value represents the flag during the elapsed wait, not
            just after it elapses. This solves a race condition if one greenlet
            sets and then clears the flag without switching, while other greenlets
            are waiting. When the waiters wake up, this will return True; previously,
            they would still wake up, but the return value would be False. This is most
            noticeable when the *timeout* is present.
        """

    @overload
    def wait(self, timeout: float) -> bool: ...

class AsyncResult(AbstractLinkable, Generic[_T]):
    """AsyncResult()

    A one-time event that stores a value or an exception.

    Like :class:`Event` it wakes up all the waiters when :meth:`set`
    or :meth:`set_exception` is called. Waiters may receive the passed
    value or exception by calling :meth:`get` instead of :meth:`wait`.
    An :class:`AsyncResult` instance cannot be reset.

    .. important::
       This object is for communicating among greenlets within the
       same thread *only*! Do not try to use it to communicate across threads.

    To pass a value call :meth:`set`. Calls to :meth:`get` (those that
    are currently blocking as well as those made in the future) will
    return the value::

        >>> from gevent.event import AsyncResult
        >>> result = AsyncResult()
        >>> result.set(100)
        >>> result.get()
        100

    To pass an exception call :meth:`set_exception`. This will cause
    :meth:`get` to raise that exception::

        >>> result = AsyncResult()
        >>> result.set_exception(RuntimeError('failure'))
        >>> result.get()
        Traceback (most recent call last):
         ...
        RuntimeError: failure

    :class:`AsyncResult` implements :meth:`__call__` and thus can be
    used as :meth:`link` target::

        >>> import gevent
        >>> result = AsyncResult()
        >>> gevent.spawn(lambda : 1/0).link(result)
        >>> try:
        ...     result.get()
        ... except ZeroDivisionError:
        ...     print('ZeroDivisionError')
        ZeroDivisionError

    .. note::

        The order and timing in which waiting greenlets are awakened is not determined.
        As an implementation note, in gevent 1.1 and 1.0, waiting greenlets are awakened in a
        undetermined order sometime *after* the current greenlet yields to the event loop. Other greenlets
        (those not waiting to be awakened) may run between the current greenlet yielding and
        the waiting greenlets being awakened. These details may change in the future.

    .. versionchanged:: 1.1

       The exact order in which waiting greenlets
       are awakened is not the same as in 1.0.

    .. versionchanged:: 1.1

       Callbacks :meth:`linked <rawlink>` to this object are required to
       be hashable, and duplicates are merged.

    .. versionchanged:: 1.5a3

       Waiting greenlets are now awakened in the order in which they
       waited.

    .. versionchanged:: 1.5a3

       The low-level ``rawlink`` method
       (most users won't use this) now automatically unlinks waiters
       before calling them.
    """

    def __init__(self) -> None: ...
    @property
    def value(self) -> _T | None:
        """
        Holds the value passed to :meth:`set` if :meth:`set` was called. Otherwise,
        ``None``
        """

    @property
    def exc_info(self) -> _OptExcInfo | tuple[None, None, None] | tuple[()]:
        """
        The three-tuple of exception information if :meth:`set_exception` was called.
        """

    @property
    def exception(self) -> BaseException | None:
        """Holds the exception instance passed to :meth:`set_exception` if :meth:`set_exception` was called.
        Otherwise ``None``.
        """

    def ready(self) -> bool:
        """AsyncResult.ready(self) -> bool
        Return true if and only if it holds a value or an exception
        """

    def successful(self) -> bool:
        """AsyncResult.successful(self) -> bool
        Return true if and only if it is ready and holds a value
        """

    def set(self, value: _T | None = None) -> None:
        """AsyncResult.set(self, value=None)
        Store the value and wake up any waiters.

                All greenlets blocking on :meth:`get` or :meth:`wait` are awakened.
                Subsequent calls to :meth:`wait` and :meth:`get` will not block at all.
        """

    @overload
    def set_exception(self, exception: BaseException, exc_info: None = None) -> None:
        """AsyncResult.set_exception(self, exception, exc_info=None)
        Store the exception and wake up any waiters.

                All greenlets blocking on :meth:`get` or :meth:`wait` are awakened.
                Subsequent calls to :meth:`wait` and :meth:`get` will not block at all.

                :keyword tuple exc_info: If given, a standard three-tuple of type, value, :class:`traceback`
                    as returned by :func:`sys.exc_info`. This will be used when the exception
                    is re-raised to propagate the correct traceback.
        """

    @overload
    def set_exception(self, exception: BaseException | None, exc_info: _OptExcInfo) -> None: ...
    # technically get/get_nowait/result should just return _T, but the API is designed in
    # such a way that it is perfectly legal for a ValueSource to have neither its value nor
    # its exception set, while still being marked successful, at which point None would be
    # stored into value, it's also legal to call set without arguments, which has the same
    # effect, this is a little annoying, since it will introduce some additional None checks
    # that may not be necessary, but it's impossible to annotate this situation, so for now
    # we just deal with the possibly redundant None checks...
    def get(self, block: bool = True, timeout: float | None = None) -> _T | None:
        """AsyncResult.get(self, block=True, timeout=None)
        Return the stored value or raise the exception.

                If this instance already holds a value or an exception, return  or raise it immediately.
                Otherwise, block until another greenlet calls :meth:`set` or :meth:`set_exception` or
                until the optional timeout occurs.

                When the *timeout* argument is present and not ``None``, it should be a
                floating point number specifying a timeout for the operation in seconds
                (or fractions thereof). If the *timeout* elapses, the *Timeout* exception will
                be raised.

                :keyword bool block: If set to ``False`` and this instance is not ready,
                    immediately raise a :class:`Timeout` exception.
        """

    def get_nowait(self) -> _T | None:
        """AsyncResult.get_nowait(self)

        Return the value or raise the exception without blocking.

        If this object is not yet :meth:`ready <ready>`, raise
        :class:`gevent.Timeout` immediately.
        """

    def wait(self, timeout: float | None = None) -> _T | None:
        """AsyncResult.wait(self, timeout=None)
        Block until the instance is ready.

                If this instance already holds a value, it is returned immediately. If this
                instance already holds an exception, ``None`` is returned immediately.

                Otherwise, block until another greenlet calls :meth:`set` or :meth:`set_exception`
                (at which point either the value or ``None`` will be returned, respectively),
                or until the optional timeout expires (at which point ``None`` will also be
                returned).

                When the *timeout* argument is present and not ``None``, it should be a
                floating point number specifying a timeout for the operation in seconds
                (or fractions thereof).

                .. note:: If a timeout is given and expires, ``None`` will be returned
                    (no timeout exception will be raised).

        """

    def __call__(self, source: _ValueSource[_T]) -> None:
        """Call self as a function."""

    def result(self, timeout: float | None = None) -> _T | None:
        """AsyncResult.result(self, timeout=None)"""
    set_result = set
    def done(self) -> bool:
        """AsyncResult.done(self) -> bool"""

    def cancel(self) -> Literal[False]:
        """AsyncResult.cancel(self) -> bool"""

    def cancelled(self) -> Literal[False]:
        """AsyncResult.cancelled(self) -> bool"""

__all__ = ["Event", "AsyncResult"]
