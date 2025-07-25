"""Use pika with the Tornado IOLoop"""

from _typeshed import Incomplete
from logging import Logger

from pika.adapters import base_connection

LOGGER: Logger

class TornadoConnection(base_connection.BaseConnection):
    """The TornadoConnection runs on the Tornado IOLoop."""

    def __init__(
        self,
        parameters: Incomplete | None = ...,
        on_open_callback: Incomplete | None = ...,
        on_open_error_callback: Incomplete | None = ...,
        on_close_callback: Incomplete | None = ...,
        custom_ioloop: Incomplete | None = ...,
        internal_connection_workflow: bool = ...,
    ) -> None:
        """Create a new instance of the TornadoConnection class, connecting
        to RabbitMQ automatically.

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
        :param ioloop.IOLoop|nbio_interface.AbstractIOServices|None custom_ioloop:
            Override using the global IOLoop in Tornado
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
