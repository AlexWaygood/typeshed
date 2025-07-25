"""Render Drawing objects within others PDFs or standalone

Usage::

    import renderpdf
    renderpdf.draw(drawing, canvas, x, y)

Execute the script to see some test drawings.
changed
"""

from _typeshed import Incomplete
from typing import IO, Final

from reportlab.graphics.renderbase import Renderer
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable

__version__: Final[str]

def draw(drawing: Drawing, canvas: Canvas, x: float, y: float, showBoundary=...) -> None:
    """As it says"""

class _PDFRenderer(Renderer):
    """This draws onto a PDF document.  It needs to be a class
    rather than a function, as some PDF-specific state tracking is
    needed outside of the state info in the SVG model.
    """

    def __init__(self) -> None: ...
    def drawNode(self, node) -> None:
        """This is the recursive method called for each node
        in the tree
        """

    def drawRect(self, rect) -> None: ...
    def drawImage(self, image) -> None: ...
    def drawLine(self, line) -> None: ...
    def drawCircle(self, circle) -> None: ...
    def drawPolyLine(self, polyline) -> None: ...
    def drawWedge(self, wedge) -> None: ...
    def drawEllipse(self, ellipse) -> None: ...
    def drawPolygon(self, polygon) -> None: ...
    def drawString(self, stringObj) -> None: ...
    def drawPath(self, path) -> None: ...
    def setStrokeColor(self, c) -> None: ...
    def setFillColor(self, c) -> None: ...
    def applyStateChanges(self, delta, newState) -> None:
        """This takes a set of states, and outputs the PDF operators
        needed to set those properties
        """

class GraphicsFlowable(Flowable):
    """Flowable wrapper around a Pingo drawing"""

    drawing: Incomplete
    width: Incomplete
    height: Incomplete
    def __init__(self, drawing) -> None: ...
    def draw(self) -> None: ...

def drawToFile(d: Drawing, fn: str | IO[bytes], msg: str = "", showBoundary=..., autoSize: int = 1, **kwds) -> None:
    """Makes a one-page PDF with just the drawing.

    If autoSize=1, the PDF will be the same size as
    the drawing; if 0, it will place the drawing on
    an A4 page with a title above it - possibly overflowing
    if too big.
    """

def drawToString(d: Drawing, msg: str = "", showBoundary=..., autoSize: int = 1, **kwds) -> str:
    """Returns a PDF as a string in memory, without touching the disk"""

def test(outDir: str = "pdfout", shout: bool = False) -> None: ...
