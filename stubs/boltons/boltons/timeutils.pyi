"""Python's :mod:`datetime` module provides some of the most complex
and powerful primitives in the Python standard library. Time is
nontrivial, but thankfully its support is first-class in
Python. ``dateutils`` provides some additional tools for working with
time.

Additionally, timeutils provides a few basic utilities for working
with timezones in Python. The Python :mod:`datetime` module's
documentation describes how to create a
:class:`~datetime.datetime`-compatible :class:`~datetime.tzinfo`
subtype. It even provides a few examples.

The following module defines usable forms of the timezones in those
docs, as well as a couple other useful ones, :data:`UTC` (aka GMT) and
:data:`LocalTZ` (representing the local timezone as configured in the
operating system). For timezones beyond these, as well as a higher
degree of accuracy in corner cases, check out `pytz`_ and `dateutil`_.

.. _pytz: https://pypi.python.org/pypi/pytz
.. _dateutil: https://dateutil.readthedocs.io/en/stable/index.html
"""

from collections.abc import Generator
from datetime import date, datetime, timedelta, tzinfo

total_seconds = timedelta.total_seconds

def dt_to_timestamp(dt: datetime) -> int:
    """Converts from a :class:`~datetime.datetime` object to an integer
    timestamp, suitable interoperation with :func:`time.time` and
    other `Epoch-based timestamps`.

    .. _Epoch-based timestamps: https://en.wikipedia.org/wiki/Unix_time

    >>> timestamp = int(time.time())
    >>> utc_dt = datetime.fromtimestamp(timestamp, timezone.utc)
    >>> timestamp - dt_to_timestamp(utc_dt)
    0.0

    ``dt_to_timestamp`` supports both timezone-aware and naïve
    :class:`~datetime.datetime` objects. Note that it assumes naïve
    datetime objects are implied UTC, such as those generated with
    :meth:`datetime.datetime.utcnow`. If your datetime objects are
    local time, such as those generated with
    :meth:`datetime.datetime.now`, first convert it using the
    :meth:`datetime.datetime.replace` method with ``tzinfo=``
    :class:`LocalTZ` object in this module, then pass the result of
    that to ``dt_to_timestamp``.
    """

def isoparse(iso_str: str) -> datetime:
    """Parses the limited subset of `ISO8601-formatted time`_ strings as
    returned by :meth:`datetime.datetime.isoformat`.

    >>> epoch_dt = datetime.fromtimestamp(0, timezone.utc).replace(tzinfo=None)
    >>> iso_str = epoch_dt.isoformat()
    >>> print(iso_str)
    1970-01-01T00:00:00
    >>> isoparse(iso_str)
    datetime.datetime(1970, 1, 1, 0, 0)

    >>> utcnow = datetime.now(timezone.utc).replace(tzinfo=None)
    >>> utcnow == isoparse(utcnow.isoformat())
    True

    For further datetime parsing, see the `iso8601`_ package for strict
    ISO parsing and `dateutil`_ package for loose parsing and more.

    .. _ISO8601-formatted time: https://en.wikipedia.org/wiki/ISO_8601
    .. _iso8601: https://pypi.python.org/pypi/iso8601
    .. _dateutil: https://pypi.python.org/pypi/python-dateutil

    """

def parse_timedelta(text: str) -> timedelta:
    """Robustly parses a short text description of a time period into a
    :class:`datetime.timedelta`. Supports weeks, days, hours, minutes,
    and seconds, with or without decimal points:

    Args:
        text (str): Text to parse.
    Returns:
        datetime.timedelta
    Raises:
        ValueError: on parse failure.

    >>> parse_td('1d 2h 3.5m 0s') == timedelta(days=1, seconds=7410)
    True

    Also supports full words and whitespace.

    >>> parse_td('2 weeks 1 day') == timedelta(days=15)
    True

    Negative times are supported, too:

    >>> parse_td('-1.5 weeks 3m 20s') == timedelta(days=-11, seconds=43400)
    True
    """

parse_td = parse_timedelta

