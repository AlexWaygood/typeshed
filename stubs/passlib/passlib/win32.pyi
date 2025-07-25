"""passlib.win32 - MS Windows support - DEPRECATED, WILL BE REMOVED IN 1.8

the LMHASH and NTHASH algorithms are used in various windows related contexts,
but generally not in a manner compatible with how passlib is structured.

in particular, they have no identifying marks, both being
32 bytes of binary data. thus, they can't be easily identified
in a context with other hashes, so a CryptHandler hasn't been defined for them.

this module provided two functions to aid in any use-cases which exist.

.. warning::

    these functions should not be used for new code unless an existing
    system requires them, they are both known broken,
    and are beyond insecure on their own.

.. autofunction:: raw_lmhash
.. autofunction:: raw_nthash

See also :mod:`passlib.hash.nthash`.
"""

from binascii import hexlify as hexlify
from typing import Final, Literal, overload

from passlib.handlers.windows import nthash as nthash

LM_MAGIC: Final[bytes]
raw_nthash = nthash.raw_nthash

@overload
def raw_lmhash(secret: str | bytes, encoding: str = "ascii", hex: Literal[False] = False) -> bytes:
    """encode password using des-based LMHASH algorithm; returns string of raw bytes, or unicode hex"""

@overload
def raw_lmhash(secret: str | bytes, encoding: str, hex: Literal[True]) -> str: ...
@overload
def raw_lmhash(secret: str | bytes, *, hex: Literal[True]) -> str: ...

__all__ = ["nthash", "raw_lmhash", "raw_nthash"]
