"""Using Pika with a Twisted reactor.

The interfaces in this module are Deferred-based when possible. This means that
the connection.channel() method and most of the channel methods return
Deferreds instead of taking a callback argument and that basic_consume()
returns a Twisted DeferredQueue where messages from the server will be
stored. Refer to the docstrings for TwistedProtocolConnection.channel() and the
TwistedChannel class for details.

"""

# twisted is optional and self-contained in this module.
# We don't want to force it as a dependency but that means we also can't test it with type-checkers given the current setup.

from _typeshed import Incomplete
from logging import Logger
from typing import Generic, NamedTuple, TypeVar

import pika.connection
from pika.adapters.utils import nbio_interface
from twisted.internet.base import DelayedCall  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
from twisted.internet.defer import (  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
    Deferred,
    DeferredQueue,
)
from twisted.internet.interfaces import ITransport  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
from twisted.internet.protocol import Protocol  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
from twisted.python.failure import Failure  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]

_T = TypeVar("_T")

LOGGER: Logger

class ClosableDeferredQueue(DeferredQueue[_T], Generic[_T]):  # pyright: ignore[reportUntypedBaseClass]  # noqa: Y060
    """
    Like the normal Twisted DeferredQueue, but after close() is called with an
    exception instance all pending Deferreds are errbacked and further attempts
    to call get() or put() return a Failure wrapping that exception.
    """

    closed: Failure | BaseException | None
    def __init__(self, size: Incomplete | None = ..., backlog: Incomplete | None = ...) -> None: ...
    # Returns a Deferred with an error if fails. None if success
    def put(self, obj: _T) -> Deferred[Failure | BaseException] | None:  # type: ignore[override]  # ignore is not needed for mypy, but is for stubtest
        """
        Like the original :meth:`DeferredQueue.put` method, but returns an
        errback if the queue is closed.

        """

    def get(self) -> Deferred[Failure | BaseException | _T]:  # type: ignore[override]  # ignore is not needed for mypy, but is for stubtest
        """
        Returns a Deferred that will fire with the next item in the queue, when
        it's available.

        The Deferred will errback if the queue is closed.

        :returns: Deferred that fires with the next item.
        :rtype: Deferred

        """
    pending: Incomplete
    def close(self, reason: BaseException | None) -> None:
        """Closes the queue.

        Errback the pending calls to :meth:`get()`.

        """

class ReceivedMessage(NamedTuple):
    """ReceivedMessage(channel, method, properties, body)"""

    channel: Incomplete
    method: Incomplete
    properties: Incomplete
    body: Incomplete

