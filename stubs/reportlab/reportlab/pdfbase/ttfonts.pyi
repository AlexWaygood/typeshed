"""TrueType font support

This defines classes to represent TrueType fonts.  They know how to calculate
their own width and how to write themselves into PDF files.  They support
subsetting and embedding and can represent all 16-bit Unicode characters.

Note on dynamic fonts
---------------------

Usually a Font in ReportLab corresponds to a fixed set of PDF objects (Font,
FontDescriptor, Encoding).  But with dynamic font subsetting a single TTFont
will result in a number of Font/FontDescriptor/Encoding object sets, and the
contents of those will depend on the actual characters used for printing.

To support dynamic font subsetting a concept of "dynamic font" was introduced.
Dynamic Fonts have a _dynamicFont attribute set to 1.

Dynamic fonts have the following additional functions::

    def splitString(self, text, doc):
        '''Splits text into a number of chunks, each of which belongs to a
        single subset.  Returns a list of tuples (subset, string).  Use
        subset numbers with getSubsetInternalName.  Doc is used to identify
        a document so that different documents may have different dynamically
        constructed subsets.'''

    def getSubsetInternalName(self, subset, doc):
        '''Returns the name of a PDF Font object corresponding to a given
        subset of this dynamic font.  Use this function instead of
        PDFDocument.getInternalFontName.'''

You must never call PDFDocument.getInternalFontName for dynamic fonts.

If you have a traditional static font, mapping to PDF text output operators
is simple::

   '%s 14 Tf (%s) Tj' % (getInternalFontName(psfontname), text)

If you have a dynamic font, use this instead::

   for subset, chunk in font.splitString(text, doc):
       '%s 14 Tf (%s) Tj' % (font.getSubsetInternalName(subset, doc), chunk)

(Tf is a font setting operator and Tj is a text ouput operator.  You should
also escape invalid characters in Tj argument, see TextObject._formatText.
Oh, and that 14 up there is font size.)

Canvas and TextObject have special support for dynamic fonts.
"""

from _typeshed import Incomplete, ReadableBuffer, StrOrBytesPath
from typing import Final, NamedTuple
from typing_extensions import Self
from weakref import WeakKeyDictionary

from reportlab.pdfbase import pdfdoc, pdfmetrics

__version__: Final[str]

class TTFError(pdfdoc.PDFError):
    """TrueType font exception"""

def SUBSETN(n, table: ReadableBuffer | None = ...) -> bytes: ...
def makeToUnicodeCMap(fontname: str, subset) -> str:
    """Creates a ToUnicode CMap for a given subset.  See Adobe
    _PDF_Reference (ISBN 0-201-75839-3) for more information.
    """

def splice(stream, offset, value):
    """Splices the given value into stream at the given offset and
    returns the resulting stream (the original is unchanged)
    """

GF_ARG_1_AND_2_ARE_WORDS: Final = 1
GF_ARGS_ARE_XY_VALUES: Final = 2
GF_ROUND_XY_TO_GRID: Final = 4
GF_WE_HAVE_A_SCALE: Final = 8
GF_RESERVED: Final = 16
GF_MORE_COMPONENTS: Final = 32
GF_WE_HAVE_AN_X_AND_Y_SCALE: Final = 64
GF_WE_HAVE_A_TWO_BY_TWO: Final = 128
GF_WE_HAVE_INSTRUCTIONS: Final = 256
GF_USE_MY_METRICS: Final = 512
GF_OVERLAP_COMPOUND: Final = 1024
GF_SCALED_COMPONENT_OFFSET: Final = 2048
GF_UNSCALED_COMPONENT_OFFSET: Final = 4096

def TTFOpenFile(fn: StrOrBytesPath) -> tuple[StrOrBytesPath,]:
    """Opens a TTF file possibly after searching TTFSearchPath
    returns (filename,file)
    """

