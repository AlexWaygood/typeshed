"""
Event-loop hub.
"""

from collections.abc import Callable
from types import TracebackType
from typing import Any, Generic, Protocol, TextIO, TypeVar, overload
from typing_extensions import ParamSpec

import gevent._hub_local
import gevent._waiter
import greenlet
from gevent._hub_primitives import WaitOperationsGreenlet
from gevent._ident import IdentRegistry
from gevent._monitor import PeriodicMonitoringThread
from gevent._types import _Loop, _Watcher
from gevent._util import Lazy, readproperty
from gevent.greenlet import Greenlet
from gevent.resolver import AbstractResolver
from gevent.threadpool import ThreadPool

_T = TypeVar("_T")
_P = ParamSpec("_P")

GreenletExit = greenlet.GreenletExit
getcurrent = greenlet.getcurrent
get_hub = gevent._hub_local.get_hub
Waiter = gevent._waiter.Waiter

class _DefaultReturnProperty(Protocol[_T]):
    @overload
    def __get__(self, obj: None, owner: type[object] | None = None) -> property: ...
    @overload
    def __get__(self, obj: object, owner: type[object] | None = None) -> _T: ...
    def __set__(self, obj: object, value: _T | None) -> None: ...
    def __del__(self) -> None: ...

def spawn_raw(function: Callable[..., object], *args: object, **kwargs: object) -> greenlet.greenlet:
    """
    Create a new :class:`greenlet.greenlet` object and schedule it to
    run ``function(*args, **kwargs)``.

    This returns a raw :class:`~greenlet.greenlet` which does not have all the useful
    methods that :class:`gevent.Greenlet` has. Typically, applications
    should prefer :func:`~gevent.spawn`, but this method may
    occasionally be useful as an optimization if there are many
    greenlets involved.

    .. versionchanged:: 1.1a3
        Verify that ``function`` is callable, raising a TypeError if not. Previously,
        the spawned greenlet would have failed the first time it was switched to.

    .. versionchanged:: 1.1b1
       If *function* is not callable, immediately raise a :exc:`TypeError`
       instead of spawning a greenlet that will raise an uncaught TypeError.

    .. versionchanged:: 1.1rc2
        Accept keyword arguments for ``function`` as previously (incorrectly)
        documented. Note that this may incur an additional expense.

    .. versionchanged:: 1.3a2
       Populate the ``spawning_greenlet`` and ``spawn_tree_locals``
       attributes of the returned greenlet.

    .. versionchanged:: 1.3b1
       *Only* populate ``spawning_greenlet`` and ``spawn_tree_locals``
       if ``GEVENT_TRACK_GREENLET_TREE`` is enabled (the default). If not enabled,
       those attributes will not be set.

    .. versionchanged:: 1.5a3
       The returned greenlet always has a *loop* attribute matching the
       current hub's loop. This helps it work better with more gevent APIs.
    """

def sleep(seconds: float = 0, ref: bool = True) -> None:
    """
    Put the current greenlet to sleep for at least *seconds*.

    *seconds* may be specified as an integer, or a float if fractional
    seconds are desired.

    .. tip:: In the current implementation, a value of 0 (the default)
       means to yield execution to any other runnable greenlets, but
       this greenlet may be scheduled again before the event loop
       cycles (in an extreme case, a greenlet that repeatedly sleeps
       with 0 can prevent greenlets that are ready to do I/O from
       being scheduled for some (small) period of time); a value greater than
       0, on the other hand, will delay running this greenlet until
       the next iteration of the loop.

    If *ref* is False, the greenlet running ``sleep()`` will not prevent :func:`gevent.wait`
    from exiting.

    .. versionchanged:: 1.3a1
       Sleeping with a value of 0 will now be bounded to approximately block the
       loop for no longer than :func:`gevent.getswitchinterval`.

    .. seealso:: :func:`idle`
    """

def idle(priority: int = 0) -> None:
    """
    Cause the calling greenlet to wait until the event loop is idle.

    Idle is defined as having no other events of the same or higher
    *priority* pending. That is, as long as sockets, timeouts or even
    signals of the same or higher priority are being processed, the loop
    is not idle.

    .. seealso:: :func:`sleep`
    """

