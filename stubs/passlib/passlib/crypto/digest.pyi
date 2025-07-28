"""passlib.crypto.digest -- crytographic helpers used by the password hashes in passlib

.. versionadded:: 1.7
"""

from typing import Any

from passlib.utils import SequenceMixin

def lookup_hash(digest, return_unknown: bool = False, required: bool = True):
    """
    Returns a :class:`HashInfo` record containing information about a given hash function.
    Can be used to look up a hash constructor by name, normalize hash name representation, etc.

    :arg digest:
        This can be any of:

        * A string containing a :mod:`!hashlib` digest name (e.g. ``"sha256"``),
        * A string containing an IANA-assigned hash name,
        * A digest constructor function (e.g. ``hashlib.sha256``).

        Case is ignored, underscores are converted to hyphens,
        and various other cleanups are made.

    :param required:
        By default (True), this function will throw an :exc:`~passlib.exc.UnknownHashError` if no hash constructor
        can be found, or if the hash is not actually available.

        If this flag is False, it will instead return a dummy :class:`!HashInfo` record
        which will defer throwing the error until it's constructor function is called.
        This is mainly used by :func:`norm_hash_name`.

    :param return_unknown:

        .. deprecated:: 1.7.3

            deprecated, and will be removed in passlib 2.0.
            this acts like inverse of **required**.

    :returns HashInfo:
        :class:`HashInfo` instance containing information about specified digest.

        Multiple calls resolving to the same hash should always
        return the same :class:`!HashInfo` instance.
    """

def norm_hash_name(name, format: str = "hashlib"):
    """Normalize hash function name (convenience wrapper for :func:`lookup_hash`).

    :arg name:
        Original hash function name.

        This name can be a Python :mod:`~hashlib` digest name,
        a SCRAM mechanism name, IANA assigned hash name, etc.
        Case is ignored, and underscores are converted to hyphens.

    :param format:
        Naming convention to normalize to.
        Possible values are:

        * ``"hashlib"`` (the default) - normalizes name to be compatible
          with Python's :mod:`!hashlib`.

        * ``"iana"`` - normalizes name to IANA-assigned hash function name.
          For hashes which IANA hasn't assigned a name for, this issues a warning,
          and then uses a heuristic to return a "best guess" name.

    :returns:
        Hash name, returned as native :class:`!str`.
    """

class HashInfo(SequenceMixin):
    """
    Record containing information about a given hash algorithm, as returned :func:`lookup_hash`.

    This class exposes the following attributes:

    .. autoattribute:: const
    .. autoattribute:: digest_size
    .. autoattribute:: block_size
    .. autoattribute:: name
    .. autoattribute:: iana_name
    .. autoattribute:: aliases
    .. autoattribute:: supported

    This object can also be treated a 3-element sequence
    containing ``(const, digest_size, block_size)``.
    """

    name: Any
    iana_name: Any
    aliases: Any
    const: Any
    digest_size: Any
    block_size: Any
    error_text: Any
    unknown: bool
    def __init__(self, const, names, required: bool = True) -> None:
        """
        initialize new instance.
        :arg const:
            hash constructor
        :arg names:
            list of 2+ names. should be list of ``(name, iana_name, ... 0+ aliases)``.
            names must be lower-case. only iana name may be None.
        """

    @property
    def supported(self):
        """
        whether hash is available for use
        (if False, constructor will throw UnknownHashError if called)
        """

    @property
    def supported_by_fastpbkdf2(self):
        """helper to detect if hash is supported by fastpbkdf2()"""

    @property
    def supported_by_hashlib_pbkdf2(self):
        """helper to detect if hash is supported by hashlib.pbkdf2_hmac()"""

def compile_hmac(digest, key, multipart: bool = False):
    """
    This function returns an efficient HMAC function, hardcoded with a specific digest & key.
    It can be used via ``hmac = compile_hmac(digest, key)``.

    :arg digest:
        digest name or constructor.

    :arg key:
        secret key as :class:`!bytes` or :class:`!unicode` (unicode will be encoded using utf-8).

    :param multipart:
        request a multipart constructor instead (see return description).

    :returns:
        By default, the returned function has the signature ``hmac(msg) -> digest output``.

        However, if ``multipart=True``, the returned function has the signature
        ``hmac() -> update, finalize``, where ``update(msg)`` may be called multiple times,
        and ``finalize() -> digest_output`` may be repeatedly called at any point to
        calculate the HMAC digest so far.

        The returned object will also have a ``digest_info`` attribute, containing
        a :class:`lookup_hash` instance for the specified digest.

    This function exists, and has the weird signature it does, in order to squeeze as
    provide as much efficiency as possible, by omitting much of the setup cost
    and features of the stdlib :mod:`hmac` module.
    """

def pbkdf1(digest, secret, salt, rounds, keylen=None):
    """pkcs#5 password-based key derivation v1.5

    :arg digest:
        digest name or constructor.

    :arg secret:
        secret to use when generating the key.
        may be :class:`!bytes` or :class:`unicode` (encoded using UTF-8).

    :arg salt:
        salt string to use when generating key.
        may be :class:`!bytes` or :class:`unicode` (encoded using UTF-8).

    :param rounds:
        number of rounds to use to generate key.

    :arg keylen:
        number of bytes to generate (if omitted / ``None``, uses digest's native size)

    :returns:
        raw :class:`bytes` of generated key

    .. note::

        This algorithm has been deprecated, new code should use PBKDF2.
        Among other limitations, ``keylen`` cannot be larger
        than the digest size of the specified hash.
    """

def pbkdf2_hmac(digest, secret, salt, rounds, keylen=None):
    """pkcs#5 password-based key derivation v2.0 using HMAC + arbitrary digest.

    :arg digest:
        digest name or constructor.

    :arg secret:
        passphrase to use to generate key.
        may be :class:`!bytes` or :class:`unicode` (encoded using UTF-8).

    :arg salt:
        salt string to use when generating key.
        may be :class:`!bytes` or :class:`unicode` (encoded using UTF-8).

    :param rounds:
        number of rounds to use to generate key.

    :arg keylen:
        number of bytes to generate.
        if omitted / ``None``, will use digest's native output size.

    :returns:
        raw bytes of generated key

    .. versionchanged:: 1.7

        This function will use the first available of the following backends:

        * `fastpbk2 <https://pypi.python.org/pypi/fastpbkdf2>`_
        * :func:`hashlib.pbkdf2_hmac` (only available in py2 >= 2.7.8, and py3 >= 3.4)
        * builtin pure-python backend

        See :data:`passlib.crypto.digest.PBKDF2_BACKENDS` to determine
        which backend(s) are in use.
    """

__all__ = [
    # hash utils
    "lookup_hash",
    "HashInfo",
    "norm_hash_name",
    # hmac utils
    "compile_hmac",
    # kdfs
    "pbkdf1",
    "pbkdf2_hmac",
]
