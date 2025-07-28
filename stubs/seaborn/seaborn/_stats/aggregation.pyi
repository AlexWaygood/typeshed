from collections.abc import Callable
from dataclasses import dataclass

from seaborn._core.typing import Vector
from seaborn._stats.base import Stat

@dataclass
class Agg(Stat):
    """
    Aggregate data along the value axis using given method.

    Parameters
    ----------
    func : str or callable
        Name of a :class:`pandas.Series` method or a vector -> scalar function.

    See Also
    --------
    objects.Est : Aggregation with error bars.

    Examples
    --------
    .. include:: ../docstrings/objects.Agg.rst

    """

    func: str | Callable[[Vector], float] = "mean"

@dataclass
class Est(Stat):
    """
    Calculate a point estimate and error bar interval.

    For more information about the various `errorbar` choices, see the
    :doc:`errorbar tutorial </tutorial/error_bars>`.

    Additional variables:

    - **weight**: When passed to a layer that uses this stat, a weighted estimate
      will be computed. Note that use of weights currently limits the choice of
      function and error bar method  to `"mean"` and `"ci"`, respectively.

    Parameters
    ----------
    func : str or callable
        Name of a :class:`numpy.ndarray` method or a vector -> scalar function.
    errorbar : str, (str, float) tuple, or callable
        Name of errorbar method (one of "ci", "pi", "se" or "sd"), or a tuple
        with a method name ane a level parameter, or a function that maps from a
        vector to a (min, max) interval.
    n_boot : int
       Number of bootstrap samples to draw for "ci" errorbars.
    seed : int
        Seed for the PRNG used to draw bootstrap samples.

    Examples
    --------
    .. include:: ../docstrings/objects.Est.rst

    """

    func: str | Callable[[Vector], float] = "mean"
    errorbar: str | tuple[str, float] = ("ci", 95)
    n_boot: int = 1000
    seed: int | None = None

@dataclass
class Rolling(Stat):
    """Rolling()"""
