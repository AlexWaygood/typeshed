"""HTTP Request Parser

This server uses asyncore to accept connections and do initial
processing but threads to do work.
"""

from collections.abc import Mapping, Sequence
from io import BytesIO
from re import Pattern

from waitress.adjustments import Adjustments
from waitress.receiver import ChunkedReceiver, FixedStreamReceiver
from waitress.utilities import Error

def unquote_bytes_to_wsgi(bytestring: str | bytes | bytearray) -> str: ...

class ParsingError(Exception): ...
class TransferEncodingNotImplemented(Exception): ...

class HTTPRequestParser:
    """A structure that collects the HTTP request.

    Once the stream is completed, the instance is passed to
    a server task constructor.
    """

    completed: bool
    empty: bool
    expect_continue: bool
    headers_finished: bool
    header_plus: bytes
    chunked: bool
    content_length: int
    header_bytes_received: int
    body_bytes_received: int
    body_rcv: ChunkedReceiver | FixedStreamReceiver | None
    version: str
    error: Error | None
    connection_close: bool
    headers: Mapping[str, str]
    adj: Adjustments
    def __init__(self, adj: Adjustments) -> None:
        """
        adj is an Adjustments object.
        """

    def received(self, data: bytes) -> int:
        """
        Receives the HTTP stream for one request.  Returns the number of
        bytes consumed.  Sets the completed flag once both the header and the
        body have been received.
        """
    first_line: str
    command: bytes
    url_scheme: str
    def parse_header(self, header_plus: bytes) -> None:
        """
        Parses the header_plus block of text (the headers plus the
        first line of the request).
        """

    def get_body_stream(self) -> BytesIO: ...
    def close(self) -> None: ...

def split_uri(uri: bytes) -> tuple[str, str, bytes, str, str]: ...
def get_header_lines(header: bytes) -> Sequence[bytes]:
    """
    Splits the header into lines, putting multi-line headers together.
    """

first_line_re: Pattern[str]

def crack_first_line(line: str) -> tuple[bytes, bytes, bytes]: ...
