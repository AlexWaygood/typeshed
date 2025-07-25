"""
passlib.utils.scrypt -- scrypt hash frontend and help utilities

XXX: add this module to public docs?
"""

def validate(n, r, p):
    """
    helper which validates a set of scrypt config parameters.
    scrypt will take ``O(n * r * p)`` time and ``O(n * r)`` memory.
    limitations are that ``n = 2**<positive integer>``, ``n < 2**(16*r)``, ``r * p < 2 ** 30``.

    :param n: scrypt rounds
    :param r: scrypt block size
    :param p: scrypt parallel factor
    """

def scrypt(secret, salt, n, r, p: int = 1, keylen: int = 32):
    """run SCrypt key derivation function using specified parameters.

    :arg secret:
        passphrase string (unicode is encoded to bytes using utf-8).

    :arg salt:
        salt string (unicode is encoded to bytes using utf-8).

    :arg n:
        integer 'N' parameter

    :arg r:
        integer 'r' parameter

    :arg p:
        integer 'p' parameter

    :arg keylen:
        number of bytes of key to generate.
        defaults to 32 (the internal block size).

    :returns:
        a *keylen*-sized bytes instance

    SCrypt imposes a number of constraints on it's input parameters:

    * ``r * p < 2**30`` -- due to a limitation of PBKDF2-HMAC-SHA256.
    * ``keylen < (2**32 - 1) * 32`` -- due to a limitation of PBKDF2-HMAC-SHA256.
    * ``n`` must a be a power of 2, and > 1 -- internal limitation of scrypt() implementation

    :raises ValueError: if the provided parameters are invalid (see constraints above).

    .. warning::

        Unless the third-party ``scrypt <https://pypi.python.org/pypi/scrypt/>``_ package
        is installed, passlib will use a builtin pure-python implementation of scrypt,
        which is *considerably* slower (and thus requires a much lower / less secure
        ``n`` value in order to be usuable). Installing the :mod:`!scrypt` package
        is strongly recommended.
    """

__all__ = ["validate", "scrypt"]
