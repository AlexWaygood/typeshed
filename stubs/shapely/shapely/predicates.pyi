"""Predicates for spatial analysis."""

import sys
from typing import Any, Literal, overload
from typing_extensions import TypeAlias, TypeGuard

import numpy as np
from numpy.typing import NDArray

from ._typing import ArrayLike, ArrayLikeSeq, OptGeoArrayLike, OptGeoArrayLikeSeq
from .geometry.base import BaseGeometry
from .lib import Geometry

if sys.version_info >= (3, 10):
    _NPTrue: TypeAlias = np.bool_[Literal[True]]
    _NPFalse: TypeAlias = np.bool_[Literal[False]]
else:
    _NPTrue: TypeAlias = np.bool_
    _NPFalse: TypeAlias = np.bool_

__all__ = [
    "contains",
    "contains_properly",
    "contains_xy",
    "covered_by",
    "covers",
    "crosses",
    "disjoint",
    "dwithin",
    "equals",
    "equals_exact",
    "equals_identical",
    "has_m",
    "has_z",
    "intersects",
    "intersects_xy",
    "is_ccw",
    "is_closed",
    "is_empty",
    "is_geometry",
    "is_missing",
    "is_prepared",
    "is_ring",
    "is_simple",
    "is_valid",
    "is_valid_input",
    "is_valid_reason",
    "overlaps",
    "relate",
    "relate_pattern",
    "touches",
    "within",
]

