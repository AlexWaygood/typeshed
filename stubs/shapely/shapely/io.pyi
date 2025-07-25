"""Input/output functions for Shapely geometries."""

from _typeshed import Incomplete
from typing import Literal, overload
from typing_extensions import TypeAlias

import numpy as np
from numpy.typing import NDArray

from ._enum import ParamEnum
from ._ragged_array import from_ragged_array as from_ragged_array, to_ragged_array as to_ragged_array
from ._typing import ArrayLikeSeq, GeoArray, OptGeoArrayLikeSeq
from .geometry.base import BaseGeometry
from .lib import Geometry

__all__ = ["from_geojson", "from_ragged_array", "from_wkb", "from_wkt", "to_geojson", "to_ragged_array", "to_wkb", "to_wkt"]

_OutputDimension: TypeAlias = Literal[2, 3, 4]

# Mypy and stubtest aren't happy with the following definition and
# raise is a reserved keyword, so we cannot use the class syntax of enums
# DecodingErrorOptions = ParamEnum("DecodingErrorOptions", {"ignore": 0, "warn": 1, "raise": 2, "fix": 3})
DecodingErrorOptions: Incomplete

class WKBFlavorOptions(ParamEnum):
    extended = 1
    iso = 2

@overload
def to_wkt(
    geometry: None,
    rounding_precision: int = 6,
    trim: bool = True,
    output_dimension: _OutputDimension | None = None,
    old_3d: bool = False,
    **kwargs,
) -> None:
    """Convert to the Well-Known Text (WKT) representation of a Geometry.

    The Well-known Text format is defined in the `OGC Simple Features
    Specification for SQL <https://www.opengeospatial.org/standards/sfs>`__.

    The following limitations apply to WKT serialization:

    - only simple empty geometries can be 3D, empty collections are always 2D

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to convert to WKT.
    rounding_precision : int, default 6
        The rounding precision when writing the WKT string. Set to a value of
        -1 to indicate the full precision.
    trim : bool, default True
        If True, trim unnecessary decimals (trailing zeros). If False,
        use fixed-precision number formatting.
    output_dimension : int, default None
        The output dimension for the WKT string. Supported values are 2, 3 and
        4 for GEOS 3.12+. Default None will automatically choose 3 or 4,
        depending on the version of GEOS.
        Specifying 3 means that up to 3 dimensions will be written but 2D
        geometries will still be represented as 2D in the WKT string.
    old_3d : bool, default False
        Enable old style 3D/4D WKT generation. By default, new style 3D/4D WKT
        (ie. "POINT Z (10 20 30)") is returned, but with ``old_3d=True``
        the WKT will be formatted in the style "POINT (10 20 30)".
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> shapely.to_wkt(Point(0, 0))
    'POINT (0 0)'
    >>> shapely.to_wkt(Point(0, 0), rounding_precision=3, trim=False)
    'POINT (0.000 0.000)'
    >>> shapely.to_wkt(Point(0, 0), rounding_precision=-1, trim=False)
    'POINT (0.0000000000000000 0.0000000000000000)'
    >>> shapely.to_wkt(Point(1, 2, 3), trim=True)
    'POINT Z (1 2 3)'
    >>> shapely.to_wkt(Point(1, 2, 3), trim=True, output_dimension=2)
    'POINT (1 2)'
    >>> shapely.to_wkt(Point(1, 2, 3), trim=True, old_3d=True)
    'POINT (1 2 3)'

    Notes
    -----
    The defaults differ from the default of some GEOS versions. To mimic this for
    versions before GEOS 3.12, use::

        shapely.to_wkt(geometry, rounding_precision=-1, trim=False, output_dimension=2)

    """

