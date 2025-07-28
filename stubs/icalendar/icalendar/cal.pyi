"""Calendar is a dictionary like Python object that can render itself as VCAL
files according to RFC 5545.

These are the defined components.
"""

import datetime
from _typeshed import Incomplete, SupportsItems
from collections.abc import Callable
from typing import Any, ClassVar, Final, Literal, NamedTuple, overload
from typing_extensions import Self

from .alarms import Alarms
from .caselessdict import CaselessDict
from .error import IncompleteComponent as IncompleteComponent
from .parser import Contentline, Contentlines
from .prop import TypesFactory, vRecur
from .timezone.tzp import TZP

__all__ = [
    "Alarm",
    "Calendar",
    "Component",
    "ComponentFactory",
    "Event",
    "FreeBusy",
    "INLINE",
    "Journal",
    "Timezone",
    "TimezoneDaylight",
    "TimezoneStandard",
    "Todo",
    "component_factory",
    "get_example",
    "IncompleteComponent",
]

def get_example(component_directory: str, example_name: str) -> bytes:
    """Return an example and raise an error if it is absent."""

class ComponentFactory(CaselessDict[Incomplete]):
    """All components defined in RFC 5545 are registered in this factory class.
    To get a component you can use it like this.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Set keys to upper for initial dict."""

INLINE: CaselessDict[int]

class Component(CaselessDict[Incomplete]):
    """Component is the base object for calendar, Event and the other
    components defined in RFC 5545. Normally you will not use this class
    directly, but rather one of the subclasses.
    """

    name: ClassVar[str | None]
    required: ClassVar[tuple[str, ...]]
    singletons: ClassVar[tuple[str, ...]]
    multiple: ClassVar[tuple[str, ...]]
    exclusive: ClassVar[tuple[str, ...]]
    inclusive: ClassVar[tuple[tuple[str, ...], ...]]
    ignore_exceptions: ClassVar[bool]
    subcomponents: list[Incomplete]
    errors: list[str]

    def __init__(self, *args, **kwargs) -> None:
        """Set keys to upper for initial dict."""

    def __bool__(self) -> bool:
        """Returns True, CaselessDict would return False if it had no items."""
    __nonzero__ = __bool__
    def is_empty(self) -> bool:
        """Returns True if Component has no items or subcomponents, else False."""

    @overload
    def add(self, name: str, value: Any, *, encode: Literal[False]) -> None:
        """Add a property.

        :param name: Name of the property.
        :type name: string

        :param value: Value of the property. Either of a basic Python type of
                      any of the icalendar's own property types.
        :type value: Python native type or icalendar property type.

        :param parameters: Property parameter dictionary for the value. Only
                           available, if encode is set to True.
        :type parameters: Dictionary

        :param encode: True, if the value should be encoded to one of
                       icalendar's own property types (Fallback is "vText")
                       or False, if not.
        :type encode: Boolean

        :returns: None
        """

    @overload
    def add(self, name: str, value: Any, parameters: None, encode: Literal[False]) -> None: ...
    @overload
    def add(
        self, name: str, value: Any, parameters: SupportsItems[str, str | None] | None = None, encode: Literal[True] = True
    ) -> None: ...
    def decoded(self, name, default=[]):
        """Returns decoded value of property."""

    def get_inline(self, name, decode: bool = True):
        """Returns a list of values (split on comma)."""

    def set_inline(self, name, values, encode: bool = True) -> None:
        """Converts a list of values into comma separated string and sets value
        to that.
        """

    def add_component(self, component: Component) -> None:
        """Add a subcomponent to this component."""

    def walk(self, name: str | None = None, select: Callable[[Component], bool] = ...) -> list[Component]:
        """Recursively traverses component and subcomponents. Returns sequence
        of same. If name is passed, only components with name will be returned.

        :param name: The name of the component or None such as ``VEVENT``.
        :param select: A function that takes the component as first argument
          and returns True/False.
        :returns: A list of components that match.
        :rtype: list[Component]
        """

    def property_items(self, recursive: bool = True, sorted: bool = True) -> list[tuple[str, object]]:
        """Returns properties in this component and subcomponents as:
        [(name, value), ...]
        """

    @overload
    @classmethod
    def from_ical(cls, st: str, multiple: Literal[False] = False) -> Component:  # or any of its subclasses
        """Populates the component recursively from a string."""

    @overload
    @classmethod
    def from_ical(cls, st: str, multiple: Literal[True]) -> list[Component]: ...  # or any of its subclasses
    def content_line(self, name: str, value, sorted: bool = True) -> Contentline:
        """Returns property as content line."""

    def content_lines(self, sorted: bool = True) -> Contentlines:
        """Converts the Component and subcomponents into content lines."""

    def to_ical(self, sorted: bool = True) -> bytes:
        """
        :param sorted: Whether parameters and properties should be
                       lexicographically sorted.
        """

    def __eq__(self, other: Component) -> bool: ...  # type: ignore[override]
    @property
    def DTSTAMP(self) -> datetime.datetime | None:
        """The DTSTAMP property. datetime in UTC

        All values will be converted to a datetime in UTC.
        RFC 5545:

            Conformance:  This property MUST be included in the "VEVENT",
            "VTODO", "VJOURNAL", or "VFREEBUSY" calendar components.

            Description: In the case of an iCalendar object that specifies a
            "METHOD" property, this property specifies the date and time that
            the instance of the iCalendar object was created.  In the case of
            an iCalendar object that doesn't specify a "METHOD" property, this
            property specifies the date and time that the information
            associated with the calendar component was last revised in the
            calendar store.

            The value MUST be specified in the UTC time format.

            In the case of an iCalendar object that doesn't specify a "METHOD"
            property, this property is equivalent to the "LAST-MODIFIED"
            property.
        """

    @DTSTAMP.setter
    def DTSTAMP(self, value: datetime.datetime) -> None: ...
    @DTSTAMP.deleter
    def DTSTAMP(self) -> None: ...
    @property
    def LAST_MODIFIED(self) -> datetime.datetime | None:
        """The LAST-MODIFIED property. datetime in UTC

        All values will be converted to a datetime in UTC.
        RFC 5545:

            Purpose:  This property specifies the date and time that the
            information associated with the calendar component was last
            revised in the calendar store.

            Note: This is analogous to the modification date and time for a
            file in the file system.

            Conformance:  This property can be specified in the "VEVENT",
            "VTODO", "VJOURNAL", or "VTIMEZONE" calendar components.
        """

    @LAST_MODIFIED.setter
    def LAST_MODIFIED(self, value: datetime.datetime) -> None: ...
    @LAST_MODIFIED.deleter
    def LAST_MODIFIED(self) -> None: ...
    def is_thunderbird(self) -> bool:
        """Whether this component has attributes that indicate that Mozilla Thunderbird created it."""

# type_def is a TypeForm
def create_single_property(
    prop: str, value_attr: str | None, value_type: tuple[type, ...], type_def: Any, doc: str, vProp: type[Incomplete] = ...
) -> property:
    """Create a single property getter and setter.

    :param prop: The name of the property.
    :param value_attr: The name of the attribute to get the value from.
    :param value_type: The type of the value.
    :param type_def: The type of the property.
    :param doc: The docstring of the property.
    :param vProp: The type of the property from :mod:`icalendar.prop`.
    """

