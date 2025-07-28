"""Core of the graphics library - defines Drawing and Shapes"""

from _typeshed import Incomplete, SupportsItems
from abc import abstractmethod
from collections.abc import Iterable, Sequence
from typing import Any, Final, Literal, NoReturn, TypedDict
from typing_extensions import Self, TypeAlias, Unpack

from reportlab.lib.colors import Color
from reportlab.lib.validators import NoneOr, Validator
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable
from reportlab.platypus.flowables import _HAlignment, _VAlignment

_IntBool: TypeAlias = Literal[0, 1]
_BoolLike: TypeAlias = _IntBool | bool
_PathOp: TypeAlias = (
    tuple[Literal["moveTo"], float, float]
    | tuple[Literal["lineTo"], float, float]
    | tuple[Literal["curveTo"], float, float, float, float, float, float]
    # close path may either be a tuple or just the string
    | Literal["closePath"]
    | tuple[Literal["closePath"]]
    # fallback for list that is not type safe
    | list[Any]
)

# NOTE: These are derived from _attrMap and can optionally be
#       verified at runtime
class _GroupKwArgs(TypedDict, total=False):
    transform: tuple[float, float, float, float, float, float] | list[float] | list[int]
    # NOTE: This should be used with care, since it will replace elements
    #       it's mostly useful for circumventing validation logic and
    #       reusing the list, rather than populating a new list
    contents: list[Shape]
    strokeOverprint: _BoolLike
    fillOverprint: _BoolLike
    overprintMask: _BoolLike

class _DrawingKwArgs(_GroupKwArgs, total=False):
    # TODO: Restrict to supported formats?
    formats: list[str] | tuple[str, ...]
    # NOTE: This looks like an implementation detail, so we may not
    #       want to include this in KwArgs
    canv: Canvas
    background: Shape | UserNode | None
    # NOTE: The runtime validation for alignments is incorrect, so
    #       we assume it is turned off and allow all valid values
    hAlign: _HAlignment
    vAlign: _VAlignment
    renderScale: float
    initialFontName: str | None
    initialFontSize: float | None

class _LineShapeKwArgs(TypedDict, total=False):
    strokeColor: Color | None
    strokeWidth: float
    strokeLineCap: Literal[0, 1, 2]
    strokeLineJoin: Literal[0, 1, 2]
    strokeMiterLimit: float
    strokeDashArray: Sequence[float] | tuple[float, Sequence[float]]
    strokeOpacity: float | None
    strokeOverprint: _BoolLike
    overprintMask: _BoolLike

class _PathKwArgs(_LineShapeKwArgs, total=False):
    fillColor: Color | None
    fillOpacity: float
    fillOverprint: _BoolLike

class _AllPathKwArgs(_PathKwArgs, total=False):
    points: list[float] | None
    operators: list[float] | None
    isClipPath: _BoolLike
    autoclose: Literal["svg", "pdf"] | None
    fillMode: Literal[0, 1]

class _SolidShapeKwArgs(_PathKwArgs, total=False):
    fillMode: Literal[0, 1]

class _DefinePathKwArgs(_SolidShapeKwArgs, total=False):
    autoclose: Literal["svg", "pdf"] | None
    bbox: tuple[float, float, float, float] | None

class _WedgeKwArgs(_SolidShapeKwArgs, total=False):
    radius1: float | None
    yradius1: float | None

class _StringKwArgs(TypedDict, total=False):
    fontName: str
    fontSize: float
    fillColor: Color | None
    textAnchor: Literal["start", "middle", "end", "numeric"]
    encoding: str
    textRenderMode: Literal[0, 1, 2, 3, 4, 5, 6, 7]

__version__: Final[str]
isOpacity: NoneOr
NON_ZERO_WINDING: Final[str]
EVEN_ODD: Final[str]
STATE_DEFAULTS: Final[Incomplete]

class _DrawTimeResizeable:
    """Addin class to provide the horribleness of _drawTimeResize"""

class _SetKeyWordArgs:
    def __init__(self, keywords: SupportsItems[str, Any] = {}) -> None:
        """In general properties may be supplied to the constructor."""

def getRectsBounds(rectList): ...
def getPathBounds(points): ...
def getPointsBounds(pointList):
    """Helper function for list of points"""

