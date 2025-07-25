"""The blocking connection adapter module implements blocking semantics on top
of Pika's core AMQP driver. While most of the asynchronous expectations are
removed when using the blocking connection adapter, it attempts to remain true
to the asynchronous RPC nature of the AMQP protocol, supporting server sent
RPC commands.

The user facing classes in the module consist of the
:py:class:`~pika.adapters.blocking_connection.BlockingConnection`
and the :class:`~pika.adapters.blocking_connection.BlockingChannel`
classes.

"""

from _typeshed import Incomplete, Unused
from collections.abc import Generator, Sequence
from logging import Logger
from types import TracebackType
from typing import NamedTuple
from typing_extensions import Self

from ..connection import Parameters
from ..data import _ArgumentMapping
from ..exchange_type import ExchangeType
from ..spec import BasicProperties

LOGGER: Logger

class _CallbackResult:
    """CallbackResult is a non-thread-safe implementation for receiving
    callback results; INTERNAL USE ONLY!
    """

    def __init__(self, value_class=None) -> None:
        """
        :param callable value_class: only needed if the CallbackResult
                                     instance will be used with
                                     `set_value_once` and `append_element`.
                                     *args and **kwargs of the value setter
                                     methods will be passed to this class.

        """

    def reset(self) -> None:
        """Reset value, but not _value_class"""

    def __bool__(self) -> bool:
        """Called by python runtime to implement truth value testing and the
        built-in operation bool(); NOTE: python 3.x
        """
    __nonzero__: Incomplete
    def __enter__(self):
        """Entry into context manager that automatically resets the object
        on exit; this usage pattern helps garbage-collection by eliminating
        potential circular references.
        """

    def __exit__(self, *args: Unused, **kwargs: Unused) -> None:
        """Reset value"""

    def is_ready(self):
        """
        :returns: True if the object is in a signaled state
        :rtype: bool
        """

    @property
    def ready(self):
        """True if the object is in a signaled state"""

    def signal_once(self, *_args, **_kwargs) -> None:
        """Set as ready

        :raises AssertionError: if result was already signalled
        """

    def set_value_once(self, *args, **kwargs) -> None:
        """Set as ready with value; the value may be retrieved via the `value`
        property getter

        :raises AssertionError: if result was already set
        """

    def append_element(self, *args, **kwargs) -> None:
        """Append an element to values"""

    @property
    def value(self):
        """
        :returns: a reference to the value that was set via `set_value_once`
        :rtype: object
        :raises AssertionError: if result was not set or value is incompatible
                                with `set_value_once`
        """

    @property
    def elements(self):
        """
        :returns: a reference to the list containing one or more elements that
            were added via `append_element`
        :rtype: list
        :raises AssertionError: if result was not set or value is incompatible
                                with `append_element`
        """

class _IoloopTimerContext:
    """Context manager for registering and safely unregistering a
    SelectConnection ioloop-based timer
    """

    def __init__(self, duration, connection) -> None:
        """
        :param float duration: non-negative timer duration in seconds
        :param select_connection.SelectConnection connection:
        """

    def __enter__(self):
        """Register a timer"""

    def __exit__(self, *_args: Unused, **_kwargs: Unused) -> None:
        """Unregister timer if it hasn't fired yet"""

    def is_ready(self):
        """
        :returns: True if timer has fired, False otherwise
        :rtype: bool
        """

class _TimerEvt:
    """Represents a timer created via `BlockingConnection.call_later`"""

    timer_id: Incomplete
    def __init__(self, callback) -> None:
        """
        :param callback: see callback in `BlockingConnection.call_later`
        """

    def dispatch(self) -> None:
        """Dispatch the user's callback method"""

class _ConnectionBlockedUnblockedEvtBase:
    """Base class for `_ConnectionBlockedEvt` and `_ConnectionUnblockedEvt`"""

    def __init__(self, callback, method_frame) -> None:
        """
        :param callback: see callback parameter in
          `BlockingConnection.add_on_connection_blocked_callback` and
          `BlockingConnection.add_on_connection_unblocked_callback`
        :param pika.frame.Method method_frame: with method_frame.method of type
          `pika.spec.Connection.Blocked` or `pika.spec.Connection.Unblocked`
        """

    def dispatch(self) -> None:
        """Dispatch the user's callback method"""

class _ConnectionBlockedEvt(_ConnectionBlockedUnblockedEvtBase):
    """Represents a Connection.Blocked notification from RabbitMQ broker`"""

class _ConnectionUnblockedEvt(_ConnectionBlockedUnblockedEvtBase):
    """Represents a Connection.Unblocked notification from RabbitMQ broker`"""