class Event(Component):
    """
    A "VEVENT" calendar component is a grouping of component
    properties that represents a scheduled amount of time on a
    calendar. For example, it can be an activity, such as a one-hour
    long department meeting from 8:00 AM to 9:00 AM, tomorrow.
    """

    name: ClassVar[Literal["VEVENT"]]
    @property
    def alarms(self) -> Alarms:
        """Compute the alarm times for this component.

        >>> from icalendar import Event
        >>> event = Event.example("rfc_9074_example_1")
        >>> len(event.alarms.times)
        1
        >>> alarm_time = event.alarms.times[0]
        >>> alarm_time.trigger  # The time when the alarm pops up
        datetime.datetime(2021, 3, 2, 10, 15, tzinfo=ZoneInfo(key='America/New_York'))
        >>> alarm_time.is_active()  # This alarm has not been acknowledged
        True

        Note that this only uses DTSTART and DTEND, but ignores
        RDATE, EXDATE, and RRULE properties.
        """

    @classmethod
    def example(cls, name: str = "rfc_9074_example_3") -> Event:
        """Return the calendar example with the given name."""

    @property
    def DTSTART(self) -> datetime.date | datetime.datetime | None:
        """The DTSTART property.

        The "DTSTART" property for a "VEVENT" specifies the inclusive start of the event.

        Accepted values: datetime, date.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTSTART.setter
    def DTSTART(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @DTSTART.deleter
    def DTSTART(self) -> None: ...
    @property
    def DTEND(self) -> datetime.date | datetime.datetime | None:
        """The DTEND property.

        The "DTEND" property for a "VEVENT" calendar component specifies the non-inclusive end of the event.

        Accepted values: datetime, date.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTEND.setter
    def DTEND(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @DTEND.deleter
    def DTEND(self) -> None: ...
    @property
    def DURATION(self) -> datetime.timedelta | None:
        """The DURATION property.

        The "DTSTART" property for a "VEVENT" specifies the inclusive start of the event.
        The "DURATION" property in conjunction with the DTSTART property
        for a "VEVENT" calendar component specifies the non-inclusive end
        of the event.

        If you would like to calculate the duration of a VEVENT, do not use this.
        Instead use the duration property (lower case).
        """

    @DURATION.setter
    def DURATION(self, value: datetime.timedelta | None) -> None: ...
    @DURATION.deleter
    def DURATION(self) -> None: ...
    @property
    def duration(self) -> datetime.timedelta:
        """The duration of the VEVENT.

        This duration is calculated from the start and end of the event.
        You cannot set the duration as it is unclear what happens to start and end.
        """

    @property
    def start(self) -> datetime.date | datetime.datetime:
        """The start of the component.

        Invalid values raise an InvalidCalendar.
        If there is no start, we also raise an IncompleteComponent error.

        You can get the start, end and duration of an event as follows:

        >>> from datetime import datetime
        >>> from icalendar import Event
        >>> event = Event()
        >>> event.start = datetime(2021, 1, 1, 12)
        >>> event.end = datetime(2021, 1, 1, 12, 30) # 30 minutes
        >>> event.duration  # 1800 seconds == 30 minutes
        datetime.timedelta(seconds=1800)
        >>> print(event.to_ical())
        BEGIN:VEVENT
        DTSTART:20210101T120000
        DTEND:20210101T123000
        END:VEVENT
        """

    @start.setter
    def start(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @property
    def end(self) -> datetime.date | datetime.datetime:
        """The end of the component.

        Invalid values raise an InvalidCalendar error.
        If there is no end, we also raise an IncompleteComponent error.
        """

    @end.setter
    def end(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @property
    def X_MOZ_SNOOZE_TIME(self) -> datetime.datetime | None:
        """The X-MOZ-SNOOZE-TIME property. datetime in UTC

        All values will be converted to a datetime in UTC.
        Thunderbird: Alarms before this time are snoozed.
        """

    @X_MOZ_SNOOZE_TIME.setter
    def X_MOZ_SNOOZE_TIME(self, value: datetime.datetime) -> None: ...
    @X_MOZ_SNOOZE_TIME.deleter
    def X_MOZ_SNOOZE_TIME(self) -> None: ...
    @property
    def X_MOZ_LASTACK(self) -> datetime.datetime | None:
        """The X-MOZ-LASTACK property. datetime in UTC

        All values will be converted to a datetime in UTC.
        Thunderbird: Alarms before this time are acknowledged.
        """

    @X_MOZ_LASTACK.setter
    def X_MOZ_LASTACK(self, value: datetime.datetime) -> None: ...
    @X_MOZ_LASTACK.deleter
    def X_MOZ_LASTACK(self) -> None: ...
    @property
    def color(self) -> str:
        """This property specifies a color used for displaying the component.

        This implements :rfc:`7986` ``COLOR`` property.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified once in an iCalendar
            object or in ``VEVENT``, ``VTODO``, or ``VJOURNAL`` calendar components.

        Description:
            This property specifies a color that clients MAY use
            when presenting the relevant data to a user.  Typically, this
            would appear as the "background" color of events or tasks.  The
            value is a case-insensitive color name taken from the CSS3 set of
            names, defined in Section 4.3 of `W3C.REC-css3-color-20110607 <https://www.w3.org/TR/css-color-3/>`_.

        Example:
            ``"turquoise"``, ``"#ffffff"``

            .. code-block:: pycon

                >>> from icalendar import Todo
                >>> todo = Todo()
                >>> todo.color = "green"
                >>> print(todo.to_ical())
                BEGIN:VTODO
                COLOR:green
                END:VTODO
        """

    @color.setter
    def color(self, value: str) -> None: ...
    @color.deleter
    def color(self) -> None: ...
    @property
    def sequence(self) -> int:
        """This property defines the revision sequence number of the calendar component within a sequence of revisions.

        Value Type:
            INTEGER

        Property Parameters:
            IANA and non-standard property parameters can be specified on this property.

        Conformance:
            The property can be specified in "VEVENT", "VTODO", or
            "VJOURNAL" calendar component.

        Description:
            When a calendar component is created, its sequence
            number is 0.  It is monotonically incremented by the "Organizer's"
            CUA each time the "Organizer" makes a significant revision to the
            calendar component.

            The "Organizer" includes this property in an iCalendar object that
            it sends to an "Attendee" to specify the current version of the
            calendar component.

            The "Attendee" includes this property in an iCalendar object that
            it sends to the "Organizer" to specify the version of the calendar
            component to which the "Attendee" is referring.

            A change to the sequence number is not the mechanism that an
            "Organizer" uses to request a response from the "Attendees".  The
            "RSVP" parameter on the "ATTENDEE" property is used by the
            "Organizer" to indicate that a response from the "Attendees" is
            requested.

            Recurrence instances of a recurring component MAY have different
            sequence numbers.

        Examples:
            The following is an example of this property for a calendar
            component that was just created by the "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.sequence
                0

            The following is an example of this property for a calendar
            component that has been revised 10 different times by the
            "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar.example("issue_156_RDATE_with_PERIOD_TZID_khal")
                >>> event = calendar.events[0]
                >>> event.sequence
                10
        """

    @sequence.setter
    def sequence(self, value: int) -> None: ...
    @sequence.deleter
    def sequence(self) -> None: ...
    @property
    def categories(self) -> list[str]:
        """This property defines the categories for a component.

        Property Parameters:
            IANA, non-standard, and language property parameters can be specified on this
            property.

        Conformance:
            The property can be specified within "VEVENT", "VTODO", or "VJOURNAL" calendar
            components.
            Since :rfc:`7986` it can also be defined on a "VCALENDAR" component.

        Description:
            This property is used to specify categories or subtypes
            of the calendar component.  The categories are useful in searching
            for a calendar component of a particular type and category.
            Within the "VEVENT", "VTODO", or "VJOURNAL" calendar components,
            more than one category can be specified as a COMMA-separated list
            of categories.

        Example:
            Below, we add the categories to an event:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.categories = ["Work", "Meeting"]
                >>> print(event.to_ical())
                BEGIN:VEVENT
                CATEGORIES:Work,Meeting
                END:VEVENT
                >>> event.categories.append("Lecture")
                >>> event.categories == ["Work", "Meeting", "Lecture"]
                True

        .. note::

           At present, we do not take the LANGUAGE parameter into account.
        """

    @categories.setter
    def categories(self, cats: list[str]) -> None: ...
    @categories.deleter
    def categories(self) -> None: ...
    @property
    def rdates(
        self,
    ) -> list[tuple[datetime.date, None] | tuple[datetime.datetime, None] | tuple[datetime.datetime, datetime.datetime]]:
        """The RDATE property defines the list of DATE-TIME values for recurring components.

        RDATE is defined in :rfc:`5545`.
        The return value is a list of tuples ``(start, end)``.

        ``start`` can be a :class:`datetime.date` or a :class:`datetime.datetime`,
        with and without timezone.

        ``end`` is :obj:`None` if the end is not specified and a :class:`datetime.datetime`
        if the end is specified.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE or PERIOD.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            This property can appear along with the "RRULE"
            property to define an aggregate set of repeating occurrences.
            When they both appear in a recurring component, the recurrence
            instances are defined by the union of occurrences defined by both
            the "RDATE" and "RRULE".

            The recurrence dates, if specified, are used in computing the
            recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

        Example:
            Below, we set one RDATE in a list and get the resulting tuple of start and end.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of recurrence dates
                >>> event.add("RDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.rdates
                [(datetime.datetime(2025, 4, 28, 16, 5), None)]

        .. note::

            You cannot modify the RDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def exdates(self) -> list[datetime.date | datetime.datetime]:
        """EXDATE defines the list of DATE-TIME exceptions for recurring components.

        EXDATE is defined in :rfc:`5545`.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            The exception dates, if specified, are used in
            computing the recurrence set.  The recurrence set is the complete
            set of recurrence instances for a calendar component.  The
            recurrence set is generated by considering the initial "DTSTART"
            property along with the "RRULE", "RDATE", and "EXDATE" properties
            contained within the recurring component.  The "DTSTART" property
            defines the first instance in the recurrence set.  The "DTSTART"
            property value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  When duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "EXDATE" property can be used to exclude the value specified
            in "DTSTART".  However, in such cases, the original "DTSTART" date
            MUST still be maintained by the calendaring and scheduling system
            because the original "DTSTART" value has inherent usage
            dependencies by other properties such as the "RECURRENCE-ID".

        Example:
            Below, we add an exdate in a list and get the resulting list of exdates.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of excluded dates
                >>> event.add("EXDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.exdates
                [datetime.datetime(2025, 4, 28, 16, 5)]

        .. note::

            You cannot modify the EXDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def rrules(self) -> list[vRecur]:
        """RRULE defines a rule or repeating pattern for recurring components.

        RRULE is defined in :rfc:`5545`.
        :rfc:`7529` adds the ``SKIP`` parameter :class:`icalendar.prop.vSkip`.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component, but it SHOULD NOT be specified more than once.
            The recurrence set generated with multiple "RRULE" properties is
            undefined.

        Description:
            The recurrence rule, if specified, is used in computing
            the recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD be synchronized with the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value not synchronized with the recurrence rule is undefined.  The
            final recurrence set is generated by gathering all of the start
            DATE-TIME values generated by any of the specified "RRULE" and
            "RDATE" properties, and then excluding any start DATE-TIME values
            specified by "EXDATE" properties.  This implies that start DATE-
            TIME values specified by "EXDATE" properties take precedence over
            those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "DTSTART" property specified within the iCalendar object
            defines the first instance of the recurrence.  In most cases, a
            "DTSTART" property of DATE-TIME value type used with a recurrence
            rule, should be specified as a date with local time and time zone
            reference to make sure all the recurrence instances start at the
            same local time regardless of time zone changes.

            If the duration of the recurring component is specified with the
            "DTEND" or "DUE" property, then the same exact duration will apply
            to all the members of the generated recurrence set.  Else, if the
            duration of the recurring component is specified with the
            "DURATION" property, then the same nominal duration will apply to
            all the members of the generated recurrence set and the exact
            duration of each recurrence instance will depend on its specific
            start time.  For example, recurrence instances of a nominal
            duration of one day will have an exact duration of more or less
            than 24 hours on a day where a time zone shift occurs.  The
            duration of a specific recurrence may be modified in an exception
            component or simply by using an "RDATE" property of PERIOD value
            type.

        Examples:
            Daily for 10 occurrences:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", "FREQ=DAILY;COUNT=10")
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;COUNT=10
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]

            Daily until December 24, 1997:

            .. code-block:: pycon

                >>> from icalendar import Event, vRecur
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", vRecur({"FREQ": ["DAILY"]}, until=datetime(1997, 12, 24, tzinfo=ZoneInfo("UTC"))))
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;UNTIL=19971224T000000Z
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'UNTIL': [datetime.datetime(1997, 12, 24, 0, 0, tzinfo=ZoneInfo(key='UTC'))]})]

        .. note::

            You cannot modify the RRULE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

class Todo(Component):
    """
    A "VTODO" calendar component is a grouping of component
    properties that represents an action item or assignment. For
    example, it can be used to represent an item of work assigned to
    an individual, such as "Prepare for the upcoming conference
    seminar on Internet Calendaring".
    """

    name: ClassVar[Literal["VTODO"]]
    @property
    def DTSTART(self) -> datetime.datetime | datetime.date | None:
        """The DTSTART property.

        The "DTSTART" property for a "VTODO" specifies the inclusive start of the Todo.

        Accepted values: datetime, date.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTSTART.setter
    def DTSTART(self, value: datetime.datetime | datetime.date | None) -> None: ...
    @DTSTART.deleter
    def DTSTART(self) -> None: ...
    @property
    def DUE(self) -> datetime.datetime | datetime.date | None:
        """The DUE property.

        The "DUE" property for a "VTODO" calendar component specifies the non-inclusive end of the Todo.

        Accepted values: datetime, date.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DUE.setter
    def DUE(self, value: datetime.datetime | datetime.date | None) -> None: ...
    @DUE.deleter
    def DUE(self) -> None: ...
    @property
    def DURATION(self) -> datetime.timedelta | None:
        """The DURATION property.

        The "DTSTART" property for a "VTODO" specifies the inclusive start of the event.
        The "DURATION" property in conjunction with the DTSTART property
        for a "VTODO" calendar component specifies the non-inclusive end
        of the event.

        If you would like to calculate the duration of a VTODO, do not use this.
        Instead use the duration property (lower case).
        """

    @DURATION.setter
    def DURATION(self, value: datetime.timedelta | None) -> None: ...
    @DURATION.deleter
    def DURATION(self) -> None: ...
    @property
    def start(self) -> datetime.datetime | datetime.date:
        """The start of the VTODO.

        Invalid values raise an InvalidCalendar.
        If there is no start, we also raise an IncompleteComponent error.

        You can get the start, end and duration of a Todo as follows:

        >>> from datetime import datetime
        >>> from icalendar import Todo
        >>> todo = Todo()
        >>> todo.start = datetime(2021, 1, 1, 12)
        >>> todo.end = datetime(2021, 1, 1, 12, 30) # 30 minutes
        >>> todo.duration  # 1800 seconds == 30 minutes
        datetime.timedelta(seconds=1800)
        >>> print(todo.to_ical())
        BEGIN:VTODO
        DTSTART:20210101T120000
        DUE:20210101T123000
        END:VTODO
        """

    @start.setter
    def start(self, value: datetime.datetime | datetime.date | None) -> None: ...
    @property
    def end(self) -> datetime.datetime | datetime.date:
        """The end of the component.

        Invalid values raise an InvalidCalendar error.
        If there is no end, we also raise an IncompleteComponent error.
        """

    @end.setter
    def end(self, value: datetime.datetime | datetime.date | None) -> None: ...
    @property
    def duration(self) -> datetime.timedelta:
        """The duration of the VTODO.

        This duration is calculated from the start and end of the Todo.
        You cannot set the duration as it is unclear what happens to start and end.
        """

    @property
    def X_MOZ_SNOOZE_TIME(self) -> datetime.datetime | None:
        """The X-MOZ-SNOOZE-TIME property. datetime in UTC

        All values will be converted to a datetime in UTC.
        Thunderbird: Alarms before this time are snoozed.
        """

    @X_MOZ_SNOOZE_TIME.setter
    def X_MOZ_SNOOZE_TIME(self, value: datetime.datetime) -> None: ...
    @X_MOZ_SNOOZE_TIME.deleter
    def X_MOZ_SNOOZE_TIME(self) -> None: ...
    @property
    def X_MOZ_LASTACK(self) -> datetime.datetime | None:
        """The X-MOZ-LASTACK property. datetime in UTC

        All values will be converted to a datetime in UTC.
        Thunderbird: Alarms before this time are acknowledged.
        """

    @X_MOZ_LASTACK.setter
    def X_MOZ_LASTACK(self, value: datetime.datetime) -> None: ...
    @X_MOZ_LASTACK.deleter
    def X_MOZ_LASTACK(self) -> None: ...
    @property
    def alarms(self) -> Alarms:
        """Compute the alarm times for this component.

        >>> from datetime import datetime
        >>> from icalendar import Todo
        >>> todo = Todo()  # empty without alarms
        >>> todo.start = datetime(2024, 10, 26, 10, 21)
        >>> len(todo.alarms.times)
        0

        Note that this only uses DTSTART and DUE, but ignores
        RDATE, EXDATE, and RRULE properties.
        """

    @property
    def color(self) -> str:
        """This property specifies a color used for displaying the component.

        This implements :rfc:`7986` ``COLOR`` property.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified once in an iCalendar
            object or in ``VEVENT``, ``VTODO``, or ``VJOURNAL`` calendar components.

        Description:
            This property specifies a color that clients MAY use
            when presenting the relevant data to a user.  Typically, this
            would appear as the "background" color of events or tasks.  The
            value is a case-insensitive color name taken from the CSS3 set of
            names, defined in Section 4.3 of `W3C.REC-css3-color-20110607 <https://www.w3.org/TR/css-color-3/>`_.

        Example:
            ``"turquoise"``, ``"#ffffff"``

            .. code-block:: pycon

                >>> from icalendar import Todo
                >>> todo = Todo()
                >>> todo.color = "green"
                >>> print(todo.to_ical())
                BEGIN:VTODO
                COLOR:green
                END:VTODO
        """

    @color.setter
    def color(self, value: str) -> None: ...
    @color.deleter
    def color(self) -> None: ...
    @property
    def sequence(self) -> int:
        """This property defines the revision sequence number of the calendar component within a sequence of revisions.

        Value Type:
            INTEGER

        Property Parameters:
            IANA and non-standard property parameters can be specified on this property.

        Conformance:
            The property can be specified in "VEVENT", "VTODO", or
            "VJOURNAL" calendar component.

        Description:
            When a calendar component is created, its sequence
            number is 0.  It is monotonically incremented by the "Organizer's"
            CUA each time the "Organizer" makes a significant revision to the
            calendar component.

            The "Organizer" includes this property in an iCalendar object that
            it sends to an "Attendee" to specify the current version of the
            calendar component.

            The "Attendee" includes this property in an iCalendar object that
            it sends to the "Organizer" to specify the version of the calendar
            component to which the "Attendee" is referring.

            A change to the sequence number is not the mechanism that an
            "Organizer" uses to request a response from the "Attendees".  The
            "RSVP" parameter on the "ATTENDEE" property is used by the
            "Organizer" to indicate that a response from the "Attendees" is
            requested.

            Recurrence instances of a recurring component MAY have different
            sequence numbers.

        Examples:
            The following is an example of this property for a calendar
            component that was just created by the "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.sequence
                0

            The following is an example of this property for a calendar
            component that has been revised 10 different times by the
            "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar.example("issue_156_RDATE_with_PERIOD_TZID_khal")
                >>> event = calendar.events[0]
                >>> event.sequence
                10
        """

    @sequence.setter
    def sequence(self, value: int) -> None: ...
    @sequence.deleter
    def sequence(self) -> None: ...
    @property
    def categories(self) -> list[str]:
        """This property defines the categories for a component.

        Property Parameters:
            IANA, non-standard, and language property parameters can be specified on this
            property.

        Conformance:
            The property can be specified within "VEVENT", "VTODO", or "VJOURNAL" calendar
            components.
            Since :rfc:`7986` it can also be defined on a "VCALENDAR" component.

        Description:
            This property is used to specify categories or subtypes
            of the calendar component.  The categories are useful in searching
            for a calendar component of a particular type and category.
            Within the "VEVENT", "VTODO", or "VJOURNAL" calendar components,
            more than one category can be specified as a COMMA-separated list
            of categories.

        Example:
            Below, we add the categories to an event:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.categories = ["Work", "Meeting"]
                >>> print(event.to_ical())
                BEGIN:VEVENT
                CATEGORIES:Work,Meeting
                END:VEVENT
                >>> event.categories.append("Lecture")
                >>> event.categories == ["Work", "Meeting", "Lecture"]
                True

        .. note::

           At present, we do not take the LANGUAGE parameter into account.
        """

    @categories.setter
    def categories(self, cats: list[str]) -> None: ...
    @categories.deleter
    def categories(self) -> None: ...
    @property
    def rdates(
        self,
    ) -> list[tuple[datetime.date, None] | tuple[datetime.datetime, None] | tuple[datetime.datetime, datetime.datetime]]:
        """The RDATE property defines the list of DATE-TIME values for recurring components.

        RDATE is defined in :rfc:`5545`.
        The return value is a list of tuples ``(start, end)``.

        ``start`` can be a :class:`datetime.date` or a :class:`datetime.datetime`,
        with and without timezone.

        ``end`` is :obj:`None` if the end is not specified and a :class:`datetime.datetime`
        if the end is specified.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE or PERIOD.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            This property can appear along with the "RRULE"
            property to define an aggregate set of repeating occurrences.
            When they both appear in a recurring component, the recurrence
            instances are defined by the union of occurrences defined by both
            the "RDATE" and "RRULE".

            The recurrence dates, if specified, are used in computing the
            recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

        Example:
            Below, we set one RDATE in a list and get the resulting tuple of start and end.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of recurrence dates
                >>> event.add("RDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.rdates
                [(datetime.datetime(2025, 4, 28, 16, 5), None)]

        .. note::

            You cannot modify the RDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def exdates(self) -> list[datetime.date | datetime.datetime]:
        """EXDATE defines the list of DATE-TIME exceptions for recurring components.

        EXDATE is defined in :rfc:`5545`.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            The exception dates, if specified, are used in
            computing the recurrence set.  The recurrence set is the complete
            set of recurrence instances for a calendar component.  The
            recurrence set is generated by considering the initial "DTSTART"
            property along with the "RRULE", "RDATE", and "EXDATE" properties
            contained within the recurring component.  The "DTSTART" property
            defines the first instance in the recurrence set.  The "DTSTART"
            property value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  When duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "EXDATE" property can be used to exclude the value specified
            in "DTSTART".  However, in such cases, the original "DTSTART" date
            MUST still be maintained by the calendaring and scheduling system
            because the original "DTSTART" value has inherent usage
            dependencies by other properties such as the "RECURRENCE-ID".

        Example:
            Below, we add an exdate in a list and get the resulting list of exdates.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of excluded dates
                >>> event.add("EXDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.exdates
                [datetime.datetime(2025, 4, 28, 16, 5)]

        .. note::

            You cannot modify the EXDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def rrules(self) -> list[vRecur]:
        """RRULE defines a rule or repeating pattern for recurring components.

        RRULE is defined in :rfc:`5545`.
        :rfc:`7529` adds the ``SKIP`` parameter :class:`icalendar.prop.vSkip`.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component, but it SHOULD NOT be specified more than once.
            The recurrence set generated with multiple "RRULE" properties is
            undefined.

        Description:
            The recurrence rule, if specified, is used in computing
            the recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD be synchronized with the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value not synchronized with the recurrence rule is undefined.  The
            final recurrence set is generated by gathering all of the start
            DATE-TIME values generated by any of the specified "RRULE" and
            "RDATE" properties, and then excluding any start DATE-TIME values
            specified by "EXDATE" properties.  This implies that start DATE-
            TIME values specified by "EXDATE" properties take precedence over
            those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "DTSTART" property specified within the iCalendar object
            defines the first instance of the recurrence.  In most cases, a
            "DTSTART" property of DATE-TIME value type used with a recurrence
            rule, should be specified as a date with local time and time zone
            reference to make sure all the recurrence instances start at the
            same local time regardless of time zone changes.

            If the duration of the recurring component is specified with the
            "DTEND" or "DUE" property, then the same exact duration will apply
            to all the members of the generated recurrence set.  Else, if the
            duration of the recurring component is specified with the
            "DURATION" property, then the same nominal duration will apply to
            all the members of the generated recurrence set and the exact
            duration of each recurrence instance will depend on its specific
            start time.  For example, recurrence instances of a nominal
            duration of one day will have an exact duration of more or less
            than 24 hours on a day where a time zone shift occurs.  The
            duration of a specific recurrence may be modified in an exception
            component or simply by using an "RDATE" property of PERIOD value
            type.

        Examples:
            Daily for 10 occurrences:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", "FREQ=DAILY;COUNT=10")
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;COUNT=10
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]

            Daily until December 24, 1997:

            .. code-block:: pycon

                >>> from icalendar import Event, vRecur
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", vRecur({"FREQ": ["DAILY"]}, until=datetime(1997, 12, 24, tzinfo=ZoneInfo("UTC"))))
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;UNTIL=19971224T000000Z
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'UNTIL': [datetime.datetime(1997, 12, 24, 0, 0, tzinfo=ZoneInfo(key='UTC'))]})]

        .. note::

            You cannot modify the RRULE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

class Journal(Component):
    """A descriptive text at a certain time or associated with a component.

    A "VJOURNAL" calendar component is a grouping of
    component properties that represent one or more descriptive text
    notes associated with a particular calendar date.  The "DTSTART"
    property is used to specify the calendar date with which the
    journal entry is associated.  Generally, it will have a DATE value
    data type, but it can also be used to specify a DATE-TIME value
    data type.  Examples of a journal entry include a daily record of
    a legislative body or a journal entry of individual telephone
    contacts for the day or an ordered list of accomplishments for the
    day.
    """

    name: ClassVar[Literal["VJOURNAL"]]
    @property
    def DTSTART(self) -> datetime.date | datetime.datetime | None:
        """The DTSTART property.

        The "DTSTART" property for a "VJOURNAL" that specifies the exact date at which the journal entry was made.

        Accepted values: datetime, date.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTSTART.setter
    def DTSTART(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @DTSTART.deleter
    def DTSTART(self) -> None: ...
    @property
    def start(self) -> datetime.date | datetime.datetime:
        """The start of the Journal.

        The "DTSTART"
        property is used to specify the calendar date with which the
        journal entry is associated.
        """

    @start.setter
    def start(self, value: datetime.date | datetime.datetime | None) -> None: ...
    end = start
    @property
    def duration(self) -> datetime.timedelta:
        """The journal has no duration: timedelta(0)."""

    @property
    def color(self) -> str:
        """This property specifies a color used for displaying the component.

        This implements :rfc:`7986` ``COLOR`` property.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified once in an iCalendar
            object or in ``VEVENT``, ``VTODO``, or ``VJOURNAL`` calendar components.

        Description:
            This property specifies a color that clients MAY use
            when presenting the relevant data to a user.  Typically, this
            would appear as the "background" color of events or tasks.  The
            value is a case-insensitive color name taken from the CSS3 set of
            names, defined in Section 4.3 of `W3C.REC-css3-color-20110607 <https://www.w3.org/TR/css-color-3/>`_.

        Example:
            ``"turquoise"``, ``"#ffffff"``

            .. code-block:: pycon

                >>> from icalendar import Todo
                >>> todo = Todo()
                >>> todo.color = "green"
                >>> print(todo.to_ical())
                BEGIN:VTODO
                COLOR:green
                END:VTODO
        """

    @color.setter
    def color(self, value: str) -> None: ...
    @color.deleter
    def color(self) -> None: ...
    @property
    def sequence(self) -> int:
        """This property defines the revision sequence number of the calendar component within a sequence of revisions.

        Value Type:
            INTEGER

        Property Parameters:
            IANA and non-standard property parameters can be specified on this property.

        Conformance:
            The property can be specified in "VEVENT", "VTODO", or
            "VJOURNAL" calendar component.

        Description:
            When a calendar component is created, its sequence
            number is 0.  It is monotonically incremented by the "Organizer's"
            CUA each time the "Organizer" makes a significant revision to the
            calendar component.

            The "Organizer" includes this property in an iCalendar object that
            it sends to an "Attendee" to specify the current version of the
            calendar component.

            The "Attendee" includes this property in an iCalendar object that
            it sends to the "Organizer" to specify the version of the calendar
            component to which the "Attendee" is referring.

            A change to the sequence number is not the mechanism that an
            "Organizer" uses to request a response from the "Attendees".  The
            "RSVP" parameter on the "ATTENDEE" property is used by the
            "Organizer" to indicate that a response from the "Attendees" is
            requested.

            Recurrence instances of a recurring component MAY have different
            sequence numbers.

        Examples:
            The following is an example of this property for a calendar
            component that was just created by the "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.sequence
                0

            The following is an example of this property for a calendar
            component that has been revised 10 different times by the
            "Organizer":

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar.example("issue_156_RDATE_with_PERIOD_TZID_khal")
                >>> event = calendar.events[0]
                >>> event.sequence
                10
        """

    @sequence.setter
    def sequence(self, value: int) -> None: ...
    @sequence.deleter
    def sequence(self) -> None: ...
    @property
    def categories(self) -> list[str]:
        """This property defines the categories for a component.

        Property Parameters:
            IANA, non-standard, and language property parameters can be specified on this
            property.

        Conformance:
            The property can be specified within "VEVENT", "VTODO", or "VJOURNAL" calendar
            components.
            Since :rfc:`7986` it can also be defined on a "VCALENDAR" component.

        Description:
            This property is used to specify categories or subtypes
            of the calendar component.  The categories are useful in searching
            for a calendar component of a particular type and category.
            Within the "VEVENT", "VTODO", or "VJOURNAL" calendar components,
            more than one category can be specified as a COMMA-separated list
            of categories.

        Example:
            Below, we add the categories to an event:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.categories = ["Work", "Meeting"]
                >>> print(event.to_ical())
                BEGIN:VEVENT
                CATEGORIES:Work,Meeting
                END:VEVENT
                >>> event.categories.append("Lecture")
                >>> event.categories == ["Work", "Meeting", "Lecture"]
                True

        .. note::

           At present, we do not take the LANGUAGE parameter into account.
        """

    @categories.setter
    def categories(self, cats: list[str]) -> None: ...
    @categories.deleter
    def categories(self) -> None: ...
    @property
    def rdates(
        self,
    ) -> list[tuple[datetime.date, None] | tuple[datetime.datetime, None] | tuple[datetime.datetime, datetime.datetime]]:
        """The RDATE property defines the list of DATE-TIME values for recurring components.

        RDATE is defined in :rfc:`5545`.
        The return value is a list of tuples ``(start, end)``.

        ``start`` can be a :class:`datetime.date` or a :class:`datetime.datetime`,
        with and without timezone.

        ``end`` is :obj:`None` if the end is not specified and a :class:`datetime.datetime`
        if the end is specified.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE or PERIOD.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            This property can appear along with the "RRULE"
            property to define an aggregate set of repeating occurrences.
            When they both appear in a recurring component, the recurrence
            instances are defined by the union of occurrences defined by both
            the "RDATE" and "RRULE".

            The recurrence dates, if specified, are used in computing the
            recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

        Example:
            Below, we set one RDATE in a list and get the resulting tuple of start and end.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of recurrence dates
                >>> event.add("RDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.rdates
                [(datetime.datetime(2025, 4, 28, 16, 5), None)]

        .. note::

            You cannot modify the RDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def exdates(self) -> list[datetime.date | datetime.datetime]:
        """EXDATE defines the list of DATE-TIME exceptions for recurring components.

        EXDATE is defined in :rfc:`5545`.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            The exception dates, if specified, are used in
            computing the recurrence set.  The recurrence set is the complete
            set of recurrence instances for a calendar component.  The
            recurrence set is generated by considering the initial "DTSTART"
            property along with the "RRULE", "RDATE", and "EXDATE" properties
            contained within the recurring component.  The "DTSTART" property
            defines the first instance in the recurrence set.  The "DTSTART"
            property value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  When duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "EXDATE" property can be used to exclude the value specified
            in "DTSTART".  However, in such cases, the original "DTSTART" date
            MUST still be maintained by the calendaring and scheduling system
            because the original "DTSTART" value has inherent usage
            dependencies by other properties such as the "RECURRENCE-ID".

        Example:
            Below, we add an exdate in a list and get the resulting list of exdates.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of excluded dates
                >>> event.add("EXDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.exdates
                [datetime.datetime(2025, 4, 28, 16, 5)]

        .. note::

            You cannot modify the EXDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def rrules(self) -> list[vRecur]:
        """RRULE defines a rule or repeating pattern for recurring components.

        RRULE is defined in :rfc:`5545`.
        :rfc:`7529` adds the ``SKIP`` parameter :class:`icalendar.prop.vSkip`.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component, but it SHOULD NOT be specified more than once.
            The recurrence set generated with multiple "RRULE" properties is
            undefined.

        Description:
            The recurrence rule, if specified, is used in computing
            the recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD be synchronized with the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value not synchronized with the recurrence rule is undefined.  The
            final recurrence set is generated by gathering all of the start
            DATE-TIME values generated by any of the specified "RRULE" and
            "RDATE" properties, and then excluding any start DATE-TIME values
            specified by "EXDATE" properties.  This implies that start DATE-
            TIME values specified by "EXDATE" properties take precedence over
            those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "DTSTART" property specified within the iCalendar object
            defines the first instance of the recurrence.  In most cases, a
            "DTSTART" property of DATE-TIME value type used with a recurrence
            rule, should be specified as a date with local time and time zone
            reference to make sure all the recurrence instances start at the
            same local time regardless of time zone changes.

            If the duration of the recurring component is specified with the
            "DTEND" or "DUE" property, then the same exact duration will apply
            to all the members of the generated recurrence set.  Else, if the
            duration of the recurring component is specified with the
            "DURATION" property, then the same nominal duration will apply to
            all the members of the generated recurrence set and the exact
            duration of each recurrence instance will depend on its specific
            start time.  For example, recurrence instances of a nominal
            duration of one day will have an exact duration of more or less
            than 24 hours on a day where a time zone shift occurs.  The
            duration of a specific recurrence may be modified in an exception
            component or simply by using an "RDATE" property of PERIOD value
            type.

        Examples:
            Daily for 10 occurrences:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", "FREQ=DAILY;COUNT=10")
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;COUNT=10
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]

            Daily until December 24, 1997:

            .. code-block:: pycon

                >>> from icalendar import Event, vRecur
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", vRecur({"FREQ": ["DAILY"]}, until=datetime(1997, 12, 24, tzinfo=ZoneInfo("UTC"))))
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;UNTIL=19971224T000000Z
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'UNTIL': [datetime.datetime(1997, 12, 24, 0, 0, tzinfo=ZoneInfo(key='UTC'))]})]

        .. note::

            You cannot modify the RRULE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

