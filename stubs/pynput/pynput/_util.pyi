"""
General utility functions and classes.
"""

import threading
from _typeshed import OptExcInfo
from collections.abc import Callable
from queue import Queue
from types import ModuleType, TracebackType
from typing import Any, ClassVar, Generic, TypedDict, TypeVar
from typing_extensions import ParamSpec, Self

_T = TypeVar("_T")
_AbstractListenerT = TypeVar("_AbstractListenerT", bound=AbstractListener)
_P = ParamSpec("_P")

class _RESOLUTIONS(TypedDict):
    darwin: str
    uinput: str
    xorg: str

RESOLUTIONS: _RESOLUTIONS

def backend(package: str) -> ModuleType:
    """Returns the backend module for a package.

    :param str package: The package for which to load a backend.
    """

def prefix(base: type | tuple[type | tuple[Any, ...], ...], cls: type) -> str | None:
    """Calculates the prefix to use for platform specific options for a
    specific class.

    The prefix if the name of the module containing the class that is an
    immediate subclass of ``base`` among the super classes of ``cls``.
    """

class AbstractListener(threading.Thread):
    """A class implementing the basic behaviour for event listeners.

    Instances of this class can be used as context managers. This is equivalent
    to the following code::

        listener.start()
        listener.wait()
        try:
            with_statements()
        finally:
            listener.stop()

    Actual implementations of this class must set the attribute ``_log``, which
    must be an instance of :class:`logging.Logger`.

    :param bool suppress: Whether to suppress events. Setting this to ``True``
        will prevent the input events from being passed to the rest of the
        system.

    :param kwargs: A mapping from callback attribute to callback handler. All
        handlers will be wrapped in a function reading the return value of the
        callback, and if it ``is False``, raising :class:`StopException`.

        Any callback that is falsy will be ignored.
    """

    class StopException(Exception):
        """If an event listener callback raises this exception, the current
        listener is stopped.
        """

    _HANDLED_EXCEPTIONS: ClassVar[tuple[type | tuple[Any, ...], ...]]  # undocumented
    _suppress: bool  # undocumented
    _running: bool  # undocumented
    _thread: threading.Thread  # undocumented
    _condition: threading.Condition  # undocumented
    _ready: bool  # undocumented
    _queue: Queue[OptExcInfo | None]  # undocumented
    daemon: bool
    def __init__(self, suppress: bool = False, **kwargs: Callable[..., bool | None] | None) -> None: ...
    @property
    def suppress(self) -> bool:
        """Whether to suppress events."""

    @property
    def running(self) -> bool:
        """Whether the listener is currently running."""

    def stop(self) -> None:
        """Stops listening for events.

        When this method returns, no more events will be delivered. Once this
        method has been called, the listener instance cannot be used any more,
        since a listener is a :class:`threading.Thread`, and once stopped it
        cannot be restarted.

        To resume listening for event, a new listener must be created.
        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def wait(self) -> None:
        """Waits for this listener to become ready."""

    def run(self) -> None:
        """The thread runner method."""

    @classmethod
    def _emitter(cls, f: Callable[_P, _T]) -> Callable[_P, _T]:  # undocumented
        """A decorator to mark a method as the one emitting the callbacks.

        This decorator will wrap the method and catch exception. If a
        :class:`StopException` is caught, the listener will be stopped
        gracefully. If any other exception is caught, it will be propagated to
        the thread calling :meth:`join` and reraised there.
        """

    def _mark_ready(self) -> None:  # undocumented
        """Marks this listener as ready to receive events.

        This method must be called from :meth:`_run`. :meth:`wait` will block
        until this method is called.
        """

    def _run(self) -> None:  # undocumented
        """The implementation of the :meth:`run` method.

        This is a platform dependent implementation.
        """

    def _stop_platform(self) -> None:  # undocumented
        """The implementation of the :meth:`stop` method.

        This is a platform dependent implementation.
        """

    def join(self, timeout: float | None = None, *args: Any) -> None: ...

class Events(Generic[_T, _AbstractListenerT]):
    """A base class to enable iterating over events."""

    _Listener: type[_AbstractListenerT] | None  # undocumented

    class Event:
        def __eq__(self, other: object) -> bool: ...

    _event_queue: Queue[_T]  # undocumented
    _sentinel: object  # undocumented
    _listener: _AbstractListenerT  # undocumented
    start: Callable[[], None]
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> _T: ...
    def get(self, timeout: float | None = None) -> _T | None:
        """Attempts to read the next event.

        :param int timeout: An optional timeout. If this is not provided, this
            method may block infinitely.

        :return: the next event, or ``None`` if the source has been stopped or
            no events were received
        """

    def _event_mapper(self, event: Callable[_P, object]) -> Callable[_P, None]:
        """Generates an event callback to transforms the callback arguments to
        an event and then publishes it.

        :param callback event: A function generating an event object.

        :return: a callback
        """

class NotifierMixin:
    """A mixin for notifiers of fake events.

    This mixin can be used for controllers on platforms where sending fake
    events does not cause a listener to receive a notification.
    """
