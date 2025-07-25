"""Basic Pie Chart class.

This permits you to customize and pop out individual wedges;
supports elliptical and circular pies.
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.areas import PlotArea
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.widgetbase import PropHolder
from reportlab.lib.attrmap import *

__version__: Final[str]

class WedgeLabel(Label): ...

class WedgeProperties(PropHolder):
    """This holds descriptive information about the wedges in a pie chart.

    It is not to be confused with the 'wedge itself'; this just holds
    a recipe for how to format one, and does not allow you to hack the
    angles.  It can format a genuine Wedge object for you with its
    format method.
    """

    strokeWidth: int
    fillColor: Incomplete
    strokeColor: Incomplete
    strokeDashArray: Incomplete
    strokeLineJoin: int
    strokeLineCap: int
    strokeMiterLimit: int
    popout: int
    fontName: Incomplete
    fontSize: Incomplete
    fontColor: Incomplete
    labelRadius: float
    label_dx: int
    label_text: Incomplete
    label_topPadding: int
    label_boxAnchor: str
    label_boxStrokeColor: Incomplete
    label_boxStrokeWidth: float
    label_boxFillColor: Incomplete
    label_strokeColor: Incomplete
    label_strokeWidth: float
    label_leading: Incomplete
    label_textAnchor: str
    label_simple_pointer: int
    label_visible: int
    label_pointer_strokeColor: Incomplete
    label_pointer_strokeWidth: float
    label_pointer_elbowLength: int
    label_pointer_edgePad: int
    label_pointer_piePad: int
    visible: int
    shadingKind: Incomplete
    shadingAmount: float
    shadingAngle: float
    shadingDirection: str
    def __init__(self) -> None: ...

class AbstractPieChart(PlotArea):
    def makeSwatchSample(self, rowNo, x, y, width, height): ...
    def getSeriesName(self, i, default=None):
        """return series name i or default"""

def boundsOverlap(P, Q): ...
def findOverlapRun(B, wrap: int = 1):
    """determine a set of overlaps in bounding boxes B or return None"""

def fixLabelOverlaps(L, sideLabels: bool = False, mult0: float = 1.0) -> None: ...
def intervalIntersection(A, B): ...
def theta0(data, direction): ...

class AngleData(float):
    """use this to carry the data along with the angle"""

    def __new__(cls, angle, data): ...

class Pie(AbstractPieChart):
    other_threshold: Incomplete
    x: int
    y: int
    width: int
    height: int
    data: Incomplete
    labels: Incomplete
    startAngle: int
    direction: str
    simpleLabels: int
    checkLabelOverlap: int
    pointerLabelMode: Incomplete
    sameRadii: bool
    orderMode: str
    xradius: Incomplete
    sideLabels: int
    sideLabelsOffset: float
    slices: Incomplete
    angleRange: int
    def __init__(self, *, angleRange: int = 360, **kwds) -> None: ...
    def demo(self): ...
    centerx: Incomplete
    centery: Incomplete
    yradius: Incomplete
    lu: Incomplete
    ru: Incomplete
    def makePointerLabels(self, angles, plMode): ...
    def normalizeData(self, keepData: bool = False): ...
    def makeAngles(self): ...
    def makeWedges(self): ...
    def draw(self): ...

class LegendedPie(Pie):
    """Pie with a two part legend (one editable with swatches, one hidden without swatches)."""

    x: int
    y: int
    height: int
    width: int
    data: Incomplete
    labels: Incomplete
    direction: str
    pieAndLegend_colors: Incomplete
    legendNumberOffset: int
    legendNumberFormat: str
    legend_data: Incomplete
    legend1: Incomplete
    legend_names: Incomplete
    leftPadding: int
    rightPadding: int
    topPadding: int
    bottomPadding: int
    drawLegend: int
    def __init__(self) -> None: ...
    def draw(self): ...
    def demo(self, drawing=None): ...

class Wedge3dProperties(PropHolder):
    """This holds descriptive information about the wedges in a pie chart.

    It is not to be confused with the 'wedge itself'; this just holds
    a recipe for how to format one, and does not allow you to hack the
    angles.  It can format a genuine Wedge object for you with its
    format method.
    """

    strokeWidth: int
    shading: float
    visible: int
    strokeColorShaded: Incomplete
    strokeColor: Incomplete
    strokeDashArray: Incomplete
    popout: int
    fontName: Incomplete
    fontSize: Incomplete
    fontColor: Incomplete
    labelRadius: float
    label_dx: int
    label_text: Incomplete
    label_topPadding: int
    label_boxAnchor: str
    label_boxStrokeColor: Incomplete
    label_boxStrokeWidth: float
    label_boxFillColor: Incomplete
    label_strokeColor: Incomplete
    label_strokeWidth: float
    label_leading: Incomplete
    label_textAnchor: str
    label_visible: int
    label_simple_pointer: int
    def __init__(self) -> None: ...

class _SL3D:
    lo: Incomplete
    hi: Incomplete
    mid: Incomplete
    not360: Incomplete
    def __init__(self, lo, hi) -> None: ...

class Pie3d(Pie):
    perspective: int
    depth_3d: int
    angle_3d: int
    def CX(self, i, d): ...
    def CY(self, i, d): ...
    def OX(self, i, o, d): ...
    def OY(self, i, o, d): ...
    def rad_dist(self, a): ...
    slices: Incomplete
    xradius: Incomplete
    width: int
    height: int
    data: Incomplete
    def __init__(self) -> None: ...
    dy: Incomplete
    def draw(self): ...
    def demo(self): ...

def sample0a():
    """Make a degenerated pie chart with only one slice."""

def sample0b():
    """Make a degenerated pie chart with only one slice."""

def sample1():
    """Make a typical pie chart with with one slice treated in a special way."""

def sample2():
    """Make a pie chart with nine slices."""

def sample3():
    """Make a pie chart with a very slim slice."""

def sample4():
    """Make a pie chart with several very slim slices."""

def sample5():
    """Make a pie with side labels."""

def sample6():
    """Illustrates the pie moving to leave space for the left labels"""

def sample7():
    """Case with overlapping pointers"""

def sample8():
    """Case with overlapping labels"""

def sample9():
    """Case with overlapping labels"""
