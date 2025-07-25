"""
datetime.tzinfo timezone definitions generated from the
Olson timezone database:

    ftp://elsie.nci.nih.gov/pub/tz*.tar.gz

See the datetime section of the Python Library Reference for information
on how to use these modules.
"""

import datetime
from _typeshed import Unused
from collections.abc import Mapping
from typing import ClassVar

from .exceptions import (
    AmbiguousTimeError as AmbiguousTimeError,
    InvalidTimeError as InvalidTimeError,
    NonExistentTimeError as NonExistentTimeError,
    UnknownTimeZoneError as UnknownTimeZoneError,
)
from .tzinfo import BaseTzInfo as BaseTzInfo, DstTzInfo, StaticTzInfo

# Actually named UTC and then masked with a singleton with the same name
class _UTCclass(BaseTzInfo):
    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime: ...
    def normalize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime: ...
    def tzname(self, dt: datetime.datetime | None) -> str: ...
    def utcoffset(self, dt: datetime.datetime | None) -> datetime.timedelta: ...
    def dst(self, dt: datetime.datetime | None) -> datetime.timedelta: ...

utc: _UTCclass
UTC: _UTCclass

def timezone(zone: str) -> _UTCclass | StaticTzInfo | DstTzInfo:
    """Return a datetime.tzinfo implementation for the given timezone

    >>> from datetime import datetime, timedelta
    >>> utc = timezone('UTC')
    >>> eastern = timezone('US/Eastern')
    >>> eastern.zone
    'US/Eastern'
    >>> timezone(unicode('US/Eastern')) is eastern
    True
    >>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
    >>> loc_dt = utc_dt.astimezone(eastern)
    >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
    >>> loc_dt.strftime(fmt)
    '2002-10-27 01:00:00 EST (-0500)'
    >>> (loc_dt - timedelta(minutes=10)).strftime(fmt)
    '2002-10-27 00:50:00 EST (-0500)'
    >>> eastern.normalize(loc_dt - timedelta(minutes=10)).strftime(fmt)
    '2002-10-27 01:50:00 EDT (-0400)'
    >>> (loc_dt + timedelta(minutes=10)).strftime(fmt)
    '2002-10-27 01:10:00 EST (-0500)'

    Raises UnknownTimeZoneError if passed an unknown zone.

    >>> try:
    ...     timezone('Asia/Shangri-La')
    ... except UnknownTimeZoneError:
    ...     print('Unknown')
    Unknown

    >>> try:
    ...     timezone(unicode('\\N{TRADE MARK SIGN}'))
    ... except UnknownTimeZoneError:
    ...     print('Unknown')
    Unknown

    """

class _FixedOffset(datetime.tzinfo):
    zone: ClassVar[None]
    def __init__(self, minutes: int) -> None: ...
    def utcoffset(self, dt: Unused) -> datetime.timedelta | None: ...
    def dst(self, dt: Unused) -> datetime.timedelta: ...
    def tzname(self, dt: Unused) -> None: ...
    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Convert naive time to local time"""

    def normalize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Correct the timezone information on the given datetime"""

def FixedOffset(offset: int, _tzinfos: dict[int, _FixedOffset] = {}) -> _UTCclass | _FixedOffset:
    """return a fixed-offset timezone based off a number of minutes.

        >>> one = FixedOffset(-330)
        >>> one
        pytz.FixedOffset(-330)
        >>> str(one.utcoffset(datetime.datetime.now()))
        '-1 day, 18:30:00'
        >>> str(one.dst(datetime.datetime.now()))
        '0:00:00'

        >>> two = FixedOffset(1380)
        >>> two
        pytz.FixedOffset(1380)
        >>> str(two.utcoffset(datetime.datetime.now()))
        '23:00:00'
        >>> str(two.dst(datetime.datetime.now()))
        '0:00:00'

    The datetime.timedelta must be between the range of -1 and 1 day,
    non-inclusive.

        >>> FixedOffset(1440)
        Traceback (most recent call last):
        ...
        ValueError: ('absolute offset is too large', 1440)

        >>> FixedOffset(-1440)
        Traceback (most recent call last):
        ...
        ValueError: ('absolute offset is too large', -1440)

    An offset of 0 is special-cased to return UTC.

        >>> FixedOffset(0) is UTC
        True

    There should always be only one instance of a FixedOffset per timedelta.
    This should be true for multiple creation calls.

        >>> FixedOffset(-330) is one
        True
        >>> FixedOffset(1380) is two
        True

    It should also be true for pickling.

        >>> import pickle
        >>> pickle.loads(pickle.dumps(one)) is one
        True
        >>> pickle.loads(pickle.dumps(two)) is two
        True
    """

all_timezones: list[str]
all_timezones_set: set[str]
common_timezones: list[str]
common_timezones_set: set[str]
country_timezones: Mapping[str, list[str]]
country_names: Mapping[str, str]
ZERO: datetime.timedelta
HOUR: datetime.timedelta
VERSION: str

__all__ = [
    "timezone",
    "utc",
    "country_timezones",
    "country_names",
    "AmbiguousTimeError",
    "InvalidTimeError",
    "NonExistentTimeError",
    "UnknownTimeZoneError",
    "all_timezones",
    "all_timezones_set",
    "common_timezones",
    "common_timezones_set",
    "BaseTzInfo",
    "FixedOffset",
]
