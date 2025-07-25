"""passlib.utils -- helpers for writing password hashes"""

import random
import timeit
from _typeshed import ReadableBuffer
from collections.abc import Iterable
from hmac import compare_digest
from typing import Final, Literal, SupportsBytes, SupportsIndex, overload

from passlib.utils.compat import JYTHON as JYTHON

__all__ = [
    "JYTHON",
    "sys_bits",
    "unix_crypt_schemes",
    "rounds_cost_values",
    "consteq",
    "saslprep",
    "xor_bytes",
    "render_bytes",
    "is_same_codec",
    "is_ascii_safe",
    "to_bytes",
    "to_unicode",
    "to_native_str",
    "has_crypt",
    "test_crypt",
    "safe_crypt",
    "tick",
    "rng",
    "getrandbytes",
    "getrandstr",
    "generate_password",
    "is_crypt_handler",
    "is_crypt_context",
    "has_rounds_info",
    "has_salt_info",
]

sys_bits: Final[int]
unix_crypt_schemes: list[str]
rounds_cost_values: Final[list[str]]

class SequenceMixin:
    """
    helper which lets result object act like a fixed-length sequence.
    subclass just needs to provide :meth:`_as_tuple()`.
    """

    def __getitem__(self, idx): ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...

consteq = compare_digest

def str_consteq(left: str | bytes, right: str | bytes) -> bool:
    """Check two strings/bytes for equality.

    This function uses an approach designed to prevent
    timing analysis, making it appropriate for cryptography.
    a and b must both be of the same type: either str (ASCII only),
    or any type that supports the buffer protocol (e.g. bytes).

    Note: If a and b are of different lengths, or if an error occurs,
    a timing attack could theoretically reveal information about the
    types and lengths of a and b--but not their values.
    """

def splitcomma(source: str, sep: str = ",") -> list[str]:
    """split comma-separated string into list of elements,
    stripping whitespace.
    """

def saslprep(source: str, param: str = "value") -> str:
    """Normalizes unicode strings using SASLPrep stringprep profile.

    The SASLPrep profile is defined in :rfc:`4013`.
    It provides a uniform scheme for normalizing unicode usernames
    and passwords before performing byte-value sensitive operations
    such as hashing. Among other things, it normalizes diacritic
    representations, removes non-printing characters, and forbids
    invalid characters such as ``\\n``. Properly internationalized
    applications should run user passwords through this function
    before hashing.

    :arg source:
        unicode string to normalize & validate

    :param param:
        Optional noun identifying source parameter in error messages
        (Defaults to the string ``"value"``). This is mainly useful to make the caller's error
        messages make more sense contextually.

    :raises ValueError:
        if any characters forbidden by the SASLPrep profile are encountered.

    :raises TypeError:
        if input is not :class:`!unicode`

    :returns:
        normalized unicode string

    .. note::

        This function is not available under Jython,
        as the Jython stdlib is missing the :mod:`!stringprep` module
        (`Jython issue 1758320 <http://bugs.jython.org/issue1758320>`_).

    .. versionadded:: 1.6
    """

def render_bytes(source: str | bytes, *args: str | bytes) -> bytes:
    """Peform ``%`` formating using bytes in a uniform manner across Python 2/3.

    This function is motivated by the fact that
    :class:`bytes` instances do not support ``%`` or ``{}`` formatting under Python 3.
    This function is an attempt to provide a replacement:
    it converts everything to unicode (decoding bytes instances as ``latin-1``),
    performs the required formatting, then encodes the result to ``latin-1``.

    Calling ``render_bytes(source, *args)`` should function roughly the same as
    ``source % args`` under Python 2.

    .. todo::
        python >= 3.5 added back limited support for bytes %,
        can revisit when 3.3/3.4 is dropped.
    """

def bytes_to_int(value: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer) -> int:
    """decode byte string as single big-endian integer"""

def int_to_bytes(value: int, count: SupportsIndex) -> bytes:
    """encode integer as single big-endian byte string"""

def xor_bytes(
    left: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
    right: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
) -> bytes:
    """Perform bitwise-xor of two byte strings (must be same size)"""

def repeat_string(source: str | bytes, size: int) -> str | bytes:
    """
    repeat or truncate <source> string, so it has length <size>
    """

def is_ascii_codec(codec: str) -> bool:
    """Test if codec is compatible with 7-bit ascii (e.g. latin-1, utf-8; but not utf-16)"""

def is_same_codec(left: str, right: str) -> bool:
    """Check if two codec names are aliases for same codec"""

def is_ascii_safe(source: str | bytes) -> bool:
    """Check if string (bytes or unicode) contains only 7-bit ascii"""

