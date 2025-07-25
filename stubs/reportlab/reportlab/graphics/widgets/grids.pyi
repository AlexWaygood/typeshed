from _typeshed import Incomplete
from typing import Final, NoReturn

from reportlab.graphics.shapes import LineShape
from reportlab.graphics.widgetbase import Widget

__version__: Final[str]

def frange(start, end=None, inc=None):
    """A range function, that does accept float increments..."""

def makeDistancesList(list):
    """Returns a list of distances between adjacent numbers in some input list.

    E.g. [1, 1, 2, 3, 5, 7] -> [0, 1, 1, 2, 2]
    """

class Grid(Widget):
    """This makes a rectangular grid of equidistant stripes.

    The grid contains an outer border rectangle, and stripes
    inside which can be drawn with lines and/or as solid tiles.
    The drawing order is: outer rectangle, then lines and tiles.

    The stripes' width is indicated as 'delta'. The sequence of
    stripes can have an offset named 'delta0'. Both values need
    to be positive!
    """

    x: int
    y: int
    width: int
    height: int
    orientation: str
    useLines: int
    useRects: int
    delta: int
    delta0: int
    deltaSteps: Incomplete
    fillColor: Incomplete
    stripeColors: Incomplete
    strokeColor: Incomplete
    strokeWidth: int
    def __init__(self) -> None: ...
    def demo(self): ...
    def makeOuterRect(self): ...
    def makeLinePosList(self, start, isX: int = 0):
        """Returns a list of positions where to place lines."""

    def makeInnerLines(self): ...
    def makeInnerTiles(self): ...
    def draw(self): ...

class DoubleGrid(Widget):
    """This combines two ordinary Grid objects orthogonal to each other."""

    x: int
    y: int
    width: int
    height: int
    grid0: Incomplete
    grid1: Incomplete
    def __init__(self) -> None: ...
    def demo(self): ...
    def draw(self): ...

class ShadedRect(Widget):
    """This makes a rectangle with shaded colors between two colors.

    Colors are interpolated linearly between 'fillColorStart'
    and 'fillColorEnd', both of which appear at the margins.
    If 'numShades' is set to one, though, only 'fillColorStart'
    is used.
    """

    x: int
    y: int
    width: int
    height: int
    orientation: str
    numShades: int
    fillColorStart: Incomplete
    fillColorEnd: Incomplete
    strokeColor: Incomplete
    strokeWidth: int
    cylinderMode: int
    def __init__(self, **kw) -> None: ...
    def demo(self): ...
    def draw(self): ...

def colorRange(c0, c1, n):
    """Return a range of intermediate colors between c0 and c1"""

def centroid(P):
    """compute average point of a set of points"""

def rotatedEnclosingRect(P, angle, rect):
    """
    given P a sequence P of x,y coordinate pairs and an angle in degrees
    find the centroid of P and the axis at angle theta through it
    find the extreme points of P wrt axis parallel distance and axis
    orthogonal distance. Then compute the least rectangle that will still
    enclose P when rotated by angle.

    The class R
    """

class ShadedPolygon(Widget, LineShape):
    angle: int
    fillColorStart: Incomplete
    fillColorEnd: Incomplete
    cylinderMode: int
    numShades: int
    points: Incomplete
    def __init__(self, **kw) -> None: ...
    def draw(self): ...
    # NOTE: widgets don't implement this, only actual shapes
    def copy(self) -> NoReturn:
        """Return a clone of this shape."""
