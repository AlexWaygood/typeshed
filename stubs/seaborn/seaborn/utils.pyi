"""Utility functions, mostly for internal use."""

import datetime as dt
from _typeshed import Incomplete, SupportsGetItem
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, Literal, SupportsIndex, TypeVar, overload
from typing_extensions import TypeAlias, deprecated

import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.text import Text
from matplotlib.ticker import Locator
from matplotlib.typing import ColorType
from numpy.typing import ArrayLike, NDArray
from pandas import DataFrame

from .axisgrid import Grid

__all__ = [
    "desaturate",
    "saturate",
    "set_hls_values",
    "move_legend",
    "despine",
    "get_dataset_names",
    "get_data_home",
    "load_dataset",
]

_VectorT = TypeVar("_VectorT", bound=SupportsGetItem[Any, Any])

# Type aliases used heavily throughout seaborn
_ErrorBar: TypeAlias = str | tuple[str, float] | Callable[[Iterable[float]], tuple[float, float]]  # noqa: Y047
_Estimator: TypeAlias = str | Callable[..., Incomplete]  # noqa: Y047
_Legend: TypeAlias = Literal["auto", "brief", "full"] | bool  # noqa: Y047
_LogScale: TypeAlias = bool | float | tuple[bool | float, bool | float]  # noqa: Y047
# `palette` requires dict but we use mapping to avoid a very long union because dict is invariant in its value type
_Palette: TypeAlias = str | Sequence[ColorType] | Mapping[Any, ColorType]  # noqa: Y047
_Seed: TypeAlias = int | np.random.Generator | np.random.RandomState  # noqa: Y047
_Scalar: TypeAlias = (
    # numeric
    float
    | complex
    | np.number[Any]
    # categorical
    | bool
    | str
    | bytes
    | None
    # dates
    | dt.date
    | dt.datetime
    | dt.timedelta
    | pd.Timestamp
    | pd.Timedelta
)
_Vector: TypeAlias = Iterable[_Scalar]
_DataSourceWideForm: TypeAlias = (  # noqa: Y047
    # Mapping of keys to "convertible to pd.Series" vectors
    Mapping[Any, _Vector]
    # Sequence of "convertible to pd.Series" vectors
    | Sequence[_Vector]
    # A "convertible to pd.DataFrame" table
    | Mapping[Any, Mapping[Any, _Scalar]]
    | NDArray[Any]
    # Flat "convertible to pd.Series" vector of scalars
    | Sequence[_Scalar]
)

DATASET_SOURCE: str
DATASET_NAMES_URL: str

def ci_to_errsize(cis: ArrayLike, heights: ArrayLike) -> NDArray[np.float64]:
    """Convert intervals to error arguments relative to plot heights.

    Parameters
    ----------
    cis : 2 x n sequence
        sequence of confidence interval limits
    heights : n sequence
        sequence of plot heights

    Returns
    -------
    errsize : 2 x n array
        sequence of error size relative to height values in correct
        format as argument for plt.bar

    """

def desaturate(color: ColorType, prop: float) -> tuple[float, float, float]:
    """Decrease the saturation channel of a color by some percent.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name
    prop : float
        saturation channel of color will be multiplied by this value

    Returns
    -------
    new_color : rgb tuple
        desaturated color code in RGB tuple representation

    """

def saturate(color: ColorType) -> tuple[float, float, float]:
    """Return a fully saturated color with the same hue.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name

    Returns
    -------
    new_color : rgb tuple
        saturated color code in RGB tuple representation

    """

def set_hls_values(
    color: ColorType, h: float | None = None, l: float | None = None, s: float | None = None
) -> tuple[float, float, float]:
    """Independently manipulate the h, l, or s channels of a color.

    Parameters
    ----------
    color : matplotlib color
        hex, rgb-tuple, or html color name
    h, l, s : floats between 0 and 1, or None
        new values for each channel in hls space

    Returns
    -------
    new_color : rgb tuple
        new color code in RGB tuple representation

    """

@deprecated("Function `axlabel` is deprecated and will be removed in a future version")
def axlabel(xlabel: str, ylabel: str, **kwargs: Any) -> None:
    """Grab current axis and label it.

    DEPRECATED: will be removed in a future version.

    """

def remove_na(vector: _VectorT) -> _VectorT:
    """Helper method for removing null values from data vectors.

    Parameters
    ----------
    vector : vector object
        Must implement boolean masking with [] subscript syntax.

    Returns
    -------
    clean_clean : same type as ``vector``
        Vector of data with null values removed. May be a copy or a view.

    """

def get_color_cycle() -> list[str]:
    """Return the list of colors in the current matplotlib color cycle

    Parameters
    ----------
    None

    Returns
    -------
    colors : list
        List of matplotlib colors in the current cycle, or dark gray if
        the current color cycle is empty.
    """

