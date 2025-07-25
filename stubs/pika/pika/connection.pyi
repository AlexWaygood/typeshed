"""Core connection objects"""

import abc
import ssl
from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from typing import Final
from typing_extensions import Self

from .callback import CallbackManager
from .channel import Channel
from .compat import AbstractBase
from .credentials import _Credentials
from .frame import Method
from .spec import Connection as SpecConnection

PRODUCT: str
LOGGER: Logger

class Parameters:
    """Base connection parameters class definition"""

    DEFAULT_USERNAME: str
    DEFAULT_PASSWORD: str
    DEFAULT_BLOCKED_CONNECTION_TIMEOUT: None
    DEFAULT_CHANNEL_MAX: int
    DEFAULT_CLIENT_PROPERTIES: None
    DEFAULT_CREDENTIALS: Incomplete
    DEFAULT_CONNECTION_ATTEMPTS: int
    DEFAULT_FRAME_MAX: int
    DEFAULT_HEARTBEAT_TIMEOUT: None
    DEFAULT_HOST: str
    DEFAULT_LOCALE: str
    DEFAULT_PORT: int
    DEFAULT_RETRY_DELAY: float
    DEFAULT_SOCKET_TIMEOUT: float
    DEFAULT_STACK_TIMEOUT: float
    DEFAULT_SSL: bool
    DEFAULT_SSL_OPTIONS: None
    DEFAULT_SSL_PORT: int
    DEFAULT_VIRTUAL_HOST: str
    DEFAULT_TCP_OPTIONS: None
    def __init__(self) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    @property
    def blocked_connection_timeout(self) -> float | None:
        """
        :returns: blocked connection timeout. Defaults to
            `DEFAULT_BLOCKED_CONNECTION_TIMEOUT`.
        :rtype: float|None

        """

    @blocked_connection_timeout.setter
    def blocked_connection_timeout(self, value: float | None) -> None: ...
    @property
    def channel_max(self) -> int:
        """
        :returns: max preferred number of channels. Defaults to
            `DEFAULT_CHANNEL_MAX`.
        :rtype: int

        """

    @channel_max.setter
    def channel_max(self, value: int) -> None: ...
    @property
    def client_properties(self) -> dict[Incomplete, Incomplete] | None:
        """
        :returns: client properties used to override the fields in the default
            client properties reported  to RabbitMQ via `Connection.StartOk`
            method. Defaults to `DEFAULT_CLIENT_PROPERTIES`.
        :rtype: dict|None

        """

    @client_properties.setter
    def client_properties(self, value: dict[Incomplete, Incomplete] | None) -> None: ...
    @property
    def connection_attempts(self) -> int:
        """
        :returns: number of socket connection attempts. Defaults to
            `DEFAULT_CONNECTION_ATTEMPTS`. See also `retry_delay`.
        :rtype: int

        """

    @connection_attempts.setter
    def connection_attempts(self, value: int) -> None: ...
    @property
    def credentials(self) -> _Credentials:
        """
        :rtype: one of the classes from `pika.credentials.VALID_TYPES`. Defaults
            to `DEFAULT_CREDENTIALS`.

        """

    @credentials.setter
    def credentials(self, value: _Credentials) -> None: ...
    @property
    def frame_max(self) -> int:
        """
        :returns: desired maximum AMQP frame size to use. Defaults to
            `DEFAULT_FRAME_MAX`.
        :rtype: int

        """

    @frame_max.setter
    def frame_max(self, value: int) -> None: ...
    @property
    def heartbeat(self) -> int | Callable[[Connection, int], int] | None:
        """
        :returns: AMQP connection heartbeat timeout value for negotiation during
            connection tuning or callable which is invoked during connection tuning.
            None to accept broker's value. 0 turns heartbeat off. Defaults to
            `DEFAULT_HEARTBEAT_TIMEOUT`.
        :rtype: int|callable|None

        """

    @heartbeat.setter
    def heartbeat(self, value: int | Callable[[Connection, int], int] | None) -> None: ...
    @property
    def host(self) -> str:
        """
        :returns: hostname or ip address of broker. Defaults to `DEFAULT_HOST`.
        :rtype: str

        """

    @host.setter
    def host(self, value: str) -> None: ...
    @property
    def locale(self) -> str:
        """
        :returns: locale value to pass to broker; e.g., 'en_US'. Defaults to
            `DEFAULT_LOCALE`.
        :rtype: str

        """

    @locale.setter
    def locale(self, value: str) -> None: ...
    @property
    def port(self) -> int:
        """
        :returns: port number of broker's listening socket. Defaults to
            `DEFAULT_PORT`.
        :rtype: int

        """

    @port.setter
    def port(self, value: int | str) -> None: ...
    @property
    def retry_delay(self) -> int | float:
        """
        :returns: interval between socket connection attempts; see also
            `connection_attempts`. Defaults to `DEFAULT_RETRY_DELAY`.
        :rtype: float

        """

    @retry_delay.setter
    def retry_delay(self, value: float) -> None: ...
    @property
    def socket_timeout(self) -> float | None:
        """
        :returns: socket connect timeout in seconds. Defaults to
            `DEFAULT_SOCKET_TIMEOUT`. The value None disables this timeout.
        :rtype: float|None

        """

    @socket_timeout.setter
    def socket_timeout(self, value: float | None) -> None: ...
    @property
    def stack_timeout(self) -> float | None:
        """
        :returns: full protocol stack TCP/[SSL]/AMQP bring-up timeout in
            seconds. Defaults to `DEFAULT_STACK_TIMEOUT`. The value None
            disables this timeout.
        :rtype: float

        """

    @stack_timeout.setter
    def stack_timeout(self, value: float | None) -> None: ...
    @property
    def ssl_options(self) -> SSLOptions | None:
        """
        :returns: None for plaintext or `pika.SSLOptions` instance for SSL/TLS.
        :rtype: `pika.SSLOptions`|None
        """

    @ssl_options.setter
    def ssl_options(self, value: SSLOptions | None) -> None: ...
    @property
    def virtual_host(self) -> str:
        """
        :returns: rabbitmq virtual host name. Defaults to
            `DEFAULT_VIRTUAL_HOST`.
        :rtype: str

        """

    @virtual_host.setter
    def virtual_host(self, value: str) -> None: ...
    @property
    def tcp_options(self) -> dict[Incomplete, Incomplete] | None:
        """
        :returns: None or a dict of options to pass to the underlying socket
        :rtype: dict|None
        """

    @tcp_options.setter
    def tcp_options(self, value: dict[Incomplete, Incomplete] | None) -> None: ...

