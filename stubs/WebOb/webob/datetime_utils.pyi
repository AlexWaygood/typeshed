from datetime import date, datetime, timedelta, tzinfo
from time import _TimeTuple, struct_time

__all__ = [
    "UTC",
    "timedelta_to_seconds",
    "year",
    "month",
    "week",
    "day",
    "hour",
    "minute",
    "second",
    "parse_date",
    "serialize_date",
    "parse_date_delta",
    "serialize_date_delta",
]

class _UTC(tzinfo):
    def dst(self, dt: datetime | None) -> timedelta: ...
    def utcoffset(self, dt: datetime | None) -> timedelta: ...
    def tzname(self, dt: datetime | None) -> str: ...

UTC: _UTC

def timedelta_to_seconds(td: timedelta) -> int:
    """
    Converts a timedelta instance to seconds.
    """

day: timedelta
week: timedelta
hour: timedelta
minute: timedelta
second: timedelta
month: timedelta
year: timedelta

def parse_date(value: str | bytes | None) -> datetime | None: ...
def serialize_date(dt: datetime | date | timedelta | _TimeTuple | struct_time | float | str | bytes) -> str: ...
def parse_date_delta(value: str | bytes | None) -> datetime | None:
    """
    like parse_date, but also handle delta seconds
    """

def serialize_date_delta(value: datetime | date | timedelta | _TimeTuple | struct_time | float | str | bytes) -> str: ...
