"""Render drawing objects in common bitmap formats

Usage::

    from reportlab.graphics import renderPM
    renderPM.drawToFile(drawing,filename,fmt='GIF',configPIL={....})

Other functions let you create a PM drawing as string or into a PM buffer.
Execute the script to see some test drawings.
"""

from _typeshed import Incomplete
from typing import IO, Final

from reportlab.graphics.renderbase import Renderer
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas

__version__: Final[str]

def Color2Hex(c): ...
def CairoColor(c):
    """
    c should be None or something convertible to Color
    rlPyCairo.GState can handle Color directly in either RGB24 or ARGB32
    """

def draw(drawing: Drawing, canvas: Canvas, x: float, y: float, showBoundary=...) -> None:
    """As it says"""

class _PMRenderer(Renderer):
    """This draws onto a pix map image. It needs to be a class
    rather than a function, as some image-specific state tracking is
    needed outside of the state info in the SVG model.
    """

    def pop(self) -> None: ...
    def push(self, node) -> None: ...
    def applyState(self) -> None: ...
    def initState(self, x, y) -> None: ...
    def drawNode(self, node) -> None:
        """This is the recursive method called for each node
        in the tree
        """

    def drawRect(self, rect) -> None: ...
    def drawLine(self, line) -> None: ...
    def drawImage(self, image) -> None: ...
    def drawCircle(self, circle) -> None: ...
    def drawPolyLine(self, polyline, _doClose: int = 0) -> None: ...
    def drawEllipse(self, ellipse) -> None: ...
    def drawPolygon(self, polygon) -> None: ...
    def drawString(self, stringObj) -> None: ...
    def drawPath(self, path): ...

BEZIER_ARC_MAGIC: float

class PMCanvas:
    ctm: Incomplete
    def __init__(self, w, h, dpi: int = 72, bg: int = 16777215, configPIL=None, backend=None, backendFmt: str = "RGB") -> None:
        """configPIL dict is passed to image save method"""

    def toPIL(self): ...
    def saveToFile(self, fn, fmt=None): ...
    def saveToString(self, fmt: str = "GIF"): ...
    def setFont(self, fontName, fontSize, leading=None) -> None: ...
    def __setattr__(self, name, value) -> None: ...
    def __getattr__(self, name): ...
    def fillstrokepath(self, stroke: int = 1, fill: int = 1) -> None: ...
    def bezierArcCCW(self, cx, cy, rx, ry, theta0, theta1):
        """return a set of control points for Bezier approximation to an arc
        with angle increasing counter clockwise. No requirement on (theta1-theta0) <= 90
        However, it must be true that theta1-theta0 > 0.
        """

    def addEllipsoidalArc(self, cx, cy, rx, ry, ang1, ang2) -> None:
        """adds an ellisesoidal arc segment to a path, with an ellipse centered
        on cx,cy and with radii (major & minor axes) rx and ry.  The arc is
        drawn in the CCW direction.  Requires: (ang2-ang1) > 0
        """

    def drawCentredString(
        self, x: float, y: float, text: str, text_anchor: str = "middle", direction: str | None = None, shaping: bool = False
    ) -> None: ...
    def drawRightString(self, text: str, x: float, y: float, direction: str | None = None) -> None: ...
    def drawString(
        self,
        x: float,
        y: float,
        text: str,
        _fontInfo=None,
        text_anchor: str = "left",
        direction: str | None = None,
        shaping: bool = False,
    ) -> None: ...
    def line(self, x1, y1, x2, y2) -> None: ...
    def rect(self, x, y, width, height, stroke: int = 1, fill: int = 1) -> None: ...
    def roundRect(self, x, y, width, height, rx, ry) -> None:
        """rect(self, x, y, width, height, rx,ry):
        Draw a rectangle if rx or rx and ry are specified the corners are
        rounded with ellipsoidal arcs determined by rx and ry
        (drawn in the counter-clockwise direction)
        """

    def circle(self, cx, cy, r) -> None:
        """add closed path circle with center cx,cy and axes r: counter-clockwise orientation"""

    def ellipse(self, cx, cy, rx, ry) -> None:
        """add closed path ellipse with center cx,cy and axes rx,ry: counter-clockwise orientation
        (remember y-axis increases downward)
        """

    def saveState(self) -> None:
        """do nothing for compatibility"""
    fillColor: Incomplete
    fillOpacity: Incomplete
    def setFillColor(self, aColor) -> None: ...
    strokeColor: Incomplete
    strokeOpacity: Incomplete
    def setStrokeColor(self, aColor) -> None: ...
    restoreState = saveState
    lineCap: Incomplete
    def setLineCap(self, cap) -> None: ...
    lineJoin: Incomplete
    def setLineJoin(self, join) -> None: ...
    strokeWidth: Incomplete
    def setLineWidth(self, width) -> None: ...
    def stringWidth(self, text, fontName=None, fontSize=None): ...

def drawToPMCanvas(
    d: Drawing,
    dpi: float = 72,
    bg: int = 0xFFFFFF,
    configPIL=None,
    showBoundary=...,
    backend="rlPyCairo",
    backendFmt: str = "RGB",
): ...
def drawToPIL(
    d: Drawing,
    dpi: float = 72,
    bg: int = 0xFFFFFF,
    configPIL=None,
    showBoundary=...,
    backend="rlPyCairo",
    backendFmt: str = "RGB",
): ...
def drawToPILP(
    d: Drawing,
    dpi: float = 72,
    bg: int = 0xFFFFFF,
    configPIL=None,
    showBoundary=...,
    backend="rlPyCairo",
    backendFmt: str = "RGB",
): ...
def drawToFile(
    d: Drawing,
    fn: str | IO[bytes],
    fmt: str = "GIF",
    dpi: float = 72,
    bg: int = 0xFFFFFF,
    configPIL=None,
    showBoundary=...,
    backend="rlPyCairo",
    backendFmt: str = "RGB",
) -> None:
    """create a pixmap and draw drawing, d to it then save as a file
    configPIL dict is passed to image save method
    """

def drawToString(
    d: Drawing,
    fmt: str = "GIF",
    dpi: float = 72,
    bg: int = 0xFFFFFF,
    configPIL=None,
    showBoundary=...,
    backend="rlPyCairo",
    backendFmt: str = "RGB",
) -> str: ...

save = drawToFile

def test(outDir: str = "pmout", shout: bool = False): ...