class ConnectionParameters(Parameters):
    """Connection parameters object that is passed into the connection adapter
    upon construction.
    """

    def __init__(
        self,
        host: str = ...,
        port: int | str = ...,
        virtual_host: str = ...,
        credentials: _Credentials = ...,
        channel_max: int = ...,
        frame_max: int = ...,
        heartbeat: int | Callable[[Connection, int], int] | None = ...,
        ssl_options: SSLOptions | None = ...,
        connection_attempts: int = ...,
        retry_delay: float = ...,
        socket_timeout: float | None = ...,
        stack_timeout: float | None = ...,
        locale: str = ...,
        blocked_connection_timeout: float | None = ...,
        client_properties: dict[Incomplete, Incomplete] | None = ...,
        tcp_options: dict[Incomplete, Incomplete] | None = ...,
    ) -> None:
        """Create a new ConnectionParameters instance. See `Parameters` for
        default values.

        :param str host: Hostname or IP Address to connect to
        :param int port: TCP port to connect to
        :param str virtual_host: RabbitMQ virtual host to use
        :param pika.credentials.Credentials credentials: auth credentials
        :param int channel_max: Maximum number of channels to allow
        :param int frame_max: The maximum byte size for an AMQP frame
        :param int|None|callable heartbeat: Controls AMQP heartbeat timeout negotiation
            during connection tuning. An integer value always overrides the value
            proposed by broker. Use 0 to deactivate heartbeats and None to always
            accept the broker's proposal. If a callable is given, it will be called
            with the connection instance and the heartbeat timeout proposed by broker
            as its arguments. The callback should return a non-negative integer that
            will be used to override the broker's proposal.
        :param `pika.SSLOptions`|None ssl_options: None for plaintext or
            `pika.SSLOptions` instance for SSL/TLS. Defaults to None.
        :param int connection_attempts: Maximum number of retry attempts
        :param int|float retry_delay: Time to wait in seconds, before the next
        :param int|float socket_timeout: Positive socket connect timeout in
            seconds.
        :param int|float stack_timeout: Positive full protocol stack
            (TCP/[SSL]/AMQP) bring-up timeout in seconds. It's recommended to
            set this value higher than `socket_timeout`.
        :param str locale: Set the locale value
        :param int|float|None blocked_connection_timeout: If not None,
            the value is a non-negative timeout, in seconds, for the
            connection to remain blocked (triggered by Connection.Blocked from
            broker); if the timeout expires before connection becomes unblocked,
            the connection will be torn down, triggering the adapter-specific
            mechanism for informing client app about the closed connection:
            passing `ConnectionBlockedTimeout` exception to on_close_callback
            in asynchronous adapters or raising it in `BlockingConnection`.
        :param client_properties: None or dict of client properties used to
            override the fields in the default client properties reported to
            RabbitMQ via `Connection.StartOk` method.
        :param tcp_options: None or a dict of TCP options to set for socket
        """

