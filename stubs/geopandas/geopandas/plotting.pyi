from _typeshed import Incomplete
from collections.abc import Collection, Hashable, Iterable, Mapping, Sequence
from typing import Literal, overload
from typing_extensions import TypeAlias

import numpy as np
import pandas as pd
from matplotlib.axes import Axes  # type: ignore[import-not-found]
from matplotlib.colors import Colormap, Normalize  # type: ignore[import-not-found]
from matplotlib.typing import ColorType  # type: ignore[import-not-found]
from numpy.typing import ArrayLike, NDArray
from pandas.plotting import PlotAccessor

from .geodataframe import GeoDataFrame
from .geoseries import GeoSeries

_ColorOrColors: TypeAlias = ColorType | Sequence[ColorType] | ArrayLike

def plot_series(
    s: GeoSeries,
    cmap: str | Colormap | None = None,
    color: _ColorOrColors | None = None,
    ax: Axes | None = None,
    figsize: tuple[float, float] | None = None,
    aspect: Literal["auto", "equal"] | float | None = "auto",
    autolim: bool = True,
    *,
    # Extracted from `**style_kwds`
    vmin: float = ...,
    vmax: float = ...,
    facecolor: _ColorOrColors | None = None,
    norm: Normalize | None = None,
    **style_kwds,
) -> Axes:
    """
    Plot a GeoSeries.

    Generate a plot of a GeoSeries geometry with matplotlib.

    Parameters
    ----------
    s : Series
        The GeoSeries to be plotted. Currently Polygon,
        MultiPolygon, LineString, MultiLineString, Point and MultiPoint
        geometries can be plotted.
    cmap : str (default None)
        The name of a colormap recognized by matplotlib. Any
        colormap will work, but categorical colormaps are
        generally recommended. Examples of useful discrete
        colormaps include:

            tab10, tab20, Accent, Dark2, Paired, Pastel1, Set1, Set2

    color : str, np.array, pd.Series, List (default None)
        If specified, all objects will be colored uniformly.
    ax : matplotlib.pyplot.Artist (default None)
        axes on which to draw the plot
    figsize : pair of floats (default None)
        Size of the resulting matplotlib.figure.Figure. If the argument
        ax is given explicitly, figsize is ignored.
    aspect : 'auto', 'equal', None or float (default 'auto')
        Set aspect of axis. If 'auto', the default aspect for map plots is 'equal'; if
        however data are not projected (coordinates are long/lat), the aspect is by
        default set to 1/cos(s_y * pi/180) with s_y the y coordinate of the middle of
        the GeoSeries (the mean of the y range of bounding box) so that a long/lat
        square appears square in the middle of the plot. This implies an
        Equirectangular projection. If None, the aspect of `ax` won't be changed. It can
        also be set manually (float) as the ratio of y-unit to x-unit.
    autolim : bool (default True)
        Update axes data limits to contain the new geometries.
    **style_kwds : dict
        Color options to be passed on to the actual plot function, such
        as ``edgecolor``, ``facecolor``, ``linewidth``, ``markersize``,
        ``alpha``.

    Returns
    -------
    ax : matplotlib axes instance
    """

