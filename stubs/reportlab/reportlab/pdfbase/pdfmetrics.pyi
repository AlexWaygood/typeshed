"""This provides a database of font metric information and
efines Font, Encoding and TypeFace classes aimed at end users.

There are counterparts to some of these in pdfbase/pdfdoc.py, but
the latter focus on constructing the right PDF objects.  These
classes are declarative and focus on letting the user construct
and query font objects.

The module maintains a registry of font objects at run time.

It is independent of the canvas or any particular context.  It keeps
a registry of Font, TypeFace and Encoding objects.  Ideally these
would be pre-loaded, but due to a nasty circularity problem we
trap attempts to access them and do it on first access.
"""

from _typeshed import Incomplete, StrOrBytesPath
from typing import Final

from reportlab.lib.rl_accel import unicode2T1 as unicode2T1

__version__: Final[str]
standardFonts: Incomplete
standardEncodings: Incomplete

class FontError(Exception): ...
class FontNotFoundError(Exception): ...

def parseAFMFile(afmFileName: StrOrBytesPath) -> tuple[dict[Incomplete, Incomplete], list[Incomplete]]:
    """Quick and dirty - gives back a top-level dictionary
    with top-level items, and a 'widths' key containing
    a dictionary of glyph names and widths.  Just enough
    needed for embedding.  A better parser would accept
    options for what data you wwanted, and preserve the
    order.
    """

class TypeFace:
    name: Incomplete
    glyphNames: Incomplete
    glyphWidths: Incomplete
    ascent: int
    descent: int
    familyName: Incomplete
    bold: int
    italic: int
    requiredEncoding: str
    builtIn: int
    def __init__(self, name) -> None: ...
    def getFontFiles(self):
        """Info function, return list of the font files this depends on."""

    def findT1File(self, ext: str = ".pfb"): ...

def bruteForceSearchForFile(fn, searchPath=None): ...
def bruteForceSearchForAFM(faceName):
    """Looks in all AFM files on path for face with given name.

    Returns AFM file name or None.  Ouch!
    """

class Encoding:
    """Object to help you create and refer to encodings."""

    name: Incomplete
    frozen: int
    baseEncodingName: Incomplete
    vector: Incomplete
    def __init__(self, name, base=None) -> None: ...
    def __getitem__(self, index):
        """Return glyph name for that code point, or None"""

    def __setitem__(self, index, value) -> None: ...
    def freeze(self) -> None: ...
    def isEqual(self, other): ...
    def modifyRange(self, base, newNames) -> None:
        """Set a group of character names starting at the code point 'base'."""

    def getDifferences(self, otherEnc):
        """
        Return a compact list of the code points differing between two encodings

        This is in the Adobe format: list of
           [[b1, name1, name2, name3],
           [b2, name4]]

        where b1...bn is the starting code point, and the glyph names following
        are assigned consecutive code points.

        """

    def makePDFObject(self):
        """Returns a PDF Object representing self"""

standardT1SubstitutionFonts: Incomplete

class Font:
    """Represents a font (i.e combination of face and encoding).

    Defines suitable machinery for single byte fonts.  This is
    a concrete class which can handle the basic built-in fonts;
    not clear yet if embedded ones need a new font class or
    just a new typeface class (which would do the job through
    composition)
    """

    fontName: Incomplete
    encoding: Incomplete
    encName: Incomplete
    substitutionFonts: Incomplete
    shapable: bool
    def __init__(self, name, faceName, encName, substitutionFonts=None) -> None: ...
    def stringWidth(self, text: str | bytes, size: float, encoding: str = "utf8") -> float: ...
    def addObjects(self, doc) -> None:
        """Makes and returns one or more PDF objects to be added
        to the document.  The caller supplies the internal name
        to be used (typically F1, F2... in sequence)
        """

PFB_MARKER: Final[str]
PFB_ASCII: Final[str]
PFB_BINARY: Final[str]
PFB_EOF: Final[str]

class EmbeddedType1Face(TypeFace):
    """A Type 1 font other than one of the basic 14.

    Its glyph data will be embedded in the PDF file.
    """

    afmFileName: Incomplete
    pfbFileName: Incomplete
    requiredEncoding: Incomplete
    def __init__(self, afmFileName, pfbFileName) -> None: ...
    def getFontFiles(self): ...
    def addObjects(self, doc):
        """Add whatever needed to PDF file, and return a FontDescriptor reference"""

def registerTypeFace(face) -> None: ...
def registerEncoding(enc) -> None: ...
def registerFontFamily(family, normal=None, bold=None, italic=None, boldItalic=None) -> None: ...
def registerFont(font) -> None:
    """Registers a font, including setting up info for accelerated stringWidth"""

def getTypeFace(faceName):
    """Lazily construct known typefaces if not found"""

def getEncoding(encName):
    """Lazily construct known encodings if not found"""

def findFontAndRegister(fontName: str) -> Font:
    """search for and register a font given its name"""

def getFont(fontName: str) -> Font:
    """Lazily constructs known fonts if not found.

    Names of form 'face-encoding' will be built if
    face and encoding are known.  Also if the name is
    just one of the standard 14, it will make up a font
    in the default encoding.
    """

def getAscentDescent(fontName: str, fontSize: float | None = None): ...
def getAscent(fontName: str, fontSize: float | None = None): ...
def getDescent(fontName: str, fontSize: float | None = None): ...
def getRegisteredFontNames() -> list[Incomplete]:
    """Returns what's in there"""

def stringWidth(text: str | bytes, fontName: str, fontSize: float, encoding: str = "utf8") -> float:
    """Compute width of string in points;
    not accelerated as fast enough because of instanceStringWidthT1/TTF
    """

def dumpFontData() -> None: ...
def test3widths(texts) -> None: ...
def testStringWidthAlgorithms() -> None: ...
def test() -> None: ...
