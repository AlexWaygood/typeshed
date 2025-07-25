from _typeshed import Incomplete, SupportsRead
from codecs import CodecInfo
from typing import Protocol, overload
from typing_extensions import TypeAlias

# Is actually webencodings.Encoding
class _Encoding(Protocol):
    name: str
    codec_info: CodecInfo
    def __init__(self, name: str, codec_info: CodecInfo) -> None: ...

_UnicodeInputStream: TypeAlias = str | SupportsRead[str]
_BinaryInputStream: TypeAlias = bytes | SupportsRead[bytes]
_InputStream: TypeAlias = _UnicodeInputStream | _BinaryInputStream  # noqa: Y047  # used in other files

spaceCharactersBytes: Incomplete
asciiLettersBytes: Incomplete
asciiUppercaseBytes: Incomplete
spacesAngleBrackets: Incomplete
invalid_unicode_no_surrogate: str
invalid_unicode_re: Incomplete
non_bmp_invalid_codepoints: Incomplete
ascii_punctuation_re: Incomplete
charsUntilRegEx: Incomplete

class BufferedStream:
    """Buffering for streams that do not have buffering of their own

    The buffer is implemented as a list of chunks on the assumption that
    joining many strings will be slow since it is O(n**2)
    """

    stream: Incomplete
    buffer: Incomplete
    position: Incomplete
    def __init__(self, stream) -> None: ...
    def tell(self): ...
    def seek(self, pos) -> None: ...
    def read(self, bytes): ...

@overload
def HTMLInputStream(source: _UnicodeInputStream) -> HTMLUnicodeInputStream: ...
@overload
def HTMLInputStream(
    source: _BinaryInputStream,
    *,
    override_encoding: str | bytes | None = None,
    transport_encoding: str | bytes | None = None,
    same_origin_parent_encoding: str | bytes | None = None,
    likely_encoding: str | bytes | None = None,
    default_encoding: str = "windows-1252",
    useChardet: bool = True,
) -> HTMLBinaryInputStream: ...

class HTMLUnicodeInputStream:
    """Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.

    """

    reportCharacterErrors: Incomplete
    newLines: Incomplete
    charEncoding: tuple[_Encoding, str]
    dataStream: Incomplete
    def __init__(self, source: _UnicodeInputStream) -> None:
        """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
    chunk: str
    chunkSize: int
    chunkOffset: int
    errors: list[str]
    prevNumLines: int
    prevNumCols: int
    def reset(self) -> None: ...
    def openStream(self, source):
        """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """

    def position(self) -> tuple[int, int]:
        """Returns (line, col) of the current position in the stream."""

    def char(self):
        """Read one character from the stream or queue if available. Return
        EOF when EOF is reached.
        """

    def readChunk(self, chunkSize=None): ...
    def characterErrorsUCS4(self, data) -> None: ...
    def characterErrorsUCS2(self, data) -> None: ...
    def charsUntil(self, characters, opposite: bool = False):
        """Returns a string of characters from the stream up to but not
        including any character in 'characters' or EOF. 'characters' must be
        a container that supports the 'in' method and iteration over its
        characters.
        """

    def unget(self, char) -> None: ...

class HTMLBinaryInputStream(HTMLUnicodeInputStream):
    """Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.

    """

    rawStream: Incomplete
    numBytesMeta: int
    numBytesChardet: int
    override_encoding: Incomplete
    transport_encoding: Incomplete
    same_origin_parent_encoding: Incomplete
    likely_encoding: Incomplete
    default_encoding: Incomplete
    charEncoding: tuple[_Encoding, str]
    def __init__(
        self,
        source: _BinaryInputStream,
        override_encoding: str | bytes | None = None,
        transport_encoding: str | bytes | None = None,
        same_origin_parent_encoding: str | bytes | None = None,
        likely_encoding: str | bytes | None = None,
        default_encoding: str = "windows-1252",
        useChardet: bool = True,
    ) -> None:
        """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
    dataStream: Incomplete
    def reset(self) -> None: ...
    def openStream(self, source):
        """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """

    def determineEncoding(self, chardet: bool = True): ...
    def changeEncoding(self, newEncoding: str | bytes | None) -> None: ...
    def detectBOM(self):
        """Attempts to detect at BOM at the start of the stream. If
        an encoding can be determined from the BOM return the name of the
        encoding otherwise return None
        """

    def detectEncodingMeta(self):
        """Report the encoding declared by the meta element"""

class EncodingBytes(bytes):
    """String-like object with an associated position and various extra methods
    If the position is ever greater than the string length then an exception is
    raised
    """

    def __new__(self, value): ...
    def __init__(self, value) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...
    def next(self): ...
    def previous(self): ...
    def setPosition(self, position) -> None: ...
    def getPosition(self): ...
    position: Incomplete
    def getCurrentByte(self): ...
    @property
    def currentByte(self): ...
    def skip(self, chars=...):
        """Skip past a list of characters"""

    def skipUntil(self, chars): ...
    def matchBytes(self, bytes):
        """Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone
        """

    def jumpTo(self, bytes):
        """Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match
        """

class EncodingParser:
    """Mini parser for detecting character encoding from meta elements"""

    data: Incomplete
    encoding: Incomplete
    def __init__(self, data) -> None:
        """string - the data to work on for encoding detection"""

    def getEncoding(self): ...
    def handleComment(self):
        """Skip over comments"""

    def handleMeta(self): ...
    def handlePossibleStartTag(self): ...
    def handlePossibleEndTag(self): ...
    def handlePossibleTag(self, endTag): ...
    def handleOther(self): ...
    def getAttribute(self):
        """Return a name,value pair for the next attribute in the stream,
        if one is found, or None
        """

class ContentAttrParser:
    data: Incomplete
    def __init__(self, data) -> None: ...
    def parse(self): ...

def lookupEncoding(encoding: str | bytes | None) -> str | None:
    """Return the python codec name corresponding to an encoding or None if the
    string doesn't correspond to a valid encoding.
    """
