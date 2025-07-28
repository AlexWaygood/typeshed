"""passlib.crypto._blowfish.base - unoptimized pure-python blowfish engine"""

from typing import Any

class BlowfishEngine:
    P: Any
    S: Any
    def __init__(self) -> None: ...
    @staticmethod
    def key_to_words(data, size: int = 18):
        """convert data to tuple of <size> 4-byte integers, repeating or
        truncating data as needed to reach specified size
        """

    def encipher(self, l, r):
        """loop version of blowfish encipher routine"""

    def expand(self, key_words) -> None:
        """perform stock Blowfish keyschedule setup"""

    def eks_salted_expand(self, key_words, salt_words) -> None:
        """perform EKS' salted version of Blowfish keyschedule setup"""

    def eks_repeated_expand(self, key_words, salt_words, rounds) -> None:
        """perform rounds stage of EKS keyschedule setup"""

    def repeat_encipher(self, l, r, count):
        """repeatedly apply encipher operation to a block"""

__all__ = ["BlowfishEngine"]