# IMPORTANT: keep roughly in sync with `GeoplotAccessor` methods below
def plot_dataframe(
    df: GeoDataFrame,
    column: Hashable | None = None,
    cmap: str | Colormap | None = None,
    color: _ColorOrColors | None = None,
    ax: Axes | None = None,
    cax: Axes | None = None,
    categorical: bool = False,
    legend: bool = False,
    scheme: str | None = None,
    k: int = 5,
    vmin: float | None = None,
    vmax: float | None = None,
    markersize: str | float | Iterable[float] | ArrayLike | None = None,
    figsize: tuple[float, float] | None = None,
    legend_kwds: dict[str, Incomplete] | None = None,
    categories: Iterable[Hashable] | None = None,
    classification_kwds: dict[str, Incomplete] | None = None,
    missing_kwds: dict[str, Incomplete] | None = None,
    aspect: Literal["auto", "equal"] | float | None = "auto",
    autolim: bool = True,
    *,
    # Extracted from `**style_kwds`
    norm: Normalize | None = None,
    alpha: float = 1,
    facecolor: _ColorOrColors | None = None,
    edgecolor: _ColorOrColors | None = None,
    linewidth: float = ...,
    label: str = "NaN",
    **style_kwds,
) -> Axes:
    """
    Plot a GeoDataFrame.

    Generate a plot of a GeoDataFrame with matplotlib.  If a
    column is specified, the plot coloring will be based on values
    in that column.

    Parameters
    ----------
    column : str, np.array, pd.Series, pd.Index (default None)
        The name of the dataframe column, np.array, pd.Series, or pd.Index
        to be plotted. If np.array, pd.Series, or pd.Index are used then it
        must have same length as dataframe. Values are used to color the plot.
        Ignored if `color` is also set.
    kind: str
        The kind of plots to produce. The default is to create a map ("geo").
        Other supported kinds of plots from pandas:

        - 'line' : line plot
        - 'bar' : vertical bar plot
        - 'barh' : horizontal bar plot
        - 'hist' : histogram
        - 'box' : BoxPlot
        - 'kde' : Kernel Density Estimation plot
        - 'density' : same as 'kde'
        - 'area' : area plot
        - 'pie' : pie plot
        - 'scatter' : scatter plot
        - 'hexbin' : hexbin plot.
    cmap : str (default None)
        The name of a colormap recognized by matplotlib.
    color : str, np.array, pd.Series (default None)
        If specified, all objects will be colored uniformly.
    ax : matplotlib.pyplot.Artist (default None)
        axes on which to draw the plot
    cax : matplotlib.pyplot Artist (default None)
        axes on which to draw the legend in case of color map.
    categorical : bool (default False)
        If False, cmap will reflect numerical values of the
        column being plotted.  For non-numerical columns, this
        will be set to True.
    legend : bool (default False)
        Plot a legend. Ignored if no `column` is given, or if `color` is given.
    scheme : str (default None)
        Name of a choropleth classification scheme (requires mapclassify).
        A mapclassify.MapClassifier object will be used
        under the hood. Supported are all schemes provided by mapclassify (e.g.
        'BoxPlot', 'EqualInterval', 'FisherJenks', 'FisherJenksSampled',
        'HeadTailBreaks', 'JenksCaspall', 'JenksCaspallForced',
        'JenksCaspallSampled', 'MaxP', 'MaximumBreaks',
        'NaturalBreaks', 'Quantiles', 'Percentiles', 'StdMean',
        'UserDefined'). Arguments can be passed in classification_kwds.
    k : int (default 5)
        Number of classes (ignored if scheme is None)
    vmin : None or float (default None)
        Minimum value of cmap. If None, the minimum data value
        in the column to be plotted is used.
    vmax : None or float (default None)
        Maximum value of cmap. If None, the maximum data value
        in the column to be plotted is used.
    markersize : str or float or sequence (default None)
        Only applies to point geometries within a frame.
        If a str, will use the values in the column of the frame specified
        by markersize to set the size of markers. Otherwise can be a value
        to apply to all points, or a sequence of the same length as the
        number of points.
    figsize : tuple of integers (default None)
        Size of the resulting matplotlib.figure.Figure. If the argument
        axes is given explicitly, figsize is ignored.
    legend_kwds : dict (default None)
        Keyword arguments to pass to :func:`matplotlib.pyplot.legend` or
        :func:`matplotlib.pyplot.colorbar`.
        Additional accepted keywords when `scheme` is specified:

        fmt : string
            A formatting specification for the bin edges of the classes in the
            legend. For example, to have no decimals: ``{"fmt": "{:.0f}"}``.
        labels : list-like
            A list of legend labels to override the auto-generated labels.
            Needs to have the same number of elements as the number of
            classes (`k`).
        interval : boolean (default False)
            An option to control brackets from mapclassify legend.
            If True, open/closed interval brackets are shown in the legend.
    categories : list-like
        Ordered list-like object of categories to be used for categorical plot.
    classification_kwds : dict (default None)
        Keyword arguments to pass to mapclassify
    missing_kwds : dict (default None)
        Keyword arguments specifying color options (as style_kwds)
        to be passed on to geometries with missing values in addition to
        or overwriting other style kwds. If None, geometries with missing
        values are not plotted.
    aspect : 'auto', 'equal', None or float (default 'auto')
        Set aspect of axis. If 'auto', the default aspect for map plots is 'equal'; if
        however data are not projected (coordinates are long/lat), the aspect is by
        default set to 1/cos(df_y * pi/180) with df_y the y coordinate of the middle of
        the GeoDataFrame (the mean of the y range of bounding box) so that a long/lat
        square appears square in the middle of the plot. This implies an
        Equirectangular projection. If None, the aspect of `ax` won't be changed. It can
        also be set manually (float) as the ratio of y-unit to x-unit.
    autolim : bool (default True)
        Update axes data limits to contain the new geometries.
    **style_kwds : dict
        Style options to be passed on to the actual plot function, such
        as ``edgecolor``, ``facecolor``, ``linewidth``, ``markersize``,
        ``alpha``.

    Returns
    -------
    ax : matplotlib axes instance

    Examples
    --------
    >>> import geodatasets
    >>> df = geopandas.read_file(geodatasets.get_path("nybb"))
    >>> df.head()  # doctest: +SKIP
       BoroCode  ...                                           geometry
    0         5  ...  MULTIPOLYGON (((970217.022 145643.332, 970227....
    1         4  ...  MULTIPOLYGON (((1029606.077 156073.814, 102957...
    2         3  ...  MULTIPOLYGON (((1021176.479 151374.797, 102100...
    3         1  ...  MULTIPOLYGON (((981219.056 188655.316, 980940....
    4         2  ...  MULTIPOLYGON (((1012821.806 229228.265, 101278...

    >>> df.plot("BoroName", cmap="Set1")  # doctest: +SKIP

    See the User Guide page :doc:`../../user_guide/mapping` for details.

    """