class TwistedChannel:
    """A wrapper around Pika's Channel.

    Channel methods that normally take a callback argument are wrapped to
    return a Deferred that fires with whatever would be passed to the callback.
    If the channel gets closed, all pending Deferreds are errbacked with a
    ChannelClosed exception. The returned Deferreds fire with whatever
    arguments the callback to the original method would receive.

    Some methods like basic_consume and basic_get are wrapped in a special way,
    see their docstrings for details.
    """

    on_closed: Deferred[Incomplete | Failure | BaseException | None]
    def __init__(self, channel) -> None: ...
    @property
    def channel_number(self): ...
    @property
    def connection(self): ...
    @property
    def is_closed(self):
        """Returns True if the channel is closed.

        :rtype: bool

        """

    @property
    def is_closing(self):
        """Returns True if client-initiated closing of the channel is in
        progress.

        :rtype: bool

        """

    @property
    def is_open(self):
        """Returns True if the channel is open.

        :rtype: bool

        """

    @property
    def flow_active(self): ...
    @property
    def consumer_tags(self): ...
    def callback_deferred(self, deferred, replies) -> None:
        """Pass in a Deferred and a list replies from the RabbitMQ broker which
        you'd like the Deferred to be callbacked on with the frame as callback
        value.

        :param Deferred deferred: The Deferred to callback
        :param list replies: The replies to callback on

        """

    def add_on_return_callback(self, callback):
        """Pass a callback function that will be called when a published
        message is rejected and returned by the server via `Basic.Return`.

        :param callable callback: The method to call on callback with the
            message as only argument. The message is a named tuple with
            the following attributes
            - channel: this TwistedChannel
            - method: pika.spec.Basic.Return
            - properties: pika.spec.BasicProperties
            - body: bytes
        """

    def basic_ack(self, delivery_tag: int = ..., multiple: bool = ...):
        """Acknowledge one or more messages. When sent by the client, this
        method acknowledges one or more messages delivered via the Deliver or
        Get-Ok methods. When sent by server, this method acknowledges one or
        more messages published with the Publish method on a channel in
        confirm mode. The acknowledgement can be for a single message or a
        set of messages up to and including a specific message.

        :param integer delivery_tag: int/long The server-assigned delivery tag
        :param bool multiple: If set to True, the delivery tag is treated as
                              "up to and including", so that multiple messages
                              can be acknowledged with a single method. If set
                              to False, the delivery tag refers to a single
                              message. If the multiple field is 1, and the
                              delivery tag is zero, this indicates
                              acknowledgement of all outstanding messages.

        """

    def basic_cancel(self, consumer_tag: str = ...) -> Deferred[Incomplete | Failure | BaseException | None]:
        """This method cancels a consumer. This does not affect already
        delivered messages, but it does mean the server will not send any more
        messages for that consumer. The client may receive an arbitrary number
        of messages in between sending the cancel method and receiving the
        cancel-ok reply. It may also be sent from the server to the client in
        the event of the consumer being unexpectedly cancelled (i.e. cancelled
        for any reason other than the server receiving the corresponding
        basic.cancel from the client). This allows clients to be notified of
        the loss of consumers due to events such as queue deletion.

        This method wraps :meth:`Channel.basic_cancel
        <pika.channel.Channel.basic_cancel>` and closes any deferred queue
        associated with that consumer.

        :param str consumer_tag: Identifier for the consumer
        :returns: Deferred that fires on the Basic.CancelOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def basic_consume(
        self,
        queue,
        auto_ack: bool = ...,
        exclusive: bool = ...,
        consumer_tag: Incomplete | None = ...,
        arguments: Incomplete | None = ...,
    ) -> Deferred[Incomplete | Failure | BaseException]:
        """Consume from a server queue.

        Sends the AMQP 0-9-1 command Basic.Consume to the broker and binds
        messages for the consumer_tag to a
        :class:`ClosableDeferredQueue`. If you do not pass in a
        consumer_tag, one will be automatically generated for you.

        For more information on basic_consume, see:
        Tutorial 2 at http://www.rabbitmq.com/getstarted.html
        http://www.rabbitmq.com/confirms.html
        http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.consume

        :param str queue: The queue to consume from. Use the empty string to
            specify the most recent server-named queue for this channel.
        :param bool auto_ack: if set to True, automatic acknowledgement mode
            will be used (see http://www.rabbitmq.com/confirms.html). This
            corresponds with the 'no_ack' parameter in the basic.consume AMQP
            0.9.1 method
        :param bool exclusive: Don't allow other consumers on the queue
        :param str consumer_tag: Specify your own consumer tag
        :param dict arguments: Custom key/value pair arguments for the consumer
        :returns: Deferred that fires with a tuple
            ``(queue_object, consumer_tag)``. The Deferred will errback with an
            instance of :class:`exceptions.ChannelClosed` if the call fails.
            The queue object is an instance of :class:`ClosableDeferredQueue`,
            where data received from the queue will be stored. Clients should
            use its :meth:`get() <ClosableDeferredQueue.get>` method to fetch
            an individual message, which will return a Deferred firing with a
            namedtuple whose attributes are:
            - channel: this TwistedChannel
            - method: pika.spec.Basic.Deliver
            - properties: pika.spec.BasicProperties
            - body: bytes
        :rtype: Deferred

        """

    def basic_get(self, queue, auto_ack: bool = ...) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Get a single message from the AMQP broker.

        Will return If the queue is empty, it will return None.
        If you want to
        be notified of Basic.GetEmpty, use the Channel.add_callback method
        adding your Basic.GetEmpty callback which should expect only one
        parameter, frame. Due to implementation details, this cannot be called
        a second time until the callback is executed.  For more information on
        basic_get and its parameters, see:

        http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.get

        This method wraps :meth:`Channel.basic_get
        <pika.channel.Channel.basic_get>`.

        :param str queue: The queue from which to get a message. Use the empty
                      string to specify the most recent server-named queue
                      for this channel.
        :param bool auto_ack: Tell the broker to not expect a reply
        :returns: Deferred that fires with a namedtuple whose attributes are:
             - channel: this TwistedChannel
             - method: pika.spec.Basic.GetOk
             - properties: pika.spec.BasicProperties
             - body: bytes
            If the queue is empty, None will be returned.
        :rtype: Deferred
        :raises pika.exceptions.DuplicateGetOkCallback:

        """

    def basic_nack(self, delivery_tag: Incomplete | None = ..., multiple: bool = ..., requeue: bool = ...):
        """This method allows a client to reject one or more incoming messages.
        It can be used to interrupt and cancel large incoming messages, or
        return untreatable messages to their original queue.

        :param integer delivery_tag: int/long The server-assigned delivery tag
        :param bool multiple: If set to True, the delivery tag is treated as
                              "up to and including", so that multiple messages
                              can be acknowledged with a single method. If set
                              to False, the delivery tag refers to a single
                              message. If the multiple field is 1, and the
                              delivery tag is zero, this indicates
                              acknowledgement of all outstanding messages.
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded
                             or dead-lettered.

        """

    def basic_publish(
        self, exchange, routing_key, body, properties: Incomplete | None = ..., mandatory: bool = ...
    ) -> Deferred[Incomplete | Failure | BaseException]:
        """Publish to the channel with the given exchange, routing key and body.

        This method wraps :meth:`Channel.basic_publish
        <pika.channel.Channel.basic_publish>`, but makes sure the channel is
        not closed before publishing.

        For more information on basic_publish and what the parameters do, see:

        http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.publish

        :param str exchange: The exchange to publish to
        :param str routing_key: The routing key to bind on
        :param bytes body: The message body
        :param pika.spec.BasicProperties properties: Basic.properties
        :param bool mandatory: The mandatory flag
        :returns: A Deferred that fires with the result of the channel's
            basic_publish.
        :rtype: Deferred
        :raises UnroutableError: raised when a message published in
            publisher-acknowledgments mode (see
            `BlockingChannel.confirm_delivery`) is returned via `Basic.Return`
            followed by `Basic.Ack`.
        :raises NackError: raised when a message published in
            publisher-acknowledgements mode is Nack'ed by the broker. See
            `BlockingChannel.confirm_delivery`.

        """

    def basic_qos(
        self, prefetch_size: int = ..., prefetch_count: int = ..., global_qos: bool = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Specify quality of service. This method requests a specific quality
        of service. The QoS can be specified for the current channel or for all
        channels on the connection. The client can request that messages be
        sent in advance so that when the client finishes processing a message,
        the following message is already held locally, rather than needing to
        be sent down the channel. Prefetching gives a performance improvement.

        :param int prefetch_size:  This field specifies the prefetch window
                                   size. The server will send a message in
                                   advance if it is equal to or smaller in size
                                   than the available prefetch size (and also
                                   falls into other prefetch limits). May be
                                   set to zero, meaning "no specific limit",
                                   although other prefetch limits may still
                                   apply. The prefetch-size is ignored by
                                   consumers who have enabled the no-ack
                                   option.
        :param int prefetch_count: Specifies a prefetch window in terms of
                                   whole messages. This field may be used in
                                   combination with the prefetch-size field; a
                                   message will only be sent in advance if both
                                   prefetch windows (and those at the channel
                                   and connection level) allow it. The
                                   prefetch-count is ignored by consumers who
                                   have enabled the no-ack option.
        :param bool global_qos:    Should the QoS apply to all channels on the
                                   connection.
        :returns: Deferred that fires on the Basic.QosOk response
        :rtype: Deferred

        """

    def basic_reject(self, delivery_tag, requeue: bool = ...):
        """Reject an incoming message. This method allows a client to reject a
        message. It can be used to interrupt and cancel large incoming
        messages, or return untreatable messages to their original queue.

        :param integer delivery_tag: int/long The server-assigned delivery tag
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded
                             or dead-lettered.
        :raises: TypeError

        """

    def basic_recover(self, requeue: bool = ...) -> Deferred[Incomplete | Failure | BaseException | None]:
        """This method asks the server to redeliver all unacknowledged messages
        on a specified channel. Zero or more messages may be redelivered. This
        method replaces the asynchronous Recover.

        :param bool requeue: If False, the message will be redelivered to the
                             original recipient. If True, the server will
                             attempt to requeue the message, potentially then
                             delivering it to an alternative subscriber.
        :returns: Deferred that fires on the Basic.RecoverOk response
        :rtype: Deferred

        """

    def close(self, reply_code: int = ..., reply_text: str = ...):
        """Invoke a graceful shutdown of the channel with the AMQP Broker.

        If channel is OPENING, transition to CLOSING and suppress the incoming
        Channel.OpenOk, if any.

        :param int reply_code: The reason code to send to broker
        :param str reply_text: The reason text to send to broker

        :raises ChannelWrongStateError: if channel is closed or closing

        """

    def confirm_delivery(self) -> Deferred[Incomplete | None]:
        """Turn on Confirm mode in the channel. Pass in a callback to be
        notified by the Broker when a message has been confirmed as received or
        rejected (Basic.Ack, Basic.Nack) from the broker to the publisher.

        For more information see:
            http://www.rabbitmq.com/confirms.html#publisher-confirms

        :returns: Deferred that fires on the Confirm.SelectOk response
        :rtype: Deferred

        """

    def exchange_bind(
        self, destination, source, routing_key: str = ..., arguments: Incomplete | None = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Bind an exchange to another exchange.

        :param str destination: The destination exchange to bind
        :param str source: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding
        :raises ValueError:
        :returns: Deferred that fires on the Exchange.BindOk response
        :rtype: Deferred

        """

    def exchange_declare(
        self,
        exchange,
        exchange_type=...,
        passive: bool = ...,
        durable: bool = ...,
        auto_delete: bool = ...,
        internal: bool = ...,
        arguments: Incomplete | None = ...,
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """This method creates an exchange if it does not already exist, and if
        the exchange exists, verifies that it is of the correct and expected
        class.

        If passive set, the server will reply with Declare-Ok if the exchange
        already exists with the same name, and raise an error if not and if the
        exchange does not already exist, the server MUST raise a channel
        exception with reply code 404 (not found).

        :param str exchange: The exchange name consists of a non-empty sequence
            of these characters: letters, digits, hyphen, underscore, period,
            or colon
        :param str exchange_type: The exchange type to use
        :param bool passive: Perform a declare or just check to see if it
            exists
        :param bool durable: Survive a reboot of RabbitMQ
        :param bool auto_delete: Remove when no more queues are bound to it
        :param bool internal: Can only be published to by other exchanges
        :param dict arguments: Custom key/value pair arguments for the exchange
        :returns: Deferred that fires on the Exchange.DeclareOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def exchange_delete(
        self, exchange: Incomplete | None = ..., if_unused: bool = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Delete the exchange.

        :param str exchange: The exchange name
        :param bool if_unused: only delete if the exchange is unused
        :returns: Deferred that fires on the Exchange.DeleteOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def exchange_unbind(
        self,
        destination: Incomplete | None = ...,
        source: Incomplete | None = ...,
        routing_key: str = ...,
        arguments: Incomplete | None = ...,
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Unbind an exchange from another exchange.

        :param str destination: The destination exchange to unbind
        :param str source: The source exchange to unbind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding
        :returns: Deferred that fires on the Exchange.UnbindOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def flow(self, active) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Turn Channel flow control off and on.

        Returns a Deferred that will fire with a bool indicating the channel
        flow state. For more information, please reference:

        http://www.rabbitmq.com/amqp-0-9-1-reference.html#channel.flow

        :param bool active: Turn flow on or off
        :returns: Deferred that fires with the channel flow state
        :rtype: Deferred
        :raises ValueError:

        """

    def open(self):
        """Open the channel"""

    def queue_bind(
        self, queue, exchange, routing_key: Incomplete | None = ..., arguments: Incomplete | None = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Bind the queue to the specified exchange

        :param str queue: The queue to bind to the exchange
        :param str exchange: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding
        :returns: Deferred that fires on the Queue.BindOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def queue_declare(
        self,
        queue,
        passive: bool = ...,
        durable: bool = ...,
        exclusive: bool = ...,
        auto_delete: bool = ...,
        arguments: Incomplete | None = ...,
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Declare queue, create if needed. This method creates or checks a
        queue. When creating a new queue the client can specify various
        properties that control the durability of the queue and its contents,
        and the level of sharing for the queue.

        Use an empty string as the queue name for the broker to auto-generate
        one

        :param str queue: The queue name; if empty string, the broker will
            create a unique queue name
        :param bool passive: Only check to see if the queue exists
        :param bool durable: Survive reboots of the broker
        :param bool exclusive: Only allow access by the current connection
        :param bool auto_delete: Delete after consumer cancels or disconnects
        :param dict arguments: Custom key/value arguments for the queue
        :returns: Deferred that fires on the Queue.DeclareOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def queue_delete(
        self, queue, if_unused: bool = ..., if_empty: bool = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Delete a queue from the broker.


        This method wraps :meth:`Channel.queue_delete
        <pika.channel.Channel.queue_delete>`, and removes the reference to the
        queue object after it gets deleted on the server.

        :param str queue: The queue to delete
        :param bool if_unused: only delete if it's unused
        :param bool if_empty: only delete if the queue is empty
        :returns: Deferred that fires on the Queue.DeleteOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def queue_purge(self, queue) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Purge all of the messages from the specified queue

        :param str queue: The queue to purge
        :returns: Deferred that fires on the Queue.PurgeOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def queue_unbind(
        self, queue, exchange: Incomplete | None = ..., routing_key: Incomplete | None = ..., arguments: Incomplete | None = ...
    ) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Unbind a queue from an exchange.

        :param str queue: The queue to unbind from the exchange
        :param str exchange: The source exchange to bind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding
        :returns: Deferred that fires on the Queue.UnbindOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def tx_commit(self) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Commit a transaction.

        :returns: Deferred that fires on the Tx.CommitOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def tx_rollback(self) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Rollback a transaction.

        :returns: Deferred that fires on the Tx.RollbackOk response
        :rtype: Deferred
        :raises ValueError:

        """

    def tx_select(self) -> Deferred[Incomplete | Failure | BaseException | None]:
        """Select standard transaction mode. This method sets the channel to use
        standard transactions. The client must use this method at least once on
        a channel before using the Commit or Rollback methods.

        :returns: Deferred that fires on the Tx.SelectOk response
        :rtype: Deferred
        :raises ValueError:

        """

class _TwistedConnectionAdapter(pika.connection.Connection):
    """A Twisted-specific implementation of a Pika Connection.

    NOTE: since `base_connection.BaseConnection`'s primary responsibility is
    management of the transport, we use `pika.connection.Connection` directly
    as our base class because this adapter uses a different transport
    management strategy.

    """

    def __init__(self, parameters, on_open_callback, on_open_error_callback, on_close_callback, custom_reactor) -> None: ...
    def connection_made(self, transport: ITransport) -> None:
        """Introduces transport to protocol after transport is connected.

        :param twisted.internet.interfaces.ITransport transport:
        :raises Exception: Exception-based exception on error

        """

    def connection_lost(self, error: Exception) -> None:
        """Called upon loss or closing of TCP connection.

        NOTE: `connection_made()` and `connection_lost()` are each called just
        once and in that order. All other callbacks are called between them.

        :param Failure: A Twisted Failure instance wrapping an exception.

        """

    def data_received(self, data) -> None:
        """Called to deliver incoming data from the server to the protocol.

        :param data: Non-empty data bytes.
        :raises Exception: Exception-based exception on error

        """

class TwistedProtocolConnection(Protocol):  # pyright: ignore[reportUntypedBaseClass]
    """A Pika-specific implementation of a Twisted Protocol. Allows using
    Twisted's non-blocking connectTCP/connectSSL methods for connecting to the
    server.

    TwistedProtocolConnection objects have a `ready` instance variable that's a
    Deferred which fires when the connection is ready to be used (the initial
    AMQP handshaking has been done). You *have* to wait for this Deferred to
    fire before requesting a channel.

    Once the connection is ready, you will be able to use the `closed` instance
    variable: a Deferred which fires when the connection is closed.

    Since it's Twisted handling connection establishing it does not accept
    connect callbacks, you have to implement that within Twisted. Also remember
    that the host, port and ssl values of the connection parameters are ignored
    because, yet again, it's Twisted who manages the connection.

    """

    ready: Deferred[None] | None
    closed: Deferred[None] | Failure | BaseException | None
    def __init__(self, parameters: Incomplete | None = ..., custom_reactor: Incomplete | None = ...) -> None: ...
    def channel(self, channel_number: Incomplete | None = ...):
        """Create a new channel with the next available channel number or pass
        in a channel number to use. Must be non-zero if you would like to
        specify but it is recommended that you let Pika manage the channel
        numbers.

        :param int channel_number: The channel number to use, defaults to the
                                   next available.
        :returns: a Deferred that fires with an instance of a wrapper around
            the Pika Channel class.
        :rtype: Deferred

        """

    @property
    def is_open(self): ...
    @property
    def is_closed(self): ...
    def close(self, reply_code: int = ..., reply_text: str = ...) -> Deferred[None] | Failure | BaseException | None: ...
    def dataReceived(self, data) -> None: ...
    def connectionLost(self, reason: Failure | BaseException = ...) -> None: ...
    def makeConnection(self, transport: ITransport) -> None: ...
    def connectionReady(self):
        """This method will be called when the underlying connection is ready."""

class _TimerHandle(nbio_interface.AbstractTimerReference):
    """This module's adaptation of `nbio_interface.AbstractTimerReference`."""

    def __init__(self, handle: DelayedCall) -> None:
        """

        :param twisted.internet.base.DelayedCall handle:
        """

    def cancel(self) -> None: ...
