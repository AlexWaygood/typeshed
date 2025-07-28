"""
Low-level waiting primitives.

"""

from types import TracebackType
from typing import Generic, TypeVar, final, overload
from typing_extensions import TypeAlias

from gevent.event import _ValueSource
from gevent.hub import Hub
from greenlet import greenlet as greenlet_t

__all__ = ["Waiter"]

_T = TypeVar("_T")
# this is annoying, it's due to them using *throw args, rather than just storing them in standardized form
_ThrowArgs: TypeAlias = (
    tuple[()]
    | tuple[BaseException]
    | tuple[BaseException, None]
    | tuple[BaseException, None, TracebackType | None]
    | tuple[type[BaseException]]
    | tuple[type[BaseException], BaseException | object]
    | tuple[type[BaseException], BaseException | object, TracebackType | None]
)

class Waiter(Generic[_T]):
    """Waiter(hub=None)

    A low level communication utility for greenlets.

    Waiter is a wrapper around greenlet's ``switch()`` and ``throw()`` calls that makes them somewhat safer:

    * switching will occur only if the waiting greenlet is executing :meth:`get` method currently;
    * any error raised in the greenlet is handled inside :meth:`switch` and :meth:`throw`
    * if :meth:`switch`/:meth:`throw` is called before the receiver calls :meth:`get`, then :class:`Waiter`
      will store the value/exception. The following :meth:`get` will return the value/raise the exception.

    The :meth:`switch` and :meth:`throw` methods must only be called from the :class:`Hub` greenlet.
    The :meth:`get` method must be called from a greenlet other than :class:`Hub`.

        >>> from gevent.hub import Waiter
        >>> from gevent import get_hub
        >>> result = Waiter()
        >>> timer = get_hub().loop.timer(0.1)
        >>> timer.start(result.switch, 'hello from Waiter')
        >>> result.get() # blocks for 0.1 seconds
        'hello from Waiter'
        >>> timer.close()

    If switch is called before the greenlet gets a chance to call :meth:`get` then
    :class:`Waiter` stores the value.

        >>> from gevent.time import sleep
        >>> result = Waiter()
        >>> timer = get_hub().loop.timer(0.1)
        >>> timer.start(result.switch, 'hi from Waiter')
        >>> sleep(0.2)
        >>> result.get() # returns immediately without blocking
        'hi from Waiter'
        >>> timer.close()

    .. warning::

        This is a limited and dangerous way to communicate between
        greenlets. It can easily leave a greenlet unscheduled forever
        if used incorrectly. Consider using safer classes such as
        :class:`gevent.event.Event`, :class:`gevent.event.AsyncResult`,
        or :class:`gevent.queue.Queue`.
    """

    @property
    def hub(self) -> Hub: ...  # readonly in Cython
    @property
    def greenlet(self) -> greenlet_t | None: ...  # readonly in Cython
    @property
    def value(self) -> _T | None: ...  # readonly in Cython
    def __init__(self, hub: Hub | None = None) -> None: ...
    def clear(self) -> None:
        """Waiter.clear(self)"""

    def ready(self) -> bool:
        """Waiter.ready(self)
        Return true if and only if it holds a value or an exception
        """

    def successful(self) -> bool:
        """Waiter.successful(self)
        Return true if and only if it is ready and holds a value
        """

    @property
    def exc_info(self) -> _ThrowArgs | None:
        """Holds the exception info passed to :meth:`throw` if :meth:`throw` was called. Otherwise ``None``."""

    def switch(self, value: _T) -> None:
        """Waiter.switch(self, value)

        Switch to the greenlet if one's available. Otherwise store the
        *value*.

        .. versionchanged:: 1.3b1
           The *value* is no longer optional.
        """

    @overload
    def throw(self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /) -> None:
        """Waiter.throw(self, *throw_args)
        Switch to the greenlet with the exception. If there's no greenlet, store the exception.
        """

    @overload
    def throw(self, typ: BaseException = ..., val: None = None, tb: TracebackType | None = None, /) -> None: ...
    def get(self) -> _T:
        """Waiter.get(self)
        If a value/an exception is stored, return/raise it. Otherwise until switch() or throw() is called.
        """

    def __call__(self, source: _ValueSource[_T]) -> None:
        """Call self as a function."""

@final
class MultipleWaiter(Waiter[_T]):
    """MultipleWaiter(hub=None)

    An internal extension of Waiter that can be used if multiple objects
    must be waited on, and there is a chance that in between waits greenlets
    might be switched out. All greenlets that switch to this waiter
    will have their value returned.

    This does not handle exceptions or throw methods.
    """
