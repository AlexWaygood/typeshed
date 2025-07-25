from _typeshed import Incomplete
from dataclasses import dataclass
from typing import Any, TypeVar
from typing_extensions import TypeAlias

from numpy.typing import NDArray
from pandas import DataFrame
from seaborn._core.properties import DashPattern, DashPatternWithOffset, RGBATuple
from seaborn._core.scales import Scale

_MarkT = TypeVar("_MarkT", bound=type[Mark])

class Mappable:
    def __init__(
        self, val: Any = None, depend: str | None = None, rc: str | None = None, auto: bool = False, grouping: bool = True
    ) -> None:
        """
        Property that can be mapped from data or set directly, with flexible defaults.

        Parameters
        ----------
        val : Any
            Use this value as the default.
        depend : str
            Use the value of this feature as the default.
        rc : str
            Use the value of this rcParam as the default.
        auto : bool
            The default value will depend on other parameters at compile time.
        grouping : bool
            If True, use the mapped variable to define groups.

        """

    @property
    def depend(self) -> Any:  # -> str | None
        """Return the name of the feature to source a default value from."""

    @property
    def grouping(self) -> bool: ...
    @property
    def default(self) -> Any:
        """Get the default value for this feature, or access the relevant rcParam."""

MappableBool: TypeAlias = bool | Mappable
MappableString: TypeAlias = str | Mappable
MappableFloat: TypeAlias = float | Mappable
MappableColor: TypeAlias = str | tuple[Incomplete, ...] | Mappable
MappableStyle: TypeAlias = str | DashPattern | DashPatternWithOffset | Mappable

@dataclass
class Mark:
    """Base class for objects that visually represent data."""

    artist_kws: dict[str, Any] = ...

def resolve_properties(mark: Mark, data: DataFrame, scales: dict[str, Scale]) -> dict[str, Any]: ...
def resolve_color(
    mark: Mark, data: DataFrame | dict[str, Any], prefix: str = "", scales: dict[str, Scale] | None = None
) -> RGBATuple | NDArray[Incomplete]:
    """
    Obtain a default, specified, or mapped value for a color feature.

    This method exists separately to support the relationship between a
    color and its corresponding alpha. We want to respect alpha values that
    are passed in specified (or mapped) color values but also make use of a
    separate `alpha` variable, which can be mapped. This approach may also
    be extended to support mapping of specific color channels (i.e.
    luminance, chroma) in the future.

    Parameters
    ----------
    mark :
        Mark with the color property.
    data :
        Container with data values for features that will be semantically mapped.
    prefix :
        Support "color", "fillcolor", etc.

    """

def document_properties(mark: _MarkT) -> _MarkT: ...
