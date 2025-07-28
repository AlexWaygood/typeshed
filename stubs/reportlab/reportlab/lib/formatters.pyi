"""
These help format numbers and dates in a user friendly way.
Used by the graphics framework.
"""

from _typeshed import Incomplete

class Formatter:
    """Base formatter - simply applies python format strings"""

    pattern: Incomplete
    def __init__(self, pattern) -> None: ...
    def format(self, obj): ...
    def __call__(self, x): ...

class DecimalFormatter(Formatter):
    """lets you specify how to build a decimal.

    A future NumberFormatter class will take Microsoft-style patterns
    instead - "$#,##0.00" is WAY easier than this.
    """

    calcPlaces: Incomplete
    places: Incomplete
    dot: Incomplete
    comma: Incomplete
    prefix: Incomplete
    suffix: Incomplete
    def __init__(self, places: int = 2, decimalSep: str = ".", thousandSep=None, prefix=None, suffix=None) -> None: ...
    def format(self, num): ...

__all__ = ("Formatter", "DecimalFormatter")
