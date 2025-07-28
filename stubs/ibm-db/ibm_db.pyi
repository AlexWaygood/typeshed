"""IBM DataServer Driver for Python."""

from typing import Any, final, overload
from typing_extensions import Self

ATTR_CASE: int
CASE_LOWER: int
CASE_NATURAL: int
CASE_UPPER: int
PARAM_FILE: int
QUOTED_LITERAL_REPLACEMENT_OFF: int
QUOTED_LITERAL_REPLACEMENT_ON: int
SQL_API_SQLROWCOUNT: int
SQL_ATTR_AUTOCOMMIT: int
SQL_ATTR_CALL_RETURN: int
SQL_ATTR_CURRENT_SCHEMA: int
SQL_ATTR_CURSOR_TYPE: int
SQL_ATTR_INFO_ACCTSTR: int
SQL_ATTR_INFO_APPLNAME: int
SQL_ATTR_INFO_PROGRAMNAME: int
SQL_ATTR_INFO_USERID: int
SQL_ATTR_INFO_WRKSTNNAME: int
SQL_ATTR_PARAMSET_SIZE: int
SQL_ATTR_PARAM_BIND_TYPE: int
SQL_ATTR_QUERY_TIMEOUT: int
SQL_ATTR_ROWCOUNT_PREFETCH: int
SQL_ATTR_TRUSTED_CONTEXT_PASSWORD: int
SQL_ATTR_TRUSTED_CONTEXT_USERID: int
SQL_ATTR_TXN_ISOLATION: int
SQL_ATTR_USE_TRUSTED_CONTEXT: int
SQL_ATTR_XML_DECLARATION: int
SQL_AUTOCOMMIT_OFF: int
SQL_AUTOCOMMIT_ON: int
SQL_BIGINT: int
SQL_BINARY: int
SQL_BIT: int
SQL_BLOB: int
SQL_BLOB_LOCATOR: int
SQL_BOOLEAN: int
SQL_CHAR: int
SQL_CLOB: int
SQL_CLOB_LOCATOR: int
SQL_CURSOR_DYNAMIC: int
SQL_CURSOR_FORWARD_ONLY: int
SQL_CURSOR_KEYSET_DRIVEN: int
SQL_CURSOR_STATIC: int
SQL_DBCLOB: int
SQL_DBCLOB_LOCATOR: int
SQL_DBMS_NAME: int
SQL_DBMS_VER: int
SQL_DECFLOAT: int
SQL_DECIMAL: int
SQL_DOUBLE: int
SQL_FALSE: int
SQL_FLOAT: int
SQL_GRAPHIC: int
SQL_INDEX_CLUSTERED: int
SQL_INDEX_OTHER: int
SQL_INTEGER: int
SQL_LONGVARBINARY: int
SQL_LONGVARCHAR: int
SQL_LONGVARGRAPHIC: int
SQL_NUMERIC: int
SQL_PARAM_BIND_BY_COLUMN: int
SQL_PARAM_INPUT: int
SQL_PARAM_INPUT_OUTPUT: int
SQL_PARAM_OUTPUT: int
SQL_REAL: int
SQL_ROWCOUNT_PREFETCH_OFF: int
SQL_ROWCOUNT_PREFETCH_ON: int
SQL_SMALLINT: int
SQL_TABLE_STAT: int
SQL_TINYINT: int
SQL_TRUE: int
SQL_TXN_NO_COMMIT: int
SQL_TXN_READ_COMMITTED: int
SQL_TXN_READ_UNCOMMITTED: int
SQL_TXN_REPEATABLE_READ: int
SQL_TXN_SERIALIZABLE: int
SQL_TYPE_DATE: int
SQL_TYPE_TIME: int
SQL_TYPE_TIMESTAMP: int
SQL_VARBINARY: int
SQL_VARCHAR: int
SQL_VARGRAPHIC: int
SQL_WCHAR: int
SQL_WLONGVARCHAR: int
SQL_WVARCHAR: int
SQL_XML: int
USE_WCHAR: int
WCHAR_NO: int
WCHAR_YES: int

