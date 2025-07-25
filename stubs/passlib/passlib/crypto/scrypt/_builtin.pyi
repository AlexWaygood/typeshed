"""passlib.utils.scrypt._builtin -- scrypt() kdf in pure-python"""

from collections.abc import Generator
from typing import Any

class ScryptEngine:
    """
    helper class used to run scrypt kdf, see scrypt() for frontend

    .. warning::
        this class does NO validation of the input ranges or types.

        it's not intended to be used directly,
        but only as a backend for :func:`passlib.utils.scrypt.scrypt()`.
    """

    n: int
    r: int
    p: int
    smix_bytes: int
    iv_bytes: int
    bmix_len: int
    bmix_half_len: int
    bmix_struct: Any
    integerify: Any
    @classmethod
    def execute(cls, secret, salt, n, r, p, keylen):
        """create engine & run scrypt() hash calculation"""

    def __init__(self, n, r, p): ...
    def run(self, secret, salt, keylen):
        """
        run scrypt kdf for specified secret, salt, and keylen

        .. note::

            * time cost is ``O(n * r * p)``
            * mem cost is ``O(n * r)``
        """

    def smix(self, input) -> Generator[None, None, Any]:
        """run SCrypt smix function on a single input block

        :arg input:
            byte string containing input data.
            interpreted as 32*r little endian 4 byte integers.

        :returns:
            byte string containing output data
            derived by mixing input using n & r parameters.

        .. note:: time & mem cost are both ``O(n * r)``
        """

    def bmix(self, source, target) -> None:
        """
        block mixing function used by smix()
        uses salsa20/8 core to mix block contents.

        :arg source:
            source to read from.
            should be list of 32*r 4-byte integers
            (2*r salsa20 blocks).

        :arg target:
            target to write to.
            should be list with same size as source.
            the existing value of this buffer is ignored.

        .. warning::

            this operates *in place* on target,
            so source & target should NOT be same list.

        .. note::

            * time cost is ``O(r)`` -- loops 16*r times, salsa20() has ``O(1)`` cost.

            * memory cost is ``O(1)`` -- salsa20() uses 16 x uint4,
              all other operations done in-place.
        """

__all__ = ["ScryptEngine"]
