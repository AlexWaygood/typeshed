"""A connection adapter that tries to use the best polling method for the
platform pika is running on.

"""

import abc
from _typeshed import Incomplete
from logging import Logger

import pika.compat
from pika.adapters.base_connection import BaseConnection
from pika.adapters.utils.selector_ioloop_adapter import AbstractSelectorIOLoop

LOGGER: Logger
SELECT_TYPE: Incomplete

class SelectConnection(BaseConnection):
    """An asynchronous connection adapter that attempts to use the fastest
    event loop adapter for the given platform.

    """

    def __init__(
        self,
        parameters=None,
        on_open_callback=None,
        on_open_error_callback=None,
        on_close_callback=None,
        custom_ioloop=None,
        internal_connection_workflow: bool = True,
    ) -> None:
        """Create a new instance of the Connection object.

        :param pika.connection.Parameters parameters: Connection parameters
        :param callable on_open_callback: Method to call on connection open
        :param None | method on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`: on_open_error_callback(Connection, exception).
        :param None | method on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the cause
            of connection failure.
        :param None | IOLoop | nbio_interface.AbstractIOServices custom_ioloop:
            Provide a custom I/O Loop object.
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory.
        :raises: RuntimeError

        """

    @classmethod
    def create_connection(cls, connection_configs, on_done, custom_ioloop=None, workflow=None):
        """Implement
        :py:classmethod::`pika.adapters.BaseConnection.create_connection()`.

        """

class _Timeout:
    """Represents a timeout"""

    deadline: Incomplete
    callback: Incomplete
    def __init__(self, deadline, callback) -> None:
        """
        :param float deadline: timer expiration as non-negative epoch number
        :param callable callback: callback to call when timeout expires
        :raises ValueError, TypeError:
        """

    def __eq__(self, other):
        """NOTE: not supporting sort stability"""

    def __ne__(self, other):
        """NOTE: not supporting sort stability"""

    def __lt__(self, other):
        """NOTE: not supporting sort stability"""

    def __gt__(self, other):
        """NOTE: not supporting sort stability"""

    def __le__(self, other):
        """NOTE: not supporting sort stability"""

    def __ge__(self, other):
        """NOTE: not supporting sort stability"""

class _Timer:
    """Manage timeouts for use in ioloop"""

    def __init__(self) -> None: ...
    def close(self) -> None:
        """Release resources. Don't use the `_Timer` instance after closing
        it
        """

    def call_later(self, delay, callback):
        """Schedule a one-shot timeout given delay seconds.

        NOTE: you may cancel the timer before dispatch of the callback. Timer
            Manager cancels the timer upon dispatch of the callback.

        :param float delay: Non-negative number of seconds from now until
            expiration
        :param callable callback: The callback method, having the signature
            `callback()`

        :rtype: _Timeout
        :raises ValueError, TypeError

        """

    def remove_timeout(self, timeout) -> None:
        """Cancel the timeout

        :param _Timeout timeout: The timer to cancel

        """

    def get_remaining_interval(self):
        """Get the interval to the next timeout expiration

        :returns: non-negative number of seconds until next timer expiration;
                  None if there are no timers
        :rtype: float

        """

    def process_timeouts(self) -> None:
        """Process pending timeouts, invoking callbacks for those whose time has
        come

        """

class PollEvents:
    """Event flags for I/O"""

    READ: Incomplete
    WRITE: Incomplete
    ERROR: Incomplete

