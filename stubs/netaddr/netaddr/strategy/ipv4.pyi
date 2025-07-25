"""IPv4 address logic."""

from _typeshed import Unused
from collections.abc import Iterable, Sequence
from socket import AddressFamily
from typing import Literal

from netaddr.core import INET_PTON as INET_PTON, ZEROFILL as ZEROFILL

width: Literal[32]
word_size: Literal[8]
word_fmt: Literal["%d"]
word_sep: Literal["."]
family: Literal[AddressFamily.AF_INET]
family_name: Literal["IPv4"]
version: Literal[4]
word_base: Literal[10]
max_int: int
num_words: Literal[4]
max_word: int
prefix_to_netmask: dict[int, int]
netmask_to_prefix: dict[int, int]
prefix_to_hostmask: dict[int, int]
hostmask_to_prefix: dict[int, int]

def valid_str(addr: str, flags: int = 0) -> bool:
    """
    :param addr: An IPv4 address in presentation (string) format.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Supported constants are INET_PTON and ZEROFILL. See the
        :class:`IPAddress` documentation for details.

    .. versionchanged:: 0.10.1
        ``flags`` is scheduled to default to :data:`INET_PTON` instead of :data:`INET_ATON`
        in the future.

    :return: ``True`` if IPv4 address is valid, ``False`` otherwise.

    .. versionchanged:: 1.0.0
        Returns ``False`` instead of raising :exc:`AddrFormatError` for empty strings.
    """

def str_to_int(addr: str, flags: int = 0) -> int:
    """
    :param addr: An IPv4 dotted decimal address in string form.

    :param flags: decides which rules are applied to the interpretation of the
        addr value. Supported constants are INET_PTON and ZEROFILL. See the
        :class:`IPAddress` documentation for details.

    :return: The equivalent unsigned integer for a given IPv4 address.
    """

def int_to_str(int_val: int, dialect: Unused = None) -> str:
    """
    :param int_val: An unsigned integer.

    :param dialect: (unused) Any value passed in is ignored.

    :return: The IPv4 presentation (string) format address equivalent to the
        unsigned integer provided.
    """

def int_to_arpa(int_val: int) -> str:
    """
    :param int_val: An unsigned integer.

    :return: The reverse DNS lookup for an IPv4 address in network byte
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
def int_to_words(int_val: int) -> tuple[int, ...]:
    """
    :param int_val: An unsigned integer.

    :return: An integer word (octet) sequence that is equivalent to value
        represented by an unsigned integer.
    """

def words_to_int(words: Sequence[int]) -> int:
    """
    :param words: A list or tuple containing integer octets.

    :return: An unsigned integer that is equivalent to value represented
        by word (octet) sequence.
    """

def valid_bits(bits: str) -> bool: ...
def bits_to_int(bits: str) -> int: ...
def int_to_bits(int_val: int, word_sep: str | None = None) -> str: ...
def valid_bin(bin_val: str) -> bool: ...
def int_to_bin(int_val: int) -> str: ...
def bin_to_int(bin_val: str) -> int: ...
def expand_partial_address(addr: str) -> str:
    """
    Expands a partial IPv4 address into a full 4-octet version.

    :param addr: an partial or abbreviated IPv4 address

    :return: an expanded IP address in presentation format (x.x.x.x)

    >>> expand_partial_address('1.2')
    '1.2.0.0'

    .. versionadded:: 1.1.0
    """
