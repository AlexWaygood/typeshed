import sys
from _typeshed import ReadableBuffer
from typing_extensions import Never

from serial.serialutil import SerialBase

class PlatformSpecificBase:
    BAUDRATE_CONSTANTS: dict[int, int]
    def set_low_latency_mode(self, low_latency_settings: bool) -> None: ...

CMSPAR: int
if sys.platform == "linux":
    TCGETS2: int
    TCSETS2: int
    BOTHER: int
    TIOCGRS485: int
    TIOCSRS485: int
    SER_RS485_ENABLED: int
    SER_RS485_RTS_ON_SEND: int
    SER_RS485_RTS_AFTER_SEND: int
    SER_RS485_RX_DURING_TX: int

    class PlatformSpecific(PlatformSpecificBase): ...

elif sys.platform == "cygwin":
    class PlatformSpecific(PlatformSpecificBase): ...

elif sys.platform == "darwin":
    IOSSIOSPEED: int

    class PlatformSpecific(PlatformSpecificBase):
        osx_version: list[str]
        TIOCSBRK: int
        TIOCCBRK: int

else:
    class PlatformSpecific(PlatformSpecificBase): ...

TIOCMGET: int
TIOCMBIS: int
TIOCMBIC: int
TIOCMSET: int
TIOCM_DTR: int
TIOCM_RTS: int
TIOCM_CTS: int
TIOCM_CAR: int
TIOCM_RNG: int
TIOCM_DSR: int
TIOCM_CD: int
TIOCM_RI: int
TIOCINQ: int
TIOCOUTQ: int
TIOCM_zero_str: bytes
TIOCM_RTS_str: bytes
TIOCM_DTR_str: bytes
TIOCSBRK: int
TIOCCBRK: int

class Serial(SerialBase, PlatformSpecific):
    """Serial port class POSIX implementation. Serial port configuration is
    done with termios and fcntl. Runs on Linux and many other Un*x like
    systems.
    """

    fd: int | None
    pipe_abort_read_w: int | None
    pipe_abort_read_r: int | None
    pipe_abort_write_w: int | None
    pipe_abort_write_r: int | None
    def open(self) -> None:
        """Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """

    @property
    def in_waiting(self) -> int:
        """Return the number of bytes currently in the input buffer."""

    def read(self, size: int = 1) -> bytes:
        """Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """

    def cancel_read(self) -> None: ...
    def cancel_write(self) -> None: ...
    def write(self, b: ReadableBuffer, /) -> int | None:
        """Output the given byte string over the serial port."""

    def reset_input_buffer(self) -> None:
        """Clear input buffer, discarding all that is in the buffer."""

    def reset_output_buffer(self) -> None:
        """Clear output buffer, aborting the current output and discarding all
        that is in the buffer.
        """

    def send_break(self, duration: float = ...) -> None:
        """Send break condition. Timed, returns to idle state after given
        duration.
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

    @property
    def out_waiting(self) -> int:
        """Return the number of bytes currently in the output buffer."""

    def set_input_flow_control(self, enable: bool = ...) -> None:
        """Manually control flow - when software flow control is enabled.
        This will send XON (true) or XOFF (false) to the other device.
        WARNING: this function is not portable to different platforms!
        """

    def set_output_flow_control(self, enable: bool = ...) -> None:
        """Manually control flow of outgoing data - when hardware or software flow
        control is enabled.
        WARNING: this function is not portable to different platforms!
        """

    def nonblocking(self) -> None:
        """DEPRECATED - has no use"""

class PosixPollSerial(Serial):
    """Poll based read implementation. Not all systems support poll properly.
    However this one has better handling of errors, such as a device
    disconnecting while it's in use (e.g. USB-serial unplugged).
    """

class VTIMESerial(Serial):
    """Implement timeout using vtime of tty device instead of using select.
    This means that no inter character timeout can be specified and that
    the error handling is degraded.

    Overall timeout is disabled when inter-character timeout is used.

    Note that this implementation does NOT support cancel_read(), it will
    just ignore that.
    """

    @property
    def cancel_read(self) -> Never: ...
