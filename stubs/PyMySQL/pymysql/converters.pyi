import datetime
import re
import time
from _typeshed import Unused
from collections.abc import Callable, Mapping, Sequence
from decimal import Decimal
from typing import Any, NoReturn, TypeVar
from typing_extensions import TypeAlias, deprecated

_EscaperMapping: TypeAlias = Mapping[type[object], Callable[..., str]] | None
_T = TypeVar("_T")

def escape_item(val: object, charset: object, mapping: _EscaperMapping = None) -> str: ...
@deprecated("dict cannot be used as parameter. It didn't produce valid SQL and might cause SQL injection.")
def escape_dict(val: Mapping[str, object], charset: object, mapping: _EscaperMapping = None) -> NoReturn: ...
def escape_sequence(val: Sequence[object], charset: object, mapping: _EscaperMapping = None) -> str: ...
def escape_set(val: set[object], charset: object, mapping: _EscaperMapping = None) -> str: ...
def escape_bool(value: bool, mapping: _EscaperMapping = None) -> str: ...
def escape_int(value: int, mapping: _EscaperMapping = None) -> str: ...
def escape_float(value: float, mapping: _EscaperMapping = None) -> str: ...
def escape_string(value: str, mapping: _EscaperMapping = None) -> str:
    """escapes *value* without adding quote.

    Value should be unicode
    """

def escape_bytes_prefixed(value: bytes, mapping: _EscaperMapping = None) -> str: ...
def escape_bytes(value: bytes, mapping: _EscaperMapping = None) -> str: ...
def escape_str(value: str, mapping: _EscaperMapping = None) -> str: ...
def escape_None(value: None, mapping: _EscaperMapping = None) -> str: ...
def escape_timedelta(obj: datetime.timedelta, mapping: _EscaperMapping = None) -> str: ...
def escape_time(obj: datetime.time, mapping: _EscaperMapping = None) -> str: ...
def escape_datetime(obj: datetime.datetime, mapping: _EscaperMapping = None) -> str: ...
def escape_date(obj: datetime.date, mapping: _EscaperMapping = None) -> str: ...
def escape_struct_time(obj: time.struct_time, mapping: _EscaperMapping = None) -> str: ...
def Decimal2Literal(o: Decimal, d: Unused) -> str: ...

DATETIME_RE: re.Pattern[str]

def convert_datetime(obj: str | bytes) -> datetime.datetime | str:
    """Returns a DATETIME or TIMESTAMP column value as a datetime object:

      >>> convert_datetime('2007-02-25 23:06:20')
      datetime.datetime(2007, 2, 25, 23, 6, 20)
      >>> convert_datetime('2007-02-25T23:06:20')
      datetime.datetime(2007, 2, 25, 23, 6, 20)

    Illegal values are returned as str:

      >>> convert_datetime('2007-02-31T23:06:20')
      '2007-02-31T23:06:20'
      >>> convert_datetime('0000-00-00 00:00:00')
      '0000-00-00 00:00:00'
    """

TIMEDELTA_RE: re.Pattern[str]

def convert_timedelta(obj: str | bytes) -> datetime.timedelta | str:
    """Returns a TIME column as a timedelta object:

      >>> convert_timedelta('25:06:17')
      datetime.timedelta(days=1, seconds=3977)
      >>> convert_timedelta('-25:06:17')
      datetime.timedelta(days=-2, seconds=82423)

    Illegal values are returned as string:

      >>> convert_timedelta('random crap')
      'random crap'

    Note that MySQL always returns TIME columns as (+|-)HH:MM:SS, but
    can accept values as (+|-)DD HH:MM:SS. The latter format will not
    be parsed correctly by this function.
    """

TIME_RE: re.Pattern[str]

def convert_time(obj: str | bytes) -> datetime.time | str:
    """Returns a TIME column as a time object:

      >>> convert_time('15:06:17')
      datetime.time(15, 6, 17)

    Illegal values are returned as str:

      >>> convert_time('-25:06:17')
      '-25:06:17'
      >>> convert_time('random crap')
      'random crap'

    Note that MySQL always returns TIME columns as (+|-)HH:MM:SS, but
    can accept values as (+|-)DD HH:MM:SS. The latter format will not
    be parsed correctly by this function.

    Also note that MySQL's TIME column corresponds more closely to
    Python's timedelta and not time. However if you want TIME columns
    to be treated as time-of-day and not a time offset, then you can
    use set this function as the converter for FIELD_TYPE.TIME.
    """

def convert_date(obj: str | bytes) -> datetime.date | str:
    """Returns a DATE column as a date object:

      >>> convert_date('2007-02-26')
      datetime.date(2007, 2, 26)

    Illegal values are returned as str:

      >>> convert_date('2007-02-31')
      '2007-02-31'
      >>> convert_date('0000-00-00')
      '0000-00-00'
    """

def through(x: _T) -> _T: ...

convert_bit = through

encoders: dict[type[object], Callable[..., str]]
decoders: dict[int, Callable[[str | bytes], Any]]
conversions: dict[type[object] | int, Callable[..., Any]]
Thing2Literal = escape_str