@overload
def has_z(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a geometry has Z coordinates.

    Note that for GEOS < 3.12 this function returns False if the (first) Z coordinate
    equals NaN.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check for Z coordinates.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    get_coordinate_dimension, has_m

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> shapely.has_z(Point(0, 0))
    False
    >>> shapely.has_z(Point(0, 0, 0))
    True
    >>> shapely.has_z(Point())
    False

    """

@overload
def has_z(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def has_m(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a geometry has M coordinates.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check for M coordinates.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    get_coordinate_dimension, has_z

    Examples
    --------
    >>> import shapely
    >>> shapely.has_m(shapely.from_wkt("POINT (0 0)"))
    False
    >>> shapely.has_m(shapely.from_wkt("POINT Z (0 0 0)"))
    False
    >>> shapely.has_m(shapely.from_wkt("POINT M (0 0 0)"))
    True
    >>> shapely.has_m(shapely.from_wkt("POINT ZM (0 0 0 0)"))
    True

    """

@overload
def has_m(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_ccw(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a linestring or linearring is counterclockwise.

    Note that there are no checks on whether lines are actually closed and
    not self-intersecting, while this is a requirement for is_ccw. The recommended
    usage of this function for linestrings is ``is_ccw(g) & is_simple(g)`` and for
    linearrings ``is_ccw(g) & is_valid(g)``.

    Parameters
    ----------
    geometry : Geometry or array_like
        This function will return False for non-linear geometries and for
        lines with fewer than 4 points (including the closing point).
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_simple : Checks if a linestring is closed and simple.
    is_valid : Checks additionally if the geometry is simple.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LinearRing, LineString, Point
    >>> shapely.is_ccw(LinearRing([(0, 0), (0, 1), (1, 1), (0, 0)]))
    False
    >>> shapely.is_ccw(LinearRing([(0, 0), (1, 1), (0, 1), (0, 0)]))
    True
    >>> shapely.is_ccw(LineString([(0, 0), (1, 1), (0, 1)]))
    False
    >>> shapely.is_ccw(Point(0, 0))
    False

    """

@overload
def is_ccw(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_closed(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a linestring's first and last points are equal.

    Parameters
    ----------
    geometry : Geometry or array_like
        This function will return False for non-linestrings.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_ring : Checks additionally if the geometry is simple.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.is_closed(LineString([(0, 0), (1, 1)]))
    False
    >>> shapely.is_closed(LineString([(0, 0), (0, 1), (1, 1), (0, 0)]))
    True
    >>> shapely.is_closed(Point(0, 0))
    False

    """

@overload
def is_closed(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_empty(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a geometry is an empty point, polygon, etc.

    Parameters
    ----------
    geometry : Geometry or array_like
        Any geometry type is accepted.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_missing : checks if the object is a geometry

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> shapely.is_empty(Point())
    True
    >>> shapely.is_empty(Point(0, 0))
    False
    >>> shapely.is_empty(None)
    False

    """

@overload
def is_empty(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_geometry(geometry: Geometry, **kwargs) -> _NPTrue:
    """Return True if the object is a geometry.

    Parameters
    ----------
    geometry : any object or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_missing : check if an object is missing (None)
    is_valid_input : check if an object is a geometry or None

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, Point
    >>> shapely.is_geometry(Point(0, 0))
    True
    >>> shapely.is_geometry(GeometryCollection())
    True
    >>> shapely.is_geometry(None)
    False
    >>> shapely.is_geometry("text")
    False

    """

@overload
def is_geometry(geometry: None, **kwargs) -> _NPFalse: ...
@overload
def is_geometry(geometry: ArrayLikeSeq[Any], **kwargs) -> NDArray[np.bool_]: ...  # type: ignore[overload-overlap]
@overload
def is_geometry(geometry: object, **kwargs) -> TypeGuard[BaseGeometry]: ...
@overload
def is_missing(geometry: Geometry, **kwargs) -> _NPFalse:
    """Return True if the object is not a geometry (None).

    Parameters
    ----------
    geometry : any object or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_geometry : check if an object is a geometry
    is_valid_input : check if an object is a geometry or None
    is_empty : checks if the object is an empty geometry

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, Point
    >>> shapely.is_missing(Point(0, 0))
    False
    >>> shapely.is_missing(GeometryCollection())
    False
    >>> shapely.is_missing(None)
    True
    >>> shapely.is_missing("text")
    False

    """

@overload
def is_missing(geometry: None, **kwargs) -> _NPTrue: ...
@overload
def is_missing(geometry: ArrayLikeSeq[Any], **kwargs) -> NDArray[np.bool_]: ...  # type: ignore[overload-overlap]
@overload
def is_missing(geometry: object, **kwargs) -> TypeGuard[None]: ...
@overload
def is_prepared(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a Geometry is prepared.

    Note that it is not necessary to check if a geometry is already prepared
    before preparing it. It is more efficient to call ``prepare`` directly
    because it will skip geometries that are already prepared.

    This function will return False for missing geometries (None).

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_valid_input : check if an object is a geometry or None
    prepare : prepare a geometry

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> geometry = Point(0, 0)
    >>> shapely.is_prepared(Point(0, 0))
    False
    >>> shapely.prepare(geometry)
    >>> shapely.is_prepared(geometry)
    True
    >>> shapely.is_prepared(None)
    False

    """

@overload
def is_prepared(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_valid_input(geometry: Geometry | None, **kwargs) -> _NPTrue:
    """Return True if the object is a geometry or None.

    Parameters
    ----------
    geometry : any object or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_geometry : checks if an object is a geometry
    is_missing : checks if an object is None

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, Point
    >>> shapely.is_valid_input(Point(0, 0))
    True
    >>> shapely.is_valid_input(GeometryCollection())
    True
    >>> shapely.is_valid_input(None)
    True
    >>> shapely.is_valid_input(1.0)
    False
    >>> shapely.is_valid_input("text")
    False

    """

@overload
def is_valid_input(geometry: ArrayLikeSeq[Any], **kwargs) -> NDArray[np.bool_]: ...  # type: ignore[overload-overlap]
@overload
def is_valid_input(geometry: object, **kwargs) -> TypeGuard[BaseGeometry | None]: ...
@overload
def is_ring(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a linestring is closed and simple.

    This function will return False for non-linestrings.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_closed : Checks only if the geometry is closed.
    is_simple : Checks only if the geometry is simple.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.is_ring(Point(0, 0))
    False
    >>> geom = LineString([(0, 0), (1, 1)])
    >>> shapely.is_closed(geom), shapely.is_simple(geom), shapely.is_ring(geom)
    (False, True, False)
    >>> geom = LineString([(0, 0), (0, 1), (1, 1), (0, 0)])
    >>> shapely.is_closed(geom), shapely.is_simple(geom), shapely.is_ring(geom)
    (True, True, True)
    >>> geom = LineString([(0, 0), (1, 1), (0, 1), (1, 0), (0, 0)])
    >>> shapely.is_closed(geom), shapely.is_simple(geom), shapely.is_ring(geom)
    (True, False, False)

    """

@overload
def is_ring(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_simple(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if the geometry is simple.

    A simple geometry has no anomalous geometric points, such as
    self-intersections or self tangency.

    Note that polygons and linearrings are assumed to be simple. Use is_valid
    to check these kind of geometries for self-intersections.

    This function will return False for geometrycollections.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_ring : Checks additionally if the geometry is closed.
    is_valid : Checks whether a geometry is well formed.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Polygon
    >>> shapely.is_simple(Polygon([(1, 1), (2, 1), (2, 2), (1, 1)]))
    True
    >>> shapely.is_simple(LineString([(0, 0), (1, 1), (0, 1), (1, 0), (0, 0)]))
    False
    >>> shapely.is_simple(None)
    False

    """

@overload
def is_simple(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_valid(geometry: Geometry | None, **kwargs) -> np.bool_:
    """Return True if a geometry is well formed.

    Returns False for missing values.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check. Any geometry type is accepted.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_valid_reason : Returns the reason in case of invalid.

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, LineString, Polygon
    >>> shapely.is_valid(LineString([(0, 0), (1, 1)]))
    True
    >>> shapely.is_valid(Polygon([(0, 0), (1, 1), (1, 2), (1, 1), (0, 0)]))
    False
    >>> shapely.is_valid(GeometryCollection())
    True
    >>> shapely.is_valid(None)
    False

    """

@overload
def is_valid(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def is_valid_reason(geometry: None, **kwargs) -> None:
    """Return a string stating if a geometry is valid and if not, why.

    Returns None for missing values.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to check. Any geometry type is accepted.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    is_valid : returns True or False

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Polygon
    >>> shapely.is_valid_reason(LineString([(0, 0), (1, 1)]))
    'Valid Geometry'
    >>> shapely.is_valid_reason(Polygon([(0, 0), (1, 1), (1, 2), (1, 1), (0, 0)]))
    'Self-intersection[1 2]'
    >>> shapely.is_valid_reason(None) is None
    True

    """

@overload
def is_valid_reason(geometry: Geometry, **kwargs) -> str: ...
@overload
def is_valid_reason(geometry: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.object_]: ...
@overload
def crosses(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if A and B spatially cross.

    A crosses B if they have some but not all interior points in common,
    the intersection is one dimension less than the maximum dimension of A or B,
    and the intersection is not equal to either A or B.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, MultiPoint, Point, Polygon
    >>> line = LineString([(0, 0), (1, 1)])
    >>> # A contains B:
    >>> shapely.crosses(line, Point(0.5, 0.5))
    False
    >>> # A and B intersect at a point but do not share all points:
    >>> shapely.crosses(line, MultiPoint([(0, 1), (0.5, 0.5)]))
    True
    >>> shapely.crosses(line, LineString([(0, 1), (1, 0)]))
    True
    >>> # A is contained by B; their intersection is a line (same dimension):
    >>> shapely.crosses(line, LineString([(0, 0), (2, 2)]))
    False
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> # A contains B:
    >>> shapely.crosses(area, line)
    False
    >>> # A and B intersect with a line (lower dimension) but do not share all points:
    >>> shapely.crosses(area, LineString([(0, 0), (2, 2)]))
    True
    >>> # A contains B:
    >>> shapely.crosses(area, Point(0.5, 0.5))
    False
    >>> # A contains some but not all points of B; they intersect at a point:
    >>> shapely.crosses(area, MultiPoint([(2, 2), (0.5, 0.5)]))
    True

    """

@overload
def crosses(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def crosses(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if geometry B is completely inside geometry A.

    A contains B if no points of B lie in the exterior of A and at least one
    point of the interior of B lies in the interior of A.

    Note: following this definition, a geometry does not contain its boundary,
    but it does contain itself. See ``contains_properly`` for a version where
    a geometry does not contain itself.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    within : ``contains(A, B) == within(B, A)``
    contains_properly : contains with no common boundary points
    prepare : improve performance by preparing ``a`` (the first argument)
    contains_xy : variant for checking against a Point with x, y coordinates

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.contains(line, Point(0, 0))
    False
    >>> shapely.contains(line, Point(0.5, 0.5))
    True
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.contains(area, Point(0, 0))
    False
    >>> shapely.contains(area, line)
    True
    >>> shapely.contains(area, LineString([(0, 0), (2, 2)]))
    False
    >>> polygon_with_hole = Polygon(
    ...     [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)],
    ...     holes=[[(2, 2), (2, 4), (4, 4), (4, 2), (2, 2)]]
    ... )
    >>> shapely.contains(polygon_with_hole, Point(1, 1))
    True
    >>> shapely.contains(polygon_with_hole, Point(2, 2))
    False
    >>> shapely.contains(polygon_with_hole, LineString([(1, 1), (5, 5)]))
    False
    >>> shapely.contains(area, area)
    True
    >>> shapely.contains(area, None)
    False

    """

@overload
def contains(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_properly(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if geometry B is completely inside geometry A, with no common
    boundary points.

    A contains B properly if B intersects the interior of A but not the
    boundary (or exterior). This means that a geometry A does not
    "contain properly" itself, which contrasts with the ``contains`` function,
    where common points on the boundary are allowed.

    Note: this function will prepare the geometries under the hood if needed.
    You can prepare the geometries in advance to avoid repeated preparation
    when calling this function multiple times.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    contains : contains which allows common boundary points
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> area1 = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
    >>> area2 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> area3 = Polygon([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])

    ``area1`` and ``area2`` have a common border:

    >>> shapely.contains(area1, area2)
    True
    >>> shapely.contains_properly(area1, area2)
    False

    ``area3`` is completely inside ``area1`` with no common border:

    >>> shapely.contains(area1, area3)
    True
    >>> shapely.contains_properly(area1, area3)
    True

    """

@overload
def contains_properly(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_properly(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def covered_by(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if no point in geometry A is outside geometry B.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    covers : ``covered_by(A, B) == covers(B, A)``
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.covered_by(Point(0, 0), line)
    True
    >>> shapely.covered_by(Point(0.5, 0.5), line)
    True
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.covered_by(Point(0, 0), area)
    True
    >>> shapely.covered_by(line, area)
    True
    >>> shapely.covered_by(LineString([(0, 0), (2, 2)]), area)
    False
    >>> polygon_with_hole = Polygon(
    ...     [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)],
    ...     holes=[[(2, 2), (2, 4), (4, 4), (4, 2), (2, 2)]]
    ... )
    >>> shapely.covered_by(Point(1, 1), polygon_with_hole)
    True
    >>> shapely.covered_by(Point(2, 2), polygon_with_hole)
    True
    >>> shapely.covered_by(LineString([(1, 1), (5, 5)]), polygon_with_hole)
    False
    >>> shapely.covered_by(area, area)
    True
    >>> shapely.covered_by(None, area)
    False

    """

@overload
def covered_by(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def covered_by(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def covers(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if no point in geometry B is outside geometry A.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    covered_by : ``covers(A, B) == covered_by(B, A)``
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.covers(line, Point(0, 0))
    True
    >>> shapely.covers(line, Point(0.5, 0.5))
    True
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.covers(area, Point(0, 0))
    True
    >>> shapely.covers(area, line)
    True
    >>> shapely.covers(area, LineString([(0, 0), (2, 2)]))
    False
    >>> polygon_with_hole = Polygon(
    ...     [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)],
    ...     holes=[[(2, 2), (2, 4), (4, 4), (4, 2), (2, 2)]]
    ... )
    >>> shapely.covers(polygon_with_hole, Point(1, 1))
    True
    >>> shapely.covers(polygon_with_hole, Point(2, 2))
    True
    >>> shapely.covers(polygon_with_hole, LineString([(1, 1), (5, 5)]))
    False
    >>> shapely.covers(area, area)
    True
    >>> shapely.covers(area, None)
    False

    """

@overload
def covers(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def covers(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def disjoint(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if A and B do not share any point in space.

    Disjoint implies that overlaps, touches, within, and intersects are False.
    Note missing (None) values are never disjoint.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    intersects : ``disjoint(A, B) == ~intersects(A, B)``
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, LineString, Point
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.disjoint(line, Point(0, 0))
    False
    >>> shapely.disjoint(line, Point(0, 1))
    True
    >>> shapely.disjoint(line, LineString([(0, 2), (2, 0)]))
    False
    >>> empty = GeometryCollection()
    >>> shapely.disjoint(line, empty)
    True
    >>> shapely.disjoint(empty, empty)
    True
    >>> shapely.disjoint(empty, None)
    False
    >>> shapely.disjoint(None, None)
    False

    """

@overload
def disjoint(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def disjoint(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def equals(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if A and B are spatially equal.

    If A is within B and B is within A, A and B are considered equal. The
    ordering of points can be different.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    equals_exact : Check if A and B are structurally equal given a specified
        tolerance.

    Examples
    --------
    >>> import shapely
    >>> from shapely import GeometryCollection, LineString, Polygon
    >>> line = LineString([(0, 0), (5, 5), (10, 10)])
    >>> shapely.equals(line, LineString([(0, 0), (10, 10)]))
    True
    >>> shapely.equals(Polygon(), GeometryCollection())
    True
    >>> shapely.equals(None, None)
    False

    """

@overload
def equals(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def equals(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if A and B share any portion of space.

    Intersects implies that overlaps, touches, covers, or within are True.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    disjoint : ``intersects(A, B) == ~disjoint(A, B)``
    prepare : improve performance by preparing ``a`` (the first argument)
    intersects_xy : variant for checking against a Point with x, y coordinates

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.intersects(line, Point(0, 0))
    True
    >>> shapely.intersects(line, Point(0, 1))
    False
    >>> shapely.intersects(line, LineString([(0, 2), (2, 0)]))
    True
    >>> shapely.intersects(None, None)
    False

    """

@overload
def intersects(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def overlaps(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if A and B spatially overlap.

    A and B overlap if they have some but not all points/space in
    common, have the same dimension, and the intersection of the
    interiors of the two geometries has the same dimension as the
    geometries themselves. That is, only polyons can overlap other
    polygons and only lines can overlap other lines. If A covers or is
    within B, overlaps won't be True.

    If either A or B are None, the output is always False.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword
        arguments.

    See Also
    --------
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> poly = Polygon([(0, 0), (0, 4), (4, 4), (4, 0), (0, 0)])
    >>> # A and B share all points (are spatially equal):
    >>> shapely.overlaps(poly, poly)
    False
    >>> # A contains B; all points of B are within A:
    >>> shapely.overlaps(poly, Polygon([(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]))
    False
    >>> # A partially overlaps with B:
    >>> shapely.overlaps(poly, Polygon([(2, 2), (2, 6), (6, 6), (6, 2), (2, 2)]))
    True
    >>> line = LineString([(2, 2), (6, 6)])
    >>> # A and B are different dimensions; they cannot overlap:
    >>> shapely.overlaps(poly, line)
    False
    >>> shapely.overlaps(poly, Point(2, 2))
    False
    >>> # A and B share some but not all points:
    >>> shapely.overlaps(line, LineString([(0, 0), (4, 4)]))
    True
    >>> # A and B intersect only at a point (lower dimension); they do not overlap
    >>> shapely.overlaps(line, LineString([(6, 0), (0, 6)]))
    False
    >>> shapely.overlaps(poly, None)
    False
    >>> shapely.overlaps(None, None)
    False

    """

@overload
def overlaps(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def overlaps(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def touches(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if the only points shared between A and B are on their boundaries.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> line = LineString([(0, 2), (2, 0)])
    >>> shapely.touches(line, Point(0, 2))
    True
    >>> shapely.touches(line, Point(1, 1))
    False
    >>> shapely.touches(line, LineString([(0, 0), (1, 1)]))
    True
    >>> shapely.touches(line, LineString([(0, 0), (2, 2)]))
    False
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.touches(area, Point(0.5, 0))
    True
    >>> shapely.touches(area, Point(0.5, 0.5))
    False
    >>> shapely.touches(area, line)
    True
    >>> shapely.touches(area, Polygon([(0, 1), (1, 1), (1, 2), (0, 2), (0, 1)]))
    True

    """

@overload
def touches(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def touches(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def within(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if geometry A is completely inside geometry B.

    A is within B if no points of A lie in the exterior of B and at least one
    point of the interior of A lies in the interior of B.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    contains : ``within(A, B) == contains(B, A)``
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point, Polygon
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.within(Point(0, 0), line)
    False
    >>> shapely.within(Point(0.5, 0.5), line)
    True
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.within(Point(0, 0), area)
    False
    >>> shapely.within(line, area)
    True
    >>> shapely.within(LineString([(0, 0), (2, 2)]), area)
    False
    >>> polygon_with_hole = Polygon(
    ...     [(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)],
    ...     holes=[[(2, 2), (2, 4), (4, 4), (4, 2), (2, 2)]]
    ... )
    >>> shapely.within(Point(1, 1), polygon_with_hole)
    True
    >>> shapely.within(Point(2, 2), polygon_with_hole)
    False
    >>> shapely.within(LineString([(1, 1), (5, 5)]), polygon_with_hole)
    False
    >>> shapely.within(area, area)
    True
    >>> shapely.within(None, area)
    False

    """

@overload
def within(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def within(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def equals_exact(
    a: Geometry | None, b: Geometry | None, tolerance: float = 0.0, *, normalize: bool = False, **kwargs
) -> np.bool_:
    """Return True if the geometries are structurally equivalent within a given
    tolerance.

    This method uses exact coordinate equality, which requires coordinates
    to be equal (within specified tolerance) and in the same order for
    all components (vertices, rings, or parts) of a geometry. This is in
    contrast with the :func:`equals` function which uses spatial
    (topological) equality and does not require all components to be in the
    same order. Because of this, it is possible for :func:`equals` to
    be ``True`` while :func:`equals_exact` is ``False``.

    The order of the coordinates can be normalized (by setting the `normalize`
    keyword to ``True``) so that this function will return ``True`` when geometries
    are structurally equivalent but differ only in the ordering of vertices.
    However, this function will still return ``False`` if the order of interior
    rings within a :class:`Polygon` or the order of geometries within a multi
    geometry are different.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    tolerance : float or array_like (default: 0.)
        The tolerance to use in the comparison.
    normalize : bool, optional (default: False)
        If True, normalize the two geometries so that the coordinates are
        in the same order.

        .. versionadded:: 2.1.0
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    equals : Check if `a` and `b` are spatially (topologically) equal.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point, Polygon
    >>> point1 = Point(50, 50)
    >>> point2 = Point(50.1, 50.1)
    >>> shapely.equals_exact(point1, point2)
    False
    >>> shapely.equals_exact(point1, point2, tolerance=0.2)
    True
    >>> shapely.equals_exact(point1, None, tolerance=0.2)
    False

    Difference between structural and spatial equality:

    >>> polygon1 = Polygon([(0, 0), (1, 1), (0, 1), (0, 0)])
    >>> polygon2 = Polygon([(0, 0), (0, 1), (1, 1), (0, 0)])
    >>> shapely.equals_exact(polygon1, polygon2)
    False
    >>> shapely.equals(polygon1, polygon2)
    True

    """

@overload
def equals_exact(
    a: OptGeoArrayLike, b: OptGeoArrayLike, tolerance: ArrayLikeSeq[float], *, normalize: bool = False, **kwargs
) -> NDArray[np.bool_]: ...
@overload
def equals_exact(
    a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, tolerance: ArrayLike[float] = 0.0, *, normalize: bool = False, **kwargs
) -> NDArray[np.bool_]: ...
@overload
def equals_exact(
    a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, tolerance: ArrayLike[float] = 0.0, *, normalize: bool = False, **kwargs
) -> NDArray[np.bool_]: ...
@overload
def equals_identical(a: Geometry | None, b: Geometry | None, **kwargs) -> np.bool_:
    """Return True if the geometries are identical.

    This function verifies whether geometries are pointwise equivalent by checking
    that the structure, ordering, and values of all vertices are identical
    in all dimensions.

    Similarly to :func:`equals_exact`, this function uses exact coordinate
    equality and requires coordinates to be in the same order for all
    components (vertices, rings, or parts) of a geometry. However, in
    contrast :func:`equals_exact`, this function does not allow to specify
    a tolerance, but does require all dimensions to be the same
    (:func:`equals_exact` ignores the Z and M dimensions), and NaN values
    are considered to be equal to other NaN values.

    This function is the vectorized equivalent of scalar equality of
    geometry objects (``a == b``, i.e. ``__eq__``).

    .. versionadded:: 2.1.0

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    equals_exact : Check if geometries are structurally equal given a specified
        tolerance.
    equals : Check if geometries are spatially (topologically) equal.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> shapely.equals_identical(Point(1, 2, 3), Point(1, 2, 3))
    True
    >>> shapely.equals_identical(Point(1, 2, 3), Point(1, 2, 0))
    False
    """

@overload
def equals_identical(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.bool_]: ...
@overload
def equals_identical(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.bool_]: ...
@overload
def relate(a: Geometry | None, b: None, **kwargs) -> None:
    """Return a string representation of the DE-9IM intersection matrix.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> point = Point(0, 0)
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.relate(point, line)
    'F0FFFF102'

    """

@overload
def relate(a: None, b: Geometry | None, **kwargs) -> None: ...
@overload
def relate(a: Geometry, b: Geometry, **kwargs) -> str: ...
@overload
def relate(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, **kwargs) -> NDArray[np.object_]: ...
@overload
def relate(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, **kwargs) -> NDArray[np.object_]: ...
@overload
def relate_pattern(a: Geometry | None, b: Geometry | None, pattern: str, **kwargs) -> np.bool_:
    """Return True if the DE-9IM relationship code satisfies the pattern.

    This function compares the DE-9IM code string for two geometries
    against a specified pattern. If the string matches the pattern then
    ``True`` is returned, otherwise ``False``. The pattern specified can
    be an exact match (``0``, ``1`` or ``2``), a boolean match
    (uppercase ``T`` or ``F``), or a wildcard (``*``). For example,
    the pattern for the ``within`` predicate is ``'T*F**F***'``.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    pattern : string
        The pattern to match the DE-9IM relationship code against.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point, Polygon
    >>> point = Point(0.5, 0.5)
    >>> square = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    >>> shapely.relate(point, square)
    '0FFFFF212'
    >>> shapely.relate_pattern(point, square, "T*F**F***")
    True

    """

@overload
def relate_pattern(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, pattern: str, **kwargs) -> NDArray[np.bool_]: ...
@overload
def relate_pattern(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, pattern: str, **kwargs) -> NDArray[np.bool_]: ...
@overload
def dwithin(a: Geometry | None, b: Geometry | None, distance: float, **kwargs) -> np.bool_:
    """Return True if the geometries are within a given distance.

    Using this function is more efficient than computing the distance and
    comparing the result.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to check.
    distance : float
        Negative distances always return False.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    distance : compute the actual distance between A and B
    prepare : improve performance by preparing ``a`` (the first argument)

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> point = Point(0.5, 0.5)
    >>> shapely.dwithin(point, Point(2, 0.5), 2)
    True
    >>> shapely.dwithin(point, Point(2, 0.5), [2, 1.5, 1]).tolist()
    [True, True, False]
    >>> shapely.dwithin(point, Point(0.5, 0.5), 0)
    True
    >>> shapely.dwithin(point, None, 100)
    False

    """

@overload
def dwithin(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, distance: float, **kwargs) -> NDArray[np.bool_]: ...
@overload
def dwithin(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, distance: float, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_xy(geom: Geometry | None, x: float, y: float, **kwargs) -> np.bool_:
    """Return True if the Point (x, y) is completely inside geom.

    This is a special-case (and faster) variant of the `contains` function
    which avoids having to create a Point object if you start from x/y
    coordinates.

    Note that in the case of points, the `contains_properly` predicate is
    equivalent to `contains`.

    See the docstring of `contains` for more details about the predicate.

    Parameters
    ----------
    geom : Geometry or array_like
        Geometry or geometries to check if they contain the point.
    x, y : float or array_like
        Coordinates as separate x and y arrays, or a single array of
        coordinate x, y tuples.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    contains : variant taking two geometries as input

    Notes
    -----
    If you compare a small number of polygons or lines with many points,
    it can be beneficial to prepare the geometries in advance using
    :func:`shapely.prepare`.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point, Polygon
    >>> area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    >>> shapely.contains(area, Point(0.5, 0.5))
    True
    >>> shapely.contains_xy(area, 0.5, 0.5)
    True

    """

@overload
def contains_xy(geom: OptGeoArrayLike, x: ArrayLikeSeq[float], y: None = None, **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_xy(geom: Geometry | None, x: ArrayLike[float], y: ArrayLikeSeq[float], **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_xy(geom: Geometry | None, x: ArrayLikeSeq[float], y: ArrayLike[float], **kwargs) -> NDArray[np.bool_]: ...
@overload
def contains_xy(geom: OptGeoArrayLikeSeq, x: ArrayLike[float], y: ArrayLike[float], **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects_xy(geom: Geometry | None, x: float, y: float, **kwargs) -> np.bool_:
    """Return True if geom and the Point (x, y) share any portion of space.

    This is a special-case (and faster) variant of the `intersects` function
    which avoids having to create a Point object if you start from x/y
    coordinates.

    See the docstring of `intersects` for more details about the predicate.

    Parameters
    ----------
    geom : Geometry or array_like
        Geometry or geometries to check if they intersect with the point.
    x, y : float or array_like
        Coordinates as separate x and y arrays, or a single array of
        coordinate x, y tuples.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    intersects : variant taking two geometries as input

    Notes
    -----
    If you compare a single or few geometries with many points, it can be
    beneficial to prepare the geometries in advance using
    :func:`shapely.prepare`.

    The `touches` predicate can be determined with this function by getting
    the boundary of the geometries: ``intersects_xy(boundary(geom), x, y)``.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> line = LineString([(0, 0), (1, 1)])
    >>> shapely.intersects(line, Point(0, 0))
    True
    >>> shapely.intersects_xy(line, 0, 0)
    True

    """

@overload
def intersects_xy(geom: OptGeoArrayLike, x: ArrayLikeSeq[float], y: None = None, **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects_xy(geom: Geometry | None, x: ArrayLike[float], y: ArrayLikeSeq[float], **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects_xy(geom: Geometry | None, x: ArrayLikeSeq[float], y: ArrayLike[float], **kwargs) -> NDArray[np.bool_]: ...
@overload
def intersects_xy(geom: OptGeoArrayLikeSeq, x: ArrayLike[float], y: ArrayLike[float], **kwargs) -> NDArray[np.bool_]: ...