class BlockingConnection:
    """The BlockingConnection creates a layer on top of Pika's asynchronous core
    providing methods that will block until their expected response has
    returned. Due to the asynchronous nature of the `Basic.Deliver` and
    `Basic.Return` calls from RabbitMQ to your application, you can still
    implement continuation-passing style asynchronous methods if you'd like to
    receive messages from RabbitMQ using
    :meth:`basic_consume <BlockingChannel.basic_consume>` or if you want to be
    notified of a delivery failure when using
    :meth:`basic_publish <BlockingChannel.basic_publish>`.

    For more information about communicating with the blocking_connection
    adapter, be sure to check out the
    :class:`BlockingChannel <BlockingChannel>` class which implements the
    :class:`Channel <pika.channel.Channel>` based communication for the
    blocking_connection adapter.

    To prevent recursion/reentrancy, the blocking connection and channel
    implementations queue asynchronously-delivered events received
    in nested context (e.g., while waiting for `BlockingConnection.channel` or
    `BlockingChannel.queue_declare` to complete), dispatching them synchronously
    once nesting returns to the desired context. This concerns all callbacks,
    such as those registered via `BlockingConnection.call_later`,
    `BlockingConnection.add_on_connection_blocked_callback`,
    `BlockingConnection.add_on_connection_unblocked_callback`,
    `BlockingChannel.basic_consume`, etc.

    Blocked Connection deadlock avoidance: when RabbitMQ becomes low on
    resources, it emits Connection.Blocked (AMQP extension) to the client
    connection when client makes a resource-consuming request on that connection
    or its channel (e.g., `Basic.Publish`); subsequently, RabbitMQ suspsends
    processing requests from that connection until the affected resources are
    restored. See http://www.rabbitmq.com/connection-blocked.html. This
    may impact `BlockingConnection` and `BlockingChannel` operations in a
    way that users might not be expecting. For example, if the user dispatches
    `BlockingChannel.basic_publish` in non-publisher-confirmation mode while
    RabbitMQ is in this low-resource state followed by a synchronous request
    (e.g., `BlockingConnection.channel`, `BlockingChannel.consume`,
    `BlockingChannel.basic_consume`, etc.), the synchronous request will block
    indefinitely (until Connection.Unblocked) waiting for RabbitMQ to reply. If
    the blocked state persists for a long time, the blocking operation will
    appear to hang. In this state, `BlockingConnection` instance and its
    channels will not dispatch user callbacks. SOLUTION: To break this potential
    deadlock, applications may configure the `blocked_connection_timeout`
    connection parameter when instantiating `BlockingConnection`. Upon blocked
    connection timeout, this adapter will raise ConnectionBlockedTimeout
    exception`. See `pika.connection.ConnectionParameters` documentation to
    learn more about the `blocked_connection_timeout` configuration.

    """

    class _OnClosedArgs(NamedTuple):
        """BlockingConnection__OnClosedArgs(connection, error)"""

        connection: Incomplete
        error: Incomplete

    class _OnChannelOpenedArgs(NamedTuple):
        """BlockingConnection__OnChannelOpenedArgs(channel,)"""

        channel: Incomplete

    def __init__(self, parameters: Parameters | Sequence[Parameters] | None = None, _impl_class=None) -> None:
        """Create a new instance of the Connection object.

        :param None | pika.connection.Parameters | sequence parameters:
            Connection parameters instance or non-empty sequence of them. If
            None, a `pika.connection.Parameters` instance will be created with
            default settings. See `pika.AMQPConnectionWorkflow` for more
            details about multiple parameter configurations and retries.
        :param _impl_class: for tests/debugging only; implementation class;
            None=default

        :raises RuntimeError:

        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    def add_on_connection_blocked_callback(self, callback) -> None:
        """RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets blocked (`Connection.Blocked` received from RabbitMQ)
        due to the broker running low on resources (memory or disk). In this
        state RabbitMQ suspends processing incoming data until the connection
        is unblocked, so it's a good idea for publishers receiving this
        notification to suspend publishing until the connection becomes
        unblocked.

        NOTE: due to the blocking nature of BlockingConnection, if it's sending
        outbound data while the connection is/becomes blocked, the call may
        remain blocked until the connection becomes unblocked, if ever. You
        may use `ConnectionParameters.blocked_connection_timeout` to abort a
        BlockingConnection method call with an exception when the connection
        remains blocked longer than the given timeout value.

        See also `Connection.add_on_connection_unblocked_callback()`

        See also `ConnectionParameters.blocked_connection_timeout`.

        :param callable callback: Callback to call on `Connection.Blocked`,
            having the signature `callback(connection, pika.frame.Method)`,
            where connection is the `BlockingConnection` instance and the method
            frame's `method` member is of type `pika.spec.Connection.Blocked`

        """

    def add_on_connection_unblocked_callback(self, callback) -> None:
        """RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets unblocked (`Connection.Unblocked` frame is received from
        RabbitMQ) letting publishers know it's ok to start publishing again.

        :param callable callback: Callback to call on Connection.Unblocked`,
            having the signature `callback(connection, pika.frame.Method)`,
            where connection is the `BlockingConnection` instance and the method
            frame's `method` member is of type `pika.spec.Connection.Unblocked`

        """

    def call_later(self, delay, callback):
        """Create a single-shot timer to fire after delay seconds. Do not
        confuse with Tornado's timeout where you pass in the time you want to
        have your callback called. Only pass in the seconds until it's to be
        called.

        NOTE: the timer callbacks are dispatched only in the scope of
        specially-designated methods: see
        `BlockingConnection.process_data_events()` and
        `BlockingChannel.start_consuming()`.

        :param float delay: The number of seconds to wait to call callback
        :param callable callback: The callback method with the signature
            callback()
        :returns: Opaque timer id
        :rtype: int

        """

    def add_callback_threadsafe(self, callback) -> None:
        """Requests a call to the given function as soon as possible in the
        context of this connection's thread.

        NOTE: This is the only thread-safe method in `BlockingConnection`. All
        other manipulations of `BlockingConnection` must be performed from the
        connection's thread.

        NOTE: the callbacks are dispatched only in the scope of
        specially-designated methods: see
        `BlockingConnection.process_data_events()` and
        `BlockingChannel.start_consuming()`.

        For example, a thread may request a call to the
        `BlockingChannel.basic_ack` method of a `BlockingConnection` that is
        running in a different thread via::

            connection.add_callback_threadsafe(
                functools.partial(channel.basic_ack, delivery_tag=...))

        NOTE: if you know that the requester is running on the same thread as
        the connection it is more efficient to use the
        `BlockingConnection.call_later()` method with a delay of 0.

        :param callable callback: The callback method; must be callable
        :raises pika.exceptions.ConnectionWrongStateError: if connection is
            closed
        """

    def remove_timeout(self, timeout_id) -> None:
        """Remove a timer if it's still in the timeout stack

        :param timeout_id: The opaque timer id to remove

        """

    def update_secret(self, new_secret, reason) -> None:
        """RabbitMQ AMQP extension - This method updates the secret used to authenticate this connection.
        It is used when secrets have an expiration date and need to be renewed, like OAuth 2 tokens.

        :param string new_secret: The new secret
        :param string reason: The reason for the secret update

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

        :raises pika.exceptions.ConnectionWrongStateError: if called on a closed
            connection (NEW in v1.0.0)
        """

    def process_data_events(self, time_limit: int = 0):
        """Will make sure that data events are processed. Dispatches timer and
        channel callbacks if not called from the scope of BlockingConnection or
        BlockingChannel callback. Your app can block on this method. If your
        application maintains a long-lived publisher connection, this method
        should be called periodically in order to respond to heartbeats and other
        data events. See `examples/long_running_publisher.py` for an example.

        :param float time_limit: suggested upper bound on processing time in
            seconds. The actual blocking time depends on the granularity of the
            underlying ioloop. Zero means return as soon as possible. None means
            there is no limit on processing time and the function will block
            until I/O produces actionable events. Defaults to 0 for backward
            compatibility. This parameter is NEW in pika 0.10.0.
        """

    def sleep(self, duration: float) -> None:
        """A safer way to sleep than calling time.sleep() directly that would
        keep the adapter from ignoring frames sent from the broker. The
        connection will "sleep" or block the number of seconds specified in
        duration in small intervals.

        :param float duration: The time to sleep in seconds

        """

    def channel(self, channel_number: int | None = None) -> BlockingChannel:
        """Create a new channel with the next available channel number or pass
        in a channel number to use. Must be non-zero if you would like to
        specify but it is recommended that you let Pika manage the channel
        numbers.

        :rtype: pika.adapters.blocking_connection.BlockingChannel
        """

    @property
    def is_closed(self) -> bool:
        """
        Returns a boolean reporting the current connection state.
        """

    @property
    def is_open(self) -> bool:
        """
        Returns a boolean reporting the current connection state.
        """

    @property
    def basic_nack_supported(self) -> bool:
        """Specifies if the server supports basic.nack on the active connection.

        :rtype: bool

        """

    @property
    def consumer_cancel_notify_supported(self) -> bool:
        """Specifies if the server supports consumer cancel notification on the
        active connection.

        :rtype: bool

        """

    @property
    def exchange_exchange_bindings_supported(self) -> bool:
        """Specifies if the active connection supports exchange to exchange
        bindings.

        :rtype: bool

        """

    @property
    def publisher_confirms_supported(self) -> bool:
        """Specifies if the active connection can use publisher confirmations.

        :rtype: bool

        """
    basic_nack = basic_nack_supported
    consumer_cancel_notify = consumer_cancel_notify_supported
    exchange_exchange_bindings = exchange_exchange_bindings_supported
    publisher_confirms = publisher_confirms_supported

class _ChannelPendingEvt:
    """Base class for BlockingChannel pending events"""

class _ConsumerDeliveryEvt(_ChannelPendingEvt):
    """This event represents consumer message delivery `Basic.Deliver`; it
    contains method, properties, and body of the delivered message.
    """

    method: Incomplete
    properties: Incomplete
    body: Incomplete
    def __init__(self, method, properties, body) -> None:
        """
        :param spec.Basic.Deliver method: NOTE: consumer_tag and delivery_tag
          are valid only within source channel
        :param spec.BasicProperties properties: message properties
        :param bytes body: message body; empty string if no body
        """

class _ConsumerCancellationEvt(_ChannelPendingEvt):
    """This event represents server-initiated consumer cancellation delivered to
    client via Basic.Cancel. After receiving Basic.Cancel, there will be no
    further deliveries for the consumer identified by `consumer_tag` in
    `Basic.Cancel`
    """

    method_frame: Incomplete
    def __init__(self, method_frame) -> None:
        """
        :param pika.frame.Method method_frame: method frame with method of type
            `spec.Basic.Cancel`
        """

    @property
    def method(self):
        """method of type spec.Basic.Cancel"""

class _ReturnedMessageEvt(_ChannelPendingEvt):
    """This event represents a message returned by broker via `Basic.Return`"""

    callback: Incomplete
    channel: Incomplete
    method: Incomplete
    properties: Incomplete
    body: Incomplete
    def __init__(self, callback, channel, method, properties, body) -> None:
        """
        :param callable callback: user's callback, having the signature
            callback(channel, method, properties, body), where
             - channel: pika.Channel
             - method: pika.spec.Basic.Return
             - properties: pika.spec.BasicProperties
             - body: bytes
        :param pika.Channel channel:
        :param pika.spec.Basic.Return method:
        :param pika.spec.BasicProperties properties:
        :param bytes body:
        """

    def dispatch(self) -> None:
        """Dispatch user's callback"""

class ReturnedMessage:
    """Represents a message returned via Basic.Return in publish-acknowledgments
    mode
    """

    method: Incomplete
    properties: Incomplete
    body: Incomplete
    def __init__(self, method, properties, body) -> None:
        """
        :param spec.Basic.Return method:
        :param spec.BasicProperties properties: message properties
        :param bytes body: message body; empty string if no body
        """

class _ConsumerInfo:
    """Information about an active consumer"""

    SETTING_UP: int
    ACTIVE: int
    TEARING_DOWN: int
    CANCELLED_BY_BROKER: int
    consumer_tag: Incomplete
    auto_ack: Incomplete
    on_message_callback: Incomplete
    alternate_event_sink: Incomplete
    state: Incomplete
    def __init__(self, consumer_tag, auto_ack, on_message_callback=None, alternate_event_sink=None) -> None:
        """
        NOTE: exactly one of callback/alternate_event_sink musts be non-None.

        :param str consumer_tag:
        :param bool auto_ack: the no-ack value for the consumer
        :param callable on_message_callback: The function for dispatching messages to
            user, having the signature:
            on_message_callback(channel, method, properties, body)
             - channel: BlockingChannel
             - method: spec.Basic.Deliver
             - properties: spec.BasicProperties
             - body: bytes
        :param callable alternate_event_sink: if specified, _ConsumerDeliveryEvt
            and _ConsumerCancellationEvt objects will be diverted to this
            callback instead of being deposited in the channel's
            `_pending_events` container. Signature:
            alternate_event_sink(evt)
        """

    @property
    def setting_up(self):
        """True if in SETTING_UP state"""

    @property
    def active(self):
        """True if in ACTIVE state"""

    @property
    def tearing_down(self):
        """True if in TEARING_DOWN state"""

    @property
    def cancelled_by_broker(self):
        """True if in CANCELLED_BY_BROKER state"""

class _QueueConsumerGeneratorInfo:
    """Container for information about the active queue consumer generator"""

    params: Incomplete
    consumer_tag: Incomplete
    pending_events: Incomplete
    def __init__(self, params, consumer_tag) -> None:
        """
        :params tuple params: a three-tuple (queue, auto_ack, exclusive) that were
           used to create the queue consumer
        :param str consumer_tag: consumer tag
        """

class BlockingChannel:
    """The BlockingChannel implements blocking semantics for most things that
    one would use callback-passing-style for with the
    :py:class:`~pika.channel.Channel` class. In addition,
    the `BlockingChannel` class implements a :term:`generator` that allows
    you to :doc:`consume messages </examples/blocking_consumer_generator>`
    without using callbacks.

    Example of creating a BlockingChannel::

        import pika

        # Create our connection object
        connection = pika.BlockingConnection()

        # The returned object will be a synchronous channel
        channel = connection.channel()

    """

    class _RxMessageArgs(NamedTuple):
        """BlockingChannel__RxMessageArgs(channel, method, properties, body)"""

        channel: Incomplete
        method: Incomplete
        properties: Incomplete
        body: Incomplete

    class _MethodFrameCallbackResultArgs(NamedTuple):
        """BlockingChannel__MethodFrameCallbackResultArgs(method_frame,)"""

        method_frame: Incomplete

    class _OnMessageConfirmationReportArgs(NamedTuple):
        """BlockingChannel__OnMessageConfirmationReportArgs(method_frame,)"""

        method_frame: Incomplete

    class _FlowOkCallbackResultArgs(NamedTuple):
        """BlockingChannel__FlowOkCallbackResultArgs(active,)"""

        active: Incomplete

    def __init__(self, channel_impl, connection) -> None:
        """Create a new instance of the Channel

        :param pika.channel.Channel channel_impl: Channel implementation object
            as returned from SelectConnection.channel()
        :param BlockingConnection connection: The connection object

        """

    def __int__(self) -> int:
        """Return the channel object as its channel number

        NOTE: inherited from legacy BlockingConnection; might be error-prone;
        use `channel_number` property instead.

        :rtype: int

        """

    def __enter__(self): ...
    def __exit__(
        self, exc_type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    @property
    def channel_number(self):
        """Channel number"""

    @property
    def connection(self):
        """The channel's BlockingConnection instance"""

    @property
    def is_closed(self):
        """Returns True if the channel is closed.

        :rtype: bool

        """

    @property
    def is_open(self):
        """Returns True if the channel is open.

        :rtype: bool

        """

    @property
    def consumer_tags(self):
        """Property method that returns a list of consumer tags for active
        consumers

        :rtype: list

        """

    def close(self, reply_code: int = 0, reply_text: str = "Normal shutdown"):
        """Will invoke a clean shutdown of the channel with the AMQP Broker.

        :param int reply_code: The reply code to close the channel with
        :param str reply_text: The reply text to close the channel with

        """

    def flow(self, active):
        """Turn Channel flow control off and on.

        NOTE: RabbitMQ doesn't support active=False; per
        https://www.rabbitmq.com/specification.html: "active=false is not
        supported by the server. Limiting prefetch with basic.qos provides much
        better control"

        For more information, please reference:

        http://www.rabbitmq.com/amqp-0-9-1-reference.html#channel.flow

        :param bool active: Turn flow on (True) or off (False)
        :returns: True if broker will start or continue sending; False if not
        :rtype: bool

        """

    def add_on_cancel_callback(self, callback) -> None:
        """Pass a callback function that will be called when Basic.Cancel
        is sent by the broker. The callback function should receive a method
        frame parameter.

        :param callable callback: a callable for handling broker's Basic.Cancel
            notification with the call signature: callback(method_frame)
            where method_frame is of type `pika.frame.Method` with method of
            type `spec.Basic.Cancel`

        """

    def add_on_return_callback(self, callback):
        """Pass a callback function that will be called when a published
        message is rejected and returned by the server via `Basic.Return`.

        :param callable callback: The method to call on callback with the
            signature callback(channel, method, properties, body), where
            - channel: pika.Channel
            - method: pika.spec.Basic.Return
            - properties: pika.spec.BasicProperties
            - body: bytes

        """

    def basic_consume(
        self, queue, on_message_callback, auto_ack: bool = False, exclusive: bool = False, consumer_tag=None, arguments=None
    ):
        """Sends the AMQP command Basic.Consume to the broker and binds messages
        for the consumer_tag to the consumer callback. If you do not pass in
        a consumer_tag, one will be automatically generated for you. Returns
        the consumer tag.

        NOTE: the consumer callbacks are dispatched only in the scope of
        specially-designated methods: see
        `BlockingConnection.process_data_events` and
        `BlockingChannel.start_consuming`.

        For more information about Basic.Consume, see:
        http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.consume

        :param str queue: The queue from which to consume
        :param callable on_message_callback: Required function for dispatching messages
            to user, having the signature:
            on_message_callback(channel, method, properties, body)
            - channel: BlockingChannel
            - method: spec.Basic.Deliver
            - properties: spec.BasicProperties
            - body: bytes
        :param bool auto_ack: if set to True, automatic acknowledgement mode will be used
                              (see http://www.rabbitmq.com/confirms.html). This corresponds
                              with the 'no_ack' parameter in the basic.consume AMQP 0.9.1
                              method
        :param bool exclusive: Don't allow other consumers on the queue
        :param str consumer_tag: You may specify your own consumer tag; if left
          empty, a consumer tag will be generated automatically
        :param dict arguments: Custom key/value pair arguments for the consumer
        :returns: consumer tag
        :rtype: str
        :raises pika.exceptions.DuplicateConsumerTag: if consumer with given
            consumer_tag is already present.

        """

    def basic_cancel(self, consumer_tag):
        """This method cancels a consumer. This does not affect already
        delivered messages, but it does mean the server will not send any more
        messages for that consumer. The client may receive an arbitrary number
        of messages in between sending the cancel method and receiving the
        cancel-ok reply.

        NOTE: When cancelling an auto_ack=False consumer, this implementation
        automatically Nacks and suppresses any incoming messages that have not
        yet been dispatched to the consumer's callback. However, when cancelling
        a auto_ack=True consumer, this method will return any pending messages
        that arrived before broker confirmed the cancellation.

        :param str consumer_tag: Identifier for the consumer; the result of
            passing a consumer_tag that was created on another channel is
            undefined (bad things will happen)
        :returns: (NEW IN pika 0.10.0) empty sequence for a auto_ack=False
            consumer; for a auto_ack=True consumer, returns a (possibly empty)
            sequence of pending messages that arrived before broker confirmed
            the cancellation (this is done instead of via consumer's callback in
            order to prevent reentrancy/recursion. Each message is four-tuple:
            (channel, method, properties, body)
            - channel: BlockingChannel
            - method: spec.Basic.Deliver
            - properties: spec.BasicProperties
            - body: bytes
        :rtype: list
        """

    def start_consuming(self) -> None:
        """Processes I/O events and dispatches timers and `basic_consume`
        callbacks until all consumers are cancelled.

        NOTE: this blocking function may not be called from the scope of a
        pika callback, because dispatching `basic_consume` callbacks from this
        context would constitute recursion.

        :raises pika.exceptions.ReentrancyError: if called from the scope of a
            `BlockingConnection` or `BlockingChannel` callback
        :raises ChannelClosed: when this channel is closed by broker.
        """

    def stop_consuming(self, consumer_tag=None) -> None:
        """Cancels all consumers, signalling the `start_consuming` loop to
        exit.

        NOTE: pending non-ackable messages will be lost; pending ackable
        messages will be rejected.

        """

    def consume(
        self, queue, auto_ack: bool = False, exclusive: bool = False, arguments=None, inactivity_timeout=None
    ) -> Generator[Incomplete, None, None]:
        """Blocking consumption of a queue instead of via a callback. This
        method is a generator that yields each message as a tuple of method,
        properties, and body. The active generator iterator terminates when the
        consumer is cancelled by client via `BlockingChannel.cancel()` or by
        broker.

        Example:
        ::
            for method, properties, body in channel.consume('queue'):
                print(body)
                channel.basic_ack(method.delivery_tag)

        You should call `BlockingChannel.cancel()` when you escape out of the
        generator loop.

        If you don't cancel this consumer, then next call on the same channel
        to `consume()` with the exact same (queue, auto_ack, exclusive) parameters
        will resume the existing consumer generator; however, calling with
        different parameters will result in an exception.

        :param str queue: The queue name to consume
        :param bool auto_ack: Tell the broker to not expect a ack/nack response
        :param bool exclusive: Don't allow other consumers on the queue
        :param dict arguments: Custom key/value pair arguments for the consumer
        :param float inactivity_timeout: if a number is given (in
            seconds), will cause the method to yield (None, None, None) after the
            given period of inactivity; this permits for pseudo-regular maintenance
            activities to be carried out by the user while waiting for messages
            to arrive. If None is given (default), then the method blocks until
            the next event arrives. NOTE that timing granularity is limited by
            the timer resolution of the underlying implementation.
            NEW in pika 0.10.0.

        :yields: tuple(spec.Basic.Deliver, spec.BasicProperties, str or unicode)

        :raises ValueError: if consumer-creation parameters don't match those
            of the existing queue consumer generator, if any.
            NEW in pika 0.10.0
        :raises ChannelClosed: when this channel is closed by broker.

        """

    def get_waiting_message_count(self):
        """Returns the number of messages that may be retrieved from the current
        queue consumer generator via `BlockingChannel.consume` without blocking.
        NEW in pika 0.10.0

        :returns: The number of waiting messages
        :rtype: int
        """

    def cancel(self):
        """Cancel the queue consumer created by `BlockingChannel.consume`,
        rejecting all pending ackable messages.

        NOTE: If you're looking to cancel a consumer issued with
        BlockingChannel.basic_consume then you should call
        BlockingChannel.basic_cancel.

        :returns: The number of messages requeued by Basic.Nack.
            NEW in 0.10.0: returns 0
        :rtype: int

        """

    def basic_ack(self, delivery_tag: int = 0, multiple: bool = False) -> None:
        """Acknowledge one or more messages. When sent by the client, this
        method acknowledges one or more messages delivered via the Deliver or
        Get-Ok methods. When sent by server, this method acknowledges one or
        more messages published with the Publish method on a channel in
        confirm mode. The acknowledgement can be for a single message or a
        set of messages up to and including a specific message.

        :param int delivery_tag: The server-assigned delivery tag
        :param bool multiple: If set to True, the delivery tag is treated as
                              "up to and including", so that multiple messages
                              can be acknowledged with a single method. If set
                              to False, the delivery tag refers to a single
                              message. If the multiple field is 1, and the
                              delivery tag is zero, this indicates
                              acknowledgement of all outstanding messages.
        """

    def basic_nack(self, delivery_tag: int = 0, multiple: bool = False, requeue: bool = True) -> None:
        """This method allows a client to reject one or more incoming messages.
        It can be used to interrupt and cancel large incoming messages, or
        return untreatable messages to their original queue.

        :param int delivery_tag: The server-assigned delivery tag
        :param bool multiple: If set to True, the delivery tag is treated as
                              "up to and including", so that multiple messages
                              can be acknowledged with a single method. If set
                              to False, the delivery tag refers to a single
                              message. If the multiple field is 1, and the
                              delivery tag is zero, this indicates
                              acknowledgement of all outstanding messages.
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.

        """

    def basic_get(self, queue, auto_ack: bool = False):
        """Get a single message from the AMQP broker. Returns a sequence with
        the method frame, message properties, and body.

        :param str queue: Name of queue from which to get a message
        :param bool auto_ack: Tell the broker to not expect a reply
        :returns: a three-tuple; (None, None, None) if the queue was empty;
            otherwise (method, properties, body); NOTE: body may be None
        :rtype: (spec.Basic.GetOk|None, spec.BasicProperties|None, bytes|None)
        """

    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: str | bytes,
        properties: BasicProperties | None = None,
        mandatory: bool = False,
    ) -> None:
        """Publish to the channel with the given exchange, routing key, and
        body.

        For more information on basic_publish and what the parameters do, see:

            http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.publish

        NOTE: mandatory may be enabled even without delivery
          confirmation, but in the absence of delivery confirmation the
          synchronous implementation has no way to know how long to wait for
          the Basic.Return.

        :param str exchange: The exchange to publish to
        :param str routing_key: The routing key to bind on
        :param bytes body: The message body; empty string if no body
        :param pika.spec.BasicProperties properties: message properties
        :param bool mandatory: The mandatory flag

        :raises UnroutableError: raised when a message published in
            publisher-acknowledgments mode (see
            `BlockingChannel.confirm_delivery`) is returned via `Basic.Return`
            followed by `Basic.Ack`.
        :raises NackError: raised when a message published in
            publisher-acknowledgements mode is Nack'ed by the broker. See
            `BlockingChannel.confirm_delivery`.

        """

    def basic_qos(self, prefetch_size: int = 0, prefetch_count: int = 0, global_qos: bool = False) -> None:
        """Specify quality of service. This method requests a specific quality
        of service. The QoS can be specified for the current channel or for all
        channels on the connection. The client can request that messages be sent
        in advance so that when the client finishes processing a message, the
        following message is already held locally, rather than needing to be
        sent down the channel. Prefetching gives a performance improvement.

        :param int prefetch_size:  This field specifies the prefetch window
                                   size. The server will send a message in
                                   advance if it is equal to or smaller in size
                                   than the available prefetch size (and also
                                   falls into other prefetch limits). May be set
                                   to zero, meaning "no specific limit",
                                   although other prefetch limits may still
                                   apply. The prefetch-size is ignored if the
                                   no-ack option is set in the consumer.
        :param int prefetch_count: Specifies a prefetch window in terms of whole
                                   messages. This field may be used in
                                   combination with the prefetch-size field; a
                                   message will only be sent in advance if both
                                   prefetch windows (and those at the channel
                                   and connection level) allow it. The
                                   prefetch-count is ignored if the no-ack
                                   option is set in the consumer.
        :param bool global_qos:    Should the QoS apply to all channels on the
                                   connection.

        """

    def basic_recover(self, requeue: bool = False) -> None:
        """This method asks the server to redeliver all unacknowledged messages
        on a specified channel. Zero or more messages may be redelivered. This
        method replaces the asynchronous Recover.

        :param bool requeue: If False, the message will be redelivered to the
                             original recipient. If True, the server will
                             attempt to requeue the message, potentially then
                             delivering it to an alternative subscriber.

        """

    def basic_reject(self, delivery_tag: int = 0, requeue: bool = True) -> None:
        """Reject an incoming message. This method allows a client to reject a
        message. It can be used to interrupt and cancel large incoming messages,
        or return untreatable messages to their original queue.

        :param int delivery_tag: The server-assigned delivery tag
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.

        """

    def confirm_delivery(self) -> None:
        """Turn on RabbitMQ-proprietary Confirm mode in the channel.

        For more information see:
            https://www.rabbitmq.com/confirms.html
        """

    def exchange_declare(
        self,
        exchange: str,
        exchange_type: ExchangeType | str = ...,
        passive: bool = False,
        durable: bool = False,
        auto_delete: bool = False,
        internal: bool = False,
        arguments: _ArgumentMapping | None = None,
    ):
        """This method creates an exchange if it does not already exist, and if
        the exchange exists, verifies that it is of the correct and expected
        class.

        If passive set, the server will reply with Declare-Ok if the exchange
        already exists with the same name, and raise an error if not and if the
        exchange does not already exist, the server MUST raise a channel
        exception with reply code 404 (not found).

        :param str exchange: The exchange name consists of a non-empty sequence of
                          these characters: letters, digits, hyphen, underscore,
                          period, or colon.
        :param str exchange_type: The exchange type to use
        :param bool passive: Perform a declare or just check to see if it exists
        :param bool durable: Survive a reboot of RabbitMQ
        :param bool auto_delete: Remove when no more queues are bound to it
        :param bool internal: Can only be published to by other exchanges
        :param dict arguments: Custom key/value pair arguments for the exchange
        :returns: Method frame from the Exchange.Declare-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Exchange.DeclareOk`

        """

    def exchange_delete(self, exchange: str | None = None, if_unused: bool = False):
        """Delete the exchange.

        :param str exchange: The exchange name
        :param bool if_unused: only delete if the exchange is unused
        :returns: Method frame from the Exchange.Delete-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Exchange.DeleteOk`

        """

    def exchange_bind(self, destination, source, routing_key: str = "", arguments=None):
        """Bind an exchange to another exchange.

        :param str destination: The destination exchange to bind
        :param str source: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding
        :returns: Method frame from the Exchange.Bind-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
          `spec.Exchange.BindOk`

        """

    def exchange_unbind(self, destination=None, source=None, routing_key: str = "", arguments=None):
        """Unbind an exchange from another exchange.

        :param str destination: The destination exchange to unbind
        :param str source: The source exchange to unbind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding
        :returns: Method frame from the Exchange.Unbind-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Exchange.UnbindOk`

        """

    def queue_declare(
        self,
        queue,
        passive: bool = False,
        durable: bool = False,
        exclusive: bool = False,
        auto_delete: bool = False,
        arguments=None,
    ):
        """Declare queue, create if needed. This method creates or checks a
        queue. When creating a new queue the client can specify various
        properties that control the durability of the queue and its contents,
        and the level of sharing for the queue.

        Use an empty string as the queue name for the broker to auto-generate
        one. Retrieve this auto-generated queue name from the returned
        `spec.Queue.DeclareOk` method frame.

        :param str queue: The queue name; if empty string, the broker will
            create a unique queue name
        :param bool passive: Only check to see if the queue exists and raise
          `ChannelClosed` if it doesn't
        :param bool durable: Survive reboots of the broker
        :param bool exclusive: Only allow access by the current connection
        :param bool auto_delete: Delete after consumer cancels or disconnects
        :param dict arguments: Custom key/value arguments for the queue
        :returns: Method frame from the Queue.Declare-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Queue.DeclareOk`

        """

    def queue_delete(self, queue, if_unused: bool = False, if_empty: bool = False):
        """Delete a queue from the broker.

        :param str queue: The queue to delete
        :param bool if_unused: only delete if it's unused
        :param bool if_empty: only delete if the queue is empty
        :returns: Method frame from the Queue.Delete-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Queue.DeleteOk`

        """

    def queue_purge(self, queue):
        """Purge all of the messages from the specified queue

        :param str queue: The queue to purge
        :returns: Method frame from the Queue.Purge-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Queue.PurgeOk`

        """

    def queue_bind(self, queue, exchange, routing_key=None, arguments=None):
        """Bind the queue to the specified exchange

        :param str queue: The queue to bind to the exchange
        :param str exchange: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding

        :returns: Method frame from the Queue.Bind-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Queue.BindOk`

        """

    def queue_unbind(self, queue, exchange=None, routing_key=None, arguments=None):
        """Unbind a queue from an exchange.

        :param str queue: The queue to unbind from the exchange
        :param str exchange: The source exchange to bind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding

        :returns: Method frame from the Queue.Unbind-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Queue.UnbindOk`

        """

    def tx_select(self):
        """Select standard transaction mode. This method sets the channel to use
        standard transactions. The client must use this method at least once on
        a channel before using the Commit or Rollback methods.

        :returns: Method frame from the Tx.Select-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Tx.SelectOk`

        """

    def tx_commit(self):
        """Commit a transaction.

        :returns: Method frame from the Tx.Commit-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Tx.CommitOk`

        """

    def tx_rollback(self):
        """Rollback a transaction.

        :returns: Method frame from the Tx.Commit-ok response
        :rtype: `pika.frame.Method` having `method` attribute of type
            `spec.Tx.CommitOk`

        """
