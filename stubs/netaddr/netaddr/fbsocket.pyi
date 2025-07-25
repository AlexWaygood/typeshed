"""Fallback routines for Python's standard library socket module"""

from typing import Literal

AF_INET: Literal[2]
AF_INET6: Literal[10]

def inet_ntoa(packed_ip: bytes) -> str:
    """
    Convert an IP address from 32-bit packed binary format to string format.
    """

def inet_ntop(af: int, packed_ip: bytes) -> str:
    """Convert an packed IP address of the given family to string format."""

def inet_pton(af: int, ip_string: str) -> str:
    """
    Convert an IP address from string format to a packed string suitable for
    use with low-level network functions.
    """