class Shape(_SetKeyWordArgs, _DrawTimeResizeable):
    """Base class for all nodes in the tree. Nodes are simply
    packets of data to be created, stored, and ultimately
    rendered - they don't do anything active.  They provide
    convenience methods for verification but do not
    check attribiute assignments or use any clever setattr
    tricks this time.
    """

    @abstractmethod
    def copy(self) -> Self:
        """Return a clone of this shape."""

    def getProperties(self, recur: int = 1) -> dict[str, Any]:
        """Interface to make it easy to extract automatic
        documentation
        """

    def setProperties(self, props) -> None:
        """Supports the bulk setting if properties from,
        for example, a GUI application or a config file.
        """

    def dumpProperties(self, prefix: str = "") -> None:
        """Convenience. Lists them on standard output.  You
        may provide a prefix - mostly helps to generate code
        samples for documentation.
        """

    def verify(self) -> None:
        """If the programmer has provided the optional
        _attrMap attribute, this checks all expected
        attributes are present; no unwanted attributes
        are present; and (if a checking function is found)
        checks each attribute.  Either succeeds or raises
        an informative exception.
        """

    @abstractmethod
    def getBounds(self) -> tuple[float, float, float, float]:
        """Returns bounding rectangle of object as (x1,y1,x2,y2)"""

class Group(Shape):
    """Groups elements together.  May apply a transform
    to its contents.  Has a publicly accessible property
    'contents' which may be used to iterate over contents.
    In addition, child nodes may be given a name in which
    case they are subsequently accessible as properties.
    """

    contents: list[Shape]
    transform: tuple[float, float, float, float, float, float] | list[float] | list[int]
    def __init__(self, *elements: Shape | UserNode, **keywords: Unpack[_GroupKwArgs]) -> None:
        """Initial lists of elements may be provided to allow
        compact definitions in literal Python code.  May or
        may not be useful.
        """

    def add(self, node: Shape | UserNode, name: str | None = None) -> None:
        """Appends non-None child node to the 'contents' attribute. In addition,
        if a name is provided, it is subsequently accessible by name
        """

    def insert(self, i: int, n: Shape | UserNode, name: str | None = None) -> None:
        """Inserts sub-node n in contents at specified location"""

    def expandUserNodes(self) -> Group:
        """Return a new object which only contains primitive shapes."""

    def copy(self) -> Self:
        """returns a copy"""

    def rotate(self, theta: float, cx: float = 0, cy: float = 0) -> None:
        """Convenience to help you set transforms"""

    def translate(self, dx: float, dy: float = 0) -> None:
        """Convenience to help you set transforms"""

    def scale(self, sx: float, sy: float = 1) -> None:
        """Convenience to help you set transforms"""

    def skew(self, kx: float, ky: float = 0) -> None:
        """Convenience to help you set transforms"""

    def shift(self, x: float, y: float = 0) -> None:
        """Convenience function to set the origin arbitrarily"""
    # NOTE: This changes the object to a Drawing, rather than returning
    #       a new one, which is not ideal...
    def asDrawing(self, width: float, height: float) -> None:
        """Convenience function to make a drawing from a group
        After calling this the instance will be a drawing!
        """

    def getContents(self) -> list[Shape | UserNode]:
        """Return the list of things to be rendered
        override to get more complicated behaviour
        """

    def getBounds(self) -> tuple[float, float, float, float]: ...

class Drawing(Group, Flowable):
    """Outermost container; the thing a renderer works on.
    This has no properties except a height, width and list
    of contents.
    """

    background: Shape | UserNode | None
    renderScale: float
    def __init__(
        self, width: float = 400, height: float = 200, *nodes: Shape | UserNode, **keywords: Unpack[_DrawingKwArgs]
    ) -> None: ...
    def draw(self, showBoundary=...) -> None:
        """This is used by the Platypus framework to let the document
        draw itself in a story.  It is specific to PDF and should not
        be used directly.
        """

    def expandUserNodes(self) -> Drawing:
        """Return a new drawing which only contains primitive shapes."""

    def asGroup(self, *args: Shape | UserNode, **kw: Unpack[_GroupKwArgs]) -> Group: ...
    def save(
        self,
        formats: Iterable[str] | None = None,
        verbose: bool | None = None,
        fnRoot: str | None = None,
        outDir: str | None = None,
        title: str = "",
        **kw,
    ):
        """Saves copies of self in desired location and formats.
        Multiple formats can be supported in one call

        the extra keywords can be of the form
        _renderPM_dpi=96 (which passes dpi=96 to renderPM)
        """

    def asString(self, format: str, verbose: bool | None = None, preview: int = 0, **kw) -> str:
        """Converts to an 8 bit string in given format."""

    def resized(
        self, kind: Literal["fit", "fitx", "fity"] = "fit", lpad: float = 0, rpad: float = 0, bpad: float = 0, tpad: float = 0
    ) -> Drawing:
        """return a base class drawing which ensures all the contents fits"""

