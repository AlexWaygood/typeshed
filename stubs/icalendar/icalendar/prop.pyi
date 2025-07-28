"""This module contains the parser/generators (or coders/encoders if you
prefer) for the classes/datatypes that are used in iCalendar:

###########################################################################

# This module defines these property value data types and property parameters

4.2 Defined property parameters are:

.. code-block:: text

     ALTREP, CN, CUTYPE, DELEGATED-FROM, DELEGATED-TO, DIR, ENCODING, FMTTYPE,
     FBTYPE, LANGUAGE, MEMBER, PARTSTAT, RANGE, RELATED, RELTYPE, ROLE, RSVP,
     SENT-BY, TZID, VALUE

4.3 Defined value data types are:

.. code-block:: text

    BINARY, BOOLEAN, CAL-ADDRESS, DATE, DATE-TIME, DURATION, FLOAT, INTEGER,
    PERIOD, RECUR, TEXT, TIME, URI, UTC-OFFSET

###########################################################################

iCalendar properties have values. The values are strongly typed. This module
defines these types, calling val.to_ical() on them will render them as defined
in rfc5545.

If you pass any of these classes a Python primitive, you will have an object
that can render itself as iCalendar formatted date.

Property Value Data Types start with a 'v'. they all have an to_ical() and
from_ical() method. The to_ical() method generates a text string in the
iCalendar format. The from_ical() method can parse this format and return a
primitive Python datatype. So it should always be true that:

.. code-block:: python

    x == vDataType.from_ical(VDataType(x).to_ical())

These types are mainly used for parsing and file generation. But you can set
them directly.
"""

import datetime
from _typeshed import ConvertibleToFloat, ConvertibleToInt, SupportsKeysAndGetItem, Unused
from collections.abc import Iterable, Iterator
from enum import Enum
from re import Pattern
from typing import Any, ClassVar, Final, Literal, Protocol, SupportsIndex, overload
from typing_extensions import Self, TypeAlias

from .caselessdict import CaselessDict
from .parser import Parameters
from .parser_tools import ICAL_TYPE
from .timezone import tzid_from_dt as tzid_from_dt, tzid_from_tzinfo as tzid_from_tzinfo

__all__ = [
    "DURATION_REGEX",
    "TimeBase",
    "TypesFactory",
    "WEEKDAY_RULE",
    "tzid_from_dt",
    "vBinary",
    "vBoolean",
    "vCalAddress",
    "vCategory",
    "vDDDLists",
    "vDDDTypes",
    "vDate",
    "vDatetime",
    "vDuration",
    "vFloat",
    "vFrequency",
    "vGeo",
    "vInline",
    "vInt",
    "vMonth",
    "vPeriod",
    "vRecur",
    "vText",
    "vTime",
    "vUTCOffset",
    "vUri",
    "vWeekday",
    "tzid_from_tzinfo",
    "vSkip",
]

_PropType: TypeAlias = type[Any]  # any of the v* classes in this file
_PeriodTuple: TypeAlias = tuple[datetime.datetime, datetime.datetime | datetime.timedelta]
_AnyTimeType: TypeAlias = datetime.datetime | datetime.date | datetime.timedelta | datetime.time | _PeriodTuple

class _vType(Protocol):
    def to_ical(self) -> bytes | str: ...

DURATION_REGEX: Final[Pattern[str]]
WEEKDAY_RULE: Final[Pattern[str]]

class vBinary:
    """Binary property values are base 64 encoded."""

    obj: str
    params: Parameters
    def __init__(self, obj: str | bytes) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE) -> bytes: ...
    def __eq__(self, other: object) -> bool:
        """self == other"""