class FreeBusy(Component):
    """
    A "VFREEBUSY" calendar component is a grouping of component
    properties that represents either a request for free or busy time
    information, a reply to a request for free or busy time
    information, or a published set of busy time information.
    """

    name: ClassVar[Literal["VFREEBUSY"]]
    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

class Timezone(Component):
    """
    A "VTIMEZONE" calendar component is a grouping of component
    properties that defines a time zone. It is used to describe the
    way in which a time zone changes its offset from UTC over time.
    """

    subcomponents: list[TimezoneStandard | TimezoneDaylight]
    name: ClassVar[Literal["VTIMEZONE"]]
    @classmethod
    def example(cls, name: str = "pacific_fiji") -> Calendar:
        """Return the timezone example with the given name."""

    def to_tz(self, tzp: TZP = ..., lookup_tzid: bool = True) -> datetime.tzinfo:
        """convert this VTIMEZONE component to a timezone object

        :param tzp: timezone provider to use
        :param lookup_tzid: whether to use the TZID property to look up existing
                            timezone definitions with tzp.
                            If it is False, a new timezone will be created.
                            If it is True, the existing timezone will be used
                            if it exists, otherwise a new timezone will be created.
        """

    @property
    def tz_name(self) -> str:
        """Return the name of the timezone component.

        Please note that the names of the timezone are different from this name
        and may change with winter/summer time.
        """

    def get_transitions(self) -> tuple[list[datetime.datetime], list[tuple[datetime.timedelta, datetime.timedelta, str]]]:
        """Return a tuple of (transition_times, transition_info)

        - transition_times = [datetime, ...]
        - transition_info = [(TZOFFSETTO, dts_offset, tzname)]

        """

    @classmethod
    def from_tzinfo(
        cls, timezone: datetime.tzinfo, tzid: str | None = None, first_date: datetime.date = ..., last_date: datetime.date = ...
    ) -> Self:
        """Return a VTIMEZONE component from a timezone object.

        This works with pytz and zoneinfo and any other timezone.
        The offsets are calculated from the tzinfo object.

        Parameters:

        :param tzinfo: the timezone object
        :param tzid: the tzid for this timezone. If None, it will be extracted from the tzinfo.
        :param first_date: a datetime that is earlier than anything that happens in the calendar
        :param last_date: a datetime that is later than anything that happens in the calendar
        :raises ValueError: If we have no tzid and cannot extract one.

        .. note::
            This can take some time. Please cache the results.
        """

    @classmethod
    def from_tzid(cls, tzid: str, tzp: TZP = ..., first_date: datetime.date = ..., last_date: datetime.date = ...) -> Self:
        """Create a VTIMEZONE from a tzid like ``"Europe/Berlin"``.

        :param tzid: the id of the timezone
        :param tzp: the timezone provider
        :param first_date: a datetime that is earlier than anything that happens in the calendar
        :param last_date: a datetime that is later than anything that happens in the calendar
        :raises ValueError: If the tzid is unknown.

        >>> from icalendar import Timezone
        >>> tz = Timezone.from_tzid("Europe/Berlin")
        >>> print(tz.to_ical()[:36])
        BEGIN:VTIMEZONE
        TZID:Europe/Berlin

        .. note::
            This can take some time. Please cache the results.
        """

    @property
    def standard(self) -> list[TimezoneStandard]:
        """The STANDARD subcomponents as a list."""

    @property
    def daylight(self) -> list[TimezoneDaylight]:
        """The DAYLIGHT subcomponents as a list.

        These are for the daylight saving time.
        """

