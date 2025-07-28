from collections.abc import Generator
from typing import TextIO

import serial

def sixteen(data: bytes) -> Generator[tuple[str, str] | tuple[None, None], None, None]:
    """yield tuples of hex and ASCII display in multiples of 16. Includes a
    space after 8 bytes and (None, None) after 16 bytes and at the end.
    """

def hexdump(data: bytes) -> Generator[tuple[int, str], None, None]:
    """yield lines with hexdump of data"""

class _Formatter:
    def rx(self, data: bytes) -> None: ...
    def tx(self, data: bytes) -> None: ...
    def control(self, name: str, value: str) -> None: ...

class FormatRaw(_Formatter):
    """Forward only RX and TX data to output."""

    output: TextIO
    color: bool
    rx_color: str
    tx_color: str
    def __init__(self, output: TextIO, color: bool) -> None: ...

class FormatHexdump(_Formatter):
    """Create a hex dump of RX ad TX data, show when control lines are read or
    written.

    output example::

        000000.000 Q-RX flushInput
        000002.469 RTS  inactive
        000002.773 RTS  active
        000003.001 TX   48 45 4C 4C 4F                                    HELLO
        000003.102 RX   48 45 4C 4C 4F                                    HELLO

    """

    start_time: float
    output: TextIO
    color: bool
    rx_color: str
    tx_color: str
    control_color: str
    def __init__(self, output: TextIO, color: bool) -> None: ...
    def write_line(self, timestamp: float, label: str, value: str, value2: str = "") -> None: ...

class Serial(serial.Serial):
    """Inherit the native Serial port implementation and wrap all the methods and
    attributes.
    """

    formatter: FormatRaw | FormatHexdump | None
    show_all: bool
    def from_url(self, url: str) -> str:
        """extract host and port from an URL string"""
