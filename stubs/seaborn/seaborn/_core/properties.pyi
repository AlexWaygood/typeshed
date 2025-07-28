from _typeshed import Incomplete
from collections.abc import Callable
from typing import Any
from typing_extensions import TypeAlias

from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
from numpy.typing import ArrayLike
from pandas import Series
from seaborn._core.scales import Scale

RGBTuple: TypeAlias = tuple[float, float, float]
RGBATuple: TypeAlias = tuple[float, float, float, float]
ColorSpec: TypeAlias = RGBTuple | RGBATuple | str
DashPattern: TypeAlias = tuple[float, ...]
DashPatternWithOffset: TypeAlias = tuple[float, DashPattern | None]
MarkerPattern: TypeAlias = float | str | tuple[int, int, float] | list[tuple[float, float]] | Path | MarkerStyle
Mapping: TypeAlias = Callable[[ArrayLike], ArrayLike]

class Property:
    """Base class for visual properties that can be set directly or be data scaling."""

    legend: bool
    normed: bool
    variable: Incomplete
    def __init__(self, variable: str | None = None) -> None:
        """Initialize the property with the name of the corresponding plot variable."""

    def default_scale(self, data: Series[Any]) -> Scale:
        """Given data, initialize appropriate scale class."""

    def infer_scale(self, arg: Any, data: Series[Any]) -> Scale:
        """Given data and a scaling argument, initialize appropriate scale class."""

    def get_mapping(self, scale: Scale, data: Series[Any]) -> Mapping:
        """Return a function that maps from data domain to property range."""

    def standardize(self, val: Any) -> Any:
        """Coerce flexible property value to standardized representation."""

class Coordinate(Property):
    """The position of visual marks with respect to the axes of the plot."""

    legend: bool
    normed: bool

class IntervalProperty(Property):
    """A numeric property where scale range can be defined as an interval."""

    legend: bool
    normed: bool
    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""

    def infer_scale(self, arg: Any, data: Series[Any]) -> Scale:
        """Given data and a scaling argument, initialize appropriate scale class."""

    def get_mapping(self, scale: Scale, data: Series[Any]) -> Mapping:
        """Return a function that maps from data domain to property range."""

class PointSize(IntervalProperty):
    """Size (diameter) of a point mark, in points, with scaling by area."""

class LineWidth(IntervalProperty):
    """Thickness of a line mark, in points."""

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""

class EdgeWidth(IntervalProperty):
    """Thickness of the edges on a patch mark, in points."""

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""

class Stroke(IntervalProperty):
    """Thickness of lines that define point glyphs."""

class Alpha(IntervalProperty):
    """Opacity of the color values for an arbitrary mark."""

class Offset(IntervalProperty):
    """Offset for edge-aligned text, in point units."""

class FontSize(IntervalProperty):
    """Font size for textual marks, in points."""

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""

class ObjectProperty(Property):
    """A property defined by arbitrary an object, with inherently nominal scaling."""

    legend: bool
    normed: bool
    null_value: Any
    def default_scale(self, data: Series[Any]) -> Scale: ...
    def infer_scale(self, arg: Any, data: Series[Any]) -> Scale: ...
    def get_mapping(self, scale: Scale, data: Series[Any]) -> Mapping:
        """Define mapping as lookup into list of object values."""

class Marker(ObjectProperty):
    """Shape of points in scatter-type marks or lines with data points marked."""

    null_value: Incomplete
    def standardize(self, val: MarkerPattern) -> MarkerStyle: ...

class LineStyle(ObjectProperty):
    """Dash pattern for line-type marks."""

    null_value: str
    def standardize(self, val: str | DashPattern) -> DashPatternWithOffset: ...

class TextAlignment(ObjectProperty):
    legend: bool

class HorizontalAlignment(TextAlignment): ...
class VerticalAlignment(TextAlignment): ...

class Color(Property):
    """Color, as RGB(A), scalable with nominal palettes or continuous gradients."""

    legend: bool
    normed: bool
    def standardize(self, val: ColorSpec) -> RGBTuple | RGBATuple: ...
    def infer_scale(self, arg: Any, data: Series[Any]) -> Scale: ...
    def get_mapping(self, scale: Scale, data: Series[Any]) -> Mapping:
        """Return a function that maps from data domain to color values."""

class Fill(Property):
    """Boolean property of points/bars/patches that can be solid or outlined."""

    legend: bool
    normed: bool
    def default_scale(self, data: Series[Any]) -> Scale: ...
    def infer_scale(self, arg: Any, data: Series[Any]) -> Scale: ...
    def standardize(self, val: Any) -> bool: ...
    def get_mapping(self, scale: Scale, data: Series[Any]) -> Mapping:
        """Return a function that maps each data value to True or False."""

PROPERTY_CLASSES: dict[str, type[Property]]
PROPERTIES: dict[str, Property]
