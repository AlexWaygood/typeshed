"""Collection of axes for charts.

The current collection comprises axes for charts using cartesian
coordinate systems. All axes might have tick marks and labels.
There are two dichotomies for axes: one of X and Y flavours and
another of category and value flavours.

Category axes have an ordering but no metric. They are divided
into a number of equal-sized buckets. Their tick marks or labels,
if available, go BETWEEN the buckets, and the labels are placed
below to/left of the X/Y-axis, respectively.

  Value axes have an ordering AND metric. They correspond to a nu-
  meric quantity. Value axis have a real number quantity associated
  with it. The chart tells it where to go.
  The most basic axis divides the number line into equal spaces
  and has tickmarks and labels associated with each; later we
  will add variants where you can specify the sampling
  interval.

The charts using axis tell them where the labels should be placed.

Axes of complementary X/Y flavours can be connected to each other
in various ways, i.e. with a specific reference point, like an
x/value axis to a y/value (or category) axis. In this case the
connection can be either at the top or bottom of the former or
at any absolute value (specified in points) or at some value of
the former axes in its own coordinate system.
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.textlabels import PMVLabel
from reportlab.graphics.widgetbase import Widget
from reportlab.lib.attrmap import *
from reportlab.lib.validators import Validator

__version__: Final[str]

class AxisLabelAnnotation:
    """Create a grid like line using the given user value to draw the line
    v       value to use
    kwds may contain
    scaleValue  True/not given --> scale the value
                otherwise use the absolute value
    labelClass  the label class to use default Label
    all Label keywords are acceptable (including say _text)
    """

    def __init__(self, v, **kwds) -> None: ...
    def __call__(self, axis): ...

class AxisLineAnnotation:
    """Create a grid like line using the given user value to draw the line
    kwds may contain
    startOffset if true v is offset from the default grid start position
    endOffset   if true v is offset from the default grid end position
    scaleValue  True/not given --> scale the value
                otherwise use the absolute value
    lo          lowest coordinate to draw default 0
    hi          highest coordinate to draw at default = length
    drawAtLimit True draw line at appropriate limit if its coordinate exceeds the lo, hi range
                False ignore if it's outside the range
    all Line keywords are acceptable
    """

    def __init__(self, v, **kwds) -> None: ...
    def __call__(self, axis): ...

class AxisBackgroundAnnotation:
    """Create a set of coloured bars on the background of a chart using axis ticks as the bar borders
    colors is a set of colors to use for the background bars. A colour of None is just a skip.
    Special effects if you pass a rect or Shaded rect instead.
    """

    def __init__(self, colors, **kwds) -> None: ...
    def __call__(self, axis): ...

class TickLU:
    """lookup special cases for tick values"""

    accuracy: Incomplete
    T: Incomplete
    def __init__(self, *T, **kwds) -> None: ...
    def __contains__(self, t) -> bool: ...
    def __getitem__(self, t): ...

class _AxisG(Widget):
    def makeGrid(self, g, dim=None, parent=None, exclude=[]) -> None:
        """this is only called by a container object"""

    def getGridDims(self, start=None, end=None): ...
    @property
    def isYAxis(self): ...
    @property
    def isXAxis(self): ...
    def addAnnotations(self, g, A=None) -> None: ...
    def draw(self): ...

class CALabel(PMVLabel):
    def __init__(self, **kw) -> None: ...

class CategoryAxis(_AxisG):
    """Abstract category axis, unusable in itself."""

    visible: int
    visibleAxis: int
    visibleTicks: int
    visibleLabels: int
    visibleGrid: int
    drawGridLast: bool
    strokeWidth: int
    strokeColor: Incomplete
    strokeDashArray: Incomplete
    gridStrokeLineJoin: Incomplete
    gridStrokeLineCap: Incomplete
    gridStrokeMiterLimit: Incomplete
    gridStrokeWidth: float
    gridStrokeColor: Incomplete
    gridStrokeDashArray: Incomplete
    gridStart: Incomplete
    strokeLineJoin: Incomplete
    strokeLineCap: Incomplete
    strokeMiterLimit: Incomplete
    labels: Incomplete
    categoryNames: Incomplete
    joinAxis: Incomplete
    joinAxisPos: Incomplete
    joinAxisMode: Incomplete
    labelAxisMode: str
    reverseDirection: int
    style: str
    tickShift: int
    loPad: int
    hiPad: int
    loLLen: int
    hiLLen: int
    def __init__(self) -> None: ...
    def setPosition(self, x, y, length) -> None: ...
    def configure(self, multiSeries, barWidth=None) -> None: ...
    def scale(self, idx):
        """Returns the position and width in drawing units"""

    def midScale(self, idx):
        """Returns the bar mid position in drawing units"""

class _XTicks:
    @property
    def actualTickStrokeWidth(self): ...
    @property
    def actualTickStrokeColor(self): ...
    def makeTicks(self): ...

class _YTicks(_XTicks):
    def makeTicks(self): ...

class XCategoryAxis(_XTicks, CategoryAxis):
    """X/category axis"""

    tickUp: int
    tickDown: int
    def __init__(self) -> None: ...
    categoryNames: Incomplete
    def demo(self): ...
    def joinToAxis(self, yAxis, mode: str = "bottom", pos=None) -> None:
        """Join with y-axis using some mode."""

    def loScale(self, idx):
        """returns the x position in drawing units"""

    def makeAxis(self): ...
    def makeTickLabels(self): ...

class YCategoryAxis(_YTicks, CategoryAxis):
    """Y/category axis"""

    tickLeft: int
    tickRight: int
    def __init__(self) -> None: ...
    categoryNames: Incomplete
    def demo(self): ...
    def joinToAxis(self, xAxis, mode: str = "left", pos=None) -> None:
        """Join with x-axis using some mode."""

    def loScale(self, idx):
        """Returns the y position in drawing units"""

    def makeAxis(self): ...
    def makeTickLabels(self): ...

class TickLabeller:
    """Abstract base class which may be used to indicate a change
    in the call signature for callable label formats
    """

    def __call__(self, axis, value): ...

class ValueAxis(_AxisG):
    """Abstract value axis, unusable in itself."""

    def __init__(self, **kw) -> None: ...
    def setPosition(self, x, y, length) -> None: ...
    def configure(self, dataSeries) -> None:
        """Let the axis configure its scale and range based on the data.

        Called after setPosition. Let it look at a list of lists of
        numbers determine the tick mark intervals.  If valueMin,
        valueMax and valueStep are configured then it
        will use them; if any of them are set to None it
        will look at the data and make some sensible decision.
        You may override this to build custom axes with
        irregular intervals.  It creates an internal
        variable self._values, which is a list of numbers
        to use in plotting.
        """

    def makeTickLabels(self): ...
    def scale(self, value):
        """Converts a numeric value to a plotarea position.
        The chart first configures the axis, then asks it to
        """

class XValueAxis(_XTicks, ValueAxis):
    """X/value axis"""

    tickUp: int
    tickDown: int
    joinAxis: Incomplete
    joinAxisMode: Incomplete
    joinAxisPos: Incomplete
    def __init__(self, **kw) -> None: ...
    def demo(self): ...
    def joinToAxis(self, yAxis, mode: str = "bottom", pos=None) -> None:
        """Join with y-axis using some mode."""

    def makeAxis(self): ...

def parseDayAndMonth(dmstr):
    """This accepts and validates strings like "31-Dec" i.e. dates
    of no particular year.  29 Feb is allowed.  These can be used
    for recurring dates.  It returns a (dd, mm) pair where mm is the
    month integer.  If the text is not valid it raises an error.
    """

class _isListOfDaysAndMonths(Validator):
    """This accepts and validates lists of strings like "31-Dec" i.e. dates
    of no particular year.  29 Feb is allowed.  These can be used
    for recurring dates.
    """

    def test(self, x): ...
    def normalize(self, x): ...

isListOfDaysAndMonths: Incomplete

class NormalDateXValueAxis(XValueAxis):
    """An X axis applying additional rules.

    Depending on the data and some built-in rules, the axis
    displays normalDate values as nicely formatted dates.

    The client chart should have NormalDate X values.
    """

    bottomAxisLabelSlack: float
    niceMonth: int
    forceEndDate: int
    forceFirstDate: int
    forceDatesEachYear: Incomplete
    dailyFreq: int
    xLabelFormat: str
    dayOfWeekName: Incomplete
    monthName: Incomplete
    specialTickClear: int
    valueSteps: Incomplete
    def __init__(self, **kw) -> None: ...
    def configure(self, data) -> None: ...

class YValueAxis(_YTicks, ValueAxis):
    """Y/value axis"""

    tickRight: int
    tickLeft: int
    joinAxis: Incomplete
    joinAxisMode: Incomplete
    joinAxisPos: Incomplete
    def __init__(self) -> None: ...
    def demo(self): ...
    def joinToAxis(self, xAxis, mode: str = "left", pos=None) -> None:
        """Join with x-axis using some mode."""

    def makeAxis(self): ...

class TimeValueAxis:
    labelTextFormat: Incomplete
    def __init__(self, *args, **kwds) -> None: ...
    def timeLabelTextFormatter(self, val): ...

class XTimeValueAxis(TimeValueAxis, XValueAxis):
    def __init__(self, *args, **kwds) -> None: ...

class AdjYValueAxis(YValueAxis):
    """A Y-axis applying additional rules.

    Depending on the data and some built-in rules, the axis
    may choose to adjust its range and origin.
    """

    requiredRange: int
    leftAxisPercent: int
    leftAxisOrigShiftIPC: float
    leftAxisOrigShiftMin: int
    leftAxisSkipLL0: int
    valueSteps: Incomplete
    def __init__(self, **kw) -> None: ...

class LogValueAxis(ValueAxis): ...

class LogAxisTickLabeller(TickLabeller):
    def __call__(self, axis, value): ...

class LogAxisTickLabellerS(TickLabeller):
    """simple log axis labeller tries to use integers
    and short forms else exponential format
    """

    def __call__(self, axis, value): ...

class LogAxisLabellingSetup:
    labels: Incomplete
    labelTextFormat: Incomplete
    def __init__(self) -> None: ...

class LogXValueAxis(LogValueAxis, LogAxisLabellingSetup, XValueAxis):
    def __init__(self) -> None: ...
    def scale(self, value):
        """Converts a numeric value to a Y position.

        The chart first configures the axis, then asks it to
        work out the x value for each point when plotting
        lines or bars.  You could override this to do
        logarithmic axes.
        """

class LogYValueAxis(LogValueAxis, LogAxisLabellingSetup, YValueAxis):
    def __init__(self) -> None: ...
    def scale(self, value):
        """Converts a numeric value to a Y position.

        The chart first configures the axis, then asks it to
        work out the x value for each point when plotting
        lines or bars.  You could override this to do
        logarithmic axes.
        """