def kill(greenlet: greenlet.greenlet, exception: type[BaseException] | BaseException = ...) -> None:
    """
    Kill greenlet asynchronously. The current greenlet is not unscheduled.

    .. note::

        The method :meth:`Greenlet.kill` method does the same and
        more (and the same caveats listed there apply here). However, the MAIN
        greenlet - the one that exists initially - does not have a
        ``kill()`` method, and neither do any created with :func:`spawn_raw`,
        so you have to use this function.

    .. caution:: Use care when killing greenlets. If they are not prepared for
       exceptions, this could result in corrupted state.

    .. versionchanged:: 1.1a2
        If the ``greenlet`` has a :meth:`kill <Greenlet.kill>` method, calls it. This prevents a
        greenlet from being switched to for the first time after it's been
        killed but not yet executed.
    """

class signal(Generic[_P]):
    """
    signal_handler(signalnum, handler, *args, **kwargs) -> object

    Call the *handler* with the *args* and *kwargs* when the process
    receives the signal *signalnum*.

    The *handler* will be run in a new greenlet when the signal is
    delivered.

    This returns an object with the useful method ``cancel``, which,
    when called, will prevent future deliveries of *signalnum* from
    calling *handler*. It's best to keep the returned object alive
    until you call ``cancel``.

    .. note::

        This may not operate correctly with ``SIGCHLD`` if libev child
        watchers are used (as they are by default with
        `gevent.os.fork`). See :mod:`gevent.signal` for a more
        general purpose solution.

    .. versionchanged:: 1.2a1

        The ``handler`` argument is required to
        be callable at construction time.

    .. versionchanged:: 20.5.1
       The ``cancel`` method now properly cleans up all native resources,
       and drops references to all the arguments of this function.
    """

    greenlet_class: type[Greenlet[..., Any]] | None
    hub: Hub
    watcher: _Watcher
    handler: Callable[_P, object]
    # we can't use _P.args/_P.kwargs here because pyright will complain
    # mypy doesn't seem to mind though
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    def __init__(self, signalnum: int, handler: Callable[_P, object], *args: _P.args, **kwargs: _P.kwargs) -> None: ...
    @property
    def ref(self) -> bool: ...
    @ref.setter
    def ref(self, value: bool) -> None: ...
    def cancel(self) -> None: ...
    def handle(self) -> None: ...

def reinit(hub: Hub | None = None) -> None:
    """
    reinit() -> None

    Prepare the gevent hub to run in a new (forked) process.

    This should be called *immediately* after :func:`os.fork` in the
    child process. This is done automatically by
    :func:`gevent.os.fork` or if the :mod:`os` module has been
    monkey-patched. If this function is not called in a forked
    process, symptoms may include hanging of functions like
    :func:`socket.getaddrinfo`, and the hub's threadpool is unlikely
    to work.

    .. note:: Registered fork watchers may or may not run before
       this function (and thus ``gevent.os.fork``) return. If they have
       not run, they will run "soon", after an iteration of the event loop.
       You can force this by inserting a few small (but non-zero) calls to :func:`sleep`
       after fork returns. (As of gevent 1.1 and before, fork watchers will
       not have run, but this may change in the future.)

    .. note:: This function may be removed in a future major release
       if the fork process can be more smoothly managed.

    .. warning:: See remarks in :func:`gevent.os.fork` about greenlets
       and event loop watchers in the child process.
    """

