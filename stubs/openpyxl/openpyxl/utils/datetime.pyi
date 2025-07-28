"""Manage Excel date weirdness."""

from datetime import datetime
from re import Pattern
from typing import Final

MAC_EPOCH: Final[datetime]
WINDOWS_EPOCH: Final[datetime]
# The following two constants are defined twice in the implementation.
CALENDAR_WINDOWS_1900 = WINDOWS_EPOCH
CALENDAR_MAC_1904 = MAC_EPOCH
SECS_PER_DAY: Final = 86400
ISO_FORMAT: Final = "%Y-%m-%dT%H:%M:%SZ"
ISO_REGEX: Final[Pattern[str]]
ISO_DURATION: Final[Pattern[str]]

def to_ISO8601(dt):
    """Convert from a datetime to a timestamp string."""

def from_ISO8601(formatted_string):
    """Convert from a timestamp string to a datetime object. According to
    18.17.4 in the specification the following ISO 8601 formats are
    supported.

    Dates B.1.1 and B.2.1
    Times B.1.2 and B.2.2
    Datetimes B.1.3 and B.2.3

    There is no concept of timedeltas in the specification, but Excel
    writes them (in strict OOXML mode), so these are also understood.
    """

def to_excel(dt, epoch=...):
    """Convert Python datetime to Excel serial"""

def from_excel(value, epoch=..., timedelta: bool = False):
    """Convert Excel serial to Python datetime"""

def time_to_days(value):
    """Convert a time value to fractions of day"""

def timedelta_to_days(value):
    """Convert a timedelta value to fractions of a day"""

def days_to_time(value): ...
