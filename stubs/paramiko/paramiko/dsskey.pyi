"""
DSS keys.
"""

from _typeshed import FileDescriptorOrPath, ReadableBuffer
from collections.abc import Callable
from typing import IO

from paramiko.message import Message
from paramiko.pkey import PKey

class DSSKey(PKey):
    """
    Representation of a DSS key which can be used to sign an verify SSH2
    data.
    """

    p: int | None
    q: int | None
    g: int | None
    y: int | None
    x: int | None
    public_blob: None
    size: int
    def __init__(
        self,
        msg: Message | None = None,
        data: ReadableBuffer | None = None,
        filename: FileDescriptorOrPath | None = None,
        password: str | None = None,
        vals: tuple[int, int, int, int] | None = None,
        file_obj: IO[str] | None = None,
    ) -> None: ...
    def asbytes(self) -> bytes: ...
    def __hash__(self) -> int: ...
    def get_name(self) -> str: ...
    def get_bits(self) -> int: ...
    def can_sign(self) -> bool: ...
    def sign_ssh_data(self, data: bytes, algorithm: str | None = None) -> Message: ...
    def verify_ssh_sig(self, data: bytes, msg: Message) -> bool: ...
    def write_private_key_file(self, filename: FileDescriptorOrPath, password: str | None = None) -> None: ...
    def write_private_key(self, file_obj: IO[str], password: str | None = None) -> None: ...
    @staticmethod
    def generate(bits: int = 1024, progress_func: Callable[..., object] | None = None) -> DSSKey:
        """
        Generate a new private DSS key.  This factory function can be used to
        generate a new host key or authentication key.

        :param int bits: number of bits the generated key should be.
        :param progress_func: Unused
        :return: new `.DSSKey` private key
        """