@overload
def to_wkt(
    geometry: Geometry,
    rounding_precision: int = 6,
    trim: bool = True,
    output_dimension: _OutputDimension | None = None,
    old_3d: bool = False,
    **kwargs,
) -> str: ...
@overload
def to_wkt(
    geometry: OptGeoArrayLikeSeq,
    rounding_precision: int = 6,
    trim: bool = True,
    output_dimension: _OutputDimension | None = None,
    old_3d: bool = False,
    **kwargs,
) -> NDArray[np.str_]: ...
@overload
def to_wkb(
    geometry: None,
    hex: bool = False,
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> None:
    """Convert to the Well-Known Binary (WKB) representation of a Geometry.

    The Well-Known Binary format is defined in the `OGC Simple Features
    Specification for SQL <https://www.opengeospatial.org/standards/sfs>`__.

    The following limitations apply to WKB serialization:

    - linearrings will be converted to linestrings
    - a point with only NaN coordinates is converted to an empty point

    Parameters
    ----------
    geometry : Geometry or array_like
        Geometry or geometries to convert to WKB.
    hex : bool, default False
        If true, export the WKB as a hexadecimal string. The default is to
        return a binary bytes object.
    output_dimension : int, default None
        The output dimension for the WKB. Supported values are 2, 3 and 4 for
        GEOS 3.12+. Default None will automatically choose 3 or 4, depending on
        the version of GEOS.
        Specifying 3 means that up to 3 dimensions will be written but 2D
        geometries will still be represented as 2D in the WKB representation.
    byte_order : int, default -1
        Defaults to native machine byte order (-1). Use 0 to force big endian
        and 1 for little endian.
    include_srid : bool, default False
        If True, the SRID is be included in WKB (this is an extension
        to the OGC WKB specification). Not allowed when flavor is "iso".
    flavor : {"iso", "extended"}, default "extended"
        Which flavor of WKB will be returned. The flavor determines how
        extra dimensionality is encoded with the type number, and whether
        SRID can be included in the WKB. ISO flavor is "more standard" for
        3D output, and does not support SRID embedding.
        Both flavors are equivalent when ``output_dimension=2`` (or with 2D
        geometries) and ``include_srid=False``.
        The `from_wkb` function can read both flavors.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> point = Point(1, 1)
    >>> shapely.to_wkb(point, byte_order=1)
    b'\\x01\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?'
    >>> shapely.to_wkb(point, hex=True, byte_order=1)
    '0101000000000000000000F03F000000000000F03F'

    """

@overload
def to_wkb(
    geometry: Geometry,
    hex: Literal[False] = False,
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> bytes: ...
@overload
def to_wkb(
    geometry: Geometry,
    hex: Literal[True],
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> str: ...
@overload
def to_wkb(
    geometry: Geometry,
    hex: bool,
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> bytes | str: ...
@overload
def to_wkb(
    geometry: OptGeoArrayLikeSeq,
    hex: Literal[False] = False,
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> NDArray[np.bytes_]: ...
@overload
def to_wkb(
    geometry: OptGeoArrayLikeSeq,
    hex: Literal[True],
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> NDArray[np.str_]: ...
@overload
def to_wkb(
    geometry: OptGeoArrayLikeSeq,
    hex: bool,
    output_dimension: _OutputDimension | None = None,
    byte_order: int = -1,
    include_srid: bool = False,
    flavor: Literal["iso", "extended"] = "extended",
    **kwargs,
) -> NDArray[np.bytes_] | NDArray[np.str_]: ...
@overload
def to_geojson(geometry: None, indent: int | None = None, **kwargs) -> None:
    """Convert to the GeoJSON representation of a Geometry.

    The GeoJSON format is defined in the `RFC 7946 <https://geojson.org/>`__.
    NaN (not-a-number) coordinates will be written as 'null'.

    The following are currently unsupported:

    - Geometries of type LINEARRING: these are output as 'null'.
    - Three-dimensional geometries: the third dimension is ignored.

    Parameters
    ----------
    geometry : str, bytes or array_like
        Geometry or geometries to convert to GeoJSON.
    indent : int, optional
        If indent is a non-negative integer, then GeoJSON will be formatted.
        An indent level of 0 will only insert newlines. None (the default)
        selects the most compact representation.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> from shapely import Point
    >>> point = Point(1, 1)
    >>> shapely.to_geojson(point)
    '{"type":"Point","coordinates":[1.0,1.0]}'
    >>> print(shapely.to_geojson(point, indent=2))
    {
      "type": "Point",
      "coordinates": [
          1.0,
          1.0
      ]
    }

    """

@overload
def to_geojson(geometry: Geometry, indent: int | None = None, **kwargs) -> str: ...
@overload
def to_geojson(geometry: OptGeoArrayLikeSeq, indent: int | None = None, **kwargs) -> NDArray[np.str_]: ...
@overload
def from_wkt(geometry: None, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs) -> None:
    """Create geometries from the Well-Known Text (WKT) representation.

    The Well-known Text format is defined in the `OGC Simple Features
    Specification for SQL <https://www.opengeospatial.org/standards/sfs>`__.

    Parameters
    ----------
    geometry : str or array_like
        The WKT string(s) to convert.
    on_invalid : {"raise", "warn", "ignore", "fix"}, default "raise"
        Indicates what to do when an invalid WKT string is encountered. Note
        that the validations involved are very basic, e.g. the minimum number of
        points for the geometry type. For a thorough check, use
        :func:`is_valid` after conversion to geometries. Valid options are:

        - raise: an exception will be raised if any input geometry is invalid.
        - warn: a warning will be raised and invalid WKT geometries will be
          returned as ``None``.
        - ignore: invalid geometries will be returned as ``None`` without a
          warning.
        - fix: an effort is made to fix invalid input geometries (currently just
          unclosed rings). If this is not possible, they are returned as
          ``None`` without a warning. Requires GEOS >= 3.11.

          .. versionadded:: 2.1.0
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> shapely.from_wkt('POINT (0 0)')
    <POINT (0 0)>

    """

@overload
def from_wkt(geometry: str, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs) -> BaseGeometry: ...  # type: ignore[overload-overlap]
@overload
def from_wkt(
    geometry: ArrayLikeSeq[str | None], on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs
) -> GeoArray: ...
@overload
def from_wkb(geometry: None, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs) -> None:
    """Create geometries from the Well-Known Binary (WKB) representation.

    The Well-Known Binary format is defined in the `OGC Simple Features
    Specification for SQL <https://www.opengeospatial.org/standards/sfs>`__.

    Parameters
    ----------
    geometry : str or array_like
        The WKB byte object(s) to convert.
    on_invalid : {"raise", "warn", "ignore", "fix"}, default "raise"
        Indicates what to do when an invalid WKB is encountered. Note that the
        validations involved are very basic, e.g. the minimum number of points
        for the geometry type. For a thorough check, use :func:`is_valid` after
        conversion to geometries. Valid options are:

        - raise: an exception will be raised if any input geometry is invalid.
        - warn: a warning will be raised and invalid WKT geometries will be
          returned as ``None``.
        - ignore: invalid geometries will be returned as ``None`` without a
          warning.
        - fix: an effort is made to fix invalid input geometries (currently just
          unclosed rings). If this is not possible, they are returned as
          ``None`` without a warning. Requires GEOS >= 3.11.

          .. versionadded:: 2.1.0
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    Examples
    --------
    >>> import shapely
    >>> shapely.from_wkb(b'\\x01\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?')
    <POINT (1 1)>

    """

@overload
def from_wkb(
    geometry: str | bytes, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs
) -> BaseGeometry: ...  # type: ignore[overload-overlap]
@overload
def from_wkb(
    geometry: ArrayLikeSeq[str | bytes | None], on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs
) -> GeoArray: ...
@overload
def from_geojson(geometry: None, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs) -> None:
    """Create geometries from GeoJSON representations (strings).

    If a GeoJSON is a FeatureCollection, it is read as a single geometry
    (with type GEOMETRYCOLLECTION). This may be unpacked using
    :meth:`shapely.get_parts`. Properties are not read.

    The GeoJSON format is defined in `RFC 7946 <https://geojson.org/>`__.

    The following are currently unsupported:

    - Three-dimensional geometries: the third dimension is ignored.
    - Geometries having 'null' in the coordinates.

    Parameters
    ----------
    geometry : str, bytes or array_like
        The GeoJSON string or byte object(s) to convert.
    on_invalid : {"raise", "warn", "ignore"}, default "raise"
        - raise: an exception will be raised if an input GeoJSON is invalid.
        - warn: a warning will be raised and invalid input geometries will be
          returned as ``None``.
        - ignore: invalid input geometries will be returned as ``None`` without
          a warning.
    **kwargs
        See :ref:`NumPy ufunc docs <ufuncs.kwargs>` for other keyword arguments.

    See Also
    --------
    get_parts

    Examples
    --------
    >>> import shapely
    >>> shapely.from_geojson('{"type": "Point","coordinates": [1, 2]}')
    <POINT (1 2)>

    """

@overload
def from_geojson(
    geometry: str | bytes, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs
) -> BaseGeometry: ...  # type: ignore[overload-overlap]
@overload
def from_geojson(
    geometry: ArrayLikeSeq[str | bytes | None], on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise", **kwargs
) -> GeoArray: ...
