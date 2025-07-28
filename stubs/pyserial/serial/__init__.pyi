import sys

from serial.serialutil import *

if sys.platform == "win32":
    from serial.serialwin32 import Serial as Serial
else:
    from serial.serialposix import PosixPollSerial as PosixPollSerial, Serial as Serial, VTIMESerial as VTIMESerial
# TODO: java? cli? These platforms raise flake8-pyi Y008. Should they be included with a noqa?

__version__: str
VERSION: str
protocol_handler_packages: list[str]

def serial_for_url(
    url: str | None,
    baudrate: int = ...,
    bytesize: int = ...,
    parity: str = ...,
    stopbits: float = ...,
    timeout: float | None = ...,
    xonxoff: bool = ...,
    rtscts: bool = ...,
    write_timeout: float | None = ...,
    dsrdtr: bool = ...,
    inter_byte_timeout: float | None = ...,
    exclusive: float | None = ...,
    *,
    do_not_open: bool = ...,
) -> Serial:
    """Get an instance of the Serial class, depending on port/url. The port is not
    opened when the keyword parameter 'do_not_open' is true, by default it
    is. All other parameters are directly passed to the __init__ method when
    the port is instantiated.

    The list of package names that is searched for protocol handlers is kept in
    ``protocol_handler_packages``.

    e.g. we want to support a URL ``foobar://``. A module
    ``my_handlers.protocol_foobar`` is provided by the user. Then
    ``protocol_handler_packages.append("my_handlers")`` would extend the search
    path so that ``serial_for_url("foobar://"))`` would work.
    """
