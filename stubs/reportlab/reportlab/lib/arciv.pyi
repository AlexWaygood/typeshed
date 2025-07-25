"""
Arciv Stream  ciphering
"""

class ArcIV:
    """
    performs 'ArcIV' Stream Encryption of S using key
    Based on what is widely thought to be RSA's ArcIV algorithm.
    It produces output streams that are identical.

    NB there is no separate decoder arciv(arciv(s,key),key) == s
    """

    def __init__(self, key) -> None: ...
    def reset(self) -> None:
        """restore the cipher to it's start state"""

    def encode(self, S):
        """ArcIV encode string S"""

def encode(text, key):
    """One-line shortcut for making an encoder object"""

def decode(text, key):
    """One-line shortcut for decoding"""

__all__ = ["ArcIV", "encode", "decode"]
