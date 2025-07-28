import io
import os
from _typeshed import Incomplete, SupportsGetItem, SupportsLenAndGetItem, SupportsRead, SupportsWrite
from collections.abc import Callable, Container, Hashable, Iterable, Iterator, Mapping, Sequence
from json import JSONEncoder
from typing import Any, Literal, overload
from typing_extensions import Self

import pandas as pd
from numpy.typing import ArrayLike
from pandas._typing import AggFuncTypeFrame, Axes, Axis, Dtype, GroupByObject, IndexLabel, Scalar
from pyproj import CRS

from ._decorator import doc
from .base import (
    GeoPandasBase,
    _BboxLike,
    _ClipMask,
    _ConvertibleToCRS,
    _ConvertibleToDataFrame,
    _GeomCol,
    _GeomSeq,
    _MaskLike,
    _SupportsGeoInterface,
)
from .explore import _explore
from .geoseries import GeoSeries
from .io._geoarrow import ArrowTable, _GeomEncoding
from .io.sql import _SQLConnection
from .plotting import GeoplotAccessor

crs_mismatch_error: str

class GeoDataFrame(GeoPandasBase, pd.DataFrame):  # type: ignore[misc]
    """A GeoDataFrame object is a pandas.DataFrame that has one or more columns
    containing geometry.

    In addition to the standard DataFrame constructor arguments,
    GeoDataFrame also accepts the following keyword arguments:

    Parameters
    ----------
    crs : value (optional)
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.
    geometry : str or array-like (optional)
        Value to use as the active geometry column.
        If str, treated as column name to use. If array-like, it will be
        added as new column named 'geometry' on the GeoDataFrame and set as the
        active geometry column.

        Note that if ``geometry`` is a (Geo)Series with a
        name, the name will not be used, a column named "geometry" will still be
        added. To preserve the name, you can use :meth:`~GeoDataFrame.rename_geometry`
        to update the geometry column name.

    Examples
    --------
    Constructing GeoDataFrame from a dictionary.

    >>> from shapely.geometry import Point
    >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
    >>> gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
    >>> gdf
        col1     geometry
    0  name1  POINT (1 2)
    1  name2  POINT (2 1)

    Notice that the inferred dtype of 'geometry' columns is geometry.

    >>> gdf.dtypes
    col1          object
    geometry    geometry
    dtype: object

    Constructing GeoDataFrame from a pandas DataFrame with a column of WKT geometries:

    >>> import pandas as pd
    >>> d = {'col1': ['name1', 'name2'], 'wkt': ['POINT (1 2)', 'POINT (2 1)']}
    >>> df = pd.DataFrame(d)
    >>> gs = geopandas.GeoSeries.from_wkt(df['wkt'])
    >>> gdf = geopandas.GeoDataFrame(df, geometry=gs, crs="EPSG:4326")
    >>> gdf
        col1          wkt     geometry
    0  name1  POINT (1 2)  POINT (1 2)
    1  name2  POINT (2 1)  POINT (2 1)

    See Also
    --------
    GeoSeries : Series object designed to store shapely geometry objects
    """

    # Override the weird annotation of DataFrame.__new__ in pandas-stubs
    @overload
    def __new__(
        cls,
        data: _ConvertibleToDataFrame | None = None,
        index: Axes | None = None,
        columns: Axes | None = None,
        dtype: Dtype | None = None,
        copy: bool | None = None,
        *,
        geometry: _GeomCol | None = None,
        crs: _ConvertibleToCRS | None = None,
    ) -> Self: ...
    @overload
    def __new__(
        cls,
        data: Scalar,
        index: Axes,
        columns: Axes,
        dtype: Dtype | None = None,
        copy: bool | None = None,
        *,
        geometry: _GeomCol | None = None,
        crs: _ConvertibleToCRS | None = None,
    ) -> Self: ...
    def __init__(
        self,
        data: _ConvertibleToDataFrame | None = None,
        index: Axes | None = None,
        columns: Axes | None = None,
        dtype: Dtype | None = None,
        copy: bool | None = None,
        *,
        geometry: _GeomCol | None = None,
        crs: _ConvertibleToCRS | None = None,
    ) -> None: ...
    def __setattr__(self, attr: str, val: Any) -> None: ...  # Can set arbitrary objects
    @property
    def geometry(self) -> GeoSeries:
        """Geometry data for GeoDataFrame"""

    @geometry.setter
    def geometry(self, col: _GeomSeq) -> None: ...
    @overload
    def set_geometry(
        self, col: _GeomCol, drop: bool | None = None, inplace: Literal[False] = False, crs: _ConvertibleToCRS | None = None
    ) -> Self:
        """
        Set the GeoDataFrame geometry using either an existing column or
        the specified input. By default yields a new object.

        The original geometry column is replaced with the input.

        Parameters
        ----------
        col : column label or array-like
            An existing column name or values to set as the new geometry column.
            If values (array-like, (Geo)Series) are passed, then if they are named
            (Series) the new geometry column will have the corresponding name,
            otherwise the existing geometry column will be replaced. If there is
            no existing geometry column, the new geometry column will use the
            default name "geometry".
        drop : boolean, default False
            When specifying a named Series or an existing column name for `col`,
            controls if the previous geometry column should be dropped from the
            result. The default of False keeps both the old and new geometry column.

            .. deprecated:: 1.0.0

        inplace : boolean, default False
            Modify the GeoDataFrame in place (do not create a new object)
        crs : pyproj.CRS, optional
            Coordinate system to use. The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
            If passed, overrides both DataFrame and col's crs.
            Otherwise, tries to get crs from passed col values or DataFrame.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        Passing an array:

        >>> df1 = gdf.set_geometry([Point(0,0), Point(1,1)])
        >>> df1
            col1     geometry
        0  name1  POINT (0 0)
        1  name2  POINT (1 1)

        Using existing column:

        >>> gdf["buffered"] = gdf.buffer(2)
        >>> df2 = gdf.set_geometry("buffered")
        >>> df2.geometry
        0    POLYGON ((3 2, 2.99037 1.80397, 2.96157 1.6098...
        1    POLYGON ((4 1, 3.99037 0.80397, 3.96157 0.6098...
        Name: buffered, dtype: geometry

        Returns
        -------
        GeoDataFrame

        See Also
        --------
        GeoDataFrame.rename_geometry : rename an active geometry column
        """

    @overload
    def set_geometry(
        self, col: _GeomCol, drop: bool | None = None, *, inplace: Literal[True], crs: _ConvertibleToCRS | None = None
    ) -> None: ...
    @overload
    def set_geometry(
        self, col: _GeomCol, drop: bool | None, inplace: Literal[True], crs: _ConvertibleToCRS | None = None
    ) -> None: ...
    @overload
    def rename_geometry(self, col: Hashable, inplace: Literal[False] = False) -> Self:
        """Rename the GeoDataFrame geometry column to the specified name.

        By default yields a new object.

        The original geometry column is replaced with the input.

        Parameters
        ----------
        col : new geometry column label
        inplace : boolean, default False
            Modify the GeoDataFrame in place (do not create a new object)

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> df = geopandas.GeoDataFrame(d, crs="EPSG:4326")
        >>> df1 = df.rename_geometry('geom1')
        >>> df1.geometry.name
        'geom1'
        >>> df.rename_geometry('geom1', inplace=True)
        >>> df.geometry.name
        'geom1'


        See Also
        --------
        GeoDataFrame.set_geometry : set the active geometry
        """

    @overload
    def rename_geometry(self, col: Hashable, inplace: Literal[True]) -> None: ...
    @property
    def active_geometry_name(self) -> str | None:
        """Return the name of the active geometry column.

        Returns a name if a GeoDataFrame has an active geometry column set,
        otherwise returns None. The return type is usually a string, but may be
        an integer, tuple or other hashable, depending on the contents of the
        dataframe columns.

        You can also access the active geometry column using the
        ``.geometry`` property. You can set a GeoSeries to be an active geometry
        using the :meth:`~GeoDataFrame.set_geometry` method.

        Returns
        -------
        str or other index label supported by pandas
            name of an active geometry column or None

        See Also
        --------
        GeoDataFrame.set_geometry : set the active geometry
        """

    @property
    def crs(self) -> CRS | None:
        """
        The Coordinate Reference System (CRS) represented as a ``pyproj.CRS``
        object.

        Returns None if the CRS is not set, and to set the value it
        :getter: Returns a ``pyproj.CRS`` or None. When setting, the value
        can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.

        Examples
        --------
        >>> gdf.crs  # doctest: +SKIP
        <Geographic 2D CRS: EPSG:4326>
        Name: WGS 84
        Axis Info [ellipsoidal]:
        - Lat[north]: Geodetic latitude (degree)
        - Lon[east]: Geodetic longitude (degree)
        Area of Use:
        - name: World
        - bounds: (-180.0, -90.0, 180.0, 90.0)
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        See Also
        --------
        GeoDataFrame.set_crs : assign CRS
        GeoDataFrame.to_crs : re-project to another CRS

        """

    @crs.setter
    def crs(self, value: _ConvertibleToCRS | None) -> None: ...
    @classmethod
    def from_dict(  # type: ignore[override]
        # Mapping[Any, Any] because of invariance keys and arbitrary values
        cls,
        data: Mapping[Any, Any],
        geometry: _GeomCol | None = None,
        crs: _ConvertibleToCRS | None = None,
        **kwargs,
    ) -> Self:
        """Construct GeoDataFrame from dict of array-like or dicts by
        overriding DataFrame.from_dict method with geometry and crs.

        Parameters
        ----------
        data : dict
            Of the form {field : array-like} or {field : dict}.
        geometry : str or array (optional)
            If str, column to use as geometry. If array, will be set as 'geometry'
            column on GeoDataFrame.
        crs : str or dict (optional)
            Coordinate reference system to set on the resulting frame.
        kwargs : key-word arguments
            These arguments are passed to DataFrame.from_dict

        Returns
        -------
        GeoDataFrame

        """
    # Keep inline with GeoSeries.from_file and geopandas.io.file._read_file
    @classmethod
    def from_file(
        cls,
        filename: str | os.PathLike[str] | SupportsRead[Incomplete],
        *,
        bbox: _BboxLike | None = None,
        mask: _MaskLike | None = None,
        rows: int | slice | None = None,
        engine: Literal["fiona", "pyogrio"] | None = None,
        ignore_geometry: Literal[False] = False,
        layer: int | str | None = None,
        encoding: str | None = None,
        **kwargs,  # engine dependent
    ) -> Self:
        """Alternate constructor to create a ``GeoDataFrame`` from a file.

        It is recommended to use :func:`geopandas.read_file` instead.

        Can load a ``GeoDataFrame`` from a file in any format recognized by
        `pyogrio`. See http://pyogrio.readthedocs.io/ for details.

        Parameters
        ----------
        filename : str
            File path or file handle to read from. Depending on which kwargs
            are included, the content of filename may vary. See
            :func:`pyogrio.read_dataframe` for usage details.
        kwargs : key-word arguments
            These arguments are passed to :func:`pyogrio.read_dataframe`, and can be
            used to access multi-layer data, data stored within archives (zip files),
            etc.

        Examples
        --------
        >>> import geodatasets
        >>> path = geodatasets.get_path('nybb')
        >>> gdf = geopandas.GeoDataFrame.from_file(path)
        >>> gdf  # doctest: +SKIP
           BoroCode       BoroName     Shape_Leng    Shape_Area                                           geometry
        0         5  Staten Island  330470.010332  1.623820e+09  MULTIPOLYGON (((970217.022 145643.332, 970227....
        1         4         Queens  896344.047763  3.045213e+09  MULTIPOLYGON (((1029606.077 156073.814, 102957...
        2         3       Brooklyn  741080.523166  1.937479e+09  MULTIPOLYGON (((1021176.479 151374.797, 102100...
        3         1      Manhattan  359299.096471  6.364715e+08  MULTIPOLYGON (((981219.056 188655.316, 980940....
        4         2          Bronx  464392.991824  1.186925e+09  MULTIPOLYGON (((1012821.806 229228.265, 101278...

        The recommended method of reading files is :func:`geopandas.read_file`:

        >>> gdf = geopandas.read_file(path)

        See Also
        --------
        read_file : read file to GeoDataFrame
        GeoDataFrame.to_file : write GeoDataFrame to file

        """

    @classmethod
    def from_features(
        cls,
        features: (
            _SupportsGeoInterface
            | Mapping[str, _SupportsGeoInterface | SupportsGetItem[str, Incomplete]]
            | Iterable[_SupportsGeoInterface | SupportsGetItem[str, Incomplete]]
        ),
        crs: _ConvertibleToCRS | None = None,
        columns: Axes | None = None,
    ) -> Self:
        """
        Alternate constructor to create GeoDataFrame from an iterable of
        features or a feature collection.

        Parameters
        ----------
        features
            - Iterable of features, where each element must be a feature
              dictionary or implement the __geo_interface__.
            - Feature collection, where the 'features' key contains an
              iterable of features.
            - Object holding a feature collection that implements the
              ``__geo_interface__``.
        crs : str or dict (optional)
            Coordinate reference system to set on the resulting frame.
        columns : list of column names, optional
            Optionally specify the column names to include in the output frame.
            This does not overwrite the property names of the input, but can
            ensure a consistent output format.

        Returns
        -------
        GeoDataFrame

        Notes
        -----
        For more information about the ``__geo_interface__``, see
        https://gist.github.com/sgillies/2217756

        Examples
        --------
        >>> feature_coll = {
        ...     "type": "FeatureCollection",
        ...     "features": [
        ...         {
        ...             "id": "0",
        ...             "type": "Feature",
        ...             "properties": {"col1": "name1"},
        ...             "geometry": {"type": "Point", "coordinates": (1.0, 2.0)},
        ...             "bbox": (1.0, 2.0, 1.0, 2.0),
        ...         },
        ...         {
        ...             "id": "1",
        ...             "type": "Feature",
        ...             "properties": {"col1": "name2"},
        ...             "geometry": {"type": "Point", "coordinates": (2.0, 1.0)},
        ...             "bbox": (2.0, 1.0, 2.0, 1.0),
        ...         },
        ...     ],
        ...     "bbox": (1.0, 1.0, 2.0, 2.0),
        ... }
        >>> df = geopandas.GeoDataFrame.from_features(feature_coll)
        >>> df
              geometry   col1
        0  POINT (1 2)  name1
        1  POINT (2 1)  name2

        """

    @overload
    @classmethod
    def from_postgis(
        cls,
        sql: str,
        con: _SQLConnection,
        geom_col: str = "geom",
        crs: _ConvertibleToCRS | None = None,
        index_col: str | list[str] | None = None,
        coerce_float: bool = True,
        parse_dates: Container[str | Mapping[str, Incomplete]] | Mapping[str, str | Mapping[str, Incomplete]] | None = None,
        params: SupportsLenAndGetItem[Scalar] | Mapping[str, Scalar] | None = None,
        *,
        chunksize: int,
    ) -> Iterator[GeoDataFrame]:
        """
        Alternate constructor to create a ``GeoDataFrame`` from a sql query
        containing a geometry column in WKB representation.

        Parameters
        ----------
        sql : string
        con : sqlalchemy.engine.Connection or sqlalchemy.engine.Engine
        geom_col : string, default 'geom'
            column name to convert to shapely geometries
        crs : optional
            Coordinate reference system to use for the returned GeoDataFrame
        index_col : string or list of strings, optional, default: None
            Column(s) to set as index(MultiIndex)
        coerce_float : boolean, default True
            Attempt to convert values of non-string, non-numeric objects (like
            decimal.Decimal) to floating point, useful for SQL result sets
        parse_dates : list or dict, default None
            - List of column names to parse as dates.
            - Dict of ``{column_name: format string}`` where format string is
              strftime compatible in case of parsing string times, or is one of
              (D, s, ns, ms, us) in case of parsing integer timestamps.
            - Dict of ``{column_name: arg dict}``, where the arg dict
              corresponds to the keyword arguments of
              :func:`pandas.to_datetime`. Especially useful with databases
              without native Datetime support, such as SQLite.
        params : list, tuple or dict, optional, default None
            List of parameters to pass to execute method.
        chunksize : int, default None
            If specified, return an iterator where chunksize is the number
            of rows to include in each chunk.

        Examples
        --------
        PostGIS

        >>> from sqlalchemy import create_engine  # doctest: +SKIP
        >>> db_connection_url = "postgresql://myusername:mypassword@myhost:5432/mydb"
        >>> con = create_engine(db_connection_url)  # doctest: +SKIP
        >>> sql = "SELECT geom, highway FROM roads"
        >>> df = geopandas.GeoDataFrame.from_postgis(sql, con)  # doctest: +SKIP

        SpatiaLite

        >>> sql = "SELECT ST_Binary(geom) AS geom, highway FROM roads"
        >>> df = geopandas.GeoDataFrame.from_postgis(sql, con)  # doctest: +SKIP

        The recommended method of reading from PostGIS is
        :func:`geopandas.read_postgis`:

        >>> df = geopandas.read_postgis(sql, con)  # doctest: +SKIP

        See Also
        --------
        geopandas.read_postgis : read PostGIS database to GeoDataFrame
        """

    @overload
    @classmethod
    def from_postgis(
        cls,
        sql: str,
        con: _SQLConnection,
        geom_col: str = "geom",
        crs: _ConvertibleToCRS | None = None,
        index_col: str | list[str] | None = None,
        coerce_float: bool = True,
        parse_dates: Container[str | Mapping[str, Incomplete]] | Mapping[str, str | Mapping[str, Incomplete]] | None = None,
        params: SupportsLenAndGetItem[Scalar] | Mapping[str, Scalar] | None = None,
        chunksize: None = None,
    ) -> GeoDataFrame: ...
    @classmethod
    def from_arrow(
        cls, table, geometry: str | None = None, to_pandas_kwargs: Mapping[str, Incomplete] | None = None
    ) -> GeoDataFrame:  # TODO: `table: pyarrow.Table | table-like`
        """
        Construct a GeoDataFrame from a Arrow table object based on GeoArrow
        extension types.

        See https://geoarrow.org/ for details on the GeoArrow specification.

        This functions accepts any tabular Arrow object implementing
        the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_array__``
        or ``__arrow_c_stream__`` method).

        .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

        .. versionadded:: 1.0

        Parameters
        ----------
        table : pyarrow.Table or Arrow-compatible table
            Any tabular object implementing the Arrow PyCapsule Protocol
            (i.e. has an ``__arrow_c_array__`` or ``__arrow_c_stream__``
            method). This table should have at least one column with a
            geoarrow geometry type.
        geometry : str, default None
            The name of the geometry column to set as the active geometry
            column. If None, the first geometry column found will be used.
        to_pandas_kwargs : dict, optional
            Arguments passed to the `pa.Table.to_pandas` method for non-geometry
            columns. This can be used to control the behavior of the conversion of the
            non-geometry columns to a pandas DataFrame. For example, you can use this
            to control the dtype conversion of the columns. By default, the `to_pandas`
            method is called with no additional arguments.

        Returns
        -------
        GeoDataFrame

        """

    def to_json(  # type: ignore[override]
        self,
        na: str = "null",
        show_bbox: bool = False,
        drop_id: bool = False,
        to_wgs84: bool = False,
        *,
        # json.dumps kwargs
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        cls: type[JSONEncoder] | None = None,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        default: Callable[..., Any] | None = None,  # as typed in the json stdlib module
        sort_keys: bool = False,
        **kwargs,
    ) -> str:
        """Return a GeoJSON representation of the ``GeoDataFrame`` as a string.

        Parameters
        ----------
        na : {'null', 'drop', 'keep'}, default 'null'
            Indicates how to output missing (NaN) values in the GeoDataFrame.
            See below.
        show_bbox : bool, optional, default: False
            Include bbox (bounds) in the geojson
        drop_id : bool, default: False
            Whether to retain the index of the GeoDataFrame as the id property
            in the generated GeoJSON. Default is False, but may want True
            if the index is just arbitrary row numbers.
        to_wgs84: bool, optional, default: False
            If the CRS is set on the active geometry column it is exported as
            WGS84 (EPSG:4326) to meet the `2016 GeoJSON specification
            <https://tools.ietf.org/html/rfc7946>`_.
            Set to True to force re-projection and set to False to ignore CRS. False by
            default.

        Notes
        -----
        The remaining *kwargs* are passed to json.dumps().

        Missing (NaN) values in the GeoDataFrame can be represented as follows:

        - ``null``: output the missing entries as JSON null.
        - ``drop``: remove the property from the feature. This applies to each
          feature individually so that features may have different properties.
        - ``keep``: output the missing entries as NaN.

        If the GeoDataFrame has a defined CRS, its definition will be included
        in the output unless it is equal to WGS84 (default GeoJSON CRS) or not
        possible to represent in the URN OGC format, or unless ``to_wgs84=True``
        is specified.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d, crs="EPSG:3857")
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        >>> gdf.to_json()
        '{"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"col1": "name1"}, "geometry": {"type": "Point", "coordinates": [1.0, 2.0]}}, {"id": "1", "type": "Feature", "properties": {"col1": "name2"}, "geometry": {"type": "Point", "coordinates": [2.0, 1.0]}}], "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}}}'

        Alternatively, you can write GeoJSON to file:

        >>> gdf.to_file(path, driver="GeoJSON")  # doctest: +SKIP

        See Also
        --------
        GeoDataFrame.to_file : write GeoDataFrame to file

        """

    @property
    def __geo_interface__(self) -> dict[str, Any]:  # values are arbitrary
        """Returns a ``GeoDataFrame`` as a python feature collection.

        Implements the `geo_interface`. The returned python data structure
        represents the ``GeoDataFrame`` as a GeoJSON-like
        ``FeatureCollection``.

        This differs from :meth:`to_geo_dict` only in that it is a property with
        default args instead of a method.

        CRS of the dataframe is not passed on to the output, unlike
        :meth:`~GeoDataFrame.to_json()`.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        >>> gdf.__geo_interface__
        {'type': 'FeatureCollection', 'features': [{'id': '0', 'type': 'Feature', 'properties': {'col1': 'name1'}, 'geometry': {'type': 'Point', 'coordinates': (1.0, 2.0)}, 'bbox': (1.0, 2.0, 1.0, 2.0)}, {'id': '1', 'type': 'Feature', 'properties': {'col1': 'name2'}, 'geometry': {'type': 'Point', 'coordinates': (2.0, 1.0)}, 'bbox': (2.0, 1.0, 2.0, 1.0)}], 'bbox': (1.0, 1.0, 2.0, 2.0)}
        """

    def iterfeatures(self, na: str = "null", show_bbox: bool = False, drop_id: bool = False) -> Iterator[dict[str, Incomplete]]:
        """Return an iterator that yields feature dictionaries that comply with
        __geo_interface__.

        Parameters
        ----------
        na : str, optional
            Options are {'null', 'drop', 'keep'}, default 'null'.
            Indicates how to output missing (NaN) values in the GeoDataFrame

            - null: output the missing entries as JSON null
            - drop: remove the property from the feature. This applies to each feature individually so that features may have different properties
            - keep: output the missing entries as NaN

        show_bbox : bool, optional
            Include bbox (bounds) in the geojson. Default False.
        drop_id : bool, default: False
            Whether to retain the index of the GeoDataFrame as the id property
            in the generated GeoJSON. Default is False, but may want True
            if the index is just arbitrary row numbers.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d, crs="EPSG:4326")
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        >>> feature = next(gdf.iterfeatures())
        >>> feature
        {'id': '0', 'type': 'Feature', 'properties': {'col1': 'name1'}, 'geometry': {'type': 'Point', 'coordinates': (1.0, 2.0)}}
        """

    def to_geo_dict(self, na: str = "null", show_bbox: bool = False, drop_id: bool = False) -> dict[str, Incomplete]:
        """Return a python feature collection representation of the GeoDataFrame
        as a dictionary with a list of features based on the ``__geo_interface__``
        GeoJSON-like specification.

        Parameters
        ----------
        na : str, optional
            Options are {'null', 'drop', 'keep'}, default 'null'.
            Indicates how to output missing (NaN) values in the GeoDataFrame

            - null: output the missing entries as JSON null
            - drop: remove the property from the feature. This applies to each feature individually so that features may have different properties
            - keep: output the missing entries as NaN

        show_bbox : bool, optional
            Include bbox (bounds) in the geojson. Default False.
        drop_id : bool, default: False
            Whether to retain the index of the GeoDataFrame as the id property
            in the generated dictionary. Default is False, but may want True
            if the index is just arbitrary row numbers.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d)
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        >>> gdf.to_geo_dict()
        {'type': 'FeatureCollection', 'features': [{'id': '0', 'type': 'Feature', 'properties': {'col1': 'name1'}, 'geometry': {'type': 'Point', 'coordinates': (1.0, 2.0)}}, {'id': '1', 'type': 'Feature', 'properties': {'col1': 'name2'}, 'geometry': {'type': 'Point', 'coordinates': (2.0, 1.0)}}]}

        See Also
        --------
        GeoDataFrame.to_json : return a GeoDataFrame as a GeoJSON string

        """

    def to_wkb(
        self,
        hex: bool = False,
        *,
        # shapely kwargs
        output_dimension: int = ...,
        byte_order: int = ...,
        include_srid: bool = ...,
        flavor: Literal["iso", "extended"] = ...,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Encode all geometry columns in the GeoDataFrame to WKB.

        Parameters
        ----------
        hex : bool
            If true, export the WKB as a hexadecimal string.
            The default is to return a binary bytes object.
        kwargs
            Additional keyword args will be passed to
            :func:`shapely.to_wkb`.

        Returns
        -------
        DataFrame
            geometry columns are encoded to WKB
        """

    def to_wkt(
        self,
        *,
        # shapely kwargs
        rounding_precision: int = ...,
        trim: bool = ...,
        output_dimension: int = ...,
        old_3d: bool = ...,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Encode all geometry columns in the GeoDataFrame to WKT.

        Parameters
        ----------
        kwargs
            Keyword args will be passed to :func:`shapely.to_wkt`.

        Returns
        -------
        DataFrame
            geometry columns are encoded to WKT
        """

    def to_arrow(
        self,
        *,
        index: bool | None = None,
        geometry_encoding: _GeomEncoding = "WKB",
        interleaved: bool = True,
        include_z: bool | None = None,
    ) -> ArrowTable:
        """Encode a GeoDataFrame to GeoArrow format.

        See https://geoarrow.org/ for details on the GeoArrow specification.

        This function returns a generic Arrow data object implementing
        the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_stream__``
        method). This object can then be consumed by your Arrow implementation
        of choice that supports this protocol.

        .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

        .. versionadded:: 1.0

        Parameters
        ----------
        index : bool, default None
            If ``True``, always include the dataframe's index(es) as columns
            in the file output.
            If ``False``, the index(es) will not be written to the file.
            If ``None``, the index(ex) will be included as columns in the file
            output except `RangeIndex` which is stored as metadata only.
        geometry_encoding : {'WKB', 'geoarrow' }, default 'WKB'
            The GeoArrow encoding to use for the data conversion.
        interleaved : bool, default True
            Only relevant for 'geoarrow' encoding. If True, the geometries'
            coordinates are interleaved in a single fixed size list array.
            If False, the coordinates are stored as separate arrays in a
            struct type.
        include_z : bool, default None
            Only relevant for 'geoarrow' encoding (for WKB, the dimensionality
            of the individial geometries is preserved).
            If False, return 2D geometries. If True, include the third dimension
            in the output (if a geometry has no third dimension, the z-coordinates
            will be NaN). By default, will infer the dimensionality from the
            input geometries. Note that this inference can be unreliable with
            empty geometries (for a guaranteed result, it is recommended to
            specify the keyword).

        Returns
        -------
        ArrowTable
            A generic Arrow table object with geometry columns encoded to
            GeoArrow.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> data = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(data)
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        >>> arrow_table = gdf.to_arrow()
        >>> arrow_table
        <geopandas.io._geoarrow.ArrowTable object at ...>

        The returned data object needs to be consumed by a library implementing
        the Arrow PyCapsule Protocol. For example, wrapping the data as a
        pyarrow.Table (requires pyarrow >= 14.0):

        >>> import pyarrow as pa
        >>> table = pa.table(arrow_table)
        >>> table
        pyarrow.Table
        col1: string
        geometry: binary
        ----
        col1: [["name1","name2"]]
        geometry: [[0101000000000000000000F03F0000000000000040,01010000000000000000000040000000000000F03F]]

        """

    def to_parquet(  # type: ignore[override]
        self,
        path: str | os.PathLike[str] | SupportsWrite[Incomplete],
        index: bool | None = None,
        compression: Literal["snappy", "gzip", "brotli"] | None = "snappy",
        geometry_encoding: _GeomEncoding = "WKB",
        write_covering_bbox: bool = False,
        schema_version: str | None = None,
        *,
        engine: Literal["auto", "pyarrow"] = "auto",  # Only these engines are supported, unlike pandas
        **kwargs,
    ) -> None:
        """Write a GeoDataFrame to the Parquet format.

        By default, all geometry columns present are serialized to WKB format
        in the file.

        Requires 'pyarrow'.

        .. versionadded:: 0.8

        Parameters
        ----------
        path : str, path object
        index : bool, default None
            If ``True``, always include the dataframe's index(es) as columns
            in the file output.
            If ``False``, the index(es) will not be written to the file.
            If ``None``, the index(ex) will be included as columns in the file
            output except `RangeIndex` which is stored as metadata only.
        compression : {'snappy', 'gzip', 'brotli', 'lz4', 'zstd', None}, default 'snappy'
            Name of the compression to use. Use ``None`` for no compression.
        geometry_encoding : {'WKB', 'geoarrow'}, default 'WKB'
            The encoding to use for the geometry columns. Defaults to "WKB"
            for maximum interoperability. Specify "geoarrow" to use one of the
            native GeoArrow-based single-geometry type encodings.
            Note: the "geoarrow" option is part of the newer GeoParquet 1.1
            specification, should be considered as experimental, and may not
            be supported by all readers.
        write_covering_bbox : bool, default False
            Writes the bounding box column for each row entry with column
            name 'bbox'. Writing a bbox column can be computationally
            expensive, but allows you to specify a `bbox` in :
            func:`read_parquet` for filtered reading.
            Note: this bbox column is part of the newer GeoParquet 1.1
            specification and should be considered as experimental. While
            writing the column is backwards compatible, using it for filtering
            may not be supported by all readers.
        schema_version : {'0.1.0', '0.4.0', '1.0.0', '1.1.0', None}
            GeoParquet specification version; if not provided, will default to
            latest supported stable version (1.0.0).
        kwargs
            Additional keyword arguments passed to :func:`pyarrow.parquet.write_table`.

        Examples
        --------
        >>> gdf.to_parquet('data.parquet')  # doctest: +SKIP

        See Also
        --------
        GeoDataFrame.to_feather : write GeoDataFrame to feather
        GeoDataFrame.to_file : write GeoDataFrame to file
        """

    def to_feather(
        self,
        path: str | os.PathLike[str] | SupportsWrite[Incomplete],
        index: bool | None = None,
        compression: Literal["zstd", "lz4", "uncompressed"] | None = None,
        schema_version: str | None = None,
        **kwargs,
    ) -> None:
        """Write a GeoDataFrame to the Feather format.

        Any geometry columns present are serialized to WKB format in the file.

        Requires 'pyarrow' >= 0.17.

        .. versionadded:: 0.8

        Parameters
        ----------
        path : str, path object
        index : bool, default None
            If ``True``, always include the dataframe's index(es) as columns
            in the file output.
            If ``False``, the index(es) will not be written to the file.
            If ``None``, the index(ex) will be included as columns in the file
            output except `RangeIndex` which is stored as metadata only.
        compression : {'zstd', 'lz4', 'uncompressed'}, optional
            Name of the compression to use. Use ``"uncompressed"`` for no
            compression. By default uses LZ4 if available, otherwise uncompressed.
        schema_version : {'0.1.0', '0.4.0', '1.0.0', None}
            GeoParquet specification version; if not provided will default to
            latest supported version.
        kwargs
            Additional keyword arguments passed to
            :func:`pyarrow.feather.write_feather`.

        Examples
        --------
        >>> gdf.to_feather('data.feather')  # doctest: +SKIP

        See Also
        --------
        GeoDataFrame.to_parquet : write GeoDataFrame to parquet
        GeoDataFrame.to_file : write GeoDataFrame to file
        """
    # Keep method to_file roughly in line with GeoSeries.to_file
    def to_file(
        self,
        filename: str | os.PathLike[str] | io.BytesIO,
        driver: str | None = None,
        schema: dict[str, Incomplete] | None = None,
        index: bool | None = None,
        *,
        # kwargs from `_to_file` function
        mode: Literal["w", "a"] = "w",
        crs: _ConvertibleToCRS | None = None,
        engine: Literal["fiona", "pyogrio"] | None = None,
        metadata: dict[str, str] | None = None,
        # kwargs extracted from engines
        layer: int | str | None = None,
        encoding: str | None = None,
        overwrite: bool | None = ...,
        **kwargs,  # engine and driver dependent
    ) -> None:
        """Write the ``GeoDataFrame`` to a file.

        By default, an ESRI shapefile is written, but any OGR data source
        supported by Pyogrio or Fiona can be written. A dictionary of supported OGR
        providers is available via:

        >>> import pyogrio
        >>> pyogrio.list_drivers()  # doctest: +SKIP

        Parameters
        ----------
        filename : string
            File path or file handle to write to. The path may specify a
            GDAL VSI scheme.
        driver : string, default None
            The OGR format driver used to write the vector file.
            If not specified, it attempts to infer it from the file extension.
            If no extension is specified, it saves ESRI Shapefile to a folder.
        schema : dict, default None
            If specified, the schema dictionary is passed to Fiona to
            better control how the file is written. If None, GeoPandas
            will determine the schema based on each column's dtype.
            Not supported for the "pyogrio" engine.
        index : bool, default None
            If True, write index into one or more columns (for MultiIndex).
            Default None writes the index into one or more columns only if
            the index is named, is a MultiIndex, or has a non-integer data
            type. If False, no index is written.

            .. versionadded:: 0.7
                Previously the index was not written.
        mode : string, default 'w'
            The write mode, 'w' to overwrite the existing file and 'a' to append.
            Not all drivers support appending. The drivers that support appending
            are listed in fiona.supported_drivers or
            https://github.com/Toblerity/Fiona/blob/master/fiona/drvsupport.py
        crs : pyproj.CRS, default None
            If specified, the CRS is passed to Fiona to
            better control how the file is written. If None, GeoPandas
            will determine the crs based on crs df attribute.
            The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string. The keyword
            is not supported for the "pyogrio" engine.
        engine : str, "pyogrio" or "fiona"
            The underlying library that is used to write the file. Currently, the
            supported options are "pyogrio" and "fiona". Defaults to "pyogrio" if
            installed, otherwise tries "fiona".
        metadata : dict[str, str], default None
            Optional metadata to be stored in the file. Keys and values must be
            strings. Supported only for "GPKG" driver.
        **kwargs :
            Keyword args to be passed to the engine, and can be used to write
            to multi-layer data, store data within archives (zip files), etc.
            In case of the "pyogrio" engine, the keyword arguments are passed to
            `pyogrio.write_dataframe`. In case of the "fiona" engine, the keyword
            arguments are passed to fiona.open`. For more information on possible
            keywords, type: ``import pyogrio; help(pyogrio.write_dataframe)``.

        Notes
        -----
        The format drivers will attempt to detect the encoding of your data, but
        may fail. In this case, the proper encoding can be specified explicitly
        by using the encoding keyword parameter, e.g. ``encoding='utf-8'``.

        See Also
        --------
        GeoSeries.to_file
        GeoDataFrame.to_postgis : write GeoDataFrame to PostGIS database
        GeoDataFrame.to_parquet : write GeoDataFrame to parquet
        GeoDataFrame.to_feather : write GeoDataFrame to feather

        Examples
        --------
        >>> gdf.to_file('dataframe.shp')  # doctest: +SKIP

        >>> gdf.to_file('dataframe.gpkg', driver='GPKG', layer='name')  # doctest: +SKIP

        >>> gdf.to_file('dataframe.geojson', driver='GeoJSON')  # doctest: +SKIP

        With selected drivers you can also append to a file with `mode="a"`:

        >>> gdf.to_file('dataframe.shp', mode="a")  # doctest: +SKIP

        Using the engine-specific keyword arguments it is possible to e.g. create a
        spatialite file with a custom layer name:

        >>> gdf.to_file(
        ...     'dataframe.sqlite', driver='SQLite', spatialite=True, layer='test'
        ... )  # doctest: +SKIP

        """

    @overload
    def set_crs(
        self, crs: _ConvertibleToCRS, epsg: int | None = None, inplace: bool = False, allow_override: bool = False
    ) -> Self:
        """
        Set the Coordinate Reference System (CRS) of the ``GeoDataFrame``.

        If there are multiple geometry columns within the GeoDataFrame, only
        the CRS of the active geometry column is set.

        Pass ``None`` to remove CRS from the active geometry column.

        Notes
        -----
        The underlying geometries are not transformed to this CRS. To
        transform the geometries to a new CRS, use the ``to_crs`` method.

        Parameters
        ----------
        crs : pyproj.CRS | None, optional
            The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        epsg : int, optional
            EPSG code specifying the projection.
        inplace : bool, default False
            If True, the CRS of the GeoDataFrame will be changed in place
            (while still returning the result) instead of making a copy of
            the GeoDataFrame.
        allow_override : bool, default False
            If the the GeoDataFrame already has a CRS, allow to replace the
            existing CRS, even when both are not equal.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d)
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)

        Setting CRS to a GeoDataFrame without one:

        >>> gdf.crs is None
        True

        >>> gdf = gdf.set_crs('epsg:3857')
        >>> gdf.crs  # doctest: +SKIP
        <Projected CRS: EPSG:3857>
        Name: WGS 84 / Pseudo-Mercator
        Axis Info [cartesian]:
        - X[east]: Easting (metre)
        - Y[north]: Northing (metre)
        Area of Use:
        - name: World - 85°S to 85°N
        - bounds: (-180.0, -85.06, 180.0, 85.06)
        Coordinate Operation:
        - name: Popular Visualisation Pseudo-Mercator
        - method: Popular Visualisation Pseudo Mercator
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        Overriding existing CRS:

        >>> gdf = gdf.set_crs(4326, allow_override=True)

        Without ``allow_override=True``, ``set_crs`` returns an error if you try to
        override CRS.

        See Also
        --------
        GeoDataFrame.to_crs : re-project to another CRS

        """

    @overload
    def set_crs(
        self, crs: _ConvertibleToCRS | None = None, *, epsg: int, inplace: bool = False, allow_override: bool = False
    ) -> Self: ...
    @overload
    def set_crs(self, crs: _ConvertibleToCRS | None, epsg: int, inplace: bool = False, allow_override: bool = False) -> Self: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS, epsg: int | None = None, inplace: Literal[False] = False) -> Self:
        """Transform geometries to a new coordinate reference system.

        Transform all geometries in an active geometry column to a different coordinate
        reference system.  The ``crs`` attribute on the current GeoSeries must
        be set.  Either ``crs`` or ``epsg`` may be specified for output.

        This method will transform all points in all objects. It has no notion
        of projecting entire geometries.  All segments joining points are
        assumed to be lines in the current projection, not geodesics. Objects
        crossing the dateline (or other projection boundary) will have
        undesirable behavior.

        Parameters
        ----------
        crs : pyproj.CRS, optional if `epsg` is specified
            The value can be anything accepted by
            :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        epsg : int, optional if `crs` is specified
            EPSG code specifying output projection.
        inplace : bool, optional, default: False
            Whether to return a new GeoDataFrame or do the transformation in
            place.

        Returns
        -------
        GeoDataFrame

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {'col1': ['name1', 'name2'], 'geometry': [Point(1, 2), Point(2, 1)]}
        >>> gdf = geopandas.GeoDataFrame(d, crs=4326)
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)
        >>> gdf.crs  # doctest: +SKIP
        <Geographic 2D CRS: EPSG:4326>
        Name: WGS 84
        Axis Info [ellipsoidal]:
        - Lat[north]: Geodetic latitude (degree)
        - Lon[east]: Geodetic longitude (degree)
        Area of Use:
        - name: World
        - bounds: (-180.0, -90.0, 180.0, 90.0)
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        >>> gdf = gdf.to_crs(3857)
        >>> gdf
            col1                       geometry
        0  name1  POINT (111319.491 222684.209)
        1  name2  POINT (222638.982 111325.143)
        >>> gdf.crs  # doctest: +SKIP
        <Projected CRS: EPSG:3857>
        Name: WGS 84 / Pseudo-Mercator
        Axis Info [cartesian]:
        - X[east]: Easting (metre)
        - Y[north]: Northing (metre)
        Area of Use:
        - name: World - 85°S to 85°N
        - bounds: (-180.0, -85.06, 180.0, 85.06)
        Coordinate Operation:
        - name: Popular Visualisation Pseudo-Mercator
        - method: Popular Visualisation Pseudo Mercator
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        See Also
        --------
        GeoDataFrame.set_crs : assign CRS without re-projection
        """

    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None = None, *, epsg: int, inplace: Literal[False] = False) -> Self: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None, epsg: int, inplace: Literal[False] = False) -> Self: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS, epsg: int | None = None, *, inplace: Literal[True]) -> None: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS, epsg: int | None, inplace: Literal[True]) -> None: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None = None, *, epsg: int, inplace: Literal[True]) -> None: ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None, epsg: int, inplace: Literal[True]) -> None: ...
    def estimate_utm_crs(self, datum_name: str = "WGS 84") -> CRS:
        """Return the estimated UTM CRS based on the bounds of the dataset.

        .. versionadded:: 0.9

        Parameters
        ----------
        datum_name : str, optional
            The name of the datum to use in the query. Default is WGS 84.

        Returns
        -------
        pyproj.CRS

        Examples
        --------
        >>> import geodatasets
        >>> df = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_health")
        ... )
        >>> df.estimate_utm_crs()  # doctest: +SKIP
        <Derived Projected CRS: EPSG:32616>
        Name: WGS 84 / UTM zone 16N
        Axis Info [cartesian]:
        - E[east]: Easting (metre)
        - N[north]: Northing (metre)
        Area of Use:
        - name: Between 90°W and 84°W, northern hemisphere between equator and 84°N...
        - bounds: (-90.0, 0.0, -84.0, 84.0)
        Coordinate Operation:
        - name: UTM zone 16N
        - method: Transverse Mercator
        Datum: World Geodetic System 1984 ensemble
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich
        """
    # def __getitem__(self, key): ...
    # def __setitem__(self, key, value) -> None: ...
    def copy(self, deep: bool = True) -> Self:
        """
        Two-dimensional, size-mutable, potentially heterogeneous tabular data.

        Data structure also contains labeled axes (rows and columns).
        Arithmetic operations align on both row and column labels. Can be
        thought of as a dict-like container for Series objects. The primary
        pandas data structure.

        Parameters
        ----------
        data : ndarray (structured or homogeneous), Iterable, dict, or DataFrame
            Dict can contain Series, arrays, constants, dataclass or list-like objects. If
            data is a dict, column order follows insertion-order. If a dict contains Series
            which have an index defined, it is aligned by its index. This alignment also
            occurs if data is a Series or a DataFrame itself. Alignment is done on
            Series/DataFrame inputs.

            If data is a list of dicts, column order follows insertion-order.

        index : Index or array-like
            Index to use for resulting frame. Will default to RangeIndex if
            no indexing information part of input data and no index provided.
        columns : Index or array-like
            Column labels to use for resulting frame when data does not have them,
            defaulting to RangeIndex(0, 1, 2, ..., n). If data contains column labels,
            will perform column selection instead.
        dtype : dtype, default None
            Data type to force. Only a single dtype is allowed. If None, infer.
        copy : bool or None, default None
            Copy data from inputs.
            For dict data, the default of None behaves like ``copy=True``.  For DataFrame
            or 2d ndarray input, the default of None behaves like ``copy=False``.
            If data is a dict containing one or more Series (possibly of different dtypes),
            ``copy=False`` will ensure that these inputs are not copied.

            .. versionchanged:: 1.3.0

        See Also
        --------
        DataFrame.from_records : Constructor from tuples, also record arrays.
        DataFrame.from_dict : From dicts of Series, arrays, or dicts.
        read_csv : Read a comma-separated values (csv) file into DataFrame.
        read_table : Read general delimited file into DataFrame.
        read_clipboard : Read text from clipboard into DataFrame.

        Notes
        -----
        Please reference the :ref:`User Guide <basics.dataframe>` for more information.

        Examples
        --------
        Constructing DataFrame from a dictionary.

        >>> d = {'col1': [1, 2], 'col2': [3, 4]}
        >>> df = pd.DataFrame(data=d)
        >>> df
           col1  col2
        0     1     3
        1     2     4

        Notice that the inferred dtype is int64.

        >>> df.dtypes
        col1    int64
        col2    int64
        dtype: object

        To enforce a single dtype:

        >>> df = pd.DataFrame(data=d, dtype=np.int8)
        >>> df.dtypes
        col1    int8
        col2    int8
        dtype: object

        Constructing DataFrame from a dictionary including Series:

        >>> d = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}
        >>> pd.DataFrame(data=d, index=[0, 1, 2, 3])
           col1  col2
        0     0   NaN
        1     1   NaN
        2     2   2.0
        3     3   3.0

        Constructing DataFrame from numpy ndarray:

        >>> df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        ...                    columns=['a', 'b', 'c'])
        >>> df2
           a  b  c
        0  1  2  3
        1  4  5  6
        2  7  8  9

        Constructing DataFrame from a numpy ndarray that has labeled columns:

        >>> data = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)],
        ...                 dtype=[("a", "i4"), ("b", "i4"), ("c", "i4")])
        >>> df3 = pd.DataFrame(data, columns=['c', 'a'])
        ...
        >>> df3
           c  a
        0  3  1
        1  6  4
        2  9  7

        Constructing DataFrame from dataclass:

        >>> from dataclasses import make_dataclass
        >>> Point = make_dataclass("Point", [("x", int), ("y", int)])
        >>> pd.DataFrame([Point(0, 0), Point(0, 3), Point(2, 3)])
           x  y
        0  0  0
        1  0  3
        2  2  3

        Constructing DataFrame from Series/DataFrame:

        >>> ser = pd.Series([1, 2, 3], index=["a", "b", "c"])
        >>> df = pd.DataFrame(data=ser, index=["a", "c"])
        >>> df
           0
        a  1
        c  3

        >>> df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
        >>> df2 = pd.DataFrame(data=df1, index=["a", "c"])
        >>> df2
           x
        a  1
        c  3
        """
    # def merge(self, *args, **kwargs) -> GeoDataFrame | pd.DataFrame: ...
    def apply(  # type: ignore[override]
        self,
        func: Callable[..., Incomplete],
        axis: Axis = 0,
        raw: bool = False,
        result_type: Literal["expand", "reduce", "broadcast"] | None = None,
        args: tuple[Any, ...] = (),  # type inexpressible in the typing system
        *,
        by_row: Literal[False, "compat"] = "compat",
        engine: Literal["python", "numba"] = "python",
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ) -> pd.DataFrame | pd.Series[Incomplete]:
        """
        Two-dimensional, size-mutable, potentially heterogeneous tabular data.

        Data structure also contains labeled axes (rows and columns).
        Arithmetic operations align on both row and column labels. Can be
        thought of as a dict-like container for Series objects. The primary
        pandas data structure.

        Parameters
        ----------
        data : ndarray (structured or homogeneous), Iterable, dict, or DataFrame
            Dict can contain Series, arrays, constants, dataclass or list-like objects. If
            data is a dict, column order follows insertion-order. If a dict contains Series
            which have an index defined, it is aligned by its index. This alignment also
            occurs if data is a Series or a DataFrame itself. Alignment is done on
            Series/DataFrame inputs.

            If data is a list of dicts, column order follows insertion-order.

        index : Index or array-like
            Index to use for resulting frame. Will default to RangeIndex if
            no indexing information part of input data and no index provided.
        columns : Index or array-like
            Column labels to use for resulting frame when data does not have them,
            defaulting to RangeIndex(0, 1, 2, ..., n). If data contains column labels,
            will perform column selection instead.
        dtype : dtype, default None
            Data type to force. Only a single dtype is allowed. If None, infer.
        copy : bool or None, default None
            Copy data from inputs.
            For dict data, the default of None behaves like ``copy=True``.  For DataFrame
            or 2d ndarray input, the default of None behaves like ``copy=False``.
            If data is a dict containing one or more Series (possibly of different dtypes),
            ``copy=False`` will ensure that these inputs are not copied.

            .. versionchanged:: 1.3.0

        See Also
        --------
        DataFrame.from_records : Constructor from tuples, also record arrays.
        DataFrame.from_dict : From dicts of Series, arrays, or dicts.
        read_csv : Read a comma-separated values (csv) file into DataFrame.
        read_table : Read general delimited file into DataFrame.
        read_clipboard : Read text from clipboard into DataFrame.

        Notes
        -----
        Please reference the :ref:`User Guide <basics.dataframe>` for more information.

        Examples
        --------
        Constructing DataFrame from a dictionary.

        >>> d = {'col1': [1, 2], 'col2': [3, 4]}
        >>> df = pd.DataFrame(data=d)
        >>> df
           col1  col2
        0     1     3
        1     2     4

        Notice that the inferred dtype is int64.

        >>> df.dtypes
        col1    int64
        col2    int64
        dtype: object

        To enforce a single dtype:

        >>> df = pd.DataFrame(data=d, dtype=np.int8)
        >>> df.dtypes
        col1    int8
        col2    int8
        dtype: object

        Constructing DataFrame from a dictionary including Series:

        >>> d = {'col1': [0, 1, 2, 3], 'col2': pd.Series([2, 3], index=[2, 3])}
        >>> pd.DataFrame(data=d, index=[0, 1, 2, 3])
           col1  col2
        0     0   NaN
        1     1   NaN
        2     2   2.0
        3     3   3.0

        Constructing DataFrame from numpy ndarray:

        >>> df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        ...                    columns=['a', 'b', 'c'])
        >>> df2
           a  b  c
        0  1  2  3
        1  4  5  6
        2  7  8  9

        Constructing DataFrame from a numpy ndarray that has labeled columns:

        >>> data = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)],
        ...                 dtype=[("a", "i4"), ("b", "i4"), ("c", "i4")])
        >>> df3 = pd.DataFrame(data, columns=['c', 'a'])
        ...
        >>> df3
           c  a
        0  3  1
        1  6  4
        2  9  7

        Constructing DataFrame from dataclass:

        >>> from dataclasses import make_dataclass
        >>> Point = make_dataclass("Point", [("x", int), ("y", int)])
        >>> pd.DataFrame([Point(0, 0), Point(0, 3), Point(2, 3)])
           x  y
        0  0  0
        1  0  3
        2  2  3

        Constructing DataFrame from Series/DataFrame:

        >>> ser = pd.Series([1, 2, 3], index=["a", "b", "c"])
        >>> df = pd.DataFrame(data=ser, index=["a", "c"])
        >>> df
           0
        a  1
        c  3

        >>> df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
        >>> df2 = pd.DataFrame(data=df1, index=["a", "c"])
        >>> df2
           x
        a  1
        c  3
        """

    def __finalize__(self, other, method: str | None = None, **kwargs) -> Self:
        """Propagate metadata from other to self."""

    def dissolve(
        self,
        by: GroupByObject | None = None,
        aggfunc: AggFuncTypeFrame = "first",
        as_index: bool = True,
        level: IndexLabel | None = None,
        sort: bool = True,
        observed: bool = False,
        dropna: bool = True,
        method: Literal["coverage", "unary", "disjoint_subset"] = "unary",
        grid_size: float | None = None,
        **kwargs,
    ) -> GeoDataFrame:
        """
        Dissolve geometries within `groupby` into single observation.
        This is accomplished by applying the `union_all` method
        to all geometries within a groupself.

        Observations associated with each `groupby` group will be aggregated
        using the `aggfunc`.

        Parameters
        ----------
        by : str or list-like, default None
            Column(s) whose values define the groups to be dissolved. If None,
            the entire GeoDataFrame is considered as a single group. If a list-like
            object is provided, the values in the list are treated as categorical
            labels, and polygons will be combined based on the equality of
            these categorical labels.
        aggfunc : function or string, default "first"
            Aggregation function for manipulation of data associated
            with each group. Passed to pandas `groupby.agg` method.
            Accepted combinations are:

            - function
            - string function name
            - list of functions and/or function names, e.g. [np.sum, 'mean']
            - dict of axis labels -> functions, function names or list of such.
        as_index : boolean, default True
            If true, groupby columns become index of result.
        level : int or str or sequence of int or sequence of str, default None
            If the axis is a MultiIndex (hierarchical), group by a
            particular level or levels.
        sort : bool, default True
            Sort group keys. Get better performance by turning this off.
            Note this does not influence the order of observations within
            each group. Groupby preserves the order of rows within each group.
        observed : bool, default False
            This only applies if any of the groupers are Categoricals.
            If True: only show observed values for categorical groupers.
            If False: show all values for categorical groupers.
        dropna : bool, default True
            If True, and if group keys contain NA values, NA values
            together with row/column will be dropped. If False, NA
            values will also be treated as the key in groups.
        method : str (default ``"unary"``)
            The method to use for the union. Options are:

            * ``"unary"``: use the unary union algorithm. This option is the most robust
              but can be slow for large numbers of geometries (default).
            * ``"coverage"``: use the coverage union algorithm. This option is optimized
              for non-overlapping polygons and can be significantly faster than the
              unary union algorithm. However, it can produce invalid geometries if the
              polygons overlap.
            * ``"disjoint_subset:``: use the disjoint subset union algorithm. This
              option is optimized for inputs that can be divided into subsets that do
              not intersect. If there is only one such subset, performance can be
              expected to be worse than ``"unary"``.  Requires Shapely >= 2.1.


        grid_size : float, default None
            When grid size is specified, a fixed-precision space is used to perform the
            union operations. This can be useful when unioning geometries that are not
            perfectly snapped or to avoid geometries not being unioned because of
            `robustness issues <https://libgeos.org/usage/faq/#why-doesnt-a-computed-point-lie-exactly-on-a-line>`_.
            The inputs are first snapped to a grid of the given size. When a line
            segment of a geometry is within tolerance off a vertex of another geometry,
            this vertex will be inserted in the line segment. Finally, the result
            vertices are computed on the same grid. Is only supported for ``method``
            ``"unary"``. If None, the highest precision of the inputs will be used.
            Defaults to None.

            .. versionadded:: 1.1.0
        **kwargs :
            Keyword arguments to be passed to the pandas `DataFrameGroupby.agg` method
            which is used by `dissolve`. In particular, `numeric_only` may be
            supplied, which will be required in pandas 2.0 for certain aggfuncs.

            .. versionadded:: 0.13.0

        Returns
        -------
        GeoDataFrame

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> d = {
        ...     "col1": ["name1", "name2", "name1"],
        ...     "geometry": [Point(1, 2), Point(2, 1), Point(0, 1)],
        ... }
        >>> gdf = geopandas.GeoDataFrame(d, crs=4326)
        >>> gdf
            col1     geometry
        0  name1  POINT (1 2)
        1  name2  POINT (2 1)
        2  name1  POINT (0 1)

        >>> dissolved = gdf.dissolve('col1')
        >>> dissolved  # doctest: +SKIP
                                geometry
        col1
        name1  MULTIPOINT ((0 1), (1 2))
        name2                POINT (2 1)

        See Also
        --------
        GeoDataFrame.explode : explode multi-part geometries into single geometries

        """

    def explode(self, column: IndexLabel | None = None, ignore_index: bool = False, index_parts: bool = False) -> Self:
        """
        Explode multi-part geometries into multiple single geometries.

        Each row containing a multi-part geometry will be split into
        multiple rows with single geometries, thereby increasing the vertical
        size of the GeoDataFrame.

        Parameters
        ----------
        column : string, default None
            Column to explode. In the case of a geometry column, multi-part
            geometries are converted to single-part.
            If None, the active geometry column is used.
        ignore_index : bool, default False
            If True, the resulting index will be labelled 0, 1, …, n - 1,
            ignoring `index_parts`.
        index_parts : boolean, default False
            If True, the resulting index will be a multi-index (original
            index with an additional level indicating the multiple
            geometries: a new zero-based index for each single part geometry
            per multi-part geometry).

        Returns
        -------
        GeoDataFrame
            Exploded geodataframe with each single geometry
            as a separate entry in the geodataframe.

        Examples
        --------
        >>> from shapely.geometry import MultiPoint
        >>> d = {
        ...     "col1": ["name1", "name2"],
        ...     "geometry": [
        ...         MultiPoint([(1, 2), (3, 4)]),
        ...         MultiPoint([(2, 1), (0, 0)]),
        ...     ],
        ... }
        >>> gdf = geopandas.GeoDataFrame(d, crs=4326)
        >>> gdf
            col1               geometry
        0  name1  MULTIPOINT ((1 2), (3 4))
        1  name2  MULTIPOINT ((2 1), (0 0))

        >>> exploded = gdf.explode(index_parts=True)
        >>> exploded
              col1     geometry
        0 0  name1  POINT (1 2)
          1  name1  POINT (3 4)
        1 0  name2  POINT (2 1)
          1  name2  POINT (0 0)

        >>> exploded = gdf.explode(index_parts=False)
        >>> exploded
            col1     geometry
        0  name1  POINT (1 2)
        0  name1  POINT (3 4)
        1  name2  POINT (2 1)
        1  name2  POINT (0 0)

        >>> exploded = gdf.explode(ignore_index=True)
        >>> exploded
            col1     geometry
        0  name1  POINT (1 2)
        1  name1  POINT (3 4)
        2  name2  POINT (2 1)
        3  name2  POINT (0 0)

        See Also
        --------
        GeoDataFrame.dissolve : dissolve geometries into a single observation.

        """

    def to_postgis(
        self,
        name: str,
        con: _SQLConnection,
        schema: str | None = None,
        if_exists: Literal["fail", "replace", "append"] = "fail",
        index: bool = False,
        index_label: IndexLabel | None = None,
        chunksize: int | None = None,
        dtype: dict[Any, Incomplete] | None = None,  # columns can be of "any" type
    ) -> None:
        """
        Upload GeoDataFrame into PostGIS database.

        This method requires SQLAlchemy and GeoAlchemy2, and a PostgreSQL
        Python driver (psycopg or psycopg2) to be installed.

        It is also possible to use :meth:`~GeoDataFrame.to_file` to write to a database.
        Especially for file geodatabases like GeoPackage or SpatiaLite this can be
        easier.

        Parameters
        ----------
        name : str
            Name of the target table.
        con : sqlalchemy.engine.Connection or sqlalchemy.engine.Engine
            Active connection to the PostGIS database.
        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            How to behave if the table already exists:

            - fail: Raise a ValueError.
            - replace: Drop the table before inserting new values.
            - append: Insert new values to the existing table.
        schema : string, optional
            Specify the schema. If None, use default schema: 'public'.
        index : bool, default False
            Write DataFrame index as a column.
            Uses *index_label* as the column name in the table.
        index_label : string or sequence, default None
            Column label for index column(s).
            If None is given (default) and index is True,
            then the index names are used.
        chunksize : int, optional
            Rows will be written in batches of this size at a time.
            By default, all rows will be written at once.
        dtype : dict of column name to SQL type, default None
            Specifying the datatype for columns.
            The keys should be the column names and the values
            should be the SQLAlchemy types.

        Examples
        --------
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("postgresql://myusername:mypassword@myhost:5432/mydatabase")  # doctest: +SKIP
        >>> gdf.to_postgis("my_table", engine)  # doctest: +SKIP

        See Also
        --------
        GeoDataFrame.to_file : write GeoDataFrame to file
        read_postgis : read PostGIS database to GeoDataFrame

        """

    @property
    def plot(self) -> GeoplotAccessor:
        """
        Custom property-like object.

        A descriptor for caching accessors.

        Parameters
        ----------
        name : str
            Namespace that will be accessed under, e.g. ``df.foo``.
        accessor : cls
            Class with the extension methods.

        Notes
        -----
        For accessor, The class's __init__ method assumes that one of
        ``Series``, ``DataFrame`` or ``Index`` as the
        single argument ``data``.
        """

    @doc(_explore)  # pyright: ignore[reportUnknownArgumentType]
    def explore(self, *args, **kwargs):  # signature of `_explore` copied in `@doc`
        """Explore data in interactive map based on GeoPandas and folium/leaflet.js.

        Generate an interactive leaflet map based on :class:`~geopandas.GeoDataFrame`

        Parameters
        ----------
        column : str, np.array, pd.Series (default None)
            The name of the dataframe column, :class:`numpy.array`,
            or :class:`pandas.Series` to be plotted. If :class:`numpy.array` or
            :class:`pandas.Series` are used then it must have same length as dataframe.
        cmap : str, matplotlib.Colormap, branca.colormap or function (default None)
            The name of a colormap recognized by ``matplotlib``, a list-like of colors,
            :class:`matplotlib.colors.Colormap`, a :class:`branca.colormap.ColorMap` or
            function that returns a named color or hex based on the column
            value, e.g.::

                def my_colormap(value):  # scalar value defined in 'column'
                    if value > 1:
                        return "green"
                    return "red"

        color : str, array-like (default None)
            Named color or a list-like of colors (named or hex).
        m : folium.Map (default None)
            Existing map instance on which to draw the plot.
        tiles : str, xyzservices.TileProvider (default 'OpenStreetMap Mapnik')
            Map tileset to use. Can choose from the list supported by folium, query a
            :class:`xyzservices.TileProvider` by a name from ``xyzservices.providers``,
            pass :class:`xyzservices.TileProvider` object or pass custom XYZ URL.
            The current list of built-in providers (when ``xyzservices`` is not available):

            ``["OpenStreetMap", "CartoDB positron", “CartoDB dark_matter"]``

            You can pass a custom tileset to Folium by passing a Leaflet-style URL
            to the tiles parameter: ``http://{s}.yourtiles.com/{z}/{x}/{y}.png``.
            Be sure to check their terms and conditions and to provide attribution with
            the ``attr`` keyword.
        attr : str (default None)
            Map tile attribution; only required if passing custom tile URL.
        tooltip : bool, str, int, list (default True)
            Display GeoDataFrame attributes when hovering over the object.
            ``True`` includes all columns. ``False`` removes tooltip. Pass string or list of
            strings to specify a column(s). Integer specifies first n columns to be
            included. Defaults to ``True``.
        popup : bool, str, int, list (default False)
            Input GeoDataFrame attributes for object displayed when clicking.
            ``True`` includes all columns. ``False`` removes popup. Pass string or list of
            strings to specify a column(s). Integer specifies first n columns to be
            included. Defaults to ``False``.
        highlight : bool (default True)
            Enable highlight functionality when hovering over a geometry.
        categorical : bool (default False)
            If ``False``, ``cmap`` will reflect numerical values of the
            column being plotted. For non-numerical columns, this
            will be set to True.
        legend : bool (default True)
            Plot a legend in choropleth plots.
            Ignored if no ``column`` is given.
        scheme : str (default None)
            Name of a choropleth classification scheme (requires ``mapclassify`` >= 2.4.0).
            A :func:`mapclassify.classify` will be used
            under the hood. Supported are all schemes provided by ``mapclassify`` (e.g.
            ``'BoxPlot'``, ``'EqualInterval'``, ``'FisherJenks'``, ``'FisherJenksSampled'``,
            ``'HeadTailBreaks'``, ``'JenksCaspall'``, ``'JenksCaspallForced'``,
            ``'JenksCaspallSampled'``, ``'MaxP'``, ``'MaximumBreaks'``,
            ``'NaturalBreaks'``, ``'Quantiles'``, ``'Percentiles'``, ``'StdMean'``,
            ``'UserDefined'``). Arguments can be passed in ``classification_kwds``.
        k : int (default 5)
            Number of classes
        vmin : None or float (default None)
            Minimum value of ``cmap``. If ``None``, the minimum data value
            in the column to be plotted is used.
        vmax : None or float (default None)
            Maximum value of ``cmap``. If ``None``, the maximum data value
            in the column to be plotted is used.
        width : pixel int or percentage string (default: '100%')
            Width of the folium :class:`~folium.folium.Map`. If the argument
            m is given explicitly, width is ignored.
        height : pixel int or percentage string (default: '100%')
            Height of the folium :class:`~folium.folium.Map`. If the argument
            m is given explicitly, height is ignored.
        categories : list-like
            Ordered list-like object of categories to be used for categorical plot.
        classification_kwds : dict (default None)
            Keyword arguments to pass to mapclassify
        control_scale : bool, (default True)
            Whether to add a control scale on the map.
        marker_type : str, folium.Circle, folium.CircleMarker, folium.Marker (default None)
            Allowed string options are ('marker', 'circle', 'circle_marker'). Defaults to
            folium.CircleMarker.
        marker_kwds: dict (default {})
            Additional keywords to be passed to the selected ``marker_type``, e.g.:

            radius : float (default 2 for ``circle_marker`` and 50 for ``circle``))
                Radius of the circle, in meters (for ``circle``) or pixels
                (for ``circle_marker``).
            fill : bool (default True)
                Whether to fill the ``circle`` or ``circle_marker`` with color.
            icon : folium.map.Icon
                the :class:`folium.map.Icon` object to use to render the marker.
            draggable : bool (default False)
                Set to True to be able to drag the marker around the map.

        style_kwds : dict (default {})
            Additional style to be passed to folium ``style_function``:

            stroke : bool (default True)
                Whether to draw stroke along the path. Set it to ``False`` to
                disable borders on polygons or circles.
            color : str
                Stroke color
            weight : int
                Stroke width in pixels
            opacity : float (default 1.0)
                Stroke opacity
            fill : boolean (default True)
                Whether to fill the path with color. Set it to ``False`` to
                disable filling on polygons or circles.
            fillColor : str
                Fill color. Defaults to the value of the color option
            fillOpacity : float (default 0.5)
                Fill opacity.
            style_function : callable
                Function mapping a GeoJson Feature to a style ``dict``.

                * Style properties :func:`folium.vector_layers.path_options`
                * GeoJson features :class:`GeoDataFrame.__geo_interface__`

                e.g.::

                    lambda x: {"color":"red" if x["properties"]["gdp_md_est"]<10**6
                                                 else "blue"}

            Plus all supported by :func:`folium.vector_layers.path_options`. See the
            documentation of :class:`folium.features.GeoJson` for details.

        highlight_kwds : dict (default {})
            Style to be passed to folium highlight_function. Uses the same keywords
            as ``style_kwds``. When empty, defaults to ``{"fillOpacity": 0.75}``.
        missing_kwds : dict (default {})
            Additional style for missing values:

            color : str
                Color of missing values. Defaults to ``None``, which uses Folium's default.
            label : str (default "NaN")
                Legend entry for missing values.
        tooltip_kwds : dict (default {})
            Additional keywords to be passed to :class:`folium.features.GeoJsonTooltip`,
            e.g. ``aliases``, ``labels``, or ``sticky``.
        popup_kwds : dict (default {})
            Additional keywords to be passed to :class:`folium.features.GeoJsonPopup`,
            e.g. ``aliases`` or ``labels``.
        legend_kwds : dict (default {})
            Additional keywords to be passed to the legend.

            Currently supported customisation:

            caption : string
                Custom caption of the legend. Defaults to the column name.

            Additional accepted keywords when ``scheme`` is specified:

            colorbar : bool (default True)
                An option to control the style of the legend. If True, continuous
                colorbar will be used. If False, categorical legend will be used for bins.
            scale : bool (default True)
                Scale bins along the colorbar axis according to the bin edges (True)
                or use the equal length for each bin (False)
            fmt : string (default "{:.2f}")
                A formatting specification for the bin edges of the classes in the
                legend. For example, to have no decimals: ``{"fmt": "{:.0f}"}``. Applies
                if ``colorbar=False``.
            labels : list-like
                A list of legend labels to override the auto-generated labels.
                Needs to have the same number of elements as the number of
                classes (`k`). Applies if ``colorbar=False``.
            interval : boolean (default False)
                An option to control brackets from mapclassify legend.
                If True, open/closed interval brackets are shown in the legend.
                Applies if ``colorbar=False``.
            max_labels : int, default 10
                Maximum number of colorbar tick labels (requires branca>=0.5.0)
        map_kwds : dict (default {})
            Additional keywords to be passed to folium :class:`~folium.folium.Map`,
            e.g. ``dragging``, or ``scrollWheelZoom``.


        **kwargs : dict
            Additional options to be passed on to the folium object.

        Returns
        -------
        m : folium.folium.Map
            folium :class:`~folium.folium.Map` instance

        Examples
        --------
        >>> import geodatasets
        >>> df = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_health")
        ... )
        >>> df.head(2)  # doctest: +SKIP
           ComAreaID  ...                                           geometry
        0         35  ...  POLYGON ((-87.60914 41.84469, -87.60915 41.844...
        1         36  ...  POLYGON ((-87.59215 41.81693, -87.59231 41.816...

        [2 rows x 87 columns]

        >>> df.explore("Pop2012", cmap="Blues")  # doctest: +SKIP
        """

    def sjoin(
        self,
        df: GeoDataFrame,
        how: Literal["left", "right", "inner"] = "inner",
        predicate: str = "intersects",
        lsuffix: str = "left",
        rsuffix: str = "right",
        *,
        # **kwargs passed to geopandas.sjoin
        distance: float | ArrayLike | None = None,
        on_attribute: str | Sequence[str] | None = None,
        **kwargs,
    ) -> GeoDataFrame:
        """Spatial join of two GeoDataFrames.

        See the User Guide page :doc:`../../user_guide/mergingdata` for details.

        Parameters
        ----------
        df : GeoDataFrame
        how : string, default 'inner'
            The type of join:

            * 'left': use keys from left_df; retain only left_df geometry column
            * 'right': use keys from right_df; retain only right_df geometry column
            * 'inner': use intersection of keys from both dfs; retain only
              left_df geometry column

        predicate : string, default 'intersects'
            Binary predicate. Valid values are determined by the spatial index used.
            You can check the valid values in left_df or right_df as
            ``left_df.sindex.valid_query_predicates`` or
            ``right_df.sindex.valid_query_predicates``
        lsuffix : string, default 'left'
            Suffix to apply to overlapping column names (left GeoDataFrame).
        rsuffix : string, default 'right'
            Suffix to apply to overlapping column names (right GeoDataFrame).
        distance : number or array_like, optional
            Distance(s) around each input geometry within which to query the tree
            for the 'dwithin' predicate. If array_like, must be
            one-dimesional with length equal to length of left GeoDataFrame.
            Required if ``predicate='dwithin'``.
        on_attribute : string, list or tuple
            Column name(s) to join on as an additional join restriction on top
            of the spatial predicate. These must be found in both DataFrames.
            If set, observations are joined only if the predicate applies
            and values in specified columns match.

        Examples
        --------
        >>> import geodatasets
        >>> chicago = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_commpop")
        ... )
        >>> groceries = geopandas.read_file(
        ...     geodatasets.get_path("geoda.groceries")
        ... ).to_crs(chicago.crs)

        >>> chicago.head()  # doctest: +SKIP
                 community  ...                                           geometry
        0          DOUGLAS  ...  MULTIPOLYGON (((-87.60914 41.84469, -87.60915 ...
        1          OAKLAND  ...  MULTIPOLYGON (((-87.59215 41.81693, -87.59231 ...
        2      FULLER PARK  ...  MULTIPOLYGON (((-87.62880 41.80189, -87.62879 ...
        3  GRAND BOULEVARD  ...  MULTIPOLYGON (((-87.60671 41.81681, -87.60670 ...
        4          KENWOOD  ...  MULTIPOLYGON (((-87.59215 41.81693, -87.59215 ...

        [5 rows x 9 columns]

        >>> groceries.head()  # doctest: +SKIP
           OBJECTID     Ycoord  ...  Category                           geometry
        0        16  41.973266  ...       NaN  MULTIPOINT ((-87.65661 41.97321))
        1        18  41.696367  ...       NaN  MULTIPOINT ((-87.68136 41.69713))
        2        22  41.868634  ...       NaN  MULTIPOINT ((-87.63918 41.86847))
        3        23  41.877590  ...       new  MULTIPOINT ((-87.65495 41.87783))
        4        27  41.737696  ...       NaN  MULTIPOINT ((-87.62715 41.73623))
        [5 rows x 8 columns]

        >>> groceries_w_communities = groceries.sjoin(chicago)
        >>> groceries_w_communities[["OBJECTID", "community", "geometry"]].head()
           OBJECTID       community                           geometry
        0        16          UPTOWN  MULTIPOINT ((-87.65661 41.97321))
        1        18     MORGAN PARK  MULTIPOINT ((-87.68136 41.69713))
        2        22  NEAR WEST SIDE  MULTIPOINT ((-87.63918 41.86847))
        3        23  NEAR WEST SIDE  MULTIPOINT ((-87.65495 41.87783))
        4        27         CHATHAM  MULTIPOINT ((-87.62715 41.73623))

        Notes
        -----
        Every operation in GeoPandas is planar, i.e. the potential third
        dimension is not taken into account.

        See Also
        --------
        GeoDataFrame.sjoin_nearest : nearest neighbor join
        sjoin : equivalent top-level function
        """

    def sjoin_nearest(
        self,
        right: GeoDataFrame,
        how: Literal["left", "right", "inner"] = "inner",
        max_distance: float | None = None,
        lsuffix: str = "left",
        rsuffix: str = "right",
        distance_col: str | None = None,
        exclusive: bool = False,
    ) -> GeoDataFrame:
        """
        Spatial join of two GeoDataFrames based on the distance between their
        geometries.

        Results will include multiple output records for a single input record
        where there are multiple equidistant nearest or intersected neighbors.

        See the User Guide page
        https://geopandas.readthedocs.io/en/latest/docs/user_guide/mergingdata.html
        for more details.


        Parameters
        ----------
        right : GeoDataFrame
        how : string, default 'inner'
            The type of join:

            * 'left': use keys from left_df; retain only left_df geometry column
            * 'right': use keys from right_df; retain only right_df geometry column
            * 'inner': use intersection of keys from both dfs; retain only
              left_df geometry column

        max_distance : float, default None
            Maximum distance within which to query for nearest geometry.
            Must be greater than 0.
            The max_distance used to search for nearest items in the tree may have a
            significant impact on performance by reducing the number of input
            geometries that are evaluated for nearest items in the tree.
        lsuffix : string, default 'left'
            Suffix to apply to overlapping column names (left GeoDataFrame).
        rsuffix : string, default 'right'
            Suffix to apply to overlapping column names (right GeoDataFrame).
        distance_col : string, default None
            If set, save the distances computed between matching geometries under a
            column of this name in the joined GeoDataFrame.
        exclusive : bool, optional, default False
            If True, the nearest geometries that are equal to the input geometry
            will not be returned, default False.

        Examples
        --------
        >>> import geodatasets
        >>> groceries = geopandas.read_file(
        ...     geodatasets.get_path("geoda.groceries")
        ... )
        >>> chicago = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_health")
        ... ).to_crs(groceries.crs)

        >>> chicago.head()  # doctest: +SKIP
           ComAreaID  ...                                           geometry
        0         35  ...  POLYGON ((-87.60914 41.84469, -87.60915 41.844...
        1         36  ...  POLYGON ((-87.59215 41.81693, -87.59231 41.816...
        2         37  ...  POLYGON ((-87.62880 41.80189, -87.62879 41.801...
        3         38  ...  POLYGON ((-87.60671 41.81681, -87.60670 41.816...
        4         39  ...  POLYGON ((-87.59215 41.81693, -87.59215 41.816...
        [5 rows x 87 columns]

        >>> groceries.head()  # doctest: +SKIP
           OBJECTID     Ycoord  ...  Category                           geometry
        0        16  41.973266  ...       NaN  MULTIPOINT ((-87.65661 41.97321))
        1        18  41.696367  ...       NaN  MULTIPOINT ((-87.68136 41.69713))
        2        22  41.868634  ...       NaN  MULTIPOINT ((-87.63918 41.86847))
        3        23  41.877590  ...       new  MULTIPOINT ((-87.65495 41.87783))
        4        27  41.737696  ...       NaN  MULTIPOINT ((-87.62715 41.73623))
        [5 rows x 8 columns]

        >>> groceries_w_communities = groceries.sjoin_nearest(chicago)
        >>> groceries_w_communities[["Chain", "community", "geometry"]].head(2)
                       Chain    community                                geometry
        0     VIET HOA PLAZA       UPTOWN   MULTIPOINT ((1168268.672 1933554.35))
        1  COUNTY FAIR FOODS  MORGAN PARK  MULTIPOINT ((1162302.618 1832900.224))


        To include the distances:

        >>> groceries_w_communities = groceries.sjoin_nearest(chicago, distance_col="distances")
        >>> groceries_w_communities[["Chain", "community", "distances"]].head(2)
                       Chain    community  distances
        0     VIET HOA PLAZA       UPTOWN        0.0
        1  COUNTY FAIR FOODS  MORGAN PARK        0.0

        In the following example, we get multiple groceries for Uptown because all
        results are equidistant (in this case zero because they intersect).
        In fact, we get 4 results in total:

        >>> chicago_w_groceries = groceries.sjoin_nearest(chicago, distance_col="distances", how="right")
        >>> uptown_results = chicago_w_groceries[chicago_w_groceries["community"] == "UPTOWN"]
        >>> uptown_results[["Chain", "community"]]
                    Chain community
        30  VIET HOA PLAZA    UPTOWN
        30      JEWEL OSCO    UPTOWN
        30          TARGET    UPTOWN
        30       Mariano's    UPTOWN

        See Also
        --------
        GeoDataFrame.sjoin : binary predicate joins
        sjoin_nearest : equivalent top-level function

        Notes
        -----
        Since this join relies on distances, results will be inaccurate
        if your geometries are in a geographic CRS.

        Every operation in GeoPandas is planar, i.e. the potential third
        dimension is not taken into account.
        """

    def clip(self, mask: _ClipMask, keep_geom_type: bool = False, sort: bool = False) -> GeoDataFrame:  # type: ignore[override]
        """Clip points, lines, or polygon geometries to the mask extent.

        Both layers must be in the same Coordinate Reference System (CRS).
        The GeoDataFrame will be clipped to the full extent of the ``mask`` object.

        If there are multiple polygons in mask, data from the GeoDataFrame will be
        clipped to the total boundary of all polygons in mask.

        Parameters
        ----------
        mask : GeoDataFrame, GeoSeries, (Multi)Polygon, list-like
            Polygon vector layer used to clip the GeoDataFrame.
            The mask's geometry is dissolved into one geometric feature
            and intersected with GeoDataFrame.
            If the mask is list-like with four elements ``(minx, miny, maxx, maxy)``,
            ``clip`` will use a faster rectangle clipping
            (:meth:`~GeoSeries.clip_by_rect`), possibly leading to slightly different
            results.
        keep_geom_type : boolean, default False
            If True, return only geometries of original type in case of intersection
            resulting in multiple geometry types or GeometryCollections.
            If False, return all resulting geometries (potentially mixed types).
        sort : boolean, default False
            If True, the order of rows in the clipped GeoDataFrame will be preserved at
            small performance cost. If False the order of rows in the clipped
            GeoDataFrame will be random.

        Returns
        -------
        GeoDataFrame
            Vector data (points, lines, polygons) from the GeoDataFrame clipped to
            polygon boundary from mask.

        See Also
        --------
        clip : equivalent top-level function

        Examples
        --------
        Clip points (grocery stores) with polygons (the Near West Side community):

        >>> import geodatasets
        >>> chicago = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_health")
        ... )
        >>> near_west_side = chicago[chicago["community"] == "NEAR WEST SIDE"]
        >>> groceries = geopandas.read_file(
        ...     geodatasets.get_path("geoda.groceries")
        ... ).to_crs(chicago.crs)
        >>> groceries.shape
        (148, 8)

        >>> nws_groceries = groceries.clip(near_west_side)
        >>> nws_groceries.shape
        (7, 8)
        """

    def overlay(
        self, right: GeoDataFrame, how: str = "intersection", keep_geom_type: bool | None = None, make_valid: bool = True
    ) -> GeoDataFrame:
        """Perform spatial overlay between GeoDataFrames.

        Currently only supports data GeoDataFrames with uniform geometry types,
        i.e. containing only (Multi)Polygons, or only (Multi)Points, or a
        combination of (Multi)LineString and LinearRing shapes.
        Implements several methods that are all effectively subsets of the union.

        See the User Guide page :doc:`../../user_guide/set_operations` for details.

        Parameters
        ----------
        right : GeoDataFrame
        how : string
            Method of spatial overlay: 'intersection', 'union',
            'identity', 'symmetric_difference' or 'difference'.
        keep_geom_type : bool
            If True, return only geometries of the same geometry type the GeoDataFrame
            has, if False, return all resulting geometries. Default is None,
            which will set keep_geom_type to True but warn upon dropping
            geometries.
        make_valid : bool, default True
            If True, any invalid input geometries are corrected with a call to
            make_valid(), if False, a `ValueError` is raised if any input geometries
            are invalid.

        Returns
        -------
        df : GeoDataFrame
            GeoDataFrame with new set of polygons and attributes
            resulting from the overlay

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> polys1 = geopandas.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
        ...                               Polygon([(2,2), (4,2), (4,4), (2,4)])])
        >>> polys2 = geopandas.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
        ...                               Polygon([(3,3), (5,3), (5,5), (3,5)])])
        >>> df1 = geopandas.GeoDataFrame({'geometry': polys1, 'df1_data':[1,2]})
        >>> df2 = geopandas.GeoDataFrame({'geometry': polys2, 'df2_data':[1,2]})

        >>> df1.overlay(df2, how='union')
           df1_data  df2_data                                           geometry
        0       1.0       1.0                POLYGON ((2 2, 2 1, 1 1, 1 2, 2 2))
        1       2.0       1.0                POLYGON ((2 2, 2 3, 3 3, 3 2, 2 2))
        2       2.0       2.0                POLYGON ((4 4, 4 3, 3 3, 3 4, 4 4))
        3       1.0       NaN      POLYGON ((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0))
        4       2.0       NaN  MULTIPOLYGON (((3 4, 3 3, 2 3, 2 4, 3 4)), ((4...
        5       NaN       1.0  MULTIPOLYGON (((2 3, 2 2, 1 2, 1 3, 2 3)), ((3...
        6       NaN       2.0      POLYGON ((3 5, 5 5, 5 3, 4 3, 4 4, 3 4, 3 5))

        >>> df1.overlay(df2, how='intersection')
           df1_data  df2_data                             geometry
        0         1         1  POLYGON ((2 2, 2 1, 1 1, 1 2, 2 2))
        1         2         1  POLYGON ((2 2, 2 3, 3 3, 3 2, 2 2))
        2         2         2  POLYGON ((4 4, 4 3, 3 3, 3 4, 4 4))

        >>> df1.overlay(df2, how='symmetric_difference')
           df1_data  df2_data                                           geometry
        0       1.0       NaN      POLYGON ((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0))
        1       2.0       NaN  MULTIPOLYGON (((3 4, 3 3, 2 3, 2 4, 3 4)), ((4...
        2       NaN       1.0  MULTIPOLYGON (((2 3, 2 2, 1 2, 1 3, 2 3)), ((3...
        3       NaN       2.0      POLYGON ((3 5, 5 5, 5 3, 4 3, 4 4, 3 4, 3 5))

        >>> df1.overlay(df2, how='difference')
                                                    geometry  df1_data
        0      POLYGON ((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0))         1
        1  MULTIPOLYGON (((3 4, 3 3, 2 3, 2 4, 3 4)), ((4...         2

        >>> df1.overlay(df2, how='identity')
           df1_data  df2_data                                           geometry
        0         1       1.0                POLYGON ((2 2, 2 1, 1 1, 1 2, 2 2))
        1         2       1.0                POLYGON ((2 2, 2 3, 3 3, 3 2, 2 2))
        2         2       2.0                POLYGON ((4 4, 4 3, 3 3, 3 4, 4 4))
        3         1       NaN      POLYGON ((2 0, 0 0, 0 2, 1 2, 1 1, 2 1, 2 0))
        4         2       NaN  MULTIPOLYGON (((3 4, 3 3, 2 3, 2 4, 3 4)), ((4...

        See Also
        --------
        GeoDataFrame.sjoin : spatial join
        overlay : equivalent top-level function

        Notes
        -----
        Every operation in GeoPandas is planar, i.e. the potential third
        dimension is not taken into account.
        """
