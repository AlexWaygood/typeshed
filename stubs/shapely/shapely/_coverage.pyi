from typing import overload

import numpy as np

from ._typing import ArrayLike, GeoArray, GeoArrayLikeSeq, OptGeoArrayLike
from .geometry import Polygon

__all__ = ["coverage_invalid_edges", "coverage_is_valid", "coverage_simplify"]

def coverage_is_valid(geometry: OptGeoArrayLike, gap_width: float = 0.0, **kwargs) -> np.bool_:
    """Verify if a coverage is valid.

    The coverage is represented by an array of polygonal geometries with
    exactly matching edges and no overlap.

    A valid coverage may contain holes (regions of no coverage). However,
    sometimes it might be desirable to detect narrow gaps as invalidities in
    the coverage. The `gap_width` parameter allows to specify the maximum
    width of gaps to detect. When gaps are detected, this function will
    return False and the `coverage_invalid_edges` function can be used to
    find the edges of those gaps.

    Geometries that are not Polygon or MultiPolygon are ignored.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    geometry : array_like
        Array of geometries to verify.
    gap_width : float, default 0.0
        The maximum width of gaps to detect.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Returns
    -------
    bool

    See Also
    --------
    coverage_invalid_edges, coverage_simplify

    """

def coverage_invalid_edges(geometry: OptGeoArrayLike, gap_width: float = 0.0, **kwargs) -> GeoArray:
    """Verify if a coverage is valid and return invalid edges.

    This functions returns linear indicators showing the location of invalid
    edges (if any) in each polygon in the input array.

    The coverage is represented by an array of polygonal geometries with
    exactly matching edges and no overlap.

    A valid coverage may contain holes (regions of no coverage). However,
    sometimes it might be desirable to detect narrow gaps as invalidities in
    the coverage. The `gap_width` parameter allows to specify the maximum
    width of gaps to detect. When gaps are detected, the `coverage_is_valid`
    function will return False and this function can be used to find the
    edges of those gaps.

    Geometries that are not Polygon or MultiPolygon are ignored.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    geometry : array_like
        Array of geometries to verify.
    gap_width : float, default 0.0
        The maximum width of gaps to detect.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Returns
    -------
    numpy.ndarray | shapely.Geometry

    See Also
    --------
    coverage_is_valid, coverage_simplify

    """

@overload
def coverage_simplify(geometry: Polygon, tolerance: ArrayLike[float], *, simplify_boundary: bool = True) -> Polygon:
    """Return a simplified version of an input geometry using coverage simplification.

    Assumes that the geometry forms a polygonal coverage. Under this assumption, the
    function simplifies the edges using the Visvalingam-Whyatt algorithm, while
    preserving a valid coverage. In the most simplified case, polygons are reduced to
    triangles.

    A collection of valid polygons is considered a coverage if the polygons are:

    * **Non-overlapping** - polygons do not overlap (their interiors do not intersect)
    * **Edge-Matched** - vertices along shared edges are identical

    The function allows simplification of all edges including the outer boundaries of
    the coverage or simplification of only the inner (shared) edges.

    If there are other geometry types than Polygons or MultiPolygons present,
    the function will raise an error.

    If the geometry is polygonal but does not form a valid coverage due to overlaps,
    it will be simplified but it may result in invalid topology.

    .. versionadded:: 2.1.0

    Parameters
    ----------
    geometry : Geometry or array_like
    tolerance : float or array_like
        The degree of simplification roughly equal to the square root of the area
        of triangles that will be removed.
    simplify_boundary : bool, optional
        By default (True), simplifies both internal edges of the coverage as well
        as its boundary. If set to False, only simplifies internal edges.

    Returns
    -------
    numpy.ndarray | shapely.Geometry

    See Also
    --------
    coverage_is_valid, coverage_invalid_edges

    Examples
    --------
    >>> import shapely
    >>> from shapely import Polygon
    >>> poly = Polygon([(0, 0), (20, 0), (20, 10), (10, 5), (0, 10), (0, 0)])
    >>> shapely.coverage_simplify(poly, tolerance=2)
    <POLYGON ((0 0, 20 0, 20 10, 10 5, 0 10, 0 0))>
    """

@overload
def coverage_simplify(geometry: GeoArrayLikeSeq, tolerance: ArrayLike[float], *, simplify_boundary: bool = True) -> GeoArray: ...