SQL_ATTR_ACCESS_MODE: int
SQL_ATTR_ALLOW_INTERLEAVED_GETDATA: int
SQL_ATTR_ANSI_APP: int
SQL_ATTR_APPEND_FOR_FETCH_ONLY: int
SQL_ATTR_APP_USES_LOB_LOCATOR: int
SQL_ATTR_ASYNC_ENABLE: int
SQL_ATTR_AUTO_IPD: int
SQL_ATTR_CACHE_USRLIBL: int
SQL_ATTR_CLIENT_APPLCOMPAT: int
SQL_ATTR_CLIENT_CODEPAGE: int
SQL_ATTR_COLUMNWISE_MRI: int
SQL_ATTR_COMMITONEOF: int
SQL_ATTR_CONCURRENT_ACCESS_RESOLUTION: int
SQL_ATTR_CONFIG_KEYWORDS_ARRAY_SIZE: int
SQL_ATTR_CONFIG_KEYWORDS_MAXLEN: int
SQL_ATTR_CONNECTION_DEAD: int
SQL_ATTR_CONNECTTYPE: int
SQL_ATTR_CONNECT_NODE: int
SQL_ATTR_CONNECT_PASSIVE: int
SQL_ATTR_CONN_CONTEXT: int
SQL_ATTR_CURRENT_CATALOG: int
SQL_ATTR_CURRENT_IMPLICIT_XMLPARSE_OPTION: int
SQL_ATTR_CURRENT_PACKAGE_PATH: int
SQL_ATTR_CURRENT_PACKAGE_SET: int
SQL_ATTR_DATE_FMT: int
SQL_ATTR_DATE_SEP: int
SQL_ATTR_DB2EXPLAIN: int
SQL_ATTR_DB2_APPLICATION_HANDLE: int
SQL_ATTR_DB2_APPLICATION_ID: int
SQL_ATTR_DB2_SQLERRP: int
SQL_ATTR_DECFLOAT_ROUNDING_MODE: int
SQL_ATTR_DECIMAL_SEP: int
SQL_ATTR_DESCRIBE_CALL: int
SQL_ATTR_DESCRIBE_OUTPUT_LEVEL: int
SQL_ATTR_DETECT_READ_ONLY_TXN: int
SQL_ATTR_ENLIST_IN_DTC: int
SQL_ATTR_EXTENDED_INDICATORS: int
SQL_ATTR_FET_BUF_SIZE: int
SQL_ATTR_FORCE_ROLLBACK: int
SQL_ATTR_FREE_LOCATORS_ON_FETCH: int
SQL_ATTR_GET_LATEST_MEMBER: int
SQL_ATTR_GET_LATEST_MEMBER_NAME: int
SQL_ATTR_IGNORE_SERVER_LIST: int
SQL_ATTR_INFO_CRRTKN: int
SQL_ATTR_INFO_PROGRAMID: int
SQL_ATTR_KEEP_DYNAMIC: int
SQL_ATTR_LOB_CACHE_SIZE: int
SQL_ATTR_LOB_FILE_THRESHOLD: int
SQL_ATTR_LOGIN_TIMEOUT: int
SQL_ATTR_LONGDATA_COMPAT: int
SQL_ATTR_MAPCHAR: int
SQL_ATTR_MAXBLKEXT: int
SQL_ATTR_MAX_LOB_BLOCK_SIZE: int
SQL_ATTR_NETWORK_STATISTICS: int
SQL_ATTR_OVERRIDE_CHARACTER_CODEPAGE: int
SQL_ATTR_OVERRIDE_CODEPAGE: int
SQL_ATTR_OVERRIDE_PRIMARY_AFFINITY: int
SQL_ATTR_PARC_BATCH: int
SQL_ATTR_PING_DB: int
SQL_ATTR_PING_NTIMES: int
SQL_ATTR_PING_REQUEST_PACKET_SIZE: int
SQL_ATTR_QUERY_PREFETCH: int
SQL_ATTR_QUIET_MODE: int
SQL_ATTR_READ_ONLY_CONNECTION: int
SQL_ATTR_RECEIVE_TIMEOUT: int
SQL_ATTR_REOPT: int
SQL_ATTR_REPORT_ISLONG_FOR_LONGTYPES_OLEDB: int
SQL_ATTR_REPORT_SEAMLESSFAILOVER_WARNING: int
SQL_ATTR_REPORT_TIMESTAMP_TRUNC_AS_WARN: int
SQL_ATTR_RETRYONERROR: int
SQL_ATTR_RETRY_ON_MERGE: int
SQL_ATTR_SERVER_MSGTXT_MASK: int
SQL_ATTR_SERVER_MSGTXT_SP: int
SQL_ATTR_SESSION_GLOBAL_VAR: int
SQL_ATTR_SESSION_TIME_ZONE: int
SQL_ATTR_SPECIAL_REGISTER: int
SQL_ATTR_SQLCOLUMNS_SORT_BY_ORDINAL_OLEDB: int
SQL_ATTR_STMT_CONCENTRATOR: int
SQL_ATTR_STREAM_GETDATA: int
SQL_ATTR_STREAM_OUTPUTLOB_ON_CALL: int
SQL_ATTR_TIME_FMT: int
SQL_ATTR_TIME_SEP: int
SQL_ATTR_TRUSTED_CONTEXT_ACCESSTOKEN: int
SQL_ATTR_USER_REGISTRY_NAME: int
SQL_ATTR_WCHARTYPE: int