class vBoolean(int):
    """Boolean

    Value Name:  BOOLEAN

    Purpose:  This value type is used to identify properties that contain
      either a "TRUE" or "FALSE" Boolean value.

    Format Definition:  This value type is defined by the following
      notation:

    .. code-block:: text

        boolean    = "TRUE" / "FALSE"

    Description:  These values are case-insensitive text.  No additional
      content value encoding is defined for this value type.

    Example:  The following is an example of a hypothetical property that
      has a BOOLEAN value type:

    .. code-block:: python

        TRUE

    .. code-block:: pycon

        >>> from icalendar.prop import vBoolean
        >>> boolean = vBoolean.from_ical('TRUE')
        >>> boolean
        True
        >>> boolean = vBoolean.from_ical('FALSE')
        >>> boolean
        False
        >>> boolean = vBoolean.from_ical('True')
        >>> boolean
        True
    """

    BOOL_MAP: Final[CaselessDict[bool]]
    params: Parameters
    def __new__(cls, x: ConvertibleToInt = ..., /, *, params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> Literal[b"TRUE", b"FALSE"]: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> bool: ...

class vText(str):
    """Simple text."""

    encoding: str
    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...
    ALTREP: property
    LANGUAGE: property
    RELTYPE: property

class vCalAddress(str):
    """Calendar User Address

    Value Name:
        CAL-ADDRESS

    Purpose:
        This value type is used to identify properties that contain a
        calendar user address.

    Description:
        The value is a URI as defined by [RFC3986] or any other
        IANA-registered form for a URI.  When used to address an Internet
        email transport address for a calendar user, the value MUST be a
        mailto URI, as defined by [RFC2368].

    Example:
        ``mailto:`` is in front of the address.

        .. code-block:: text

            mailto:jane_doe@example.com

        Parsing:

        .. code-block:: pycon

            >>> from icalendar import vCalAddress
            >>> cal_address = vCalAddress.from_ical('mailto:jane_doe@example.com')
            >>> cal_address
            vCalAddress('mailto:jane_doe@example.com')

        Encoding:

        .. code-block:: pycon

            >>> from icalendar import vCalAddress, Event
            >>> event = Event()
            >>> jane = vCalAddress("mailto:jane_doe@example.com")
            >>> jane.name = "Jane"
            >>> event["organizer"] = jane
            >>> print(event.to_ical())
            BEGIN:VEVENT
            ORGANIZER;CN=Jane:mailto:jane_doe@example.com
            END:VEVENT
    """

    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding="utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...
    @property
    def email(self) -> str:
        """The email address without mailto: at the start."""

    @property
    def name(self) -> str:
        """Specify the common name to be associated with the calendar user specified.

        Description:
            This parameter can be specified on properties with a
            CAL-ADDRESS value type.  The parameter specifies the common name
            to be associated with the calendar user specified by the property.
            The parameter value is text.  The parameter value can be used for
            display text to be associated with the calendar address specified
            by the property.
        """

    @name.setter
    def name(self, value: str) -> None: ...
    @name.deleter
    def name(self) -> None: ...
    CN: property
    CUTYPE: property
    DELEGATED_FROM: property
    DELEGATED_TO: property
    DIR: property
    LANGUAGE: property
    PARTSTAT: property
    ROLE: property
    RSVP: property
    SENT_BY: property

class vFloat(float):
    """Float

    Value Name:
        FLOAT

    Purpose:
        This value type is used to identify properties that contain
        a real-number value.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            float      = (["+"] / "-") 1*DIGIT ["." 1*DIGIT]

    Description:
        If the property permits, multiple "float" values are
        specified by a COMMA-separated list of values.

        Example:

        .. code-block:: text

            1000000.0000001
            1.333
            -3.14

        .. code-block:: pycon

            >>> from icalendar.prop import vFloat
            >>> float = vFloat.from_ical('1000000.0000001')
            >>> float
            1000000.0000001
            >>> float = vFloat.from_ical('1.333')
            >>> float
            1.333
            >>> float = vFloat.from_ical('+1.333')
            >>> float
            1.333
            >>> float = vFloat.from_ical('-3.14')
            >>> float
            -3.14
    """

    params: Parameters
    def __new__(cls, x: ConvertibleToFloat = ..., /, *, params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vInt(int):
    """Integer

    Value Name:
        INTEGER

    Purpose:
        This value type is used to identify properties that contain a
        signed integer value.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            integer    = (["+"] / "-") 1*DIGIT

    Description:
        If the property permits, multiple "integer" values are
        specified by a COMMA-separated list of values.  The valid range
        for "integer" is -2147483648 to 2147483647.  If the sign is not
        specified, then the value is assumed to be positive.

        Example:

        .. code-block:: text

            1234567890
            -1234567890
            +1234567890
            432109876

        .. code-block:: pycon

            >>> from icalendar.prop import vInt
            >>> integer = vInt.from_ical('1234567890')
            >>> integer
            1234567890
            >>> integer = vInt.from_ical('-1234567890')
            >>> integer
            -1234567890
            >>> integer = vInt.from_ical('+1234567890')
            >>> integer
            1234567890
            >>> integer = vInt.from_ical('432109876')
            >>> integer
            432109876
    """

    params: Parameters
    def __new__(cls, x: ConvertibleToInt = ..., /, *, params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vDDDLists:
    """A list of vDDDTypes values."""

    params: Parameters
    dts: list[vDDDTypes]
    def __init__(self, dt_list: Iterable[_AnyTimeType] | _AnyTimeType) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: str, timezone: str | datetime.timezone | None = None): ...
    def __eq__(self, other: object) -> bool: ...

class vCategory:
    cats: list[vText]
    params: Parameters
    def __init__(self, c_list: Iterable[ICAL_TYPE] | ICAL_TYPE, params: SupportsKeysAndGetItem[str, str] = {}) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE) -> str: ...
    def __eq__(self, other: object) -> bool:
        """self == other"""
    RANGE: property
    RELATED: property
    TZID: property

class TimeBase:
    """Make classes with a datetime/date comparable."""

    params: Parameters
    ignore_for_equality: set[str]
    def __eq__(self, other: object) -> bool:
        """self == other"""

    def __hash__(self) -> int: ...
    RANGE: property
    RELATED: property
    TZID: property

class vDDDTypes(TimeBase):
    """A combined Datetime, Date or Duration parser/generator. Their format
    cannot be confused, and often values can be of either types.
    So this is practical.
    """

    params: Parameters
    dt: _AnyTimeType
    def __init__(self, dt: _AnyTimeType) -> None: ...
    def to_ical(self) -> bytes: ...
    @overload
    @classmethod
    def from_ical(cls, ical: Self, timezone: Unused | None = None) -> _AnyTimeType: ...
    # Return type is one of vDuration, vPeriod, vDatetime, vDate, or vTime,
    # depending on the ical string.
    @overload
    @classmethod
    def from_ical(cls, ical: str, timezone: datetime.timezone | str | None = None) -> Any: ...

class vDate(TimeBase):
    """Date

    Value Name:
        DATE

    Purpose:
        This value type is used to identify values that contain a
        calendar date.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            date               = date-value

            date-value         = date-fullyear date-month date-mday
            date-fullyear      = 4DIGIT
            date-month         = 2DIGIT        ;01-12
            date-mday          = 2DIGIT        ;01-28, 01-29, 01-30, 01-31
                                               ;based on month/year

    Description:
        If the property permits, multiple "date" values are
        specified as a COMMA-separated list of values.  The format for the
        value type is based on the [ISO.8601.2004] complete
        representation, basic format for a calendar date.  The textual
        format specifies a four-digit year, two-digit month, and two-digit
        day of the month.  There are no separator characters between the
        year, month, and day component text.

    Example:
        The following represents July 14, 1997:

        .. code-block:: text

            19970714

        .. code-block:: pycon

            >>> from icalendar.prop import vDate
            >>> date = vDate.from_ical('19970714')
            >>> date.year
            1997
            >>> date.month
            7
            >>> date.day
            14
    """

    dt: datetime.date
    params: Parameters
    def __init__(self, dt: datetime.date) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE) -> datetime.date: ...

