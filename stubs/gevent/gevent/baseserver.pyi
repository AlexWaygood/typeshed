"""Base class for implementing servers"""

from collections.abc import Callable, Container
from types import TracebackType
from typing import Any, Generic, Literal, Protocol
from typing_extensions import ParamSpec, Self, TypeAlias

from gevent._types import _Loop
from gevent.pool import Pool
from gevent.socket import socket as _GeventSocket
from greenlet import greenlet

_P = ParamSpec("_P")

class _SpawnFunc(Protocol):
    def __call__(self, func: Callable[_P, object], /, *args: _P.args, **kwargs: _P.kwargs) -> greenlet: ...

_Spawner: TypeAlias = Pool | _SpawnFunc | int | Literal["default"] | None

class BaseServer(Generic[_P]):
    """
    An abstract base class that implements some common functionality for the servers in gevent.

    :param listener: Either be an address that the server should bind
        on or a :class:`gevent.socket.socket` instance that is already
        bound (and put into listening mode in case of TCP socket).

    :keyword handle: If given, the request handler. The request
        handler can be defined in a few ways. Most commonly,
        subclasses will implement a ``handle`` method as an
        instance method. Alternatively, a function can be passed
        as the ``handle`` argument to the constructor. In either
        case, the handler can later be changed by calling
        :meth:`set_handle`.

        When the request handler returns, the socket used for the
        request will be closed. Therefore, the handler must not return if
        the socket is still in use (for example, by manually spawned greenlets).

    :keyword spawn: If provided, is called to create a new
        greenlet to run the handler. By default,
        :func:`gevent.spawn` is used (meaning there is no
        artificial limit on the number of concurrent requests). Possible values for *spawn*:

        - a :class:`gevent.pool.Pool` instance -- ``handle`` will be executed
          using :meth:`gevent.pool.Pool.spawn` only if the pool is not full.
          While it is full, no new connections are accepted;
        - :func:`gevent.spawn_raw` -- ``handle`` will be executed in a raw
          greenlet which has a little less overhead then :class:`gevent.Greenlet` instances spawned by default;
        - ``None`` -- ``handle`` will be executed right away, in the :class:`Hub` greenlet.
          ``handle`` cannot use any blocking functions as it would mean switching to the :class:`Hub`.
        - an integer -- a shortcut for ``gevent.pool.Pool(integer)``

    .. versionchanged:: 1.1a1
       When the *handle* function returns from processing a connection,
       the client socket will be closed. This resolves the non-deterministic
       closing of the socket, fixing ResourceWarnings under Python 3 and PyPy.
    .. versionchanged:: 1.5
       Now a context manager that returns itself and calls :meth:`stop` on exit.

    """

    min_delay: float
    max_delay: float
    max_accept: int
    stop_timeout: float
    fatal_errors: Container[int]
    pool: Pool | None
    delay: float
    loop: _Loop
    family: int
    address: str | tuple[str, int]
    socket: _GeventSocket
    handle: Callable[..., object]
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        handle: Callable[_P, object] | None = None,
        spawn: _Spawner = "default",
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, tb: TracebackType | None, /) -> None: ...
    def set_listener(self, listener: _GeventSocket | tuple[str, int] | str) -> None: ...
    def set_spawn(self, spawn: _Spawner) -> None: ...
    def set_handle(self, handle: Callable[_P, object]) -> None: ...
    def start_accepting(self) -> None: ...
    def stop_accepting(self) -> None: ...
    # neither of these accept keyword arguments, but if we omit them, then ParamSpec
    # won't match the arguments correctly
    def do_handle(self, *args: _P.args, **_: _P.kwargs) -> None: ...
    def do_close(self, *args: _P.args, **_: _P.kwargs) -> None: ...
    # we would like to return _P.args here, however pyright will complain
    # mypy doesn't seem to mind
    def do_read(self) -> tuple[Any, ...] | None: ...
    def full(self) -> bool: ...
    @property
    def server_host(self) -> str | None:
        """IP address that the server is bound to (string)."""

    @property
    def server_port(self) -> int | None:
        """Port that the server is bound to (an integer)."""

    def init_socket(self) -> None:
        """
        If the user initialized the server with an address rather than
        socket, then this function must create a socket, bind it, and
        put it into listening mode.

        It is not supposed to be called by the user, it is called by :meth:`start` before starting
        the accept loop.
        """

    @property
    def started(self) -> bool: ...
    def start(self) -> None:
        """Start accepting the connections.

        If an address was provided in the constructor, then also create a socket,
        bind it and put it into the listening mode.
        """

    def close(self) -> None:
        """Close the listener socket and stop accepting."""

    @property
    def closed(self) -> bool: ...
    def stop(self, timeout: float | None = None) -> None:
        """
        Stop accepting the connections and close the listening socket.

        If the server uses a pool to spawn the requests, then
        :meth:`stop` also waits for all the handlers to exit. If there
        are still handlers executing after *timeout* has expired
        (default 1 second, :attr:`stop_timeout`), then the currently
        running handlers in the pool are killed.

        If the server does not use a pool, then this merely stops accepting connections;
        any spawned greenlets that are handling requests continue running until
        they naturally complete.
        """

    def serve_forever(self, stop_timeout: float | None = None) -> None:
        """Start the server if it hasn't been already started and wait until it's stopped."""

    def is_fatal_error(self, ex: BaseException) -> bool: ...

__all__ = ["BaseServer"]
