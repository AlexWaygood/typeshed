from collections.abc import Callable, Hashable, MutableMapping, Sequence
from typing import Any

import branca  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
import folium  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
import pandas as pd
import xyzservices  # type: ignore[import-not-found] # pyright: ignore[reportMissingImports]
from matplotlib.colors import Colormap  # type: ignore[import-not-found]
from numpy.typing import ArrayLike, NDArray

from .geodataframe import GeoDataFrame
from .geoseries import GeoSeries

def _explore(
    df: GeoDataFrame,
    column: Hashable | NDArray[Any] | pd.Series[Any] | None = None,  # Accepts "any" array or series
    cmap: str | Colormap | branca.colormap.ColorMap | Sequence[str] | Callable[[Any], str] | None = None,  # accepts "any" object
    color: str | ArrayLike | None = None,
    m: folium.Map | None = None,
    tiles: str | folium.TileLayer | xyzservices.TileProvider | None = "OpenStreetMap",
    attr: str | None = None,
    tooltip: bool = True,
    popup: bool = False,
    highlight: bool = True,
    categorical: bool = False,
    legend: bool = True,
    scheme: str | None = None,
    k: int = 5,
    vmin: float | None = None,
    vmax: float | None = None,
    width: float | str = "100%",
    height: float | str = "100%",
    categories: Sequence[Any] | NDArray[Any] | pd.Series[Any] | pd.Index[Any] | None = None,  # categories can have "any" type
    classification_kwds: MutableMapping[str, Any] | None = None,
    control_scale: bool = True,
    marker_type: str | folium.Marker | None = None,
    # The following kwds will never be typed more precisely than "Any"
    marker_kwds: MutableMapping[str, Any] = {},
    style_kwds: MutableMapping[str, Any] = {},
    highlight_kwds: MutableMapping[str, Any] = {},
    missing_kwds: MutableMapping[str, Any] = {},
    tooltip_kwds: MutableMapping[str, Any] = {},
    popup_kwds: MutableMapping[str, Any] = {},
    legend_kwds: MutableMapping[str, Any] = {},
    map_kwds: MutableMapping[str, Any] = {},
    **kwargs,
) -> folium.Map:
    """Explore data in interactive map based on GeoPandas and folium/leaflet.js.

    Generate an interactive leaflet map based on :class:`~geopandas.GeoDataFrame`

    Parameters
    ----------
    column : str, np.array, pd.Series (default None)
        The name of the dataframe column, :class:`numpy.array`,
        or :class:`pandas.Series` to be plotted. If :class:`numpy.array` or
        :class:`pandas.Series` are used then it must have same length as dataframe.
    cmap : str, matplotlib.Colormap, branca.colormap or function (default None)
        The name of a colormap recognized by ``matplotlib``, a list-like of colors,
        :class:`matplotlib.colors.Colormap`, a :class:`branca.colormap.ColorMap` or
        function that returns a named color or hex based on the column
        value, e.g.::

            def my_colormap(value):  # scalar value defined in 'column'
                if value > 1:
                    return "green"
                return "red"

    color : str, array-like (default None)
        Named color or a list-like of colors (named or hex).
    m : folium.Map (default None)
        Existing map instance on which to draw the plot.
    tiles : str, xyzservices.TileProvider (default 'OpenStreetMap Mapnik')
        Map tileset to use. Can choose from the list supported by folium, query a
        :class:`xyzservices.TileProvider` by a name from ``xyzservices.providers``,
        pass :class:`xyzservices.TileProvider` object or pass custom XYZ URL.
        The current list of built-in providers (when ``xyzservices`` is not available):

        ``["OpenStreetMap", "CartoDB positron", “CartoDB dark_matter"]``

        You can pass a custom tileset to Folium by passing a Leaflet-style URL
        to the tiles parameter: ``http://{s}.yourtiles.com/{z}/{x}/{y}.png``.
        Be sure to check their terms and conditions and to provide attribution with
        the ``attr`` keyword.
    attr : str (default None)
        Map tile attribution; only required if passing custom tile URL.
    tooltip : bool, str, int, list (default True)
        Display GeoDataFrame attributes when hovering over the object.
        ``True`` includes all columns. ``False`` removes tooltip. Pass string or list of
        strings to specify a column(s). Integer specifies first n columns to be
        included. Defaults to ``True``.
    popup : bool, str, int, list (default False)
        Input GeoDataFrame attributes for object displayed when clicking.
        ``True`` includes all columns. ``False`` removes popup. Pass string or list of
        strings to specify a column(s). Integer specifies first n columns to be
        included. Defaults to ``False``.
    highlight : bool (default True)
        Enable highlight functionality when hovering over a geometry.
    categorical : bool (default False)
        If ``False``, ``cmap`` will reflect numerical values of the
        column being plotted. For non-numerical columns, this
        will be set to True.
    legend : bool (default True)
        Plot a legend in choropleth plots.
        Ignored if no ``column`` is given.
    scheme : str (default None)
        Name of a choropleth classification scheme (requires ``mapclassify`` >= 2.4.0).
        A :func:`mapclassify.classify` will be used
        under the hood. Supported are all schemes provided by ``mapclassify`` (e.g.
        ``'BoxPlot'``, ``'EqualInterval'``, ``'FisherJenks'``, ``'FisherJenksSampled'``,
        ``'HeadTailBreaks'``, ``'JenksCaspall'``, ``'JenksCaspallForced'``,
        ``'JenksCaspallSampled'``, ``'MaxP'``, ``'MaximumBreaks'``,
        ``'NaturalBreaks'``, ``'Quantiles'``, ``'Percentiles'``, ``'StdMean'``,
        ``'UserDefined'``). Arguments can be passed in ``classification_kwds``.
    k : int (default 5)
        Number of classes
    vmin : None or float (default None)
        Minimum value of ``cmap``. If ``None``, the minimum data value
        in the column to be plotted is used.
    vmax : None or float (default None)
        Maximum value of ``cmap``. If ``None``, the maximum data value
        in the column to be plotted is used.
    width : pixel int or percentage string (default: '100%')
        Width of the folium :class:`~folium.folium.Map`. If the argument
        m is given explicitly, width is ignored.
    height : pixel int or percentage string (default: '100%')
        Height of the folium :class:`~folium.folium.Map`. If the argument
        m is given explicitly, height is ignored.
    categories : list-like
        Ordered list-like object of categories to be used for categorical plot.
    classification_kwds : dict (default None)
        Keyword arguments to pass to mapclassify
    control_scale : bool, (default True)
        Whether to add a control scale on the map.
    marker_type : str, folium.Circle, folium.CircleMarker, folium.Marker (default None)
        Allowed string options are ('marker', 'circle', 'circle_marker'). Defaults to
        folium.CircleMarker.
    marker_kwds: dict (default {})
        Additional keywords to be passed to the selected ``marker_type``, e.g.:

        radius : float (default 2 for ``circle_marker`` and 50 for ``circle``))
            Radius of the circle, in meters (for ``circle``) or pixels
            (for ``circle_marker``).
        fill : bool (default True)
            Whether to fill the ``circle`` or ``circle_marker`` with color.
        icon : folium.map.Icon
            the :class:`folium.map.Icon` object to use to render the marker.
        draggable : bool (default False)
            Set to True to be able to drag the marker around the map.

    style_kwds : dict (default {})
        Additional style to be passed to folium ``style_function``:

        stroke : bool (default True)
            Whether to draw stroke along the path. Set it to ``False`` to
            disable borders on polygons or circles.
        color : str
            Stroke color
        weight : int
            Stroke width in pixels
        opacity : float (default 1.0)
            Stroke opacity
        fill : boolean (default True)
            Whether to fill the path with color. Set it to ``False`` to
            disable filling on polygons or circles.
        fillColor : str
            Fill color. Defaults to the value of the color option
        fillOpacity : float (default 0.5)
            Fill opacity.
        style_function : callable
            Function mapping a GeoJson Feature to a style ``dict``.

            * Style properties :func:`folium.vector_layers.path_options`
            * GeoJson features :class:`GeoDataFrame.__geo_interface__`

            e.g.::

                lambda x: {"color":"red" if x["properties"]["gdp_md_est"]<10**6
                                             else "blue"}

        Plus all supported by :func:`folium.vector_layers.path_options`. See the
        documentation of :class:`folium.features.GeoJson` for details.

    highlight_kwds : dict (default {})
        Style to be passed to folium highlight_function. Uses the same keywords
        as ``style_kwds``. When empty, defaults to ``{"fillOpacity": 0.75}``.
    missing_kwds : dict (default {})
        Additional style for missing values:

        color : str
            Color of missing values. Defaults to ``None``, which uses Folium's default.
        label : str (default "NaN")
            Legend entry for missing values.
    tooltip_kwds : dict (default {})
        Additional keywords to be passed to :class:`folium.features.GeoJsonTooltip`,
        e.g. ``aliases``, ``labels``, or ``sticky``.
    popup_kwds : dict (default {})
        Additional keywords to be passed to :class:`folium.features.GeoJsonPopup`,
        e.g. ``aliases`` or ``labels``.
    legend_kwds : dict (default {})
        Additional keywords to be passed to the legend.

        Currently supported customisation:

        caption : string
            Custom caption of the legend. Defaults to the column name.

        Additional accepted keywords when ``scheme`` is specified:

        colorbar : bool (default True)
            An option to control the style of the legend. If True, continuous
            colorbar will be used. If False, categorical legend will be used for bins.
        scale : bool (default True)
            Scale bins along the colorbar axis according to the bin edges (True)
            or use the equal length for each bin (False)
        fmt : string (default "{:.2f}")
            A formatting specification for the bin edges of the classes in the
            legend. For example, to have no decimals: ``{"fmt": "{:.0f}"}``. Applies
            if ``colorbar=False``.
        labels : list-like
            A list of legend labels to override the auto-generated labels.
            Needs to have the same number of elements as the number of
            classes (`k`). Applies if ``colorbar=False``.
        interval : boolean (default False)
            An option to control brackets from mapclassify legend.
            If True, open/closed interval brackets are shown in the legend.
            Applies if ``colorbar=False``.
        max_labels : int, default 10
            Maximum number of colorbar tick labels (requires branca>=0.5.0)
    map_kwds : dict (default {})
        Additional keywords to be passed to folium :class:`~folium.folium.Map`,
        e.g. ``dragging``, or ``scrollWheelZoom``.


    **kwargs : dict
        Additional options to be passed on to the folium object.

    Returns
    -------
    m : folium.folium.Map
        folium :class:`~folium.folium.Map` instance

    Examples
    --------
    >>> import geodatasets
    >>> df = geopandas.read_file(
    ...     geodatasets.get_path("geoda.chicago_health")
    ... )
    >>> df.head(2)  # doctest: +SKIP
       ComAreaID  ...                                           geometry
    0         35  ...  POLYGON ((-87.60914 41.84469, -87.60915 41.844...
    1         36  ...  POLYGON ((-87.59215 41.81693, -87.59231 41.816...

    [2 rows x 87 columns]

    >>> df.explore("Pop2012", cmap="Blues")  # doctest: +SKIP
    """

