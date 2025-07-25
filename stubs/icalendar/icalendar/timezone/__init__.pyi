"""This package contains all functionality for timezones."""

from ..timezone.tzp import TZP as TZP  # to prevent "tzp" from being defined here
from .tzid import tzid_from_dt as tzid_from_dt, tzid_from_tzinfo as tzid_from_tzinfo, tzids_from_tzinfo as tzids_from_tzinfo

__all__ = ["TZP", "tzp", "use_pytz", "use_zoneinfo", "tzid_from_tzinfo", "tzid_from_dt", "tzids_from_tzinfo"]

tzp: TZP

def use_pytz() -> None:
    """Use pytz as the implementation that looks up and creates timezones."""

def use_zoneinfo() -> None:
    """Use zoneinfo as the implementation that looks up and creates timezones."""
