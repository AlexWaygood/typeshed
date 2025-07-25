"""Base classes and helpers for building zone specific tzinfo classes"""

import datetime
from abc import abstractmethod
from typing import Any, overload

class BaseTzInfo(datetime.tzinfo):
    _utcoffset: datetime.timedelta | None
    _tzname: str | None
    zone: str | None  # Actually None but should be set on concrete subclasses
    # The following abstract methods don't exist in the implementation, but
    # are implemented by all sub-classes.
    @abstractmethod
    def localize(self, dt: datetime.datetime, is_dst: bool | None = ...) -> datetime.datetime: ...
    @abstractmethod
    def normalize(self, dt: datetime.datetime) -> datetime.datetime: ...
    @abstractmethod
    def tzname(self, dt: datetime.datetime | None, /) -> str:
        """datetime -> string name of time zone."""

    @abstractmethod
    def utcoffset(self, dt: datetime.datetime | None, /) -> datetime.timedelta | None:
        """datetime -> timedelta showing offset from UTC, negative values indicating West of UTC"""

    @abstractmethod
    def dst(self, dt: datetime.datetime | None, /) -> datetime.timedelta | None:
        """datetime -> DST offset as timedelta positive east of UTC."""

class StaticTzInfo(BaseTzInfo):
    """A timezone that has a constant offset from UTC

    These timezones are rare, as most locations have changed their
    offset at some point in their history
    """

    def fromutc(self, dt: datetime.datetime) -> datetime.datetime:
        """See datetime.tzinfo.fromutc"""

    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Convert naive time to local time"""

    def normalize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Correct the timezone information on the given datetime.

        This is normally a no-op, as StaticTzInfo timezones never have
        ambiguous cases to correct:

        >>> from pytz import timezone
        >>> gmt = timezone('GMT')
        >>> isinstance(gmt, StaticTzInfo)
        True
        >>> dt = datetime(2011, 5, 8, 1, 2, 3, tzinfo=gmt)
        >>> gmt.normalize(dt) is dt
        True

        The supported method of converting between timezones is to use
        datetime.astimezone(). Currently normalize() also works:

        >>> la = timezone('America/Los_Angeles')
        >>> dt = la.localize(datetime(2011, 5, 7, 1, 2, 3))
        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
        >>> gmt.normalize(dt).strftime(fmt)
        '2011-05-07 08:02:03 GMT (+0000)'
        """

    def tzname(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> str:
        """See datetime.tzinfo.tzname

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """

    def utcoffset(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta:
        """See datetime.tzinfo.utcoffset

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """

    def dst(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta:
        """See datetime.tzinfo.dst

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """

class DstTzInfo(BaseTzInfo):
    """A timezone that has a variable offset from UTC

    The offset might change if daylight saving time comes into effect,
    or at a point in history when the region decides to change their
    timezone definition.
    """

    def __init__(self, _inf: Any = None, _tzinfos: Any = None) -> None: ...
    def fromutc(self, dt: datetime.datetime) -> datetime.datetime:
        """See datetime.tzinfo.fromutc"""

    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Convert naive time to local time.

        This method should be used to construct localtimes, rather
        than passing a tzinfo argument to a datetime constructor.

        is_dst is used to determine the correct timezone in the ambigous
        period at the end of daylight saving time.

        >>> from pytz import timezone
        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
        >>> amdam = timezone('Europe/Amsterdam')
        >>> dt  = datetime(2004, 10, 31, 2, 0, 0)
        >>> loc_dt1 = amdam.localize(dt, is_dst=True)
        >>> loc_dt2 = amdam.localize(dt, is_dst=False)
        >>> loc_dt1.strftime(fmt)
        '2004-10-31 02:00:00 CEST (+0200)'
        >>> loc_dt2.strftime(fmt)
        '2004-10-31 02:00:00 CET (+0100)'
        >>> str(loc_dt2 - loc_dt1)
        '1:00:00'

        Use is_dst=None to raise an AmbiguousTimeError for ambiguous
        times at the end of daylight saving time

        >>> try:
        ...     loc_dt1 = amdam.localize(dt, is_dst=None)
        ... except AmbiguousTimeError:
        ...     print('Ambiguous')
        Ambiguous

        is_dst defaults to False

        >>> amdam.localize(dt) == amdam.localize(dt, False)
        True

        is_dst is also used to determine the correct timezone in the
        wallclock times jumped over at the start of daylight saving time.

        >>> pacific = timezone('US/Pacific')
        >>> dt = datetime(2008, 3, 9, 2, 0, 0)
        >>> ploc_dt1 = pacific.localize(dt, is_dst=True)
        >>> ploc_dt2 = pacific.localize(dt, is_dst=False)
        >>> ploc_dt1.strftime(fmt)
        '2008-03-09 02:00:00 PDT (-0700)'
        >>> ploc_dt2.strftime(fmt)
        '2008-03-09 02:00:00 PST (-0800)'
        >>> str(ploc_dt2 - ploc_dt1)
        '1:00:00'

        Use is_dst=None to raise a NonExistentTimeError for these skipped
        times.

        >>> try:
        ...     loc_dt1 = pacific.localize(dt, is_dst=None)
        ... except NonExistentTimeError:
        ...     print('Non-existent')
        Non-existent
        """

    def normalize(self, dt: datetime.datetime) -> datetime.datetime:
        """Correct the timezone information on the given datetime

        If date arithmetic crosses DST boundaries, the tzinfo
        is not magically adjusted. This method normalizes the
        tzinfo to the correct one.

        To test, first we need to do some setup

        >>> from pytz import timezone
        >>> utc = timezone('UTC')
        >>> eastern = timezone('US/Eastern')
        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'

        We next create a datetime right on an end-of-DST transition point,
        the instant when the wallclocks are wound back one hour.

        >>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
        >>> loc_dt = utc_dt.astimezone(eastern)
        >>> loc_dt.strftime(fmt)
        '2002-10-27 01:00:00 EST (-0500)'

        Now, if we subtract a few minutes from it, note that the timezone
        information has not changed.

        >>> before = loc_dt - timedelta(minutes=10)
        >>> before.strftime(fmt)
        '2002-10-27 00:50:00 EST (-0500)'

        But we can fix that by calling the normalize method

        >>> before = eastern.normalize(before)
        >>> before.strftime(fmt)
        '2002-10-27 01:50:00 EDT (-0400)'

        The supported method of converting between timezones is to use
        datetime.astimezone(). Currently, normalize() also works:

        >>> th = timezone('Asia/Bangkok')
        >>> am = timezone('Europe/Amsterdam')
        >>> dt = th.localize(datetime(2011, 5, 7, 1, 2, 3))
        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
        >>> am.normalize(dt).strftime(fmt)
        '2011-05-06 20:02:03 CEST (+0200)'
        """

    def tzname(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> str:
        """See datetime.tzinfo.tzname

        The is_dst parameter may be used to remove ambiguity during DST
        transitions.

        >>> from pytz import timezone
        >>> tz = timezone('America/St_Johns')

        >>> normal = datetime(2009, 9, 1)

        >>> tz.tzname(normal)
        'NDT'
        >>> tz.tzname(normal, is_dst=False)
        'NDT'
        >>> tz.tzname(normal, is_dst=True)
        'NDT'

        >>> ambiguous = datetime(2009, 10, 31, 23, 30)

        >>> tz.tzname(ambiguous, is_dst=False)
        'NST'
        >>> tz.tzname(ambiguous, is_dst=True)
        'NDT'
        >>> try:
        ...     tz.tzname(ambiguous)
        ... except AmbiguousTimeError:
        ...     print('Ambiguous')
        Ambiguous
        """
    # https://github.com/python/mypy/issues/12379
    @overload  # type: ignore[override]
    def utcoffset(self, dt: None, is_dst: bool | None = None) -> None:
        """See datetime.tzinfo.utcoffset

        The is_dst parameter may be used to remove ambiguity during DST
        transitions.

        >>> from pytz import timezone
        >>> tz = timezone('America/St_Johns')
        >>> ambiguous = datetime(2009, 10, 31, 23, 30)

        >>> str(tz.utcoffset(ambiguous, is_dst=False))
        '-1 day, 20:30:00'

        >>> str(tz.utcoffset(ambiguous, is_dst=True))
        '-1 day, 21:30:00'

        >>> try:
        ...     tz.utcoffset(ambiguous)
        ... except AmbiguousTimeError:
        ...     print('Ambiguous')
        Ambiguous

        """

    @overload
    def utcoffset(self, dt: datetime.datetime, is_dst: bool | None = None) -> datetime.timedelta: ...
    def dst(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta | None:
        """See datetime.tzinfo.dst

        The is_dst parameter may be used to remove ambiguity during DST
        transitions.

        >>> from pytz import timezone
        >>> tz = timezone('America/St_Johns')

        >>> normal = datetime(2009, 9, 1)

        >>> str(tz.dst(normal))
        '1:00:00'
        >>> str(tz.dst(normal, is_dst=False))
        '1:00:00'
        >>> str(tz.dst(normal, is_dst=True))
        '1:00:00'

        >>> ambiguous = datetime(2009, 10, 31, 23, 30)

        >>> str(tz.dst(ambiguous, is_dst=False))
        '0:00:00'
        >>> str(tz.dst(ambiguous, is_dst=True))
        '1:00:00'
        >>> try:
        ...     tz.dst(ambiguous)
        ... except AmbiguousTimeError:
        ...     print('Ambiguous')
        Ambiguous

        """

__all__: list[str] = []