class TimezoneStandard(Component):
    """
    The "STANDARD" sub-component of "VTIMEZONE" defines the standard
    time offset from UTC for a time zone. It represents a time zone's
    standard time, typically used during winter months in locations
    that observe Daylight Saving Time.
    """

    name: ClassVar[Literal["STANDARD"]]
    @property
    def DTSTART(self) -> datetime.date | datetime.datetime | None:
        """The DTSTART property.

        The mandatory "DTSTART" property gives the effective onset date
            and local time for the time zone sub-component definition.
            "DTSTART" in this usage MUST be specified as a date with a local
            time value.

        Accepted values: datetime.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTSTART.setter
    def DTSTART(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @DTSTART.deleter
    def DTSTART(self) -> None: ...
    @property
    def TZOFFSETTO(self) -> datetime.timedelta | None:
        """The TZOFFSETTO property.

        The mandatory "TZOFFSETTO" property gives the UTC offset for the
            time zone sub-component (Standard Time or Daylight Saving Time)
            when this observance is in use.


        Accepted values: timedelta.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @TZOFFSETTO.setter
    def TZOFFSETTO(self, value: datetime.timedelta | None) -> None: ...
    @TZOFFSETTO.deleter
    def TZOFFSETTO(self) -> None: ...
    @property
    def TZOFFSETFROM(self) -> datetime.timedelta | None:
        """The TZOFFSETFROM property.

        The mandatory "TZOFFSETFROM" property gives the UTC offset that is
            in use when the onset of this time zone observance begins.
            "TZOFFSETFROM" is combined with "DTSTART" to define the effective
            onset for the time zone sub-component definition.  For example,
            the following represents the time at which the observance of
            Standard Time took effect in Fall 1967 for New York City:

                DTSTART:19671029T020000
                TZOFFSETFROM:-0400


        Accepted values: timedelta.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @TZOFFSETFROM.setter
    def TZOFFSETFROM(self, value: datetime.timedelta | None) -> None: ...
    @TZOFFSETFROM.deleter
    def TZOFFSETFROM(self) -> None: ...
    @property
    def rdates(
        self,
    ) -> list[tuple[datetime.date, None] | tuple[datetime.datetime, None] | tuple[datetime.datetime, datetime.datetime]]:
        """The RDATE property defines the list of DATE-TIME values for recurring components.

        RDATE is defined in :rfc:`5545`.
        The return value is a list of tuples ``(start, end)``.

        ``start`` can be a :class:`datetime.date` or a :class:`datetime.datetime`,
        with and without timezone.

        ``end`` is :obj:`None` if the end is not specified and a :class:`datetime.datetime`
        if the end is specified.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE or PERIOD.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            This property can appear along with the "RRULE"
            property to define an aggregate set of repeating occurrences.
            When they both appear in a recurring component, the recurrence
            instances are defined by the union of occurrences defined by both
            the "RDATE" and "RRULE".

            The recurrence dates, if specified, are used in computing the
            recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

        Example:
            Below, we set one RDATE in a list and get the resulting tuple of start and end.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of recurrence dates
                >>> event.add("RDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.rdates
                [(datetime.datetime(2025, 4, 28, 16, 5), None)]

        .. note::

            You cannot modify the RDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def exdates(self) -> list[datetime.date | datetime.datetime]:
        """EXDATE defines the list of DATE-TIME exceptions for recurring components.

        EXDATE is defined in :rfc:`5545`.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            The exception dates, if specified, are used in
            computing the recurrence set.  The recurrence set is the complete
            set of recurrence instances for a calendar component.  The
            recurrence set is generated by considering the initial "DTSTART"
            property along with the "RRULE", "RDATE", and "EXDATE" properties
            contained within the recurring component.  The "DTSTART" property
            defines the first instance in the recurrence set.  The "DTSTART"
            property value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  When duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "EXDATE" property can be used to exclude the value specified
            in "DTSTART".  However, in such cases, the original "DTSTART" date
            MUST still be maintained by the calendaring and scheduling system
            because the original "DTSTART" value has inherent usage
            dependencies by other properties such as the "RECURRENCE-ID".

        Example:
            Below, we add an exdate in a list and get the resulting list of exdates.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of excluded dates
                >>> event.add("EXDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.exdates
                [datetime.datetime(2025, 4, 28, 16, 5)]

        .. note::

            You cannot modify the EXDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def rrules(self) -> list[vRecur]:
        """RRULE defines a rule or repeating pattern for recurring components.

        RRULE is defined in :rfc:`5545`.
        :rfc:`7529` adds the ``SKIP`` parameter :class:`icalendar.prop.vSkip`.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component, but it SHOULD NOT be specified more than once.
            The recurrence set generated with multiple "RRULE" properties is
            undefined.

        Description:
            The recurrence rule, if specified, is used in computing
            the recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD be synchronized with the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value not synchronized with the recurrence rule is undefined.  The
            final recurrence set is generated by gathering all of the start
            DATE-TIME values generated by any of the specified "RRULE" and
            "RDATE" properties, and then excluding any start DATE-TIME values
            specified by "EXDATE" properties.  This implies that start DATE-
            TIME values specified by "EXDATE" properties take precedence over
            those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "DTSTART" property specified within the iCalendar object
            defines the first instance of the recurrence.  In most cases, a
            "DTSTART" property of DATE-TIME value type used with a recurrence
            rule, should be specified as a date with local time and time zone
            reference to make sure all the recurrence instances start at the
            same local time regardless of time zone changes.

            If the duration of the recurring component is specified with the
            "DTEND" or "DUE" property, then the same exact duration will apply
            to all the members of the generated recurrence set.  Else, if the
            duration of the recurring component is specified with the
            "DURATION" property, then the same nominal duration will apply to
            all the members of the generated recurrence set and the exact
            duration of each recurrence instance will depend on its specific
            start time.  For example, recurrence instances of a nominal
            duration of one day will have an exact duration of more or less
            than 24 hours on a day where a time zone shift occurs.  The
            duration of a specific recurrence may be modified in an exception
            component or simply by using an "RDATE" property of PERIOD value
            type.

        Examples:
            Daily for 10 occurrences:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", "FREQ=DAILY;COUNT=10")
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;COUNT=10
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]

            Daily until December 24, 1997:

            .. code-block:: pycon

                >>> from icalendar import Event, vRecur
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", vRecur({"FREQ": ["DAILY"]}, until=datetime(1997, 12, 24, tzinfo=ZoneInfo("UTC"))))
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;UNTIL=19971224T000000Z
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'UNTIL': [datetime.datetime(1997, 12, 24, 0, 0, tzinfo=ZoneInfo(key='UTC'))]})]

        .. note::

            You cannot modify the RRULE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