@final
class IBM_DBClientInfo:
    """IBM DataServer Client Information object"""

    def __new__(cls, *args: object, **kwargs: object) -> Self: ...
    APPL_CODEPAGE: int
    CONN_CODEPAGE: int
    DATA_SOURCE_NAME: str
    DRIVER_NAME: str
    DRIVER_ODBC_VER: str
    DRIVER_VER: str
    ODBC_SQL_CONFORMANCE: str
    ODBC_VER: str

@final
class IBM_DBConnection:
    """IBM DataServer connection object"""

    def __new__(cls, *args: object, **kwargs: object) -> Self: ...

@final
class IBM_DBServerInfo:
    """IBM DataServer Information object"""

    def __new__(cls, *args: object, **kwargs: object) -> Self: ...
    DBMS_NAME: str
    DBMS_VER: str
    DB_CODEPAGE: int
    DB_NAME: str
    DFT_ISOLATION: str
    IDENTIFIER_QUOTE_CHAR: str
    INST_NAME: str
    ISOLATION_OPTION: tuple[str, str, str, str, str]
    KEYWORDS: str
    LIKE_ESCAPE_CLAUSE: bool
    MAX_COL_NAME_LEN: int
    MAX_IDENTIFIER_LEN: int
    MAX_INDEX_SIZE: int
    MAX_PROC_NAME_LEN: int
    MAX_ROW_SIZE: int
    MAX_SCHEMA_NAME_LEN: int
    MAX_STATEMENT_LEN: int
    MAX_TABLE_NAME_LEN: int
    NON_NULLABLE_COLUMNS: bool
    PROCEDURES: bool
    SPECIAL_CHARS: str
    SQL_CONFORMANCE: str

@final
class IBM_DBStatement:
    """IBM DataServer cursor object"""

    def __new__(cls, *args: object, **kwargs: object) -> Self: ...

def active(connection: IBM_DBConnection | None, /) -> bool:
    """Checks if the specified connection resource is active"""

def autocommit(connection: IBM_DBConnection, value: int = ..., /) -> int | bool:
    """Returns or sets the AUTOCOMMIT state for a database connection"""

def bind_param(
    stmt: IBM_DBStatement,
    parameter_number: int,
    variable: str,
    parameter_type: int | None = ...,
    data_type: int | None = ...,
    precision: int | None = ...,
    scale: int | None = ...,
    size: int | None = ...,
    /,
) -> bool:
    """Binds a Python variable to an SQL statement parameter"""

@overload
def callproc(connection: IBM_DBConnection, procname: str, /) -> IBM_DBStatement | None:
    """Returns a tuple containing OUT/INOUT variable value"""

@overload
def callproc(connection: IBM_DBConnection, procname: str, parameters: tuple[object, ...], /) -> tuple[object, ...] | None: ...
def check_function_support(connection: IBM_DBConnection, function_id: int, /) -> bool:
    """return true if fuction is supported otherwise return false"""

def client_info(connection: IBM_DBConnection, /) -> IBM_DBClientInfo | bool:
    """Returns a read-only object with information about the DB2 database client"""

def close(connection: IBM_DBConnection, /) -> bool:
    """Close a database connection"""

