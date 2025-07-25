"""Validate geometries and make them valid."""

from .geometry.base import BaseGeometry
from .lib import Geometry

__all__ = ["explain_validity", "make_valid"]

def explain_validity(ob: Geometry) -> str:
    """Explain the validity of the input geometry, if it is invalid.

    This will describe why the geometry is invalid, and might
    include a location if there is a self-intersection or a
    ring self-intersection.

    Parameters
    ----------
    ob: Geometry
        A shapely geometry object

    Returns
    -------
    str
        A string describing the reason the geometry is invalid.

    """

def make_valid(ob: Geometry) -> BaseGeometry:
    """Make the input geometry valid according to the GEOS MakeValid algorithm.

    If the input geometry is already valid, then it will be returned.

    If the geometry must be split into multiple parts of the same type to be
    made valid, then a multi-part geometry will be returned.

    If the geometry must be split into multiple parts of different types to be
    made valid, then a GeometryCollection will be returned.

    Parameters
    ----------
    ob : Geometry
        A shapely geometry object which should be made valid. If the object is
        already valid, it will be returned as-is.

    Returns
    -------
    Geometry
        The input geometry, made valid according to the GEOS MakeValid algorithm.

    """
