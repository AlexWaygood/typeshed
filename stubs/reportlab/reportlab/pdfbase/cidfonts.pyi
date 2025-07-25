"""CID (Asian multi-byte) font support.

This defines classes to represent CID fonts.  They know how to calculate
their own width and how to write themselves into PDF files.
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.pdfbase import pdfmetrics

__version__: Final[str]
DISABLE_CMAP: bool

def findCMapFile(name):
    """Returns full filename, or raises error"""

def structToPDF(structure):
    """Converts deeply nested structure to PDFdoc dictionary/array objects"""

class CIDEncoding(pdfmetrics.Encoding):
    """Multi-byte encoding.  These are loaded from CMAP files.

    A CMAP file is like a mini-codec.  It defines the correspondence
    between code points in the (multi-byte) input data and Character
    IDs.
    """

    name: Incomplete
    source: Incomplete
    def __init__(self, name, useCache: int = 1) -> None: ...
    def parseCMAPFile(self, name) -> None:
        """This is a tricky one as CMAP files are Postscript
        ones.  Some refer to others with a 'usecmap'
        command
        """

    def translate(self, text):
        """Convert a string into a list of CIDs"""

    def fastSave(self, directory) -> None: ...
    def fastLoad(self, directory) -> None: ...
    def getData(self):
        """Simple persistence helper.  Return a dict with all that matters."""

class CIDTypeFace(pdfmetrics.TypeFace):
    """Multi-byte type face.

    Conceptually similar to a single byte typeface,
    but the glyphs are identified by a numeric Character
    ID (CID) and not a glyph name.
    """

    def __init__(self, name) -> None:
        """Initialised from one of the canned dictionaries in allowedEncodings

        Or rather, it will be shortly...
        """

    def getCharWidth(self, characterId): ...

class CIDFont(pdfmetrics.Font):
    """Represents a built-in multi-byte font"""

    faceName: Incomplete
    face: Incomplete
    encodingName: Incomplete
    encoding: Incomplete
    fontName: Incomplete
    name: Incomplete
    isVertical: Incomplete
    substitutionFonts: Incomplete
    def __init__(self, face, encoding) -> None: ...
    def formatForPdf(self, text): ...
    def stringWidth(self, text, size, encoding=None):
        """This presumes non-Unicode input.  UnicodeCIDFont wraps it for that context"""

    def addObjects(self, doc) -> None:
        """The explicit code in addMinchoObjects and addGothicObjects
        will be replaced by something that pulls the data from
        _cidfontdata.py in the next few days.
        """

class UnicodeCIDFont(CIDFont):
    """Wraps up CIDFont to hide explicit encoding choice;
    encodes text for output as UTF16.

    lang should be one of 'jpn',chs','cht','kor' for now.
    if vertical is set, it will select a different widths array
    and possibly glyphs for some punctuation marks.

    halfWidth is only for Japanese.


    >>> dodgy = UnicodeCIDFont('nonexistent')
    Traceback (most recent call last):
    ...
    KeyError: "don't know anything about CID font nonexistent"
    >>> heisei = UnicodeCIDFont('HeiseiMin-W3')
    >>> heisei.name
    'HeiseiMin-W3'
    >>> heisei.language
    'jpn'
    >>> heisei.encoding.name
    'UniJIS-UCS2-H'
    >>> #This is how PDF data gets encoded.
    >>> print(heisei.formatForPdf('hello'))
    \\000h\\000e\\000l\\000l\\000o
    >>> tokyo = u'東䫬'
    >>> print(heisei.formatForPdf(tokyo))
    gqJ\\354
    >>> print(heisei.stringWidth(tokyo,10))
    20.0
    >>> print(heisei.stringWidth('hello world',10))
    45.83
    """

    language: Incomplete
    name: Incomplete
    vertical: Incomplete
    isHalfWidth: Incomplete
    unicodeWidths: Incomplete
    def __init__(self, face, isVertical: bool = False, isHalfWidth: bool = False) -> None: ...
    def formatForPdf(self, text): ...
    def stringWidth(self, text, size, encoding=None):
        """Just ensure we do width test on characters, not bytes..."""

def precalculate(cmapdir) -> None: ...
def test() -> None: ...