class _DrawingEditorMixin:
    """This is a mixin to provide functionality for edited drawings"""

class _isStrokeDashArray(Validator):
    def test(self, x): ...

isStrokeDashArray: _isStrokeDashArray

class LineShape(Shape):
    strokeColor: Color | None
    strokeWidth: float
    strokeLineCap: Literal[0, 1, 2]
    strokeLineJoin: Literal[0, 1, 2]
    strokeMiterLimit: float
    strokeDashArray: Sequence[float] | tuple[float, Sequence[float]]
    strokeOpacity: float | None
    def __init__(self, kw: _LineShapeKwArgs) -> None: ...
    @abstractmethod
    def copy(self) -> Self:
        """Return a clone of this shape."""

    @abstractmethod
    def getBounds(self) -> tuple[float, float, float, float]:
        """Returns bounding rectangle of object as (x1,y1,x2,y2)"""

class Line(LineShape):
    x1: float
    y1: float
    x2: float
    y2: float
    def __init__(self, x1: float, y1: float, x2: float, y2: float, **kw: Unpack[_LineShapeKwArgs]) -> None: ...
    # NOTE: For some reason Line doesn't implement copy
    def copy(self) -> NoReturn:
        """Return a clone of this shape."""

    def getBounds(self) -> tuple[float, float, float, float]:
        """Returns bounding rectangle of object as (x1,y1,x2,y2)"""

class SolidShape(LineShape):
    fillColor: Color | None
    fillOpacity: float | None
    def __init__(self, kw: _SolidShapeKwArgs) -> None: ...
    @abstractmethod
    def copy(self) -> Self:
        """Return a clone of this shape."""

    @abstractmethod
    def getBounds(self) -> tuple[float, float, float, float]:
        """Returns bounding rectangle of object as (x1,y1,x2,y2)"""

