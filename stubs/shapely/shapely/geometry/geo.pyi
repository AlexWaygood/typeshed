"""Geometry factories based on the geo interface."""

from typing import Any

from .._typing import SupportsGeoInterface
from .base import BaseGeometry
from .polygon import Polygon

def box(minx: float, miny: float, maxx: float, maxy: float, ccw: bool = True) -> Polygon:
    """Return a rectangular polygon with configurable normal vector."""

def shape(context: dict[str, Any] | SupportsGeoInterface) -> BaseGeometry:
    """Return a new, independent geometry with coordinates copied from the context.

    Changes to the original context will not be reflected in the geometry
    object.

    Parameters
    ----------
    context :
        a GeoJSON-like dict, which provides a "type" member describing the type
        of the geometry and "coordinates" member providing a list of coordinates,
        or an object which implements __geo_interface__.

    Returns
    -------
    Geometry object

    Examples
    --------
    Create a Point from GeoJSON, and then create a copy using __geo_interface__.

    >>> from shapely.geometry import shape
    >>> context = {'type': 'Point', 'coordinates': [0, 1]}
    >>> geom = shape(context)
    >>> geom.geom_type == 'Point'
    True
    >>> geom.wkt
    'POINT (0 1)'
    >>> geom2 = shape(geom)
    >>> geom == geom2
    True

    """

def mapping(ob: SupportsGeoInterface) -> dict[str, Any]:
    """Return a GeoJSON-like mapping.

    Input should be a Geometry or an object which implements __geo_interface__.

    Parameters
    ----------
    ob : geometry or object
        An object which implements __geo_interface__.

    Returns
    -------
    dict

    Examples
    --------
    >>> from shapely.geometry import mapping, Point
    >>> pt = Point(0, 0)
    >>> mapping(pt)
    {'type': 'Point', 'coordinates': (0.0, 0.0)}

    """