class URLParameters(Parameters):
    """Connect to RabbitMQ via an AMQP URL in the format::

         amqp://username:password@host:port/<virtual_host>[?query-string]

    Ensure that the virtual host is URI encoded when specified. For example if
    you are using the default "/" virtual host, the value should be `%2f`.

    See `Parameters` for default values.

    Valid query string values are:

        - channel_max:
            Override the default maximum channel count value
        - client_properties:
            dict of client properties used to override the fields in the default
            client properties reported to RabbitMQ via `Connection.StartOk`
            method
        - connection_attempts:
            Specify how many times pika should try and reconnect before it gives up
        - frame_max:
            Override the default maximum frame size for communication
        - heartbeat:
            Desired connection heartbeat timeout for negotiation. If not present
            the broker's value is accepted. 0 turns heartbeat off.
        - locale:
            Override the default `en_US` locale value
        - ssl_options:
            None for plaintext; for SSL: dict of public ssl context-related
            arguments that may be passed to :meth:`ssl.SSLSocket` as kwargs,
            except `sock`, `server_side`,`do_handshake_on_connect`, `family`,
            `type`, `proto`, `fileno`.
        - retry_delay:
            The number of seconds to sleep before attempting to connect on
            connection failure.
        - socket_timeout:
            Socket connect timeout value in seconds (float or int)
        - stack_timeout:
            Positive full protocol stack (TCP/[SSL]/AMQP) bring-up timeout in
            seconds. It's recommended to set this value higher than
            `socket_timeout`.
        - blocked_connection_timeout:
            Set the timeout, in seconds, that the connection may remain blocked
            (triggered by Connection.Blocked from broker); if the timeout
            expires before connection becomes unblocked, the connection will be
            torn down, triggering the connection's on_close_callback
        - tcp_options:
            Set the tcp options for the underlying socket.

    :param str url: The AMQP URL to connect to

    """

    def __init__(self, url: str) -> None:
        """Create a new URLParameters instance.

        :param str url: The URL value

        """

class SSLOptions:
    """Class used to provide parameters for optional fine grained control of SSL
    socket wrapping.

    """

    context: ssl.SSLContext
    server_hostname: str | None
    def __init__(self, context: ssl.SSLContext, server_hostname: str | None = None) -> None:
        """
        :param ssl.SSLContext context: SSLContext instance
        :param str|None server_hostname: SSLContext.wrap_socket, used to enable
            SNI
        """

