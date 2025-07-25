"""Python 'hex' Codec - 2-digit hex with spaces content transfer encoding.

Encode and decode may be a bit missleading at first sight...

The textual representation is a hex dump: e.g. "40 41"
The "encoded" data of this is the binary form, e.g. b"@A"

Therefore decoding is binary to text and thus converting binary data to hex dump.

"""

import codecs
from _typeshed import ReadableBuffer

HEXDIGITS: str

def hex_encode(data: str, errors: str = "strict") -> tuple[bytes, int]:
    """'40 41 42' -> b'@ab'"""

def hex_decode(data: bytes, errors: str = "strict") -> tuple[str, int]:
    """b'@ab' -> '40 41 42'"""

class Codec(codecs.Codec):
    def encode(self, data: str, errors: str = "strict") -> tuple[bytes, int]:
        """'40 41 42' -> b'@ab'"""

    def decode(self, data: bytes, errors: str = "strict") -> tuple[str, int]:
        """b'@ab' -> '40 41 42'"""

class IncrementalEncoder(codecs.IncrementalEncoder):
    """Incremental hex encoder"""

    state: int
    def encode(self, data: str, final: bool = False) -> bytes:
        """Incremental encode, keep track of digits and emit a byte when a pair
        of hex digits is found. The space is optional unless the error
        handling is defined to be 'strict'.
        """

class IncrementalDecoder(codecs.IncrementalDecoder):
    """Incremental decoder"""

    def decode(self, data: ReadableBuffer, final: bool = False) -> str: ...

class StreamWriter(Codec, codecs.StreamWriter):
    """Combination of hexlify codec and StreamWriter"""

class StreamReader(Codec, codecs.StreamReader):
    """Combination of hexlify codec and StreamReader"""

def getregentry() -> codecs.CodecInfo:
    """encodings module API"""
