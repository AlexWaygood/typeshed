from collections.abc import Sequence
from socket import _RetAddress, socket
from threading import Condition, Lock

from waitress.adjustments import Adjustments
from waitress.buffers import OverflowableBuffer
from waitress.parser import HTTPRequestParser
from waitress.server import BaseWSGIServer
from waitress.task import ErrorTask, WSGITask

from . import wasyncore
from .wasyncore import _SocketMap

class ClientDisconnected(Exception):
    """Raised when attempting to write to a closed socket."""

class HTTPChannel(wasyncore.dispatcher):
    """
    Setting self.requests = [somerequest] prevents more requests from being
    received until the out buffers have been flushed.

    Setting self.requests = [] allows more requests to be received.
    """

    task_class: type[WSGITask]
    error_task_class: type[ErrorTask]
    parser_class: type[HTTPRequestParser]
    request: HTTPRequestParser | None
    last_activity: float
    will_close: bool
    close_when_flushed: bool
    requests: Sequence[HTTPRequestParser]
    sent_continue: bool
    total_outbufs_len: int
    current_outbuf_count: int
    server: BaseWSGIServer
    adj: Adjustments
    outbufs: Sequence[OverflowableBuffer]
    creation_time: float
    sendbuf_len: int
    task_lock: Lock
    outbuf_lock: Condition
    connected: bool
    addr: _RetAddress
    def __init__(
        self, server: BaseWSGIServer, sock: socket, addr: _RetAddress, adj: Adjustments, map: _SocketMap | None = None
    ) -> None: ...
    def check_client_disconnected(self) -> None:
        """
        This method is inserted into the environment of any created task so it
        may occasionally check if the client has disconnected and interrupt
        execution.
        """

    def writable(self) -> bool: ...
    def handle_write(self) -> None: ...
    def readable(self) -> bool: ...
    def handle_read(self) -> None: ...
    def send_continue(self) -> None:
        """
        Send a 100-Continue header to the client. This is either called from
        receive (if no requests are running and the client expects it) or at
        the end of service (if no more requests are queued and a request has
        been read partially that expects it).
        """

    def received(self, data: bytes) -> bool:
        """
        Receives input asynchronously and assigns one or more requests to the
        channel.
        """

    def handle_close(self) -> None: ...
    def add_channel(self, map: _SocketMap | None = None) -> None:
        """See wasyncore.dispatcher

        This hook keeps track of opened channels.
        """

    def del_channel(self, map: _SocketMap | None = None) -> None:
        """See wasyncore.dispatcher

        This hook keeps track of closed channels.
        """

    def write_soon(self, data: bytes) -> int: ...
    def service(self) -> None:
        """Execute one request. If there are more, we add another task to the
        server at the end.
        """

    def cancel(self) -> None:
        """Cancels all pending / active requests"""
