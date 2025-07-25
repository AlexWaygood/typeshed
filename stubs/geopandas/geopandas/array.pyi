import builtins
from _typeshed import Incomplete, Unused
from collections.abc import Callable, Collection, Sequence
from typing import Any, ClassVar, Final, Literal, NoReturn, SupportsIndex, TypeVar, overload
from typing_extensions import Self, TypeAlias, deprecated

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, DTypeLike, NDArray
from pandas.api.extensions import ExtensionArray, ExtensionDtype
from pyproj import CRS, Transformer
from shapely import Geometry
from shapely.geometry.base import BaseGeometry

from .base import _AffinityOrigin, _ConvertibleToCRS
from .sindex import SpatialIndex

_ScalarType = TypeVar("_ScalarType", bound=np.generic)
_Array1D: TypeAlias = np.ndarray[tuple[int], np.dtype[_ScalarType]]
_Array2D: TypeAlias = np.ndarray[tuple[int, int], np.dtype[_ScalarType]]
_ArrayOrGeom: TypeAlias = GeometryArray | ArrayLike | Geometry

TransformerFromCRS = Transformer.from_crs
POLYGON_GEOM_TYPES: Final[set[str]]
LINE_GEOM_TYPES: Final[set[str]]
POINT_GEOM_TYPES: Final[set[str]]

class GeometryDtype(ExtensionDtype):
    type: ClassVar[type[BaseGeometry]]
    name: ClassVar[str]
    na_value: None
    @classmethod
    def construct_from_string(cls, string: str) -> Self: ...
    @classmethod
    def construct_array_type(cls) -> builtins.type[GeometryArray]: ...

def isna(value: object) -> bool:
    """
    Check if scalar value is NA-like (None, np.nan or pd.NA).

    Custom version that only works for scalars (returning True or False),
    as `pd.isna` also works for array-like input returning a boolean array.
    """

def from_shapely(data, crs: _ConvertibleToCRS | None = None) -> GeometryArray:
    """
    Convert a list or array of shapely objects to a GeometryArray.

    Validates the elements.

    Parameters
    ----------
    data : array-like
        list or array of shapely objects
    crs : value, optional
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.

    """

def to_shapely(geoms: GeometryArray) -> _Array1D[np.object_]:
    """Convert GeometryArray to numpy object array of shapely objects."""

def from_wkb(
    data, crs: _ConvertibleToCRS | None = None, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise"
) -> GeometryArray:
    """
    Convert a list or array of WKB objects to a GeometryArray.

    Parameters
    ----------
    data : array-like
        list or array of WKB objects
    crs : value, optional
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.
    on_invalid: {"raise", "warn", "ignore"}, default "raise"
        - raise: an exception will be raised if a WKB input geometry is invalid.
        - warn: a warning will be raised and invalid WKB geometries will be returned as
          None.
        - ignore: invalid WKB geometries will be returned as None without a warning.
        - fix: an effort is made to fix invalid input geometries (e.g. close
          unclosed rings). If this is not possible, they are returned as ``None``
          without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

    """

@overload
def to_wkb(geoms: GeometryArray, hex: Literal[False] = False, **kwargs) -> _Array1D[np.bytes_]:
    """Convert GeometryArray to a numpy object array of WKB objects."""

@overload
def to_wkb(geoms: GeometryArray, hex: Literal[True], **kwargs) -> _Array1D[np.str_]: ...
def from_wkt(
    data, crs: _ConvertibleToCRS | None = None, on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise"
) -> GeometryArray:
    """
    Convert a list or array of WKT objects to a GeometryArray.

    Parameters
    ----------
    data : array-like
        list or array of WKT objects
    crs : value, optional
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.
    on_invalid : {"raise", "warn", "ignore"}, default "raise"
        - raise: an exception will be raised if a WKT input geometry is invalid.
        - warn: a warning will be raised and invalid WKT geometries will be
          returned as ``None``.
        - ignore: invalid WKT geometries will be returned as ``None`` without a warning.
        - fix: an effort is made to fix invalid input geometries (e.g. close
          unclosed rings). If this is not possible, they are returned as ``None``
          without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

    """

