"""Set-theoretic operations on geometry objects."""

from typing import overload
from typing_extensions import deprecated

from ._typing import GeoArray, OptGeoArrayLike, OptGeoArrayLikeSeq
from .geometry.base import BaseGeometry
from .lib import Geometry

__all__ = [
    "coverage_union",
    "coverage_union_all",
    "difference",
    "disjoint_subset_union",
    "disjoint_subset_union_all",
    "intersection",
    "intersection_all",
    "symmetric_difference",
    "symmetric_difference_all",
    "unary_union",
    "union",
    "union_all",
]

@overload
def difference(a: Geometry, b: Geometry, grid_size: float | None = None, **kwargs) -> BaseGeometry:
    """Return the part of geometry A that does not intersect with geometry B.

    If grid_size is nonzero, input coordinates will be snapped to a precision
    grid of that size and resulting coordinates will be snapped to that same
    grid.  If 0, this operation will use double precision coordinates.  If None,
    the highest precision of the inputs will be used, which may be previously
    set using set_precision.  Note: returned geometry does not have precision
    set unless specified previously by set_precision.

    Parameters
    ----------
    a : Geometry or array_like
        Geometry or geometries to subtract b from.
    b : Geometry or array_like
        Geometry or geometries to subtract from a.
    grid_size : float, optional
        Precision grid size; will use the highest precision of the inputs by default.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``grid_size`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    set_precision

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line = LineString([(0, 0), (2, 2)])
    >>> shapely.difference(line, LineString([(1, 1), (3, 3)]))
    <LINESTRING (0 0, 1 1)>
    >>> shapely.difference(line, LineString())
    <LINESTRING (0 0, 2 2)>
    >>> shapely.difference(line, None) is None
    True
    >>> box1 = shapely.box(0, 0, 2, 2)
    >>> box2 = shapely.box(1, 1, 3, 3)
    >>> shapely.difference(box1, box2).normalize()
    <POLYGON ((0 0, 0 2, 1 2, 1 1, 2 1, 2 0, 0 0))>
    >>> box1 = shapely.box(0.1, 0.2, 2.1, 2.1)
    >>> shapely.difference(box1, box2, grid_size=1)
    <POLYGON ((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0))>

    """

