import decimal
from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Callable, Sequence
from datetime import date, datetime, time
from types import TracebackType
from typing import Any, Final, Literal, overload
from typing_extensions import Self, TypeAlias

from .resultrow import ResultRow

apilevel: Final[str]
threadsafety: Final[int]
paramstyle: Final[tuple[str, ...]]  # hdbcli defines it as a tuple which does not follow PEP 249

class Connection:
    def __init__(
        self,
        address: str = "",
        port: int = 0,
        user: str = "",
        password: str = "",
        autocommit: bool = True,
        packetsize: int | None = None,
        userkey: str | None = ...,
        *,
        sessionvariables: dict[str, str] | None = ...,
        forcebulkfetch: bool | None = ...,
    ) -> None: ...
    def cancel(self) -> bool:
        """Cancels the running database request that is executed on the connection."""

    def close(self) -> None:
        """Close the connection."""

    def commit(self) -> None:
        """Commit any pending transaction to the database."""

    def cursor(self) -> Cursor:
        """Create a new cursor"""

    def getaddress(self) -> str:
        """getaddress"""

    def getautocommit(self) -> bool:
        """Gets this connection's auto-commit mode."""

    def getclientinfo(self, key: str = ...) -> str | dict[str, str]:
        """Gets this connection's client information."""

    def getproperty(self, *args, **kwargs):
        """Gets this connection's property."""

    def isconnected(self) -> bool:
        """Checks the state of the connection with which the cursor is bound"""

    def rollback(self) -> None:
        """Roll back to the start of any pending transaction."""

    def setautocommit(self, auto: bool = ...) -> None:
        """Sets this connection's auto-commit mode."""

    def setclientinfo(self, key: str, value: str | None = ...) -> None:
        """Sets this connection's client information."""

    def ontrace(self, callback: Callable[[str], Any], options: str = ...) -> None:
        """Sets the trace callback"""

connect = Connection

class LOB:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def close(self) -> bool:
        """Close LOB object"""

    def find(self, object: str, length: int, position: int = ...) -> int:
        """Return the offset of the given pattern in the LOB object"""

    def read(self, size: int = ..., position: int = ...) -> str | bytes:
        """Return a portion (or all) of the data in the LOB object"""

    def write(self, object: str | bytes) -> int:
        """Write the data to the LOB object"""

_Parameters: TypeAlias = Sequence[tuple[Any, ...]] | None
_Holdability: TypeAlias = Literal[0, 1, 2, 3]

class Cursor:
    description: tuple[tuple[Any, ...], ...]
    rowcount: int
    statementhash: str | None
    connection: Connection
    arraysize: int
    refreshts: int | None
    maxage: int
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, typ: type[BaseException] | None, val: BaseException | None, tb: TracebackType | None) -> None: ...
    def callproc(self, procname: str, parameters: tuple[Any, ...] = ..., overview: bool = ...) -> tuple[Any, ...]:
        """Call a stored database procedure with the given name"""

    def close(self) -> None:
        """Close the cursor now"""

    def description_ext(self) -> Sequence[tuple[Any, ...]]:
        """Retrieve a sequence of descriptions of result columns"""

    def execute(self, operation: str, parameters: tuple[Any, ...] | None = ...) -> bool:
        """Prepare and execute a database operation."""

    def executemany(self, operation: str, parameters: _Parameters = ..., batcherrors: bool = False) -> Any:
        """Execute in batch"""

    def executemanyprepared(self, parameters: _Parameters = ...) -> Any:
        """Execute a prepared database operation in batch."""

    def executeprepared(self, parameters: _Parameters = ...) -> Any:
        """Execute a prepared database operation."""

    def fetchone(self, uselob: bool = ...) -> ResultRow | None:
        """Fetch the next row of a query result set"""

    def fetchall(self) -> list[ResultRow]:
        """Fetch all rows of a query result set"""

    def fetchmany(self, size: int | None = ...) -> list[ResultRow]:
        """Fetch the specified number of rows of a query result set"""

    def getrowsaffectedcounts(self) -> tuple[Any, ...]:
        """Retrieves a tuple of rows affected counts, one entry for each input row provided to the previous executemany() invocation"""

    def getpacketsize(self) -> int:
        """Gets the packet size used currently for the cursor"""

    def get_resultset_holdability(self) -> _Holdability:
        """Retrieves the result set holdability"""

    def getwarning(self) -> Warning | None:
        """Retrieve warning object if there is a warning from the previous execution"""

    def haswarning(self) -> bool:
        """Checks whether there is any warning from the previous execution"""

    def clearwarning(self) -> None:
        """make warning flag false"""

    def has_result_set(self) -> bool:
        """Check if SQL statement is query that has result set"""

    def nextset(self) -> None:
        """Make the cursot skip to the next result set, closing current result set"""

    def parameter_description(self) -> tuple[str, ...]:
        """Retrieve a sequence of descriptions of parameters"""

    @overload
    def prepare(self, operation: str, newcursor: Literal[True]) -> Cursor:
        """Prepare a database operation."""

    @overload
    def prepare(self, operation: str, newcursor: Literal[False]) -> Any: ...
    def print_message(self):
        """Retreves list of print messages from last statement"""

    def parsenamedquery(self, *args, **kwargs):
        """Internal Use Only"""

    def scroll(self, value: int, mode: Literal["absolute", "relative"] = ...) -> None:
        """Scroll the cursor"""

    def server_cpu_time(self) -> int:
        """Retrieves the server cpu time in microseconds"""

    def server_memory_usage(self) -> int:
        """Retrieves the server memory usage in bytes"""

    def server_processing_time(self) -> int:
        """Retrieves the server processing time in microseconds"""

    def setinputsizes(self, *args: Any, **kwargs: Any) -> None: ...
    def setfetchsize(self, value: int) -> None:
        """Set size of prefetched resultsets"""

    def setquerytimeout(self, value: int) -> None:
        """Set the query timeout"""

    def setpacketsize(self, value: int) -> None:
        """Sets the packet size used for the cursor"""

    def set_resultset_holdability(self, holdability: _Holdability) -> None:
        """Set the result set holdability"""

    def setoutputsize(self, *args: Any, **kwargs: Any) -> None: ...
    def setcommandinfo(self, command_info: str, line_number: int) -> None:
        """Set the command info and line number for the next execute"""

class Warning(Exception):
    errorcode: int
    errortext: str

class Error(Exception):
    errorcode: int
    errortext: str

class DatabaseError(Error): ...
class OperationalError(DatabaseError): ...
class ProgrammingError(DatabaseError): ...
class IntegrityError(DatabaseError): ...
class InterfaceError(Error): ...
class InternalError(DatabaseError): ...
class DataError(DatabaseError): ...
class NotSupportedError(DatabaseError): ...

class ExecuteManyError(Error):
    errors: Incomplete

class ExecuteManyErrorEntry(Error):
    rownumber: int

def Date(year: int, month: int, day: int) -> date: ...
def Time(hour: int, minute: int, second: int, millisecond: int = 0) -> time: ...
def Timestamp(year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int = 0) -> datetime: ...
def DateFromTicks(ticks: float) -> date: ...
def TimeFromTicks(ticks: float) -> time: ...
def TimestampFromTicks(ticks: float) -> datetime: ...
def Binary(data: ReadableBuffer) -> memoryview: ...

Decimal = decimal.Decimal

NUMBER: type[int | float | complex]
DATETIME: type[date | time | datetime]
STRING = str
BINARY = memoryview
ROWID = int
