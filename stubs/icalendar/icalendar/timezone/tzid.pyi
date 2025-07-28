"""This module identifies timezones.

Normally, timezones have ids.
This is a way to access the ids if you have a
datetime.tzinfo object.
"""

import datetime

__all__ = ["tzid_from_tzinfo", "tzid_from_dt", "tzids_from_tzinfo"]

def tzids_from_tzinfo(tzinfo: datetime.tzinfo | None) -> tuple[str, ...]:
    """Get several timezone ids if we can identify the timezone.

    >>> import zoneinfo
    >>> from icalendar.timezone.tzid import tzids_from_tzinfo
    >>> tzids_from_tzinfo(zoneinfo.ZoneInfo("Arctic/Longyearbyen"))
    ('Arctic/Longyearbyen', 'Atlantic/Jan_Mayen', 'Europe/Berlin', 'Europe/Budapest', 'Europe/Copenhagen', 'Europe/Oslo', 'Europe/Stockholm', 'Europe/Vienna')
    >>> from dateutil.tz import gettz
    >>> tzids_from_tzinfo(gettz("Europe/Berlin"))
    ('Europe/Berlin', 'Arctic/Longyearbyen', 'Atlantic/Jan_Mayen', 'Europe/Budapest', 'Europe/Copenhagen', 'Europe/Oslo', 'Europe/Stockholm', 'Europe/Vienna')

    """

def tzid_from_tzinfo(tzinfo: datetime.tzinfo | None) -> str | None:
    """Retrieve the timezone id from the tzinfo object.

    Some timezones are equivalent.
    Thus, we might return one ID that is equivelant to others.
    """

def tzid_from_dt(dt: datetime.datetime) -> str | None:
    """Retrieve the timezone id from the datetime object."""
