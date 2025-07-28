"""
Implementation of `nbio_interface.AbstractIOServices` on top of a
selector-based I/O loop, such as tornado's and our home-grown
select_connection's I/O loops.

"""

import abc
from _typeshed import Incomplete
from logging import Logger

from pika.adapters.utils import io_services_utils, nbio_interface

LOGGER: Logger

class AbstractSelectorIOLoop(metaclass=abc.ABCMeta):
    """Selector-based I/O loop interface expected by
    `selector_ioloop_adapter.SelectorIOServicesAdapter`

    NOTE: this interface follows the corresponding methods and attributes
     of `tornado.ioloop.IOLoop` in order to avoid additional adapter layering
     when wrapping tornado's IOLoop.
    """

    @property
    @abc.abstractmethod
    def READ(self):
        """The value of the I/O loop's READ flag; READ/WRITE/ERROR may be used
        with bitwise operators as expected.

        Implementation note: the implementations can simply replace these
        READ/WRITE/ERROR properties with class-level attributes

        """

    @property
    @abc.abstractmethod
    def WRITE(self):
        """The value of the I/O loop's WRITE flag; READ/WRITE/ERROR may be used
        with bitwise operators as expected

        """

    @property
    @abc.abstractmethod
    def ERROR(self):
        """The value of the I/O loop's ERROR flag; READ/WRITE/ERROR may be used
        with bitwise operators as expected

        """

    @abc.abstractmethod
    def close(self):
        """Release IOLoop's resources.

        the `close()` method is intended to be called by the application or test
        code only after `start()` returns. After calling `close()`, no other
        interaction with the closed instance of `IOLoop` should be performed.

        """

    @abc.abstractmethod
    def start(self):
        """Run the I/O loop. It will loop until requested to exit. See `stop()`."""

    @abc.abstractmethod
    def stop(self):
        """Request exit from the ioloop. The loop is NOT guaranteed to
        stop before this method returns.

        To invoke `stop()` safely from a thread other than this IOLoop's thread,
        call it via `add_callback_threadsafe`; e.g.,

            `ioloop.add_callback(ioloop.stop)`

        """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def remove_timeout(self, timeout_handle):
        """Remove a timeout

        :param timeout_handle: Handle of timeout to remove

        """

    @abc.abstractmethod
    def add_callback(self, callback):
        """Requests a call to the given function as soon as possible in the
        context of this IOLoop's thread.

        NOTE: This is the only thread-safe method in IOLoop. All other
        manipulations of IOLoop must be performed from the IOLoop's thread.

        For example, a thread may request a call to the `stop` method of an
        ioloop that is running in a different thread via
        `ioloop.add_callback_threadsafe(ioloop.stop)`

        :param callable callback: The callback method

        """

    @abc.abstractmethod
    def add_handler(self, fd, handler, events):
        """Start watching the given file descriptor for events

        :param int fd: The file descriptor
        :param callable handler: When requested event(s) occur,
            `handler(fd, events)` will be called.
        :param int events: The event mask using READ, WRITE, ERROR.

        """

    @abc.abstractmethod
    def update_handler(self, fd, events):
        """Changes the events we watch for

        :param int fd: The file descriptor
        :param int events: The event mask using READ, WRITE, ERROR

        """

    @abc.abstractmethod
    def remove_handler(self, fd):
        """Stop watching the given file descriptor for events

        :param int fd: The file descriptor

        """

class SelectorIOServicesAdapter(
    io_services_utils.SocketConnectionMixin,
    io_services_utils.StreamingConnectionMixin,
    nbio_interface.AbstractIOServices,
    nbio_interface.AbstractFileDescriptorServices,
):
    """Implements the
    :py:class:`.nbio_interface.AbstractIOServices` interface
    on top of selector-style native loop having the
    :py:class:`AbstractSelectorIOLoop` interface, such as
    :py:class:`pika.selection_connection.IOLoop` and :py:class:`tornado.IOLoop`.

    NOTE:
    :py:class:`.nbio_interface.AbstractFileDescriptorServices`
    interface is only required by the mixins.

    """

    def __init__(self, native_loop) -> None:
        """
        :param AbstractSelectorIOLoop native_loop: An instance compatible with
            the `AbstractSelectorIOLoop` interface, but not necessarily derived
            from it.
        """

    def get_native_ioloop(self):
        """Implement
        :py:meth:`.nbio_interface.AbstractIOServices.get_native_ioloop()`.

        """

    def close(self) -> None:
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.close()`."""

    def run(self) -> None:
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.run()`."""

    def stop(self) -> None:
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.stop()`."""

    def add_callback_threadsafe(self, callback) -> None:
        """Implement
        :py:meth:`.nbio_interface.AbstractIOServices.add_callback_threadsafe()`.

        """

    def call_later(self, delay, callback):
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.call_later()`."""

    def getaddrinfo(self, host, port, on_done, family: int = 0, socktype: int = 0, proto: int = 0, flags: int = 0):
        """Implement :py:meth:`.nbio_interface.AbstractIOServices.getaddrinfo()`."""

    def set_reader(self, fd, on_readable) -> None:
        """Implement
        :py:meth:`.nbio_interface.AbstractFileDescriptorServices.set_reader()`.

        """

    def remove_reader(self, fd):
        """Implement
        :py:meth:`.nbio_interface.AbstractFileDescriptorServices.remove_reader()`.

        """

    def set_writer(self, fd, on_writable) -> None:
        """Implement
        :py:meth:`.nbio_interface.AbstractFileDescriptorServices.set_writer()`.

        """

    def remove_writer(self, fd):
        """Implement
        :py:meth:`.nbio_interface.AbstractFileDescriptorServices.remove_writer()`.

        """

class _FileDescriptorCallbacks:
    """Holds reader and writer callbacks for a file descriptor"""

    reader: Incomplete
    writer: Incomplete
    def __init__(self, reader=None, writer=None) -> None: ...

class _TimerHandle(nbio_interface.AbstractTimerReference):
    """This module's adaptation of `nbio_interface.AbstractTimerReference`."""

    def __init__(self, handle, loop) -> None:
        """

        :param opaque handle: timer handle from the underlying loop
            implementation that may be passed to its `remove_timeout()` method
        :param AbstractSelectorIOLoop loop: the I/O loop instance that created
            the timeout.
        """

    def cancel(self) -> None: ...

class _SelectorIOLoopIOHandle(nbio_interface.AbstractIOReference):
    """This module's adaptation of `nbio_interface.AbstractIOReference`"""

    def __init__(self, subject) -> None:
        """
        :param subject: subject of the reference containing a `cancel()` method

        """

    def cancel(self):
        """Cancel pending operation

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool

        """

class _AddressResolver:
    """Performs getaddrinfo asynchronously using a thread, then reports result
    via callback from the given I/O loop.

    NOTE: at this stage, we're using a thread per request, which may prove
    inefficient and even prohibitive if the app performs many of these
    operations concurrently.
    """

    NOT_STARTED: int
    ACTIVE: int
    CANCELED: int
    COMPLETED: int
    def __init__(self, native_loop, host, port, family, socktype, proto, flags, on_done) -> None:
        """

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

    def start(self):
        """Start asynchronous DNS lookup.

        :rtype: nbio_interface.AbstractIOReference

        """

    def cancel(self):
        """Cancel the pending resolver

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool

        """
