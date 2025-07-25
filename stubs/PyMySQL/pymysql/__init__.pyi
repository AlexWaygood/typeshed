"""
PyMySQL: A pure-Python MySQL client library.

Copyright (c) 2010-2016 PyMySQL contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from _typeshed import ReadableBuffer
from collections.abc import Iterable
from typing import Final, SupportsBytes, SupportsIndex

from . import connections as connections, constants as constants, converters as converters, cursors as cursors
from .constants import FIELD_TYPE as FIELD_TYPE
from .err import (
    DatabaseError as DatabaseError,
    DataError as DataError,
    Error as Error,
    IntegrityError as IntegrityError,
    InterfaceError as InterfaceError,
    InternalError as InternalError,
    MySQLError as MySQLError,
    NotSupportedError as NotSupportedError,
    OperationalError as OperationalError,
    ProgrammingError as ProgrammingError,
    Warning as Warning,
)
from .times import (
    Date as Date,
    DateFromTicks as DateFromTicks,
    Time as Time,
    TimeFromTicks as TimeFromTicks,
    Timestamp as Timestamp,
    TimestampFromTicks as TimestampFromTicks,
)

VERSION: Final[tuple[str | int, ...]]
VERSION_STRING: Final[str]
version_info: tuple[int, int, int, str, int]
__version__: str

def get_client_info() -> str: ...
def install_as_MySQLdb() -> None:
    """
    After this function is called, any application that imports MySQLdb
    will unwittingly actually use pymysql.
    """

threadsafety: int
apilevel: str
paramstyle: str

class DBAPISet(frozenset[int]):
    def __ne__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

STRING: DBAPISet
BINARY: DBAPISet
NUMBER: DBAPISet
DATE: DBAPISet
TIME: DBAPISet
TIMESTAMP: DBAPISet
DATETIME: DBAPISet
ROWID: DBAPISet

def Binary(x: Iterable[SupportsIndex] | SupportsIndex | SupportsBytes | ReadableBuffer) -> bytes:
    """Return x as a binary type."""

def thread_safe() -> bool: ...

NULL: str

Connect = connections.Connection
connect = connections.Connection
Connection = connections.Connection

__all__ = [
    "BINARY",
    "Binary",
    "Connect",
    "Connection",
    "DATE",
    "Date",
    "Time",
    "Timestamp",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",
    "DataError",
    "DatabaseError",
    "Error",
    "FIELD_TYPE",
    "IntegrityError",
    "InterfaceError",
    "InternalError",
    "MySQLError",
    "NULL",
    "NUMBER",
    "NotSupportedError",
    "DBAPISet",
    "OperationalError",
    "ProgrammingError",
    "ROWID",
    "STRING",
    "TIME",
    "TIMESTAMP",
    "Warning",
    "apilevel",
    "connect",
    "connections",
    "constants",
    "converters",
    "cursors",
    "get_client_info",
    "paramstyle",
    "threadsafety",
    "version_info",
    "install_as_MySQLdb",
    "__version__",
]
