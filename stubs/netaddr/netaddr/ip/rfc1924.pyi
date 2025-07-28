"""A basic implementation of RFC 1924 ;-)"""

from netaddr.ip import _IPAddressAddr

def chr_range(low: str, high: str) -> list[str]:
    """Returns all characters between low and high chars."""

BASE_85: list[str]
BASE_85_DICT: dict[str, int]

def ipv6_to_base85(addr: _IPAddressAddr) -> str:
    """Convert a regular IPv6 address to base 85."""

def base85_to_ipv6(addr: str) -> str:
    """
    Convert a base 85 IPv6 address to its hexadecimal format.
    """
