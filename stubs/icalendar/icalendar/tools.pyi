"""Utility functions for icalendar."""

import datetime
from typing import Final
from typing_extensions import TypeGuard, TypeIs, deprecated

from pytz.tzinfo import BaseTzInfo

from .prop import vText

__all__ = ["UIDGenerator", "is_date", "is_datetime", "to_datetime", "is_pytz", "is_pytz_dt", "normalize_pytz"]

class UIDGenerator:
    """Use this only if you're too lazy to create real UUIDs.

    .. deprecated:: 6.2.1

        Use the Python standard library's :func:`uuid.uuid4` instead.
    """

    chars: Final[list[str]]
    @staticmethod
    @deprecated("Use the Python standard library's :func:`uuid.uuid4` instead.")
    def rnd_string(length: int = 16) -> str:
        """Generates a string with random characters of length.

        .. deprecated:: 6.2.1

            Use the Python standard library's :func:`uuid.uuid4` instead.
        """

    @staticmethod
    @deprecated("Use the Python standard library's :func:`uuid.uuid5` instead.")
    def uid(host_name: str = "example.com", unique: str = "") -> vText:
        """Generates a unique ID consisting of ``datetime-uniquevalue@host``.

        For example:

            .. code-block:: text

                20050105T225746Z-HKtJMqUgdO0jDUwm@example.com

        .. deprecated:: 6.2.1

            Use the Python standard library's :func:`uuid.uuid5` instead.
        """

def is_date(dt: datetime.date) -> bool:  # and not datetime.date
    """Whether this is a date and not a datetime."""

def is_datetime(dt: datetime.date) -> TypeIs[datetime.datetime]:
    """Whether this is a date and not a datetime."""

def to_datetime(dt: datetime.date) -> datetime.datetime:
    """Make sure we have a datetime, not a date."""

def is_pytz(tz: datetime.tzinfo) -> TypeIs[BaseTzInfo]:
    """Whether the timezone requires localize() and normalize()."""

def is_pytz_dt(dt: datetime.date) -> TypeGuard[datetime.datetime]:  # and dt.tzinfo is BaseTZInfo
    """Whether the time requires localize() and normalize()."""

def normalize_pytz(dt: datetime.date) -> datetime.datetime:
    """We have to normalize the time after a calculation if we use pytz.

    pytz requires this function to be used in order to correctly calculate the
    timezone's offset after calculations.
    """
