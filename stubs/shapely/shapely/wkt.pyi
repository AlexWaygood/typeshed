"""Load/dump geometries using the well-known text (WKT) format.

Also provides pickle-like convenience functions.
"""

from ._typing import SupportsRead, SupportsWrite
from .geometry.base import BaseGeometry
from .lib import Geometry

def loads(data: str) -> BaseGeometry:
    """Load a geometry from a WKT string.

    Parameters
    ----------
    data : str
        A WKT string

    Returns
    -------
    Shapely geometry object

    """

def load(fp: SupportsRead[str]) -> BaseGeometry:
    """Load a geometry from an open file.

    Parameters
    ----------
    fp :
        A file-like object which implements a `read` method.

    Returns
    -------
    Shapely geometry object

    """

def dumps(ob: Geometry, trim: bool = False, rounding_precision: int = -1, **kw) -> str:
    """Dump a WKT representation of a geometry to a string.

    Parameters
    ----------
    ob :
        A geometry object of any type to be dumped to WKT.
    trim : bool, default False
        Remove excess decimals from the WKT.
    rounding_precision : int, default -1
        Round output to the specified number of digits.
        Default behavior returns full precision.
    **kw : kwargs, optional
        Keyword output options passed to :func:`~shapely.to_wkt`.

    Returns
    -------
    input geometry as WKT string

    """

def dump(ob: Geometry, fp: SupportsWrite[str], *, trim: bool = False, rounding_precision: int = -1, **kw) -> None:
    """Dump a geometry to an open file.

    Parameters
    ----------
    ob :
        A geometry object of any type to be dumped to WKT.
    fp :
        A file-like object which implements a `write` method.
    **settings : kwargs, optional
        Keyword output options passed to :func:`~shapely.wkt.dumps`.

    Returns
    -------
    None

    """
