"""Methods that operate on the coordinates of geometries."""

from collections.abc import Callable
from typing import Literal, overload

import numpy as np
from numpy.typing import NDArray

from ._typing import ArrayLikeSeq, GeoArray, GeoT, OptGeoArrayLike, OptGeoArrayLikeSeq, OptGeoT

__all__ = ["transform", "count_coordinates", "get_coordinates", "set_coordinates"]

@overload
def transform(
    geometry: OptGeoT,
    transformation: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    include_z: bool = False,
    *,
    interleaved: bool = True,
) -> OptGeoT:
    """Apply a function to the coordinates of a geometry.

    With the default of ``include_z=False``, all returned geometries will be
    two-dimensional; the third dimension will be discarded, if present.
    When specifying ``include_z=True``, the returned geometries preserve
    the dimensionality of the respective input geometries.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to transform.
    transformation : function
        A function that transforms a (N, 2) or (N, 3) ndarray of float64 to
        another (N, 2) or (N, 3) ndarray of float64.
        The function may not change N.
    include_z : bool, optional, default False
        If False, always return 2D geometries.
        If True, the data being passed to the
        transformation function will include the third dimension
        (if a geometry has no third dimension, the z-coordinates
        will be NaN). If None, will infer the dimensionality per
        input geometry using ``has_z``, which may result in 2 calls to
        the transformation function. Note that this inference
        can be unreliable with empty geometries or NaN coordinates: for a
        guaranteed result, it is recommended to specify ``include_z`` explicitly.
    interleaved : bool, default True
        If set to False, the transformation function should accept 2 or 3 separate
        one-dimensional arrays (x, y and optional z) instead of a single
        two-dimensional array.

        .. versionadded:: 2.1.0

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``include_z`` is specified as a
        positional argument. This will need to be specified as a keyword
        argument in a future release.

    See Also
    --------
    has_z

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.transform(Point(0, 0), lambda x: x + 1)
    <POINT (1 1)>
    >>> shapely.transform(LineString([(2, 2), (4, 4)]), lambda x: x * [2, 3])
    <LINESTRING (4 6, 8 12)>
    >>> shapely.transform(None, lambda x: x) is None
    True
    >>> shapely.transform([Point(0, 0), None], lambda x: x).tolist()
    [<POINT (0 0)>, None]

    The presence of a third dimension can be automatically detected, or
    controlled explicitly:

    >>> shapely.transform(Point(0, 0, 0), lambda x: x + 1)
    <POINT (1 1)>
    >>> shapely.transform(Point(0, 0, 0), lambda x: x + 1, include_z=True)
    <POINT Z (1 1 1)>
    >>> shapely.transform(Point(0, 0, 0), lambda x: x + 1, include_z=None)
    <POINT Z (1 1 1)>

    With interleaved=False, the call signature of the transformation is different:

    >>> shapely.transform(LineString([(1, 2), (3, 4)]), lambda x, y: (x + 1, y), interleaved=False)
    <LINESTRING (2 2, 4 4)>

    Or with a z coordinate:

    >>> shapely.transform(Point(0, 0, 0), lambda x, y, z: (x + 1, y, z + 2), interleaved=False, include_z=True)
    <POINT Z (1 0 2)>

    Using pyproj >= 2.1, the following example will reproject Shapely geometries
    from EPSG 4326 to EPSG 32618:

    >>> from pyproj import Transformer
    >>> transformer = Transformer.from_crs(4326, 32618, always_xy=True)
    >>> shapely.transform(Point(-75, 50), transformer.transform, interleaved=False)
    <POINT (500000 5538630.703)>

    """

@overload
def transform(
    geometry: OptGeoArrayLikeSeq,
    transformation: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    include_z: bool = False,
    *,
    interleaved: bool = True,
) -> GeoArray: ...
def count_coordinates(geometry: OptGeoArrayLike) -> int:
    """Count the number of coordinate pairs in a geometry array.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to count the coordinates of.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.count_coordinates(Point(0, 0))
    1
    >>> shapely.count_coordinates(LineString([(2, 2), (4, 2)]))
    2
    >>> shapely.count_coordinates(None)
    0
    >>> shapely.count_coordinates([Point(0, 0), None])
    1

    """

