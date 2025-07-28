import sqlite3
from _typeshed import Incomplete, SupportsLenAndGetItem
from collections.abc import Container, Iterator, Mapping
from contextlib import AbstractContextManager
from typing import Any, Protocol, overload
from typing_extensions import TypeAlias

from pandas._typing import Scalar

from ..base import _ConvertibleToCRS
from ..geodataframe import GeoDataFrame

# Start SQLAlchemy hack
# ---------------------
# The code actually explicitly checks for SQLAlchemy's `Connection` and `Engine` with
# isinstance checks. However to avoid a dependency on SQLAlchemy, we use "good-enough"
# protocols that match as much as possible the SQLAlchemy implementation. This makes it
# very hard for someone to pass in the wrong object.
class _SqlalchemyTransactionLike(Protocol):
    # is_active: bool
    # connection: _SqlalchemyConnectionLike
    # def __init__(self, connection: _SqlalchemyConnectionLike): ...
    # @property
    # def is_valid(self) -> bool: ...
    def close(self) -> None: ...
    def rollback(self) -> None: ...
    def commit(self) -> None: ...

# `Any` is used in places where it would require to copy a lot of types from sqlalchemy
class _SqlAlchemyEventTarget(Protocol):
    dispatch: Any

class _SqlalchemyConnectionLike(_SqlAlchemyEventTarget, Protocol):
    engine: Any
    @property
    def closed(self) -> bool: ...
    @property
    def invalidated(self) -> bool: ...
    def __enter__(self) -> _SqlalchemyConnectionLike: ...  # noqa: Y034
    def __exit__(self, type_, value, traceback, /) -> None: ...
    @property
    def info(self) -> dict[Any, Any]: ...
    def invalidate(self, exception: BaseException | None = None) -> None: ...
    def detach(self) -> None: ...
    def begin(self) -> _SqlalchemyTransactionLike: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def recover_twophase(self) -> list[Any]: ...
    def rollback_prepared(self, xid: Any, recover: bool = ...) -> None: ...
    def commit_prepared(self, xid: Any, recover: bool = ...) -> None: ...
    def in_transaction(self) -> bool: ...
    def in_nested_transaction(self) -> bool: ...
    def close(self) -> None: ...

class _SqlalchemyEngineLike(_SqlAlchemyEventTarget, Protocol):
    dialect: Any
    pool: Any
    url: Any
    hide_parameters: bool
    @property
    def engine(self) -> _SqlalchemyEngineLike: ...
    def clear_compiled_cache(self) -> None: ...
    def update_execution_options(self, **opt: Any) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def driver(self) -> str: ...
    def dispose(self, close: bool = True) -> None: ...
    def begin(self) -> AbstractContextManager[Any]: ...
    def connect(self) -> Any: ...

_SqlalchemyConnectableLike: TypeAlias = _SqlalchemyConnectionLike | _SqlalchemyEngineLike
# ---------------------
# End SQLAlchemy hack

_SQLConnection: TypeAlias = str | _SqlalchemyConnectableLike | sqlite3.Connection  # coppied from pandas.io.sql

@overload
def _read_postgis(
    sql: str,
    con: _SQLConnection,
    geom_col: str = "geom",
    crs: _ConvertibleToCRS | None = None,
    index_col: str | Container[str] | None = None,
    coerce_float: bool = True,
    parse_dates: Container[str | Mapping[str, Incomplete]] | Mapping[str, str | Mapping[str, Incomplete]] | None = None,
    params: SupportsLenAndGetItem[Scalar] | Mapping[str, Scalar] | None = None,
    *,
    chunksize: int,
) -> Iterator[GeoDataFrame]:
    """Return a GeoDataFrame corresponding to the result of the query
    string, which must contain a geometry column in WKB representation.

    It is also possible to use :meth:`~GeoDataFrame.read_file` to read from a database.
    Especially for file geodatabases like GeoPackage or SpatiaLite this can be easier.

    Parameters
    ----------
    sql : string
        SQL query to execute in selecting entries from database, or name
        of the table to read from the database.
    con : sqlalchemy.engine.Connection or sqlalchemy.engine.Engine
        Active connection to the database to query.
    geom_col : string, default 'geom'
        column name to convert to shapely geometries
    crs : dict or str, optional
        CRS to use for the returned GeoDataFrame; if not set, tries to
        determine CRS from the SRID associated with the first geometry in
        the database, and assigns that to all geometries.
    chunksize : int, default None
        If specified, return an iterator where chunksize is the number of rows to
        include in each chunk.

    See the documentation for pandas.read_sql for further explanation
    of the following parameters:
    index_col, coerce_float, parse_dates, params, chunksize

    Returns
    -------
    GeoDataFrame

    Examples
    --------
    PostGIS

    >>> from sqlalchemy import create_engine  # doctest: +SKIP
    >>> db_connection_url = "postgresql://myusername:mypassword@myhost:5432/mydatabase"
    >>> con = create_engine(db_connection_url)  # doctest: +SKIP
    >>> sql = "SELECT geom, highway FROM roads"
    >>> df = geopandas.read_postgis(sql, con)  # doctest: +SKIP

    SpatiaLite

    >>> sql = "SELECT ST_AsBinary(geom) AS geom, highway FROM roads"
    >>> df = geopandas.read_postgis(sql, con)  # doctest: +SKIP
    """

@overload
def _read_postgis(
    sql: str,
    con: _SQLConnection,
    geom_col: str = "geom",
    crs: _ConvertibleToCRS | None = None,
    index_col: str | Container[str] | None = None,
    coerce_float: bool = True,
    parse_dates: Container[str | Mapping[str, Incomplete]] | Mapping[str, str | Mapping[str, Incomplete]] | None = None,
    params: SupportsLenAndGetItem[Scalar] | Mapping[str, Scalar] | None = None,
    chunksize: None = None,
) -> GeoDataFrame: ...
@overload
def _read_postgis(
    sql: str,
    con: _SQLConnection,
    geom_col: str = "geom",
    crs: _ConvertibleToCRS | None = None,
    index_col: str | Container[str] | None = None,
    coerce_float: bool = True,
    parse_dates: Container[str | Mapping[str, Incomplete]] | Mapping[str, str | Mapping[str, Incomplete]] | None = None,
    params: SupportsLenAndGetItem[Scalar] | Mapping[str, Scalar] | None = None,
    chunksize: int | None = None,
) -> GeoDataFrame | Iterator[GeoDataFrame]: ...
