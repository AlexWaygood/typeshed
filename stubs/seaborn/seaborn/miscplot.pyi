from _typeshed import Unused
from collections.abc import Sequence

from matplotlib.typing import ColorType

__all__ = ["palplot", "dogplot"]

def palplot(pal: Sequence[ColorType], size: int = 1) -> None:
    """Plot the values in a color palette as a horizontal array.

    Parameters
    ----------
    pal : sequence of matplotlib colors
        colors, i.e. as returned by seaborn.color_palette()
    size :
        scaling factor for size of plot

    """

def dogplot(*_: Unused, **__: Unused) -> None:
    """Who's a good boy?"""
