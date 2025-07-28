"""This module defines a very preliminary Line Plot example."""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.linecharts import AbstractLineChart
from reportlab.graphics.charts.utils import *
from reportlab.graphics.shapes import Polygon, _SetKeyWordArgs
from reportlab.graphics.widgetbase import PropHolder
from reportlab.graphics.widgets.grids import ShadedPolygon
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]

class LinePlotProperties(PropHolder): ...

class InFillValue(int):
    yValue: Incomplete
    def __new__(cls, v, yValue=None): ...

class Shader(_SetKeyWordArgs):
    def shade(self, lp, g, rowNo, rowColor, row) -> None: ...

class NoFiller:
    def fill(self, lp, g, rowNo, rowColor, points) -> None: ...

class Filler:
    """mixin providing simple polygon fill"""

    __dict__: Incomplete
    def __init__(self, **kw) -> None: ...
    def fill(self, lp, g, rowNo, rowColor, points) -> None: ...

class ShadedPolyFiller(Filler, ShadedPolygon): ...
class PolyFiller(Filler, Polygon): ...

class LinePlot(AbstractLineChart):
    """Line plot with multiple lines.

    Both x- and y-axis are value axis (so there are no seperate
    X and Y versions of this class).
    """

    reversePlotOrder: int
    xValueAxis: Incomplete
    yValueAxis: Incomplete
    data: Incomplete
    lines: Incomplete
    lineLabels: Incomplete
    lineLabelFormat: Incomplete
    lineLabelArray: Incomplete
    lineLabelNudge: int
    annotations: Incomplete
    behindAxes: int
    gridFirst: int
    def __init__(self) -> None: ...
    @property
    def joinedLines(self): ...
    @joinedLines.setter
    def joinedLines(self, v) -> None: ...
    def demo(self):
        """Shows basic use of a line chart."""

    def calcPositions(self) -> None:
        """Works out where they go.

        Sets an attribute _positions which is a list of
        lists of (x, y) matching the data.
        """

    def drawLabel(self, G, rowNo, colNo, x, y) -> None:
        """Draw a label for a given item in the list.
        G must have an add method
        """

    def makeLines(self): ...
    def draw(self): ...
    def addCrossHair(self, name, xv, yv, strokeColor=..., strokeWidth: int = 1, beforeLines: bool = True): ...

class LinePlot3D(LinePlot):
    theta_x: float
    theta_y: float
    zDepth: int
    zSpace: int
    def calcPositions(self) -> None: ...
    def makeLines(self): ...

class SimpleTimeSeriesPlot(LinePlot):
    """A customized version of LinePlot.
    It uses NormalDateXValueAxis() and AdjYValueAxis() for the X and Y axes.
    """

    xValueAxis: Incomplete
    yValueAxis: Incomplete
    data: Incomplete
    def __init__(self) -> None: ...

class GridLinePlot(SimpleTimeSeriesPlot):
    """A customized version of SimpleTimeSeriesSPlot.
    It uses NormalDateXValueAxis() and AdjYValueAxis() for the X and Y axes.
    The chart has a default grid background with thin horizontal lines
    aligned with the tickmarks (and labels). You can change the back-
    ground to be any Grid or ShadedRect, or scale the whole chart.
    If you do provide a background, you can specify the colours of the
    stripes with 'background.stripeColors'.
    """

    scaleFactor: Incomplete
    background: Incomplete
    def __init__(self) -> None: ...
    def demo(self, drawing=None): ...
    def draw(self): ...

class AreaLinePlot(LinePlot):
    """we're given data in the form [(X1,Y11,..Y1M)....(Xn,Yn1,...YnM)]"""

    reversePlotOrder: int
    data: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class SplitLinePlot(AreaLinePlot):
    xValueAxis: Incomplete
    yValueAxis: Incomplete
    data: Incomplete
    def __init__(self) -> None: ...

class ScatterPlot(LinePlot):
    """A scatter plot widget"""

    width: int
    height: int
    outerBorderOn: int
    outerBorderColor: Incomplete
    background: Incomplete
    xLabel: str
    yLabel: str
    data: Incomplete
    joinedLines: int
    leftPadding: int
    rightPadding: int
    topPadding: int
    bottomPadding: int
    x: Incomplete
    y: Incomplete
    lineLabelFormat: str
    lineLabelNudge: int
    def __init__(self) -> None: ...
    def demo(self, drawing=None): ...
    def draw(self): ...

def sample1a():
    """A line plot with non-equidistant points in x-axis."""

def sample1b():
    """A line plot with non-equidistant points in x-axis."""

def sample1c():
    """A line plot with non-equidistant points in x-axis."""

def preprocessData(series):
    """Convert date strings into seconds and multiply values by 100."""

def sample2():
    """A line plot with non-equidistant points in x-axis."""

def sampleFillPairedData(): ...
