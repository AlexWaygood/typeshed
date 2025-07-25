"""
IPv6 address logic.
"""

from collections.abc import Iterable, Sequence
from typing import ClassVar, Final, Literal

from netaddr.fbsocket import AF_INET6

OPT_IMPORTS: bool
width: Literal[128]
word_size: Literal[16]
word_sep: Literal[":"]
family: Final = AF_INET6
family_name: Literal["IPv6"]
version: Literal[6]
word_base: Literal[16]
max_int: int
num_words: Literal[8]
max_word: int
prefix_to_netmask: dict[int, int]
netmask_to_prefix: dict[int, int]
prefix_to_hostmask: dict[int, int]
hostmask_to_prefix: dict[int, int]

class ipv6_compact:
    """An IPv6 dialect class - compact form."""

    word_fmt: ClassVar[str]
    compact: ClassVar[bool]

class ipv6_full(ipv6_compact):
    """An IPv6 dialect class - 'all zeroes' form."""

class ipv6_verbose(ipv6_compact):
    """An IPv6 dialect class - extra wide 'all zeroes' form."""

def valid_str(addr: str, flags: int = 0) -> bool:
    """
    :param addr: An IPv6 address in presentation (string) format.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Future use - currently has no effect.

    :return: ``True`` if IPv6 address is valid, ``False`` otherwise.

    .. versionchanged:: 1.0.0
        Returns ``False`` instead of raising :exc:`AddrFormatError` for empty strings.
    """

def str_to_int(addr: str, flags: int = 0) -> int:
    """
    :param addr: An IPv6 address in string form.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Future use - currently has no effect.

    :return: The equivalent unsigned integer for a given IPv6 address.
    """

def int_to_str(int_val: int, dialect: type[ipv6_compact] | None = None) -> str:
    """
    :param int_val: An unsigned integer.

    :param dialect: (optional) a Python class defining formatting options.

    :return: The IPv6 presentation (string) format address equivalent to the
        unsigned integer provided.
    """

def int_to_arpa(int_val: int) -> str:
    """
    :param int_val: An unsigned integer.

    :return: The reverse DNS lookup for an IPv6 address in network byte
        order integer form.
    """

def int_to_packed(int_val: int) -> bytes:
    """
    :param int_val: the integer to be packed.

    :return: a packed string that is equivalent to value represented by an
    unsigned integer.
    """

def packed_to_int(packed_int: bytes) -> int:
    """
    :param packed_int: a packed string containing an unsigned integer.
        It is assumed that string is packed in network byte order.

    :return: An unsigned integer equivalent to value of network address
        represented by packed binary string.
    """

def valid_words(words: Iterable[int]) -> bool: ...
def int_to_words(int_val: int, num_words: int | None = None, word_size: int | None = None) -> tuple[int, ...]: ...
def words_to_int(words: Sequence[int]) -> int: ...
def valid_bits(bits: str) -> bool: ...
def bits_to_int(bits: str) -> int: ...
def int_to_bits(int_val: int, word_sep: str | None = None) -> str: ...
def valid_bin(bin_val: str) -> bool: ...
def int_to_bin(int_val: int) -> str: ...
def bin_to_int(bin_val: str) -> int: ...
