"""Base class for user-defined graphical widgets"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics import shapes
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]

class PropHolder:
    """Base for property holders"""

    def verify(self) -> None:
        """If the _attrMap attribute is not None, this
        checks all expected attributes are present; no
        unwanted attributes are present; and (if a
        checking function is found) checks each
        attribute has a valid value.  Either succeeds
        or raises an informative exception.
        """

    def __setattr__(self, name, value) -> None:
        """By default we verify.  This could be off
        in some parallel base classes.
        """

    def getProperties(self, recur: int = 1):
        """Returns a list of all properties which can be edited and
        which are not marked as private. This may include 'child
        widgets' or 'primitive shapes'.  You are free to override
        this and provide alternative implementations; the default
        one simply returns everything without a leading underscore.
        """

    def setProperties(self, propDict) -> None:
        """Permits bulk setting of properties.  These may include
        child objects e.g. "chart.legend.width = 200".

        All assignments will be validated by the object as if they
        were set individually in python code.

        All properties of a top-level object are guaranteed to be
        set before any of the children, which may be helpful to
        widget designers.
        """

    def dumpProperties(self, prefix: str = "") -> None:
        """Convenience. Lists them on standard output.  You
        may provide a prefix - mostly helps to generate code
        samples for documentation.
        """

class Widget(PropHolder, shapes.UserNode):
    """Base for all user-defined widgets.  Keep as simple as possible. Does
    not inherit from Shape so that we can rewrite shapes without breaking
    widgets and vice versa.
    """

    # TODO: draw should probably be marked abstract
    def draw(self) -> None: ...
    def demo(self) -> None: ...
    def provideNode(self) -> shapes.Shape: ...
    def getBounds(self) -> tuple[float, float, float, float]:
        """Return outer boundary as x1,y1,x2,y2.  Can be overridden for efficiency"""

class ScaleWidget(Widget):
    """Contents with a scale and offset"""

    x: Incomplete
    y: Incomplete
    contents: Incomplete
    scale: Incomplete
    def __init__(self, x: int = 0, y: int = 0, scale: float = 1.0, contents=None) -> None: ...
    def draw(self): ...

class CloneMixin:
    def clone(self, **kwds): ...

class TypedPropertyCollection(PropHolder):
    """A container with properties for objects of the same kind.

    This makes it easy to create lists of objects. You initialize
    it with a class of what it is to contain, and that is all you
    can add to it.  You can assign properties to the collection
    as a whole, or to a numeric index within it; if so it creates
    a new child object to hold that data.

    So:
        wedges = TypedPropertyCollection(WedgeProperties)
        wedges.strokeWidth = 2                # applies to all
        wedges.strokeColor = colors.red       # applies to all
        wedges[3].strokeColor = colors.blue   # only to one

    The last line should be taken as a prescription of how to
    create wedge no. 3 if one is needed; no error is raised if
    there are only two data points.

    We try and make sensible use of tuple indices.
        line[(3,x)] is backed by line[(3,)] == line[3] & line
    """

    def __init__(self, exampleClass, **kwds) -> None: ...
    def wKlassFactory(self, Klass): ...
    def __getitem__(self, x): ...
    def __contains__(self, key) -> bool: ...
    def __setitem__(self, key, value) -> None: ...
    def __len__(self) -> int: ...
    def getProperties(self, recur: int = 1): ...
    def setVector(self, **kw) -> None: ...
    def __getattr__(self, name): ...
    def __setattr__(self, name, value): ...
    def checkAttr(self, key, a, default=None): ...

def tpcGetItem(obj, x):
    """return obj if it's not a TypedPropertyCollection else obj[x]"""

def isWKlass(obj): ...

class StyleProperties(PropHolder):
    """A container class for attributes used in charts and legends.

    Attributes contained can be those for any graphical element
    (shape?) in the ReportLab graphics package. The idea for this
    container class is to be useful in combination with legends
    and/or the individual appearance of data series in charts.

    A legend could be as simple as a wrapper around a list of style
    properties, where the 'desc' attribute contains a descriptive
    string and the rest could be used by the legend e.g. to draw
    something like a color swatch. The graphical presentation of
    the legend would be its own business, though.

    A chart could be inspecting a legend or, more directly, a list
    of style properties to pick individual attributes that it knows
    about in order to render a particular row of the data. A bar
    chart e.g. could simply use 'strokeColor' and 'fillColor' for
    drawing the bars while a line chart could also use additional
    ones like strokeWidth.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize with attributes if any."""

    def __setattr__(self, name, value) -> None:
        """Verify attribute name and value, before setting it."""

class TwoCircles(Widget):
    leftCircle: Incomplete
    rightCircle: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class Face(Widget):
    """This draws a face with two eyes.

    It exposes a couple of properties
    to configure itself and hides all other details.
    """

    x: int
    y: int
    size: int
    skinColor: Incomplete
    eyeColor: Incomplete
    mood: str
    def __init__(self) -> None: ...
    def demo(self) -> None: ...
    def draw(self): ...

class TwoFaces(Widget):
    faceOne: Incomplete
    faceTwo: Incomplete
    def __init__(self) -> None: ...
    def draw(self):
        """Just return a group"""

    def demo(self) -> None:
        """The default case already looks good enough,
        no implementation needed here
        """

class Sizer(Widget):
    """Container to show size of all enclosed objects"""

    contents: Incomplete
    fillColor: Incomplete
    strokeColor: Incomplete
    def __init__(self, *elements) -> None: ...
    def add(self, node, name=None) -> None:
        """Appends non-None child node to the 'contents' attribute. In addition,
        if a name is provided, it is subsequently accessible by name
        """

    def getBounds(self): ...
    def draw(self): ...

class CandleStickProperties(PropHolder):
    strokeWidth: Incomplete
    strokeColor: Incomplete
    strokeDashArray: Incomplete
    crossWidth: Incomplete
    crossLo: Incomplete
    crossHi: Incomplete
    boxWidth: Incomplete
    boxFillColor: Incomplete
    boxStrokeColor: Incomplete
    boxStrokeWidth: Incomplete
    boxStrokeDashArray: Incomplete
    boxLo: Incomplete
    boxMid: Incomplete
    boxHi: Incomplete
    boxSides: Incomplete
    position: Incomplete
    candleKind: Incomplete
    axes: Incomplete
    chart: Incomplete
    def __init__(self, **kwds) -> None: ...
    def __call__(self, _x, _y, _size, _color):
        """the symbol interface"""

def CandleSticks(**kwds): ...
def test() -> None: ...
