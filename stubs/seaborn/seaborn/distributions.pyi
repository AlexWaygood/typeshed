"""Plotting functions for visualizing distributions."""

from collections.abc import Iterable
from typing import Any, Literal, Protocol, TypeVar
from typing_extensions import TypeAlias, deprecated

from matplotlib.axes import Axes
from matplotlib.colors import Colormap
from matplotlib.typing import ColorType
from numpy.typing import ArrayLike

from ._core.typing import ColumnName, DataSource, NormSpec
from .axisgrid import FacetGrid
from .external.kde import _BwMethodType
from .utils import _DataSourceWideForm, _LogScale, _Palette, _Vector

__all__ = ["displot", "histplot", "kdeplot", "ecdfplot", "rugplot", "distplot"]

_T = TypeVar("_T")
_OneOrPair: TypeAlias = _T | tuple[_T, _T]

class _Fit(Protocol):
    def fit(self, a: ArrayLike) -> tuple[ArrayLike, ...]: ...
    def pdf(self, x: ArrayLike, *params: ArrayLike) -> ArrayLike: ...

def histplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    stat: str = "count",
    bins: _OneOrPair[str | int | ArrayLike] = "auto",
    binwidth: float | tuple[float, float] | None = None,
    binrange: _OneOrPair[tuple[float, float]] | None = None,
    discrete: bool | None = None,
    cumulative: bool = False,
    common_bins: bool = True,
    common_norm: bool = True,
    multiple: Literal["layer", "dodge", "stack", "fill"] = "layer",
    element: Literal["bars", "step", "poly"] = "bars",
    fill: bool = True,
    shrink: float = 1,
    kde: bool = False,
    kde_kws: dict[str, Any] | None = None,
    line_kws: dict[str, Any] | None = None,
    thresh: float | None = 0,
    pthresh: float | None = None,
    pmax: float | None = None,
    cbar: bool = False,
    cbar_ax: Axes | None = None,
    cbar_kws: dict[str, Any] | None = None,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    color: ColorType | None = None,
    log_scale: _LogScale | None = None,
    legend: bool = True,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot univariate or bivariate histograms to show distributions of datasets.

    A histogram is a classic visualization tool that represents the distribution
    of one or more variables by counting the number of observations that fall within
    discrete bins.

    This function can normalize the statistic computed within each bin to estimate
    frequency, density or probability mass, and it can add a smooth curve obtained
    using a kernel density estimate, similar to :func:`kdeplot`.

    More information is provided in the :ref:`user guide <tutorial_hist>`.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    weights : vector or key in ``data``
        If provided, weight the contribution of the corresponding data points
        towards the count in each bin by these factors.
    stat : str
        Aggregate statistic to compute in each bin.

        - `count`: show the number of observations in each bin
        - `frequency`: show the number of observations divided by the bin width
        - `probability` or `proportion`: normalize such that bar heights sum to 1
        - `percent`: normalize such that bar heights sum to 100
        - `density`: normalize such that the total area of the histogram equals 1
    bins : str, number, vector, or a pair of such values
        Generic bin parameter that can be the name of a reference rule,
        the number of bins, or the breaks of the bins.
        Passed to :func:`numpy.histogram_bin_edges`.
    binwidth : number or pair of numbers
        Width of each bin, overrides ``bins`` but can be used with
        ``binrange``.
    binrange : pair of numbers or a pair of pairs
        Lowest and highest value for bin edges; can be used either
        with ``bins`` or ``binwidth``. Defaults to data extremes.
    discrete : bool
        If True, default to ``binwidth=1`` and draw the bars so that they are
        centered on their corresponding data points. This avoids "gaps" that may
        otherwise appear when using discrete (integer) data.
    cumulative : bool
        If True, plot the cumulative counts as bins increase.
    common_bins : bool
        If True, use the same bins when semantic variables produce multiple
        plots. If using a reference rule to determine the bins, it will be computed
        with the full dataset.
    common_norm : bool
        If True and using a normalized statistic, the normalization will apply over
        the full dataset. Otherwise, normalize each histogram independently.
    multiple : {"layer", "dodge", "stack", "fill"}
        Approach to resolving multiple elements when semantic mapping creates subsets.
        Only relevant with univariate data.
    element : {"bars", "step", "poly"}
        Visual representation of the histogram statistic.
        Only relevant with univariate data.
    fill : bool
        If True, fill in the space under the histogram.
        Only relevant with univariate data.
    shrink : number
        Scale the width of each bar relative to the binwidth by this factor.
        Only relevant with univariate data.
    kde : bool
        If True, compute a kernel density estimate to smooth the distribution
        and show on the plot as (one or more) line(s).
        Only relevant with univariate data.
    kde_kws : dict
        Parameters that control the KDE computation, as in :func:`kdeplot`.
    line_kws : dict
        Parameters that control the KDE visualization, passed to
        :meth:`matplotlib.axes.Axes.plot`.
    thresh : number or None
        Cells with a statistic less than or equal to this value will be transparent.
        Only relevant with bivariate data.
    pthresh : number or None
        Like ``thresh``, but a value in [0, 1] such that cells with aggregate counts
        (or other statistics, when used) up to this proportion of the total will be
        transparent.
    pmax : number or None
        A value in [0, 1] that sets that saturation point for the colormap at a value
        such that cells below constitute this proportion of the total count (or
        other statistic, when used).
    cbar : bool
        If True, add a colorbar to annotate the color mapping in a bivariate plot.
        Note: Does not currently support plots with a ``hue`` variable well.
    cbar_ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the colorbar.
    cbar_kws : dict
        Additional parameters passed to :meth:`matplotlib.figure.Figure.colorbar`.
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    color : :mod:`matplotlib color <matplotlib.colors>`
        Single color specification for when hue mapping is not used. Otherwise, the
        plot will try to hook into the matplotlib property cycle.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.
    legend : bool
        If False, suppress the legend for semantic variables.
    ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the plot. Otherwise, call :func:`matplotlib.pyplot.gca`
        internally.
    kwargs
        Other keyword arguments are passed to one of the following matplotlib
        functions:

        - :meth:`matplotlib.axes.Axes.bar` (univariate, element="bars")
        - :meth:`matplotlib.axes.Axes.fill_between` (univariate, other element, fill=True)
        - :meth:`matplotlib.axes.Axes.plot` (univariate, other element, fill=False)
        - :meth:`matplotlib.axes.Axes.pcolormesh` (bivariate)

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The matplotlib axes containing the plot.

    See Also
    --------
    displot : Figure-level interface to distribution plot functions.
    kdeplot : Plot univariate or bivariate distributions using kernel density estimation.
    rugplot : Plot a tick at each observation value along the x and/or y axes.
    ecdfplot : Plot empirical cumulative distribution functions.
    jointplot : Draw a bivariate plot with univariate marginal distributions.

    Notes
    -----

    The choice of bins for computing and plotting a histogram can exert
    substantial influence on the insights that one is able to draw from the
    visualization. If the bins are too large, they may erase important features.
    On the other hand, bins that are too small may be dominated by random
    variability, obscuring the shape of the true underlying distribution. The
    default bin size is determined using a reference rule that depends on the
    sample size and variance. This works well in many cases, (i.e., with
    "well-behaved" data) but it fails in others. It is always a good to try
    different bin sizes to be sure that you are not missing something important.
    This function allows you to specify bins in several different ways, such as
    by setting the total number of bins to use, the width of each bin, or the
    specific locations where the bins should break.

    Examples
    --------

    .. include:: ../docstrings/histplot.rst

    """

def kdeplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    color: ColorType | None = None,
    fill: bool | None = None,
    multiple: Literal["layer", "stack", "fill"] = "layer",
    common_norm: bool = True,
    common_grid: bool = False,
    cumulative: bool = False,
    bw_method: _BwMethodType = "scott",
    bw_adjust: float = 1,
    warn_singular: bool = True,
    log_scale: _LogScale | None = None,
    levels: int | Iterable[float] = 10,
    thresh: float = 0.05,
    gridsize: int = 200,
    cut: float = 3,
    clip: _OneOrPair[tuple[float | None, float | None]] | None = None,
    legend: bool = True,
    cbar: bool = False,
    cbar_ax: Axes | None = None,
    cbar_kws: dict[str, Any] | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot univariate or bivariate distributions using kernel density estimation.

    A kernel density estimate (KDE) plot is a method for visualizing the
    distribution of observations in a dataset, analogous to a histogram. KDE
    represents the data using a continuous probability density curve in one or
    more dimensions.

    The approach is explained further in the :ref:`user guide <tutorial_kde>`.

    Relative to a histogram, KDE can produce a plot that is less cluttered and
    more interpretable, especially when drawing multiple distributions. But it
    has the potential to introduce distortions if the underlying distribution is
    bounded or not smooth. Like a histogram, the quality of the representation
    also depends on the selection of good smoothing parameters.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    weights : vector or key in ``data``
        If provided, weight the kernel density estimation using these values.
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    color : :mod:`matplotlib color <matplotlib.colors>`
        Single color specification for when hue mapping is not used. Otherwise, the
        plot will try to hook into the matplotlib property cycle.
    fill : bool or None
        If True, fill in the area under univariate density curves or between
        bivariate contours. If None, the default depends on ``multiple``.
    multiple : {{"layer", "stack", "fill"}}
        Method for drawing multiple elements when semantic mapping creates subsets.
        Only relevant with univariate data.
    common_norm : bool
        If True, scale each conditional density by the number of observations
        such that the total area under all densities sums to 1. Otherwise,
        normalize each density independently.
    common_grid : bool
        If True, use the same evaluation grid for each kernel density estimate.
        Only relevant with univariate data.
    cumulative : bool, optional
        If True, estimate a cumulative distribution function. Requires scipy.
    bw_method : string, scalar, or callable, optional
        Method for determining the smoothing bandwidth to use; passed to
        :class:`scipy.stats.gaussian_kde`.
    bw_adjust : number, optional
        Factor that multiplicatively scales the value chosen using
        ``bw_method``. Increasing will make the curve smoother. See Notes.
    warn_singular : bool
        If True, issue a warning when trying to estimate the density of data
        with zero variance.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.
    levels : int or vector
        Number of contour levels or values to draw contours at. A vector argument
        must have increasing values in [0, 1]. Levels correspond to iso-proportions
        of the density: e.g., 20% of the probability mass will lie below the
        contour drawn for 0.2. Only relevant with bivariate data.
    thresh : number in [0, 1]
        Lowest iso-proportion level at which to draw a contour line. Ignored when
        ``levels`` is a vector. Only relevant with bivariate data.
    gridsize : int
        Number of points on each dimension of the evaluation grid.
    cut : number, optional
        Factor, multiplied by the smoothing bandwidth, that determines how
        far the evaluation grid extends past the extreme datapoints. When
        set to 0, truncate the curve at the data limits.
    clip : pair of numbers or None, or a pair of such pairs
        Do not evaluate the density outside of these limits.
    legend : bool
        If False, suppress the legend for semantic variables.
    cbar : bool
        If True, add a colorbar to annotate the color mapping in a bivariate plot.
        Note: Does not currently support plots with a ``hue`` variable well.
    cbar_ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the colorbar.
    cbar_kws : dict
        Additional parameters passed to :meth:`matplotlib.figure.Figure.colorbar`.
    ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the plot. Otherwise, call :func:`matplotlib.pyplot.gca`
        internally.
    kwargs
        Other keyword arguments are passed to one of the following matplotlib
        functions:

        - :meth:`matplotlib.axes.Axes.plot` (univariate, ``fill=False``),
        - :meth:`matplotlib.axes.Axes.fill_between` (univariate, ``fill=True``),
        - :meth:`matplotlib.axes.Axes.contour` (bivariate, ``fill=False``),
        - :meth:`matplotlib.axes.contourf` (bivariate, ``fill=True``).

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The matplotlib axes containing the plot.

    See Also
    --------
    displot : Figure-level interface to distribution plot functions.
    histplot : Plot a histogram of binned counts with optional normalization or smoothing.
    ecdfplot : Plot empirical cumulative distribution functions.
    jointplot : Draw a bivariate plot with univariate marginal distributions.
    violinplot : Draw an enhanced boxplot using kernel density estimation.

    Notes
    -----

    The *bandwidth*, or standard deviation of the smoothing kernel, is an
    important parameter. Misspecification of the bandwidth can produce a
    distorted representation of the data. Much like the choice of bin width in a
    histogram, an over-smoothed curve can erase true features of a
    distribution, while an under-smoothed curve can create false features out of
    random variability. The rule-of-thumb that sets the default bandwidth works
    best when the true distribution is smooth, unimodal, and roughly bell-shaped.
    It is always a good idea to check the default behavior by using ``bw_adjust``
    to increase or decrease the amount of smoothing.

    Because the smoothing algorithm uses a Gaussian kernel, the estimated density
    curve can extend to values that do not make sense for a particular dataset.
    For example, the curve may be drawn over negative values when smoothing data
    that are naturally positive. The ``cut`` and ``clip`` parameters can be used
    to control the extent of the curve, but datasets that have many observations
    close to a natural boundary may be better served by a different visualization
    method.

    Similar considerations apply when a dataset is naturally discrete or "spiky"
    (containing many repeated observations of the same value). Kernel density
    estimation will always produce a smooth curve, which would be misleading
    in these situations.

    The units on the density axis are a common source of confusion. While kernel
    density estimation produces a probability distribution, the height of the curve
    at each point gives a density, not a probability. A probability can be obtained
    only by integrating the density across a range. The curve is normalized so
    that the integral over all possible values is 1, meaning that the scale of
    the density axis depends on the data values.

    Examples
    --------

    .. include:: ../docstrings/kdeplot.rst

    """

def ecdfplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    stat: Literal["proportion", "percent", "count"] = "proportion",
    complementary: bool = False,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    log_scale: _LogScale | None = None,
    legend: bool = True,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot empirical cumulative distribution functions.

    An ECDF represents the proportion or count of observations falling below each
    unique value in a dataset. Compared to a histogram or density plot, it has the
    advantage that each observation is visualized directly, meaning that there are
    no binning or smoothing parameters that need to be adjusted. It also aids direct
    comparisons between multiple distributions. A downside is that the relationship
    between the appearance of the plot and the basic properties of the distribution
    (such as its central tendency, variance, and the presence of any bimodality)
    may not be as intuitive.

    More information is provided in the :ref:`user guide <tutorial_ecdf>`.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    weights : vector or key in ``data``
        If provided, weight the contribution of the corresponding data points
        towards the cumulative distribution using these values.
    stat : {{"proportion", "percent", "count"}}
        Distribution statistic to compute.
    complementary : bool
        If True, use the complementary CDF (1 - CDF)
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.
    legend : bool
        If False, suppress the legend for semantic variables.
    ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the plot. Otherwise, call :func:`matplotlib.pyplot.gca`
        internally.
    kwargs
        Other keyword arguments are passed to :meth:`matplotlib.axes.Axes.plot`.

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The matplotlib axes containing the plot.

    See Also
    --------
    displot : Figure-level interface to distribution plot functions.
    histplot : Plot a histogram of binned counts with optional normalization or smoothing.
    kdeplot : Plot univariate or bivariate distributions using kernel density estimation.
    rugplot : Plot a tick at each observation value along the x and/or y axes.

    Examples
    --------

    .. include:: ../docstrings/ecdfplot.rst

    """

def rugplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    height: float = 0.025,
    expand_margins: bool = True,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    legend: bool = True,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot marginal distributions by drawing ticks along the x and y axes.

    This function is intended to complement other plots by showing the location
    of individual observations in an unobtrusive way.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    height : float
        Proportion of axes extent covered by each rug element. Can be negative.
    expand_margins : bool
        If True, increase the axes margins by the height of the rug to avoid
        overlap with other elements.
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    legend : bool
        If False, do not add a legend for semantic variables.
    ax : :class:`matplotlib.axes.Axes`
        Pre-existing axes for the plot. Otherwise, call :func:`matplotlib.pyplot.gca`
        internally.
    kwargs
        Other keyword arguments are passed to
        :meth:`matplotlib.collections.LineCollection`

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        The matplotlib axes containing the plot.

    Examples
    --------

    .. include:: ../docstrings/rugplot.rst

    """

