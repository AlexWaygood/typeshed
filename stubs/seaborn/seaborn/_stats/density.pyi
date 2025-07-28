from dataclasses import dataclass

from seaborn._stats.base import Stat
from seaborn.external.kde import _BwMethodType

@dataclass
class KDE(Stat):
    """
    Compute a univariate kernel density estimate.

    Parameters
    ----------
    bw_adjust : float
        Factor that multiplicatively scales the value chosen using
        `bw_method`. Increasing will make the curve smoother. See Notes.
    bw_method : string, scalar, or callable
        Method for determining the smoothing bandwidth to use. Passed directly
        to :class:`scipy.stats.gaussian_kde`; see there for options.
    common_norm : bool or list of variables
        If `True`, normalize so that the areas of all curves sums to 1.
        If `False`, normalize each curve independently. If a list, defines
        variable(s) to group by and normalize within.
    common_grid : bool or list of variables
        If `True`, all curves will share the same evaluation grid.
        If `False`, each evaluation grid is independent. If a list, defines
        variable(s) to group by and share a grid within.
    gridsize : int or None
        Number of points in the evaluation grid. If None, the density is
        evaluated at the original datapoints.
    cut : float
        Factor, multiplied by the kernel bandwidth, that determines how far
        the evaluation grid extends past the extreme datapoints. When set to 0,
        the curve is truncated at the data limits.
    cumulative : bool
        If True, estimate a cumulative distribution function. Requires scipy.

    Notes
    -----
    The *bandwidth*, or standard deviation of the smoothing kernel, is an
    important parameter. Much like histogram bin width, using the wrong
    bandwidth can produce a distorted representation. Over-smoothing can erase
    true features, while under-smoothing can create false ones. The default
    uses a rule-of-thumb that works best for distributions that are roughly
    bell-shaped. It is a good idea to check the default by varying `bw_adjust`.

    Because the smoothing is performed with a Gaussian kernel, the estimated
    density curve can extend to values that may not make sense. For example, the
    curve may be drawn over negative values when data that are naturally
    positive. The `cut` parameter can be used to control the evaluation range,
    but datasets that have many observations close to a natural boundary may be
    better served by a different method.

    Similar distortions may arise when a dataset is naturally discrete or "spiky"
    (containing many repeated observations of the same value). KDEs will always
    produce a smooth curve, which could be misleading.

    The units on the density axis are a common source of confusion. While kernel
    density estimation produces a probability distribution, the height of the curve
    at each point gives a density, not a probability. A probability can be obtained
    only by integrating the density across a range. The curve is normalized so
    that the integral over all possible values is 1, meaning that the scale of
    the density axis depends on the data values.

    If scipy is installed, its cython-accelerated implementation will be used.

    Examples
    --------
    .. include:: ../docstrings/objects.KDE.rst

    """

    bw_adjust: float = 1
    bw_method: _BwMethodType = "scott"
    common_norm: bool | list[str] = True
    common_grid: bool | list[str] = True
    gridsize: int | None = 200
    cut: float = 3
    cumulative: bool = False
    def __post_init__(self) -> None: ...
