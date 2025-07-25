"""
Utility functions for dealing with primes.
"""

from _typeshed import FileDescriptorOrPath

class ModulusPack:
    """
    convenience object for holding the contents of the /etc/ssh/moduli file,
    on systems that have such a file.
    """

    pack: dict[int, list[tuple[int, int]]]
    discarded: list[tuple[int, str]]
    def __init__(self) -> None: ...
    def read_file(self, filename: FileDescriptorOrPath) -> None:
        """
        :raises IOError: passed from any file operations that fail.
        """

    def get_modulus(self, min: int, prefer: int, max: int) -> tuple[int, int]: ...