class vDatetime(TimeBase):
    """Render and generates icalendar datetime format.

    vDatetime is timezone aware and uses a timezone library.
    When a vDatetime object is created from an
    ical string, you can pass a valid timezone identifier. When a
    vDatetime object is created from a python datetime object, it uses the
    tzinfo component, if present. Otherwise a timezone-naive object is
    created. Be aware that there are certain limitations with timezone naive
    DATE-TIME components in the icalendar standard.
    """

    dt: datetime.datetime
    params: Parameters
    def __init__(self, dt: datetime.datetime, params: SupportsKeysAndGetItem[str, str] = {}) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE, timezone: datetime.timezone | str | None = None) -> datetime.datetime:
        """Create a datetime from the RFC string.

        Format:

        .. code-block:: text

            YYYYMMDDTHHMMSS

        .. code-block:: pycon

            >>> from icalendar import vDatetime
            >>> vDatetime.from_ical("20210302T101500")
            datetime.datetime(2021, 3, 2, 10, 15)

            >>> vDatetime.from_ical("20210302T101500", "America/New_York")
            datetime.datetime(2021, 3, 2, 10, 15, tzinfo=ZoneInfo(key='America/New_York'))

            >>> from zoneinfo import ZoneInfo
            >>> timezone = ZoneInfo("Europe/Berlin")
            >>> vDatetime.from_ical("20210302T101500", timezone)
            datetime.datetime(2021, 3, 2, 10, 15, tzinfo=ZoneInfo(key='Europe/Berlin'))
        """

