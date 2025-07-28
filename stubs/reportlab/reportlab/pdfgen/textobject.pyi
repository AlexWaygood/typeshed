"""
PDFTextObject is an efficient way to add text to a Canvas. Do not
instantiate directly, obtain one from the Canvas instead.

Progress Reports:
8.83, 2000-01-13, gmcm: created from pdfgen.py
"""

from _typeshed import Incomplete, Unused
from collections.abc import Callable
from typing import Final, Literal
from typing_extensions import TypeAlias

from reportlab.lib.colors import Color
from reportlab.pdfbase.ttfonts import ShapedStr
from reportlab.pdfgen.canvas import Canvas

# NOTE: This is slightly different from what toColor accepts and interprets
_Color: TypeAlias = Color | tuple[float, float, float, float] | tuple[float, float, float] | list[float] | str

__version__: Final[str]
log2vis: Callable[..., str | None]
BidiStr: type[str]
BidiList: type[list[Incomplete]]
BidiIndex: Incomplete

def bidiText(text: str, direction: str | None) -> str: ...
def bidiShapedText(
    text: str, direction: str = "RTL", clean: bool = True, fontName: str = "Helvetica", fontSize: int = 10, shaping: bool = False
) -> tuple[ShapedStr | str, float]: ...
def isBidiStr(_: Unused) -> bool: ...
def isBidiList(_: Unused) -> bool: ...
def innerBidiStrWrap(s: str, bidiV: int = -1, bidiL: int = -1) -> str: ...
def bidiStrWrap(s: str, orig: str) -> str: ...
def bidiListWrap(L, orig) -> list[Incomplete]: ...
def bidiFragWord(w: str, direction: str | None = None, bidiV: int = -1, bidiL: int = -1, clean: bool = True): ...
def bidiWordList(
    words: list[str] | tuple[str], direction: str = "RTL", clean: bool = True, wx: bool = False
) -> list[Incomplete]: ...

rtlSupport: bool

class _PDFColorSetter:
    """Abstracts the color setting operations; used in Canvas and Textobject
    asseumes we have a _code object
    """

    def setFillColorCMYK(self, c: float, m: float, y: float, k: float, alpha: float | None = None) -> None:
        """set the fill color useing negative color values
        (cyan, magenta, yellow and darkness value).
        Takes 4 arguments between 0.0 and 1.0
        """

    def setStrokeColorCMYK(self, c: float, m: float, y: float, k: float, alpha: float | None = None) -> None:
        """set the stroke color useing negative color values
        (cyan, magenta, yellow and darkness value).
        Takes 4 arguments between 0.0 and 1.0
        """

    def setFillColorRGB(self, r: float, g: float, b: float, alpha: float | None = None) -> None:
        """Set the fill color using positive color description
        (Red,Green,Blue).  Takes 3 arguments between 0.0 and 1.0
        """

    def setStrokeColorRGB(self, r: float, g: float, b: float, alpha: float | None = None) -> None:
        """Set the stroke color using positive color description
        (Red,Green,Blue).  Takes 3 arguments between 0.0 and 1.0
        """

    def setFillColor(self, aColor: _Color, alpha: float | None = None) -> None:
        """Takes a color object, allowing colors to be referred to by name"""

    def setStrokeColor(self, aColor: _Color, alpha: float | None = None) -> None:
        """Takes a color object, allowing colors to be referred to by name"""

    def setFillGray(self, gray: float, alpha: float | None = None) -> None:
        """Sets the gray level; 0.0=black, 1.0=white"""

    def setStrokeGray(self, gray: float, alpha: float | None = None) -> None:
        """Sets the gray level; 0.0=black, 1.0=white"""

    def setStrokeAlpha(self, a: float) -> None: ...
    def setFillAlpha(self, a: float) -> None: ...
    def setStrokeOverprint(self, a) -> None: ...
    def setFillOverprint(self, a) -> None: ...
    def setOverprintMask(self, a) -> None: ...

