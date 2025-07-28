"""Handle AMQP Heartbeats"""

from logging import Logger

LOGGER: Logger

class HeartbeatChecker:
    """Sends heartbeats to the broker. The provided timeout is used to
    determine if the connection is stale - no received heartbeats or
    other activity will close the connection. See the parameter list for more
    details.

    """

    def __init__(self, connection, timeout) -> None:
        """Create an object that will check for activity on the provided
        connection as well as receive heartbeat frames from the broker. The
        timeout parameter defines a window within which this activity must
        happen. If not, the connection is considered dead and closed.

        The value passed for timeout is also used to calculate an interval
        at which a heartbeat frame is sent to the broker. The interval is
        equal to the timeout value divided by two.

        :param pika.connection.Connection: Connection object
        :param int timeout: Connection idle timeout. If no activity occurs on the
                            connection nor heartbeat frames received during the
                            timeout window the connection will be closed. The
                            interval used to send heartbeats is calculated from
                            this value by dividing it by two.

        """

    @property
    def bytes_received_on_connection(self):
        """Return the number of bytes received by the connection bytes object.

        :rtype int

        """

    @property
    def connection_is_idle(self):
        """Returns true if the byte count hasn't changed in enough intervals
        to trip the max idle threshold.

        """

    def received(self) -> None:
        """Called when a heartbeat is received"""

    def stop(self) -> None:
        """Stop the heartbeat checker"""