def column_privileges(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    column_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the columns and associated privileges for a table."""

def columns(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    column_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the columns and associated metadata for a table"""

def commit(connection: IBM_DBConnection, /) -> bool:
    """Commits a transaction"""

def conn_error(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns a string containing the SQLSTATE returned by the last connection attempt"""

def conn_errormsg(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns an error message and SQLCODE value representing the reason the last database connection attempt failed"""

def conn_warn(connection: IBM_DBConnection | None = ..., /) -> str:
    """Returns a warning string containing the SQLSTATE returned by the last connection attempt"""

def connect(
    database: str, user: str, password: str, options: dict[int, int | str] | None = ..., replace_quoted_literal: int = ..., /
) -> IBM_DBConnection | None:
    """Connect to the database"""

def createdb(connection: IBM_DBConnection, dbName: str, codeSet: str = ..., mode: str = ..., /) -> bool:
    """Create db"""

def createdbNX(connection: IBM_DBConnection, dbName: str, codeSet: str = ..., mode: str = ..., /) -> bool:
    """createdbNX"""

def cursor_type(stmt: IBM_DBStatement, /) -> int:
    """Returns the cursor type used by a statement resource"""

def debug(option: str | bool) -> None:
    """Enable logging with optional log file or disable logging"""

def dropdb(connection: IBM_DBConnection, dbName: str, /) -> bool:
    """Drop db"""

def exec_immediate(
    connection: IBM_DBConnection, statement: str | None, options: dict[int, int] = ..., /
) -> IBM_DBStatement | bool:
    """Prepares and executes an SQL statement."""

def execute(stmt: IBM_DBStatement, parameters: tuple[object, ...] | None = ..., /) -> bool:
    """Executes an SQL statement that was prepared by ibm_db.prepare()"""

def execute_many(stmt: IBM_DBStatement, seq_of_parameters: tuple[object, ...], options: dict[int, int] = ..., /) -> int | None:
    """Execute SQL with multiple rows."""

def fetchall(stmt: IBM_DBStatement, /) -> list[tuple[object, ...]]:
    """Fetch all rows from the result set."""

def fetchmany(stmt: IBM_DBStatement, numberOfRows: int, /) -> list[tuple[object, ...]]:
    """Fetch a specified number of rows from the result set."""

def fetchone(stmt: IBM_DBStatement, /) -> tuple[object, ...]:
    """Fetch a single row from the result set."""

def fetch_assoc(stmt: IBM_DBStatement, row_number: int = ..., /) -> dict[str, object] | bool:
    """Returns a dictionary, indexed by column name, representing a row in a result set"""

def fetch_both(stmt: IBM_DBStatement, row_number: int = ..., /) -> dict[int | str, object] | bool:
    """Returns a dictionary, indexed by both column name and position, representing a row in a result set"""

def fetch_row(stmt: IBM_DBStatement, row_number: int = ..., /) -> bool:
    """Sets the result set pointer to the next row or requested row"""

def fetch_tuple(stmt: IBM_DBStatement, row_number: int = ..., /) -> tuple[object, ...]:
    """Returns an tuple, indexed by column position, representing a row in a result set"""

def field_display_size(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the maximum number of bytes required to display a column"""

def field_name(stmt: IBM_DBStatement, column: int | str, /) -> str | bool:
    """Returns the name of the column in the result set"""

def field_nullable(stmt: IBM_DBStatement, column: int | str, /) -> bool:
    """Returns indicated column can contain nulls or not"""

def field_num(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the position of the named column in a result set"""

def field_precision(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the precision of the indicated column in a result set"""

def field_scale(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the scale of the indicated column in a result set"""

def field_type(stmt: IBM_DBStatement, column: int | str, /) -> str | bool:
    """Returns the data type of the indicated column in a result set"""

def field_width(stmt: IBM_DBStatement, column: int | str, /) -> int | bool:
    """Returns the width of the indicated column in a result set"""

def foreign_keys(
    connection: IBM_DBConnection,
    pk_qualifier: str | None,
    pk_schema: str | None,
    pk_table_name: str | None,
    fk_qualifier: str | None = ...,
    fk_schema: str | None = ...,
    fk_table_name: str | None = ...,
    /,
) -> IBM_DBStatement:
    """Returns a result set listing the foreign keys for a table"""

def free_result(stmt: IBM_DBStatement, /) -> bool:
    """Frees resources associated with a result set"""

def free_stmt(stmt: IBM_DBStatement, /) -> bool:
    """Frees resources associated with the indicated statement resource"""

def get_db_info(connection: IBM_DBConnection, option: int, /) -> str | bool:
    """Returns an object with properties that describe the DB2 database server according to the option passed"""

def get_last_serial_value(stmt: IBM_DBStatement, /) -> str | bool:
    """Returns last serial value inserted for identity column"""

def get_num_result(stmt: IBM_DBStatement, /) -> int | bool:
    """Returns the number of rows in a current open non-dynamic scrollable cursor"""

def get_option(resc: IBM_DBConnection | IBM_DBStatement, options: int, type: int, /) -> Any:
    """Gets the specified option in the resource."""

def get_sqlcode(connection_or_stmt: IBM_DBConnection | IBM_DBStatement | None = None, /) -> str:
    """Returns a string containing the SQLCODE returned by the last connection attempt/ SQL statement"""

def next_result(stmt: IBM_DBStatement, /) -> IBM_DBStatement | bool:
    """Requests the next result set from a stored procedure"""

def num_fields(stmt: IBM_DBStatement, /) -> int | bool:
    """Returns the number of fields contained in a result set"""

def num_rows(stmt: IBM_DBStatement, /) -> int:
    """Returns the number of rows affected by an SQL statement"""

def pconnect(
    database: str, username: str, password: str, options: dict[int, int | str] | None = ..., /
) -> IBM_DBConnection | None:
    """Returns a persistent connection to a database"""

def prepare(
    connection: IBM_DBConnection, statement: str, options: dict[int, int | str] | None = ..., /
) -> IBM_DBStatement | bool:
    """Prepares an SQL statement."""

def primary_keys(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, /
) -> IBM_DBStatement:
    """Returns a result set listing primary keys for a table"""

def procedure_columns(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, procedure: str | None, parameter: str | None, /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the parameters for one or more stored procedures."""

def procedures(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, procedure: str | None, /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the stored procedures registered in a database"""

def recreatedb(connection: IBM_DBConnection, dbName: str, codeSet: str | None = ..., mode: str | None = ..., /) -> bool:
    """recreate db"""

def result(stmt: IBM_DBStatement, column: int | str, /) -> Any:
    """Returns a single column from a row in the result set"""

def rollback(connection: IBM_DBConnection, /) -> bool:
    """Rolls back a transaction"""

def server_info(connection: IBM_DBConnection, /) -> IBM_DBServerInfo | bool:
    """Returns an object with properties that describe the DB2 database server"""

def set_option(resc: IBM_DBConnection | IBM_DBStatement, options: dict[int, int | str], type: int, /) -> bool:
    """Sets the specified option in the resource"""

def special_columns(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, scope: int, /
) -> IBM_DBStatement:
    """Returns a result set listing the unique row identifier columns for a table"""

def statistics(
    connection: IBM_DBConnection, qualifier: str | None, schema: str | None, table_name: str | None, unique: bool | None, /
) -> IBM_DBStatement:
    """Returns a result set listing the index and statistics for a table"""

def stmt_error(stmt: IBM_DBStatement = ..., /) -> str:
    """Returns a string containing the SQLSTATE returned by an SQL statement"""

def stmt_errormsg(stmt: IBM_DBStatement = ..., /) -> str:
    """Returns a string containing the last SQL statement error message"""

def stmt_warn(connection: IBM_DBConnection = ..., /) -> IBM_DBStatement:
    """Returns a warning string containing the SQLSTATE returned by last SQL statement"""

def table_privileges(
    connection: IBM_DBConnection, qualifier: str | None = ..., schema: str | None = ..., table_name: str | None = ..., /
) -> IBM_DBStatement | bool:
    """Returns a result set listing the tables and associated privileges in a database"""

def tables(
    connection: IBM_DBConnection,
    qualifier: str | None = ...,
    schema: str | None = ...,
    table_name: str | None = ...,
    table_type: str | None = ...,
    /,
) -> IBM_DBStatement | bool:
    """Returns a result set listing the tables and associated metadata in a database"""
