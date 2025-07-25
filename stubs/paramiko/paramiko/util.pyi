"""
Useful functions used by the rest of paramiko.
"""

from _typeshed import FileDescriptorOrPath, ReadableBuffer
from collections.abc import Iterable
from hashlib import _Hash
from logging import Logger, LogRecord
from types import TracebackType
from typing import IO, AnyStr, Protocol
from typing_extensions import Self

from paramiko.config import SSHConfig, SSHConfigDict
from paramiko.hostkeys import HostKeys

class SupportsClose(Protocol):
    def close(self) -> None: ...

def inflate_long(s: bytes | bytearray, always_positive: bool = False) -> int:
    """turns a normalized byte string into a long-int
    (adapted from Crypto.Util.number)
    """

def deflate_long(n: int, add_sign_padding: bool = True) -> bytes:
    """turns a long-int into a normalized byte string
    (adapted from Crypto.Util.number)
    """

def format_binary(data: bytes | bytearray, prefix: str = "") -> list[str]: ...
def format_binary_line(data: bytes | bytearray) -> str: ...
def safe_string(s: Iterable[int | str]) -> bytes: ...
def bit_length(n: int) -> int: ...
def tb_strings() -> list[str]: ...
def generate_key_bytes(hash_alg: type[_Hash], salt: ReadableBuffer, key: bytes | str, nbytes: int) -> bytes:
    """
    Given a password, passphrase, or other human-source key, scramble it
    through a secure hash into some keyworthy bytes.  This specific algorithm
    is used for encrypting/decrypting private key files.

    :param function hash_alg: A function which creates a new hash object, such
        as ``hashlib.sha256``.
    :param salt: data to salt the hash with.
    :type bytes salt: Hash salt bytes.
    :param str key: human-entered password or passphrase.
    :param int nbytes: number of bytes to generate.
    :return: Key data, as `bytes`.
    """

def load_host_keys(filename: FileDescriptorOrPath) -> HostKeys:
    """
    Read a file of known SSH host keys, in the format used by openssh, and
    return a compound dict of ``hostname -> keytype ->`` `PKey
    <paramiko.pkey.PKey>`. The hostname may be an IP address or DNS name.  The
    keytype will be either ``"ssh-rsa"`` or ``"ssh-dss"``.

    This type of file unfortunately doesn't exist on Windows, but on posix,
    it will usually be stored in ``os.path.expanduser("~/.ssh/known_hosts")``.

    Since 1.5.3, this is just a wrapper around `.HostKeys`.

    :param str filename: name of the file to read host keys from
    :return:
        nested dict of `.PKey` objects, indexed by hostname and then keytype
    """

def parse_ssh_config(file_obj: IO[str]) -> SSHConfig:
    """
    Provided only as a backward-compatible wrapper around `.SSHConfig`.

    .. deprecated:: 2.7
        Use `SSHConfig.from_file` instead.
    """

def lookup_ssh_host_config(hostname: str, config: SSHConfig) -> SSHConfigDict:
    """
    Provided only as a backward-compatible wrapper around `.SSHConfig`.
    """

def mod_inverse(x: int, m: int) -> int: ...
def get_thread_id() -> int: ...
def log_to_file(filename: FileDescriptorOrPath, level: int = 10) -> None:
    """send paramiko logs to a logfile,
    if they're not already going somewhere
    """

class PFilter:
    def filter(self, record: LogRecord) -> bool: ...

def get_logger(name: str) -> Logger: ...
def constant_time_bytes_eq(a: AnyStr, b: AnyStr) -> bool: ...

class ClosingContextManager:
    def __enter__(self) -> Self: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...

def clamp_value(minimum: int, val: int, maximum: int) -> int: ...

# This function attempts to convert objects to bytes,
# *but* just returns the object unchanged if that was unsuccessful!
def asbytes(s: object) -> object:
    """
    Coerce to bytes if possible or return unchanged.
    """

def b(s: str | bytes, encoding: str = "utf8") -> bytes:
    """cast unicode or bytes to bytes"""

def u(s: str | bytes, encoding: str = "utf8") -> str:
    """cast bytes or unicode to unicode"""
