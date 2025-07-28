"""Base class extended by connection adapters. This extends the
connection.Connection class to encapsulate connection behavior but still
isolate socket and low level communication.

"""

import abc
from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from typing_extensions import Self

from ..adapters.utils import nbio_interface
from ..connection import Connection

LOGGER: Logger

class BaseConnection(Connection, metaclass=abc.ABCMeta):
    """BaseConnection class that should be extended by connection adapters.

    This class abstracts I/O loop and transport services from pika core.

    """

    def __init__(
        self,
        parameters,
        on_open_callback: Callable[[Self], object] | None,
        on_open_error_callback: Callable[[Self, BaseException], object] | None,
        on_close_callback: Callable[[Self, BaseException], object] | None,
        nbio,
        internal_connection_workflow: bool,
    ) -> None:
        """Create a new instance of the Connection object.

        :param None|pika.connection.Parameters parameters: Connection parameters
        :param None|method on_open_callback: Method to call on connection open
        :param None | method on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`: on_open_error_callback(Connection, exception).
        :param None | method on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the cause
            of connection failure.
        :param pika.adapters.utils.nbio_interface.AbstractIOServices nbio:
            asynchronous services
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory.
        :raises: RuntimeError
        :raises: ValueError

        """

    @classmethod
    @abc.abstractmethod
    def create_connection(cls, connection_configs, on_done, custom_ioloop=None, workflow=None):
        """Asynchronously create a connection to an AMQP broker using the given
        configurations. Will attempt to connect using each config in the given
        order, including all compatible resolved IP addresses of the hostname
        supplied in each config, until one is established or all attempts fail.

        See also `_start_connection_workflow()`.

        :param sequence connection_configs: A sequence of one or more
            `pika.connection.Parameters`-based objects.
        :param callable on_done: as defined in
            `connection_workflow.AbstractAMQPConnectionWorkflow.start()`.
        :param object | None custom_ioloop: Provide a custom I/O loop that is
            native to the specific adapter implementation; if None, the adapter
            will use a default loop instance, which is typically a singleton.
        :param connection_workflow.AbstractAMQPConnectionWorkflow | None workflow:
            Pass an instance of an implementation of the
            `connection_workflow.AbstractAMQPConnectionWorkflow` interface;
            defaults to a `connection_workflow.AMQPConnectionWorkflow` instance
            with default values for optional args.
        :returns: Connection workflow instance in use. The user should limit
            their interaction with this object only to it's `abort()` method.
        :rtype: connection_workflow.AbstractAMQPConnectionWorkflow

        """

    @property
    def ioloop(self):
        """
        :returns: the native I/O loop instance underlying async services selected
            by user or the default selected by the specialized connection
            adapter (e.g., Twisted reactor, `asyncio.SelectorEventLoop`,
            `select_connection.IOLoop`, etc.)
        :rtype: object
        """

class _StreamingProtocolShim(nbio_interface.AbstractStreamProtocol):
    """Shim for callbacks from transport so that we BaseConnection can
    delegate to private methods, thus avoiding contamination of API with
    methods that look public, but aren't.

    """

    connection_made: Incomplete
    connection_lost: Incomplete
    eof_received: Incomplete
    data_received: Incomplete
    conn: Incomplete
    def __init__(self, conn) -> None:
        """
        :param BaseConnection conn:
        """

    def __getattr__(self, attr: str):
        """Proxy inexistent attribute requests to our connection instance
        so that AMQPConnectionWorkflow/AMQPConnector may treat the shim as an
        actual connection.

        """
