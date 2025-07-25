"""A frame is a container for content on a page."""

from typing import Literal

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.flowables import Flowable

class Frame:
    """
    A Frame is a piece of space in a document that is filled by the
    "flowables" in the story.  For example in a book like document most
    pages have the text paragraphs in one or two frames.  For generality
    a page might have several frames (for example for 3 column text or
    for text that wraps around a graphic).

    After creation a Frame is not usually manipulated directly by the
    applications program -- it is used internally by the platypus modules.

    Here is a diagramatid abstraction for the definitional part of a Frame::

                width                    x2,y2
        +---------------------------------+
        | l  top padding                r | h
        | e +-------------------------+ i | e
        | f |                         | g | i
        | t |                         | h | g
        |   |                         | t | h
        | p |                         |   | t
        | a |                         | p |
        | d |                         | a |
        |   |                         | d |
        |   +-------------------------+   |
        |    bottom padding               |
        +---------------------------------+
        (x1,y1) <-- lower left corner

    NOTE!! Frames are stateful objects.  No single frame should be used in
    two documents at the same time (especially in the presence of multithreading.
    """

    id: str | None
    x1: float
    y1: float
    width: float
    height: float
    leftPadding: float
    bottomPadding: float
    rightPadding: float
    topPadding: float
    showBoundary: int
    def __init__(
        self,
        x1: float,
        y1: float,
        width: float,
        height: float,
        leftPadding: float = 6,
        bottomPadding: float = 6,
        rightPadding: float = 6,
        topPadding: float = 6,
        id: str | None = None,
        showBoundary: int = 0,
        overlapAttachedSpace=None,
        _debug=None,
    ) -> None: ...
    def add(self, flowable: Flowable, canv: Canvas, trySplit: int = 0) -> Literal[0, 1]:
        """Draws the flowable at the current position.
        Returns 1 if successful, 0 if it would not fit.
        Raises a LayoutError if the object is too wide,
        or if it is too high for a totally empty frame,
        to avoid infinite loops
        """

    def split(self, flowable: Flowable, canv: Canvas) -> list[Flowable]:
        """Ask the flowable to split using up the available space."""

    def drawBoundary(self, canv: Canvas) -> None: ...
    def addFromList(self, drawlist: list[Flowable], canv: Canvas) -> None:
        """Consumes objects from the front of the list until the
        frame is full.  If it cannot fit one object, raises
        an exception.
        """

    def add_generated_content(self, *C: Flowable) -> None: ...

__all__ = ("Frame",)
