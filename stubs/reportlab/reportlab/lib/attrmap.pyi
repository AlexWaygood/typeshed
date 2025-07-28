'''Framework for objects whose assignments are checked. Used by graphics.

We developed reportlab/graphics prior to Python 2 and metaclasses. For the
graphics, we wanted to be able to declare the attributes of a class, check
them on assignment, and convert from string arguments.  Examples of
attrmap-based objects can be found in reportlab/graphics/shapes.  It lets
us defined structures like the one below, which are seen more modern form in
Django models and other frameworks.

We'll probably replace this one day soon, hopefully with no impact on client
code.

class Rect(SolidShape):
    """Rectangle, possibly with rounded corners."""

    _attrMap = AttrMap(BASE=SolidShape,
        x = AttrMapValue(isNumber),
        y = AttrMapValue(isNumber),
        width = AttrMapValue(isNumber),
        height = AttrMapValue(isNumber),
        rx = AttrMapValue(isNumber),
        ry = AttrMapValue(isNumber),
        )


'''

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

class CallableValue:
    """a class to allow callable initial values"""

    func: Incomplete
    args: Incomplete
    kw: Incomplete
    def __init__(self, func, *args, **kw) -> None: ...
    def __call__(self): ...

class AttrMapValue:
    """Simple multi-value holder for attribute maps"""

    validate: Incomplete
    desc: Incomplete
    def __init__(self, validate=None, desc=None, initial=None, advancedUsage: int = 0, **kw) -> None: ...
    def __getattr__(self, name): ...

class AttrMap(dict[str, AttrMapValue]):
    def __init__(self, BASE=None, UNWANTED=[], **kw) -> None: ...
    def remove(self, unwanted) -> None: ...
    def clone(self, UNWANTED=[], **kw): ...

def validateSetattr(obj, name, value) -> None:
    """validate setattr(obj,name,value)"""

def hook__setattr__(obj): ...
def addProxyAttribute(src, name, validate=None, desc=None, initial=None, dst=None) -> None:
    """
    Add a proxy attribute 'name' to src with targets dst
    """
