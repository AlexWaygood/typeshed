import os
from _typeshed import Incomplete, SupportsRead
from collections import OrderedDict
from typing import Literal, TypedDict, overload

import pandas as pd
from pandas._typing import Axes

from ..base import _BboxLike, _MaskLike
from ..geodataframe import GeoDataFrame

# Keep inline with GeoDataFrame.from_file and GeoSeries.from_file
@overload
def _read_file(
    filename: str | os.PathLike[str] | SupportsRead[Incomplete],
    bbox: _BboxLike | None = None,
    mask: _MaskLike | None = None,
    columns: Axes | None = None,
    rows: int | slice | None = None,
    engine: Literal["fiona", "pyogrio"] | None = None,
    *,
    ignore_geometry: Literal[False] = False,
    layer: int | str | None = None,
    encoding: str | None = None,
    **kwargs,  # depend on engine
) -> GeoDataFrame:
    """Return a GeoDataFrame from a file or URL.

    Parameters
    ----------
    filename : str, path object or file-like object
        Either the absolute or relative path to the file or URL to
        be opened, or any object with a read() method (such as an open file
        or StringIO)
    bbox : tuple | GeoDataFrame or GeoSeries | shapely Geometry, default None
        Filter features by given bounding box, GeoSeries, GeoDataFrame or a shapely
        geometry. With engine="fiona", CRS mis-matches are resolved if given a GeoSeries
        or GeoDataFrame. With engine="pyogrio", bbox must be in the same CRS as the
        dataset. Tuple is (minx, miny, maxx, maxy) to match the bounds property of
        shapely geometry objects. Cannot be used with mask.
    mask : dict | GeoDataFrame or GeoSeries | shapely Geometry, default None
        Filter for features that intersect with the given dict-like geojson
        geometry, GeoSeries, GeoDataFrame or shapely geometry.
        CRS mis-matches are resolved if given a GeoSeries or GeoDataFrame.
        Cannot be used with bbox. If multiple geometries are passed, this will
        first union all geometries, which may be computationally expensive.
    columns : list, optional
        List of column names to import from the data source. Column names
        must exactly match the names in the data source. To avoid reading
        any columns (besides the geometry column), pass an empty list-like.
        By default reads all columns.
    rows : int or slice, default None
        Load in specific rows by passing an integer (first `n` rows) or a
        slice() object.
    engine : str,  "pyogrio" or "fiona"
        The underlying library that is used to read the file. Currently, the
        supported options are "pyogrio" and "fiona". Defaults to "pyogrio" if
        installed, otherwise tries "fiona". Engine can also be set globally
        with the ``geopandas.options.io_engine`` option.
    **kwargs :
        Keyword args to be passed to the engine, and can be used to write
        to multi-layer data, store data within archives (zip files), etc.
        In case of the "pyogrio" engine, the keyword arguments are passed to
        `pyogrio.read_dataframe`. In case of the "fiona" engine, the keyword
        arguments are passed to fiona.open`. For more information on possible
        keywords, type: ``import pyogrio; help(pyogrio.read_dataframe)``.


    Examples
    --------
    >>> df = geopandas.read_file("nybb.shp")  # doctest: +SKIP

    Specifying layer of GPKG:

    >>> df = geopandas.read_file("file.gpkg", layer='cities')  # doctest: +SKIP

    Reading only first 10 rows:

    >>> df = geopandas.read_file("nybb.shp", rows=10)  # doctest: +SKIP

    Reading only geometries intersecting ``mask``:

    >>> df = geopandas.read_file("nybb.shp", mask=polygon)  # doctest: +SKIP

    Reading only geometries intersecting ``bbox``:

    >>> df = geopandas.read_file("nybb.shp", bbox=(0, 0, 10, 20))  # doctest: +SKIP

    Returns
    -------
    :obj:`geopandas.GeoDataFrame` or :obj:`pandas.DataFrame` :
        If `ignore_geometry=True` a :obj:`pandas.DataFrame` will be returned.

    Notes
    -----
    The format drivers will attempt to detect the encoding of your data, but
    may fail. In this case, the proper encoding can be specified explicitly
    by using the encoding keyword parameter, e.g. ``encoding='utf-8'``.

    For faster data reading with the default pyogrio engine when
    pyarrow is installed, pass ``use_arrow=True`` as an argument. See the User
    Guide page :doc:`../../user_guide/io` for details.


    When specifying a URL, geopandas will check if the server supports reading
    partial data and in that case pass the URL as is to the underlying engine,
    which will then use the network file system handler of GDAL to read from
    the URL. Otherwise geopandas will download the data from the URL and pass
    all data in-memory to the underlying engine.
    If you need more control over how the URL is read, you can specify the
    GDAL virtual filesystem manually (e.g. ``/vsicurl/https://...``). See the
    GDAL documentation on filesystems for more details
    (https://gdal.org/user/virtual_file_systems.html#vsicurl-http-https-ftp-files-random-access).

    """

@overload
def _read_file(
    filename: str | os.PathLike[str] | SupportsRead[Incomplete],
    bbox: _BboxLike | None = None,
    mask: _MaskLike | None = None,
    columns: Axes | None = None,
    rows: int | slice | None = None,
    engine: Literal["fiona", "pyogrio"] | None = None,
    *,
    ignore_geometry: Literal[True],
    layer: int | str | None = None,
    encoding: str | None = None,
    **kwargs,  # depend on engine
) -> pd.DataFrame: ...

class _Schema(TypedDict):
    geometry: str | list[str]
    properties: OrderedDict[str, str]

def infer_schema(df: GeoDataFrame) -> _Schema: ...
def _list_layers(filename: str | bytes | os.PathLike[str] | os.PathLike[bytes] | SupportsRead[Incomplete]) -> pd.DataFrame:
    """List layers available in a file.

    Provides an overview of layers available in a file or URL together with their
    geometry types. When supported by the data source, this includes both spatial and
    non-spatial layers. Non-spatial layers are indicated by the ``"geometry_type"``
    column being ``None``. GeoPandas will not read such layers but they can be read into
    a pd.DataFrame using :func:`pyogrio.read_dataframe`.

    Parameters
    ----------
    filename : str, path object or file-like object
        Either the absolute or relative path to the file or URL to
        be opened, or any object with a read() method (such as an open file
        or StringIO)

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns "name" and "geometry_type" and one row per layer.
    """
