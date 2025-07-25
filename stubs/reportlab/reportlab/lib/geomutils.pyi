"""Utility functions for geometrical operations."""

from typing import Final

__version__: Final[str]

def normalizeTRBL(p):
    """
    Useful for interpreting short descriptions of paddings, borders, margin, etc.
    Expects a single value or a tuple of length 2 to 4.
    Returns a tuple representing (clockwise) the value(s) applied to the 4 sides of a rectangle:
    If a single value is given, that value is applied to all four sides.
    If two or three values are given, the missing values are taken from the opposite side(s).
    If four values are given they are returned unchanged.

    >>> normalizeTRBL(1)
    (1, 1, 1, 1)
    >>> normalizeTRBL((1, 1.2))
    (1, 1.2, 1, 1.2)
    >>> normalizeTRBL((1, 1.2, 0))
    (1, 1.2, 0, 1.2)
    >>> normalizeTRBL((1, 1.2, 0, 8))
    (1, 1.2, 0, 8)
    """
