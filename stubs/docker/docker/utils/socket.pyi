from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Generator, Iterable
from typing import Final, Literal, TypeVar, overload

_T = TypeVar("_T")

STDOUT: Final = 1
STDERR: Final = 2

class SocketError(Exception): ...

NPIPE_ENDED: Final = 109

def read(socket, n: int = 4096):
    """
    Reads at most n bytes from socket
    """

def read_exactly(socket, n: int) -> bytes:
    """
    Reads exactly n bytes from socket
    Raises SocketError if there isn't enough data
    """

def next_frame_header(socket) -> tuple[Incomplete, int]:
    """
    Returns the stream and size of the next frame of data waiting to be read
    from socket, according to the protocol defined here:

    https://docs.docker.com/engine/api/v1.24/#attach-to-a-container
    """

def frames_iter(socket, tty):
    """
    Return a generator of frames read from socket. A frame is a tuple where
    the first item is the stream number and the second item is a chunk of data.

    If the tty setting is enabled, the streams are multiplexed into the stdout
    stream.
    """

def frames_iter_no_tty(socket) -> Generator[tuple[str | Incomplete, str | bytes | Incomplete]]:
    """
    Returns a generator of data read from the socket when the tty setting is
    not enabled.
    """

def frames_iter_tty(socket) -> Generator[Incomplete]:
    """
    Return a generator of data read from the socket when the tty setting is
    enabled.
    """

@overload
def consume_socket_output(frames: Iterable[tuple[Incomplete, Incomplete]], demux: Literal[True]) -> tuple[Incomplete, Incomplete]:
    """
    Iterate through frames read from the socket and return the result.

    Args:

        demux (bool):
            If False, stdout and stderr are multiplexed, and the result is the
            concatenation of all the frames. If True, the streams are
            demultiplexed, and the result is a 2-tuple where each item is the
            concatenation of frames belonging to the same stream.
    """

@overload
def consume_socket_output(frames: Iterable[ReadableBuffer], demux: Literal[False] = False) -> bytes: ...
@overload
def demux_adaptor(stream_id: Literal[1], data: _T) -> tuple[_T, None]:
    """
    Utility to demultiplex stdout and stderr when reading frames from the
    socket.
    """

@overload
def demux_adaptor(stream_id: Literal[2], data: _T) -> tuple[None, _T]: ...