class Path(SolidShape):
    """Path, made up of straight lines and bezier curves."""

    points: list[float]
    operators: list[float]
    isClipPath: _BoolLike
    autoclose: Literal["svg", "pdf"] | None
    fillMode: Literal[0, 1]
    def __init__(
        self,
        points: list[float] | None = None,
        operators: list[float] | None = None,
        isClipPath: _BoolLike = 0,
        autoclose: Literal["svg", "pdf"] | None = None,
        fillMode: Literal[0, 1] = 0,
        **kw: Unpack[_PathKwArgs],
    ) -> None: ...
    def copy(self) -> Self: ...
    def moveTo(self, x: float, y: float) -> None: ...
    def lineTo(self, x: float, y: float) -> None: ...
    def curveTo(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None: ...
    def closePath(self) -> None: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

EmptyClipPath: Final[Path]

def getArcPoints(
    centerx: float,
    centery: float,
    radius: float,
    startangledegrees: float,
    endangledegrees: float,
    yradius: float | None = None,
    degreedelta: float | None = None,
    reverse: _BoolLike | None = None,
) -> list[float]: ...

class ArcPath(Path):
    """Path with an addArc method"""

    def addArc(
        self,
        centerx: float,
        centery: float,
        radius: float,
        startangledegrees: float,
        endangledegrees: float,
        yradius: float | None = None,
        degreedelta: float | None = None,
        moveTo: _BoolLike | None = None,
        reverse: _BoolLike | None = None,
    ) -> None: ...

def definePath(
    pathSegs: Iterable[_PathOp] = [], isClipPath: _BoolLike = 0, dx: float = 0, dy: float = 0, **kw: Unpack[_DefinePathKwArgs]
) -> Path: ...

class Rect(SolidShape):
    """Rectangle, possibly with rounded corners."""

    x: float
    y: float
    width: float
    height: float
    rx: float
    ry: float
    def __init__(
        self, x: float, y: float, width: float, height: float, rx: float = 0, ry: float = 0, **kw: _SolidShapeKwArgs
    ) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Image(SolidShape):
    """Bitmap image."""

    x: float
    y: float
    width: float
    height: float
    path: Incomplete
    def __init__(self, x: float, y: float, width: float, height: float, path, **kw: Unpack[_SolidShapeKwArgs]) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Circle(SolidShape):
    cx: float
    cy: float
    r: float
    def __init__(self, cx: float, cy: float, r: float, **kw: Unpack[_SolidShapeKwArgs]) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Ellipse(SolidShape):
    cx: float
    cy: float
    rx: float
    ry: float
    def __init__(self, cx: float, cy: float, rx: float, ry: float, **kw: Unpack[_SolidShapeKwArgs]) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Wedge(SolidShape):
    """A "slice of a pie" by default translates to a polygon moves anticlockwise
    from start angle to end angle
    """

    centerx: float
    centery: float
    radius: float
    startangledegrees: float
    endangledegrees: float
    yradius: float | None
    annular: bool
    # NOTE: This one is not actually settable on the instance if runtime validation
    #       is turned on, but it seems bad to disallow it anyways
    degreedelta: float
    def __init__(
        self,
        centerx: float,
        centery: float,
        radius: float,
        startangledegrees: float,
        endangledegrees: float,
        yradius: float | None = None,
        annular: bool = False,
        **kw: Unpack[_WedgeKwArgs],
    ) -> None: ...
    def asPolygon(self) -> Path | Polygon: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Polygon(SolidShape):
    """Defines a closed shape; Is implicitly
    joined back to the start for you.
    """

    points: list[float]
    def __init__(self, points: list[float] = [], **kw: Unpack[_SolidShapeKwArgs]) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class PolyLine(LineShape):
    """Series of line segments.  Does not define a
    closed shape; never filled even if apparently joined.
    Put the numbers in the list, not two-tuples.
    """

    points: list[float]
    def __init__(self, points: list[float] = [], **kw: Unpack[_SolidShapeKwArgs]) -> None: ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class Hatching(Path):
    """define a hatching of a set of polygons defined by lists of the form [x0,y0,x1,y1,....,xn,yn]"""

    xyLists: Sequence[tuple[float, float]]
    angles: Sequence[float]
    spacings: Sequence[float]
    def __init__(
        self,
        spacings: float | Sequence[float] = 2,
        angles: float | Sequence[float] = 45,
        xyLists: Sequence[tuple[float, float] | list[float]] = [],
        **kwds: Unpack[_AllPathKwArgs],
    ) -> None: ...

def numericXShift(
    tA, text: str, w: float, fontName: str, fontSize: float, encoding: str | None = None, pivotCharacter: str = "."
) -> float: ...

class String(Shape):
    """Not checked against the spec, just a way to make something work.
    Can be anchored left, middle or end.
    """

    encoding: str
    x: float
    y: float
    text: str
    textAnchor: Literal["start", "middle", "end", "numeric"]
    fontName: str
    fontSize: float
    fillColor: Color | None
    def __init__(self, x: float, y: float, text: str, **kw: Unpack[_StringKwArgs]) -> None: ...
    def getEast(self): ...
    def copy(self) -> Self: ...
    def getBounds(self) -> tuple[float, float, float, float]: ...

class UserNode(_DrawTimeResizeable):
    """A simple template for creating a new node.  The user (Python
    programmer) may subclasses this.  provideNode() must be defined to
    provide a Shape primitive when called by a renderer.  It does
    NOT inherit from Shape, as the renderer always replaces it, and
    your own classes can safely inherit from it without getting
    lots of unintended behaviour.
    """

    @abstractmethod
    def provideNode(self) -> Shape:
        """Override this to create your own node. This lets widgets be
        added to drawings; they must create a shape (typically a group)
        so that the renderer can draw the custom node.
        """

class DirectDraw(Shape):
    """try to draw directly on the canvas"""

    @abstractmethod
    def drawDirectly(self, canvas: Canvas) -> None: ...

def test() -> None: ...
