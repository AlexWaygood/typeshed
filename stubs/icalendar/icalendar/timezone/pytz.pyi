"""Use pytz timezones."""

__all__ = ["PYTZ"]

import datetime
from typing import Literal

from dateutil.rrule import rrule

from ..cal import Timezone
from ..prop import vRecur
from .provider import TZProvider

class PYTZ(TZProvider):
    """Provide icalendar with timezones from pytz."""

    @property
    def name(self) -> Literal["pytz"]:
        """str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str

        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to 'utf-8'.
        errors defaults to 'strict'.
        """

    def localize_utc(self, dt: datetime.datetime) -> datetime.datetime:
        """Return the datetime in UTC."""

    def localize(self, dt: datetime.datetime, tz: datetime.tzinfo) -> datetime.datetime:
        """Localize a datetime to a timezone."""

    def knows_timezone_id(self, id: str) -> bool:
        """Whether the timezone is already cached by the implementation."""

    def fix_rrule_until(self, rrule: rrule, ical_rrule: vRecur) -> None:
        """Make sure the until value works for the rrule generated from the ical_rrule."""

    def create_timezone(self, tz: Timezone) -> datetime.tzinfo:  # type: ignore[override]
        """Create a pytz timezone from the given information."""

    def timezone(self, name: str) -> datetime.tzinfo | None:
        """Return a timezone with a name or None if we cannot find it."""

    def uses_pytz(self) -> bool:
        """Whether we use pytz."""

    def uses_zoneinfo(self) -> bool:
        """Whether we use zoneinfo."""