class PDFTextObject(_PDFColorSetter):
    """PDF logically separates text and graphics drawing; text
    operations need to be bracketed between BT (Begin text) and
    ET operators. This class ensures text operations are
    properly encapusalted. Ask the canvas for a text object
    with beginText(x, y).  Do not construct one directly.
    Do not use multiple text objects in parallel; PDF is
    not multi-threaded!

    It keeps track of x and y coordinates relative to its origin.
    """

    direction: Literal["LTR", "RTL"]
    def __init__(self, canvas: Canvas, x: float = 0, y: float = 0, direction: Literal["LTR", "RTL"] | None = None) -> None: ...
    def getCode(self) -> str:
        """pack onto one line; used internally"""

    def setTextOrigin(self, x: float, y: float) -> None: ...
    def setTextTransform(self, a: float, b: float, c: float, d: float, e: float, f: float) -> None:
        """Like setTextOrigin, but does rotation, scaling etc."""

    def moveCursor(self, dx: float, dy: float) -> None:
        """Starts a new line at an offset dx,dy from the start of the
        current line. This does not move the cursor relative to the
        current position, and it changes the current offset of every
        future line drawn (i.e. if you next do a textLine() call, it
        will move the cursor to a position one line lower than the
        position specificied in this call.
        """

    def setXPos(self, dx: float) -> None:
        """Starts a new line dx away from the start of the
        current line - NOT from the current point! So if
        you call it in mid-sentence, watch out.
        """

    def getCursor(self) -> tuple[float, float]:
        """Returns current text position relative to the last origin."""

    def getStartOfLine(self) -> tuple[float, float]:
        """Returns a tuple giving the text position of the start of the
        current line.
        """

    def getX(self) -> float:
        """Returns current x position relative to the last origin."""

    def getY(self) -> float:
        """Returns current y position relative to the last origin."""

    def setFont(self, psfontname: str, size: float, leading: float | None = None) -> None:
        """Sets the font.  If leading not specified, defaults to 1.2 x
        font size. Raises a readable exception if an illegal font
        is supplied.  Font names are case-sensitive! Keeps track
        of font anme and size for metrics.
        """

    def setCharSpace(self, charSpace: float) -> None:
        """Adjusts inter-character spacing"""

    def setWordSpace(self, wordSpace: float) -> None:
        """Adjust inter-word spacing.  This can be used
        to flush-justify text - you get the width of the
        words, and add some space between them.
        """

    def setHorizScale(self, horizScale: float) -> None:
        """Stretches text out horizontally"""

    def setLeading(self, leading: float) -> None:
        """How far to move down at the end of a line."""

    def setTextRenderMode(self, mode: Literal[0, 1, 2, 3, 4, 5, 6, 7]) -> None:
        """Set the text rendering mode.

        0 = Fill text
        1 = Stroke text
        2 = Fill then stroke
        3 = Invisible
        4 = Fill text and add to clipping path
        5 = Stroke text and add to clipping path
        6 = Fill then stroke and add to clipping path
        7 = Add to clipping path

        after we start clipping we mustn't change the mode back until after the ET
        """

    def setRise(self, rise: float) -> None:
        """Move text baseline up or down to allow superscript/subscripts"""

    def textOut(self, text: str) -> None:
        """prints string at current point, text cursor moves across."""

    def textLine(self, text: str = "") -> None:
        """prints string at current point, text cursor moves down.
        Can work with no argument to simply move the cursor down.
        """

    def textLines(self, stuff: list[str] | tuple[str, ...] | str, trim: int = 1) -> None:
        """prints multi-line or newlined strings, moving down.  One
        comon use is to quote a multi-line block in your Python code;
        since this may be indented, by default it trims whitespace
        off each line and from the beginning; set trim=0 to preserve
        whitespace.
        """

    def __nonzero__(self) -> bool:
        """PDFTextObject is true if it has something done after the init"""
