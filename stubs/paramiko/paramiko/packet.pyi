"""
Packet handling
"""

from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Callable
from hashlib import _Hash
from logging import Logger
from socket import socket
from typing import Any

from cryptography.hazmat.primitives.ciphers import Cipher
from paramiko.compress import ZlibCompressor, ZlibDecompressor
from paramiko.message import Message

def compute_hmac(key: bytes | bytearray, message: ReadableBuffer, digest_class: _Hash) -> bytes: ...

class NeedRekeyException(Exception):
    """
    Exception indicating a rekey is needed.
    """

def first_arg(e: Exception) -> Any: ...

class Packetizer:
    """
    Implementation of the base SSH packet protocol.
    """

    REKEY_PACKETS: int
    REKEY_BYTES: int
    REKEY_PACKETS_OVERFLOW_MAX: int
    REKEY_BYTES_OVERFLOW_MAX: int
    def __init__(self, socket: socket) -> None: ...
    @property
    def closed(self) -> bool: ...
    def reset_seqno_out(self) -> None: ...
    def reset_seqno_in(self) -> None: ...
    def set_log(self, log: Logger) -> None:
        """
        Set the Python log object to use for logging.
        """

    def set_outbound_cipher(
        self,
        block_engine: Cipher[Incomplete],
        block_size: int,
        mac_engine: _Hash,
        mac_size: int,
        mac_key: bytes | bytearray,
        sdctr: bool = False,
        etm: bool = False,
        aead: bool = False,
        iv_out: bytes | None = None,
    ) -> None:
        """
        Switch outbound data cipher.
        :param etm: Set encrypt-then-mac from OpenSSH
        """

    def set_inbound_cipher(
        self,
        block_engine: Cipher[Incomplete],
        block_size: int,
        mac_engine: _Hash,
        mac_size: int,
        mac_key: bytes | bytearray,
        etm: bool = False,
        aead: bool = False,
        iv_in: bytes | None = None,
    ) -> None:
        """
        Switch inbound data cipher.
        :param etm: Set encrypt-then-mac from OpenSSH
        """

    def set_outbound_compressor(self, compressor: ZlibCompressor) -> None: ...
    def set_inbound_compressor(self, compressor: ZlibDecompressor) -> None: ...
    def close(self) -> None: ...
    def set_hexdump(self, hexdump: bool) -> None: ...
    def get_hexdump(self) -> bool: ...
    def get_mac_size_in(self) -> int: ...
    def get_mac_size_out(self) -> int: ...
    def need_rekey(self) -> bool:
        """
        Returns ``True`` if a new set of keys needs to be negotiated.  This
        will be triggered during a packet read or write, so it should be
        checked after every read or write, or at least after every few.
        """

    def set_keepalive(self, interval: int, callback: Callable[[], object]) -> None:
        """
        Turn on/off the callback keepalive.  If ``interval`` seconds pass with
        no data read from or written to the socket, the callback will be
        executed and the timer will be reset.
        """

    def read_timer(self) -> None: ...
    def start_handshake(self, timeout: float) -> None:
        """
        Tells `Packetizer` that the handshake process started.
        Starts a book keeping timer that can signal a timeout in the
        handshake process.

        :param float timeout: amount of seconds to wait before timing out
        """

    def handshake_timed_out(self) -> bool:
        """
        Checks if the handshake has timed out.

        If `start_handshake` wasn't called before the call to this function,
        the return value will always be `False`. If the handshake completed
        before a timeout was reached, the return value will be `False`

        :return: handshake time out status, as a `bool`
        """

    def complete_handshake(self) -> None:
        """
        Tells `Packetizer` that the handshake has completed.
        """

    def read_all(self, n: int, check_rekey: bool = False) -> bytes:
        """
        Read as close to N bytes as possible, blocking as long as necessary.

        :param int n: number of bytes to read
        :return: the data read, as a `str`

        :raises:
            ``EOFError`` -- if the socket was closed before all the bytes could
            be read
        """

    def write_all(self, out: ReadableBuffer) -> None: ...
    def readline(self, timeout: float) -> str:
        """
        Read a line from the socket.  We assume no data is pending after the
        line, so it's okay to attempt large reads.
        """

    def send_message(self, data: Message) -> None:
        """
        Write a block of data using the current cipher, as an SSH block.
        """

    def read_message(self) -> tuple[int, Message]:
        """
        Only one thread should ever be in this function (no other locking is
        done).

        :raises: `.SSHException` -- if the packet is mangled
        :raises: `.NeedRekeyException` -- if the transport should rekey
        """