def to_wkt(geoms: GeometryArray, **kwargs) -> _Array1D[np.str_]:
    """Convert GeometryArray to a numpy object array of WKT objects."""

def points_from_xy(x: ArrayLike, y: ArrayLike, z: ArrayLike | None = None, crs: _ConvertibleToCRS | None = None) -> GeometryArray:
    """
    Generate GeometryArray of shapely Point geometries from x, y(, z) coordinates.

    In case of geographic coordinates, it is assumed that longitude is captured by
    ``x`` coordinates and latitude by ``y``.

    Parameters
    ----------
    x, y, z : iterable
    crs : value, optional
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'x': [0, 1, 2], 'y': [0, 1, 2], 'z': [0, 1, 2]})
    >>> df
       x  y  z
    0  0  0  0
    1  1  1  1
    2  2  2  2
    >>> geometry = geopandas.points_from_xy(x=[1, 0], y=[0, 1])
    >>> geometry = geopandas.points_from_xy(df['x'], df['y'], df['z'])
    >>> gdf = geopandas.GeoDataFrame(
    ...     df, geometry=geopandas.points_from_xy(df['x'], df['y']))

    Having geographic coordinates:

    >>> df = pd.DataFrame({'longitude': [-140, 0, 123], 'latitude': [-65, 1, 48]})
    >>> df
       longitude  latitude
    0       -140       -65
    1          0         1
    2        123        48
    >>> geometry = geopandas.points_from_xy(df.longitude, df.latitude, crs="EPSG:4326")

    Returns
    -------
    output : GeometryArray
    """

