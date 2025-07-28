"""
A collection of primitives used by the hub, and suitable for
compilation with Cython because of their frequency of use.


"""

from _typeshed import FileDescriptor
from collections.abc import Callable, Collection, Iterable
from types import TracebackType
from typing import Any, Generic, Protocol, TypeVar, overload
from typing_extensions import Self, TypeVarTuple, Unpack

from gevent._greenlet_primitives import SwitchOutGreenletWithLoop
from gevent._types import _Loop, _Watcher
from gevent.hub import Hub
from gevent.socket import socket

__all__ = ["WaitOperationsGreenlet", "iwait_on_objects", "wait_on_objects", "wait_read", "wait_write", "wait_readwrite"]

_T = TypeVar("_T")
_Ts = TypeVarTuple("_Ts")
_WaitableT = TypeVar("_WaitableT", bound=_Waitable)

class _Waitable(Protocol):
    def rawlink(self, callback: Callable[[Any], object], /) -> object: ...
    def unlink(self, callback: Callable[[Any], object], /) -> object: ...

class WaitOperationsGreenlet(SwitchOutGreenletWithLoop):
    loop: _Loop
    def wait(self, watcher: _Watcher) -> None:
        """WaitOperationsGreenlet.wait(self, watcher)

        Wait until the *watcher* (which must not be started) is ready.

        The current greenlet will be unscheduled during this time.
        """

    def cancel_waits_close_and_then(
        self,
        watchers: Iterable[_Watcher],
        exc_kind: type[BaseException] | BaseException,
        then: Callable[[Unpack[_Ts]], object],
        *then_args: Unpack[_Ts],
    ) -> None:
        """WaitOperationsGreenlet.cancel_waits_close_and_then(self, watchers, exc_kind, then, *then_args)"""

    def cancel_wait(self, watcher: _Watcher, error: type[BaseException] | BaseException, close_watcher: bool = False) -> None:
        """WaitOperationsGreenlet.cancel_wait(self, watcher, error, close_watcher=False)

        Cancel an in-progress call to :meth:`wait` by throwing the given *error*
        in the waiting greenlet.

        .. versionchanged:: 1.3a1
           Added the *close_watcher* parameter. If true, the watcher
           will be closed after the exception is thrown. The watcher should then
           be discarded. Closing the watcher is important to release native resources.
        .. versionchanged:: 1.3a2
           Allow the *watcher* to be ``None``. No action is taken in that case.

        """

class _WaitIterator(Generic[_T]):
    """_WaitIterator(objects, hub, timeout, count)"""

    def __init__(self, objects: Collection[_T], hub: Hub, timeout: float, count: None | int) -> None: ...
    def __enter__(self) -> Self:
        """_WaitIterator.__enter__(self)"""

    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None) -> None:
        """_WaitIterator.__exit__(self, typ, value, tb)"""

    def __iter__(self) -> Self:
        """Implement iter(self)."""

    def __next__(self) -> _T: ...
    next = __next__

@overload
def iwait_on_objects(objects: None, timeout: float | None = None, count: int | None = None) -> list[bool]:
    """iwait_on_objects(objects, timeout=None, count=None)

    Iteratively yield *objects* as they are ready, until all (or *count*) are ready
    or *timeout* expired.

    If you will only be consuming a portion of the *objects*, you should
    do so inside a ``with`` block on this object to avoid leaking resources::

        with gevent.iwait((a, b, c)) as it:
            for i in it:
                if i is a:
                    break

    :param objects: A sequence (supporting :func:`len`) containing objects
        implementing the wait protocol (rawlink() and unlink()).
    :keyword int count: If not `None`, then a number specifying the maximum number
        of objects to wait for. If ``None`` (the default), all objects
        are waited for.
    :keyword float timeout: If given, specifies a maximum number of seconds
        to wait. If the timeout expires before the desired waited-for objects
        are available, then this method returns immediately.

    .. seealso:: :func:`wait`

    .. versionchanged:: 1.1a1
       Add the *count* parameter.
    .. versionchanged:: 1.1a2
       No longer raise :exc:`LoopExit` if our caller switches greenlets
       in between items yielded by this function.
    .. versionchanged:: 1.4
       Add support to use the returned object as a context manager.
    """

