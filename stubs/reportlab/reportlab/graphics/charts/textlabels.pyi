from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.utils import CustomDrawChanger
from reportlab.graphics.widgetbase import PropHolder, Widget
from reportlab.lib.attrmap import *

__version__: Final[str]

class Label(Widget):
    """A text label to attach to something else, such as a chart axis.

    This allows you to specify an offset, angle and many anchor
    properties relative to the label's origin.  It allows, for example,
    angled multiline axis labels.
    """

    def __init__(self, **kw) -> None: ...
    def setText(self, text) -> None:
        """Set the text property.  May contain embedded newline characters.
        Called by the containing chart or axis.
        """
    x: Incomplete
    y: Incomplete
    def setOrigin(self, x, y) -> None:
        """Set the origin.  This would be the tick mark or bar top relative to
        which it is defined.  Called by the containing chart or axis.
        """

    def demo(self):
        """This shows a label positioned with its top right corner
        at the top centre of the drawing, and rotated 45 degrees.
        """

    def computeSize(self) -> None: ...
    def draw(self): ...

class LabelDecorator:
    textAnchor: str
    boxAnchor: str
    def __init__(self) -> None: ...
    def decorate(self, l, L) -> None: ...
    def __call__(self, l) -> None: ...

isOffsetMode: Incomplete

class LabelOffset(PropHolder):
    posMode: str
    pos: int
    def __init__(self) -> None: ...

NoneOrInstanceOfLabelOffset: Incomplete

class PMVLabel(Label):
    def __init__(self, **kwds) -> None: ...

class BarChartLabel(PMVLabel):
    """
    An extended Label allowing for nudging, lines visibility etc
    """

    lineStrokeWidth: int
    lineStrokeColor: Incomplete
    fixedStart: Incomplete
    nudge: int
    def __init__(self, **kwds) -> None: ...

class NA_Label(BarChartLabel):
    """
    An extended Label allowing for nudging, lines visibility etc
    """

    text: str
    def __init__(self) -> None: ...

NoneOrInstanceOfNA_Label: Incomplete

class RedNegativeChanger(CustomDrawChanger):
    fillColor: Incomplete
    def __init__(self, fillColor=...) -> None: ...

class XLabel(Label):
    """like label but uses XPreFormatted/Paragraph to draw the _text"""

    ddfKlass: Incomplete
    ddf: Incomplete
    def __init__(self, *args, **kwds) -> None: ...
    def computeSize(self) -> None: ...