# IMPORTANT: keep roughly in sync with `plot_dataframe`
class GeoplotAccessor(PlotAccessor):
    """
    Plot a GeoDataFrame.

    Generate a plot of a GeoDataFrame with matplotlib.  If a
    column is specified, the plot coloring will be based on values
    in that column.

    Parameters
    ----------
    column : str, np.array, pd.Series, pd.Index (default None)
        The name of the dataframe column, np.array, pd.Series, or pd.Index
        to be plotted. If np.array, pd.Series, or pd.Index are used then it
        must have same length as dataframe. Values are used to color the plot.
        Ignored if `color` is also set.
    kind: str
        The kind of plots to produce. The default is to create a map ("geo").
        Other supported kinds of plots from pandas:

        - 'line' : line plot
        - 'bar' : vertical bar plot
        - 'barh' : horizontal bar plot
        - 'hist' : histogram
        - 'box' : BoxPlot
        - 'kde' : Kernel Density Estimation plot
        - 'density' : same as 'kde'
        - 'area' : area plot
        - 'pie' : pie plot
        - 'scatter' : scatter plot
        - 'hexbin' : hexbin plot.
    cmap : str (default None)
        The name of a colormap recognized by matplotlib.
    color : str, np.array, pd.Series (default None)
        If specified, all objects will be colored uniformly.
    ax : matplotlib.pyplot.Artist (default None)
        axes on which to draw the plot
    cax : matplotlib.pyplot Artist (default None)
        axes on which to draw the legend in case of color map.
    categorical : bool (default False)
        If False, cmap will reflect numerical values of the
        column being plotted.  For non-numerical columns, this
        will be set to True.
    legend : bool (default False)
        Plot a legend. Ignored if no `column` is given, or if `color` is given.
    scheme : str (default None)
        Name of a choropleth classification scheme (requires mapclassify).
        A mapclassify.MapClassifier object will be used
        under the hood. Supported are all schemes provided by mapclassify (e.g.
        'BoxPlot', 'EqualInterval', 'FisherJenks', 'FisherJenksSampled',
        'HeadTailBreaks', 'JenksCaspall', 'JenksCaspallForced',
        'JenksCaspallSampled', 'MaxP', 'MaximumBreaks',
        'NaturalBreaks', 'Quantiles', 'Percentiles', 'StdMean',
        'UserDefined'). Arguments can be passed in classification_kwds.
    k : int (default 5)
        Number of classes (ignored if scheme is None)
    vmin : None or float (default None)
        Minimum value of cmap. If None, the minimum data value
        in the column to be plotted is used.
    vmax : None or float (default None)
        Maximum value of cmap. If None, the maximum data value
        in the column to be plotted is used.
    markersize : str or float or sequence (default None)
        Only applies to point geometries within a frame.
        If a str, will use the values in the column of the frame specified
        by markersize to set the size of markers. Otherwise can be a value
        to apply to all points, or a sequence of the same length as the
        number of points.
    figsize : tuple of integers (default None)
        Size of the resulting matplotlib.figure.Figure. If the argument
        axes is given explicitly, figsize is ignored.
    legend_kwds : dict (default None)
        Keyword arguments to pass to :func:`matplotlib.pyplot.legend` or
        :func:`matplotlib.pyplot.colorbar`.
        Additional accepted keywords when `scheme` is specified:

        fmt : string
            A formatting specification for the bin edges of the classes in the
            legend. For example, to have no decimals: ``{"fmt": "{:.0f}"}``.
        labels : list-like
            A list of legend labels to override the auto-generated labels.
            Needs to have the same number of elements as the number of
            classes (`k`).
        interval : boolean (default False)
            An option to control brackets from mapclassify legend.
            If True, open/closed interval brackets are shown in the legend.
    categories : list-like
        Ordered list-like object of categories to be used for categorical plot.
    classification_kwds : dict (default None)
        Keyword arguments to pass to mapclassify
    missing_kwds : dict (default None)
        Keyword arguments specifying color options (as style_kwds)
        to be passed on to geometries with missing values in addition to
        or overwriting other style kwds. If None, geometries with missing
        values are not plotted.
    aspect : 'auto', 'equal', None or float (default 'auto')
        Set aspect of axis. If 'auto', the default aspect for map plots is 'equal'; if
        however data are not projected (coordinates are long/lat), the aspect is by
        default set to 1/cos(df_y * pi/180) with df_y the y coordinate of the middle of
        the GeoDataFrame (the mean of the y range of bounding box) so that a long/lat
        square appears square in the middle of the plot. This implies an
        Equirectangular projection. If None, the aspect of `ax` won't be changed. It can
        also be set manually (float) as the ratio of y-unit to x-unit.
    autolim : bool (default True)
        Update axes data limits to contain the new geometries.
    **style_kwds : dict
        Style options to be passed on to the actual plot function, such
        as ``edgecolor``, ``facecolor``, ``linewidth``, ``markersize``,
        ``alpha``.

    Returns
    -------
    ax : matplotlib axes instance

    Examples
    --------
    >>> import geodatasets
    >>> df = geopandas.read_file(geodatasets.get_path("nybb"))
    >>> df.head()  # doctest: +SKIP
       BoroCode  ...                                           geometry
    0         5  ...  MULTIPOLYGON (((970217.022 145643.332, 970227....
    1         4  ...  MULTIPOLYGON (((1029606.077 156073.814, 102957...
    2         3  ...  MULTIPOLYGON (((1021176.479 151374.797, 102100...
    3         1  ...  MULTIPOLYGON (((981219.056 188655.316, 980940....
    4         2  ...  MULTIPOLYGON (((1012821.806 229228.265, 101278...

    >>> df.plot("BoroName", cmap="Set1")  # doctest: +SKIP

    See the User Guide page :doc:`../../user_guide/mapping` for details.

    """

    # The first 3 overloads of calls are from pandas, the last overload is geopandas specific
    @overload  # type: ignore[override]
    def __call__(
        self,
        x: Hashable = ...,
        y: Hashable | Sequence[Hashable] = ...,
        *,
        kind: Literal["line", "bar", "barh", "hist", "box", "kde", "density", "area", "pie", "scatter", "hexbin"],
        ax: Axes | None = None,
        subplots: Literal[False] = False,
        sharex: bool | None = None,
        sharey: bool | None = None,
        layout: tuple[int, int] | None = None,
        figsize: tuple[float, float] | None = None,
        use_index: bool = True,
        title: str | None = None,
        grid: bool | None = None,
        legend: bool | Literal["reverse"] = True,
        style: str | Sequence[str] | Mapping[Incomplete, str] | None = None,
        logx: bool | Literal["sym"] = False,
        logy: bool | Literal["sym"] = False,
        loglog: bool | Literal["sym"] = False,
        xticks: Sequence[float] | None = None,
        yticks: Sequence[float] | None = None,
        xlim: tuple[float, float] | list[float] | None = None,
        ylim: tuple[float, float] | list[float] | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        rot: float | None = None,
        fontsize: float | None = None,
        cmap: str | Colormap | None = None,  # also accepts `colormap` but plot_dataframe uses `cmap`
        colorbar: bool | None = None,
        position: float = 0.5,
        table: bool | pd.Series[Incomplete] | pd.DataFrame = False,
        yerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        xerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        stacked: bool = ...,  # default value depends on kind
        secondary_y: bool | Sequence[Hashable] = False,
        mark_right: bool = True,
        include_bool: bool = False,
        backend: str | None = None,
        **kwargs,
    ) -> Axes: ...
    @overload
    def __call__(
        self,
        x: Hashable = ...,
        y: Hashable | Sequence[Hashable] = ...,
        *,
        kind: Literal["line", "bar", "barh", "hist", "kde", "density", "area", "pie", "scatter", "hexbin"],
        ax: Sequence[Axes] | None = None,
        subplots: Literal[True] | Iterable[Iterable[Hashable]],
        sharex: bool | None = None,
        sharey: bool | None = None,
        layout: tuple[int, int] | None = None,
        figsize: tuple[float, float] | None = None,
        use_index: bool = True,
        title: str | Collection[str] | None = None,
        grid: bool | None = None,
        legend: bool | Literal["reverse"] = True,
        style: str | Sequence[str] | Mapping[Incomplete, str] | None = None,
        logx: bool | Literal["sym"] = False,
        logy: bool | Literal["sym"] = False,
        loglog: bool | Literal["sym"] = False,
        xticks: Sequence[float] | None = None,
        yticks: Sequence[float] | None = None,
        xlim: tuple[float, float] | list[float] | None = None,
        ylim: tuple[float, float] | list[float] | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        rot: float | None = None,
        fontsize: float | None = None,
        cmap: str | Colormap | None = None,  # also accepts `colormap` but plot_dataframe uses `cmap`
        colorbar: bool | None = None,
        position: float = 0.5,
        table: bool | pd.Series[Incomplete] | pd.DataFrame = False,
        yerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        xerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        stacked: bool = ...,  # default value depends on kind
        secondary_y: bool | Sequence[Hashable] = False,
        mark_right: bool = True,
        include_bool: bool = False,
        backend: str | None = None,
        **kwargs,
    ) -> NDArray[np.object_]: ...  # should be NDArray[Axes] but it is not supported
    @overload
    def __call__(
        self,
        x: Hashable = ...,
        y: Hashable | Sequence[Hashable] = ...,
        *,
        kind: Literal["box"],
        ax: Sequence[Axes] | None = None,
        subplots: Literal[True] | Iterable[Iterable[Hashable]],
        sharex: bool | None = None,
        sharey: bool | None = None,
        layout: tuple[int, int] | None = None,
        figsize: tuple[float, float] | None = None,
        use_index: bool = True,
        title: str | Collection[str] | None = None,
        grid: bool | None = None,
        legend: bool | Literal["reverse"] = True,
        style: str | Sequence[str] | Mapping[Incomplete, str] | None = None,
        logx: bool | Literal["sym"] = False,
        logy: bool | Literal["sym"] = False,
        loglog: bool | Literal["sym"] = False,
        xticks: Sequence[float] | None = None,
        yticks: Sequence[float] | None = None,
        xlim: tuple[float, float] | list[float] | None = None,
        ylim: tuple[float, float] | list[float] | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        rot: float | None = None,
        fontsize: float | None = None,
        cmap: str | Colormap | None = None,  # also accepts `colormap` but plot_dataframe uses `cmap`
        colorbar: bool | None = None,
        position: float = 0.5,
        table: bool | pd.Series[Incomplete] | pd.DataFrame = False,
        yerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        xerr: pd.DataFrame | pd.Series[float] | ArrayLike | Mapping[Incomplete, ArrayLike] | str = ...,
        stacked: bool = ...,  # default value depends on kind
        secondary_y: bool | Sequence[Hashable] = False,
        mark_right: bool = True,
        include_bool: bool = False,
        backend: str | None = None,
        **kwargs,
    ) -> pd.Series[Axes]: ...  # type: ignore[type-var] # pyright: ignore[reportInvalidTypeArguments]
    @overload
    def __call__(
        self,
        column: Hashable | pd.Series | pd.Index | NDArray | None = None,
        cmap: str | Colormap | None = None,
        color: _ColorOrColors | None = None,
        ax: Axes | None = None,
        cax: Axes | None = None,
        categorical: bool = False,
        legend: bool = False,
        scheme: str | None = None,
        k: int = 5,
        vmin: float | None = None,
        vmax: float | None = None,
        markersize: str | float | Iterable[float] | ArrayLike | None = None,
        figsize: tuple[float, float] | None = None,
        legend_kwds: dict[str, Incomplete] | None = None,
        categories: Iterable[Hashable] | None = None,
        classification_kwds: dict[str, Incomplete] | None = None,
        missing_kwds: dict[str, Incomplete] | None = None,
        aspect: Literal["auto", "equal"] | float | None = "auto",
        *,
        kind: Literal["geo"] = "geo",
        # Extracted from `**style_kwds`
        norm: Normalize | None = None,
        alpha: float = 1,
        facecolor: _ColorOrColors | None = None,
        edgecolor: _ColorOrColors | None = None,
        linewidth: float = ...,
        label: str = "NaN",
        **style_kwds,
    ) -> Axes: ...
    def geo(
        self,
        column: Hashable | pd.Series | pd.Index | NDArray | None = None,
        cmap: str | Colormap | None = None,
        color: _ColorOrColors | None = None,
        ax: Axes | None = None,
        cax: Axes | None = None,
        categorical: bool = False,
        legend: bool = False,
        scheme: str | None = None,
        k: int = 5,
        vmin: float | None = None,
        vmax: float | None = None,
        markersize: str | float | Iterable[float] | ArrayLike | None = None,
        figsize: tuple[float, float] | None = None,
        legend_kwds: dict[str, Incomplete] | None = None,
        categories: Iterable[Hashable] | None = None,
        classification_kwds: dict[str, Incomplete] | None = None,
        missing_kwds: dict[str, Incomplete] | None = None,
        aspect: Literal["auto", "equal"] | float | None = "auto",
        *,
        # Extracted from `**style_kwds`
        norm: Normalize | None = None,
        alpha: float = 1,
        facecolor: _ColorOrColors | None = None,
        edgecolor: _ColorOrColors | None = None,
        linewidth: float = ...,
        label: str = "NaN",
        **style_kwds,
    ) -> Axes: ...