def to_bytes(source: str | bytes, encoding: str = "utf-8", param: str = "value", source_encoding: str | None = None) -> bytes:
    """Helper to normalize input to bytes.

    :arg source:
        Source bytes/unicode to process.

    :arg encoding:
        Target encoding (defaults to ``"utf-8"``).

    :param param:
        Optional name of variable/noun to reference when raising errors

    :param source_encoding:
        If this is specified, and the source is bytes,
        the source will be transcoded from *source_encoding* to *encoding*
        (via unicode).

    :raises TypeError: if source is not unicode or bytes.

    :returns:
        * unicode strings will be encoded using *encoding*, and returned.
        * if *source_encoding* is not specified, byte strings will be
          returned unchanged.
        * if *source_encoding* is specified, byte strings will be transcoded
          to *encoding*.
    """

def to_unicode(source: str | bytes, encoding: str = "utf-8", param: str = "value") -> str:
    """Helper to normalize input to unicode.

    :arg source:
        source bytes/unicode to process.

    :arg encoding:
        encoding to use when decoding bytes instances.

    :param param:
        optional name of variable/noun to reference when raising errors.

    :raises TypeError: if source is not unicode or bytes.

    :returns:
        * returns unicode strings unchanged.
        * returns bytes strings decoded using *encoding*
    """

def to_native_str(source: str | bytes, encoding: str = "utf-8", param: str = "value") -> str:
    """Take in unicode or bytes, return native string.

    Python 2: encodes unicode using specified encoding, leaves bytes alone.
    Python 3: leaves unicode alone, decodes bytes using specified encoding.

    :raises TypeError: if source is not unicode or bytes.

    :arg source:
        source unicode or bytes string.

    :arg encoding:
        encoding to use when encoding unicode or decoding bytes.
        this defaults to ``"utf-8"``.

    :param param:
        optional name of variable/noun to reference when raising errors.

    :returns: :class:`str` instance
    """

has_crypt: bool

def safe_crypt(secret: str | bytes, hash: str | bytes) -> str | None:
    """Wrapper around stdlib's crypt.

    This is a wrapper around stdlib's :func:`!crypt.crypt`, which attempts
    to provide uniform behavior across Python 2 and 3.

    :arg secret:
        password, as bytes or unicode (unicode will be encoded as ``utf-8``).

    :arg hash:
        hash or config string, as ascii bytes or unicode.

    :returns:
        resulting hash as ascii unicode; or ``None`` if the password
        couldn't be hashed due to one of the issues:

        * :func:`crypt()` not available on platform.

        * Under Python 3, if *secret* is specified as bytes,
          it must be use ``utf-8`` or it can't be passed
          to :func:`crypt()`.

        * Some OSes will return ``None`` if they don't recognize
          the algorithm being used (though most will simply fall
          back to des-crypt).

        * Some OSes will return an error string if the input config
          is recognized but malformed; current code converts these to ``None``
          as well.
    """

def test_crypt(secret: str | bytes, hash: str) -> bool:
    """check if :func:`crypt.crypt` supports specific hash
    :arg secret: password to test
    :arg hash: known hash of password to use as reference
    :returns: True or False
    """

timer = timeit.default_timer
tick = timer
rng: random.Random

@overload
def getrandbytes(rng: random.Random, count: None) -> Literal[b""]:
    """return byte-string containing *count* number of randomly generated bytes, using specified rng"""

@overload
def getrandbytes(rng: random.Random, count) -> bytes: ...
def getrandstr(rng: random.Random, charset: str, count: int) -> str:
    """return string containing *count* number of chars/bytes, whose elements are drawn from specified charset, using specified rng"""

def generate_password(size: int = 10, charset: str = ...) -> str:
    """generate random password using given length & charset

    :param size:
        size of password.

    :param charset:
        optional string specified set of characters to draw from.

        the default charset contains all normal alphanumeric characters,
        except for the characters ``1IiLl0OoS5``, which were omitted
        due to their visual similarity.

    :returns: :class:`!str` containing randomly generated password.

    .. note::

        Using the default character set, on a OS with :class:`!SystemRandom` support,
        this function should generate passwords with 5.7 bits of entropy per character.
    """

def is_crypt_handler(obj) -> bool:
    """check if object follows the :ref:`password-hash-api`"""

def is_crypt_context(obj) -> bool:
    """check if object appears to be a :class:`~passlib.context.CryptContext` instance"""

def has_rounds_info(handler) -> bool:
    """check if handler provides the optional :ref:`rounds information <rounds-attributes>` attributes"""

def has_salt_info(handler) -> bool:
    """check if handler provides the optional :ref:`salt information <salt-attributes>` attributes"""
