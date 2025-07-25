from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar
from typing_extensions import Self, TypeAlias

from matplotlib.axis import Ticker
from matplotlib.scale import ScaleBase
from matplotlib.ticker import Formatter, Locator
from matplotlib.units import ConversionInterface
from numpy.typing import ArrayLike, NDArray
from pandas import Series
from seaborn._core.typing import Default

TransFuncs: TypeAlias = tuple[Callable[[ArrayLike], ArrayLike], Callable[[ArrayLike], ArrayLike]]
Pipeline: TypeAlias = Sequence[Callable[[Any], Any] | None]

class Scale:
    """Base class for objects that map data values to visual properties."""

    values: tuple[Incomplete, ...] | str | list[Incomplete] | dict[Incomplete, Incomplete] | None
    def __post_init__(self) -> None: ...
    def tick(self) -> Self: ...
    def label(self) -> Self: ...
    def __call__(self, data: Series[Any]) -> ArrayLike: ...

@dataclass
class Boolean(Scale):
    """
    A scale with a discrete domain of True and False values.

    The behavior is similar to the :class:`Nominal` scale, but property
    mappings and legends will use a [True, False] ordering rather than
    a sort using numeric rules. Coordinate variables accomplish this by
    inverting axis limits so as to maintain underlying numeric positioning.
    Input data are cast to boolean values, respecting missing data.

    """

    values: tuple[Incomplete, ...] | list[Incomplete] | dict[Incomplete, Incomplete] | None = None
    def tick(self, locator: Locator | None = None) -> Self: ...
    def label(self, formatter: Formatter | None = None) -> Self: ...

@dataclass
class Nominal(Scale):
    """
    A categorical scale without relative importance / magnitude.
    """

    values: tuple[Incomplete, ...] | str | list[Incomplete] | dict[Incomplete, Incomplete] | None = None
    order: list[Incomplete] | None = None
    def tick(self, locator: Locator | None = None) -> Self:
        """
        Configure the selection of ticks for the scale's axis or legend.

        .. note::
            This API is under construction and will be enhanced over time.
            At the moment, it is probably not very useful.

        Parameters
        ----------
        locator : :class:`matplotlib.ticker.Locator` subclass
            Pre-configured matplotlib locator; other parameters will not be used.

        Returns
        -------
        Copy of self with new tick configuration.

        """

    def label(self, formatter: Formatter | None = None) -> Self:
        """
        Configure the selection of labels for the scale's axis or legend.

        .. note::
            This API is under construction and will be enhanced over time.
            At the moment, it is probably not very useful.

        Parameters
        ----------
        formatter : :class:`matplotlib.ticker.Formatter` subclass
            Pre-configured matplotlib formatter; other parameters will not be used.

        Returns
        -------
        scale
            Copy of self with new tick configuration.

        """

@dataclass
class Ordinal(Scale):
    """Ordinal()"""

@dataclass
class Discrete(Scale):
    """Discrete()"""

@dataclass
class ContinuousBase(Scale):
    """ContinuousBase(values: 'tuple | str | None' = None, norm: 'tuple | None' = None)"""

    values: tuple[Incomplete, ...] | str | None = None
    norm: tuple[Incomplete, ...] | None = None