class vDuration(TimeBase):
    """Duration

    Value Name:
        DURATION

    Purpose:
        This value type is used to identify properties that contain
        a duration of time.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            dur-value  = (["+"] / "-") "P" (dur-date / dur-time / dur-week)

            dur-date   = dur-day [dur-time]
            dur-time   = "T" (dur-hour / dur-minute / dur-second)
            dur-week   = 1*DIGIT "W"
            dur-hour   = 1*DIGIT "H" [dur-minute]
            dur-minute = 1*DIGIT "M" [dur-second]
            dur-second = 1*DIGIT "S"
            dur-day    = 1*DIGIT "D"

    Description:
        If the property permits, multiple "duration" values are
        specified by a COMMA-separated list of values.  The format is
        based on the [ISO.8601.2004] complete representation basic format
        with designators for the duration of time.  The format can
        represent nominal durations (weeks and days) and accurate
        durations (hours, minutes, and seconds).  Note that unlike
        [ISO.8601.2004], this value type doesn't support the "Y" and "M"
        designators to specify durations in terms of years and months.
        The duration of a week or a day depends on its position in the
        calendar.  In the case of discontinuities in the time scale, such
        as the change from standard time to daylight time and back, the
        computation of the exact duration requires the subtraction or
        addition of the change of duration of the discontinuity.  Leap
        seconds MUST NOT be considered when computing an exact duration.
        When computing an exact duration, the greatest order time
        components MUST be added first, that is, the number of days MUST
        be added first, followed by the number of hours, number of
        minutes, and number of seconds.

    Example:
        A duration of 15 days, 5 hours, and 20 seconds would be:

        .. code-block:: text

            P15DT5H0M20S

        A duration of 7 weeks would be:

        .. code-block:: text

            P7W

        .. code-block:: pycon

            >>> from icalendar.prop import vDuration
            >>> duration = vDuration.from_ical('P15DT5H0M20S')
            >>> duration
            datetime.timedelta(days=15, seconds=18020)
            >>> duration = vDuration.from_ical('P7W')
            >>> duration
            datetime.timedelta(days=49)
    """

    td: datetime.timedelta
    params: Parameters
    def __init__(self, td: datetime.timedelta, params: SupportsKeysAndGetItem[str, str] = {}) -> None: ...
    def to_ical(self) -> bytes: ...
    @staticmethod
    def from_ical(ical: str) -> datetime.timedelta: ...
    @property
    def dt(self) -> datetime.timedelta:
        """The time delta for compatibility."""

class vPeriod(TimeBase):
    """Period of Time

    Value Name:
        PERIOD

    Purpose:
        This value type is used to identify values that contain a
        precise period of time.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            period     = period-explicit / period-start

           period-explicit = date-time "/" date-time
           ; [ISO.8601.2004] complete representation basic format for a
           ; period of time consisting of a start and end.  The start MUST
           ; be before the end.

           period-start = date-time "/" dur-value
           ; [ISO.8601.2004] complete representation basic format for a
           ; period of time consisting of a start and positive duration
           ; of time.

    Description:
        If the property permits, multiple "period" values are
        specified by a COMMA-separated list of values.  There are two
        forms of a period of time.  First, a period of time is identified
        by its start and its end.  This format is based on the
        [ISO.8601.2004] complete representation, basic format for "DATE-
        TIME" start of the period, followed by a SOLIDUS character
        followed by the "DATE-TIME" of the end of the period.  The start
        of the period MUST be before the end of the period.  Second, a
        period of time can also be defined by a start and a positive
        duration of time.  The format is based on the [ISO.8601.2004]
        complete representation, basic format for the "DATE-TIME" start of
        the period, followed by a SOLIDUS character, followed by the
        [ISO.8601.2004] basic format for "DURATION" of the period.

    Example:
        The period starting at 18:00:00 UTC, on January 1, 1997 and
        ending at 07:00:00 UTC on January 2, 1997 would be:

        .. code-block:: text

            19970101T180000Z/19970102T070000Z

        The period start at 18:00:00 on January 1, 1997 and lasting 5 hours
        and 30 minutes would be:

        .. code-block:: text

            19970101T180000Z/PT5H30M

        .. code-block:: pycon

            >>> from icalendar.prop import vPeriod
            >>> period = vPeriod.from_ical('19970101T180000Z/19970102T070000Z')
            >>> period = vPeriod.from_ical('19970101T180000Z/PT5H30M')
    """

    params: Parameters
    start: datetime.datetime
    end: datetime.datetime
    by_duration: bool
    duration: datetime.timedelta
    def __init__(self, per: _PeriodTuple) -> None: ...
    def overlaps(self, other: vPeriod) -> bool: ...
    def to_ical(self) -> bytes: ...
    # Return type is a tuple of vDuration, vPeriod, vDatetime, vDate, or vTime,
    # depending on the ical string. If the ical string is formed according to
    # the iCalendar specification, this should always return a
    # (datetime, datetime) or a (datetime, timedelta) tuple, but this is not
    # enforced.
    @staticmethod
    def from_ical(ical: str, timezone: datetime.timezone | str | None = None) -> tuple[Any, Any]: ...
    @property
    def dt(self) -> _PeriodTuple:
        """Make this cooperate with the other vDDDTypes."""
    FBTYPE: property

