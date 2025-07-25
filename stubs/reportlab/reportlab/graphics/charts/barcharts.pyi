"""This module defines a variety of Bar Chart components.

The basic flavors are stacked and side-by-side, available in horizontal and
vertical versions.

"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.areas import PlotArea
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgetbase import PropHolder

__version__: Final[str]

class BarChartProperties(PropHolder):
    strokeColor: Incomplete
    fillColor: Incomplete
    strokeWidth: float
    symbol: Incomplete
    strokeDashArray: Incomplete
    def __init__(self) -> None: ...

class BarChart(PlotArea):
    """Abstract base class, unusable by itself."""

    def makeSwatchSample(self, rowNo, x, y, width, height): ...
    def getSeriesName(self, i, default=None):
        """return series name i or default"""
    categoryAxis: Incomplete
    valueAxis: Incomplete
    barSpacing: int
    reversePlotOrder: int
    data: Incomplete
    useAbsolute: int
    barWidth: int
    groupSpacing: int
    barLabels: Incomplete
    barLabelFormat: Incomplete
    barLabelArray: Incomplete
    bars: Incomplete
    naLabel: Incomplete
    zIndexOverrides: Incomplete
    def __init__(self) -> None: ...
    def demo(self):
        """Shows basic use of a bar chart"""

    def getSeriesOrder(self) -> None: ...
    def calcBarPositions(self) -> None:
        """Works out where they go. default vertical.

        Sets an attribute _barPositions which is a list of
        lists of (x, y, width, height) matching the data.
        """

    def makeBars(self): ...
    def draw(self): ...

class VerticalBarChart(BarChart):
    """Vertical bar chart with multiple side-by-side bars."""

class HorizontalBarChart(BarChart):
    """Horizontal bar chart with multiple side-by-side bars."""

class _FakeGroup:
    def __init__(self, cmp=None) -> None: ...
    def add(self, what) -> None: ...
    def value(self): ...
    def sort(self) -> None: ...

class BarChart3D(BarChart):
    theta_x: float
    theta_y: float
    zDepth: Incomplete
    zSpace: Incomplete
    def calcBarPositions(self) -> None: ...
    def makeBars(self): ...

class VerticalBarChart3D(BarChart3D, VerticalBarChart): ...
class HorizontalBarChart3D(BarChart3D, HorizontalBarChart): ...

def sampleV0a():
    """A slightly pathologic bar chart with only TWO data items."""

def sampleV0b():
    """A pathologic bar chart with only ONE data item."""

def sampleV0c():
    """A really pathologic bar chart with NO data items at all!"""

def sampleV1():
    """Sample of multi-series bar chart."""

def sampleV2a():
    """Sample of multi-series bar chart."""

def sampleV2b():
    """Sample of multi-series bar chart."""

def sampleV2c():
    """Sample of multi-series bar chart."""

def sampleV3():
    """Faked horizontal bar chart using a vertical real one (deprecated)."""

def sampleV4a():
    """A bar chart showing value axis region starting at *exactly* zero."""

def sampleV4b():
    """A bar chart showing value axis region starting *below* zero."""

def sampleV4c():
    """A bar chart showing value axis region staring *above* zero."""

def sampleV4d():
    """A bar chart showing value axis region entirely *below* zero."""

dataSample5: Incomplete

def sampleV5a():
    """A simple bar chart with no expressed spacing attributes."""

def sampleV5b():
    """A simple bar chart with proportional spacing."""

def sampleV5c1():
    """Make sampe simple bar chart but with absolute spacing."""

def sampleV5c2():
    """Make sampe simple bar chart but with absolute spacing."""

def sampleV5c3():
    """Make sampe simple bar chart but with absolute spacing."""

def sampleV5c4():
    """Make sampe simple bar chart but with absolute spacing."""

def sampleH0a():
    """Make a slightly pathologic bar chart with only TWO data items."""

def sampleH0b():
    """Make a pathologic bar chart with only ONE data item."""

def sampleH0c():
    """Make a really pathologic bar chart with NO data items at all!"""

def sampleH1():
    """Sample of multi-series bar chart."""

def sampleH2a():
    """Sample of multi-series bar chart."""

def sampleH2b():
    """Sample of multi-series bar chart."""

def sampleH2c():
    """Sample of multi-series bar chart."""

def sampleH3():
    """A really horizontal bar chart (compared to the equivalent faked one)."""

def sampleH4a():
    """A bar chart showing value axis region starting at *exactly* zero."""

def sampleH4b():
    """A bar chart showing value axis region starting *below* zero."""

def sampleH4c():
    """A bar chart showing value axis region starting *above* zero."""

def sampleH4d():
    """A bar chart showing value axis region entirely *below* zero."""

def sampleH5a():
    """A simple bar chart with no expressed spacing attributes."""

def sampleH5b():
    """A simple bar chart with proportional spacing."""

def sampleH5c1():
    """A simple bar chart with absolute spacing."""

def sampleH5c2():
    """Simple bar chart with absolute spacing."""

def sampleH5c3():
    """Simple bar chart with absolute spacing."""

def sampleH5c4():
    """Simple bar chart with absolute spacing."""

def sampleSymbol1():
    """Simple bar chart using symbol attribute."""

def sampleStacked1():
    """Simple bar chart using symbol attribute."""

class SampleH5c4(Drawing):
    """Simple bar chart with absolute spacing."""

    def __init__(self, width: int = 400, height: int = 200, *args, **kw) -> None: ...