class TimezoneDaylight(Component):
    """
    The "DAYLIGHT" sub-component of "VTIMEZONE" defines the daylight
    saving time offset from UTC for a time zone. It represents a time
    zone's daylight saving time, typically used during summer months
    in locations that observe Daylight Saving Time.
    """

    name: ClassVar[Literal["DAYLIGHT"]]
    @property
    def DTSTART(self) -> datetime.date | datetime.datetime | None:
        """The DTSTART property.

        The mandatory "DTSTART" property gives the effective onset date
            and local time for the time zone sub-component definition.
            "DTSTART" in this usage MUST be specified as a date with a local
            time value.

        Accepted values: datetime.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @DTSTART.setter
    def DTSTART(self, value: datetime.date | datetime.datetime | None) -> None: ...
    @DTSTART.deleter
    def DTSTART(self) -> None: ...
    @property
    def TZOFFSETTO(self) -> datetime.timedelta | None:
        """The TZOFFSETTO property.

        The mandatory "TZOFFSETTO" property gives the UTC offset for the
            time zone sub-component (Standard Time or Daylight Saving Time)
            when this observance is in use.


        Accepted values: timedelta.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @TZOFFSETTO.setter
    def TZOFFSETTO(self, value: datetime.timedelta | None) -> None: ...
    @TZOFFSETTO.deleter
    def TZOFFSETTO(self) -> None: ...
    @property
    def TZOFFSETFROM(self) -> datetime.timedelta | None:
        """The TZOFFSETFROM property.

        The mandatory "TZOFFSETFROM" property gives the UTC offset that is
            in use when the onset of this time zone observance begins.
            "TZOFFSETFROM" is combined with "DTSTART" to define the effective
            onset for the time zone sub-component definition.  For example,
            the following represents the time at which the observance of
            Standard Time took effect in Fall 1967 for New York City:

                DTSTART:19671029T020000
                TZOFFSETFROM:-0400


        Accepted values: timedelta.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @TZOFFSETFROM.setter
    def TZOFFSETFROM(self, value: datetime.timedelta | None) -> None: ...
    @TZOFFSETFROM.deleter
    def TZOFFSETFROM(self) -> None: ...
    @property
    def rdates(
        self,
    ) -> list[tuple[datetime.date, None] | tuple[datetime.datetime, None] | tuple[datetime.datetime, datetime.datetime]]:
        """The RDATE property defines the list of DATE-TIME values for recurring components.

        RDATE is defined in :rfc:`5545`.
        The return value is a list of tuples ``(start, end)``.

        ``start`` can be a :class:`datetime.date` or a :class:`datetime.datetime`,
        with and without timezone.

        ``end`` is :obj:`None` if the end is not specified and a :class:`datetime.datetime`
        if the end is specified.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE or PERIOD.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            This property can appear along with the "RRULE"
            property to define an aggregate set of repeating occurrences.
            When they both appear in a recurring component, the recurrence
            instances are defined by the union of occurrences defined by both
            the "RDATE" and "RRULE".

            The recurrence dates, if specified, are used in computing the
            recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

        Example:
            Below, we set one RDATE in a list and get the resulting tuple of start and end.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of recurrence dates
                >>> event.add("RDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.rdates
                [(datetime.datetime(2025, 4, 28, 16, 5), None)]

        .. note::

            You cannot modify the RDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def exdates(self) -> list[datetime.date | datetime.datetime]:
        """EXDATE defines the list of DATE-TIME exceptions for recurring components.

        EXDATE is defined in :rfc:`5545`.

        Value Type:
            The default value type for this property is DATE-TIME.
            The value type can be set to DATE.

        Property Parameters:
            IANA, non-standard, value data type, and time
            zone identifier property parameters can be specified on this
            property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component.

        Description:
            The exception dates, if specified, are used in
            computing the recurrence set.  The recurrence set is the complete
            set of recurrence instances for a calendar component.  The
            recurrence set is generated by considering the initial "DTSTART"
            property along with the "RRULE", "RDATE", and "EXDATE" properties
            contained within the recurring component.  The "DTSTART" property
            defines the first instance in the recurrence set.  The "DTSTART"
            property value SHOULD match the pattern of the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value that doesn't match the pattern of the rule is undefined.
            The final recurrence set is generated by gathering all of the
            start DATE-TIME values generated by any of the specified "RRULE"
            and "RDATE" properties, and then excluding any start DATE-TIME
            values specified by "EXDATE" properties.  This implies that start
            DATE-TIME values specified by "EXDATE" properties take precedence
            over those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  When duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "EXDATE" property can be used to exclude the value specified
            in "DTSTART".  However, in such cases, the original "DTSTART" date
            MUST still be maintained by the calendaring and scheduling system
            because the original "DTSTART" value has inherent usage
            dependencies by other properties such as the "RECURRENCE-ID".

        Example:
            Below, we add an exdate in a list and get the resulting list of exdates.

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> event = Event()

                # Add a list of excluded dates
                >>> event.add("EXDATE", [datetime(2025, 4, 28, 16, 5)])
                >>> event.exdates
                [datetime.datetime(2025, 4, 28, 16, 5)]

        .. note::

            You cannot modify the EXDATE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

    @property
    def rrules(self) -> list[vRecur]:
        """RRULE defines a rule or repeating pattern for recurring components.

        RRULE is defined in :rfc:`5545`.
        :rfc:`7529` adds the ``SKIP`` parameter :class:`icalendar.prop.vSkip`.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified in recurring "VEVENT",
            "VTODO", and "VJOURNAL" calendar components as well as in the
            "STANDARD" and "DAYLIGHT" sub-components of the "VTIMEZONE"
            calendar component, but it SHOULD NOT be specified more than once.
            The recurrence set generated with multiple "RRULE" properties is
            undefined.

        Description:
            The recurrence rule, if specified, is used in computing
            the recurrence set.  The recurrence set is the complete set of
            recurrence instances for a calendar component.  The recurrence set
            is generated by considering the initial "DTSTART" property along
            with the "RRULE", "RDATE", and "EXDATE" properties contained
            within the recurring component.  The "DTSTART" property defines
            the first instance in the recurrence set.  The "DTSTART" property
            value SHOULD be synchronized with the recurrence rule, if
            specified.  The recurrence set generated with a "DTSTART" property
            value not synchronized with the recurrence rule is undefined.  The
            final recurrence set is generated by gathering all of the start
            DATE-TIME values generated by any of the specified "RRULE" and
            "RDATE" properties, and then excluding any start DATE-TIME values
            specified by "EXDATE" properties.  This implies that start DATE-
            TIME values specified by "EXDATE" properties take precedence over
            those specified by inclusion properties (i.e., "RDATE" and
            "RRULE").  Where duplicate instances are generated by the "RRULE"
            and "RDATE" properties, only one recurrence is considered.
            Duplicate instances are ignored.

            The "DTSTART" property specified within the iCalendar object
            defines the first instance of the recurrence.  In most cases, a
            "DTSTART" property of DATE-TIME value type used with a recurrence
            rule, should be specified as a date with local time and time zone
            reference to make sure all the recurrence instances start at the
            same local time regardless of time zone changes.

            If the duration of the recurring component is specified with the
            "DTEND" or "DUE" property, then the same exact duration will apply
            to all the members of the generated recurrence set.  Else, if the
            duration of the recurring component is specified with the
            "DURATION" property, then the same nominal duration will apply to
            all the members of the generated recurrence set and the exact
            duration of each recurrence instance will depend on its specific
            start time.  For example, recurrence instances of a nominal
            duration of one day will have an exact duration of more or less
            than 24 hours on a day where a time zone shift occurs.  The
            duration of a specific recurrence may be modified in an exception
            component or simply by using an "RDATE" property of PERIOD value
            type.

        Examples:
            Daily for 10 occurrences:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", "FREQ=DAILY;COUNT=10")
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;COUNT=10
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'COUNT': [10]})]

            Daily until December 24, 1997:

            .. code-block:: pycon

                >>> from icalendar import Event, vRecur
                >>> from datetime import datetime
                >>> from zoneinfo import ZoneInfo
                >>> event = Event()
                >>> event.start = datetime(1997, 9, 2, 9, 0, tzinfo=ZoneInfo("America/New_York"))
                >>> event.add("RRULE", vRecur({"FREQ": ["DAILY"]}, until=datetime(1997, 12, 24, tzinfo=ZoneInfo("UTC"))))
                >>> print(event.to_ical())
                BEGIN:VEVENT
                DTSTART;TZID=America/New_York:19970902T090000
                RRULE:FREQ=DAILY;UNTIL=19971224T000000Z
                END:VEVENT
                >>> event.rrules
                [vRecur({'FREQ': ['DAILY'], 'UNTIL': [datetime.datetime(1997, 12, 24, 0, 0, tzinfo=ZoneInfo(key='UTC'))]})]

        .. note::

            You cannot modify the RRULE value by modifying the result.
            Use :func:`icalendar.cal.Component.add` to add values.

            If you want to compute recurrences, have a look at :ref:`Related projects`.

        """

class Alarm(Component):
    """
    A "VALARM" calendar component is a grouping of component
    properties that defines an alarm or reminder for an event or a
    to-do. For example, it may be used to define a reminder for a
    pending event or an overdue to-do.
    """

    name: ClassVar[Literal["VALARM"]]
    @property
    def REPEAT(self) -> int:
        """The REPEAT property of an alarm component.

        The alarm can be defined such that it triggers repeatedly.  A
        definition of an alarm with a repeating trigger MUST include both
        the "DURATION" and "REPEAT" properties.  The "DURATION" property
        specifies the delay period, after which the alarm will repeat.
        The "REPEAT" property specifies the number of additional
        repetitions that the alarm will be triggered.  This repetition
        count is in addition to the initial triggering of the alarm.
        """

    @REPEAT.setter
    def REPEAT(self, value: int) -> None: ...
    @REPEAT.deleter
    def REPEAT(self) -> None: ...
    @property
    def DURATION(self) -> datetime.timedelta | None:
        """The DURATION property of an alarm component.

        The alarm can be defined such that it triggers repeatedly.  A
        definition of an alarm with a repeating trigger MUST include both
        the "DURATION" and "REPEAT" properties.  The "DURATION" property
        specifies the delay period, after which the alarm will repeat.
        """

    @DURATION.setter
    def DURATION(self, value: datetime.timedelta | None) -> None: ...
    @DURATION.deleter
    def DURATION(self) -> None: ...
    @property
    def ACKNOWLEDGED(self) -> datetime.datetime | None:
        """The ACKNOWLEDGED property. datetime in UTC

        All values will be converted to a datetime in UTC.
        This is defined in RFC 9074:

        Purpose: This property specifies the UTC date and time at which the
        corresponding alarm was last sent or acknowledged.

        This property is used to specify when an alarm was last sent or acknowledged.
        This allows clients to determine when a pending alarm has been acknowledged
        by a calendar user so that any alerts can be dismissed across multiple devices.
        It also allows clients to track repeating alarms or alarms on recurring events or
        to-dos to ensure that the right number of missed alarms can be tracked.

        Clients SHOULD set this property to the current date-time value in UTC
        when a calendar user acknowledges a pending alarm. Certain kinds of alarms,
        such as email-based alerts, might not provide feedback as to when the calendar user
        sees them. For those kinds of alarms, the client SHOULD set this property
        when the alarm is triggered and the action is successfully carried out.

        When an alarm is triggered on a client, clients can check to see if an "ACKNOWLEDGED"
        property is present. If it is, and the value of that property is greater than or
        equal to the computed trigger time for the alarm, then the client SHOULD NOT trigger
        the alarm. Similarly, if an alarm has been triggered and
        an "alert" has been presented to a calendar user, clients can monitor
        the iCalendar data to determine whether an "ACKNOWLEDGED" property is added or
        changed in the alarm component. If the value of any "ACKNOWLEDGED" property
        in the alarm changes and is greater than or equal to the trigger time of the alarm,
        then clients SHOULD dismiss or cancel any "alert" presented to the calendar user.
        """

    @ACKNOWLEDGED.setter
    def ACKNOWLEDGED(self, value: datetime.datetime | None) -> None: ...
    @ACKNOWLEDGED.deleter
    def ACKNOWLEDGED(self) -> None: ...
    @property
    def TRIGGER(self) -> datetime.timedelta | datetime.datetime | None:
        """The TRIGGER property.

        Purpose:  This property specifies when an alarm will trigger.

        Value Type:  The default value type is DURATION.  The value type can
        be set to a DATE-TIME value type, in which case the value MUST
        specify a UTC-formatted DATE-TIME value.

        Either a positive or negative duration may be specified for the
        "TRIGGER" property.  An alarm with a positive duration is
        triggered after the associated start or end of the event or to-do.
        An alarm with a negative duration is triggered before the
        associated start or end of the event or to-do.

        Accepted values: datetime, timedelta.
        If the attribute has invalid values, we raise InvalidCalendar.
        If the value is absent, we return None.
        You can also delete the value with del or by setting it to None.
        """

    @TRIGGER.setter
    def TRIGGER(self, value: datetime.timedelta | datetime.datetime | None) -> None: ...
    @TRIGGER.deleter
    def TRIGGER(self) -> None: ...
    @property
    def TRIGGER_RELATED(self) -> Literal["START", "END"]:
        """The RELATED parameter of the TRIGGER property.

        Values are either "START" (default) or "END".

        A value of START will set the alarm to trigger off the
        start of the associated event or to-do.  A value of END will set
        the alarm to trigger off the end of the associated event or to-do.

        In this example, we create an alarm that triggers two hours after the
        end of its parent component:

        >>> from icalendar import Alarm
        >>> from datetime import timedelta
        >>> alarm = Alarm()
        >>> alarm.TRIGGER = timedelta(hours=2)
        >>> alarm.TRIGGER_RELATED = "END"
        """

    @TRIGGER_RELATED.setter
    def TRIGGER_RELATED(self, value: Literal["START", "END"]) -> None: ...

    class Triggers(NamedTuple):
        """The computed times of alarm triggers.

        start - triggers relative to the start of the Event or Todo (timedelta)

        end - triggers relative to the end of the Event or Todo (timedelta)

        absolute - triggers at a datetime in UTC
        """

        start: tuple[datetime.timedelta, ...]
        end: tuple[datetime.timedelta, ...]
        absolute: tuple[datetime.datetime, ...]

    @property
    def triggers(self) -> Alarm.Triggers:
        """The computed triggers of an Alarm.

        This takes the TRIGGER, DURATION and REPEAT properties into account.

        Here, we create an alarm that triggers 3 times before the start of the
        parent component:

        >>> from icalendar import Alarm
        >>> from datetime import timedelta
        >>> alarm = Alarm()
        >>> alarm.TRIGGER = timedelta(hours=-4)  # trigger 4 hours before START
        >>> alarm.DURATION = timedelta(hours=1)  # after 1 hour trigger again
        >>> alarm.REPEAT = 2  # trigger 2 more times
        >>> alarm.triggers.start == (timedelta(hours=-4),  timedelta(hours=-3),  timedelta(hours=-2))
        True
        >>> alarm.triggers.end
        ()
        >>> alarm.triggers.absolute
        ()
        """

    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

class Calendar(Component):
    """
    The "VCALENDAR" object is a collection of calendar information.
    This information can include a variety of components, such as
    "VEVENT", "VTODO", "VJOURNAL", "VFREEBUSY", "VTIMEZONE", or any
    other type of calendar component.
    """

    name: ClassVar[Literal["VCALENDAR"]]
    @classmethod
    def example(cls, name: str = "example") -> Calendar:
        """Return the calendar example with the given name."""

    @property
    def freebusy(self) -> list[FreeBusy]:
        """All FreeBusy components in the calendar.

        This is a shortcut to get all FreeBusy.
        Modifications do not change the calendar.
        Use :py:meth:`Component.add_component`.
        """

    @property
    def events(self) -> list[Event]:
        """All event components in the calendar.

        This is a shortcut to get all events.
        Modifications do not change the calendar.
        Use :py:meth:`Component.add_component`.

        >>> from icalendar import Calendar
        >>> calendar = Calendar.example()
        >>> event = calendar.events[0]
        >>> event.start
        datetime.date(2022, 1, 1)
        >>> print(event["SUMMARY"])
        New Year's Day
        """

    @property
    def todos(self) -> list[Todo]:
        """All todo components in the calendar.

        This is a shortcut to get all todos.
        Modifications do not change the calendar.
        Use :py:meth:`Component.add_component`.
        """

    def get_used_tzids(self) -> set[str]:
        """The set of TZIDs in use.

        This goes through the whole calendar to find all occurrences of
        timezone information like the TZID parameter in all attributes.

        >>> from icalendar import Calendar
        >>> calendar = Calendar.example("timezone_rdate")
        >>> calendar.get_used_tzids()
        {'posix/Europe/Vaduz'}

        Even if you use UTC, this will not show up.
        """

    def get_missing_tzids(self) -> set[str]:
        """The set of missing timezone component tzids.

        To create a :rfc:`5545` compatible calendar,
        all of these timezones should be added.
        """

    @property
    def timezones(self) -> list[Timezone]:
        """Return the timezones components in this calendar.

        >>> from icalendar import Calendar
        >>> calendar = Calendar.example("pacific_fiji")
        >>> [timezone.tz_name for timezone in calendar.timezones]
        ['custom_Pacific/Fiji']

        .. note::

            This is a read-only property.
        """

    def add_missing_timezones(self, first_date: datetime.date = ..., last_date: datetime.date = ...) -> None:
        """Add all missing VTIMEZONE components.

        This adds all the timezone components that are required.

        .. note::

            Timezones that are not known will not be added.

        :param first_date: earlier than anything that happens in the calendar
        :param last_date: later than anything happening in the calendar

        >>> from icalendar import Calendar, Event
        >>> from datetime import datetime
        >>> from zoneinfo import ZoneInfo
        >>> calendar = Calendar()
        >>> event = Event()
        >>> calendar.add_component(event)
        >>> event.start = datetime(1990, 10, 11, 12, tzinfo=ZoneInfo("Europe/Berlin"))
        >>> calendar.timezones
        []
        >>> calendar.add_missing_timezones()
        >>> calendar.timezones[0].tz_name
        'Europe/Berlin'
        >>> calendar.get_missing_tzids()  # check that all are added
        set()
        """

    @property
    def calendar_name(self) -> str | None:
        """This property specifies the name of the calendar.

        This implements :rfc:`7986` ``NAME`` and ``X-WR-CALNAME``.

        Property Parameters:
            IANA, non-standard, alternate text
            representation, and language property parameters can be specified
            on this property.

        Conformance:
            This property can be specified multiple times in an
            iCalendar object.  However, each property MUST represent the name
            of the calendar in a different language.

        Description:
            This property is used to specify a name of the
            iCalendar object that can be used by calendar user agents when
            presenting the calendar data to a user.  Whilst a calendar only
            has a single name, multiple language variants can be specified by
            including this property multiple times with different "LANGUAGE"
            parameter values on each.

        Example:
            Below, we set the name of the calendar.

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar()
                >>> calendar.calendar_name = "My Calendar"
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                NAME:My Calendar
                END:VCALENDAR
        """

    @calendar_name.setter
    def calendar_name(self, value: str) -> None: ...
    @calendar_name.deleter
    def calendar_name(self) -> None: ...
    @property
    def description(self) -> str | None:
        """This property specifies the description of the calendar.

        This implements :rfc:`7986` ``DESCRIPTION`` and ``X-WR-CALDESC``.

        Conformance:
            This property can be specified multiple times in an
            iCalendar object.  However, each property MUST represent the
            description of the calendar in a different language.

        Description:
            This property is used to specify a lengthy textual
            description of the iCalendar object that can be used by calendar
            user agents when describing the nature of the calendar data to a
            user.  Whilst a calendar only has a single description, multiple
            language variants can be specified by including this property
            multiple times with different "LANGUAGE" parameter values on each.

        Example:
            Below, we add a description to a calendar.

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar()
                >>> calendar.description = "This is a calendar"
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                DESCRIPTION:This is a calendar
                END:VCALENDAR
        """

    @description.setter
    def description(self, value: str) -> None: ...
    @description.deleter
    def description(self) -> None: ...
    @property
    def color(self) -> str:
        """This property specifies a color used for displaying the calendar.

        This implements :rfc:`7986` ``COLOR`` and ``X-APPLE-CALENDAR-COLOR``.
        Please note that since :rfc:`7986`, subcomponents can have their own color.

        Property Parameters:
            IANA and non-standard property parameters can
            be specified on this property.

        Conformance:
            This property can be specified once in an iCalendar
            object or in ``VEVENT``, ``VTODO``, or ``VJOURNAL`` calendar components.

        Description:
            This property specifies a color that clients MAY use
            when presenting the relevant data to a user.  Typically, this
            would appear as the "background" color of events or tasks.  The
            value is a case-insensitive color name taken from the CSS3 set of
            names, defined in Section 4.3 of `W3C.REC-css3-color-20110607 <https://www.w3.org/TR/css-color-3/>`_.

        Example:
            ``"turquoise"``, ``"#ffffff"``

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> calendar = Calendar()
                >>> calendar.color = "black"
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                COLOR:black
                END:VCALENDAR

        """

    @color.setter
    def color(self, value: str) -> None: ...
    @color.deleter
    def color(self) -> None: ...
    @property
    def categories(self) -> list[str]:
        """This property defines the categories for a component.

        Property Parameters:
            IANA, non-standard, and language property parameters can be specified on this
            property.

        Conformance:
            The property can be specified within "VEVENT", "VTODO", or "VJOURNAL" calendar
            components.
            Since :rfc:`7986` it can also be defined on a "VCALENDAR" component.

        Description:
            This property is used to specify categories or subtypes
            of the calendar component.  The categories are useful in searching
            for a calendar component of a particular type and category.
            Within the "VEVENT", "VTODO", or "VJOURNAL" calendar components,
            more than one category can be specified as a COMMA-separated list
            of categories.

        Example:
            Below, we add the categories to an event:

            .. code-block:: pycon

                >>> from icalendar import Event
                >>> event = Event()
                >>> event.categories = ["Work", "Meeting"]
                >>> print(event.to_ical())
                BEGIN:VEVENT
                CATEGORIES:Work,Meeting
                END:VEVENT
                >>> event.categories.append("Lecture")
                >>> event.categories == ["Work", "Meeting", "Lecture"]
                True

        .. note::

           At present, we do not take the LANGUAGE parameter into account.
        """

    @categories.setter
    def categories(self, cats: list[str]) -> None: ...
    @categories.deleter
    def categories(self) -> None: ...
    @property
    def uid(self) -> str:
        """UID specifies the persistent, globally unique identifier for a component.

        We recommend using :func:`uuid.uuid4` to generate new values.

        Returns:
            The value of the UID property as a string or ``""`` if no value is set.

        Description:
            The "UID" itself MUST be a globally unique identifier.
            The generator of the identifier MUST guarantee that the identifier
            is unique.

            This is the method for correlating scheduling messages with the
            referenced "VEVENT", "VTODO", or "VJOURNAL" calendar component.
            The full range of calendar components specified by a recurrence
            set is referenced by referring to just the "UID" property value
            corresponding to the calendar component.  The "RECURRENCE-ID"
            property allows the reference to an individual instance within the
            recurrence set.

            This property is an important method for group-scheduling
            applications to match requests with later replies, modifications,
            or deletion requests.  Calendaring and scheduling applications
            MUST generate this property in "VEVENT", "VTODO", and "VJOURNAL"
            calendar components to assure interoperability with other group-
            scheduling applications.  This identifier is created by the
            calendar system that generates an iCalendar object.

            Implementations MUST be able to receive and persist values of at
            least 255 octets for this property, but they MUST NOT truncate
            values in the middle of a UTF-8 multi-octet sequence.

            :rfc:`7986` states that UID can be used, for
            example, to identify duplicate calendar streams that a client may
            have been given access to.  It can be used in conjunction with the
            "LAST-MODIFIED" property also specified on the "VCALENDAR" object
            to identify the most recent version of a calendar.

        Conformance:
            :rfc:`5545` states that the "UID" property can be specified on "VEVENT", "VTODO",
            and "VJOURNAL" calendar components.
            :rfc:`7986` modifies the definition of the "UID" property to
            allow it to be defined in an iCalendar object.
            :rfc:`9074`  adds a "UID" property to "VALARM" components to allow a unique
            identifier to be specified. The value of this property can then be used
            to refer uniquely to the "VALARM" component.

            This property can be specified once only.

        Security:
            :rfc:`7986` states that UID values MUST NOT include any data that
            might identify a user, host, domain, or any other security- or
            privacy-sensitive information.  It is RECOMMENDED that calendar user
            agents now generate "UID" values that are hex-encoded random
            Universally Unique Identifier (UUID) values as defined in
            Sections 4.4 and 4.5 of :rfc:`4122`.
            You can use the :mod:`uuid` module to generate new UUIDs.

        Compatibility:
            For Alarms, ``X-ALARMUID`` is also considered.

        Examples:
            The following is an example of such a property value:
            ``5FC53010-1267-4F8E-BC28-1D7AE55A7C99``.

            Set the UID of a calendar:

            .. code-block:: pycon

                >>> from icalendar import Calendar
                >>> from uuid import uuid4
                >>> calendar = Calendar()
                >>> calendar.uid = uuid4()
                >>> print(calendar.to_ical())
                BEGIN:VCALENDAR
                UID:d755cef5-2311-46ed-a0e1-6733c9e15c63
                END:VCALENDAR

        """

    @uid.setter
    def uid(self, value: str) -> None: ...
    @uid.deleter
    def uid(self) -> None: ...

types_factory: Final[TypesFactory]
component_factory: Final[ComponentFactory]