class Connection(AbstractBase, metaclass=abc.ABCMeta):
    """This is the core class that implements communication with RabbitMQ. This
    class should not be invoked directly but rather through the use of an
    adapter such as SelectConnection or BlockingConnection.

    """

    ON_CONNECTION_CLOSED: Final[str]
    ON_CONNECTION_ERROR: Final[str]
    ON_CONNECTION_OPEN_OK: Final[str]
    CONNECTION_CLOSED: Final[int]
    CONNECTION_INIT: Final[int]
    CONNECTION_PROTOCOL: Final[int]
    CONNECTION_START: Final[int]
    CONNECTION_TUNE: Final[int]
    CONNECTION_OPEN: Final[int]
    CONNECTION_CLOSING: Final[int]
    connection_state: int  # one of the constants above
    params: Parameters
    callbacks: CallbackManager
    server_capabilities: Incomplete
    server_properties: Incomplete
    known_hosts: Incomplete
    def __init__(
        self,
        parameters: Parameters | None = None,
        on_open_callback: Callable[[Self], object] | None = None,
        on_open_error_callback: Callable[[Self, BaseException], object] | None = None,
        on_close_callback: Callable[[Self, BaseException], object] | None = None,
        internal_connection_workflow: bool = True,
    ) -> None:
        """Connection initialization expects an object that has implemented the
         Parameters class and a callback function to notify when we have
         successfully connected to the AMQP Broker.

        Available Parameters classes are the ConnectionParameters class and
        URLParameters class.

        :param pika.connection.Parameters parameters: Read-only connection
            parameters.
        :param callable on_open_callback: Called when the connection is opened:
            on_open_callback(connection)
        :param None | method on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`: on_open_error_callback(Connection, exception).
        :param None | method on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the cause
            of connection failure.
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory.

        """

    def add_on_close_callback(self, callback: Callable[[Self, BaseException], object]) -> None:
        """Add a callback notification when the connection has closed. The
        callback will be passed the connection and an exception instance. The
        exception will either be an instance of `exceptions.ConnectionClosed` if
        a fully-open connection was closed by user or broker or exception of
        another type that describes the cause of connection closure/failure.

        :param callable callback: Callback to call on close, having the signature:
            callback(pika.connection.Connection, exception)

        """

    def add_on_connection_blocked_callback(self, callback: Callable[[Self, Method[SpecConnection.Blocked]], object]) -> None:
        """RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets blocked (`Connection.Blocked` received from RabbitMQ)
        due to the broker running low on resources (memory or disk). In this
        state RabbitMQ suspends processing incoming data until the connection
        is unblocked, so it's a good idea for publishers receiving this
        notification to suspend publishing until the connection becomes
        unblocked.

        See also `Connection.add_on_connection_unblocked_callback()`

        See also `ConnectionParameters.blocked_connection_timeout`.

        :param callable callback: Callback to call on `Connection.Blocked`,
            having the signature `callback(connection, pika.frame.Method)`,
            where the method frame's `method` member is of type
            `pika.spec.Connection.Blocked`

        """

    def add_on_connection_unblocked_callback(self, callback: Callable[[Self, Method[SpecConnection.Unblocked]], object]) -> None:
        """RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets unblocked (`Connection.Unblocked` frame is received from
        RabbitMQ) letting publishers know it's ok to start publishing again.

        :param callable callback: Callback to call on
            `Connection.Unblocked`, having the signature
            `callback(connection, pika.frame.Method)`, where the method frame's
            `method` member is of type `pika.spec.Connection.Unblocked`

        """

    def add_on_open_callback(self, callback: Callable[[Self], object]) -> None:
        """Add a callback notification when the connection has opened. The
        callback will be passed the connection instance as its only arg.

        :param callable callback: Callback to call when open

        """

    def add_on_open_error_callback(self, callback: Callable[[Self, BaseException], object], remove_default: bool = True) -> None:
        """Add a callback notification when the connection can not be opened.

        The callback method should accept the connection instance that could not
        connect, and either a string or an exception as its second arg.

        :param callable callback: Callback to call when can't connect, having
            the signature _(Connection, Exception)
        :param bool remove_default: Remove default exception raising callback

        """

    def channel(self, channel_number: int | None = None, on_open_callback: Callable[[Channel], object] | None = None) -> Channel:
        """Create a new channel with the next available channel number or pass
        in a channel number to use. Must be non-zero if you would like to
        specify but it is recommended that you let Pika manage the channel
        numbers.

        :param int channel_number: The channel number to use, defaults to the
                                   next available.
        :param callable on_open_callback: The callback when the channel is
            opened.  The callback will be invoked with the `Channel` instance
            as its only argument.
        :rtype: pika.channel.Channel

        """

    def update_secret(self, new_secret, reason, callback=None) -> None:
        """RabbitMQ AMQP extension - This method updates the secret used to authenticate this connection.
        It is used when secrets have an expiration date and need to be renewed, like OAuth 2 tokens.
        Pass a callback to be notified of the response from the server.

        :param string new_secret: The new secret
        :param string reason: The reason for the secret update
        :param callable callback: Callback to call on
            `Connection.UpdateSecretOk`, having the signature
            `callback(pika.frame.Method)`, where the method frame's
            `method` member is of type `pika.spec.Connection.UpdateSecretOk`

        :raises pika.exceptions.ConnectionWrongStateError: if connection is
            not open.
        """

    def close(self, reply_code: int = 200, reply_text: str = "Normal shutdown") -> None:
        """Disconnect from RabbitMQ. If there are any open channels, it will
        attempt to close them prior to fully disconnecting. Channels which
        have active consumers will attempt to send a Basic.Cancel to RabbitMQ
        to cleanly stop the delivery of messages prior to closing the channel.

        :param int reply_code: The code number for the close
        :param str reply_text: The text reason for the close

        :raises pika.exceptions.ConnectionWrongStateError: if connection is
            closed or closing.
        """

    @property
    def is_closed(self) -> bool:
        """
        Returns a boolean reporting the current connection state.
        """

    @property
    def is_closing(self) -> bool:
        """
        Returns True if connection is in the process of closing due to
        client-initiated `close` request, but closing is not yet complete.
        """

    @property
    def is_open(self) -> bool:
        """
        Returns a boolean reporting the current connection state.
        """

    @property
    def basic_nack(self) -> bool:
        """Specifies if the server supports basic.nack on the active connection.

        :rtype: bool

        """

    @property
    def consumer_cancel_notify(self) -> bool:
        """Specifies if the server supports consumer cancel notification on the
        active connection.

        :rtype: bool

        """

    @property
    def exchange_exchange_bindings(self) -> bool:
        """Specifies if the active connection supports exchange to exchange
        bindings.

        :rtype: bool

        """

    @property
    def publisher_confirms(self) -> bool:
        """Specifies if the active connection can use publisher confirmations.

        :rtype: bool

        """
