"""Utilities used here and there."""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

def mkTimeTuple(timeString):
    """Convert a 'dd/mm/yyyy' formatted string to a tuple for use in the time module."""

def str2seconds(timeString):
    """Convert a number of seconds since the epoch into a date string."""

def seconds2str(seconds):
    """Convert a date string into the number of seconds since the epoch."""

def nextRoundNumber(x):
    """Return the first 'nice round number' greater than or equal to x

    Used in selecting apropriate tick mark intervals; we say we want
    an interval which places ticks at least 10 points apart, work out
    what that is in chart space, and ask for the nextRoundNumber().
    Tries the series 1,2,5,10,20,50,100.., going up or down as needed.
    """

def find_interval(lo, hi, I: int = 5):
    """determine tick parameters for range [lo, hi] using I intervals"""

def find_good_grid(lower, upper, n=(4, 5, 6, 7, 8, 9), grid=None): ...
def ticks(lower, upper, n=(4, 5, 6, 7, 8, 9), split: int = 1, percent: int = 0, grid=None, labelVOffset: int = 0):
    """
    return tick positions and labels for range lower<=x<=upper
    n=number of intervals to try (can be a list or sequence)
    split=1 return ticks then labels else (tick,label) pairs
    """

def findNones(data): ...
def pairFixNones(pairs): ...
def maverage(data, n: int = 6): ...
def pairMaverage(data, n: int = 6): ...

class DrawTimeCollector:
    """
    generic mechanism for collecting information about nodes at the time they are about to be drawn
    """

    formats: Incomplete
    disabled: bool
    def __init__(self, formats=["gif"]) -> None: ...
    def clear(self) -> None: ...
    def record(self, func, node, *args, **kwds) -> None: ...
    def __call__(self, node, canvas, renderer) -> None: ...
    @staticmethod
    def rectDrawTimeCallback(node, canvas, renderer, **kwds): ...
    @staticmethod
    def transformAndFlatten(A, p):
        """transform an flatten a list of points
        A   transformation matrix
        p   points [(x0,y0),....(xk,yk).....]
        """

    @property
    def pmcanv(self): ...
    def wedgeDrawTimeCallback(self, node, canvas, renderer, **kwds): ...
    def save(self, fnroot) -> None:
        """
        save the current information known to this collector
        fnroot is the root name of a resource to name the saved info
        override this to get the right semantics for your collector
        """

def xyDist(xxx_todo_changeme, xxx_todo_changeme1):
    """return distance between two points"""

def lineSegmentIntersect(xxx_todo_changeme2, xxx_todo_changeme3, xxx_todo_changeme4, xxx_todo_changeme5): ...
def makeCircularString(x, y, radius, angle, text, fontName, fontSize, inside: int = 0, G=None, textAnchor: str = "start"):
    """make a group with circular text in it"""

class CustomDrawChanger:
    """
    a class to simplify making changes at draw time
    """

    store: Incomplete
    def __init__(self) -> None: ...
    def __call__(self, change, obj) -> None: ...

class FillPairedData(list[Incomplete]):
    other: Incomplete
    def __init__(self, v, other: int = 0) -> None: ...
