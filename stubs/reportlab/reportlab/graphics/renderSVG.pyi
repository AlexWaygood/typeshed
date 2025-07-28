"""An experimental SVG renderer for the ReportLab graphics framework.

This will create SVG code from the ReportLab Graphics API (RLG).
To read existing SVG code and convert it into ReportLab graphics
objects download the svglib module here:

  http://python.net/~gherman/#svglib
"""

from _typeshed import Incomplete
from collections.abc import Sequence
from math import cos as cos, pi as pi, sin as sin
from typing import IO, Final

from reportlab.graphics.renderbase import Renderer
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen.canvas import Canvas

AREA_STYLES: Final[Sequence[str]]
LINE_STYLES: Final[Sequence[str]]
TEXT_STYLES: Final[Sequence[str]]
EXTRA_STROKE_STYLES: Final[Sequence[str]]
EXTRA_FILL_STYLES: Final[Sequence[str]]

def drawToString(d: Drawing, showBoundary=0, **kwds) -> str:
    """Returns a SVG as a string in memory, without touching the disk"""

def drawToFile(d: Drawing, fn: str | IO[str], showBoundary=0, **kwds) -> None: ...
def draw(drawing: Drawing, canvas: Canvas, x: float = 0, y: float = 0, showBoundary=0) -> None:
    """As it says."""

def transformNode(doc, newTag, node=None, **attrDict):
    """Transform a DOM node into new node and copy selected attributes.

    Creates a new DOM node with tag name 'newTag' for document 'doc'
    and copies selected attributes from an existing 'node' as provided
    in 'attrDict'. The source 'node' can be None. Attribute values will
    be converted to strings.

    E.g.

        n = transformNode(doc, "node1", x="0", y="1")
        -> DOM node for <node1 x="0" y="1"/>

        n = transformNode(doc, "node1", x=0, y=1+1)
        -> DOM node for <node1 x="0" y="2"/>

        n = transformNode(doc, "node1", node0, x="x0", y="x0", zoo=bar())
        -> DOM node for <node1 x="[node0.x0]" y="[node0.y0]" zoo="[bar()]"/>
    """

class EncodedWriter(list[Incomplete]):
    """
    EncodedWriter(encoding) assumes .write will be called with
    either unicode or utf8 encoded bytes. it will accumulate
    unicode
    """

    BOMS: Incomplete
    encoding: Incomplete
    def __init__(self, encoding, bom: bool = False) -> None: ...
    def write(self, u) -> None: ...
    def getvalue(self): ...

def py_fp_str(*args): ...

