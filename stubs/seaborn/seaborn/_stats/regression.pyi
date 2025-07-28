from dataclasses import dataclass

from seaborn._stats.base import Stat

@dataclass
class PolyFit(Stat):
    """
    Fit a polynomial of the given order and resample data onto predicted curve.
    """

    order: int = 2
    gridsize: int = 100

@dataclass
class OLSFit(Stat):
    """OLSFit()"""
