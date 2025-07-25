"""Pika specific exceptions"""

from collections.abc import Sequence

from pika.adapters.blocking_connection import ReturnedMessage

class AMQPError(Exception): ...
class AMQPConnectionError(AMQPError): ...

class ConnectionOpenAborted(AMQPConnectionError):
    """Client closed connection while opening."""

class StreamLostError(AMQPConnectionError):
    """Stream (TCP) connection lost."""

class IncompatibleProtocolError(AMQPConnectionError): ...
class AuthenticationError(AMQPConnectionError): ...
class ProbableAuthenticationError(AMQPConnectionError): ...
class ProbableAccessDeniedError(AMQPConnectionError): ...
class NoFreeChannels(AMQPConnectionError): ...

class ConnectionWrongStateError(AMQPConnectionError):
    """Connection is in wrong state for the requested operation."""

class ConnectionClosed(AMQPConnectionError):
    def __init__(self, reply_code: int, reply_text: str) -> None:
        """

        :param int reply_code: reply-code that was used in user's or broker's
            `Connection.Close` method. NEW in v1.0.0
        :param str reply_text: reply-text that was used in user's or broker's
            `Connection.Close` method. Human-readable string corresponding to
            `reply_code`. NEW in v1.0.0
        """

    @property
    def reply_code(self) -> int:
        """NEW in v1.0.0
        :rtype: int

        """

    @property
    def reply_text(self) -> str:
        """NEW in v1.0.0
        :rtype: str

        """

class ConnectionClosedByBroker(ConnectionClosed):
    """Connection.Close from broker."""

class ConnectionClosedByClient(ConnectionClosed):
    """Connection was closed at request of Pika client."""

class ConnectionBlockedTimeout(AMQPConnectionError):
    """RabbitMQ-specific: timed out waiting for connection.unblocked."""

class AMQPHeartbeatTimeout(AMQPConnectionError):
    """Connection was dropped as result of heartbeat timeout."""

class AMQPChannelError(AMQPError): ...

class ChannelWrongStateError(AMQPChannelError):
    """Channel is in wrong state for the requested operation."""

class ChannelClosed(AMQPChannelError):
    """The channel closed by client or by broker"""

    def __init__(self, reply_code: int, reply_text: str) -> None:
        """

        :param int reply_code: reply-code that was used in user's or broker's
            `Channel.Close` method. One of the AMQP-defined Channel Errors.
            NEW in v1.0.0
        :param str reply_text: reply-text that was used in user's or broker's
            `Channel.Close` method. Human-readable string corresponding to
            `reply_code`;
            NEW in v1.0.0

        """

    @property
    def reply_code(self) -> int:
        """NEW in v1.0.0
        :rtype: int

        """

    @property
    def reply_text(self) -> str:
        """NEW in v1.0.0
        :rtype: str

        """

class ChannelClosedByBroker(ChannelClosed):
    """`Channel.Close` from broker; may be passed as reason to channel's
    on-closed callback of non-blocking connection adapters or raised by
    `BlockingConnection`.

    NEW in v1.0.0
    """

class ChannelClosedByClient(ChannelClosed):
    """Channel closed by client upon receipt of `Channel.CloseOk`; may be passed
    as reason to channel's on-closed callback of non-blocking connection
    adapters, but not raised by `BlockingConnection`.

    NEW in v1.0.0
    """

class DuplicateConsumerTag(AMQPChannelError): ...
class ConsumerCancelled(AMQPChannelError): ...

class UnroutableError(AMQPChannelError):
    """Exception containing one or more unroutable messages returned by broker
    via Basic.Return.

    Used by BlockingChannel.

    In publisher-acknowledgements mode, this is raised upon receipt of Basic.Ack
    from broker; in the event of Basic.Nack from broker, `NackError` is raised
    instead
    """

    messages: Sequence[ReturnedMessage]
    def __init__(self, messages: Sequence[ReturnedMessage]) -> None:
        """
        :param sequence(blocking_connection.ReturnedMessage) messages: Sequence
            of returned unroutable messages
        """

class NackError(AMQPChannelError):
    """This exception is raised when a message published in
    publisher-acknowledgements mode is Nack'ed by the broker.

    Used by BlockingChannel.
    """

    messages: Sequence[ReturnedMessage]
    def __init__(self, messages: Sequence[ReturnedMessage]) -> None:
        """
        :param sequence(blocking_connection.ReturnedMessage) messages: Sequence
            of returned unroutable messages
        """

class InvalidChannelNumber(AMQPError): ...
class ProtocolSyntaxError(AMQPError): ...
class UnexpectedFrameError(ProtocolSyntaxError): ...
class ProtocolVersionMismatch(ProtocolSyntaxError): ...
class BodyTooLongError(ProtocolSyntaxError): ...
class InvalidFrameError(ProtocolSyntaxError): ...
class InvalidFieldTypeException(ProtocolSyntaxError): ...
class UnsupportedAMQPFieldException(ProtocolSyntaxError): ...
class MethodNotImplemented(AMQPError): ...
class ChannelError(Exception): ...

class ReentrancyError(Exception):
    """The requested operation would result in unsupported recursion or
    reentrancy.

    Used by BlockingConnection/BlockingChannel

    """

class ShortStringTooLong(AMQPError): ...
class DuplicateGetOkCallback(ChannelError): ...
