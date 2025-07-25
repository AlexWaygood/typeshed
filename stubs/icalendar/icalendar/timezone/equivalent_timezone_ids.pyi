"""This module helps identifying the timezone ids and where they differ.

The algorithm: We use the tzname and the utcoffset for each hour from
1970 - 2030.
We make a big map.
If they are equivalent, they are equivalent within the time that is mostly used.

You can regenerate the information from this module.

See also:
- https://stackoverflow.com/questions/79185519/which-timezones-are-equivalent

Run this module:

    python -m icalendar.timezone.equivalent_timezone_ids

"""

import datetime
from collections.abc import Callable
from typing import Final

__all__ = ["main"]

START: Final[datetime.datetime]
END: Final[datetime.datetime]
DISTANCE_FROM_TIMEZONE_CHANGE: Final[datetime.timedelta]

DTS: Final[list[datetime.datetime]]

def main(create_timezones: list[Callable[[str], datetime.tzinfo]], name: str) -> None:
    """Generate a lookup table for timezone information if unknown timezones.

    We cannot create one lookup for all because they seem to be all equivalent
    if we mix timezone implementations.
    """