def decimal_relative_time(
    d: datetime, other: datetime | None = None, ndigits: int = 0, cardinalize: bool = True
) -> tuple[float, str]:
    """Get a tuple representing the relative time difference between two
    :class:`~datetime.datetime` objects or one
    :class:`~datetime.datetime` and now.

    Args:
        d (datetime): The first datetime object.
        other (datetime): An optional second datetime object. If
            unset, defaults to the current time as determined
            :meth:`datetime.utcnow`.
        ndigits (int): The number of decimal digits to round to,
            defaults to ``0``.
        cardinalize (bool): Whether to pluralize the time unit if
            appropriate, defaults to ``True``.
    Returns:
        (float, str): A tuple of the :class:`float` difference and
           respective unit of time, pluralized if appropriate and
           *cardinalize* is set to ``True``.

    Unlike :func:`relative_time`, this method's return is amenable to
    localization into other languages and custom phrasing and
    formatting.

    >>> now = datetime.now(timezone.utc).replace(tzinfo=None)
    >>> decimal_relative_time(now - timedelta(days=1, seconds=3600), now)
    (1.0, 'day')
    >>> decimal_relative_time(now - timedelta(seconds=0.002), now, ndigits=5)
    (0.002, 'seconds')
    >>> decimal_relative_time(now, now - timedelta(days=900), ndigits=1)
    (-2.5, 'years')

    """

def relative_time(d: datetime, other: datetime | None = None, ndigits: int = 0) -> str:
    """Get a string representation of the difference between two
    :class:`~datetime.datetime` objects or one
    :class:`~datetime.datetime` and the current time. Handles past and
    future times.

    Args:
        d (datetime): The first datetime object.
        other (datetime): An optional second datetime object. If
            unset, defaults to the current time as determined
            :meth:`datetime.utcnow`.
        ndigits (int): The number of decimal digits to round to,
            defaults to ``0``.
    Returns:
        A short English-language string.

    >>> now = datetime.now(timezone.utc).replace(tzinfo=None)
    >>> relative_time(now, ndigits=1)
    '0 seconds ago'
    >>> relative_time(now - timedelta(days=1, seconds=36000), ndigits=1)
    '1.4 days ago'
    >>> relative_time(now + timedelta(days=7), now, ndigits=1)
    '1 week from now'

    """

def strpdate(string: str, format: str) -> date:
    """Parse the date string according to the format in `format`.  Returns a
    :class:`date` object.  Internally, :meth:`datetime.strptime` is used to
    parse the string and thus conversion specifiers for time fields (e.g. `%H`)
    may be provided;  these will be parsed but ignored.

    Args:
        string (str): The date string to be parsed.
        format (str): The `strptime`_-style date format string.
    Returns:
        datetime.date

    .. _`strptime`: https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

    >>> strpdate('2016-02-14', '%Y-%m-%d')
    datetime.date(2016, 2, 14)
    >>> strpdate('26/12 (2015)', '%d/%m (%Y)')
    datetime.date(2015, 12, 26)
    >>> strpdate('20151231 23:59:59', '%Y%m%d %H:%M:%S')
    datetime.date(2015, 12, 31)
    >>> strpdate('20160101 00:00:00.001', '%Y%m%d %H:%M:%S.%f')
    datetime.date(2016, 1, 1)
    """

