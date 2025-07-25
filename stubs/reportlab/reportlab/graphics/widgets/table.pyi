from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]

class TableWidget(Widget):
    """A two dimensions table of labels"""

    x: Incomplete
    y: Incomplete
    width: int
    height: int
    borderStrokeColor: Incomplete
    fillColor: Incomplete
    borderStrokeWidth: float
    horizontalDividerStrokeColor: Incomplete
    verticalDividerStrokeColor: Incomplete
    horizontalDividerStrokeWidth: float
    verticalDividerStrokeWidth: float
    dividerDashArray: Incomplete
    data: Incomplete
    boxAnchor: str
    fontSize: int
    fontColor: Incomplete
    alignment: str
    textAnchor: str
    def __init__(self, x: int = 10, y: int = 10, **kw) -> None: ...
    def demo(self):
        """returns a sample of this widget with data"""

    def draw(self):
        """returns a group of shapes"""

    def preProcessData(self, data):
        """preprocess and return a new array with at least one row
        and column (use a None) if needed, and all rows the same
        length (adding Nones if needed)

        """
