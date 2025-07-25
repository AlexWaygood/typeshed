"""This modules defines a very preliminary Line Chart example."""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.areas import PlotArea
from reportlab.graphics.widgetbase import PropHolder
from reportlab.lib.attrmap import *

__version__: Final[str]

class LineChartProperties(PropHolder): ...

class AbstractLineChart(PlotArea):
    def makeSwatchSample(self, rowNo, x, y, width, height): ...
    def getSeriesName(self, i, default=None):
        """return series name i or default"""

class LineChart(AbstractLineChart): ...

class HorizontalLineChart(LineChart):
    """Line chart with multiple lines.

    A line chart is assumed to have one category and one value axis.
    Despite its generic name this particular line chart class has
    a vertical value axis and a horizontal category one. It may
    evolve into individual horizontal and vertical variants (like
    with the existing bar charts).

    Available attributes are:

        x: x-position of lower-left chart origin
        y: y-position of lower-left chart origin
        width: chart width
        height: chart height

        useAbsolute: disables auto-scaling of chart elements (?)
        lineLabelNudge: distance of data labels to data points
        lineLabels: labels associated with data values
        lineLabelFormat: format string or callback function
        groupSpacing: space between categories

        joinedLines: enables drawing of lines

        strokeColor: color of chart lines (?)
        fillColor: color for chart background (?)
        lines: style list, used cyclically for data series

        valueAxis: value axis object
        categoryAxis: category axis object
        categoryNames: category names

        data: chart data, a list of data series of equal length
    """

    strokeColor: Incomplete
    fillColor: Incomplete
    categoryAxis: Incomplete
    valueAxis: Incomplete
    data: Incomplete
    categoryNames: Incomplete
    lines: Incomplete
    useAbsolute: int
    groupSpacing: int
    lineLabels: Incomplete
    lineLabelFormat: Incomplete
    lineLabelArray: Incomplete
    lineLabelNudge: int
    joinedLines: int
    inFill: int
    reversePlotOrder: int
    def __init__(self) -> None: ...
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
    def draw(self):
        """Draws itself."""

class _FakeGroup:
    def __init__(self) -> None: ...
    def add(self, what) -> None: ...
    def value(self): ...
    def sort(self) -> None: ...

class HorizontalLineChart3D(HorizontalLineChart):
    theta_x: float
    theta_y: float
    zDepth: int
    zSpace: int
    def calcPositions(self) -> None: ...
    def makeLines(self): ...

class VerticalLineChart(LineChart): ...

def sample1(): ...

class SampleHorizontalLineChart(HorizontalLineChart):
    """Sample class overwriting one method to draw additional horizontal lines."""

    def demo(self):
        """Shows basic use of a line chart."""

    def makeBackground(self): ...

def sample1a(): ...
def sample2(): ...
def sample3(): ...
def sampleCandleStick(): ...
