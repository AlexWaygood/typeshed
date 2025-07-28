import io
from _typeshed import ReadableBuffer, WriteableBuffer
from abc import abstractmethod
from collections.abc import Callable, Generator
from typing import Any, Final

from serial.rs485 import RS485Settings

XON: Final = b"\x11"
XOFF: Final = b"\x13"
CR: Final = b"\r"
LF: Final = b"\n"
PARITY_NONE: Final = "N"
PARITY_EVEN: Final = "E"
PARITY_ODD: Final = "O"
PARITY_MARK: Final = "M"
PARITY_SPACE: Final = "S"
STOPBITS_ONE: Final = 1
STOPBITS_ONE_POINT_FIVE: float
STOPBITS_TWO: Final = 2
FIVEBITS: Final = 5
SIXBITS: Final = 6
SEVENBITS: Final = 7
EIGHTBITS: Final = 8
PARITY_NAMES: dict[str, str]

class SerialException(OSError):
    """Base class for serial port related exceptions."""

class SerialTimeoutException(SerialException):
    """Write timeouts give an exception"""

class PortNotOpenError(SerialException):
    """Port is not open"""

    def __init__(self) -> None: ...

class Timeout:
    """Abstraction for timeout operations. Using time.monotonic() if available
    or time.time() in all other cases.

    The class can also be initialized with 0 or None, in order to support
    non-blocking and fully blocking I/O operations. The attributes
    is_non_blocking and is_infinite are set accordingly.
    """

    TIME: Callable[[], float]
    is_infinite: bool
    is_non_blocking: bool
    duration: float
    target_time: float
    def __init__(self, duration: float) -> None:
        """Initialize a timeout with given duration"""

    def expired(self) -> bool:
        """Return a boolean, telling if the timeout has expired"""

    def time_left(self) -> float:
        """Return how many seconds are left until the timeout expires"""

    def restart(self, duration: float) -> None:
        """Restart a timeout, only supported if a timeout was already set up
        before.
        """

class SerialBase(io.RawIOBase):
    """Serial port base class. Provides __init__ function and properties to
    get/set port settings.
    """

    BAUDRATES: tuple[int, ...]
    BYTESIZES: tuple[int, ...]
    PARITIES: tuple[str, ...]
    STOPBITS: tuple[int, float, int]
    is_open: bool
    portstr: str | None
    name: str | None
    def __init__(
        self,
        port: str | None = None,
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: float = 1,
        timeout: float | None = None,
        xonxoff: bool = False,
        rtscts: bool = False,
        write_timeout: float | None = None,
        dsrdtr: bool = False,
        inter_byte_timeout: float | None = None,
        exclusive: bool | None = None,
    ) -> None:
        """Initialize comm port object. If a "port" is given, then the port will be
        opened immediately. Otherwise a Serial port object in closed state
        is returned.
        """
    # Return type:
    # ------------
    # `io.RawIOBase`, the super class, declares the return type of read as `-> bytes | None`.
    # `SerialBase` does not define `read` at runtime but REQUIRES subclasses to implement it and
    # require it to return `bytes`.
    # Abstract:
    # ---------
    # `io.RawIOBase` implements `read` in terms of `readinto`. `SerialBase` implements `readinto`
    # in terms of `read`. If subclasses do not implement `read`, any call to `read` or `read_into`
    # will fail at runtime with a `RecursionError`.
    @abstractmethod
    def read(self, size: int = -1, /) -> bytes: ...
    @abstractmethod
    def write(self, b: ReadableBuffer, /) -> int | None: ...
    @property
    def port(self) -> str | None:
        """Get the current port setting. The value that was passed on init or using
        setPort() is passed back.
        """

    @port.setter
    def port(self, port: str | None) -> None: ...
    @property
    def baudrate(self) -> int:
        """Get the current baud rate setting."""

    @baudrate.setter
    def baudrate(self, baudrate: int) -> None: ...
    @property
    def bytesize(self) -> int:
        """Get the current byte size setting."""

    @bytesize.setter
    def bytesize(self, bytesize: int) -> None: ...
    @property
    def exclusive(self) -> bool | None:
        """Get the current exclusive access setting."""

    @exclusive.setter
    def exclusive(self, exclusive: bool | None) -> None: ...
    @property
    def parity(self) -> str:
        """Get the current parity setting."""

    @parity.setter
    def parity(self, parity: str) -> None: ...
    @property
    def stopbits(self) -> float:
        """Get the current stop bits setting."""

    @stopbits.setter
    def stopbits(self, stopbits: float) -> None: ...
    @property
    def timeout(self) -> float | None:
        """Get the current timeout setting."""

    @timeout.setter
    def timeout(self, timeout: float | None) -> None: ...
    @property
    def write_timeout(self) -> float | None:
        """Get the current timeout setting."""

    @write_timeout.setter
    def write_timeout(self, timeout: float | None) -> None: ...
    @property
    def inter_byte_timeout(self) -> float | None:
        """Get the current inter-character timeout setting."""

    @inter_byte_timeout.setter
    def inter_byte_timeout(self, ic_timeout: float | None) -> None: ...
    @property
    def xonxoff(self) -> bool:
        """Get the current XON/XOFF setting."""

    @xonxoff.setter
    def xonxoff(self, xonxoff: bool) -> None: ...
    @property
    def rtscts(self) -> bool:
        """Get the current RTS/CTS flow control setting."""

    @rtscts.setter
    def rtscts(self, rtscts: bool) -> None: ...
    @property
    def dsrdtr(self) -> bool:
        """Get the current DSR/DTR flow control setting."""

    @dsrdtr.setter
    def dsrdtr(self, dsrdtr: bool | None = ...) -> None: ...
    @property
    def rts(self) -> bool: ...
    @rts.setter
    def rts(self, value: bool) -> None: ...
    @property
    def dtr(self) -> bool: ...
    @dtr.setter
    def dtr(self, value: bool) -> None: ...
    @property
    def break_condition(self) -> bool: ...
    @break_condition.setter
    def break_condition(self, value: bool) -> None: ...
    @property
    def rs485_mode(self) -> RS485Settings | None:
        """Enable RS485 mode and apply new settings, set to None to disable.
        See serial.rs485.RS485Settings for more info about the value.
        """

    @rs485_mode.setter
    def rs485_mode(self, rs485_settings: RS485Settings | None) -> None: ...
    def get_settings(self) -> dict[str, Any]:
        """Get current port settings as a dictionary. For use with
        apply_settings().
        """

    def apply_settings(self, d: dict[str, Any]) -> None:
        """Apply stored settings from a dictionary returned from
        get_settings(). It's allowed to delete keys from the dictionary. These
        values will simply left unchanged.
        """

    def readinto(self, buffer: WriteableBuffer, /) -> int: ...  # returns int unlike `io.RawIOBase`
    def send_break(self, duration: float = 0.25) -> None:
        """Send break condition. Timed, returns to idle state after given
        duration.
        """

    def read_all(self) -> bytes | None:
        """Read all bytes currently available in the buffer of the OS."""

    def read_until(self, expected: bytes = b"\n", size: int | None = None) -> bytes:
        """Read until an expected sequence is found ('
        ' by default), the size
                is exceeded or until timeout occurs.
        """

    def iread_until(self, expected: bytes = ..., size: int | None = ...) -> Generator[bytes, None, None]:
        """Read lines, implemented as generator. It will raise StopIteration on
        timeout (empty read).
        """
