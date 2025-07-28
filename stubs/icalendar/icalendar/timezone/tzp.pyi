import datetime
from typing import Final

from dateutil.rrule import rrule

from ..cal import Timezone
from ..prop import vRecur
from .provider import TZProvider

__all__ = ["TZP"]

DEFAULT_TIMEZONE_PROVIDER: Final = "zoneinfo"

class TZP:
    """This is the timezone provider proxy.

    If you would like to have another timezone implementation,
    you can create a new one and pass it to this proxy.
    All of icalendar will then use this timezone implementation.
    """

    def __init__(self, provider: str | TZProvider = "zoneinfo") -> None:
        """Create a new timezone implementation proxy."""

    def use_pytz(self) -> None:
        """Use pytz as the timezone provider."""

    def use_zoneinfo(self) -> None:
        """Use zoneinfo as the timezone provider."""

    def use(self, provider: str | TZProvider) -> None:
        """Switch to a different timezone provider."""

    def use_default(self) -> None:
        """Use the default timezone provider."""

    def localize_utc(self, dt: datetime.date) -> datetime.datetime:
        """Return the datetime in UTC.

        If the datetime has no timezone, set UTC as its timezone.
        """

    def localize(self, dt: datetime.date, tz: datetime.tzinfo | str) -> datetime.datetime:
        """Localize a datetime to a timezone."""

    def cache_timezone_component(self, timezone_component: Timezone) -> None:
        """Cache the timezone that is created from a timezone component
        if it is not already known.

        This can influence the result from timezone(): Once cached, the
        custom timezone is returned from timezone().
        """

    def fix_rrule_until(self, rrule: rrule, ical_rrule: vRecur) -> None:
        """Make sure the until value works."""

    def create_timezone(self, timezone_component: Timezone) -> datetime.tzinfo:
        """Create a timezone from a timezone component.

        This component will not be cached.
        """

    def clean_timezone_id(self, tzid: str) -> str:
        """Return a clean version of the timezone id.

        Timezone ids can be a bit unclean, starting with a / for example.
        Internally, we should use this to identify timezones.
        """

    def timezone(self, tz_id: str) -> datetime.tzinfo | None:
        """Return a timezone with an id or None if we cannot find it."""

    def uses_pytz(self) -> bool:
        """Whether we use pytz at all."""

    def uses_zoneinfo(self) -> bool:
        """Whether we use zoneinfo."""

    @property
    def name(self) -> str:
        """The name of the timezone component used."""