@overload
def difference(a: None, b: Geometry | None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def difference(a: Geometry | None, b: None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def difference(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def difference(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def intersection(a: Geometry, b: Geometry, grid_size: float | None = None, **kwargs) -> BaseGeometry:
    """Return the geometry that is shared between input geometries.

    If grid_size is nonzero, input coordinates will be snapped to a precision
    grid of that size and resulting coordinates will be snapped to that same
    grid.  If 0, this operation will use double precision coordinates.  If None,
    the highest precision of the inputs will be used, which may be previously
    set using set_precision.  Note: returned geometry does not have precision
    set unless specified previously by set_precision.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to intersect with.
    grid_size : float, optional
        Precision grid size; will use the highest precision of the inputs by default.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``grid_size`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    intersection_all
    set_precision

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line = LineString([(0, 0), (2, 2)])
    >>> shapely.intersection(line, LineString([(1, 1), (3, 3)]))
    <LINESTRING (1 1, 2 2)>
    >>> box1 = shapely.box(0, 0, 2, 2)
    >>> box2 = shapely.box(1, 1, 3, 3)
    >>> shapely.intersection(box1, box2).normalize()
    <POLYGON ((1 1, 1 2, 2 2, 2 1, 1 1))>
    >>> box1 = shapely.box(0.1, 0.2, 2.1, 2.1)
    >>> shapely.intersection(box1, box2, grid_size=1)
    <POLYGON ((2 2, 2 1, 1 1, 1 2, 2 2))>

    """

@overload
def intersection(a: None, b: Geometry | None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def intersection(a: Geometry | None, b: None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def intersection(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def intersection(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def intersection_all(geometries: OptGeoArrayLike, axis: None = None, **kwargs) -> BaseGeometry:
    """Return the intersection of multiple geometries.

    This function ignores None values when other Geometry elements are present.
    If all elements of the given axis are None, an empty GeometryCollection is
    returned.

    Parameters
    ----------
    geometries : array_like
        Geometries to calculate the intersection of.
    axis : int, optional
        Axis along which the operation is performed. The default (None)
        performs the operation over all axes, returning a scalar value.
        Axis may be negative, in which case it counts from the last to the
        first axis.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``axis`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    intersection

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line1 = LineString([(0, 0), (2, 2)])
    >>> line2 = LineString([(1, 1), (3, 3)])
    >>> shapely.intersection_all([line1, line2])
    <LINESTRING (1 1, 2 2)>
    >>> shapely.intersection_all([[line1, line2, None]], axis=1).tolist()
    [<LINESTRING (1 1, 2 2)>]
    >>> shapely.intersection_all([line1, None])
    <LINESTRING (0 0, 2 2)>

    """

@overload
def intersection_all(geometries: OptGeoArrayLikeSeq, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...
@overload
def symmetric_difference(a: Geometry, b: Geometry, grid_size: float | None = None, **kwargs) -> BaseGeometry:
    """Return the geometry with the portions of input geometries that do not intersect.

    If grid_size is nonzero, input coordinates will be snapped to a precision
    grid of that size and resulting coordinates will be snapped to that same
    grid.  If 0, this operation will use double precision coordinates.  If None,
    the highest precision of the inputs will be used, which may be previously
    set using set_precision.  Note: returned geometry does not have precision
    set unless specified previously by set_precision.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to evaluate symmetric difference with.
    grid_size : float, optional
        Precision grid size; will use the highest precision of the inputs by default.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``grid_size`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    symmetric_difference_all
    set_precision

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line = LineString([(0, 0), (2, 2)])
    >>> shapely.symmetric_difference(line, LineString([(1, 1), (3, 3)]))
    <MULTILINESTRING ((0 0, 1 1), (2 2, 3 3))>
    >>> box1 = shapely.box(0, 0, 2, 2)
    >>> box2 = shapely.box(1, 1, 3, 3)
    >>> shapely.symmetric_difference(box1, box2).normalize()
    <MULTIPOLYGON (((1 2, 1 3, 3 3, 3 1, 2 1, 2 2, 1 2)), ((0 0, 0 2, 1 2, 1 1, ...>
    >>> box1 = shapely.box(0.1, 0.2, 2.1, 2.1)
    >>> shapely.symmetric_difference(box1, box2, grid_size=1)
    <MULTIPOLYGON (((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0)), ((2 2, 1 2, 1 3, 3 3, ...>

    """

@overload
def symmetric_difference(a: None, b: Geometry | None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def symmetric_difference(a: Geometry | None, b: None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def symmetric_difference(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def symmetric_difference(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
@deprecated("symmetric_difference_all behaves incorrectly and will be removed in a future version.")
def symmetric_difference_all(geometries: OptGeoArrayLike, axis: None = None, **kwargs) -> BaseGeometry:
    """Return the symmetric difference of multiple geometries.

    This function ignores None values when other Geometry elements are present.
    If all elements of the given axis are None an empty GeometryCollection is
    returned.

    .. deprecated:: 2.1.0

        This function behaves incorrectly and will be removed in a future
        version. See https://github.com/shapely/shapely/issues/2027 for more
        details.

    Parameters
    ----------
    geometries : array_like
        Geometries to calculate the combined symmetric difference of.
    axis : int, optional
        Axis along which the operation is performed. The default (None)
        performs the operation over all axes, returning a scalar value.
        Axis may be negative, in which case it counts from the last to the
        first axis.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``axis`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    symmetric_difference

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line1 = LineString([(0, 0), (2, 2)])
    >>> line2 = LineString([(1, 1), (3, 3)])
    >>> shapely.symmetric_difference_all([line1, line2])
    <MULTILINESTRING ((0 0, 1 1), (2 2, 3 3))>
    >>> shapely.symmetric_difference_all([[line1, line2, None]], axis=1).tolist()
    [<MULTILINESTRING ((0 0, 1 1), (2 2, 3 3))>]
    >>> shapely.symmetric_difference_all([line1, None])
    <LINESTRING (0 0, 2 2)>
    >>> shapely.symmetric_difference_all([None, None])
    <GEOMETRYCOLLECTION EMPTY>

    """

@overload
@deprecated("symmetric_difference_all behaves incorrectly and will be removed in a future version.")
def symmetric_difference_all(geometries: OptGeoArrayLikeSeq, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...
@overload
def union(a: Geometry, b: Geometry, grid_size: float | None = None, **kwargs) -> BaseGeometry:
    """Merge geometries into one.

    If grid_size is nonzero, input coordinates will be snapped to a precision
    grid of that size and resulting coordinates will be snapped to that same
    grid.  If 0, this operation will use double precision coordinates.  If None,
    the highest precision of the inputs will be used, which may be previously
    set using set_precision.  Note: returned geometry does not have precision
    set unless specified previously by set_precision.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to merge (union).
    grid_size : float, optional
        Precision grid size; will use the highest precision of the inputs by default.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``grid_size`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    union_all
    set_precision

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString
    >>> line = LineString([(0, 0), (2, 2)])
    >>> shapely.union(line, LineString([(2, 2), (3, 3)]))
    <MULTILINESTRING ((0 0, 2 2), (2 2, 3 3))>
    >>> shapely.union(line, None) is None
    True
    >>> box1 = shapely.box(0, 0, 2, 2)
    >>> box2 = shapely.box(1, 1, 3, 3)
    >>> shapely.union(box1, box2).normalize()
    <POLYGON ((0 0, 0 2, 1 2, 1 3, 3 3, 3 1, 2 1, 2 0, 0 0))>
    >>> box1 = shapely.box(0.1, 0.2, 2.1, 2.1)
    >>> shapely.union(box1, box2, grid_size=1)
    <POLYGON ((2 0, 0 0, 0 2, 1 2, 1 3, 3 3, 3 1, 2 1, 2 0))>

    """

@overload
def union(a: None, b: Geometry | None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def union(a: Geometry | None, b: None, grid_size: float | None = None, **kwargs) -> None: ...
@overload
def union(a: OptGeoArrayLikeSeq, b: OptGeoArrayLike, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def union(a: OptGeoArrayLike, b: OptGeoArrayLikeSeq, grid_size: float | None = None, **kwargs) -> GeoArray: ...
@overload
def union_all(geometries: OptGeoArrayLike, grid_size: float | None = None, axis: None = None, **kwargs) -> BaseGeometry:
    """Return the union of multiple geometries.

    This function ignores None values when other Geometry elements are present.
    If all elements of the given axis are None an empty GeometryCollection is
    returned.

    If grid_size is nonzero, input coordinates will be snapped to a precision
    grid of that size and resulting coordinates will be snapped to that same
    grid.  If 0, this operation will use double precision coordinates.  If None,
    the highest precision of the inputs will be used, which may be previously
    set using set_precision.  Note: returned geometry does not have precision
    set unless specified previously by set_precision.

    `unary_union` is an alias of `union_all`.

    Parameters
    ----------
    geometries : array_like
        Geometries to merge/union.
    grid_size : float, optional
        Precision grid size; will use the highest precision of the inputs by default.
    axis : int, optional
        Axis along which the operation is performed. The default (None)
        performs the operation over all axes, returning a scalar value.
        Axis may be negative, in which case it counts from the last to the
        first axis.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``grid_size`` or ``axis`` are
        specified as positional arguments. In a future release, these will
        need to be specified as keyword arguments.

    See Also
    --------
    union
    set_precision

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> line1 = LineString([(0, 0), (2, 2)])
    >>> line2 = LineString([(2, 2), (3, 3)])
    >>> shapely.union_all([line1, line2])
    <MULTILINESTRING ((0 0, 2 2), (2 2, 3 3))>
    >>> shapely.union_all([[line1, line2, None]], axis=1).tolist()
    [<MULTILINESTRING ((0 0, 2 2), (2 2, 3 3))>]
    >>> box1 = shapely.box(0, 0, 2, 2)
    >>> box2 = shapely.box(1, 1, 3, 3)
    >>> shapely.union_all([box1, box2]).normalize()
    <POLYGON ((0 0, 0 2, 1 2, 1 3, 3 3, 3 1, 2 1, 2 0, 0 0))>
    >>> box1 = shapely.box(0.1, 0.2, 2.1, 2.1)
    >>> shapely.union_all([box1, box2], grid_size=1)
    <POLYGON ((2 0, 0 0, 0 2, 1 2, 1 3, 3 3, 3 1, 2 1, 2 0))>
    >>> shapely.union_all([None, Point(0, 1)])
    <POINT (0 1)>
    >>> shapely.union_all([None, None])
    <GEOMETRYCOLLECTION EMPTY>
    >>> shapely.union_all([])
    <GEOMETRYCOLLECTION EMPTY>

    """

@overload
def union_all(
    geometries: OptGeoArrayLikeSeq, grid_size: float | None = None, *, axis: int, **kwargs
) -> BaseGeometry | GeoArray: ...
@overload
def union_all(geometries: OptGeoArrayLikeSeq, grid_size: float | None, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...

unary_union = union_all

@overload
def coverage_union(a: OptGeoArrayLike, b: OptGeoArrayLike, *, axis: None = None, **kwargs) -> BaseGeometry:
    """Merge multiple polygons into one.

    This is an optimized version of union which assumes the polygons to be
    non-overlapping.

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to merge (union).
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    coverage_union_all

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> polygon_1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    >>> polygon_2 = Polygon([(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)])
    >>> shapely.coverage_union(polygon_1, polygon_2).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 2 1, 2 0, 1 0, 0 0))>

    Union with None returns same polygon

    >>> shapely.coverage_union(polygon_1, None).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))>

    """

@overload
def coverage_union(a: OptGeoArrayLike, b: OptGeoArrayLike, *, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...
@overload
def coverage_union_all(geometries: OptGeoArrayLike, axis: None = None, **kwargs) -> BaseGeometry:
    """Return the union of multiple polygons of a geometry collection.

    This is an optimized version of union which assumes the polygons
    to be non-overlapping.

    This function ignores None values when other Geometry elements are present.
    If all elements of the given axis are None, an empty GeometryCollection is
    returned (before GEOS 3.12 this was an empty MultiPolygon).

    Parameters
    ----------
    geometries : array_like
        Geometries to merge/union.
    axis : int, optional
        Axis along which the operation is performed. The default (None)
        performs the operation over all axes, returning a scalar value.
        Axis may be negative, in which case it counts from the last to the
        first axis.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``axis`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    coverage_union

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> polygon_1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    >>> polygon_2 = Polygon([(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)])
    >>> shapely.coverage_union_all([polygon_1, polygon_2]).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 2 1, 2 0, 1 0, 0 0))>
    >>> shapely.coverage_union_all([polygon_1, None]).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))>
    >>> shapely.coverage_union_all([None, None]).normalize()
    <GEOMETRYCOLLECTION EMPTY>

    """

@overload
def coverage_union_all(geometries: OptGeoArrayLikeSeq, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...
def disjoint_subset_union(a: OptGeoArrayLike, b: OptGeoArrayLike, **kwargs) -> BaseGeometry | GeoArray:
    """Merge multiple polygons into one using algorithm optimised for subsets.

    This is an optimized version of union which assumes inputs can be
    divided into subsets that do not intersect.

    If there is only one such subset, performance can be expected to be worse than
    :func:`union`. As such, it is recommeded to use ``disjoint_subset_union`` with
    GeometryCollections rather than individual geometries.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    a, b : Geometry or array_like
        Geometry or geometries to merge (union).
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    union
    coverage_union
    disjoint_subset_union_all

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> polygon_1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    >>> polygon_2 = Polygon([(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)])
    >>> shapely.disjoint_subset_union(polygon_1, polygon_2).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 2 1, 2 0, 1 0, 0 0))>

    Union with None returns same polygon:

    >>> shapely.disjoint_subset_union(polygon_1, None).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))>
    """

@overload
def disjoint_subset_union_all(geometries: OptGeoArrayLike, *, axis: None = None, **kwargs) -> BaseGeometry:
    """Return the union of multiple polygons.

    This is an optimized version of union which assumes inputs can be divided into
    subsets that do not intersect.

    If there is only one such subset, performance can be expected to be worse than
    :func:`union_all`.

    This function ignores None values when other Geometry elements are present.
    If all elements of the given axis are None, an empty GeometryCollection is
    returned.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    geometries : array_like
        Geometries to union.
    axis : int, optional
        Axis along which the operation is performed. The default (None)
        performs the operation over all axes, returning a scalar value.
        Axis may be negative, in which case it counts from the last to the
        first axis.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    coverage_union_all
    union_all
    disjoint_subset_union

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> polygon_1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    >>> polygon_2 = Polygon([(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)])
    >>> shapely.disjoint_subset_union_all([polygon_1, polygon_2]).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 2 1, 2 0, 1 0, 0 0))>
    >>> shapely.disjoint_subset_union_all([polygon_1, None]).normalize()
    <POLYGON ((0 0, 0 1, 1 1, 1 0, 0 0))>
    >>> shapely.disjoint_subset_union_all([None, None]).normalize()
    <GEOMETRYCOLLECTION EMPTY>
    """

@overload
def disjoint_subset_union_all(geometries: OptGeoArrayLikeSeq, *, axis: int, **kwargs) -> BaseGeometry | GeoArray: ...
