import logging
from _typeshed import ReadableBuffer
from collections.abc import Callable, Generator
from typing import Any

from serial.serialutil import SerialBase

LOGGER_LEVELS: dict[str, int]
SE: bytes
NOP: bytes
DM: bytes
BRK: bytes
IP: bytes
AO: bytes
AYT: bytes
EC: bytes
EL: bytes
GA: bytes
SB: bytes
WILL: bytes
WONT: bytes
DO: bytes
DONT: bytes
IAC: bytes
IAC_DOUBLED: bytes
BINARY: bytes
ECHO: bytes
SGA: bytes
COM_PORT_OPTION: bytes
SET_BAUDRATE: bytes
SET_DATASIZE: bytes
SET_PARITY: bytes
SET_STOPSIZE: bytes
SET_CONTROL: bytes
NOTIFY_LINESTATE: bytes
NOTIFY_MODEMSTATE: bytes
FLOWCONTROL_SUSPEND: bytes
FLOWCONTROL_RESUME: bytes
SET_LINESTATE_MASK: bytes
SET_MODEMSTATE_MASK: bytes
PURGE_DATA: bytes
SERVER_SET_BAUDRATE: bytes
SERVER_SET_DATASIZE: bytes
SERVER_SET_PARITY: bytes
SERVER_SET_STOPSIZE: bytes
SERVER_SET_CONTROL: bytes
SERVER_NOTIFY_LINESTATE: bytes
SERVER_NOTIFY_MODEMSTATE: bytes
SERVER_FLOWCONTROL_SUSPEND: bytes
SERVER_FLOWCONTROL_RESUME: bytes
SERVER_SET_LINESTATE_MASK: bytes
SERVER_SET_MODEMSTATE_MASK: bytes
SERVER_PURGE_DATA: bytes
RFC2217_ANSWER_MAP: dict[bytes, bytes]
SET_CONTROL_REQ_FLOW_SETTING: bytes
SET_CONTROL_USE_NO_FLOW_CONTROL: bytes
SET_CONTROL_USE_SW_FLOW_CONTROL: bytes
SET_CONTROL_USE_HW_FLOW_CONTROL: bytes
SET_CONTROL_REQ_BREAK_STATE: bytes
SET_CONTROL_BREAK_ON: bytes
SET_CONTROL_BREAK_OFF: bytes
SET_CONTROL_REQ_DTR: bytes
SET_CONTROL_DTR_ON: bytes
SET_CONTROL_DTR_OFF: bytes
SET_CONTROL_REQ_RTS: bytes
SET_CONTROL_RTS_ON: bytes
SET_CONTROL_RTS_OFF: bytes
SET_CONTROL_REQ_FLOW_SETTING_IN: bytes
SET_CONTROL_USE_NO_FLOW_CONTROL_IN: bytes
SET_CONTROL_USE_SW_FLOW_CONTOL_IN: bytes
SET_CONTROL_USE_HW_FLOW_CONTOL_IN: bytes
SET_CONTROL_USE_DCD_FLOW_CONTROL: bytes
SET_CONTROL_USE_DTR_FLOW_CONTROL: bytes
SET_CONTROL_USE_DSR_FLOW_CONTROL: bytes
LINESTATE_MASK_TIMEOUT: int
LINESTATE_MASK_SHIFTREG_EMPTY: int
LINESTATE_MASK_TRANSREG_EMPTY: int
LINESTATE_MASK_BREAK_DETECT: int
LINESTATE_MASK_FRAMING_ERROR: int
LINESTATE_MASK_PARTIY_ERROR: int
LINESTATE_MASK_OVERRUN_ERROR: int
LINESTATE_MASK_DATA_READY: int
MODEMSTATE_MASK_CD: int
MODEMSTATE_MASK_RI: int
MODEMSTATE_MASK_DSR: int
MODEMSTATE_MASK_CTS: int
MODEMSTATE_MASK_CD_CHANGE: int
MODEMSTATE_MASK_RI_CHANGE: int
MODEMSTATE_MASK_DSR_CHANGE: int
MODEMSTATE_MASK_CTS_CHANGE: int
PURGE_RECEIVE_BUFFER: bytes
PURGE_TRANSMIT_BUFFER: bytes
PURGE_BOTH_BUFFERS: bytes
RFC2217_PARITY_MAP: dict[str, int]
RFC2217_REVERSE_PARITY_MAP: dict[int, str]
RFC2217_STOPBIT_MAP: dict[int | float, int]
RFC2217_REVERSE_STOPBIT_MAP: dict[int, int | float]
M_NORMAL: int
M_IAC_SEEN: int
M_NEGOTIATE: int
REQUESTED: str
ACTIVE: str
INACTIVE: str
REALLY_INACTIVE: str