def _explore_geoseries(
    s: GeoSeries,
    color: str | ArrayLike | None = None,
    m: folium.Map | None = None,
    tiles: str | folium.TileLayer | xyzservices.TileProvider | None = "OpenStreetMap",
    attr: str | None = None,
    highlight: bool = True,
    width: float | str = "100%",
    height: float | str = "100%",
    control_scale: bool = True,
    marker_type: str | folium.Marker | None = None,
    # The following kwds will never be typed more precisely than "Any"
    marker_kwds: MutableMapping[str, Any] = {},
    style_kwds: MutableMapping[str, Any] = {},
    highlight_kwds: MutableMapping[str, Any] = {},
    map_kwds: MutableMapping[str, Any] = {},
    **kwargs,
) -> folium.Map:
    """Interactive map based on GeoPandas and folium/leaflet.js.

    Generate an interactive leaflet map based on :class:`~geopandas.GeoSeries`

    Parameters
    ----------
    color : str, array-like (default None)
        Named color or a list-like of colors (named or hex).
    m : folium.Map (default None)
        Existing map instance on which to draw the plot.
    tiles : str, xyzservices.TileProvider (default 'OpenStreetMap Mapnik')
        Map tileset to use. Can choose from the list supported by folium, query a
        :class:`xyzservices.TileProvider` by a name from ``xyzservices.providers``,
        pass :class:`xyzservices.TileProvider` object or pass custom XYZ URL.
        The current list of built-in providers (when ``xyzservices`` is not available):

        ``["OpenStreetMap", "CartoDB positron", “CartoDB dark_matter"]``

        You can pass a custom tileset to Folium by passing a Leaflet-style URL
        to the tiles parameter: ``http://{s}.yourtiles.com/{z}/{x}/{y}.png``.
        Be sure to check their terms and conditions and to provide attribution with
        the ``attr`` keyword.
    attr : str (default None)
        Map tile attribution; only required if passing custom tile URL.
    highlight : bool (default True)
        Enable highlight functionality when hovering over a geometry.
    width : pixel int or percentage string (default: '100%')
        Width of the folium :class:`~folium.folium.Map`. If the argument
        m is given explicitly, width is ignored.
    height : pixel int or percentage string (default: '100%')
        Height of the folium :class:`~folium.folium.Map`. If the argument
        m is given explicitly, height is ignored.
    control_scale : bool, (default True)
        Whether to add a control scale on the map.
    marker_type : str, folium.Circle, folium.CircleMarker, folium.Marker (default None)
        Allowed string options are ('marker', 'circle', 'circle_marker'). Defaults to
        folium.Marker.
    marker_kwds: dict (default {})
        Additional keywords to be passed to the selected ``marker_type``, e.g.:

        radius : float
            Radius of the circle, in meters (for ``'circle'``) or pixels
            (for ``circle_marker``).
        icon : folium.map.Icon
            the :class:`folium.map.Icon` object to use to render the marker.
        draggable : bool (default False)
            Set to True to be able to drag the marker around the map.

    style_kwds : dict (default {})
        Additional style to be passed to folium ``style_function``:

        stroke : bool (default True)
            Whether to draw stroke along the path. Set it to ``False`` to
            disable borders on polygons or circles.
        color : str
            Stroke color
        weight : int
            Stroke width in pixels
        opacity : float (default 1.0)
            Stroke opacity
        fill : boolean (default True)
            Whether to fill the path with color. Set it to ``False`` to
            disable filling on polygons or circles.
        fillColor : str
            Fill color. Defaults to the value of the color option
        fillOpacity : float (default 0.5)
            Fill opacity.
        style_function : callable
            Function mapping a GeoJson Feature to a style ``dict``.

            * Style properties :func:`folium.vector_layers.path_options`
            * GeoJson features :class:`GeoSeries.__geo_interface__`

            e.g.::

                lambda x: {"color":"red" if x["properties"]["gdp_md_est"]<10**6
                                             else "blue"}


        Plus all supported by :func:`folium.vector_layers.path_options`. See the
        documentation of :class:`folium.features.GeoJson` for details.

    highlight_kwds : dict (default {})
        Style to be passed to folium highlight_function. Uses the same keywords
        as ``style_kwds``. When empty, defaults to ``{"fillOpacity": 0.75}``.
    map_kwds : dict (default {})
        Additional keywords to be passed to folium :class:`~folium.folium.Map`,
        e.g. ``dragging``, or ``scrollWheelZoom``.

    **kwargs : dict
        Additional options to be passed on to the folium.

    Returns
    -------
    m : folium.folium.Map
        folium :class:`~folium.folium.Map` instance

    """
