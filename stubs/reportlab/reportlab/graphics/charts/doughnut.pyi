"""Doughnut chart

Produces a circular chart like the doughnut charts produced by Excel.
Can handle multiple series (which produce concentric 'rings' in the chart).

"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.piecharts import AbstractPieChart, WedgeProperties
from reportlab.lib.attrmap import *

__version__: Final[str]

class SectorProperties(WedgeProperties):
    """This holds descriptive information about the sectors in a doughnut chart.

    It is not to be confused with the 'sector itself'; this just holds
    a recipe for how to format one, and does not allow you to hack the
    angles.  It can format a genuine Sector object for you with its
    format method.
    """

class Doughnut(AbstractPieChart):
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
    sideLabels: int
    innerRadiusFraction: Incomplete
    slices: Incomplete
    angleRange: int
    def __init__(self, *, angleRange: int = 360, **kwds) -> None: ...
    def demo(self): ...
    def normalizeData(self, data=None): ...
    def makeSectors(self): ...
    def draw(self): ...

def sample1():
    """Make up something from the individual Sectors"""

def sample2():
    """Make a simple demo"""

def sample3():
    """Make a more complex demo"""

def sample4():
    """Make a more complex demo with Label Overlap fixing"""
