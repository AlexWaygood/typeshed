from logging import Logger
from typing import Final

from aws_xray_sdk.core.models.entity import Entity

log: Logger
PROTOCOL_HEADER: Final[str]
PROTOCOL_DELIMITER: Final[str]
DEFAULT_DAEMON_ADDRESS: Final[str]

class UDPEmitter:
    """
    The default emitter the X-Ray recorder uses to send segments/subsegments
    to the X-Ray daemon over UDP using a non-blocking socket. If there is an
    exception on the actual data transfer between the socket and the daemon,
    it logs the exception and continue.
    """

    def __init__(self, daemon_address: str = "127.0.0.1:2000") -> None: ...
    def send_entity(self, entity: Entity) -> None:
        """
        Serializes a segment/subsegment and sends it to the X-Ray daemon
        over UDP. By default it doesn't retry on failures.

        :param entity: a trace entity to send to the X-Ray daemon
        """

    def set_daemon_address(self, address: str | None) -> None:
        """
        Set up UDP ip and port from the raw daemon address
        string using ``DaemonConfig`` class utlities.
        """

    @property
    def ip(self): ...
    @property
    def port(self): ...