class GeometryArray(ExtensionArray):
    """Class wrapping a numpy array of Shapely objects.

    It also holds the array-based implementations.
    """

    def __init__(self, data: GeometryArray | NDArray[np.object_], crs: _ConvertibleToCRS | None = None) -> None: ...
    @property
    def sindex(self) -> SpatialIndex:
        """Spatial index for the geometries in this array."""

    @property
    def has_sindex(self) -> bool:
        """Check the existence of the spatial index without generating it.

        Use the `.sindex` attribute on a GeoDataFrame or GeoSeries
        to generate a spatial index if it does not yet exist,
        which may take considerable time based on the underlying index
        implementation.

        Note that the underlying spatial index may not be fully
        initialized until the first use.

        See Also
        --------
        GeoDataFrame.has_sindex

        Returns
        -------
        bool
            `True` if the spatial index has been generated or
            `False` if not.
        """

    @property
    def crs(self) -> CRS | None:
        """The Coordinate Reference System (CRS) represented as a ``pyproj.CRS`` object.

        Returns None if the CRS is not set, and to set the value it
        :getter: Returns a ``pyproj.CRS`` or None. When setting, the value
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.
        """

    @crs.setter
    def crs(self, value: _ConvertibleToCRS | None) -> None: ...
    def check_geographic_crs(self, stacklevel: int) -> None:
        """Check CRS and warn if the planar operation is done in a geographic CRS."""

    @property
    def dtype(self) -> GeometryDtype: ...
    def __len__(self) -> int: ...
    # np.integer[Any] because precision is not important
    @overload
    def __getitem__(self, idx: int | np.integer[Any]) -> BaseGeometry: ...  # Always 1-D, doesn't accept tuple
    @overload
    def __getitem__(
        self, idx: slice | Sequence[SupportsIndex] | NDArray[np.bool_] | NDArray[np.integer[Any]]
    ) -> GeometryArray: ...
    @overload
    def __getitem__(
        self, idx: int | np.integer[Any] | slice | Sequence[int] | NDArray[np.bool_] | NDArray[np.integer[Any]]
    ) -> BaseGeometry | GeometryArray: ...
    def __setitem__(
        self, key, value: _ArrayOrGeom | pd.DataFrame | pd.Series[Any]  # Cannot use pd.Series[BaseGeometry]
    ) -> None: ...
    @property
    def is_valid(self) -> _Array1D[np.bool_]: ...
    def is_valid_reason(self) -> _Array1D[np.object_]: ...
    def is_valid_coverage(self, gap_width: float = 0.0) -> bool: ...
    def invalid_coverage_edges(self, gap_width: float = 0.0) -> _Array1D[np.object_]: ...
    @property
    def is_empty(self) -> _Array1D[np.bool_]: ...
    @property
    def is_simple(self) -> _Array1D[np.bool_]: ...
    @property
    def is_ring(self) -> _Array1D[np.bool_]: ...
    @property
    def is_closed(self) -> _Array1D[np.bool_]: ...
    @property
    def is_ccw(self) -> _Array1D[np.bool_]: ...
    @property
    def has_z(self) -> _Array1D[np.bool_]: ...
    @property
    def has_m(self) -> _Array1D[np.bool_]: ...
    @property
    def geom_type(self) -> _Array1D[np.str_]: ...
    @property
    def area(self) -> _Array1D[np.float64]:
        """Return the area of the geometries in this array.

        Raises a UserWarning if the CRS is geographic, as the area
        calculation is not accurate in that case.

        Note that the area is calculated in the units of the CRS.

        Returns
        -------
        np.ndarray of float
            Area of the geometries.
        """

    @property
    def length(self) -> _Array1D[np.float64]: ...
    def count_coordinates(self) -> _Array1D[np.int32]: ...
    def count_geometries(self) -> _Array1D[np.int32]: ...
    def count_interior_rings(self) -> _Array1D[np.int32]: ...
    def get_precision(self) -> _Array1D[np.float64]: ...
    def get_geometry(self, index: SupportsIndex | ArrayLike) -> _Array1D[np.object_]: ...
    @property
    def boundary(self) -> GeometryArray: ...
    @property
    def centroid(self) -> GeometryArray: ...
    def concave_hull(self, ratio: float, allow_holes: bool) -> _Array1D[np.object_]: ...
    def constrained_delaunay_triangles(self) -> GeometryArray: ...
    @property
    def convex_hull(self) -> GeometryArray:
        """Return the convex hull of the geometries in this array."""

    @property
    def envelope(self) -> GeometryArray:
        """Return the envelope of the geometries in this array."""

    def minimum_rotated_rectangle(self) -> GeometryArray:
        """Return the minimum rotated rectangle of the geometries in this array."""

    @property
    def exterior(self) -> GeometryArray: ...
    def extract_unique_points(self) -> GeometryArray: ...
    def offset_curve(
        self,
        distance: float | ArrayLike,
        quad_segs: int = 8,
        join_style: Literal["round", "bevel", "mitre"] = "round",
        mitre_limit: float = 5.0,
    ) -> GeometryArray: ...
    @property
    def interiors(self) -> _Array1D[np.object_]: ...
    def remove_repeated_points(self, tolerance: float | ArrayLike = 0.0) -> GeometryArray: ...
    def representative_point(self) -> GeometryArray: ...
    def minimum_bounding_circle(self) -> GeometryArray: ...
    def maximum_inscribed_circle(self, tolerance: float | ArrayLike) -> GeometryArray: ...
    def minimum_bounding_radius(self) -> _Array1D[np.float64]: ...
    def minimum_clearance(self) -> _Array1D[np.float64]: ...
    def minimum_clearance_line(self) -> GeometryArray: ...
    def normalize(self) -> GeometryArray: ...
    def orient_polygons(self, exterior_cw: bool = False) -> GeometryArray: ...
    def make_valid(self, method: Literal["linework", "structure"] = "linework", keep_collapsed: bool = True) -> GeometryArray: ...
    def reverse(self) -> GeometryArray: ...
    def segmentize(self, max_segment_length: float | ArrayLike) -> GeometryArray: ...
    def force_2d(self) -> GeometryArray: ...
    def force_3d(self, z: float | ArrayLike = 0) -> GeometryArray: ...
    def transform(
        self, transformation: Callable[[NDArray[np.float64]], NDArray[np.float64]], include_z: bool = False
    ) -> GeometryArray: ...
    def line_merge(self, directed: bool = False) -> GeometryArray: ...
    def set_precision(
        self, grid_size: float, mode: Literal["valid_output", "pointwise", "keep_collapsed", 0, 1, 2] = "valid_output"
    ) -> GeometryArray: ...
    def covers(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def covered_by(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def contains(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def contains_properly(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def crosses(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def disjoint(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def geom_equals(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def intersects(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def overlaps(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def touches(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def within(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def dwithin(self, other: _ArrayOrGeom, distance: float) -> _Array1D[np.bool_]: ...
    def geom_equals_exact(self, other: _ArrayOrGeom, tolerance: float | ArrayLike) -> _Array1D[np.bool_]: ...
    def geom_equals_identical(self, other: _ArrayOrGeom) -> _Array1D[np.bool_]: ...
    def clip_by_rect(self, xmin: float, ymin: float, xmax: float, ymax: float) -> GeometryArray: ...
    def difference(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def intersection(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def symmetric_difference(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def union(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def shortest_line(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def snap(self, other: _ArrayOrGeom, tolerance: float | ArrayLike) -> GeometryArray: ...
    def shared_paths(self, other: _ArrayOrGeom) -> GeometryArray: ...
    def distance(self, other: _ArrayOrGeom) -> _Array1D[np.float64]: ...
    def hausdorff_distance(self, other: _ArrayOrGeom, **kwargs) -> _Array1D[np.float64]: ...
    def frechet_distance(self, other: _ArrayOrGeom, **kwargs) -> _Array1D[np.float64]: ...
    def buffer(self, distance: float | ArrayLike, resolution: int = 16, **kwargs) -> GeometryArray: ...
    def interpolate(self, distance: float | ArrayLike, normalized: bool = False) -> GeometryArray: ...
    def simplify(self, tolerance: float | ArrayLike, preserve_topology: bool = True) -> GeometryArray: ...
    def simplify_coverage(self, tolerance: float | ArrayLike, simplify_boundary: bool = True) -> GeometryArray: ...
    def project(self, other: _ArrayOrGeom, normalized: bool = False) -> _Array1D[np.float64]: ...
    def relate(self, other: _ArrayOrGeom) -> _Array1D[np.str_]: ...
    def relate_pattern(self, other: _ArrayOrGeom, pattern: str) -> _Array1D[np.bool_]: ...
    @deprecated("Use method `union_all` instead.")
    def unary_union(self) -> BaseGeometry: ...
    def union_all(
        self, method: Literal["coverage", "unary", "disjoint_subset"] = "unary", grid_size: float | None = None
    ) -> BaseGeometry: ...
    def intersection_all(self) -> BaseGeometry: ...
    def affine_transform(self, matrix: Collection[float]) -> GeometryArray: ...
    def translate(self, xoff: float = 0.0, yoff: float = 0.0, zoff: float = 0.0) -> GeometryArray: ...
    def rotate(self, angle: float, origin: _AffinityOrigin = "center", use_radians: bool = False) -> GeometryArray: ...
    def scale(
        self, xfact: float = 1.0, yfact: float = 1.0, zfact: float = 1.0, origin: _AffinityOrigin = "center"
    ) -> GeometryArray: ...
    def skew(
        self, xs: float = 0.0, ys: float = 0.0, origin: _AffinityOrigin = "center", use_radians: bool = False
    ) -> GeometryArray: ...
    def to_crs(self, crs: _ConvertibleToCRS | None = None, epsg: int | None = None) -> GeometryArray: ...
    def estimate_utm_crs(self, datum_name: str = "WGS 84") -> CRS: ...
    @property
    def x(self) -> _Array1D[np.float64]:
        """Return the x location of point geometries in a GeoSeries."""

    @property
    def y(self) -> _Array1D[np.float64]:
        """Return the y location of point geometries in a GeoSeries."""

    @property
    def z(self) -> _Array1D[np.float64]:
        """Return the z location of point geometries in a GeoSeries."""

    @property
    def m(self) -> _Array1D[np.float64]:
        """Return the m coordinate of point geometries in a GeoSeries."""

    @property
    def bounds(self) -> _Array2D[np.float64]: ...
    @property
    def total_bounds(self) -> _Array1D[np.float64]: ...
    @property
    def size(self) -> int: ...
    @property
    def shape(self) -> tuple[int]: ...  # Always 1-D, this is not mistaken for tuple[int, ...]
    @property
    def ndim(self) -> Literal[1]: ...
    def copy(self, *args: Unused, **kwargs: Unused) -> GeometryArray: ...
    def take(
        self, indices: Sequence[SupportsIndex] | NDArray[np.integer], allow_fill: bool = False, fill_value: Geometry | None = None
    ) -> GeometryArray: ...
    def fillna(
        self,
        value: Geometry | GeometryArray | None = None,
        method: Literal["backfill", "bfill", "pad", "ffill"] | None = None,
        limit: int | None = None,
        copy: bool = True,
    ) -> GeometryArray:
        """
        Fill NA values with geometry (or geometries) or using the specified method.

        Parameters
        ----------
        value : shapely geometry object or GeometryArray
            If a geometry value is passed it is used to fill all missing values.
            Alternatively, an GeometryArray 'value' can be given. It's expected
            that the GeometryArray has the same length as 'self'.

        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes in reindexed Series
            pad / ffill: propagate last valid observation forward to next valid
            backfill / bfill: use NEXT valid observation to fill gap

        limit : int, default None
            The maximum number of entries where NA values will be filled.

        copy : bool, default True
            Whether to make a copy of the data before filling. If False, then
            the original should be modified and no new memory should be allocated.

        Returns
        -------
        GeometryArray
        """

    @overload
    def astype(self, dtype: GeometryDtype, copy: bool = True) -> GeometryArray:
        """
        Cast to a NumPy array with 'dtype'.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        array : ndarray
            NumPy ndarray with 'dtype' for its dtype.
        """

    @overload
    def astype(self, dtype: ExtensionDtype | Literal["string"], copy: bool = True) -> ExtensionArray: ...  # type: ignore[overload-overlap]
    @overload
    def astype(self, dtype: DTypeLike, copy: bool = True) -> _Array1D[Incomplete]: ...
    def isna(self) -> _Array1D[np.bool_]:
        """Boolean NumPy array indicating if each value is missing."""

    def value_counts(self, dropna: bool = True) -> pd.Series[int]:
        """
        Compute a histogram of the counts of non-null values.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN

        Returns
        -------
        pd.Series
        """

    def unique(self) -> GeometryArray:
        """Compute the ExtensionArray of unique values.

        Returns
        -------
        uniques : ExtensionArray
        """

    @property
    def nbytes(self) -> int: ...
    def shift(self, periods: int = 1, fill_value: Geometry | None = None) -> GeometryArray:  # type: ignore[override]
        """
        Shift values by desired number.

        Newly introduced missing values are filled with
        ``self.dtype.na_value``.

        Parameters
        ----------
        periods : int, default 1
            The number of periods to shift. Negative values are allowed
            for shifting backwards.

        fill_value : object, optional (default None)
            The scalar value to use for newly introduced missing values.
            The default is ``self.dtype.na_value``.

        Returns
        -------
        GeometryArray
            Shifted.

        Notes
        -----
        If ``self`` is empty or ``periods`` is 0, a copy of ``self`` is
        returned.

        If ``periods > len(self)``, then an array of size
        len(self) is returned, with all values filled with
        ``self.dtype.na_value``.
        """

    def argmin(self, skipna: bool = True) -> NoReturn: ...
    def argmax(self, skipna: bool = True) -> NoReturn: ...
    def __array__(self, dtype: DTypeLike | None = None, copy: bool | None = None) -> _Array1D[np.object_]:
        """Return the data as a numpy array.

        This is the numpy array interface.

        Returns
        -------
        values : numpy array
        """

    def __eq__(self, other: object) -> _Array1D[np.bool_]: ...  # type: ignore[override]
    def __ne__(self, other: object) -> _Array1D[np.bool_]: ...  # type: ignore[override]
    def __contains__(self, item: object) -> np.bool_:
        """Return for `item in self`."""

# TODO: Improve `func` type with a callable protocol (with overloads for 2D and 3D geometries)
def transform(
    data: NDArray[np.object_] | GeometryArray | pd.Series[Any],  # Cannot use pd.Series[BaseGeometry]
    func: Callable[..., NDArray[np.float64]],
) -> NDArray[np.object_]: ...
