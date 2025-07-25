"""This file is a"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget

__version__: Final[str]

class EventCalendar(Widget):
    x: int
    y: int
    width: int
    height: int
    timeColWidth: Incomplete
    trackRowHeight: int
    data: Incomplete
    trackNames: Incomplete
    startTime: Incomplete
    endTime: Incomplete
    day: int
    def __init__(self) -> None: ...
    def computeSize(self) -> None:
        """Called at start of draw.  Sets various column widths"""

    def computeStartAndEndTimes(self) -> None:
        """Work out first and last times to display"""

    def getAllTracks(self): ...
    def getRelevantTalks(self, talkList):
        """Scans for tracks actually used"""

    def scaleTime(self, theTime):
        """Return y-value corresponding to times given"""

    def getTalkRect(self, startTime, duration, trackId, text):
        """Return shapes for a specific talk"""

    def draw(self): ...

def test() -> None:
    """Make a conference event for day 1 of UP Python 2003"""
