"""This is like :mod:`pexpect`, but it will work with any socket that you
pass it. You are responsible for opening and closing the socket.

PEXPECT LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier <noah@noah.org>
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""

from collections.abc import Iterable
from socket import socket as Socket
from typing import AnyStr

from .spawnbase import SpawnBase, _Logfile

__all__ = ["SocketSpawn"]

class SocketSpawn(SpawnBase[AnyStr]):
    """This is like :mod:`pexpect.fdpexpect` but uses the cross-platform python socket api,
    rather than the unix-specific file descriptor api. Thus, it works with
    remote connections on both unix and windows.
    """

    args: None
    command: None
    socket: Socket
    child_fd: int
    closed: bool
    name: str
    use_poll: bool
    def __init__(
        self,
        socket: Socket,
        args: None = None,
        timeout: float | None = 30,
        maxread: int = 2000,
        searchwindowsize: int | None = None,
        logfile: _Logfile | None = None,
        encoding: str | None = None,
        codec_errors: str = "strict",
        use_poll: bool = False,
    ) -> None:
        """This takes an open socket."""

    def close(self) -> None:
        """Close the socket.

        Calling this method a second time does nothing, but if the file
        descriptor was closed elsewhere, :class:`OSError` will be raised.
        """

    def isalive(self) -> bool:
        """Alive if the fileno is valid"""

    def send(self, s: str | bytes) -> int:
        """Write to socket, return number of bytes written"""

    def sendline(self, s: str | bytes) -> int:
        """Write to socket with trailing newline, return number of bytes written"""

    def write(self, s: str | bytes) -> None:
        """Write to socket, return None"""

    def writelines(self, sequence: Iterable[str | bytes]) -> None:
        """Call self.write() for each item in sequence"""

    def read_nonblocking(self, size: int = 1, timeout: float | None = -1) -> AnyStr:
        """
        Read from the file descriptor and return the result as a string.

        The read_nonblocking method of :class:`SpawnBase` assumes that a call
        to os.read will not block (timeout parameter is ignored). This is not
        the case for POSIX file-like objects such as sockets and serial ports.

        Use :func:`select.select`, timeout is implemented conditionally for
        POSIX systems.

        :param int size: Read at most *size* bytes.
        :param int timeout: Wait timeout seconds for file descriptor to be
            ready to read. When -1 (default), use self.timeout. When 0, poll.
        :return: String containing the bytes read
        """
