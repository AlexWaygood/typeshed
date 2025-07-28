"""Compute the times and states of alarms.

This takes different calendar software into account and the RFC 9074 (Alarm Extension).

- RFC 9074 defines an ACKNOWLEDGED property in the VALARM.
- Outlook does not export VALARM information.
- Google Calendar uses the DTSTAMP to acknowledge the alarms.
- Thunderbird snoozes the alarms with a X-MOZ-SNOOZE-TIME attribute in the event.
- Thunderbird acknowledges the alarms with a X-MOZ-LASTACK attribute in the event.
- Etar deletes alarms that are acknowledged.
- Nextcloud's Webinterface does not do anything with the alarms when the time passes.
"""

import datetime
from typing_extensions import TypeAlias

from .cal import Alarm, Event, Todo
from .error import (
    ComponentEndMissing as ComponentEndMissing,
    ComponentStartMissing as ComponentStartMissing,
    IncompleteAlarmInformation as IncompleteAlarmInformation,
    LocalTimezoneMissing as LocalTimezoneMissing,
)

__all__ = ["Alarms", "AlarmTime", "IncompleteAlarmInformation", "ComponentEndMissing", "ComponentStartMissing"]

Parent: TypeAlias = Event | Todo

class AlarmTime:
    """An alarm time with all the information."""

    def __init__(
        self,
        alarm: Alarm,
        trigger: datetime.datetime,
        acknowledged_until: datetime.datetime | None = None,
        snoozed_until: datetime.datetime | None = None,
        parent: Parent | None = None,
    ):
        """Create a new AlarmTime.

        alarm
            the Alarm component

        trigger
            a date or datetime at which to trigger the alarm

        acknowledged_until
            an optional datetime in UTC until when all alarms
            have been acknowledged

        snoozed_until
            an optional datetime in UTC until which all alarms of
            the same parent are snoozed

        parent
            the optional parent component the alarm refers to

        local_tzinfo
            the local timezone that events without tzinfo should have
        """

    @property
    def acknowledged(self) -> datetime.datetime | None:
        """The time in UTC at which this alarm was last acknowledged.

        If the alarm was not acknowledged (dismissed), then this is None.
        """

    @property
    def alarm(self) -> Alarm:
        """The alarm component."""

    @property
    def parent(self) -> Parent | None:
        """This is the component that contains the alarm.

        This is None if you did not use Alarms.set_component().
        """

    def is_active(self) -> bool:
        """Whether this alarm is active (True) or acknowledged (False).

        For example, in some calendar software, this is True until the user looks
        at the alarm message and clicked the dismiss button.

        Alarms can be in local time (without a timezone).
        To calculate if the alarm really happened, we need it to be in a timezone.
        If a timezone is required but not given, we throw an IncompleteAlarmInformation.
        """

    @property
    def trigger(self) -> datetime.date:
        """This is the time to trigger the alarm.

        If the alarm has been snoozed, this can differ from the TRIGGER property.
        """

class Alarms:
    """Compute the times and states of alarms.

    This is an example using RFC 9074.
    One alarm is 30 minutes before the event and acknowledged.
    Another alarm is 15 minutes before the event and still active.

    >>> from icalendar import Event, Alarms
    >>> event = Event.from_ical(
    ... '''BEGIN:VEVENT
    ... CREATED:20210301T151004Z
    ... UID:AC67C078-CED3-4BF5-9726-832C3749F627
    ... DTSTAMP:20210301T151004Z
    ... DTSTART;TZID=America/New_York:20210302T103000
    ... DTEND;TZID=America/New_York:20210302T113000
    ... SUMMARY:Meeting
    ... BEGIN:VALARM
    ... UID:8297C37D-BA2D-4476-91AE-C1EAA364F8E1
    ... TRIGGER:-PT30M
    ... ACKNOWLEDGED:20210302T150004Z
    ... DESCRIPTION:Event reminder
    ... ACTION:DISPLAY
    ... END:VALARM
    ... BEGIN:VALARM
    ... UID:8297C37D-BA2D-4476-91AE-C1EAA364F8E1
    ... TRIGGER:-PT15M
    ... DESCRIPTION:Event reminder
    ... ACTION:DISPLAY
    ... END:VALARM
    ... END:VEVENT
    ... ''')
    >>> alarms = Alarms(event)
    >>> len(alarms.times)   # all alarms including those acknowledged
    2
    >>> len(alarms.active)  # the alarms that are not acknowledged, yet
    1
    >>> alarms.active[0].trigger  # this alarm triggers 15 minutes before 10:30
    datetime.datetime(2021, 3, 2, 10, 15, tzinfo=ZoneInfo(key='America/New_York'))

    RFC 9074 specifies that alarms can also be triggered by proximity.
    This is not implemented yet.
    """

    def __init__(self, component: Alarm | Event | Todo | None = None):
        """Start computing alarm times."""

    def add_component(self, component: Alarm | Parent) -> None:
        """Add a component.

        If this is an alarm, it is added.
        Events and Todos are added as a parent and all
        their alarms are added, too.
        """

    def set_parent(self, parent: Parent) -> None:
        """Set the parent of all the alarms.

        If you would like to collect alarms from a component, use add_component
        """

    def add_alarm(self, alarm: Alarm) -> None:
        """Optional: Add an alarm component."""

    def set_start(self, dt: datetime.date | None) -> None:
        """Set the start of the component.

        If you have only absolute alarms, this is not required.
        If you have alarms relative to the start of a compoment, set the start here.
        """

    def set_end(self, dt: datetime.date | None) -> None:
        """Set the end of the component.

        If you have only absolute alarms, this is not required.
        If you have alarms relative to the end of a compoment, set the end here.
        """

    def acknowledge_until(self, dt: datetime.date | None) -> None:
        """This is the time in UTC when all the alarms of this component were acknowledged.

        Only the last call counts.

        Since RFC 9074 (Alarm Extension) was created later,
        calendar implementations differ in how they acknowledge alarms.
        For example, Thunderbird and Google Calendar store the last time
        an event has been acknowledged because of an alarm.
        All alarms that happen before this time count as acknowledged.
        """

    def snooze_until(self, dt: datetime.date | None) -> None:
        """This is the time in UTC when all the alarms of this component were snoozed.

        Only the last call counts.

        The alarms are supposed to turn up again at dt when they are not acknowledged
        but snoozed.
        """

    def set_local_timezone(self, tzinfo: datetime.tzinfo | str | None) -> None:
        """Set the local timezone.

        Events are sometimes in local time.
        In order to compute the exact time of the alarm, some
        alarms without timezone are considered local.

        Some computations work without setting this, others don't.
        If they need this information, expect a LocalTimezoneMissing exception
        somewhere down the line.
        """

    @property
    def times(self) -> list[AlarmTime]:
        """Compute and return the times of the alarms given.

        If the information for calculation is incomplete, this will raise a
        IncompleteAlarmInformation exception.

        Please make sure to set all the required parameters before calculating.
        If you forget to set the acknowledged times, that is not problem.
        """

    @property
    def active(self) -> list[AlarmTime]:
        """The alarm times that are still active and not acknowledged.

        This considers snoozed alarms.

        Alarms can be in local time (without a timezone).
        To calculate if the alarm really happened, we need it to be in a timezone.
        If a timezone is required but not given, we throw an IncompleteAlarmInformation.
        """