class vWeekday(str):
    """Either a ``weekday`` or a ``weekdaynum``

    .. code-block:: pycon

        >>> from icalendar import vWeekday
        >>> vWeekday("MO") # Simple weekday
        'MO'
        >>> vWeekday("2FR").relative # Second friday
        2
        >>> vWeekday("2FR").weekday
        'FR'
        >>> vWeekday("-1SU").relative # Last Sunday
        -1

    Definition from `RFC 5545, Section 3.3.10 <https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10>`_:

    .. code-block:: text

        weekdaynum = [[plus / minus] ordwk] weekday
        plus        = "+"
        minus       = "-"
        ordwk       = 1*2DIGIT       ;1 to 53
        weekday     = "SU" / "MO" / "TU" / "WE" / "TH" / "FR" / "SA"
        ;Corresponding to SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
        ;FRIDAY, and SATURDAY days of the week.

    """

    week_days: Final[CaselessDict[int]]
    weekday: Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"] | None
    relative: int | None
    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vFrequency(str):
    """A simple class that catches illegal values."""

    frequencies: Final[CaselessDict[str]]
    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vMonth(int):
    """The number of the month for recurrence.

    In :rfc:`5545`, this is just an int.
    In :rfc:`7529`, this can be followed by `L` to indicate a leap month.

    .. code-block:: pycon

        >>> from icalendar import vMonth
        >>> vMonth(1) # first month January
        vMonth('1')
        >>> vMonth("5L") # leap month in Hebrew calendar
        vMonth('5L')
        >>> vMonth(1).leap
        False
        >>> vMonth("5L").leap
        True

    Definition from RFC:

    .. code-block:: text

        type-bymonth = element bymonth {
           xsd:positiveInteger |
           xsd:string
        }
    """

    params: Parameters
    def __new__(cls, month: vMonth | str | int, params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes:
        """The ical representation."""

    @classmethod
    def from_ical(cls, ical: vMonth | str | int) -> Self: ...
    @property
    def leap(self) -> bool:
        """Whether this is a leap month."""

    @leap.setter
    def leap(self, value: bool) -> None: ...

class vSkip(vText, Enum):
    """Skip values for RRULE.

    These are defined in :rfc:`7529`.

    OMIT  is the default value.

    Examples:

    .. code-block:: pycon

        >>> from icalendar import vSkip
        >>> vSkip.OMIT
        vSkip('OMIT')
        >>> vSkip.FORWARD
        vSkip('FORWARD')
        >>> vSkip.BACKWARD
        vSkip('BACKWARD')
    """

    OMIT = "OMIT"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"

    def __reduce_ex__(self, _p: Unused) -> tuple[Self, tuple[str]]:
        """For pickling."""

# The type of the values depend on the key. Each key maps to a v* class, and
# the allowed types are the types that the corresponding v* class can parse.
class vRecur(CaselessDict[Iterable[Any] | Any]):
    """Recurrence definition.

    Property Name:
        RRULE

    Purpose:
        This property defines a rule or repeating pattern for recurring events, to-dos,
        journal entries, or time zone definitions.

    Value Type:
        RECUR

    Property Parameters:
        IANA and non-standard property parameters can be specified on this property.

    Conformance:
        This property can be specified in recurring "VEVENT", "VTODO", and "VJOURNAL"
        calendar components as well as in the "STANDARD" and "DAYLIGHT" sub-components
        of the "VTIMEZONE" calendar component, but it SHOULD NOT be specified more than once.
        The recurrence set generated with multiple "RRULE" properties is undefined.

    Description:
        The recurrence rule, if specified, is used in computing the recurrence set.
        The recurrence set is the complete set of recurrence instances for a calendar component.
        The recurrence set is generated by considering the initial "DTSTART" property along
        with the "RRULE", "RDATE", and "EXDATE" properties contained within the
        recurring component. The "DTSTART" property defines the first instance in the
        recurrence set. The "DTSTART" property value SHOULD be synchronized with the
        recurrence rule, if specified. The recurrence set generated with a "DTSTART" property
        value not synchronized with the recurrence rule is undefined.
        The final recurrence set is generated by gathering all of the start DATE-TIME
        values generated by any of the specified "RRULE" and "RDATE" properties, and then
        excluding any start DATE-TIME values specified by "EXDATE" properties.
        This implies that start DATE- TIME values specified by "EXDATE" properties take
        precedence over those specified by inclusion properties (i.e., "RDATE" and "RRULE").
        Where duplicate instances are generated by the "RRULE" and "RDATE" properties,
        only one recurrence is considered. Duplicate instances are ignored.

        The "DTSTART" property specified within the iCalendar object defines the first
        instance of the recurrence. In most cases, a "DTSTART" property of DATE-TIME value
        type used with a recurrence rule, should be specified as a date with local time
        and time zone reference to make sure all the recurrence instances start at the
        same local time regardless of time zone changes.

        If the duration of the recurring component is specified with the "DTEND" or
        "DUE" property, then the same exact duration will apply to all the members of the
        generated recurrence set. Else, if the duration of the recurring component is
        specified with the "DURATION" property, then the same nominal duration will apply
        to all the members of the generated recurrence set and the exact duration of each
        recurrence instance will depend on its specific start time. For example, recurrence
        instances of a nominal duration of one day will have an exact duration of more or less
        than 24 hours on a day where a time zone shift occurs. The duration of a specific
        recurrence may be modified in an exception component or simply by using an
        "RDATE" property of PERIOD value type.

    Examples:
        The following RRULE specifies daily events for 10 occurrences.

        .. code-block:: text

            RRULE:FREQ=DAILY;COUNT=10

        Below, we parse the RRULE ical string.

        .. code-block:: pycon

            >>> from icalendar.prop import vRecur
            >>> rrule = vRecur.from_ical('FREQ=DAILY;COUNT=10')
            >>> rrule
            vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})

        You can choose to add an rrule to an :class:`icalendar.cal.Event` or
        :class:`icalendar.cal.Todo`.

        .. code-block:: pycon

            >>> from icalendar import Event
            >>> event = Event()
            >>> event.add('RRULE', 'FREQ=DAILY;COUNT=10')
            >>> event.rrules
            [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]
    """

    params: Parameters
    frequencies: Final[list[str]]
    canonical_order: ClassVar[tuple[str, ...]]
    types: Final[CaselessDict[_PropType]]
    def __init__(
        self, *args, params: SupportsKeysAndGetItem[str, str] = {}, **kwargs: list[Any] | tuple[Any, ...] | Any
    ) -> None: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def parse_type(cls, key: str, values: str) -> list[Any]: ...  # Returns a list of v* objects
    @classmethod
    def from_ical(cls, ical: vRecur | str) -> Self: ...

class vTime(TimeBase):
    """Time

    Value Name:
        TIME

    Purpose:
        This value type is used to identify values that contain a
        time of day.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            time         = time-hour time-minute time-second [time-utc]

            time-hour    = 2DIGIT        ;00-23
            time-minute  = 2DIGIT        ;00-59
            time-second  = 2DIGIT        ;00-60
            ;The "60" value is used to account for positive "leap" seconds.

            time-utc     = "Z"

    Description:
        If the property permits, multiple "time" values are
        specified by a COMMA-separated list of values.  No additional
        content value encoding (i.e., BACKSLASH character encoding, see
        vText) is defined for this value type.

        The "TIME" value type is used to identify values that contain a
        time of day.  The format is based on the [ISO.8601.2004] complete
        representation, basic format for a time of day.  The text format
        consists of a two-digit, 24-hour of the day (i.e., values 00-23),
        two-digit minute in the hour (i.e., values 00-59), and two-digit
        seconds in the minute (i.e., values 00-60).  The seconds value of
        60 MUST only be used to account for positive "leap" seconds.
        Fractions of a second are not supported by this format.

        In parallel to the "DATE-TIME" definition above, the "TIME" value
        type expresses time values in three forms:

        The form of time with UTC offset MUST NOT be used.  For example,
        the following is not valid for a time value:

        .. code-block:: text

            230000-0800        ;Invalid time format

        **FORM #1 LOCAL TIME**

        The local time form is simply a time value that does not contain
        the UTC designator nor does it reference a time zone.  For
        example, 11:00 PM:

        .. code-block:: text

            230000

        Time values of this type are said to be "floating" and are not
        bound to any time zone in particular.  They are used to represent
        the same hour, minute, and second value regardless of which time
        zone is currently being observed.  For example, an event can be
        defined that indicates that an individual will be busy from 11:00
        AM to 1:00 PM every day, no matter which time zone the person is
        in.  In these cases, a local time can be specified.  The recipient
        of an iCalendar object with a property value consisting of a local
        time, without any relative time zone information, SHOULD interpret
        the value as being fixed to whatever time zone the "ATTENDEE" is
        in at any given moment.  This means that two "Attendees", may
        participate in the same event at different UTC times; floating
        time SHOULD only be used where that is reasonable behavior.

        In most cases, a fixed time is desired.  To properly communicate a
        fixed time in a property value, either UTC time or local time with
        time zone reference MUST be specified.

        The use of local time in a TIME value without the "TZID" property
        parameter is to be interpreted as floating time, regardless of the
        existence of "VTIMEZONE" calendar components in the iCalendar
        object.

        **FORM #2: UTC TIME**

        UTC time, or absolute time, is identified by a LATIN CAPITAL
        LETTER Z suffix character, the UTC designator, appended to the
        time value.  For example, the following represents 07:00 AM UTC:

        .. code-block:: text

            070000Z

        The "TZID" property parameter MUST NOT be applied to TIME
        properties whose time values are specified in UTC.

        **FORM #3: LOCAL TIME AND TIME ZONE REFERENCE**

        The local time with reference to time zone information form is
        identified by the use the "TZID" property parameter to reference
        the appropriate time zone definition.

        Example:
            The following represents 8:30 AM in New York in winter,
            five hours behind UTC, in each of the three formats:

        .. code-block:: text

            083000
            133000Z
            TZID=America/New_York:083000
    """

    dt: datetime.time | datetime.datetime
    params: Parameters
    @overload
    def __init__(self, dt: datetime.time | datetime.datetime, /) -> None: ...
    # args are passed to the datetime.time() constructor
    @overload
    def __init__(
        self,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: datetime.tzinfo | None = ...,
        /,
    ) -> None: ...
    def to_ical(self) -> str: ...
    @staticmethod
    def from_ical(ical: ICAL_TYPE) -> datetime.time: ...

class vUri(str):
    """URI

    Value Name:
        URI

    Purpose:
        This value type is used to identify values that contain a
        uniform resource identifier (URI) type of reference to the
        property value.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            uri = scheme ":" hier-part [ "?" query ] [ "#" fragment ]

    Description:
        This value type might be used to reference binary
        information, for values that are large, or otherwise undesirable
        to include directly in the iCalendar object.

        Property values with this value type MUST follow the generic URI
        syntax defined in [RFC3986].

        When a property parameter value is a URI value type, the URI MUST
        be specified as a quoted-string value.

        Example:
            The following is a URI for a network file:

            .. code-block:: text

                http://example.com/my-report.txt

            .. code-block:: pycon

                >>> from icalendar.prop import vUri
                >>> uri = vUri.from_ical('http://example.com/my-report.txt')
                >>> uri
                'http://example.com/my-report.txt'
    """

    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class vGeo:
    """Geographic Position

    Property Name:
        GEO

    Purpose:
        This property specifies information related to the global
        position for the activity specified by a calendar component.

    Value Type:
        FLOAT.  The value MUST be two SEMICOLON-separated FLOAT values.

    Property Parameters:
        IANA and non-standard property parameters can be specified on
        this property.

    Conformance:
        This property can be specified in "VEVENT" or "VTODO"
        calendar components.

    Description:
        This property value specifies latitude and longitude,
        in that order (i.e., "LAT LON" ordering).  The longitude
        represents the location east or west of the prime meridian as a
        positive or negative real number, respectively.  The longitude and
        latitude values MAY be specified up to six decimal places, which
        will allow for accuracy to within one meter of geographical
        position.  Receiving applications MUST accept values of this
        precision and MAY truncate values of greater precision.

        Example:

        .. code-block:: text

            GEO:37.386013;-122.082932

        Parse vGeo:

        .. code-block:: pycon

            >>> from icalendar.prop import vGeo
            >>> geo = vGeo.from_ical('37.386013;-122.082932')
            >>> geo
            (37.386013, -122.082932)

        Add a geo location to an event:

        .. code-block:: pycon

            >>> from icalendar import Event
            >>> event = Event()
            >>> latitude = 37.386013
            >>> longitude = -122.082932
            >>> event.add('GEO', (latitude, longitude))
            >>> event['GEO']
            vGeo((37.386013, -122.082932))
    """

    latitude: float
    longitude: float
    params: Parameters
    def __init__(self, geo: tuple[float | str, float | str], params: SupportsKeysAndGetItem[str, str] = {}) -> None:
        """Create a new vGeo from a tuple of (latitude, longitude).

        Raises:
            ValueError: if geo is not a tuple of (latitude, longitude)
        """

    def to_ical(self) -> str: ...
    @staticmethod
    def from_ical(ical: str) -> tuple[float, float]: ...
    def __eq__(self, other: _vType) -> bool: ...  # type: ignore[override]

class vUTCOffset:
    """UTC Offset

    Value Name:
        UTC-OFFSET

    Purpose:
        This value type is used to identify properties that contain
        an offset from UTC to local time.

    Format Definition:
        This value type is defined by the following notation:

        .. code-block:: text

            utc-offset = time-numzone

            time-numzone = ("+" / "-") time-hour time-minute [time-second]

    Description:
        The PLUS SIGN character MUST be specified for positive
        UTC offsets (i.e., ahead of UTC).  The HYPHEN-MINUS character MUST
        be specified for negative UTC offsets (i.e., behind of UTC).  The
        value of "-0000" and "-000000" are not allowed.  The time-second,
        if present, MUST NOT be 60; if absent, it defaults to zero.

        Example:
            The following UTC offsets are given for standard time for
            New York (five hours behind UTC) and Geneva (one hour ahead of
            UTC):

        .. code-block:: text

            -0500

            +0100

        .. code-block:: pycon

            >>> from icalendar.prop import vUTCOffset
            >>> utc_offset = vUTCOffset.from_ical('-0500')
            >>> utc_offset
            datetime.timedelta(days=-1, seconds=68400)
            >>> utc_offset = vUTCOffset.from_ical('+0100')
            >>> utc_offset
            datetime.timedelta(seconds=3600)
    """

    ignore_exceptions: bool
    td: datetime.timedelta
    params: Parameters
    def __init__(self, td: datetime.timedelta, params: SupportsKeysAndGetItem[str, str] = {}) -> None: ...
    def to_ical(self) -> str: ...
    @classmethod
    def from_ical(cls, ical: Self | ICAL_TYPE) -> datetime.timedelta: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class vInline(str):
    """This is an especially dumb class that just holds raw unparsed text and
    has parameters. Conversion of inline values are handled by the Component
    class, so no further processing is needed.
    """

    params: Parameters
    def __new__(cls, value: ICAL_TYPE, encoding: str = "utf-8", params: SupportsKeysAndGetItem[str, str] = {}) -> Self: ...
    def to_ical(self) -> bytes: ...
    @classmethod
    def from_ical(cls, ical: ICAL_TYPE) -> Self: ...

class TypesFactory(CaselessDict[_PropType]):
    """All Value types defined in RFC 5545 are registered in this factory
    class.

    The value and parameter names don't overlap. So one factory is enough for
    both kinds.
    """

    all_types: tuple[_PropType, ...]
    types_map: CaselessDict[str]
    def for_property(self, name: str) -> _PropType:
        """Returns a the default type for a property or parameter"""
    # value is str | bytes, depending on what the v* class supports
    def to_ical(self, name: str, value: Any) -> bytes:
        """Encodes a named value from a primitive python type to an icalendar
        encoded string.
        """
    # value and return type depend on what the v* class supports
    def from_ical(self, name: str, value: Any) -> Any:
        """Decodes a named property or parameter value from an icalendar
        encoded string to a primitive python type.
        """