class TTFontParser:
    """Basic TTF file parser"""

    ttfVersions: Incomplete
    ttcVersions: Incomplete
    fileKind: str
    validate: Incomplete
    subfontNameX: bytes
    def __init__(self, file, validate: int = 0, subfontIndex: int = 0) -> None:
        """Loads and parses a TrueType font file.  file can be a filename or a
        file object.  If validate is set to a false values, skips checksum
        validation.  This can save time, especially if the font is large.
        """
    ttcVersion: Incomplete
    numSubfonts: Incomplete
    subfontOffsets: Incomplete
    def readTTCHeader(self) -> None: ...
    def getSubfont(self, subfontIndex) -> None: ...
    numTables: Incomplete
    searchRange: Incomplete
    entrySelector: Incomplete
    rangeShift: Incomplete
    table: Incomplete
    tables: Incomplete
    def readTableDirectory(self) -> None: ...
    version: Incomplete
    def readHeader(self):
        """read the sfnt header at the current position"""
    filename: Incomplete
    def readFile(self, f) -> None: ...
    def checksumTables(self) -> None: ...
    def checksumFile(self) -> None: ...
    def get_table_pos(self, tag):
        """Returns the offset and size of a given TTF table."""

    def seek(self, pos) -> None:
        """Moves read pointer to a given offset in file."""

    def skip(self, delta) -> None:
        """Skip the given number of bytes."""

    def seek_table(self, tag, offset_in_table: int = 0):
        """Moves read pointer to the given offset within a given table and
        returns absolute offset of that position in the file.
        """

    def read_tag(self):
        """Read a 4-character tag"""

    def get_chunk(self, pos, length):
        """Return a chunk of raw data at given position"""

    def read_uint8(self): ...
    def read_ushort(self):
        """Reads an unsigned short"""

    def read_ulong(self):
        """Reads an unsigned long"""

    def read_short(self):
        """Reads a signed short"""

    def get_ushort(self, pos):
        """Return an unsigned short at given position"""

    def get_ulong(self, pos):
        """Return an unsigned long at given position"""

    def get_table(self, tag):
        """Return the given TTF table"""

class TTFontMaker:
    """Basic TTF file generator"""

    tables: Incomplete
    def __init__(self) -> None:
        """Initializes the generator."""

    def add(self, tag, data) -> None:
        """Adds a table to the TTF file."""

    def makeStream(self):
        """Finishes the generation and returns the TTF file as a string"""

class CMapFmt2SubHeader(NamedTuple):
    """CMapFmt2SubHeader(firstCode, entryCount, idDelta, idRangeOffset)"""

    firstCode: Incomplete
    entryCount: Incomplete
    idDelta: Incomplete
    idRangeOffset: Incomplete

class TTFNameBytes(bytes):
    """class used to return named strings"""

    ustr: Incomplete
    def __new__(cls, b, enc: str = "utf8"): ...

class TTFontFile(TTFontParser):
    """TTF file parser and generator"""

    def __init__(self, file, charInfo: int = 1, validate: int = 0, subfontIndex: int = 0) -> None:
        """Loads and parses a TrueType font file.

        file can be a filename or a file object.  If validate is set to a false
        values, skips checksum validation.  This can save time, especially if
        the font is large.  See TTFontFile.extractInfo for more information.
        """
    name: Incomplete
    familyName: Incomplete
    styleName: Incomplete
    fullName: Incomplete
    uniqueFontID: Incomplete
    fontRevision: Incomplete
    unitsPerEm: Incomplete
    bbox: Incomplete
    ascent: Incomplete
    descent: Incomplete
    capHeight: Incomplete
    stemV: Incomplete
    italicAngle: Incomplete
    underlinePosition: Incomplete
    underlineThickness: Incomplete
    flags: Incomplete
    numGlyphs: Incomplete
    charToGlyph: Incomplete
    defaultWidth: Incomplete
    charWidths: Incomplete
    hmetrics: Incomplete
    glyphPos: Incomplete
    def extractInfo(self, charInfo: int = 1):
        """
        Extract typographic information from the loaded font file.

        The following attributes will be set::

            name         PostScript font name
            flags        Font flags
            ascent       Typographic ascender in 1/1000ths of a point
            descent      Typographic descender in 1/1000ths of a point
            capHeight    Cap height in 1/1000ths of a point (0 if not available)
            bbox         Glyph bounding box [l,t,r,b] in 1/1000ths of a point
            _bbox        Glyph bounding box [l,t,r,b] in unitsPerEm
            unitsPerEm   Glyph units per em
            italicAngle  Italic angle in degrees ccw
            stemV        stem weight in 1/1000ths of a point (approximate)

        If charInfo is true, the following will also be set::

            defaultWidth   default glyph width in 1/1000ths of a point
            charWidths     dictionary of character widths for every supported UCS character
                           code

        This will only work if the font has a Unicode cmap (platform 3,
        encoding 1, format 4 or platform 0 any encoding format 4).  Setting
        charInfo to false avoids this requirement

        """

    def makeSubset(self, subset):
        """Create a subset of a TrueType font"""

