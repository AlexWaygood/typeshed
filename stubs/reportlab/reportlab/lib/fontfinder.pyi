"""This provides some general-purpose tools for finding fonts.

The FontFinder object can search for font files.  It aims to build
a catalogue of fonts which our framework can work with.  It may be useful
if you are building GUIs or design-time interfaces and want to present users
with a choice of fonts.

There are 3 steps to using it
1. create FontFinder and set options and directories
2. search
3. query

>>> import fontfinder
>>> ff = fontfinder.FontFinder()
>>> ff.addDirectories([dir1, dir2, dir3])
>>> ff.search()
>>> ff.getFamilyNames()   #or whichever queries you want...

Because the disk search takes some time to find and parse hundreds of fonts,
it can use a cache to store a file with all fonts found. The cache file name

For each font found, it creates a structure with
- the short font name
- the long font name
- the principal file (.pfb for type 1 fonts), and the metrics file if appropriate
- the time modified (unix time stamp)
- a type code ('ttf')
- the family name
- bold and italic attributes

One common use is to display families in a dialog for end users;
then select regular, bold and italic variants of the font.  To get
the initial list, use getFamilyNames; these will be in alpha order.

>>> ff.getFamilyNames()
['Bitstream Vera Sans', 'Century Schoolbook L', 'Dingbats', 'LettErrorRobot',
'MS Gothic', 'MS Mincho', 'Nimbus Mono L', 'Nimbus Roman No9 L',
'Nimbus Sans L', 'Vera', 'Standard Symbols L',
'URW Bookman L', 'URW Chancery L', 'URW Gothic L', 'URW Palladio L']

One can then obtain a specific font as follows

>>> f = ff.getFont('Bitstream Vera Sans', bold=False, italic=True)
>>> f.fullName
'Bitstream Vera Sans'
>>> f.fileName
'C:\\code\\reportlab\\fonts\\Vera.ttf'
>>>

It can also produce an XML report of fonts found by family, for the benefit
of non-Python applications.

Future plans might include using this to auto-register fonts; and making it
update itself smartly on repeated instantiation.
"""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

def asNative(s): ...

EXTENSIONS: Incomplete
FF_FIXED: Incomplete
FF_SERIF: Incomplete
FF_SYMBOLIC: Incomplete
FF_SCRIPT: Incomplete
FF_NONSYMBOLIC: Incomplete
FF_ITALIC: Incomplete
FF_ALLCAP: Incomplete
FF_SMALLCAP: Incomplete
FF_FORCEBOLD: Incomplete

class FontDescriptor:
    """This is a short descriptive record about a font.

    typeCode should be a file extension e.g. ['ttf','ttc','otf','pfb','pfa']
    """

    name: Incomplete
    fullName: Incomplete
    familyName: Incomplete
    styleName: Incomplete
    isBold: bool
    isItalic: bool
    isFixedPitch: bool
    isSymbolic: bool
    typeCode: Incomplete
    fileName: Incomplete
    metricsFileName: Incomplete
    timeModified: int
    def __init__(self) -> None: ...
    def getTag(self):
        """Return an XML tag representation"""

class FontFinder:
    useCache: Incomplete
    validate: Incomplete
    verbose: Incomplete
    def __init__(
        self, dirs=[], useCache: bool = True, validate: bool = False, recur: bool = False, fsEncoding=None, verbose: int = 0
    ) -> None: ...
    def addDirectory(self, dirName, recur=None) -> None: ...
    def addDirectories(self, dirNames, recur=None) -> None: ...
    def getFamilyNames(self):
        """Returns a list of the distinct font families found"""

    def getFontsInFamily(self, familyName):
        """Return list of all font objects with this family name"""

    def getFamilyXmlReport(self):
        """Reports on all families found as XML."""

    def getFontsWithAttributes(self, **kwds):
        """This is a general lightweight search."""

    def getFont(self, familyName, bold: bool = False, italic: bool = False):
        """Try to find a font matching the spec"""

    def save(self, fileName) -> None: ...
    def load(self, fileName) -> None: ...
    def search(self) -> None: ...

def test() -> None: ...