@overload
def get_coordinates(
    geometry: OptGeoArrayLike, include_z: bool = False, return_index: Literal[False] = False, *, include_m: bool = False
) -> NDArray[np.float64]:
    """Get coordinates from a geometry array as an array of floats.

    The shape of the returned array is (N, 2), with N being the number of
    coordinate pairs. The shape of the data may also be (N, 3) or (N, 4),
    depending on ``include_z`` and ``include_m`` options.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to get the coordinates of.
    include_z, include_m : bool, default False
        If both are False, return XY (2D) geometries.
        If both are True, return XYZM (4D) geometries.
        If either are True, return XYZ or XYM (3D) geometries.
        If a geometry has no Z or M dimension, extra coordinate data will be NaN.

        .. versionadded:: 2.1.0
            The ``include_m`` parameter was added to support XYM (3D) and
            XYZM (4D) geometries available with GEOS 3.12.0 or later.
            With older GEOS versions, M dimension coordinates will be NaN.

    return_index : bool, default False
        If True, also return the index of each returned geometry as a separate
        ndarray of integers. For multidimensional arrays, this indexes into the
        flattened array (in C contiguous order).

    Notes
    -----

    .. deprecated:: 2.1.0
        A deprecation warning is shown if ``include_z`` or ``return_index`` are
        specified as positional arguments. In a future release, these will
        need to be specified as keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.get_coordinates(Point(1, 2)).tolist()
    [[1.0, 2.0]]
    >>> shapely.get_coordinates(LineString([(2, 2), (4, 4)])).tolist()
    [[2.0, 2.0], [4.0, 4.0]]
    >>> shapely.get_coordinates(None)
    array([], shape=(0, 2), dtype=float64)

    By default the third dimension is ignored:

    >>> shapely.get_coordinates(Point(1, 2, 3)).tolist()
    [[1.0, 2.0]]
    >>> shapely.get_coordinates(Point(1, 2, 3), include_z=True).tolist()
    [[1.0, 2.0, 3.0]]

    If geometries don't have Z or M dimension, these values will be NaN:

    >>> pt = Point(1, 2)
    >>> shapely.get_coordinates(pt, include_z=True).tolist()
    [[1.0, 2.0, nan]]
    >>> shapely.get_coordinates(pt, include_z=True, include_m=True).tolist()
    [[1.0, 2.0, nan, nan]]

    When ``return_index=True``, indexes are returned also:

    >>> geometries = [LineString([(2, 2), (4, 4)]), Point(0, 0)]
    >>> coordinates, index = shapely.get_coordinates(geometries, return_index=True)
    >>> coordinates.tolist(), index.tolist()
    ([[2.0, 2.0], [4.0, 4.0], [0.0, 0.0]], [0, 0, 1])

    """

@overload
def get_coordinates(
    geometry: OptGeoArrayLike, include_z: bool = False, *, return_index: Literal[True], include_m: bool = False
) -> tuple[NDArray[np.float64], NDArray[np.int64]]: ...
@overload
def get_coordinates(
    geometry: OptGeoArrayLike, include_z: bool, return_index: Literal[True], *, include_m: bool = False
) -> tuple[NDArray[np.float64], NDArray[np.int64]]: ...
@overload
def get_coordinates(
    geometry: OptGeoArrayLike, include_z: bool = False, *, return_index: bool, include_m: bool = False
) -> NDArray[np.float64] | tuple[NDArray[np.float64], NDArray[np.int64]]: ...
@overload
def get_coordinates(
    geometry: OptGeoArrayLike, include_z: bool, return_index: bool, *, include_m: bool = False
) -> NDArray[np.float64] | tuple[NDArray[np.float64], NDArray[np.int64]]: ...
@overload
def set_coordinates(geometry: GeoT, coordinates: ArrayLikeSeq[float]) -> GeoT:
    """Adapts the coordinates of a geometry array in-place.

    If the coordinates array has shape (N, 2), all returned geometries
    will be two-dimensional, and the third dimension will be discarded,
    if present. If the coordinates array has shape (N, 3), the returned
    geometries preserve the dimensionality of the input geometries.

    .. warning::

        The geometry array is modified in-place! If you do not want to
        modify the original array, you can do
        ``set_coordinates(arr.copy(), newcoords)``.

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to set the coordinates of.
    coordinates: array_like
        An array of coordinates to set.

    See Also
    --------
    transform : Returns a copy of a geometry array with a function applied to its
        coordinates.

    Examples
    --------
    >>> import shapely
    >>> from shapely import LineString, Point
    >>> shapely.set_coordinates(Point(0, 0), [[1, 1]])
    <POINT (1 1)>
    >>> shapely.set_coordinates(
    ...     [Point(0, 0), LineString([(0, 0), (0, 0)])],
    ...     [[1, 2], [3, 4], [5, 6]]
    ... ).tolist()
    [<POINT (1 2)>, <LINESTRING (3 4, 5 6)>]
    >>> shapely.set_coordinates([None, Point(0, 0)], [[1, 2]]).tolist()
    [None, <POINT (1 2)>]

    Third dimension of input geometry is discarded if coordinates array does
    not include one:

    >>> shapely.set_coordinates(Point(0, 0, 0), [[1, 1]])
    <POINT (1 1)>
    >>> shapely.set_coordinates(Point(0, 0, 0), [[1, 1, 1]])
    <POINT Z (1 1 1)>

    """

@overload
def set_coordinates(geometry: OptGeoArrayLikeSeq, coordinates: ArrayLikeSeq[float]) -> GeoArray: ...
