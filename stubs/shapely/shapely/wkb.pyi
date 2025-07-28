"""Load/dump geometries using the well-known binary (WKB) format.

Also provides pickle-like convenience functions.
"""

from typing import Literal, overload

from ._typing import SupportsRead, SupportsWrite
from .geometry.base import BaseGeometry
from .lib import Geometry

def loads(data: str | bytes, hex: bool = False) -> BaseGeometry:
    """Load a geometry from a WKB byte string.

    If ``hex=True``, the string will be hex-encoded.

    Raises
    ------
    GEOSException, UnicodeDecodeError
        If ``data`` contains an invalid geometry.

    """

def load(fp: SupportsRead[str] | SupportsRead[bytes], hex: bool = False) -> BaseGeometry:
    """Load a geometry from an open file.

    Raises
    ------
    GEOSException, UnicodeDecodeError
        If the given file contains an invalid geometry.

    """

@overload
def dumps(ob: Geometry, hex: Literal[False] = False, srid: int | None = None, **kw) -> bytes:
    """Dump a WKB representation of a geometry to a byte string.

    If ``hex=True``, the string will be hex-encoded.

    Parameters
    ----------
    ob : geometry
        The geometry to export to well-known binary (WKB) representation.
    hex : bool
        If true, export the WKB as a hexadecimal string. The default is to
        return a binary string/bytes object.
    srid : int
        Spatial reference system ID to include in the output. The default value
        means no SRID is included.
    **kw : kwargs, optional
        Keyword output options passed to :func:`~shapely.to_wkb`.

    """

@overload
def dumps(ob: Geometry, hex: Literal[True], srid: int | None = None, **kw) -> str: ...
@overload
def dump(ob: Geometry, fp: SupportsWrite[bytes], hex: Literal[False] = False, *, srid: int | None = None, **kw) -> None:
    """Dump a geometry to an open file."""

@overload
def dump(ob: Geometry, fp: SupportsWrite[str], hex: Literal[True], *, srid: int | None = None, **kw) -> None: ...
