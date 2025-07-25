import os
from _typeshed import Incomplete, SupportsGetItem, SupportsKeysAndGetItem
from collections.abc import Iterable, Mapping
from typing import Any, Final

from ..geodataframe import GeoDataFrame

METADATA_VERSION: Final[str]
SUPPORTED_VERSIONS_LITERAL = Incomplete
SUPPORTED_VERSIONS: Final[list[str]]
GEOARROW_ENCODINGS: Final[list[str]]
SUPPORTED_ENCODINGS: Final[list[str]]
PARQUET_GEOMETRY_ENCODINGS = Incomplete

def _read_parquet(
    path: str | os.PathLike[str],
    columns: Iterable[str] | None = None,
    storage_options: SupportsKeysAndGetItem[str, Any] | None = None,  # type depend on the connection
    bbox: SupportsGetItem[int, float] | None = None,
    to_pandas_kwargs: Mapping[str, Incomplete] | None = None,
    **kwargs,  # kwargs passed to pyarrow.parquet.read_table
) -> GeoDataFrame:
    """
    Load a Parquet object from the file path, returning a GeoDataFrame.

    You can read a subset of columns in the file using the ``columns`` parameter.
    However, the structure of the returned GeoDataFrame will depend on which
    columns you read:

    * if no geometry columns are read, this will raise a ``ValueError`` - you
      should use the pandas `read_parquet` method instead.
    * if the primary geometry column saved to this file is not included in
      columns, the first available geometry column will be set as the geometry
      column of the returned GeoDataFrame.

    Supports versions 0.1.0, 0.4.0 and 1.0.0 of the GeoParquet
    specification at: https://github.com/opengeospatial/geoparquet

    If 'crs' key is not present in the GeoParquet metadata associated with the
    Parquet object, it will default to "OGC:CRS84" according to the specification.

    Requires 'pyarrow'.

    .. versionadded:: 0.8

    Parameters
    ----------
    path : str, path object
    columns : list-like of strings, default=None
        If not None, only these columns will be read from the file.  If
        the primary geometry column is not included, the first secondary
        geometry read from the file will be set as the geometry column
        of the returned GeoDataFrame.  If no geometry columns are present,
        a ``ValueError`` will be raised.
    storage_options : dict, optional
        Extra options that make sense for a particular storage connection, e.g. host,
        port, username, password, etc. For HTTP(S) URLs the key-value pairs are
        forwarded to urllib as header options. For other URLs (e.g. starting with
        "s3://", and "gcs://") the key-value pairs are forwarded to fsspec. Please
        see fsspec and urllib for more details.

        When no storage options are provided and a filesystem is implemented by
        both ``pyarrow.fs`` and ``fsspec`` (e.g. "s3://") then the ``pyarrow.fs``
        filesystem is preferred. Provide the instantiated fsspec filesystem using
        the ``filesystem`` keyword if you wish to use its implementation.
    bbox : tuple, optional
        Bounding box to be used to filter selection from geoparquet data. This
        is only usable if the data was saved with the bbox covering metadata.
        Input is of the tuple format (xmin, ymin, xmax, ymax).
    to_pandas_kwargs : dict, optional
        Arguments passed to the `pa.Table.to_pandas` method for non-geometry columns.
        This can be used to control the behavior of the conversion of the non-geometry
        columns to a pandas DataFrame. For example, you can use this to control the
        dtype conversion of the columns. By default, the `to_pandas` method is called
        with no additional arguments.

    **kwargs
        Any additional kwargs passed to :func:`pyarrow.parquet.read_table`.

    Returns
    -------
    GeoDataFrame

    Examples
    --------
    >>> df = geopandas.read_parquet("data.parquet")  # doctest: +SKIP

    Specifying columns to read:

    >>> df = geopandas.read_parquet(
    ...     "data.parquet",
    ...     columns=["geometry", "pop_est"]
    ... )  # doctest: +SKIP
    """

def _read_feather(
    path: str | os.PathLike[str],
    columns: Iterable[str] | None = None,
    to_pandas_kwargs: Mapping[str, Incomplete] | None = None,
    **kwargs,  # kwargs passed to pyarrow.feather.read_table
) -> GeoDataFrame:
    """
    Load a Feather object from the file path, returning a GeoDataFrame.

    You can read a subset of columns in the file using the ``columns`` parameter.
    However, the structure of the returned GeoDataFrame will depend on which
    columns you read:

    * if no geometry columns are read, this will raise a ``ValueError`` - you
      should use the pandas `read_feather` method instead.
    * if the primary geometry column saved to this file is not included in
      columns, the first available geometry column will be set as the geometry
      column of the returned GeoDataFrame.

    Supports versions 0.1.0, 0.4.0, 1.0.0 and 1.1.0 of the GeoParquet
    specification at: https://github.com/opengeospatial/geoparquet

    If 'crs' key is not present in the Feather metadata associated with the
    Parquet object, it will default to "OGC:CRS84" according to the specification.

    Requires 'pyarrow' >= 0.17.

    .. versionadded:: 0.8

    Parameters
    ----------
    path : str, path object
    columns : list-like of strings, default=None
        If not None, only these columns will be read from the file.  If
        the primary geometry column is not included, the first secondary
        geometry read from the file will be set as the geometry column
        of the returned GeoDataFrame.  If no geometry columns are present,
        a ``ValueError`` will be raised.
    to_pandas_kwargs : dict, optional
        Arguments passed to the `pa.Table.to_pandas` method for non-geometry columns.
        This can be used to control the behavior of the conversion of the non-geometry
        columns to a pandas DataFrame. For example, you can use this to control the
        dtype conversion of the columns. By default, the `to_pandas` method is called
        with no additional arguments.
    **kwargs
        Any additional kwargs passed to pyarrow.feather.read_table().

    Returns
    -------
    GeoDataFrame

    Examples
    --------
    >>> df = geopandas.read_feather("data.feather")  # doctest: +SKIP

    Specifying columns to read:

    >>> df = geopandas.read_feather(
    ...     "data.feather",
    ...     columns=["geometry", "pop_est"]
    ... )  # doctest: +SKIP
    """
