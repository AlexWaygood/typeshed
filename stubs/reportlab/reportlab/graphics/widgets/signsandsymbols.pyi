"""This file is a collection of widgets to produce some common signs and symbols.

Widgets include:

- ETriangle (an equilateral triangle),
- RTriangle (a right angled triangle),
- Octagon,
- Crossbox,
- Tickbox,
- SmileyFace,
- StopSign,
- NoEntry,
- NotAllowed (the red roundel from 'no smoking' signs),
- NoSmoking,
- DangerSign (a black exclamation point in a yellow triangle),
- YesNo (returns a tickbox or a crossbox depending on a testvalue),
- FloppyDisk,
- ArrowOne, and
- ArrowTwo
- CrossHair
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]

class _Symbol(Widget):
    """Abstract base widget
    possible attributes:
    'x', 'y', 'size', 'fillColor', 'strokeColor'
    """

    x: int
    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    strokeWidth: float
    def __init__(self) -> None: ...
    def demo(self): ...

class ETriangle(_Symbol):
    """This draws an equilateral triangle."""

    def __init__(self) -> None: ...
    def draw(self): ...

class RTriangle(_Symbol):
    """This draws a right-angled triangle.

    possible attributes:
    'x', 'y', 'size', 'fillColor', 'strokeColor'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class Octagon(_Symbol):
    """This widget draws an Octagon.

    possible attributes:
    'x', 'y', 'size', 'fillColor', 'strokeColor'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class Crossbox(_Symbol):
    """This draws a black box with a red cross in it - a 'checkbox'.

    possible attributes:
    'x', 'y', 'size', 'crossColor', 'strokeColor', 'crosswidth'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    crossColor: Incomplete
    strokeColor: Incomplete
    crosswidth: int
    def __init__(self) -> None: ...
    def draw(self): ...

class Tickbox(_Symbol):
    """This draws a black box with a red tick in it - another 'checkbox'.

    possible attributes:
    'x', 'y', 'size', 'tickColor', 'strokeColor', 'tickwidth'

    """

    x: int
    y: int
    size: int
    tickColor: Incomplete
    strokeColor: Incomplete
    fillColor: Incomplete
    tickwidth: int
    def __init__(self) -> None: ...
    def draw(self): ...

class SmileyFace(_Symbol):
    """This draws a classic smiley face.

    possible attributes:
    'x', 'y', 'size', 'fillColor'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class StopSign(_Symbol):
    """This draws a (British) stop sign.

    possible attributes:
    'x', 'y', 'size'

    """

    x: int
    y: int
    size: int
    strokeColor: Incomplete
    fillColor: Incomplete
    stopColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class NoEntry(_Symbol):
    """This draws a (British) No Entry sign - a red circle with a white line on it.

    possible attributes:
    'x', 'y', 'size'

    """

    x: int
    y: int
    size: int
    strokeColor: Incomplete
    fillColor: Incomplete
    innerBarColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class NotAllowed(_Symbol):
    """This draws a 'forbidden' roundel (as used in the no-smoking sign).

    possible attributes:
    'x', 'y', 'size'

    """

    x: int
    y: int
    size: int
    strokeColor: Incomplete
    fillColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class NoSmoking(NotAllowed):
    """This draws a no-smoking sign.

    possible attributes:
    'x', 'y', 'size'

    """

    def __init__(self) -> None: ...
    def draw(self): ...

class DangerSign(_Symbol):
    """This draws a 'danger' sign: a yellow box with a black exclamation point.

    possible attributes:
    'x', 'y', 'size', 'strokeColor', 'fillColor', 'strokeWidth'

    """

    x: int
    y: int
    size: int
    strokeColor: Incomplete
    fillColor: Incomplete
    strokeWidth: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class YesNo(_Symbol):
    """This widget draw a tickbox or crossbox depending on 'testValue'.

    If this widget is supplied with a 'True' or 1 as a value for
    testValue, it will use the tickbox widget. Otherwise, it will
    produce a crossbox.

    possible attributes:
    'x', 'y', 'size', 'tickcolor', 'crosscolor', 'testValue'

    """

    x: int
    y: int
    size: int
    tickcolor: Incomplete
    crosscolor: Incomplete
    testValue: int
    def __init__(self) -> None: ...
    def draw(self): ...
    def demo(self): ...

class FloppyDisk(_Symbol):
    """This widget draws an icon of a floppy disk.

    possible attributes:
    'x', 'y', 'size', 'diskcolor'

    """

    x: int
    y: int
    size: int
    diskColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class ArrowOne(_Symbol):
    """This widget draws an arrow (style one).

    possible attributes:
    'x', 'y', 'size', 'fillColor'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    strokeWidth: int
    strokeColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class ArrowTwo(ArrowOne):
    """This widget draws an arrow (style two).

    possible attributes:
    'x', 'y', 'size', 'fillColor'

    """

    x: int
    y: int
    size: int
    fillColor: Incomplete
    strokeWidth: int
    strokeColor: Incomplete
    def __init__(self) -> None: ...
    def draw(self): ...

class CrossHair(_Symbol):
    """This draws an equilateral triangle."""

    x: int
    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    strokeWidth: float
    innerGap: str
    def __init__(self) -> None: ...
    def draw(self): ...

def test() -> None:
    """This function produces a pdf with examples of all the signs and symbols from this file."""