FF_FIXED: Incomplete
FF_SERIF: Incomplete
FF_SYMBOLIC: Incomplete
FF_SCRIPT: Incomplete
FF_NONSYMBOLIC: Incomplete
FF_ITALIC: Incomplete
FF_ALLCAP: Incomplete
FF_SMALLCAP: Incomplete
FF_FORCEBOLD: Incomplete

class TTFontFace(TTFontFile, pdfmetrics.TypeFace):
    """TrueType typeface.

    Conceptually similar to a single byte typeface, but the glyphs are
    identified by UCS character codes instead of glyph names.
    """

    def __init__(self, filename, validate: int = 0, subfontIndex: int = 0) -> None:
        """Loads a TrueType font from filename."""

    def getCharWidth(self, code):
        """Returns the width of character U+<code>"""

    def addSubsetObjects(self, doc, fontname, subset):
        """Generate a TrueType font subset and add it to the PDF document.
        Returns a PDFReference to the new FontDescriptor object.
        """

class TTEncoding:
    """Encoding for TrueType fonts (always UTF-8).

    TTEncoding does not directly participate in PDF object creation, since
    we need a number of different 8-bit encodings for every generated font
    subset.  TTFont itself cares about that.
    """

    name: str
    def __init__(self) -> None: ...

class TTFont:
    """Represents a TrueType font.

    Its encoding is always UTF-8.

    Note: you cannot use the same TTFont object for different documents
    at the same time.

    Example of usage:

        font = ttfonts.TTFont('PostScriptFontName', '/path/to/font.ttf')
        pdfmetrics.registerFont(font)

        canvas.setFont('PostScriptFontName', size)
        canvas.drawString(x, y, "Some text encoded in UTF-8")
    """

    class State:
        namePrefix: str
        nextCode: int
        internalName: Incomplete
        frozen: int
        subsets: Incomplete
        def __init__(self, asciiReadable=None, ttf=None) -> None: ...

    fontName: str
    face: TTFontFace
    encoding: TTEncoding
    state: WeakKeyDictionary[Incomplete, State]
    def __init__(
        self,
        name: str,
        filename,
        validate: int = 0,
        subfontIndex: int = 0,
        asciiReadable: int | None = None,
        shapable: bool = True,
    ) -> None:
        """Loads a TrueType font from filename.

        If validate is set to a false values, skips checksum validation.  This
        can save time, especially if the font is large.
        """

    def stringWidth(self, text, size, encoding: str = "utf8"): ...
    def splitString(self, text, doc, encoding: str = "utf-8"):
        """Splits text into a number of chunks, each of which belongs to a
        single subset.  Returns a list of tuples (subset, string).  Use subset
        numbers with getSubsetInternalName.  Doc is needed for distinguishing
        subsets when building different documents at the same time.
        """

    def getSubsetInternalName(self, subset, doc):
        """Returns the name of a PDF Font object corresponding to a given
        subset of this dynamic font.  Use this function instead of
        PDFDocument.getInternalFontName.
        """

    def addObjects(self, doc) -> None:
        """Makes  one or more PDF objects to be added to the document.  The
        caller supplies the internal name to be used (typically F1, F2, ... in
        sequence).

        This method creates a number of Font and FontDescriptor objects.  Every
        FontDescriptor is a (no more than) 256 character subset of the original
        TrueType font.
        """

    @property
    def hbFace(self) -> Incomplete | None:
        """return uharbuzz.Face"""

    def hbFont(self, fontSize: float = 10):
        """return uharfbuzz Font"""

    @property
    def shapable(self) -> bool: ...
    @shapable.setter
    def shapable(self, v) -> None: ...
    def pdfScale(self, v): ...
    def unregister(self) -> None: ...

class ShapedFragWord(list[Incomplete]):
    """list class to distinguish frag words that have been shaped"""

class ShapeData(NamedTuple):
    cluster: int
    x_advance: float
    y_advance: float
    x_offset: float
    y_offset: float
    width: float

class ShapedStr(str):
    def __new__(cls, s, shapeData: ShapeData | None = None) -> Self: ...
    def __radd__(self, other) -> Self: ...

def shapeStr(s: str, fontName: str, fontSize: float, force: bool = False): ...
def freshTTFont(ttfn, ttfpath, **kwds) -> TTFont:
    """return a new instance corrsponding to a ttf path"""

def makeShapedFragWord(w, K: list[Incomplete] = [], V: list[Incomplete] = []) -> type[ShapedFragWord]: ...
def shapeFragWord(w, features=..., force: bool = False): ...
