"""This module defines a Area mixin classes"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget

__version__: Final[str]

class PlotArea(Widget):
    """Abstract base class representing a chart's plot area, pretty unusable by itself."""

    x: int
    y: int
    height: int
    width: int
    strokeColor: Incomplete
    strokeWidth: int
    fillColor: Incomplete
    background: Incomplete
    debug: int
    def __init__(self) -> None: ...
    def makeBackground(self): ...
