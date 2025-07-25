"""
IEEE 48-bit EUI (MAC address) logic.

Supports numerous MAC string formats including Cisco's triple hextet as well
as bare MACs containing no delimiters.
"""

from collections.abc import Iterable, Sequence
from re import Pattern
from typing import ClassVar, Literal

width: Literal[48]
version: Literal[48]
max_int: int

class mac_eui48:
    """A standard IEEE EUI-48 dialect class."""

    word_size: ClassVar[int]
    num_words: ClassVar[int]
    max_word: ClassVar[int]
    word_sep: ClassVar[str]
    word_fmt: ClassVar[str]
    word_base: ClassVar[int]

class mac_unix(mac_eui48):
    """A UNIX-style MAC address dialect class."""

class mac_unix_expanded(mac_unix):
    """A UNIX-style MAC address dialect class with leading zeroes."""

class mac_cisco(mac_eui48):
    """A Cisco 'triple hextet' MAC address dialect class."""

class mac_bare(mac_eui48):
    """A bare (no delimiters) MAC address dialect class."""

class mac_pgsql(mac_eui48):
    """A PostgreSQL style (2 x 24-bit words) MAC address dialect class."""

DEFAULT_DIALECT: type[mac_eui48]
RE_MAC_FORMATS: list[Pattern[str]]

def valid_str(addr: str) -> bool:
    """
    :param addr: An IEEE EUI-48 (MAC) address in string form.

    :return: ``True`` if MAC address string is valid, ``False`` otherwise.
    """

def str_to_int(addr: str) -> int:
    """
    :param addr: An IEEE EUI-48 (MAC) address in string form.

    :return: An unsigned integer that is equivalent to value represented
        by EUI-48/MAC string address formatted according to the dialect
        settings.
    """

def int_to_str(int_val: int, dialect: type[mac_eui48] | None = None) -> str:
    """
    :param int_val: An unsigned integer.

    :param dialect: (optional) a Python class defining formatting options.

    :return: An IEEE EUI-48 (MAC) address string that is equivalent to
        unsigned integer formatted according to the dialect settings.
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

def valid_words(words: Iterable[int], dialect: type[mac_eui48] | None = None) -> bool: ...
def int_to_words(int_val: int, dialect: type[mac_eui48] | None = None) -> tuple[int, ...]: ...
def words_to_int(words: Sequence[int], dialect: type[mac_eui48] | None = None) -> int: ...
def valid_bits(bits: str, dialect: type[mac_eui48] | None = None) -> bool: ...
def bits_to_int(bits: str, dialect: type[mac_eui48] | None = None) -> int: ...
def int_to_bits(int_val: int, dialect: type[mac_eui48] | None = None) -> str: ...
def valid_bin(bin_val: str, dialect: type[mac_eui48] | None = None) -> bool: ...
def int_to_bin(int_val: int) -> str: ...
def bin_to_int(bin_val: str) -> int: ...
