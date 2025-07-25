"""Defines inch, cm, mm etc as multiples of a point

You can now in user-friendly units by doing::

    from reportlab.lib.units import inch
    r = Rect(0, 0, 3 * inch, 6 * inch)

"""

from typing import Final

__version__: Final[str]
inch: Final[float]
cm: Final[float]
mm: Final[float]
pica: Final[float]

def toLength(s: str) -> float:
    """convert a string to  a length"""
