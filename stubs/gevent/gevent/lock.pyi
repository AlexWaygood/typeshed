"""
Locking primitives.

These include semaphores with arbitrary bounds (:class:`Semaphore` and
its safer subclass :class:`BoundedSemaphore`) and a semaphore with
infinite bounds (:class:`DummySemaphore`), along with a reentrant lock
(:class:`RLock`) with the same API as :class:`threading.RLock`.
"""

from collections.abc import Callable
from types import TracebackType
from typing import Any, Literal

from gevent._abstract_linkable import AbstractLinkable
from gevent.hub import Hub

__all__ = ["Semaphore", "BoundedSemaphore", "DummySemaphore", "RLock"]

class Semaphore(AbstractLinkable):
    """Semaphore(value=1, hub=None)

    Semaphore(value=1) -> Semaphore

    .. seealso:: :class:`BoundedSemaphore` for a safer version that prevents
       some classes of bugs. If unsure, most users should opt for `BoundedSemaphore`.

    A semaphore manages a counter representing the number of `release`
    calls minus the number of `acquire` calls, plus an initial value.
    The `acquire` method blocks if necessary until it can return
    without making the counter negative. A semaphore does not track ownership
    by greenlets; any greenlet can call `release`, whether or not it has previously
    called `acquire`.

    If not given, ``value`` defaults to 1.

    The semaphore is a context manager and can be used in ``with`` statements.

    This Semaphore's ``__exit__`` method does not call the trace function
    on CPython, but does under PyPy.

    .. versionchanged:: 1.4.0
        Document that the order in which waiters are awakened is not specified. It was not
        specified previously, but due to CPython implementation quirks usually went in FIFO order.
    .. versionchanged:: 1.5a3
       Waiting greenlets are now awakened in the order in which they waited.
    .. versionchanged:: 1.5a3
       The low-level ``rawlink`` method (most users won't use this) now automatically
       unlinks waiters before calling them.
    .. versionchanged:: 20.12.0
       Improved support for multi-threaded usage. When multi-threaded usage is detected,
       instances will no longer create the thread's hub if it's not present.

    .. versionchanged:: 24.2.1
       Uses Python 3 native lock timeouts for cross-thread operations instead
       of spinning.
    """

    counter: int
    def __init__(self, value: int = 1, hub: Hub | None = None) -> None: ...
    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        """Semaphore.acquire(self, bool blocking=True, timeout=None) -> bool

        acquire(blocking=True, timeout=None) -> bool

        Acquire the semaphore.

        .. note:: If this semaphore was initialized with a *value* of 0,
           this method will block forever (unless a timeout is given or blocking is
           set to false).

        :keyword bool blocking: If True (the default), this function will block
           until the semaphore is acquired.
        :keyword float timeout: If given, and *blocking* is true,
           specifies the maximum amount of seconds
           this method will block.
        :return: A `bool` indicating whether the semaphore was acquired.
           If ``blocking`` is True and ``timeout`` is None (the default), then
           (so long as this semaphore was initialized with a size greater than 0)
           this will always return True. If a timeout was given, and it expired before
           the semaphore was acquired, False will be returned. (Note that this can still
           raise a ``Timeout`` exception, if some other caller had already started a timer.)
        """

    def locked(self) -> bool:
        """Semaphore.locked(self) -> bool

        Return a boolean indicating whether the semaphore can be
        acquired (`False` if the semaphore *can* be acquired). Most
        useful with binary semaphores (those with an initial value of 1).

        :rtype: bool
        """

    def ready(self) -> bool:
        """Semaphore.ready(self) -> bool

        Return a boolean indicating whether the semaphore can be
        acquired (`True` if the semaphore can be acquired).

        :rtype: bool
        """

    def release(self) -> int:
        """Semaphore.release(self) -> int

        Release the semaphore, notifying any waiters if needed. There
        is no return value.

        .. note::

            This can be used to over-release the semaphore.
            (Release more times than it has been acquired or was initially
            created with.)

            This is usually a sign of a bug, but under some circumstances it can be
            used deliberately, for example, to model the arrival of additional
            resources.

        :rtype: None
        """

    def wait(self, timeout: float | None = None) -> int:
        """Semaphore.wait(self, timeout=None) -> int

        Wait until it is possible to acquire this semaphore, or until the optional
        *timeout* elapses.

        .. note:: If this semaphore was initialized with a *value* of 0,
           this method will block forever if no timeout is given.

        :keyword float timeout: If given, specifies the maximum amount of seconds
           this method will block.
        :return: A number indicating how many times the semaphore can be acquired
            before blocking. *This could be 0,* if other waiters acquired
            the semaphore.
        :rtype: int
        """

    def __enter__(self) -> None:
        """Semaphore.__enter__(self)"""

    def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None:
        """Semaphore.__exit__(self, t, v, tb)"""