class TelnetOption:
    """Manage a single telnet option, keeps track of DO/DONT WILL/WONT."""

    connection: Serial
    name: str
    option: bytes
    send_yes: bytes
    send_no: bytes
    ack_yes: bytes
    ack_no: bytes
    state: str
    active: bool
    activation_callback: Callable[[], Any]

    def __init__(
        self,
        connection: Serial,
        name: str,
        option: bytes,
        send_yes: bytes,
        send_no: bytes,
        ack_yes: bytes,
        ack_no: bytes,
        initial_state: str,
        activation_callback: Callable[[], Any] | None = None,
    ) -> None:
        """Initialize option.
        :param connection: connection used to transmit answers
        :param name: a readable name for debug outputs
        :param send_yes: what to send when option is to be enabled.
        :param send_no: what to send when option is to be disabled.
        :param ack_yes: what to expect when remote agrees on option.
        :param ack_no: what to expect when remote disagrees on option.
        :param initial_state: options initialized with REQUESTED are tried to
            be enabled on startup. use INACTIVE for all others.
        """

    def process_incoming(self, command: bytes) -> None:
        """A DO/DONT/WILL/WONT was received for this option, update state and
        answer when needed.
        """

class TelnetSubnegotiation:
    """A object to handle subnegotiation of options. In this case actually
    sub-sub options for RFC 2217. It is used to track com port options.
    """

    connection: Serial
    name: str
    option: bytes
    value: bytes | None
    ack_option: bytes
    state: str
    def __init__(self, connection: Serial, name: str, option: bytes, ack_option: bytes | None = None) -> None: ...
    def set(self, value: bytes) -> None:
        """Request a change of the value. a request is sent to the server. if
        the client needs to know if the change is performed he has to check the
        state of this object.
        """

    def is_ready(self) -> bool:
        """Check if answer from server has been received. when server rejects
        the change, raise a ValueError.
        """

    @property
    def active(self) -> bool:
        """Check if answer from server has been received. when server rejects
        the change, raise a ValueError.
        """

    def wait(self, timeout: float = 3) -> None:
        """Wait until the subnegotiation has been acknowledged or timeout. It
        can also throw a value error when the answer from the server does not
        match the value sent.
        """

    def check_answer(self, suboption: bytes) -> None:
        """Check an incoming subnegotiation block. The parameter already has
        cut off the header like sub option number and com port option value.
        """

class Serial(SerialBase):
    """Serial port implementation for RFC 2217 remote serial ports."""

    logger: logging.Logger | None
    def open(self) -> None:
        """Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """

    def from_url(self, url: str) -> tuple[str, int]:
        """extract host and port from an URL string, other settings are extracted
        an stored in instance
        """

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
        """Read terminal status line: Clear To Send."""

    @property
    def dsr(self) -> bool:
        """Read terminal status line: Data Set Ready."""

    @property
    def ri(self) -> bool:
        """Read terminal status line: Ring Indicator."""

    @property
    def cd(self) -> bool:
        """Read terminal status line: Carrier Detect."""

    def telnet_send_option(self, action: bytes, option: bytes) -> None:
        """Send DO, DONT, WILL, WONT."""

    def rfc2217_send_subnegotiation(self, option: bytes, value: bytes = b"") -> None:
        """Subnegotiation of RFC2217 parameters."""

    def rfc2217_send_purge(self, value: bytes) -> None:
        """Send purge request to the remote.
        (PURGE_RECEIVE_BUFFER / PURGE_TRANSMIT_BUFFER / PURGE_BOTH_BUFFERS)
        """

    def rfc2217_set_control(self, value: bytes) -> None:
        """transmit change of control line to remote"""

    def rfc2217_flow_server_ready(self) -> None:
        """check if server is ready to receive data. block for some time when
        not.
        """

    def get_modem_state(self) -> int:
        """get last modem state (cached value. If value is "old", request a new
        one. This cache helps that we don't issue to many requests when e.g. all
        status lines, one after the other is queried by the user (CTS, DSR
        etc.)
        """

class PortManager:
    """This class manages the state of Telnet and RFC 2217. It needs a serial
    instance and a connection to work with. Connection is expected to implement
    a (thread safe) write function, that writes the string to the network.
    """

    serial: Serial
    connection: Serial
    logger: logging.Logger | None
    mode: int
    suboption: bytes | None
    telnet_command: bytes | None
    modemstate_mask: int
    last_modemstate: int | None
    linstate_mask: int
    def __init__(self, serial_port: Serial, connection: Serial, logger: logging.Logger | None = None) -> None: ...
    def telnet_send_option(self, action: bytes, option: bytes) -> None:
        """Send DO, DONT, WILL, WONT."""

    def rfc2217_send_subnegotiation(self, option: bytes, value: bytes = b"") -> None:
        """Subnegotiation of RFC 2217 parameters."""

    def check_modem_lines(self, force_notification: bool = False) -> None:
        """read control lines from serial port and compare the last value sent to remote.
        send updates on changes.
        """

    def escape(self, data: bytes) -> Generator[bytes, None, None]:
        """This generator function is for the user. All outgoing data has to be
        properly escaped, so that no IAC character in the data stream messes up
        the Telnet state machine in the server.

        socket.sendall(escape(data))
        """

    def filter(self, data: bytes) -> Generator[bytes, None, None]:
        """Handle a bunch of incoming bytes. This is a generator. It will yield
        all characters not of interest for Telnet/RFC 2217.

        The idea is that the reader thread pushes data from the socket through
        this filter:

        for byte in filter(socket.recv(1024)):
            # do things like CR/LF conversion/whatever
            # and write data to the serial port
            serial.write(byte)

        (socket error handling code left as exercise for the reader)
        """
