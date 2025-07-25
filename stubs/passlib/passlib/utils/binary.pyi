"""
passlib.utils.binary - binary data encoding/decoding/manipulation
"""

from _typeshed import ReadableBuffer
from logging import Logger
from typing import Any, Final

log: Logger

BASE64_CHARS: Final[str]
AB64_CHARS: Final[str]
HASH64_CHARS: Final[str]
BCRYPT_CHARS: Final[str]
PADDED_BASE64_CHARS: Final[str]
HEX_CHARS: Final[str]
UPPER_HEX_CHARS: Final[str]
LOWER_HEX_CHARS: Final[str]
ALL_BYTE_VALUES: Final[bytes]

def compile_byte_translation(mapping: dict[str | bytes | int, str | bytes], source: bytes | None = None) -> bytes:
    """
    return a 256-byte string for translating bytes using specified mapping.
    bytes not specified by mapping will be left alone.

    :param mapping:
        dict mapping input byte (str or int) -> output byte (str or int).

    :param source:
        optional existing byte translation string to use as base.
        (must be 255-length byte string).  defaults to identity mapping.

    :returns:
        255-length byte string for passing to bytes().translate.
    """

def b64s_encode(data: ReadableBuffer) -> bytes:
    """
    encode using shortened base64 format which omits padding & whitespace.
    uses default ``+/`` altchars.
    """

def b64s_decode(data: str | ReadableBuffer) -> bytes:
    """
    decode from shortened base64 format which omits padding & whitespace.
    uses default ``+/`` altchars.
    """

def ab64_encode(data: ReadableBuffer) -> bytes:
    """
    encode using shortened base64 format which omits padding & whitespace.
    uses custom ``./`` altchars.

    it is primarily used by Passlib's custom pbkdf2 hashes.
    """

def ab64_decode(data: str | ReadableBuffer) -> bytes:
    """
    decode from shortened base64 format which omits padding & whitespace.
    uses custom ``./`` altchars, but supports decoding normal ``+/`` altchars as well.

    it is primarily used by Passlib's custom pbkdf2 hashes.
    """

def b32encode(source: ReadableBuffer) -> str:
    """
    wrapper around :func:`base64.b32encode` which strips padding,
    and returns a native string.
    """

def b32decode(source: str | bytes) -> bytes:
    """
    wrapper around :func:`base64.b32decode`
    which handles common mistyped chars.
    padding optional, ignored if present.
    """

class Base64Engine:
    """Provides routines for encoding/decoding base64 data using
    arbitrary character mappings, selectable endianness, etc.

    :arg charmap:
        A string of 64 unique characters,
        which will be used to encode successive 6-bit chunks of data.
        A character's position within the string should correspond
        to its 6-bit value.

    :param big:
        Whether the encoding should be big-endian (default False).

    .. note::
        This class does not currently handle base64's padding characters
        in any way what so ever.

    Raw Bytes <-> Encoded Bytes
    ===========================
    The following methods convert between raw bytes,
    and strings encoded using the engine's specific base64 variant:

    .. automethod:: encode_bytes
    .. automethod:: decode_bytes
    .. automethod:: encode_transposed_bytes
    .. automethod:: decode_transposed_bytes

    ..
        .. automethod:: check_repair_unused
        .. automethod:: repair_unused

    Integers <-> Encoded Bytes
    ==========================
    The following methods allow encoding and decoding
    unsigned integers to and from the engine's specific base64 variant.
    Endianess is determined by the engine's ``big`` constructor keyword.

    .. automethod:: encode_int6
    .. automethod:: decode_int6

    .. automethod:: encode_int12
    .. automethod:: decode_int12

    .. automethod:: encode_int24
    .. automethod:: decode_int24

    .. automethod:: encode_int64
    .. automethod:: decode_int64

    Informational Attributes
    ========================
    .. attribute:: charmap

        unicode string containing list of characters used in encoding;
        position in string matches 6bit value of character.

    .. attribute:: bytemap

        bytes version of :attr:`charmap`

    .. attribute:: big

        boolean flag indicating this using big-endian encoding.
    """

    bytemap: Any
    big: Any
    def __init__(self, charmap, big: bool = False) -> None: ...
    @property
    def charmap(self):
        """charmap as unicode"""

    def encode_bytes(self, source):
        """encode bytes to base64 string.

        :arg source: byte string to encode.
        :returns: byte string containing encoded data.
        """

    def decode_bytes(self, source):
        """decode bytes from base64 string.

        :arg source: byte string to decode.
        :returns: byte string containing decoded data.
        """

    def check_repair_unused(self, source):
        """helper to detect & clear invalid unused bits in last character.

        :arg source:
            encoded data (as ascii bytes or unicode).

        :returns:
            `(True, result)` if the string was repaired,
            `(False, source)` if the string was ok as-is.
        """

    def repair_unused(self, source): ...
    def encode_transposed_bytes(self, source, offsets):
        """encode byte string, first transposing source using offset list"""

    def decode_transposed_bytes(self, source, offsets):
        """decode byte string, then reverse transposition described by offset list"""

    def decode_int6(self, source):
        """decode single character -> 6 bit integer"""

    def decode_int12(self, source):
        """decodes 2 char string -> 12-bit integer"""

    def decode_int24(self, source):
        """decodes 4 char string -> 24-bit integer"""

    def decode_int30(self, source):
        """decode 5 char string -> 30 bit integer"""

    def decode_int64(self, source):
        """decode 11 char base64 string -> 64-bit integer

        this format is used primarily by des-crypt & variants to encode
        the DES output value used as a checksum.
        """

    def encode_int6(self, value):
        """encodes 6-bit integer -> single hash64 character"""

    def encode_int12(self, value):
        """encodes 12-bit integer -> 2 char string"""

    def encode_int24(self, value):
        """encodes 24-bit integer -> 4 char string"""

    def encode_int30(self, value):
        """decode 5 char string -> 30 bit integer"""

    def encode_int64(self, value):
        """encode 64-bit integer -> 11 char hash64 string

        this format is used primarily by des-crypt & variants to encode
        the DES output value used as a checksum.
        """

class LazyBase64Engine(Base64Engine):
    """Base64Engine which delays initialization until it's accessed"""

    def __init__(self, *args, **kwds) -> None: ...
    def __getattribute__(self, attr: str): ...

h64: Base64Engine
h64big: Base64Engine
bcrypt64: Base64Engine

__all__ = [
    # constants
    "BASE64_CHARS",
    "PADDED_BASE64_CHARS",
    "AB64_CHARS",
    "HASH64_CHARS",
    "BCRYPT_CHARS",
    "HEX_CHARS",
    "LOWER_HEX_CHARS",
    "UPPER_HEX_CHARS",
    "ALL_BYTE_VALUES",
    # misc
    "compile_byte_translation",
    # base64
    "ab64_encode",
    "ab64_decode",
    "b64s_encode",
    "b64s_decode",
    # base32
    "b32encode",
    "b32decode",
    # custom encodings
    "Base64Engine",
    "LazyBase64Engine",
    "h64",
    "h64big",
    "bcrypt64",
]
