"""Support for GEOS prepared geometry operations."""

from typing import Generic, Literal

from ._typing import GeoT
from .lib import Geometry

class PreparedGeometry(Generic[GeoT]):
    """A geometry prepared for efficient comparison to a set of other geometries.

    Examples
    --------
    >>> from shapely.prepared import prep
    >>> from shapely.geometry import Point, Polygon
    >>> triangle = Polygon([(0.0, 0.0), (1.0, 1.0), (1.0, -1.0)])
    >>> p = prep(triangle)
    >>> p.intersects(Point(0.5, 0.5))
    True

    """

    context: GeoT
    prepared: Literal[True]
    def __init__(self, context: GeoT | PreparedGeometry[GeoT]) -> None:
        """Prepare a geometry for efficient comparison to other geometries."""

    def contains(self, other: Geometry | None) -> bool:
        """Return True if the geometry contains the other, else False."""

    def contains_properly(self, other: Geometry | None) -> bool:
        """Return True if the geometry properly contains the other, else False."""

    def covers(self, other: Geometry | None) -> bool:
        """Return True if the geometry covers the other, else False."""

    def crosses(self, other: Geometry | None) -> bool:
        """Return True if the geometries cross, else False."""

    def disjoint(self, other: Geometry | None) -> bool:
        """Return True if geometries are disjoint, else False."""

    def intersects(self, other: Geometry | None) -> bool:
        """Return True if geometries intersect, else False."""

    def overlaps(self, other: Geometry | None) -> bool:
        """Return True if geometries overlap, else False."""

    def touches(self, other: Geometry | None) -> bool:
        """Return True if geometries touch, else False."""

    def within(self, other: Geometry | None) -> bool:
        """Return True if geometry is within the other, else False."""

def prep(ob: GeoT | PreparedGeometry[GeoT]) -> PreparedGeometry[GeoT]:
    """Create and return a prepared geometric object."""
