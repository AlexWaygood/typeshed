import codecs
import sys
import threading
from _typeshed import SupportsFlush, SupportsWrite, Unused
from collections.abc import Iterable
from typing import Any, Protocol, TypeVar, type_check_only
from typing_extensions import Self

from serial import Serial

_AnyStrT_contra = TypeVar("_AnyStrT_contra", contravariant=True)

@type_check_only
class _SupportsWriteAndFlush(SupportsWrite[_AnyStrT_contra], SupportsFlush, Protocol): ...

@type_check_only
class _SupportsRead(Protocol):
    def read(self, n: int, /) -> str: ...

def key_description(character: str) -> str:
    """generate a readable description for a key"""

class ConsoleBase:
    """OS abstraction for console (input/output codec, no echo)"""

    byte_output: _SupportsWriteAndFlush[bytes]
    output: _SupportsWriteAndFlush[str]
    def __init__(self) -> None: ...
    def setup(self) -> None:
        """Set console to read single characters, no echo"""

    def cleanup(self) -> None:
        """Restore default console settings"""

    def getkey(self) -> None:
        """Read a single key from the console"""

    def write_bytes(self, byte_string: bytes) -> None:
        """Write bytes (already encoded)"""

    def write(self, text: str) -> None:
        """Write string"""

    def cancel(self) -> None:
        """Cancel getkey operation"""

    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused, **kwargs: Unused) -> None: ...

if sys.platform == "win32":
    class Out:
        fd: int
        def __init__(self, fd: int) -> None: ...
        def flush(self) -> None: ...
        def write(self, s: bytes) -> None: ...

    class Console(ConsoleBase):
        fncodes: dict[str, str]
        navcodes: dict[str, str]
        def __del__(self) -> None: ...

else:
    class Console(ConsoleBase):
        fd: int
        old: list[Any]  # return type of termios.tcgetattr()
        enc_stdin: _SupportsRead

class Transform:
    """do-nothing: forward all data unchanged"""

    def rx(self, text: str) -> str:
        """text received from serial port"""

    def tx(self, text: str) -> str:
        """text to be sent to serial port"""

    def echo(self, text: str) -> str:
        """text to be sent but displayed on console"""

class CRLF(Transform):
    """ENTER sends CR+LF"""

class CR(Transform):
    """ENTER sends CR"""

class LF(Transform):
    """ENTER sends LF"""

class NoTerminal(Transform):
    """remove typical terminal control codes from input"""

    REPLACEMENT_MAP: dict[int, int]

class NoControls(NoTerminal):
    """Remove all control codes, incl. CR+LF"""

    REPLACEMENT_MAP: dict[int, int]

class Printable(Transform):
    """Show decimal code for all non-ASCII characters and replace most control codes"""

class Colorize(Transform):
    """Apply different colors for received and echo"""

    input_color: str
    echo_color: str

class DebugIO(Transform):
    """Print what is sent and received"""

EOL_TRANSFORMATIONS: dict[str, type[Transform]]
TRANSFORMATIONS: dict[str, type[Transform]]

def ask_for_port() -> str:
    """Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """

class Miniterm:
    """Terminal application. Copy data from serial port to console and vice versa.
    Handle special keys from the console to show menu etc.
    """

    console: Console
    serial: Serial
    echo: bool
    raw: bool
    input_encoding: str
    output_encoding: str
    eol: str
    filters: Iterable[str]
    exit_character: str
    menu_character: str
    alive: bool | None
    receiver_thread: threading.Thread | None
    rx_decoder: codecs.IncrementalDecoder | None
    tx_decoder: codecs.IncrementalDecoder | None
    tx_encoder: codecs.IncrementalEncoder | None
    def __init__(self, serial_instance: Serial, echo: bool = False, eol: str = "crlf", filters: Iterable[str] = ()) -> None: ...
    transmitter_thread: threading.Thread
    def start(self) -> None:
        """start worker threads"""

    def stop(self) -> None:
        """set flag to stop worker threads"""

    def join(self, transmit_only: bool = False) -> None:
        """wait for worker threads to terminate"""

    def close(self) -> None: ...
    tx_transformations: list[Transform]
    rx_transformations: list[Transform]
    def update_transformations(self) -> None:
        """take list of transformation classes and instantiate them for rx and tx"""

    def set_rx_encoding(self, encoding: str, errors: str = "replace") -> None:
        """set encoding for received data"""

    def set_tx_encoding(self, encoding: str, errors: str = "replace") -> None:
        """set encoding for transmitted data"""

    def dump_port_settings(self) -> None:
        """Write current settings to sys.stderr"""

    def reader(self) -> None:
        """loop and copy serial->console"""

    def writer(self) -> None:
        """Loop and copy console->serial until self.exit_character character is
        found. When self.menu_character is found, interpret the next key
        locally.
        """

    def handle_menu_key(self, c: str) -> None:
        """Implement a simple menu / settings"""

    def upload_file(self) -> None:
        """Ask user for filenname and send its contents"""

    def change_filter(self) -> None:
        """change the i/o transformations"""

    def change_encoding(self) -> None:
        """change encoding on the serial port"""

    def change_baudrate(self) -> None:
        """change the baudrate"""

    def change_port(self) -> None:
        """Have a conversation with the user to change the serial port"""

    def suspend_port(self) -> None:
        """open port temporarily, allow reconnect, exit and port change to get
        out of the loop
        """

    def get_help_text(self) -> str:
        """return the help text"""

def main(
    default_port: str | None = None, default_baudrate: int = 9600, default_rts: int | None = None, default_dtr: int | None = None
) -> None:
    """Command line tool, entry point"""
