import logging
from _typeshed import ReadableBuffer

from serial.serialutil import SerialBase

LOGGER_LEVELS: dict[str, int]
POLL_TIMEOUT: float

class Serial(SerialBase):
    """Serial port implementation for plain sockets."""

    logger: logging.Logger | None
    def open(self) -> None:
        """Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """

    def from_url(self, url: str) -> tuple[str, int]:
        """extract host and port from an URL string"""

    @property
    def in_waiting(self) -> int:
        """Return the number of bytes currently in the input buffer."""

    def read(self, size: int = 1) -> bytes:
        """Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """

    def write(self, b: ReadableBuffer, /) -> int | None:
        """Output the given byte string over the serial port. Can block if the
        connection is blocked. May raise SerialException if the connection is
        closed.
        """

    def reset_input_buffer(self) -> None:
        """Clear input buffer, discarding all that is in the buffer."""

    def reset_output_buffer(self) -> None:
        """Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """

    @property
    def cts(self) -> bool:
        """Read terminal status line: Clear To Send"""

    @property
    def dsr(self) -> bool:
        """Read terminal status line: Data Set Ready"""

    @property
    def ri(self) -> bool:
        """Read terminal status line: Ring Indicator"""

    @property
    def cd(self) -> bool:
        """Read terminal status line: Carrier Detect"""
