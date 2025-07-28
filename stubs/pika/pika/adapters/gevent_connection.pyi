"""Use pika with the Gevent IOLoop."""

from _typeshed import Incomplete
from logging import Logger

from pika.adapters.base_connection import BaseConnection
from pika.adapters.utils.nbio_interface import AbstractIOReference
from pika.adapters.utils.selector_ioloop_adapter import AbstractSelectorIOLoop, SelectorIOServicesAdapter

LOGGER: Logger

class GeventConnection(BaseConnection):
    """Implementation of pika's ``BaseConnection``.

    An async selector-based connection which integrates with Gevent.
    """

    def __init__(
        self,
        parameters: Incomplete | None = ...,
        on_open_callback: Incomplete | None = ...,
        on_open_error_callback: Incomplete | None = ...,
        on_close_callback: Incomplete | None = ...,
        custom_ioloop: Incomplete | None = ...,
        internal_connection_workflow: bool = ...,
    ) -> None:
        """Create a new GeventConnection instance and connect to RabbitMQ on
        Gevent's event-loop.

        :param pika.connection.Parameters|None parameters: The connection
            parameters
        :param callable|None on_open_callback: The method to call when the
            connection is open
        :param callable|None on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`:
            on_open_error_callback(Connection, exception)
        :param callable|None on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the
            cause of connection failure
        :param gevent._interfaces.ILoop|nbio_interface.AbstractIOServices|None
            custom_ioloop: Use a custom Gevent ILoop.
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory
        """

    @classmethod
    def create_connection(
        cls, connection_configs, on_done, custom_ioloop: Incomplete | None = ..., workflow: Incomplete | None = ...
    ):
        """Implement
        :py:classmethod::`pika.adapters.BaseConnection.create_connection()`.
        """

class _TSafeCallbackQueue:
    """Dispatch callbacks from any thread to be executed in the main thread
    efficiently with IO events.
    """

    def __init__(self) -> None:
        """
        :param _GeventSelectorIOLoop loop: IO loop to add callbacks to.
        """

    @property
    def fd(self):
        """The file-descriptor to register for READ events in the IO loop."""

    def add_callback_threadsafe(self, callback) -> None:
        """Add an item to the queue from any thread. The configured handler
        will be invoked with the item in the main thread.

        :param item: Object to add to the queue.
        """

    def run_next_callback(self) -> None:
        """Invoke the next callback from the queue.

        MUST run in the main thread. If no callback was added to the queue,
        this will block the IO loop.

        Performs a blocking READ on the pipe so must only be called when the
        pipe is ready for reading.
        """

class _GeventSelectorIOLoop(AbstractSelectorIOLoop):
    """Implementation of `AbstractSelectorIOLoop` using the Gevent event loop.

    Required by implementations of `SelectorIOServicesAdapter`.
    """

    READ: int
    WRITE: int
    ERROR: int
    def __init__(self, gevent_hub: Incomplete | None = ...) -> None:
        """
        :param gevent._interfaces.ILoop gevent_loop:
        """

    def close(self) -> None:
        """Release the loop's resources."""

    def start(self) -> None:
        """Run the I/O loop. It will loop until requested to exit. See `stop()`."""

    def stop(self) -> None:
        """Request exit from the ioloop. The loop is NOT guaranteed to
        stop before this method returns.

        To invoke `stop()` safely from a thread other than this IOLoop's thread,
        call it via `add_callback_threadsafe`; e.g.,

            `ioloop.add_callback(ioloop.stop)`
        """

    def add_callback(self, callback) -> None:
        """Requests a call to the given function as soon as possible in the
        context of this IOLoop's thread.

        NOTE: This is the only thread-safe method in IOLoop. All other
        manipulations of IOLoop must be performed from the IOLoop's thread.

        For example, a thread may request a call to the `stop` method of an
        ioloop that is running in a different thread via
        `ioloop.add_callback_threadsafe(ioloop.stop)`

        :param callable callback: The callback method
        """

    def call_later(self, delay, callback):
        """Add the callback to the IOLoop timer to be called after delay seconds
        from the time of call on best-effort basis. Returns a handle to the
        timeout.

        :param float delay: The number of seconds to wait to call callback
        :param callable callback: The callback method
        :returns: handle to the created timeout that may be passed to
            `remove_timeout()`
        :rtype: object
        """

    def remove_timeout(self, timeout_handle) -> None:
        """Remove a timeout

        :param timeout_handle: Handle of timeout to remove
        """

    def add_handler(self, fd, handler, events) -> None:
        """Start watching the given file descriptor for events

        :param int fd: The file descriptor
        :param callable handler: When requested event(s) occur,
            `handler(fd, events)` will be called.
        :param int events: The event mask (READ|WRITE)
        """

    def update_handler(self, fd, events) -> None:
        """Change the events being watched for.

        :param int fd: The file descriptor
        :param int events: The new event mask (READ|WRITE)
        """

    def remove_handler(self, fd) -> None:
        """Stop watching the given file descriptor for events

        :param int fd: The file descriptor
        """

class _GeventSelectorIOServicesAdapter(SelectorIOServicesAdapter):
    """SelectorIOServicesAdapter implementation using Gevent's DNS resolver."""

    def getaddrinfo(self, host, port, on_done, family: int = ..., socktype: int = ..., proto: int = ..., flags: int = ...):
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.getaddrinfo()`."""

class _GeventIOLoopIOHandle(AbstractIOReference):
    """Implement `AbstractIOReference`.

    Only used to wrap the _GeventAddressResolver.
    """

    def __init__(self, subject) -> None:
        """
        :param subject: subject of the reference containing a `cancel()` method
        """

    def cancel(self):
        """Cancel pending operation

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool
        """

class _GeventAddressResolver:
    """Performs getaddrinfo asynchronously Gevent's configured resolver in a
    separate greenlet and invoking the provided callback with the result.

    See: http://www.gevent.org/dns.html
    """

    def __init__(self, native_loop, host, port, family, socktype, proto, flags, on_done) -> None:
        """Initialize the `_GeventAddressResolver`.

        :param AbstractSelectorIOLoop native_loop:
        :param host: `see socket.getaddrinfo()`
        :param port: `see socket.getaddrinfo()`
        :param family: `see socket.getaddrinfo()`
        :param socktype: `see socket.getaddrinfo()`
        :param proto: `see socket.getaddrinfo()`
        :param flags: `see socket.getaddrinfo()`
        :param on_done: on_done(records|BaseException) callback for reporting
            result from the given I/O loop. The single arg will be either an
            exception object (check for `BaseException`) in case of failure or
            the result returned by `socket.getaddrinfo()`.
        """

    def start(self) -> None:
        """Start an asynchronous getaddrinfo invocation."""

    def cancel(self):
        """Cancel the pending resolver."""
