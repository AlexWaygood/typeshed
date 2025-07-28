"""Polygons and their linear ring components."""

from collections.abc import Collection
from typing import NoReturn, overload
from typing_extensions import Self, TypeAlias

from .base import BaseGeometry
from .linestring import LineString, _ConvertibleToLineString
from .multilinestring import MultiLineString

__all__ = ["orient", "Polygon", "LinearRing"]

_ConvertibleToLinearRing: TypeAlias = _ConvertibleToLineString  # same alias but with better name for doc purposes
_PolygonShellLike: TypeAlias = Polygon | _ConvertibleToLinearRing | None
_PolygonHolesLike: TypeAlias = Collection[_ConvertibleToLinearRing | None] | None

class LinearRing(LineString):
    """Geometry type composed of one or more line segments that forms a closed loop.

    A LinearRing is a closed, one-dimensional feature.
    A LinearRing that crosses itself or touches itself at a single point is
    invalid and operations on it may fail.

    Parameters
    ----------
    coordinates : sequence
        A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
        an array-like with shape (N, 2) or (N, 3).
        Also can be a sequence of Point objects.

    Notes
    -----
    Rings are automatically closed. There is no need to specify a final
    coordinate pair identical to the first.

    Examples
    --------
    Construct a square ring.

    >>> from shapely import LinearRing
    >>> ring = LinearRing( ((0, 0), (0, 1), (1 ,1 ), (1 , 0)) )
    >>> ring.is_closed
    True
    >>> list(ring.coords)
    [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)]
    >>> ring.length
    4.0

    """

    def __new__(self, coordinates: _ConvertibleToLinearRing | None = None) -> Self:
        """Create a new LinearRing geometry."""

    @property
    def is_ccw(self) -> bool:
        """True if the ring is oriented counter clock-wise."""

class InteriorRingSequence:
    def __init__(self, parent: Polygon) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> LinearRing: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, key: int) -> LinearRing: ...
    @overload
    def __getitem__(self, key: slice) -> list[LinearRing]: ...

class Polygon(BaseGeometry):
    """A geometry type representing an area that is enclosed by a linear ring.

    A polygon is a two-dimensional feature and has a non-zero area. It may
    have one or more negative-space "holes" which are also bounded by linear
    rings. If any rings cross each other, the feature is invalid and
    operations on it may fail.

    Parameters
    ----------
    shell : sequence
        A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
        an array-like with shape (N, 2) or (N, 3).
        Also can be a sequence of Point objects.
    holes : sequence
        A sequence of objects which satisfy the same requirements as the
        shell parameters above

    Attributes
    ----------
    exterior : LinearRing
        The ring which bounds the positive space of the polygon.
    interiors : sequence
        A sequence of rings which bound all existing holes.

    Examples
    --------
    Create a square polygon with no holes

    >>> from shapely import Polygon
    >>> coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))
    >>> polygon = Polygon(coords)
    >>> polygon.area
    1.0

    """

    def __new__(self, shell: _PolygonShellLike = None, holes: _PolygonHolesLike = None) -> Self:
        """Create a new Polygon geometry."""

    @property
    def exterior(self) -> LinearRing:
        """Return the exterior ring of the polygon."""

    @property
    def interiors(self) -> list[LinearRing] | InteriorRingSequence:
        """Return the sequence of interior rings of the polygon."""

    @property
    def coords(self) -> NoReturn:
        """Not implemented for polygons."""

    def svg(self, scale_factor: float = 1.0, fill_color: str | None = None, opacity: float | None = None) -> str:  # type: ignore[override]
        """Return SVG path element for the Polygon geometry.

        Parameters
        ----------
        scale_factor : float
            Multiplication factor for the SVG stroke-width.  Default is 1.
        fill_color : str, optional
            Hex string for fill color. Default is to use "#66cc99" if
            geometry is valid, and "#ff3333" if invalid.
        opacity : float
            Float number between 0 and 1 for color opacity. Default value is 0.6

        """

    @classmethod
    def from_bounds(cls, xmin: float, ymin: float, xmax: float, ymax: float) -> Self:
        """Construct a `Polygon()` from spatial bounds."""
    # more precise base overrides
    @property
    def boundary(self) -> MultiLineString:
        """Return a lower dimension geometry that bounds the object.

        The boundary of a polygon is a line, the boundary of a line is a
        collection of points. The boundary of a point is an empty (null)
        collection.
        """

def orient(polygon: Polygon, sign: float = 1.0) -> Polygon:
    """Return an oriented polygon.

    It is recommended to use :func:`shapely.orient_polygons` instead.

    Parameters
    ----------
    polygon : shapely.Polygon
    sign : float, default 1.
        The sign of the result's signed area.
        A non-negative sign means that the coordinates of the geometry's exterior
        rings will be oriented counter-clockwise.

    Returns
    -------
    Geometry or array_like

    Refer to :func:`shapely.orient_polygons` for full documentation.

    """
