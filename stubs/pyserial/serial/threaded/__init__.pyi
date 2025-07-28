"""Support threading with serial ports."""

import threading
from _typeshed import ReadableBuffer
from collections.abc import Callable
from types import TracebackType
from typing import Generic, TypeVar
from typing_extensions import Self

from serial import Serial

_P = TypeVar("_P", bound=Protocol, default=Protocol)

class Protocol:
    """Protocol as used by the ReaderThread. This base class provides empty
    implementations of all methods.
    """

    def connection_made(self, transport: ReaderThread[Self]) -> None:
        """Called when reader thread is started"""

    def data_received(self, data: bytes) -> None:
        """Called with snippets received from the serial port"""

    def connection_lost(self, exc: BaseException | None) -> None:
        """Called when the serial port is closed or the reader loop terminated
        otherwise.
        """

class Packetizer(Protocol):
    """
    Read binary packets from serial port. Packets are expected to be terminated
    with a TERMINATOR byte (null byte by default).

    The class also keeps track of the transport.
    """

    TERMINATOR: bytes
    buffer: bytearray
    transport: ReaderThread[Self] | None
    def handle_packet(self, packet: bytes) -> None:
        """Process packets - to be overridden by subclassing"""

class FramedPacket(Protocol):
    """
    Read binary packets. Packets are expected to have a start and stop marker.

    The class also keeps track of the transport.
    """

    START: bytes
    STOP: bytes
    packet: bytearray
    in_packet: bool
    transport: ReaderThread[Self] | None
    def handle_packet(self, packet: bytes) -> None:
        """Process packets - to be overridden by subclassing"""

    def handle_out_of_packet_data(self, data: bytes) -> None:
        """Process data that is received outside of packets"""

class LineReader(Packetizer):
    """
    Read and write (Unicode) lines from/to serial port.
    The encoding is applied.
    """

    ENCODING: str
    UNICODE_HANDLING: str
    def handle_line(self, line: str) -> None:
        """Process one line - to be overridden by subclassing"""

    def write_line(self, text: str) -> None:
        """
        Write text to the transport. ``text`` is a Unicode string and the encoding
        is applied before sending ans also the newline is append.
        """

class ReaderThread(threading.Thread, Generic[_P]):
    """Implement a serial port read loop and dispatch to a Protocol instance (like
    the asyncio.Protocol) but do it with threads.

    Calls to close() will close the serial port but it is also possible to just
    stop() this thread and continue the serial port instance otherwise.
    """

    serial: Serial
    protocol_factory: Callable[[], _P]
    alive: bool
    protocol: _P
    def __init__(self, serial_instance: Serial, protocol_factory: Callable[[], _P]) -> None:
        """Initialize thread.

        Note that the serial_instance' timeout is set to one second!
        Other settings are not changed.
        """

    def stop(self) -> None:
        """Stop the reader thread"""

    def write(self, data: ReadableBuffer) -> int:
        """Thread safe writing (uses lock)"""

    def close(self) -> None:
        """Close the serial port and exit reader thread (uses lock)"""

    def connect(self) -> tuple[Self, _P]:
        """
        Wait until connection is set up and return the transport and protocol
        instances.
        """

    def __enter__(self) -> _P:
        """Enter context handler. May raise RuntimeError in case the connection
        could not be created.
        """

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None, /
    ) -> None:
        """Leave context: close port"""