@dataclass
class Continuous(ContinuousBase):
    """
    A numeric scale supporting norms and functional transforms.
    """

    values: tuple[Incomplete, ...] | str | None = None
    trans: str | TransFuncs | None = None
    def tick(
        self,
        locator: Locator | None = None,
        *,
        at: Sequence[float] | None = None,
        upto: int | None = None,
        count: int | None = None,
        every: float | None = None,
        between: tuple[float, float] | None = None,
        minor: int | None = None,
    ) -> Self:
        """
        Configure the selection of ticks for the scale's axis or legend.

        Parameters
        ----------
        locator : :class:`matplotlib.ticker.Locator` subclass
            Pre-configured matplotlib locator; other parameters will not be used.
        at : sequence of floats
            Place ticks at these specific locations (in data units).
        upto : int
            Choose "nice" locations for ticks, but do not exceed this number.
        count : int
            Choose exactly this number of ticks, bounded by `between` or axis limits.
        every : float
            Choose locations at this interval of separation (in data units).
        between : pair of floats
            Bound upper / lower ticks when using `every` or `count`.
        minor : int
            Number of unlabeled ticks to draw between labeled "major" ticks.

        Returns
        -------
        scale
            Copy of self with new tick configuration.

        """

    def label(
        self,
        formatter: Formatter | None = None,
        *,
        like: str | Callable[[float], str] | None = None,
        base: int | None | Default = ...,
        unit: str | None = None,
    ) -> Self:
        """
        Configure the appearance of tick labels for the scale's axis or legend.

        Parameters
        ----------
        formatter : :class:`matplotlib.ticker.Formatter` subclass
            Pre-configured formatter to use; other parameters will be ignored.
        like : str or callable
            Either a format pattern (e.g., `".2f"`), a format string with fields named
            `x` and/or `pos` (e.g., `"${x:.2f}"`), or a callable with a signature like
            `f(x: float, pos: int) -> str`. In the latter variants, `x` is passed as the
            tick value and `pos` is passed as the tick index.
        base : number
            Use log formatter (with scientific notation) having this value as the base.
            Set to `None` to override the default formatter with a log transform.
        unit : str or (str, str) tuple
            Use  SI prefixes with these units (e.g., with `unit="g"`, a tick value
            of 5000 will appear as `5 kg`). When a tuple, the first element gives the
            separator between the number and unit.

        Returns
        -------
        scale
            Copy of self with new label configuration.

        """

@dataclass
class Temporal(ContinuousBase):
    """
    A scale for date/time data.
    """

    trans: ClassVar[Incomplete]  # not sure it is a classvar but the runtime has no annotation so it is not a dataclass field
    def tick(self, locator: Locator | None = None, *, upto: int | None = None) -> Self:
        """
        Configure the selection of ticks for the scale's axis or legend.

        .. note::
            This API is under construction and will be enhanced over time.

        Parameters
        ----------
        locator : :class:`matplotlib.ticker.Locator` subclass
            Pre-configured matplotlib locator; other parameters will not be used.
        upto : int
            Choose "nice" locations for ticks, but do not exceed this number.

        Returns
        -------
        scale
            Copy of self with new tick configuration.

        """

    def label(self, formatter: Formatter | None = None, *, concise: bool = False) -> Self:
        """
        Configure the appearance of tick labels for the scale's axis or legend.

        .. note::
            This API is under construction and will be enhanced over time.

        Parameters
        ----------
        formatter : :class:`matplotlib.ticker.Formatter` subclass
            Pre-configured formatter to use; other parameters will be ignored.
        concise : bool
            If True, use :class:`matplotlib.dates.ConciseDateFormatter` to make
            the tick labels as compact as possible.

        Returns
        -------
        scale
            Copy of self with new label configuration.

        """

class PseudoAxis:
    """
    Internal class implementing minimal interface equivalent to matplotlib Axis.

    Coordinate variables are typically scaled by attaching the Axis object from
    the figure where the plot will end up. Matplotlib has no similar concept of
    and axis for the other mappable variables (color, etc.), but to simplify the
    code, this object acts like an Axis and can be used to scale other variables.

    """

    axis_name: str
    converter: ConversionInterface | None
    units: Incomplete | None
    scale: ScaleBase
    major: Ticker
    minor: Ticker
    def __init__(self, scale: ScaleBase) -> None: ...
    def set_view_interval(self, vmin: float, vmax: float) -> None: ...
    def get_view_interval(self) -> tuple[float, float]: ...
    def set_data_interval(self, vmin: float, vmax: float) -> None: ...
    def get_data_interval(self) -> tuple[float, float]: ...
    def get_tick_space(self) -> int: ...
    def set_major_locator(self, locator: Locator) -> None: ...
    def set_major_formatter(self, formatter: Formatter) -> None: ...
    def set_minor_locator(self, locator: Locator) -> None: ...
    def set_minor_formatter(self, formatter: Formatter) -> None: ...
    def set_units(self, units) -> None: ...
    def update_units(self, x) -> None:
        """Pass units to the internal converter, potentially updating its mapping."""

    def convert_units(self, x):
        """Return a numeric representation of the input data."""

    def get_scale(self) -> ScaleBase: ...
    def get_majorticklocs(self) -> NDArray[Incomplete]: ...