class Hub(WaitOperationsGreenlet):
    """
    A greenlet that runs the event loop.

    It is created automatically by :func:`get_hub`.

    .. rubric:: Switching

    Every time this greenlet (i.e., the event loop) is switched *to*,
    if the current greenlet has a ``switch_out`` method, it will be
    called. This allows a greenlet to take some cleanup actions before
    yielding control. This method should not call any gevent blocking
    functions.
    """

    SYSTEM_ERROR: tuple[type[BaseException], ...]
    NOT_ERROR: tuple[type[BaseException], ...]
    threadpool_size: int
    periodic_monitoring_thread: PeriodicMonitoringThread | None
    thread_ident: int
    name: str
    loop: _Loop
    format_context: Callable[[object], str]
    minimal_ident: int
    @overload
    def __init__(self, loop: _Loop, default: None = None) -> None: ...
    @overload
    def __init__(self, loop: None = None, default: bool | None = None) -> None: ...
    @Lazy
    def ident_registry(self) -> IdentRegistry: ...
    @property
    def loop_class(self) -> type[_Loop]: ...
    @property
    def backend(self) -> int | str: ...
    @property
    def main_hub(self) -> bool:
        """
        Is this the hub for the main thread?

        .. versionadded:: 1.3b1
        """

    def handle_error(
        self,
        context: object | None,
        type: type[BaseException] | None,
        value: BaseException | str | None,
        tb: TracebackType | None,
    ) -> None:
        """
        Called by the event loop when an error occurs. The default
        action is to print the exception to the :attr:`exception
        stream <exception_stream>`.

        The arguments ``type``, ``value``, and ``tb`` are the standard
        tuple as returned by :func:`sys.exc_info`. (Note that when
        this is called, it may not be safe to call
        :func:`sys.exc_info`.)

        Errors that are :attr:`not errors <NOT_ERROR>` are not
        printed.

        Errors that are :attr:`system errors <SYSTEM_ERROR>` are
        passed to :meth:`handle_system_error` after being printed.

        Applications can set a property on the hub instance with this
        same signature to override the error handling provided by this
        class. This is an advanced usage and requires great care. This
        function *must not* raise any exceptions.

        :param context: If this is ``None``, indicates a system error
            that should generally result in exiting the loop and being
            thrown to the parent greenlet.
        """

    def handle_system_error(
        self, type: type[BaseException], value: BaseException | None, tb: TracebackType | None = None
    ) -> None:
        """
        Called from `handle_error` when the exception type is determined
        to be a :attr:`system error <SYSTEM_ERROR>`.

        System errors cause the exception to be raised in the main
        greenlet (the parent of this hub).

        .. versionchanged:: 20.5.1
           Allow passing the traceback to associate with the
           exception if it is rethrown into the main greenlet.
        """

    @readproperty
    def exception_stream(self) -> TextIO | None:
        """
        The stream to which exceptions will be written.
        Defaults to ``sys.stderr`` unless assigned. Assigning a
        false (None) value disables printing exceptions.

        .. versionadded:: 1.2a1
        """

    def print_exception(
        self, context: object | None, t: type[BaseException] | None, v: BaseException | str | None, tb: TracebackType | None
    ) -> None: ...
    def run(self) -> None:
        """
        Entry-point to running the loop. This method is called automatically
        when the hub greenlet is scheduled; do not call it directly.

        :raises gevent.exceptions.LoopExit: If the loop finishes running. This means
           that there are no other scheduled greenlets, and no active
           watchers or servers. In some situations, this indicates a
           programming error.
        """

    def start_periodic_monitoring_thread(self) -> PeriodicMonitoringThread: ...
    def join(self, timeout: float | None = None) -> bool:
        """
        Wait for the event loop to finish. Exits only when there
        are no more spawned greenlets, started servers, active
        timeouts or watchers.

        .. caution:: This doesn't clean up all resources associated
           with the hub. For that, see :meth:`destroy`.

        :param float timeout: If *timeout* is provided, wait no longer
            than the specified number of seconds.

        :return: `True` if this method returns because the loop
                 finished execution. Or `False` if the timeout
                 expired.
        """

    def destroy(self, destroy_loop: bool | None = None) -> None:
        """
        Destroy this hub and clean up its resources.

        If you manually create hubs, or you use a hub or the gevent
        blocking API from multiple native threads, you *should* call this
        method before disposing of the hub object reference. Ideally,
        this should be called from the same thread running the hub, but
        it can be called from other threads after that thread has exited.

        Once this is done, it is impossible to continue running the
        hub. Attempts to use the blocking gevent API with pre-existing
        objects from this native thread and bound to this hub will fail.

        .. versionchanged:: 20.5.1
            Attempt to ensure that Python stack frames and greenlets referenced by this
            hub are cleaned up. This guarantees that switching to the hub again
            is not safe after this. (It was never safe, but it's even less safe.)

            Note that this only works if the hub is destroyed in the same thread it
            is running in. If the hub is destroyed by a different thread
            after a ``fork()``, for example, expect some garbage to leak.
        """

    @property
    def resolver_class(self) -> type[AbstractResolver]: ...
    resolver: _DefaultReturnProperty[AbstractResolver]
    @property
    def threadpool_class(self) -> type[ThreadPool]: ...
    threadpool: _DefaultReturnProperty[ThreadPool]

class linkproxy:
    callback: Callable[[object], object]
    obj: object
    def __init__(self, callback: Callable[[_T], object], obj: _T) -> None: ...
    def __call__(self, *args: object) -> None: ...

__all__ = ["getcurrent", "GreenletExit", "spawn_raw", "sleep", "kill", "signal", "reinit", "get_hub", "Hub", "Waiter"]
