"""Multi-part collections of geometries."""

from collections.abc import Collection
from typing import overload
from typing_extensions import Self

from .._typing import OptGeoArrayLike
from .base import BaseMultipartGeometry, GeometrySequence, _GeoT_co

class GeometryCollection(BaseMultipartGeometry[_GeoT_co]):
    """Collection of one or more geometries that can be of different types.

    Parameters
    ----------
    geoms : list
        A list of shapely geometry instances, which may be of varying geometry
        types.

    Attributes
    ----------
    geoms : sequence
        A sequence of Shapely geometry instances

    Examples
    --------
    Create a GeometryCollection with a Point and a LineString

    >>> from shapely import GeometryCollection, LineString, Point
    >>> p = Point(51, -1)
    >>> l = LineString([(52, -1), (49, 2)])
    >>> gc = GeometryCollection([p, l])

    """

    # Overloads of __new__ are used because mypy is unable to narrow the typevar otherwise
    @overload
    def __new__(
        self, geoms: BaseMultipartGeometry[_GeoT_co] | GeometrySequence[BaseMultipartGeometry[_GeoT_co]] | Collection[_GeoT_co]
    ) -> Self:
        """Create a new GeometryCollection."""

    @overload
    def __new__(self, geoms: OptGeoArrayLike = None) -> Self: ...
    # more precise base overrides
    @property
    def boundary(self) -> None:
        """Return a lower dimension geometry that bounds the object.

        The boundary of a polygon is a line, the boundary of a line is a
        collection of points. The boundary of a point is an empty (null)
        collection.
        """