class SVGCanvas:
    verbose: Incomplete
    encoding: Incomplete
    bom: Incomplete
    fontHacks: Incomplete
    extraXmlDecl: Incomplete
    code: Incomplete
    style: Incomplete
    path: str
    fp_str: Incomplete
    cfp_str: Incomplete
    doc: Incomplete
    svg: Incomplete
    groupTree: Incomplete
    scaleTree: Incomplete
    currGroup: Incomplete
    def __init__(self, size=(300, 300), encoding: str = "utf-8", verbose: int = 0, bom: bool = False, **kwds) -> None:
        """
        verbose = 0 >0 means do verbose stuff
        useClip = False True means don't use a clipPath definition put the global clip into the clip property
                        to get around an issue with safari
        extraXmlDecl = ''   use to add extra xml declarations
        scaleGroupId = ''   id of an extra group to add around the drawing to allow easy scaling
        svgAttrs = {}       dictionary of attributes to be applied to the svg tag itself
        """

    def save(self, fn=None) -> None: ...
    def NOTUSED_stringWidth(self, s, font=None, fontSize=None):
        """Return the logical width of the string if it were drawn
        in the current font (defaults to self.font).
        """

    def setLineCap(self, v) -> None: ...
    def setLineJoin(self, v) -> None: ...
    def setDash(self, array=[], phase: int = 0) -> None:
        """Two notations. Pass two numbers, or an array and phase."""

    def setStrokeColor(self, color) -> None: ...
    def setFillColor(self, color) -> None: ...
    def setFillMode(self, v) -> None: ...
    def setLineWidth(self, width) -> None: ...
    def setFont(self, font, fontSize) -> None: ...
    def rect(self, x1, y1, x2, y2, rx: int = 8, ry: int = 8, link_info=None, **_svgAttrs) -> None:
        """Draw a rectangle between x1,y1 and x2,y2."""

    def roundRect(self, x1, y1, x2, y2, rx: int = 8, ry: int = 8, link_info=None, **_svgAttrs) -> None:
        """Draw a rounded rectangle between x1,y1 and x2,y2.

        Corners inset as ellipses with x-radius rx and y-radius ry.
        These should have x1<x2, y1<y2, rx>0, and ry>0.
        """

    def drawString(
        self, s, x, y, angle: int = 0, link_info=None, text_anchor: str = "left", textRenderMode: int = 0, **_svgAttrs
    ) -> None: ...
    def drawCentredString(
        self, s, x, y, angle: int = 0, text_anchor: str = "middle", link_info=None, textRenderMode: int = 0, **_svgAttrs
    ) -> None: ...
    def drawRightString(
        self, text, x, y, angle: int = 0, text_anchor: str = "end", link_info=None, textRenderMode: int = 0, **_svgAttrs
    ) -> None: ...
    def comment(self, data) -> None:
        """Add a comment."""

    def drawImage(self, image, x, y, width, height, embed: bool = True) -> None: ...
    def line(self, x1, y1, x2, y2) -> None: ...
    def ellipse(self, x1, y1, x2, y2, link_info=None) -> None:
        """Draw an orthogonal ellipse inscribed within the rectangle x1,y1,x2,y2.

        These should have x1<x2 and y1<y2.
        """

    def circle(self, xc, yc, r, link_info=None) -> None: ...
    def drawCurve(self, x1, y1, x2, y2, x3, y3, x4, y4, closed: int = 0) -> None: ...
    def drawArc(self, x1, y1, x2, y2, startAng: int = 0, extent: int = 360, fromcenter: int = 0) -> None:
        """Draw a partial ellipse inscribed within the rectangle x1,y1,x2,y2.

        Starting at startAng degrees and covering extent degrees. Angles
        start with 0 to the right (+x) and increase counter-clockwise.
        These should have x1<x2 and y1<y2.
        """

    def polygon(self, points, closed: int = 0, link_info=None) -> None: ...
    def lines(self, lineList, color=None, width=None) -> None: ...
    def polyLine(self, points) -> None: ...
    def startGroup(self, attrDict={"transform": ""}): ...
    def endGroup(self, currGroup) -> None: ...
    def transform(self, a, b, c, d, e, f) -> None: ...
    def translate(self, x, y) -> None: ...
    def scale(self, sx, sy) -> None: ...
    def moveTo(self, x, y) -> None: ...
    def lineTo(self, x, y) -> None: ...
    def curveTo(self, x1, y1, x2, y2, x3, y3) -> None: ...
    def closePath(self) -> None: ...
    def saveState(self) -> None: ...
    def restoreState(self) -> None: ...

class _SVGRenderer(Renderer):
    """This draws onto an SVG document."""

    verbose: int
    def __init__(self) -> None: ...
    def drawNode(self, node) -> None:
        """This is the recursive method called for each node in the tree."""

    def drawGroup(self, group) -> None: ...
    def drawRect(self, rect) -> None: ...
    def drawString(self, stringObj) -> None: ...
    def drawLine(self, line) -> None: ...
    def drawCircle(self, circle) -> None: ...
    def drawWedge(self, wedge) -> None: ...
    def drawPolyLine(self, p) -> None: ...
    def drawEllipse(self, ellipse) -> None: ...
    def drawPolygon(self, p) -> None: ...
    def drawPath(self, path, fillMode=0): ...
    def drawImage(self, image) -> None: ...
    def applyStateChanges(self, delta, newState) -> None:
        """This takes a set of states, and outputs the operators
        needed to set those properties
        """

def test(outDir: str = "out-svg") -> None: ...