def displot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    row: ColumnName | _Vector | None = None,
    col: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    kind: Literal["hist", "kde", "ecdf"] = "hist",
    rug: bool = False,
    rug_kws: dict[str, Any] | None = None,
    log_scale: _LogScale | None = None,
    legend: bool = True,
    palette: _Palette | Colormap | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    hue_norm: NormSpec = None,
    color: ColorType | None = None,
    col_wrap: int | None = None,
    row_order: Iterable[ColumnName] | None = None,
    col_order: Iterable[ColumnName] | None = None,
    height: float = 5,
    aspect: float = 1,
    facet_kws: dict[str, Any] | None = None,
    **kwargs: Any,
) -> FacetGrid:
    """Figure-level interface for drawing distribution plots onto a FacetGrid.

    This function provides access to several approaches for visualizing the
    univariate or bivariate distribution of data, including subsets of data
    defined by semantic mapping and faceting across multiple subplots. The
    ``kind`` parameter selects the approach to use:

    - :func:`histplot` (with ``kind="hist"``; the default)
    - :func:`kdeplot` (with ``kind="kde"``)
    - :func:`ecdfplot` (with ``kind="ecdf"``; univariate-only)

    Additionally, a :func:`rugplot` can be added to any kind of plot to show
    individual observations.

    Extra keyword arguments are passed to the underlying function, so you should
    refer to the documentation for each to understand the complete set of options
    for making plots with this interface.

    See the :doc:`distribution plots tutorial <../tutorial/distributions>` for a more
    in-depth discussion of the relative strengths and weaknesses of each approach.
    The distinction between figure-level and axes-level functions is explained
    further in the :doc:`user guide <../tutorial/function_overview>`.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`, :class:`numpy.ndarray`, mapping, or sequence
        Input data structure. Either a long-form collection of vectors that can be
        assigned to named variables or a wide-form dataset that will be internally
        reshaped.
    x, y : vectors or keys in ``data``
        Variables that specify positions on the x and y axes.
    hue : vector or key in ``data``
        Semantic variable that is mapped to determine the color of plot elements.
    row, col : vectors or keys in ``data``
        Variables that define subsets to plot on different facets.
    weights : vector or key in ``data``
        Observation weights used for computing the distribution function.
    kind : {"hist", "kde", "ecdf"}
        Approach for visualizing the data. Selects the underlying plotting function
        and determines the additional set of valid parameters.
    rug : bool
        If True, show each observation with marginal ticks (as in :func:`rugplot`).
    rug_kws : dict
        Parameters to control the appearance of the rug plot.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.
    legend : bool
        If False, suppress the legend for semantic variables.
    palette : string, list, dict, or :class:`matplotlib.colors.Colormap`
        Method for choosing the colors to use when mapping the ``hue`` semantic.
        String values are passed to :func:`color_palette`. List or dict values
        imply categorical mapping, while a colormap object implies numeric mapping.
    hue_order : vector of strings
        Specify the order of processing and plotting for categorical levels of the
        ``hue`` semantic.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize`
        Either a pair of values that set the normalization range in data units
        or an object that will map from data units into a [0, 1] interval. Usage
        implies numeric mapping.
    color : :mod:`matplotlib color <matplotlib.colors>`
        Single color specification for when hue mapping is not used. Otherwise, the
        plot will try to hook into the matplotlib property cycle.
    col_wrap : int
        "Wrap" the column variable at this width, so that the column facets
        span multiple rows. Incompatible with a ``row`` facet.
    {row,col}_order : vector of strings
        Specify the order in which levels of the ``row`` and/or ``col`` variables
        appear in the grid of subplots.
    height : scalar
        Height (in inches) of each facet. See also: ``aspect``.
    aspect : scalar
        Aspect ratio of each facet, so that ``aspect * height`` gives the width
        of each facet in inches.
    facet_kws : dict
        Additional parameters passed to :class:`FacetGrid`.

    kwargs
        Other keyword arguments are documented with the relevant axes-level function:

        - :func:`histplot` (with ``kind="hist"``)
        - :func:`kdeplot` (with ``kind="kde"``)
        - :func:`ecdfplot` (with ``kind="ecdf"``)

    Returns
    -------
    :class:`FacetGrid`
        An object managing one or more subplots that correspond to conditional data
        subsets with convenient methods for batch-setting of axes attributes.

    See Also
    --------
    histplot : Plot a histogram of binned counts with optional normalization or smoothing.
    kdeplot : Plot univariate or bivariate distributions using kernel density estimation.
    rugplot : Plot a tick at each observation value along the x and/or y axes.
    ecdfplot : Plot empirical cumulative distribution functions.
    jointplot : Draw a bivariate plot with univariate marginal distributions.

    Examples
    --------

    See the API documentation for the axes-level functions for more details
    about the breadth of options available for each plot kind.

    .. include:: ../docstrings/displot.rst

    """

@deprecated("Function `distplot` is deprecated and will be removed in seaborn v0.14.0")
def distplot(
    a: ArrayLike | None = None,
    bins: ArrayLike | None = None,
    hist: bool = True,
    kde: bool = True,
    rug: bool = False,
    fit: _Fit | None = None,
    hist_kws: dict[str, Any] | None = None,
    kde_kws: dict[str, Any] | None = None,
    rug_kws: dict[str, Any] | None = None,
    fit_kws: dict[str, Any] | None = None,
    color: ColorType | None = None,
    vertical: bool = False,
    norm_hist: bool = False,
    axlabel: str | Literal[False] | None = None,
    label: str | None = None,
    ax: Axes | None = None,
    x: ArrayLike | None = None,
) -> Axes:
    """
    DEPRECATED

    This function has been deprecated and will be removed in seaborn v0.14.0.
    It has been replaced by :func:`histplot` and :func:`displot`, two functions
    with a modern API and many more capabilities.

    For a guide to updating, please see this notebook:

    https://gist.github.com/mwaskom/de44147ed2974457ad6372750bbe5751

    """
