"""
binaryornot.helpers
-------------------

Helper utilities used by BinaryOrNot.
"""

from _typeshed import StrOrBytesPath

def print_as_hex(s: str) -> None:
    """
    Print a string as hex bytes.
    """

def get_starting_chunk(filename: StrOrBytesPath, length: int = 1024) -> bytes:
    """
    :param filename: File to open and get the first little chunk of.
    :param length: Number of bytes to read, default 1024.
    :returns: Starting chunk of bytes.
    """

def is_binary_string(bytes_to_check: bytes | bytearray) -> bool:
    """
    Uses a simplified version of the Perl detection algorithm,
    based roughly on Eli Bendersky's translation to Python:
    http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python/

    This is biased slightly more in favour of deeming files as text
    files than the Perl algorithm, since all ASCII compatible character
    sets are accepted as text, not just utf-8.

    :param bytes: A chunk of bytes to check.
    :returns: True if appears to be a binary, otherwise False.
    """
