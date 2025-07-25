"""Plot single geometries using Matplotlib.

Note: this module is experimental, and mainly targeting (interactive)
exploration, debugging and illustration purposes.

"""

from typing import Any, Literal, overload

from matplotlib.axes import Axes  # type: ignore[import-not-found]
from matplotlib.lines import Line2D  # type: ignore[import-not-found]
from matplotlib.patches import PathPatch  # type: ignore[import-not-found]
from matplotlib.typing import ColorType  # type: ignore[import-not-found]

from .geometry import LinearRing, LineString, MultiLineString, MultiPolygon, Polygon
from .lib import Geometry

def patch_from_polygon(polygon: Polygon | MultiPolygon, **kwargs: Any) -> PathPatch:
    """Get a Matplotlib patch from a (Multi)Polygon.

    Note: this function is experimental, and mainly targeting (interactive)
    exploration, debugging and illustration purposes.

    Parameters
    ----------
    polygon : shapely.Polygon or shapely.MultiPolygon
        The polygon to convert to a Matplotlib Patch.
    **kwargs
        Additional keyword arguments passed to the matplotlib Patch.

    Returns
    -------
    Matplotlib artist (PathPatch)

    """

@overload
def plot_polygon(
    polygon: Polygon | MultiPolygon,
    ax: Axes | None = None,
    add_points: Literal[True] = True,
    color: ColorType | None = None,
    facecolor: ColorType | None = None,
    edgecolor: ColorType | None = None,
    linewidth: float | None = None,
    **kwargs: Any,
) -> tuple[PathPatch, Line2D]:
    """Plot a (Multi)Polygon.

    Note: this function is experimental, and mainly targeting (interactive)
    exploration, debugging and illustration purposes.

    Parameters
    ----------
    polygon : shapely.Polygon or shapely.MultiPolygon
        The polygon to plot.
    ax : matplotlib Axes, default None
        The axes on which to draw the plot. If not specified, will get the
        current active axes or create a new figure.
    add_points : bool, default True
        If True, also plot the coordinates (vertices) as points.
    color : matplotlib color specification
        Color for both the polygon fill (face) and boundary (edge). By default,
        the fill is using an alpha of 0.3. You can specify `facecolor` and
        `edgecolor` separately for greater control.
    facecolor : matplotlib color specification
        Color for the polygon fill.
    edgecolor : matplotlib color specification
        Color for the polygon boundary.
    linewidth : float
        The line width for the polygon boundary.
    **kwargs
        Additional keyword arguments passed to the matplotlib Patch.

    Returns
    -------
    Matplotlib artist (PathPatch), if `add_points` is false.
    A tuple of Matplotlib artists (PathPatch, Line2D), if `add_points` is true.

    """

@overload
def plot_polygon(
    polygon: Polygon | MultiPolygon,
    ax: Axes | None = None,
    *,
    add_points: Literal[False],
    color: ColorType | None = None,
    facecolor: ColorType | None = None,
    edgecolor: ColorType | None = None,
    linewidth: float | None = None,
    **kwargs: Any,
) -> PathPatch: ...
@overload
def plot_polygon(
    polygon: Polygon | MultiPolygon,
    ax: Axes | None,
    add_points: Literal[False],
    color: ColorType | None = None,
    facecolor: ColorType | None = None,
    edgecolor: ColorType | None = None,
    linewidth: float | None = None,
    **kwargs: Any,
) -> PathPatch: ...
@overload
def plot_line(
    line: LineString | LinearRing | MultiLineString,
    ax: Axes | None = None,
    add_points: Literal[True] = True,
    color: ColorType | None = None,
    linewidth: float = 2,
    **kwargs: Any,
) -> tuple[PathPatch, Line2D]:
    """Plot a (Multi)LineString/LinearRing.

    Note: this function is experimental, and mainly targeting (interactive)
    exploration, debugging and illustration purposes.

    Parameters
    ----------
    line : shapely.LineString or shapely.LinearRing
        The line to plot.
    ax : matplotlib Axes, default None
        The axes on which to draw the plot. If not specified, will get the
        current active axes or create a new figure.
    add_points : bool, default True
        If True, also plot the coordinates (vertices) as points.
    color : matplotlib color specification
        Color for the line (edgecolor under the hood) and points.
    linewidth : float, default 2
        The line width for the polygon boundary.
    **kwargs
        Additional keyword arguments passed to the matplotlib Patch.

    Returns
    -------
    Matplotlib artist (PathPatch)

    """

@overload
def plot_line(
    line: LineString | LinearRing | MultiLineString,
    ax: Axes | None = None,
    *,
    add_points: Literal[False],
    color: ColorType | None = None,
    linewidth: float = 2,
    **kwargs: Any,
) -> PathPatch: ...
@overload
def plot_line(
    line: LineString | LinearRing | MultiLineString,
    ax: Axes | None,
    add_points: Literal[False],
    color: ColorType | None = None,
    linewidth: float = 2,
    **kwargs: Any,
) -> PathPatch: ...
def plot_points(
    geom: Geometry, ax: Axes | None = None, color: ColorType | None = None, marker: str = "o", **kwargs: Any
) -> Line2D:
    """Plot a Point/MultiPoint or the vertices of any other geometry type.

    Parameters
    ----------
    geom : shapely.Geometry
        Any shapely Geometry object, from which all vertices are extracted
        and plotted.
    ax : matplotlib Axes, default None
        The axes on which to draw the plot. If not specified, will get the
        current active axes or create a new figure.
    color : matplotlib color specification
        Color for the filled points. You can use `markeredgecolor` and
        `markerfacecolor` to have different edge and fill colors.
    marker : str, default "o"
        The matplotlib marker for the points.
    **kwargs
        Additional keyword arguments passed to matplotlib `plot` (Line2D).

    Returns
    -------
    Matplotlib artist (Line2D)

    """
