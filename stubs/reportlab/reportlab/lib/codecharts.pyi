"""Routines to print code page (character set) drawings. Predates unicode.

To be sure we can accurately represent characters in various encodings
and fonts, we need some routines to display all those characters.
These are defined herein.  The idea is to include flowable, drawable
and graphic objects for single and multi-byte fonts.
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget
from reportlab.platypus import Flowable

__version__: Final[str]
adobe2codec: Incomplete

class CodeChartBase(Flowable):
    """Basic bits of drawing furniture used by
    single and multi-byte versions: ability to put letters
    into boxes.
    """

    rows: Incomplete
    width: Incomplete
    height: Incomplete
    ylist: Incomplete
    xlist: Incomplete
    def calcLayout(self) -> None:
        """Work out x and y positions for drawing"""

    def formatByte(self, byt): ...
    def drawChars(self, charList) -> None:
        """Fills boxes in order.  None means skip a box.
        Empty boxes at end get filled with gray
        """

    def drawLabels(self, topLeft: str = "") -> None:
        """Writes little labels in the top row and first column"""

class SingleByteEncodingChart(CodeChartBase):
    codePoints: int
    faceName: Incomplete
    encodingName: Incomplete
    fontName: Incomplete
    charsPerRow: Incomplete
    boxSize: Incomplete
    hex: Incomplete
    rowLabels: Incomplete
    def __init__(
        self,
        faceName: str = "Helvetica",
        encodingName: str = "WinAnsiEncoding",
        charsPerRow: int = 16,
        boxSize: int = 14,
        hex: int = 1,
    ) -> None: ...
    def draw(self): ...

class KutenRowCodeChart(CodeChartBase):
    """Formats one 'row' of the 94x94 space used in many Asian encodings.aliases

    These deliberately resemble the code charts in Ken Lunde's "Understanding
    CJKV Information Processing", to enable manual checking.  Due to the large
    numbers of characters, we don't try to make one graphic with 10,000 characters,
    but rather output a sequence of these.
    """

    row: Incomplete
    codePoints: int
    boxSize: int
    charsPerRow: int
    rows: int
    rowLabels: Incomplete
    hex: int
    faceName: Incomplete
    encodingName: Incomplete
    fontName: Incomplete
    def __init__(self, row, faceName, encodingName) -> None: ...
    def makeRow(self, row):
        """Works out the character values for this kuten row"""

    def draw(self) -> None: ...

class Big5CodeChart(CodeChartBase):
    """Formats one 'row' of the 94x160 space used in Big 5

    These deliberately resemble the code charts in Ken Lunde's "Understanding
    CJKV Information Processing", to enable manual checking.
    """

    row: Incomplete
    codePoints: int
    boxSize: int
    charsPerRow: int
    rows: int
    hex: int
    faceName: Incomplete
    encodingName: Incomplete
    rowLabels: Incomplete
    fontName: Incomplete
    def __init__(self, row, faceName, encodingName) -> None: ...
    def makeRow(self, row):
        """Works out the character values for this Big5 row.
        Rows start at 0xA1
        """

    def draw(self) -> None: ...

def hBoxText(msg, canvas, x, y, fontName) -> None:
    """Helper for stringwidth tests on Asian fonts.

    Registers font if needed.  Then draws the string,
    and a box around it derived from the stringWidth function
    """

class CodeWidget(Widget):
    """Block showing all the characters"""

    x: int
    y: int
    width: int
    height: int
    def __init__(self) -> None: ...
    def draw(self): ...

def test() -> None: ...
