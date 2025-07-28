"""Superclass for renderers to factor out common functionality and default implementations."""

from typing import Final

__version__: Final[str]

def getStateDelta(shape):
    """Used to compute when we need to change the graphics state.
    For example, if we have two adjacent red shapes we don't need
    to set the pen color to red in between. Returns the effect
    the given shape would have on the graphics state
    """

class StateTracker:
    """Keeps a stack of transforms and state
    properties.  It can contain any properties you
    want, but the keys 'transform' and 'ctm' have
    special meanings.  The getCTM()
    method returns the current transformation
    matrix at any point, without needing to
    invert matrixes when you pop.
    """

    def __init__(self, defaults=None, defaultObj=None) -> None: ...
    def push(self, delta) -> None:
        """Take a new state dictionary of changes and push it onto
        the stack.  After doing this, the combined state is accessible
        through getState()
        """

    def pop(self):
        """steps back one, and returns a state dictionary with the
        deltas to reverse out of wherever you are.  Depending
        on your back end, you may not need the return value,
        since you can get the complete state afterwards with getState()
        """

    def getState(self):
        """returns the complete graphics state at this point"""

    def getCTM(self):
        """returns the current transformation matrix at this point"""

    def __getitem__(self, key):
        """returns the complete graphics state value of key at this point"""

    def __setitem__(self, key, value) -> None:
        """sets the complete graphics state value of key to value"""

def testStateTracker() -> None: ...
def renderScaledDrawing(d): ...

class Renderer:
    """Virtual superclass for graphics renderers."""

    def undefined(self, operation) -> None: ...
    def draw(self, drawing, canvas, x: int = 0, y: int = 0, showBoundary=...) -> None:
        """This is the top level function, which draws the drawing at the given
        location. The recursive part is handled by drawNode.
        """

    def initState(self, x, y) -> None: ...
    def pop(self) -> None: ...
    def drawNode(self, node) -> None:
        """This is the recursive method called for each node
        in the tree
        """

    def getStateValue(self, key):
        """Return current state parameter for given key"""

    def fillDerivedValues(self, node) -> None:
        """Examine a node for any values which are Derived,
        and replace them with their calculated values.
        Generally things may look at the drawing or their
        parent.

        """

    def drawNodeDispatcher(self, anode) -> None:
        """dispatch on the node's (super) class: shared code"""

    def drawGroup(self, group) -> None: ...
    def drawWedge(self, wedge) -> None: ...
    def drawPath(self, path) -> None: ...
    def drawRect(self, rect) -> None: ...
    def drawLine(self, line) -> None: ...
    def drawCircle(self, circle) -> None: ...
    def drawPolyLine(self, p) -> None: ...
    def drawEllipse(self, ellipse) -> None: ...
    def drawPolygon(self, p) -> None: ...
    def drawString(self, stringObj) -> None: ...
    def applyStateChanges(self, delta, newState) -> None:
        """This takes a set of states, and outputs the operators
        needed to set those properties
        """

    def drawImage(self, *args, **kwds) -> None: ...