class BoundedSemaphore(Semaphore):
    """BoundedSemaphore(*args, **kwargs)

    BoundedSemaphore(value=1) -> BoundedSemaphore

    A bounded semaphore checks to make sure its current value doesn't
    exceed its initial value. If it does, :class:`ValueError` is
    raised. In most situations semaphores are used to guard resources
    with limited capacity. If the semaphore is released too many times
    it's a sign of a bug.

    If not given, *value* defaults to 1.
    """

class DummySemaphore:
    """
    DummySemaphore(value=None) -> DummySemaphore

    An object with the same API as :class:`Semaphore`,
    initialized with "infinite" initial value. None of its
    methods ever block.

    This can be used to parameterize on whether or not to actually
    guard access to a potentially limited resource. If the resource is
    actually limited, such as a fixed-size thread pool, use a real
    :class:`Semaphore`, but if the resource is unbounded, use an
    instance of this class. In that way none of the supporting code
    needs to change.

    Similarly, it can be used to parameterize on whether or not to
    enforce mutual exclusion to some underlying object. If the
    underlying object is known to be thread-safe itself mutual
    exclusion is not needed and a ``DummySemaphore`` can be used, but
    if that's not true, use a real ``Semaphore``.
    """

    def __init__(self, value: int | None = None) -> None:
        """
        .. versionchanged:: 1.1rc3
            Accept and ignore a *value* argument for compatibility with Semaphore.
        """

    def locked(self) -> Literal[False]:
        """A DummySemaphore is never locked so this always returns False."""

    def ready(self) -> Literal[True]:
        """A DummySemaphore is never locked so this always returns True."""

    def release(self) -> None:
        """Releasing a dummy semaphore does nothing."""

    def rawlink(self, callback: Callable[[Any], object]) -> None: ...
    def unlink(self, callback: Callable[[Any], object]) -> None: ...
    def wait(self, timeout: float | None = None) -> Literal[1]:
        """Waiting for a DummySemaphore returns immediately."""

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> Literal[True]:
        """
        A DummySemaphore can always be acquired immediately so this always
        returns True and ignores its arguments.

        .. versionchanged:: 1.1a1
           Always return *true*.
        """

    def __enter__(self) -> None: ...
    def __exit__(self, typ: type[BaseException] | None, val: BaseException | None, tb: TracebackType | None) -> None: ...

class RLock:
    """
    A mutex that can be acquired more than once by the same greenlet.

    A mutex can only be locked by one greenlet at a time. A single greenlet
    can `acquire` the mutex as many times as desired, though. Each call to
    `acquire` must be paired with a matching call to `release`.

    It is an error for a greenlet that has not acquired the mutex
    to release it.

    Instances are context managers.
    """

    def __init__(self, hub: Hub | None = None) -> None:
        """
        .. versionchanged:: 20.5.1
           Add the ``hub`` argument.
        """

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        """
        Acquire the mutex, blocking if *blocking* is true, for up to
        *timeout* seconds.

        .. versionchanged:: 1.5a4
           Added the *timeout* parameter.

        :return: A boolean indicating whether the mutex was acquired.
        """

    def __enter__(self) -> bool: ...
    def release(self) -> None:
        """
        Release the mutex.

        Only the greenlet that originally acquired the mutex can
        release it.
        """

    def __exit__(self, typ: type[BaseException] | None, val: BaseException | None, tb: TracebackType | None) -> None: ...
    def locked(self) -> bool:
        """
        Return a boolean indicating whether this object is locked right now.

        .. versionadded:: 25.4.1
        """
