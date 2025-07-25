"""Provides multi-point element-wise operations such as ``contains``."""

from typing import overload
from typing_extensions import deprecated

import numpy as np
from numpy.typing import NDArray

from .._typing import ArrayLike, ArrayLikeSeq
from ..lib import Geometry
from ..prepared import PreparedGeometry

@overload
@deprecated("Use 'shapely.contains_xy' instead (available since shapely 2.0.0).")
def contains(geometry: Geometry | PreparedGeometry[Geometry], x: float, y: float) -> np.bool_:
    """Check whether multiple points are contained by a single geometry.

    Vectorized (element-wise) version of `contains`.

    Parameters
    ----------
    geometry : PreparedGeometry or subclass of BaseGeometry
        The geometry which is to be checked to see whether each point is
        contained within. The geometry will be "prepared" if it is not already
        a PreparedGeometry instance.
    x : array
        The x coordinates of the points to check.
    y : array
        The y coordinates of the points to check.

    Returns
    -------
    Mask of points contained by the given `geometry`.

    """

@overload
@deprecated("Use 'shapely.contains_xy' instead (available since shapely 2.0.0).")
def contains(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLikeSeq[float], y: ArrayLike[float]
) -> NDArray[np.bool_]: ...
@overload
@deprecated("Use 'shapely.contains_xy' instead (available since shapely 2.0.0).")
def contains(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLike[float], y: ArrayLikeSeq[float]
) -> NDArray[np.bool_]: ...
@overload
@deprecated("Use 'shapely.contains_xy' instead (available since shapely 2.0.0).")
def contains(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLike[float], y: ArrayLike[float]
) -> np.bool_ | NDArray[np.bool_]: ...
@overload
@deprecated("Use 'shapely.intersects_xy' instead (available since shapely 2.0.0).")
def touches(geometry: Geometry | PreparedGeometry[Geometry], x: float, y: float) -> np.bool_:
    """Check whether multiple points touch the exterior of a single geometry.

    Vectorized (element-wise) version of `touches`.

    Parameters
    ----------
    geometry : PreparedGeometry or subclass of BaseGeometry
        The geometry which is to be checked to see whether each point is
        contained within. The geometry will be "prepared" if it is not already
        a PreparedGeometry instance.
    x : array
        The x coordinates of the points to check.
    y : array
        The y coordinates of the points to check.

    Returns
    -------
    Mask of points which touch the exterior of the given `geometry`.

    """

@overload
@deprecated("Use 'shapely.intersects_xy' instead (available since shapely 2.0.0).")
def touches(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLikeSeq[float], y: ArrayLike[float]
) -> NDArray[np.bool_]: ...
@overload
@deprecated("Use 'shapely.intersects_xy' instead (available since shapely 2.0.0).")
def touches(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLike[float], y: ArrayLikeSeq[float]
) -> NDArray[np.bool_]: ...
@overload
@deprecated("Use 'shapely.intersects_xy' instead (available since shapely 2.0.0).")
def touches(
    geometry: Geometry | PreparedGeometry[Geometry], x: ArrayLike[float], y: ArrayLike[float]
) -> np.bool_ | NDArray[np.bool_]: ...
