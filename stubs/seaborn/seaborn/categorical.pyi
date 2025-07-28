from collections.abc import Callable, Iterable
from typing import Any, Literal

from matplotlib.axes import Axes
from matplotlib.typing import ColorType, LineStyleType, MarkerType

from ._core.typing import ColumnName, DataSource, Default, NormSpec
from .axisgrid import FacetGrid
from .external.kde import _BwMethodType
from .utils import _DataSourceWideForm, _ErrorBar, _Estimator, _Legend, _LogScale, _Palette, _Seed, _Vector

__all__ = ["catplot", "stripplot", "swarmplot", "boxplot", "violinplot", "boxenplot", "pointplot", "barplot", "countplot"]

def boxplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    saturation: float = 0.75,
    fill: bool = True,
    dodge: bool | Literal["auto"] = "auto",
    width: float = 0.8,
    gap: float = 0,
    whis: float = 1.5,
    linecolor: ColorType = "auto",
    linewidth: float | None = None,
    fliersize: float | None = None,
    hue_norm: NormSpec = None,
    native_scale: bool = False,
    log_scale: _LogScale | None = None,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Draw a box plot to show distributions with respect to categories.

    A box plot (or box-and-whisker plot) shows the distribution of quantitative
    data in a way that facilitates comparisons between variables or across
    levels of a categorical variable. The box shows the quartiles of the
    dataset while the whiskers extend to show the rest of the distribution,
    except for points that are determined to be "outliers" using a method
    that is a function of the inter-quartile range.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    saturation : float
        Proportion of the original saturation to draw fill colors in. Large
        patches often look better with desaturated colors, but set this to
        `1` if you want the colors to perfectly match the input values.
    fill : bool
        If True, use a solid patch. Otherwise, draw as line art.

        .. versionadded:: v0.13.0
    dodge : "auto" or bool
        When hue mapping is used, whether elements should be narrowed and shifted along
        the orient axis to eliminate overlap. If `"auto"`, set to `True` when the
        orient variable is crossed with the categorical variable or `False` otherwise.

        .. versionchanged:: 0.13.0

            Added `"auto"` mode as a new default.
    width : float
        Width allotted to each element on the orient axis. When `native_scale=True`,
        it is relative to the minimum distance between two values in the native scale.
    gap : float
        Shrink on the orient axis by this factor to add a gap between dodged elements.

        .. versionadded:: 0.13.0
    whis : float or pair of floats
        Paramater that controls whisker length. If scalar, whiskers are drawn
        to the farthest datapoint within *whis * IQR* from the nearest hinge.
        If a tuple, it is interpreted as percentiles that whiskers represent.
    linecolor : color
        Color to use for line elements, when `fill` is True.

        .. versionadded:: v0.13.0
    linewidth : float
        Width of the lines that frame the plot elements.
    fliersize : float
        Size of the markers used to indicate outlier observations.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other keyword arguments are passed through to
        :meth:`matplotlib.axes.Axes.boxplot`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    violinplot : A combination of boxplot and kernel density estimation.
    stripplot : A scatterplot where one variable is categorical. Can be used
                in conjunction with other plots to show each observation.
    swarmplot : A categorical scatterplot where the points do not overlap. Can
                be used with other plots to show each observation.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Examples
    --------
    .. include:: ../docstrings/boxplot.rst

    """

def violinplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    saturation: float = 0.75,
    fill: bool = True,
    inner: str | None = "box",
    split: bool = False,
    width: float = 0.8,
    dodge: bool | Literal["auto"] = "auto",
    gap: float = 0,
    linewidth: float | None = None,
    linecolor: ColorType = "auto",
    cut: float = 2,
    gridsize: int = 100,
    bw_method: _BwMethodType = "scott",
    bw_adjust: float = 1,
    density_norm: Literal["area", "count", "width"] = "area",
    common_norm: bool | None = False,
    hue_norm: NormSpec = None,
    formatter: Callable[[Any], str] | None = None,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    legend: _Legend = "auto",
    scale=...,  # deprecated
    scale_hue=...,  # deprecated
    bw=...,  # deprecated
    inner_kws: dict[str, Any] | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Draw a patch representing a KDE and add observations or box plot statistics.

    A violin plot plays a similar role as a box-and-whisker plot. It shows the
    distribution of data points after grouping by one (or more) variables.
    Unlike a box plot, each violin is drawn using a kernel density estimate
    of the underlying distribution.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    saturation : float
        Proportion of the original saturation to draw fill colors in. Large
        patches often look better with desaturated colors, but set this to
        `1` if you want the colors to perfectly match the input values.
    fill : bool
        If True, use a solid patch. Otherwise, draw as line art.

        .. versionadded:: v0.13.0
    inner : {"box", "quart", "point", "stick", None}
        Representation of the data in the violin interior. One of the following:

        - `"box"`: draw a miniature box-and-whisker plot
        - `"quart"`: show the quartiles of the data
        - `"point"` or `"stick"`: show each observation
    split : bool
        Show an un-mirrored distribution, alternating sides when using `hue`.

        .. versionchanged:: v0.13.0
            Previously, this option required a `hue` variable with exactly two levels.
    width : float
        Width allotted to each element on the orient axis. When `native_scale=True`,
        it is relative to the minimum distance between two values in the native scale.
    dodge : "auto" or bool
        When hue mapping is used, whether elements should be narrowed and shifted along
        the orient axis to eliminate overlap. If `"auto"`, set to `True` when the
        orient variable is crossed with the categorical variable or `False` otherwise.

        .. versionchanged:: 0.13.0

            Added `"auto"` mode as a new default.
    gap : float
        Shrink on the orient axis by this factor to add a gap between dodged elements.

        .. versionadded:: 0.13.0
    linewidth : float
        Width of the lines that frame the plot elements.
    linecolor : color
        Color to use for line elements, when `fill` is True.

        .. versionadded:: v0.13.0
    cut : float
        Distance, in units of bandwidth, to extend the density past extreme
        datapoints. Set to 0 to limit the violin within the data range.
    gridsize : int
        Number of points in the discrete grid used to evaluate the KDE.
    bw_method : {"scott", "silverman", float}
        Either the name of a reference rule or the scale factor to use when
        computing the kernel bandwidth. The actual kernel size will be
        determined by multiplying the scale factor by the standard deviation of
        the data within each group.

        .. versionadded:: v0.13.0
    bw_adjust: float
        Factor that scales the bandwidth to use more or less smoothing.

        .. versionadded:: v0.13.0
    density_norm : {"area", "count", "width"}
        Method that normalizes each density to determine the violin's width.
        If `area`, each violin will have the same area. If `count`, the width
        will be proportional to the number of observations. If `width`, each
        violin will have the same width.

        .. versionadded:: v0.13.0
    common_norm : bool
        When `True`, normalize the density across all violins.

        .. versionadded:: v0.13.0
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    scale : {"area", "count", "width"}
        .. deprecated:: v0.13.0
            See `density_norm`.
    scale_hue : bool
        .. deprecated:: v0.13.0
            See `common_norm`.
    bw : {'scott', 'silverman', float}
        .. deprecated:: v0.13.0
            See `bw_method` and `bw_adjust`.
    inner_kws : dict of key, value mappings
        Keyword arguments for the "inner" plot, passed to one of:

        - :class:`matplotlib.collections.LineCollection` (with `inner="stick"`)
        - :meth:`matplotlib.axes.Axes.scatter` (with `inner="point"`)
        - :meth:`matplotlib.axes.Axes.plot` (with `inner="quart"` or `inner="box"`)

        Additionally, with `inner="box"`, the keywords `box_width`, `whis_width`,
        and `marker` receive special handling for the components of the "box" plot.

        .. versionadded:: v0.13.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Keyword arguments for the violin patches, passsed through to
        :meth:`matplotlib.axes.Axes.fill_between`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    boxplot : A traditional box-and-whisker plot with a similar API.
    stripplot : A scatterplot where one variable is categorical. Can be used
                in conjunction with other plots to show each observation.
    swarmplot : A categorical scatterplot where the points do not overlap. Can
                be used with other plots to show each observation.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Examples
    --------
    .. include:: ../docstrings/violinplot.rst

    """

def boxenplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    saturation: float = 0.75,
    fill: bool = True,
    dodge: bool | Literal["auto"] = "auto",
    width: float = 0.8,
    gap: float = 0,
    linewidth: float | None = None,
    linecolor: ColorType | None = None,
    width_method: Literal["exponential", "linear", "area"] = "exponential",
    k_depth: Literal["tukey", "proportion", "trustworthy", "full"] | int = "tukey",
    outlier_prop: float = 0.007,
    trust_alpha: float = 0.05,
    showfliers: bool = True,
    hue_norm: NormSpec = None,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    scale=...,  # deprecated
    box_kws: dict[str, Any] | None = None,
    flier_kws: dict[str, Any] | None = None,
    line_kws: dict[str, Any] | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Draw an enhanced box plot for larger datasets.

    This style of plot was originally named a "letter value" plot because it
    shows a large number of quantiles that are defined as "letter values".  It
    is similar to a box plot in plotting a nonparametric representation of a
    distribution in which all features correspond to actual observations. By
    plotting more quantiles, it provides more information about the shape of
    the distribution, particularly in the tails.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    saturation : float
        Proportion of the original saturation to draw fill colors in. Large
        patches often look better with desaturated colors, but set this to
        `1` if you want the colors to perfectly match the input values.
    fill : bool
        If True, use a solid patch. Otherwise, draw as line art.

        .. versionadded:: v0.13.0
    dodge : "auto" or bool
        When hue mapping is used, whether elements should be narrowed and shifted along
        the orient axis to eliminate overlap. If `"auto"`, set to `True` when the
        orient variable is crossed with the categorical variable or `False` otherwise.

        .. versionchanged:: 0.13.0

            Added `"auto"` mode as a new default.
    width : float
        Width allotted to each element on the orient axis. When `native_scale=True`,
        it is relative to the minimum distance between two values in the native scale.
    gap : float
        Shrink on the orient axis by this factor to add a gap between dodged elements.

        .. versionadded:: 0.13.0
    linewidth : float
        Width of the lines that frame the plot elements.
    linecolor : color
        Color to use for line elements, when `fill` is True.

        .. versionadded:: v0.13.0
    width_method : {"exponential", "linear", "area"}
        Method to use for the width of the letter value boxes:

        - `"exponential"`: Represent the corresponding percentile
        - `"linear"`: Decrease by a constant amount for each box
        - `"area"`: Represent the density of data points in that box
    k_depth : {"tukey", "proportion", "trustworthy", "full"} or int
        The number of levels to compute and draw in each tail:

        - `"tukey"`: Use log2(n) - 3 levels, covering similar range as boxplot whiskers
        - `"proportion"`: Leave approximately `outlier_prop` fliers
        - `"trusthworthy"`: Extend to level with confidence of at least `trust_alpha`
        - `"full"`: Use log2(n) + 1 levels and extend to most extreme points
    outlier_prop : float
        Proportion of data expected to be outliers; used when `k_depth="proportion"`.
    trust_alpha : float
        Confidence threshold for most extreme level; used when `k_depth="trustworthy"`.
    showfliers : bool
        If False, suppress the plotting of outliers.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    box_kws: dict
        Keyword arguments for the box artists; passed to
        :class:`matplotlib.patches.Rectangle`.

        .. versionadded:: v0.12.0
    line_kws: dict
        Keyword arguments for the line denoting the median; passed to
        :meth:`matplotlib.axes.Axes.plot`.

        .. versionadded:: v0.12.0
    flier_kws: dict
        Keyword arguments for the scatter denoting the outlier observations;
        passed to :meth:`matplotlib.axes.Axes.scatter`.

        .. versionadded:: v0.12.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other keyword arguments are passed to :class:`matplotlib.patches.Rectangle`,
        superceded by those in `box_kws`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    violinplot : A combination of boxplot and kernel density estimation.
    boxplot : A traditional box-and-whisker plot with a similar API.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Notes
    -----

    For a more extensive explanation, you can read the paper that introduced the plot:
    https://vita.had.co.nz/papers/letter-value-plot.html

    Examples
    --------
    .. include:: ../docstrings/boxenplot.rst

    """

def stripplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    jitter: float | Literal[True] = True,
    dodge: bool = False,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    size: float = 5,
    edgecolor: ColorType | Default = ...,
    linewidth: float = 0,
    hue_norm: NormSpec = None,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Draw a categorical scatterplot using jitter to reduce overplotting.

    A strip plot can be drawn on its own, but it is also a good complement
    to a box or violin plot in cases where you want to show all observations
    along with some representation of the underlying distribution.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    jitter : float, `True`/`1` is special-cased
        Amount of jitter (only along the categorical axis) to apply. This
        can be useful when you have many points and they overlap, so that
        it is easier to see the distribution. You can specify the amount
        of jitter (half the width of the uniform random variable support),
        or use `True` for a good default.
    dodge : bool
        When a `hue` variable is assigned, setting this to `True` will
        separate the strips for different hue levels along the categorical
        axis and narrow the amount of space allotedto each strip. Otherwise,
        the points for each level will be plotted in the same strip.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    size : float
        Radius of the markers, in points.
    edgecolor : matplotlib color, "gray" is special-cased
        Color of the lines around each point. If you pass `"gray"`, the
        brightness is determined by the color palette used for the body
        of the points. Note that `stripplot` has `linewidth=0` by default,
        so edge colors are only visible with nonzero line width.
    linewidth : float
        Width of the lines that frame the plot elements.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other keyword arguments are passed through to
        :meth:`matplotlib.axes.Axes.scatter`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    swarmplot : A categorical scatterplot where the points do not overlap. Can
                be used with other plots to show each observation.
    boxplot : A traditional box-and-whisker plot with a similar API.
    violinplot : A combination of boxplot and kernel density estimation.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Examples
    --------
    .. include:: ../docstrings/stripplot.rst

    """

def swarmplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    dodge: bool = False,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    size: float = 5,
    edgecolor: ColorType | None = None,
    linewidth: float = 0,
    hue_norm: NormSpec = None,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    warn_thresh: float = 0.05,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Draw a categorical scatterplot with points adjusted to be non-overlapping.

    This function is similar to :func:`stripplot`, but the points are adjusted
    (only along the categorical axis) so that they don't overlap. This gives a
    better representation of the distribution of values, but it does not scale
    well to large numbers of observations. This style of plot is sometimes
    called a "beeswarm".

    A swarm plot can be drawn on its own, but it is also a good complement
    to a box or violin plot in cases where you want to show all observations
    along with some representation of the underlying distribution.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    dodge : bool
        When a `hue` variable is assigned, setting this to `True` will
        separate the swarms for different hue levels along the categorical
        axis and narrow the amount of space allotedto each strip. Otherwise,
        the points for each level will be plotted in the same swarm.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    size : float
        Radius of the markers, in points.
    edgecolor : matplotlib color, "gray" is special-cased
        Color of the lines around each point. If you pass `"gray"`, the
        brightness is determined by the color palette used for the body
        of the points.
    linewidth : float
        Width of the lines that frame the plot elements.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other keyword arguments are passed through to
        :meth:`matplotlib.axes.Axes.scatter`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    boxplot : A traditional box-and-whisker plot with a similar API.
    violinplot : A combination of boxplot and kernel density estimation.
    stripplot : A scatterplot where one variable is categorical. Can be used
                in conjunction with other plots to show each observation.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Examples
    --------
    .. include:: ../docstrings/swarmplot.rst

    """

def barplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    estimator: _Estimator = "mean",
    errorbar: _ErrorBar | None = ("ci", 95),
    n_boot: int = 1000,
    units: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    seed: _Seed | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    saturation: float = 0.75,
    fill: bool = True,
    hue_norm: NormSpec = None,
    width: float = 0.8,
    dodge: bool | Literal["auto"] = "auto",
    gap: float = 0,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    capsize: float = 0,
    err_kws: dict[str, Any] | None = None,
    ci=...,  # deprecated
    errcolor=...,  # deprecated
    errwidth=...,  # deprecated
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Show point estimates and errors as rectangular bars.

    A bar plot represents an aggregate or statistical estimate for a numeric
    variable with the height of each rectangle and indicates the uncertainty
    around that estimate using an error bar. Bar plots include 0 in the
    axis range, and they are a good choice when 0 is a meaningful value
    for the variable to take.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    estimator : string or callable that maps vector -> scalar
        Statistical function to estimate within each categorical bin.
    errorbar : string, (string, number) tuple, callable or None
        Name of errorbar method (either "ci", "pi", "se", or "sd"), or a tuple
        with a method name and a level parameter, or a function that maps from a
        vector to a (min, max) interval, or None to hide errorbar. See the
        :doc:`errorbar tutorial </tutorial/error_bars>` for more information.

        .. versionadded:: v0.12.0
    n_boot : int
        Number of bootstrap samples used to compute confidence intervals.
    seed : int, `numpy.random.Generator`, or `numpy.random.RandomState`
        Seed or random number generator for reproducible bootstrapping.
    units : name of variable in `data` or vector data
        Identifier of sampling units; used by the errorbar function to
        perform a multilevel bootstrap and account for repeated measures
    weights : name of variable in `data` or vector data
        Data values or column used to compute weighted statistics.
        Note that the use of weights may limit other statistical options.

        .. versionadded:: v0.13.1
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    saturation : float
        Proportion of the original saturation to draw fill colors in. Large
        patches often look better with desaturated colors, but set this to
        `1` if you want the colors to perfectly match the input values.
    fill : bool
        If True, use a solid patch. Otherwise, draw as line art.

        .. versionadded:: v0.13.0
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    width : float
        Width allotted to each element on the orient axis. When `native_scale=True`,
        it is relative to the minimum distance between two values in the native scale.
    dodge : "auto" or bool
        When hue mapping is used, whether elements should be narrowed and shifted along
        the orient axis to eliminate overlap. If `"auto"`, set to `True` when the
        orient variable is crossed with the categorical variable or `False` otherwise.

        .. versionchanged:: 0.13.0

            Added `"auto"` mode as a new default.
    gap : float
        Shrink on the orient axis by this factor to add a gap between dodged elements.

        .. versionadded:: 0.13.0
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    capsize : float
        Width of the "caps" on error bars, relative to bar spacing.
    err_kws : dict
        Parameters of :class:`matplotlib.lines.Line2D`, for the error bar artists.

        .. versionadded:: v0.13.0
    ci : float
        Level of the confidence interval to show, in [0, 100].

        .. deprecated:: v0.12.0
            Use `errorbar=("ci", ...)`.
    errcolor : matplotlib color
        Color used for the error bar lines.

        .. deprecated:: 0.13.0
            Use `err_kws={'color': ...}`.
    errwidth : float
        Thickness of error bar lines (and caps), in points.

        .. deprecated:: 0.13.0
            Use `err_kws={'linewidth': ...}`.
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other parameters are passed through to :class:`matplotlib.patches.Rectangle`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    countplot : Show the counts of observations in each categorical bin.
    pointplot : Show point estimates and confidence intervals using dots.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Notes
    -----

    For datasets where 0 is not a meaningful value, a :func:`pointplot` will
    allow you to focus on differences between levels of one or more categorical
    variables.

    It is also important to keep in mind that a bar plot shows only the mean (or
    other aggregate) value, but it is often more informative to show the
    distribution of values at each level of the categorical variables. In those
    cases, approaches such as a :func:`boxplot` or :func:`violinplot` may be
    more appropriate.

    Examples
    --------
    .. include:: ../docstrings/barplot.rst

    """

def pointplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    estimator: _Estimator = "mean",
    errorbar: _ErrorBar | None = ("ci", 95),
    n_boot: int = 1000,
    units: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    seed: _Seed | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    hue_norm: NormSpec = None,
    markers: MarkerType | list[MarkerType] | Default = ...,
    linestyles: LineStyleType | list[LineStyleType] | Default = ...,
    dodge: bool = False,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    orient: Literal["v", "h", "x", "y"] | None = None,
    capsize: float = 0,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    err_kws: dict[str, Any] | None = None,
    ci=...,  # deprecated
    errwidth=...,  # deprecated
    join=...,  # deprecated
    scale=...,  # deprecated
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Show point estimates and errors using lines with markers.

    A point plot represents an estimate of central tendency for a numeric
    variable by the position of the dot and provides some indication of the
    uncertainty around that estimate using error bars.

    Point plots can be more useful than bar plots for focusing comparisons
    between different levels of one or more categorical variables. They are
    particularly adept at showing interactions: how the relationship between
    levels of one categorical variable changes across levels of a second
    categorical variable. The lines that join each point from the same `hue`
    level allow interactions to be judged by differences in slope, which is
    easier for the eyes than comparing the heights of several groups of points
    or bars.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    estimator : string or callable that maps vector -> scalar
        Statistical function to estimate within each categorical bin.
    errorbar : string, (string, number) tuple, callable or None
        Name of errorbar method (either "ci", "pi", "se", or "sd"), or a tuple
        with a method name and a level parameter, or a function that maps from a
        vector to a (min, max) interval, or None to hide errorbar. See the
        :doc:`errorbar tutorial </tutorial/error_bars>` for more information.

        .. versionadded:: v0.12.0
    n_boot : int
        Number of bootstrap samples used to compute confidence intervals.
    seed : int, `numpy.random.Generator`, or `numpy.random.RandomState`
        Seed or random number generator for reproducible bootstrapping.
    units : name of variable in `data` or vector data
        Identifier of sampling units; used by the errorbar function to
        perform a multilevel bootstrap and account for repeated measures
    weights : name of variable in `data` or vector data
        Data values or column used to compute weighted statistics.
        Note that the use of weights may limit other statistical options.

        .. versionadded:: v0.13.1
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    markers : string or list of strings
        Markers to use for each of the `hue` levels.
    linestyles : string or list of strings
        Line styles to use for each of the `hue` levels.
    dodge : bool or float
        Amount to separate the points for each level of the `hue` variable along
        the categorical axis. Setting to `True` will apply a small default.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    capsize : float
        Width of the "caps" on error bars, relative to bar spacing.
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    err_kws : dict
        Parameters of :class:`matplotlib.lines.Line2D`, for the error bar artists.

        .. versionadded:: v0.13.0
    ci : float
        Level of the confidence interval to show, in [0, 100].

        .. deprecated:: v0.12.0
            Use `errorbar=("ci", ...)`.
    errwidth : float
        Thickness of error bar lines (and caps), in points.

        .. deprecated:: 0.13.0
            Use `err_kws={'linewidth': ...}`.
    join : bool
        If `True`, connect point estimates with a line.

        .. deprecated:: v0.13.0
            Set `linestyle="none"` to remove the lines between the points.
    scale : float
        Scale factor for the plot elements.

        .. deprecated:: v0.13.0
            Control element sizes with :class:`matplotlib.lines.Line2D` parameters.
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other parameters are passed through to :class:`matplotlib.lines.Line2D`.

        .. versionadded:: v0.13.0

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    barplot : Show point estimates and confidence intervals using bars.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Notes
    -----
    It is important to keep in mind that a point plot shows only the mean (or
    other estimator) value, but in many cases it may be more informative to
    show the distribution of values at each level of the categorical variables.
    In that case, other approaches such as a box or violin plot may be more
    appropriate.

    Examples
    --------
    .. include:: ../docstrings/pointplot.rst

    """

def countplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    saturation: float = 0.75,
    fill: bool = True,
    hue_norm: NormSpec = None,
    stat: Literal["count", "percent", "proportion", "probability"] = "count",
    width: float = 0.8,
    dodge: bool | Literal["auto"] = "auto",
    gap: float = 0,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    legend: _Legend = "auto",
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Show the counts of observations in each categorical bin using bars.

    A count plot can be thought of as a histogram across a categorical, instead
    of quantitative, variable. The basic API and options are identical to those
    for :func:`barplot`, so you can compare counts across nested variables.

    Note that :func:`histplot` function offers similar functionality with additional
    features (e.g. bar stacking), although its default behavior is somewhat different.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    saturation : float
        Proportion of the original saturation to draw fill colors in. Large
        patches often look better with desaturated colors, but set this to
        `1` if you want the colors to perfectly match the input values.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    stat : {'count', 'percent', 'proportion', 'probability'}
        Statistic to compute; when not `'count'`, bar heights will be normalized so that
        they sum to 100 (for `'percent'`) or 1 (otherwise) across the plot.

        .. versionadded:: v0.13.0
    width : float
        Width allotted to each element on the orient axis. When `native_scale=True`,
        it is relative to the minimum distance between two values in the native scale.
    dodge : "auto" or bool
        When hue mapping is used, whether elements should be narrowed and shifted along
        the orient axis to eliminate overlap. If `"auto"`, set to `True` when the
        orient variable is crossed with the categorical variable or `False` otherwise.

        .. versionchanged:: 0.13.0

            Added `"auto"` mode as a new default.
    log_scale : bool or number, or pair of bools or numbers
        Set axis scale(s) to log. A single value sets the data axis for any numeric
        axes in the plot. A pair of values sets each axis independently.
        Numeric values are interpreted as the desired base (default 10).
        When `None` or `False`, seaborn defers to the existing Axes scale.

        .. versionadded:: v0.13.0
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    ax : matplotlib Axes
        Axes object to draw the plot onto, otherwise uses the current Axes.
    kwargs : key, value mappings
        Other parameters are passed through to :class:`matplotlib.patches.Rectangle`.

    Returns
    -------
    ax : matplotlib Axes
        Returns the Axes object with the plot drawn onto it.

    See Also
    --------
    histplot : Bin and count observations with additional options.
    barplot : Show point estimates and confidence intervals using bars.
    catplot : Combine a categorical plot with a :class:`FacetGrid`.

    Examples
    --------
    .. include:: ../docstrings/countplot.rst

    """

