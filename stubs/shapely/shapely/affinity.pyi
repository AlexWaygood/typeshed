"""Affine transforms, both in general and specific, named transforms."""

from collections.abc import Collection
from typing import Literal, overload
from typing_extensions import TypeAlias

from ._typing import GeoT
from .geometry import Point
from .lib import Geometry

__all__ = ["affine_transform", "rotate", "scale", "skew", "translate"]

_Origin: TypeAlias = Literal["center", "centroid"] | Point | tuple[float, float] | tuple[float, float, float]

def affine_transform(geom: GeoT, matrix: Collection[float]) -> GeoT:
    """Return a transformed geometry using an affine transformation matrix.

    The coefficient matrix is provided as a list or tuple with 6 or 12 items
    for 2D or 3D transformations, respectively.

    For 2D affine transformations, the 6 parameter matrix is::

        [a, b, d, e, xoff, yoff]

    which represents the augmented matrix::

        [x']   / a  b xoff \\ [x]
        [y'] = | d  e yoff | [y]
        [1 ]   \\ 0  0   1  / [1]

    or the equations for the transformed coordinates::

        x' = a * x + b * y + xoff
        y' = d * x + e * y + yoff

    For 3D affine transformations, the 12 parameter matrix is::

        [a, b, c, d, e, f, g, h, i, xoff, yoff, zoff]

    which represents the augmented matrix::

        [x']   / a  b  c xoff \\ [x]
        [y'] = | d  e  f yoff | [y]
        [z']   | g  h  i zoff | [z]
        [1 ]   \\ 0  0  0   1  / [1]

    or the equations for the transformed coordinates::

        x' = a * x + b * y + c * z + xoff
        y' = d * x + e * y + f * z + yoff
        z' = g * x + h * y + i * z + zoff
    """

@overload
def interpret_origin(geom: Geometry, origin: _Origin, ndim: Literal[2]) -> tuple[float, float]:
    """Return interpreted coordinate tuple for origin parameter.

    This is a helper function for other transform functions.

    The point of origin can be a keyword 'center' for the 2D bounding box
    center, 'centroid' for the geometry's 2D centroid, a Point object or a
    coordinate tuple (x0, y0, z0).
    """

@overload
def interpret_origin(geom: Geometry, origin: _Origin, ndim: Literal[3]) -> tuple[float, float, float]: ...
@overload
def interpret_origin(geom: Geometry, origin: _Origin, ndim: int) -> tuple[float, float] | tuple[float, float, float]: ...
def rotate(geom: GeoT, angle: float, origin: _Origin = "center", use_radians: bool = False) -> GeoT:
    """Return a rotated geometry on a 2D plane.

The angle of rotation can be specified in either degrees (default) or
radians by setting ``use_radians=True``. Positive angles are
counter-clockwise and negative are clockwise rotations.

The point of origin can be a keyword 'center' for the bounding box
center (default), 'centroid' for the geometry's centroid, a Point object
or a coordinate tuple (x0, y0).

The affine transformation matrix for 2D rotation is:

  / cos(r) -sin(r) xoff \\
  | sin(r)  cos(r) yoff |
  \\   0       0      1  /

where the offsets are calculated from the origin Point(x0, y0):

    xoff = x0 - x0 * cos(r) + y0 * sin(r)
    yoff = y0 - x0 * sin(r) - y0 * cos(r)
"""

def scale(geom: GeoT, xfact: float = 1.0, yfact: float = 1.0, zfact: float = 1.0, origin: _Origin = "center") -> GeoT:
    """Return a scaled geometry, scaled by factors along each dimension.

The point of origin can be a keyword 'center' for the 2D bounding box
center (default), 'centroid' for the geometry's 2D centroid, a Point
object or a coordinate tuple (x0, y0, z0).

Negative scale factors will mirror or reflect coordinates.

The general 3D affine transformation matrix for scaling is:

    / xfact  0    0   xoff \\
    |   0  yfact  0   yoff |
    |   0    0  zfact zoff |
    \\   0    0    0     1  /

where the offsets are calculated from the origin Point(x0, y0, z0):

    xoff = x0 - x0 * xfact
    yoff = y0 - y0 * yfact
    zoff = z0 - z0 * zfact
"""

def skew(geom: GeoT, xs: float = 0.0, ys: float = 0.0, origin: _Origin = "center", use_radians: bool = False) -> GeoT:
    """Return a skewed geometry, sheared by angles along x and y dimensions.

The shear angle can be specified in either degrees (default) or radians
by setting ``use_radians=True``.

The point of origin can be a keyword 'center' for the bounding box
center (default), 'centroid' for the geometry's centroid, a Point object
or a coordinate tuple (x0, y0).

The general 2D affine transformation matrix for skewing is:

    /   1    tan(xs) xoff \\
    | tan(ys)  1     yoff |
    \\   0      0       1  /

where the offsets are calculated from the origin Point(x0, y0):

    xoff = -y0 * tan(xs)
    yoff = -x0 * tan(ys)
"""

def translate(geom: GeoT, xoff: float = 0.0, yoff: float = 0.0, zoff: float = 0.0) -> GeoT:
    """Return a translated geometry shifted by offsets along each dimension.

The general 3D affine transformation matrix for translation is:

    / 1  0  0 xoff \\
    | 0  1  0 yoff |
    | 0  0  1 zoff |
    \\ 0  0  0   1  /
"""