def daterange(start: date, stop: date, step: int = 1, inclusive: bool = False) -> Generator[date, None, None]:
    """In the spirit of :func:`range` and :func:`xrange`, the `daterange`
    generator that yields a sequence of :class:`~datetime.date`
    objects, starting at *start*, incrementing by *step*, until *stop*
    is reached.

    When *inclusive* is True, the final date may be *stop*, **if**
    *step* falls evenly on it. By default, *step* is one day. See
    details below for many more details.

    Args:
        start (datetime.date): The starting date The first value in
            the sequence.
        stop (datetime.date): The stopping date. By default not
            included in return. Can be `None` to yield an infinite
            sequence.
        step (int): The value to increment *start* by to reach
            *stop*. Can be an :class:`int` number of days, a
            :class:`datetime.timedelta`, or a :class:`tuple` of integers,
            `(year, month, day)`. Positive and negative *step* values
            are supported.
        inclusive (bool): Whether or not the *stop* date can be
            returned. *stop* is only returned when a *step* falls evenly
            on it.

    >>> christmas = date(year=2015, month=12, day=25)
    >>> boxing_day = date(year=2015, month=12, day=26)
    >>> new_year = date(year=2016, month=1,  day=1)
    >>> for day in daterange(christmas, new_year):
    ...     print(repr(day))
    datetime.date(2015, 12, 25)
    datetime.date(2015, 12, 26)
    datetime.date(2015, 12, 27)
    datetime.date(2015, 12, 28)
    datetime.date(2015, 12, 29)
    datetime.date(2015, 12, 30)
    datetime.date(2015, 12, 31)
    >>> for day in daterange(christmas, boxing_day):
    ...     print(repr(day))
    datetime.date(2015, 12, 25)
    >>> for day in daterange(date(2017, 5, 1), date(2017, 8, 1),
    ...                      step=(0, 1, 0), inclusive=True):
    ...     print(repr(day))
    datetime.date(2017, 5, 1)
    datetime.date(2017, 6, 1)
    datetime.date(2017, 7, 1)
    datetime.date(2017, 8, 1)

    *Be careful when using stop=None, as this will yield an infinite
    sequence of dates.*
    """

ZERO: timedelta
HOUR: timedelta

class ConstantTZInfo(tzinfo):
    """
    A :class:`~datetime.tzinfo` subtype whose *offset* remains constant
    (no daylight savings).

    Args:
        name (str): Name of the timezone.
        offset (datetime.timedelta): Offset of the timezone.
    """

    name: str
    offset: timedelta
    def __init__(self, name: str = "ConstantTZ", offset: timedelta = ...) -> None: ...
    @property
    def utcoffset_hours(self) -> str: ...
    def utcoffset(self, dt: datetime | None) -> timedelta: ...
    def tzname(self, dt: datetime | None) -> str: ...
    def dst(self, dt: datetime | None) -> timedelta: ...

UTC: ConstantTZInfo
EPOCH_AWARE: datetime

class LocalTZInfo(tzinfo):
    """The ``LocalTZInfo`` type takes data available in the time module
    about the local timezone and makes a practical
    :class:`datetime.tzinfo` to represent the timezone settings of the
    operating system.

    For a more in-depth integration with the operating system, check
    out `tzlocal`_. It builds on `pytz`_ and implements heuristics for
    many versions of major operating systems to provide the official
    ``pytz`` tzinfo, instead of the LocalTZ generalization.

    .. _tzlocal: https://pypi.python.org/pypi/tzlocal
    .. _pytz: https://pypi.python.org/pypi/pytz

    """

    def is_dst(self, dt: datetime) -> bool: ...
    def utcoffset(self, dt: datetime) -> timedelta: ...  # type: ignore[override] # Doesn't support None
    def dst(self, dt: datetime) -> timedelta: ...  # type: ignore[override] # Doesn't support None
    def tzname(self, dt: datetime) -> str: ...  # type: ignore[override] # Doesn't support None

LocalTZ: LocalTZInfo
DSTSTART_2007: datetime
DSTEND_2007: datetime
DSTSTART_1987_2006: datetime
DSTEND_1987_2006: datetime
DSTSTART_1967_1986: datetime
DSTEND_1967_1986: datetime

class USTimeZone(tzinfo):
    """Copied directly from the Python docs, the ``USTimeZone`` is a
    :class:`datetime.tzinfo` subtype used to create the
    :data:`Eastern`, :data:`Central`, :data:`Mountain`, and
    :data:`Pacific` tzinfo types.
    """

    stdoffset: timedelta
    reprname: str
    stdname: str
    dstname: str
    def __init__(self, hours: int, reprname: str, stdname: str, dstname: str) -> None: ...
    def tzname(self, dt: datetime | None) -> str: ...
    def utcoffset(self, dt: datetime | None) -> timedelta: ...
    def dst(self, dt: datetime | None) -> timedelta: ...

Eastern: USTimeZone
Central: USTimeZone
Mountain: USTimeZone
Pacific: USTimeZone
