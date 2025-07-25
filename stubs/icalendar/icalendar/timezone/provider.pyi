"""The interface for timezone implementations."""

__all__ = ["TZProvider"]

import datetime
from abc import ABC, abstractmethod

from dateutil.rrule import rrule

from ..prop import vRecur

class TZProvider(ABC):
    """Interface for timezone implementations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the implementation."""

    @abstractmethod
    def localize_utc(self, dt: datetime.datetime) -> datetime.datetime:
        """Return the datetime in UTC."""

    @abstractmethod
    def localize(self, dt: datetime.datetime, tz: datetime.tzinfo) -> datetime.datetime:
        """Localize a datetime to a timezone."""

    @abstractmethod
    def knows_timezone_id(self, id: str) -> bool:
        """Whether the timezone is already cached by the implementation."""

    @abstractmethod
    def fix_rrule_until(self, rrule: rrule, ical_rrule: vRecur) -> None:
        """Make sure the until value works for the rrule generated from the ical_rrule."""

    @abstractmethod
    def create_timezone(self, name: str, transition_times, transition_info) -> datetime.tzinfo:
        """Create a pytz timezone file given information."""

    @abstractmethod
    def timezone(self, name: str) -> datetime.tzinfo | None:
        """Return a timezone with a name or None if we cannot find it."""

    @abstractmethod
    def uses_pytz(self) -> bool:
        """Whether we use pytz."""

    @abstractmethod
    def uses_zoneinfo(self) -> bool:
        """Whether we use zoneinfo."""