@overload
def iwait_on_objects(
    objects: Collection[_WaitableT], timeout: float | None = None, count: int | None = None
) -> _WaitIterator[_WaitableT]: ...
@overload
def wait_on_objects(objects: None = None, timeout: float | None = None, count: int | None = None) -> bool:
    """wait_on_objects(objects=None, timeout=None, count=None)

    Wait for *objects* to become ready or for event loop to finish.

    If *objects* is provided, it must be a list containing objects
    implementing the wait protocol (rawlink() and unlink() methods):

    - :class:`gevent.Greenlet` instance
    - :class:`gevent.event.Event` instance
    - :class:`gevent.lock.Semaphore` instance
    - :class:`gevent.subprocess.Popen` instance

    If *objects* is ``None`` (the default), ``wait()`` blocks until
    the current event loop has nothing to do (or until *timeout* passes):

    - all greenlets have finished
    - all servers were stopped
    - all event loop watchers were stopped.

    If *count* is ``None`` (the default), wait for all *objects*
    to become ready.

    If *count* is a number, wait for (up to) *count* objects to become
    ready. (For example, if count is ``1`` then the function exits
    when any object in the list is ready).

    If *timeout* is provided, it specifies the maximum number of
    seconds ``wait()`` will block.

    Returns the list of ready objects, in the order in which they were
    ready.

    .. seealso:: :func:`iwait`
    """

@overload
def wait_on_objects(
    objects: Collection[_WaitableT], timeout: float | None = None, count: int | None = None
) -> list[_WaitableT]: ...
def set_default_timeout_error(e: type[BaseException]) -> None:
    """set_default_timeout_error(e)"""

def wait_on_socket(socket: socket, watcher: _Watcher, timeout_exc: type[BaseException] | BaseException | None = None) -> None:
    """wait_on_socket(socket, watcher, timeout_exc=None)"""

def wait_on_watcher(
    watcher: _Watcher,
    timeout: float | None = None,
    timeout_exc: type[BaseException] | BaseException = ...,
    hub: Hub | None = None,
) -> None:
    """wait_on_watcher(watcher, timeout=None, timeout_exc=_NONE, WaitOperationsGreenlet hub=None)

    wait(watcher, timeout=None, [timeout_exc=None]) -> None

    Block the current greenlet until *watcher* is ready.

    If *timeout* is non-negative, then *timeout_exc* is raised after
    *timeout* second has passed.

    If :func:`cancel_wait` is called on *watcher* by another greenlet,
    raise an exception in this blocking greenlet
    (``socket.error(EBADF, 'File descriptor was closed in another
    greenlet')`` by default).

    :param watcher: An event loop watcher, most commonly an IO watcher obtained from
        :meth:`gevent.core.loop.io`
    :keyword timeout_exc: The exception to raise if the timeout expires.
        By default, a :class:`socket.timeout` exception is raised.
        If you pass a value for this keyword, it is interpreted as for
        :class:`gevent.timeout.Timeout`.

    :raises ~gevent.hub.ConcurrentObjectUseError: If the *watcher* is
        already started.
    """

def wait_read(
    fileno: FileDescriptor, timeout: float | None = None, timeout_exc: type[BaseException] | BaseException = ...
) -> None:
    """wait_read(fileno, timeout=None, timeout_exc=_NONE)

    wait_read(fileno, timeout=None, [timeout_exc=None]) -> None

    Block the current greenlet until *fileno* is ready to read.

    For the meaning of the other parameters and possible exceptions,
    see :func:`wait`.

    .. seealso:: :func:`cancel_wait`
    """

def wait_write(
    fileno: FileDescriptor, timeout: float | None = None, timeout_exc: type[BaseException] | BaseException = ...
) -> None:
    """wait_write(fileno, timeout=None, timeout_exc=_NONE, event=_NONE)

    wait_write(fileno, timeout=None, [timeout_exc=None]) -> None

    Block the current greenlet until *fileno* is ready to write.

    For the meaning of the other parameters and possible exceptions,
    see :func:`wait`.

    .. deprecated:: 1.1
       The keyword argument *event* is ignored. Applications should not pass this parameter.
       In the future, doing so will become an error.

    .. seealso:: :func:`cancel_wait`
    """

def wait_readwrite(
    fileno: FileDescriptor, timeout: float | None = None, timeout_exc: type[BaseException] | BaseException = ...
) -> None:
    """wait_readwrite(fileno, timeout=None, timeout_exc=_NONE, event=_NONE)

    wait_readwrite(fileno, timeout=None, [timeout_exc=None]) -> None

    Block the current greenlet until *fileno* is ready to read or
    write.

    For the meaning of the other parameters and possible exceptions,
    see :func:`wait`.

    .. deprecated:: 1.1
       The keyword argument *event* is ignored. Applications should not pass this parameter.
       In the future, doing so will become an error.

    .. seealso:: :func:`cancel_wait`
    """