def catplot(
    data: DataSource | _DataSourceWideForm | None = None,
    *,
    x: ColumnName | _Vector | None = None,
    y: ColumnName | _Vector | None = None,
    hue: ColumnName | _Vector | None = None,
    row: ColumnName | _Vector | None = None,
    col: ColumnName | _Vector | None = None,
    kind: Literal["strip", "swarm", "box", "violin", "boxen", "point", "bar", "count"] = "strip",
    estimator: _Estimator = "mean",
    errorbar: _ErrorBar | None = ("ci", 95),
    n_boot: int = 1000,
    units: ColumnName | _Vector | None = None,
    weights: ColumnName | _Vector | None = None,
    seed: _Seed | None = None,
    order: Iterable[ColumnName] | None = None,
    hue_order: Iterable[ColumnName] | None = None,
    row_order: Iterable[ColumnName] | None = None,
    col_order: Iterable[ColumnName] | None = None,
    col_wrap: int | None = None,
    height: float = 5,
    aspect: float = 1,
    log_scale: _LogScale | None = None,
    native_scale: bool = False,
    formatter: Callable[[Any], str] | None = None,
    orient: Literal["v", "h", "x", "y"] | None = None,
    color: ColorType | None = None,
    palette: _Palette | None = None,
    hue_norm: NormSpec = None,
    legend: _Legend = "auto",
    legend_out: bool = True,
    sharex: bool = True,
    sharey: bool = True,
    margin_titles: bool = False,
    facet_kws: dict[str, Any] | None = None,
    ci=...,  # deprecated
    **kwargs: Any,
) -> FacetGrid:
    """Figure-level interface for drawing categorical plots onto a FacetGrid.

    This function provides access to several axes-level functions that
    show the relationship between a numerical and one or more categorical
    variables using one of several visual representations. The `kind`
    parameter selects the underlying axes-level function to use.

    Categorical scatterplots:

    - :func:`stripplot` (with `kind="strip"`; the default)
    - :func:`swarmplot` (with `kind="swarm"`)

    Categorical distribution plots:

    - :func:`boxplot` (with `kind="box"`)
    - :func:`violinplot` (with `kind="violin"`)
    - :func:`boxenplot` (with `kind="boxen"`)

    Categorical estimate plots:

    - :func:`pointplot` (with `kind="point"`)
    - :func:`barplot` (with `kind="bar"`)
    - :func:`countplot` (with `kind="count"`)

    Extra keyword arguments are passed to the underlying function, so you
    should refer to the documentation for each to see kind-specific options.

    See the :ref:`tutorial <categorical_tutorial>` for more information.

    .. note::
        By default, this function treats one of the variables as categorical
        and draws data at ordinal positions (0, 1, ... n) on the relevant axis.
        As of version 0.13.0, this can be disabled by setting `native_scale=True`.


    After plotting, the :class:`FacetGrid` with the plot is returned and can
    be used directly to tweak supporting plot details or add other layers.

    Parameters
    ----------
    data : DataFrame, Series, dict, array, or list of arrays
        Dataset for plotting. If `x` and `y` are absent, this is
        interpreted as wide-form. Otherwise it is expected to be long-form.
    x, y, hue : names of variables in `data` or vector data
        Inputs for plotting long-form data. See examples for interpretation.
    row, col : names of variables in `data` or vector data
        Categorical variables that will determine the faceting of the grid.
    kind : str
        The kind of plot to draw, corresponds to the name of a categorical
        axes-level plotting function. Options are: "strip", "swarm", "box", "violin",
        "boxen", "point", "bar", or "count".
    estimator : string or callable that maps vector -> scalar
        Statistical function to estimate within each categorical bin.
    errorbar : string, (string, number) tuple, callable or None
        Name of errorbar method (either "ci", "pi", "se", or "sd"), or a tuple
        with a method name and a level parameter, or a function that maps from a
        vector to a (min, max) interval, or None to hide errorbar. See the
        :doc:`errorbar tutorial </tutorial/error_bars>` for more information.

        .. versionadded:: v0.12.0
    n_boot : int
        Number of bootstrap samples used to compute confidence intervals.
    seed : int, `numpy.random.Generator`, or `numpy.random.RandomState`
        Seed or random number generator for reproducible bootstrapping.
    units : name of variable in `data` or vector data
        Identifier of sampling units; used by the errorbar function to
        perform a multilevel bootstrap and account for repeated measures
    weights : name of variable in `data` or vector data
        Data values or column used to compute weighted statistics.
        Note that the use of weights may limit other statistical options.

        .. versionadded:: v0.13.1
    order, hue_order : lists of strings
        Order to plot the categorical levels in; otherwise the levels are
        inferred from the data objects.
    row_order, col_order : lists of strings
        Order to organize the rows and/or columns of the grid in; otherwise the
        orders are inferred from the data objects.
    col_wrap : int
        "Wrap" the column variable at this width, so that the column facets
        span multiple rows. Incompatible with a ``row`` facet.
    height : scalar
        Height (in inches) of each facet. See also: ``aspect``.
    aspect : scalar
        Aspect ratio of each facet, so that ``aspect * height`` gives the width
        of each facet in inches.
    native_scale : bool
        When True, numeric or datetime values on the categorical axis will maintain
        their original scaling rather than being converted to fixed indices.

        .. versionadded:: v0.13.0
    formatter : callable
        Function for converting categorical data into strings. Affects both grouping
        and tick labels.

        .. versionadded:: v0.13.0
    orient : "v" | "h" | "x" | "y"
        Orientation of the plot (vertical or horizontal). This is usually
        inferred based on the type of the input variables, but it can be used
        to resolve ambiguity when both `x` and `y` are numeric or when
        plotting wide-form data.

        .. versionchanged:: v0.13.0
            Added 'x'/'y' as options, equivalent to 'v'/'h'.
    color : matplotlib color
        Single color for the elements in the plot.
    palette : palette name, list, or dict
        Colors to use for the different levels of the ``hue`` variable. Should
        be something that can be interpreted by :func:`color_palette`, or a
        dictionary mapping hue levels to matplotlib colors.
    hue_norm : tuple or :class:`matplotlib.colors.Normalize` object
        Normalization in data units for colormap applied to the `hue`
        variable when it is numeric. Not relevant if `hue` is categorical.

        .. versionadded:: v0.12.0
    legend : "auto", "brief", "full", or False
        How to draw the legend. If "brief", numeric `hue` and `size`
        variables will be represented with a sample of evenly spaced values.
        If "full", every group will get an entry in the legend. If "auto",
        choose between brief or full representation based on number of levels.
        If `False`, no legend data is added and no legend is drawn.

        .. versionadded:: v0.13.0
    legend_out : bool
        If ``True``, the figure size will be extended, and the legend will be
        drawn outside the plot on the center right.
    share{x,y} : bool, 'col', or 'row' optional
        If true, the facets will share y axes across columns and/or x axes
        across rows.
    margin_titles : bool
        If ``True``, the titles for the row variable are drawn to the right of
        the last column. This option is experimental and may not work in all
        cases.
    facet_kws : dict
        Dictionary of other keyword arguments to pass to :class:`FacetGrid`.
    kwargs : key, value pairings
        Other keyword arguments are passed through to the underlying plotting
        function.

    Returns
    -------
    :class:`FacetGrid`
        Returns the :class:`FacetGrid` object with the plot on it for further
        tweaking.

    Examples
    --------
    .. include:: ../docstrings/catplot.rst

    """