# `despine` should be kept roughly in line with `seaborn.axisgrid.FacetGrid.despine`
def despine(
    fig: Figure | None = None,
    ax: Axes | None = None,
    top: bool = True,
    right: bool = True,
    left: bool = False,
    bottom: bool = False,
    offset: int | Mapping[str, int] | None = None,
    trim: bool = False,
) -> None:
    """Remove the top and right spines from plot(s).

    fig : matplotlib figure, optional
        Figure to despine all axes of, defaults to the current figure.
    ax : matplotlib axes, optional
        Specific axes object to despine. Ignored if fig is provided.
    top, right, left, bottom : boolean, optional
        If True, remove that spine.
    offset : int or dict, optional
        Absolute distance, in points, spines should be moved away
        from the axes (negative values move spines inward). A single value
        applies to all spines; a dict can be used to set offset values per
        side.
    trim : bool, optional
        If True, limit spines to the smallest and largest major tick
        on each non-despined axis.

    Returns
    -------
    None

    """

def move_legend(obj: Grid | Axes | Figure, loc: str | int, **kwargs: Any) -> None:
    """
    Recreate a plot's legend at a new location.

    The name is a slight misnomer. Matplotlib legends do not expose public
    control over their position parameters. So this function creates a new legend,
    copying over the data from the original object, which is then removed.

    Parameters
    ----------
    obj : the object with the plot
        This argument can be either a seaborn or matplotlib object:

        - :class:`seaborn.FacetGrid` or :class:`seaborn.PairGrid`
        - :class:`matplotlib.axes.Axes` or :class:`matplotlib.figure.Figure`

    loc : str or int
        Location argument, as in :meth:`matplotlib.axes.Axes.legend`.

    kwargs
        Other keyword arguments are passed to :meth:`matplotlib.axes.Axes.legend`.

    Examples
    --------

    .. include:: ../docstrings/move_legend.rst

    """

def ci(
    a: float | ArrayLike, which: float | ArrayLike = 95, axis: SupportsIndex | Sequence[SupportsIndex] | None = None
) -> NDArray[np.float64]:
    """Return a percentile range from an array of values."""

def get_dataset_names() -> list[str]:
    """Report available example datasets, useful for reporting issues.

    Requires an internet connection.

    """

def get_data_home(data_home: str | None = None) -> str:
    """Return a path to the cache directory for example datasets.

    This directory is used by :func:`load_dataset`.

    If the ``data_home`` argument is not provided, it will use a directory
    specified by the `SEABORN_DATA` environment variable (if it exists)
    or otherwise default to an OS-appropriate user cache location.

    """

def load_dataset(name: str, cache: bool = True, data_home: str | None = None, **kws: Any) -> DataFrame:
    """Load an example dataset from the online repository (requires internet).

    This function provides quick access to a small number of example datasets
    that are useful for documenting seaborn or generating reproducible examples
    for bug reports. It is not necessary for normal usage.

    Note that some of the datasets have a small amount of preprocessing applied
    to define a proper ordering for categorical variables.

    Use :func:`get_dataset_names` to see a list of available datasets.

    Parameters
    ----------
    name : str
        Name of the dataset (``{name}.csv`` on
        https://github.com/mwaskom/seaborn-data).
    cache : boolean, optional
        If True, try to load from the local cache first, and save to the cache
        if a download is required.
    data_home : string, optional
        The directory in which to cache data; see :func:`get_data_home`.
    kws : keys and values, optional
        Additional keyword arguments are passed to passed through to
        :func:`pandas.read_csv`.

    Returns
    -------
    df : :class:`pandas.DataFrame`
        Tabular data, possibly with some preprocessing applied.

    """

def axis_ticklabels_overlap(labels: Iterable[Text]) -> bool:
    """Return a boolean for whether the list of ticklabels have overlaps.

    Parameters
    ----------
    labels : list of matplotlib ticklabels

    Returns
    -------
    overlap : boolean
        True if any of the labels overlap.

    """

def axes_ticklabels_overlap(ax: Axes) -> tuple[bool, bool]:
    """Return booleans for whether the x and y ticklabels on an Axes overlap.

    Parameters
    ----------
    ax : matplotlib Axes

    Returns
    -------
    x_overlap, y_overlap : booleans
        True when the labels on that axis overlap.

    """

def locator_to_legend_entries(locator: Locator, limits: Iterable[float], dtype) -> tuple[list[Incomplete], list[str]]:
    """Return levels and formatted levels for brief numeric legends."""

@overload
def relative_luminance(color: ColorType) -> float:  # type: ignore[overload-overlap]
    """Calculate the relative luminance of a color according to W3C standards

    Parameters
    ----------
    color : matplotlib color or sequence of matplotlib colors
        Hex code, rgb-tuple, or html color name.

    Returns
    -------
    luminance : float(s) between 0 and 1

    """

@overload
def relative_luminance(color: Sequence[ColorType]) -> NDArray[np.float64]: ...
@overload
def relative_luminance(color: ColorType | Sequence[ColorType] | ArrayLike) -> float | NDArray[np.float64]: ...
def to_utf8(obj: object) -> str:
    """Return a string representing a Python object.

    Strings (i.e. type ``str``) are returned unchanged.

    Byte strings (i.e. type ``bytes``) are returned as UTF-8-decoded strings.

    For other objects, the method ``__str__()`` is called, and the result is
    returned as a string.

    Parameters
    ----------
    obj : object
        Any Python object

    Returns
    -------
    s : str
        UTF-8-decoded string representation of ``obj``

    """

def adjust_legend_subtitles(legend: Legend) -> None:  # not public API
    """
    Make invisible-handle "subtitles" entries look more like titles.

    Note: This function is not part of the public API and may be changed or removed.

    """