class IOLoop(AbstractSelectorIOLoop):
    """I/O loop implementation that picks a suitable poller (`select`,
    `poll`, `epoll`, `kqueue`) to use based on platform.

    Implements the
    `pika.adapters.utils.selector_ioloop_adapter.AbstractSelectorIOLoop`
    interface.

    """

    READ: Incomplete
    WRITE: Incomplete
    ERROR: Incomplete
    def __init__(self) -> None: ...
    def close(self) -> None:
        """Release IOLoop's resources.

        `IOLoop.close` is intended to be called by the application or test code
        only after `IOLoop.start()` returns. After calling `close()`, no other
        interaction with the closed instance of `IOLoop` should be performed.

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

    def add_callback_threadsafe(self, callback) -> None:
        """Requests a call to the given function as soon as possible in the
        context of this IOLoop's thread.

        NOTE: This is the only thread-safe method in IOLoop. All other
        manipulations of IOLoop must be performed from the IOLoop's thread.

        For example, a thread may request a call to the `stop` method of an
        ioloop that is running in a different thread via
        `ioloop.add_callback_threadsafe(ioloop.stop)`

        :param callable callback: The callback method

        """
    add_callback: Incomplete
    def process_timeouts(self) -> None:
        """[Extension] Process pending callbacks and timeouts, invoking those
        whose time has come. Internal use only.

        """

    def add_handler(self, fd, handler, events) -> None:
        """Start watching the given file descriptor for events

        :param int fd: The file descriptor
        :param callable handler: When requested event(s) occur,
            `handler(fd, events)` will be called.
        :param int events: The event mask using READ, WRITE, ERROR.

        """

    def update_handler(self, fd, events) -> None:
        """Changes the events we watch for

        :param int fd: The file descriptor
        :param int events: The event mask using READ, WRITE, ERROR

        """

    def remove_handler(self, fd) -> None:
        """Stop watching the given file descriptor for events

        :param int fd: The file descriptor

        """

    def start(self) -> None:
        """[API] Start the main poller loop. It will loop until requested to
        exit. See `IOLoop.stop`.

        """

    def stop(self) -> None:
        """[API] Request exit from the ioloop. The loop is NOT guaranteed to
        stop before this method returns.

        To invoke `stop()` safely from a thread other than this IOLoop's thread,
        call it via `add_callback_threadsafe`; e.g.,

            `ioloop.add_callback_threadsafe(ioloop.stop)`

        """

    def activate_poller(self) -> None:
        """[Extension] Activate the poller"""

    def deactivate_poller(self) -> None:
        """[Extension] Deactivate the poller"""

    def poll(self) -> None:
        """[Extension] Wait for events of interest on registered file
        descriptors until an event of interest occurs or next timer deadline or
        `_PollerBase._MAX_POLL_TIMEOUT`, whichever is sooner, and dispatch the
        corresponding event handlers.

        """

class _PollerBase(pika.compat.AbstractBase, metaclass=abc.ABCMeta):
    """Base class for select-based IOLoop implementations"""

    POLL_TIMEOUT_MULT: int
    def __init__(self, get_wait_seconds, process_timeouts) -> None:
        """
        :param get_wait_seconds: Function for getting the maximum number of
                                 seconds to wait for IO for use by the poller
        :param process_timeouts: Function for processing timeouts for use by the
                                 poller

        """

    def close(self) -> None:
        """Release poller's resources.

        `close()` is intended to be called after the poller's `start()` method
        returns. After calling `close()`, no other interaction with the closed
        poller instance should be performed.

        """

    def wake_threadsafe(self) -> None:
        """Wake up the poller as soon as possible. As the name indicates, this
        method is thread-safe.

        """

    def add_handler(self, fileno, handler, events) -> None:
        """Add a new fileno to the set to be monitored

        :param int fileno: The file descriptor
        :param callable handler: What is called when an event happens
        :param int events: The event mask using READ, WRITE, ERROR

        """

    def update_handler(self, fileno, events) -> None:
        """Set the events to the current events

        :param int fileno: The file descriptor
        :param int events: The event mask using READ, WRITE, ERROR

        """

    def remove_handler(self, fileno) -> None:
        """Remove a file descriptor from the set

        :param int fileno: The file descriptor

        """

    def activate_poller(self) -> None:
        """Activate the poller"""

    def deactivate_poller(self) -> None:
        """Deactivate the poller"""

    def start(self) -> None:
        """Start the main poller loop. It will loop until requested to exit.
        This method is not reentrant and will raise an error if called
        recursively (pika/pika#1095)

        :raises: RuntimeError

        """

    def stop(self) -> None:
        """Request exit from the ioloop. The loop is NOT guaranteed to stop
        before this method returns.

        """

    @abc.abstractmethod
    def poll(self):
        """Wait for events on interested filedescriptors."""

class SelectPoller(_PollerBase):
    """Default behavior is to use Select since it's the widest supported and has
    all of the methods we need for child classes as well. One should only need
    to override the update_handler and start methods for additional types.

    """

    POLL_TIMEOUT_MULT: int
    def poll(self) -> None:
        """Wait for events of interest on registered file descriptors until an
        event of interest occurs or next timer deadline or _MAX_POLL_TIMEOUT,
        whichever is sooner, and dispatch the corresponding event handlers.

        """

class KQueuePoller(_PollerBase):
    """KQueuePoller works on BSD based systems and is faster than select"""

    def __init__(self, get_wait_seconds, process_timeouts) -> None:
        """Create an instance of the KQueuePoller"""

    def poll(self) -> None:
        """Wait for events of interest on registered file descriptors until an
        event of interest occurs or next timer deadline or _MAX_POLL_TIMEOUT,
        whichever is sooner, and dispatch the corresponding event handlers.

        """

class PollPoller(_PollerBase):
    """Poll works on Linux and can have better performance than EPoll in
    certain scenarios.  Both are faster than select.

    """

    POLL_TIMEOUT_MULT: int
    def __init__(self, get_wait_seconds, process_timeouts) -> None:
        """Create an instance of the KQueuePoller"""

    def poll(self) -> None:
        """Wait for events of interest on registered file descriptors until an
        event of interest occurs or next timer deadline or _MAX_POLL_TIMEOUT,
        whichever is sooner, and dispatch the corresponding event handlers.

        """

class EPollPoller(PollPoller):
    """EPoll works on Linux and can have better performance than Poll in
    certain scenarios. Both are faster than select.

    """

    POLL_TIMEOUT_MULT: int
