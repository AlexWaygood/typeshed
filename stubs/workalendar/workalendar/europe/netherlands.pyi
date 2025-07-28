from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Netherlands(WesternCalendar):
    """Netherlands"""

    include_good_friday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_ascension: ClassVar[bool]
    include_whit_sunday: ClassVar[bool]
    include_whit_monday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    include_carnival: Incomplete
    def __init__(self, include_carnival: bool = False) -> None: ...
    def get_king_queen_day(self, year):
        """27 April unless this is a Sunday in which case it is the 26th

        Before 2013 it was called Queensday, falling on
        30 April, unless this is a Sunday in which case it is the 29th.
        """

    def get_carnival_days(self, year):
        """Carnival starts 7 weeks before Easter Sunday and lasts 3 days."""

    def get_variable_days(self, year): ...

FALL_HOLIDAYS_EARLY_REGIONS: Incomplete
SPRING_HOLIDAYS_EARLY_REGIONS: Incomplete
SUMMER_HOLIDAYS_EARLY_REGIONS: Incomplete
SUMMER_HOLIDAYS_LATE_REGIONS: Incomplete

class NetherlandsWithSchoolHolidays(Netherlands):
    """Netherlands with school holidays (2016 to 2025).

    Data source and regulating body:
    https://www.rijksoverheid.nl/onderwerpen/schoolvakanties/overzicht-schoolvakanties-per-schooljaar
    """

    region: Incomplete
    carnival_instead_of_spring: Incomplete

    def __init__(self, region, carnival_instead_of_spring: bool = False, **kwargs) -> None:
        """Set up a calendar incl. school holidays for a specific region

        :param region: either "north", "middle" or "south"
        """

    def get_fall_holidays(self, year):
        """
        Return Fall holidays.

        They start at week 43 or 44 and last for 9 days
        """

    def get_christmas_holidays(self, year):
        """
        Return Christmas holidays

        Christmas holidays run partially in December and partially in January
        (spillover from previous year).
        """

    def get_spring_holidays(self, year):
        """
        Return the Spring holidays

        They start at week 8 or 9 and last for 9 days.
        """

    def get_carnival_holidays(self, year):
        """
        Return Carnival holidays

        Carnival holidays start 7 weeks and 1 day before Easter Sunday
        and last 9 days.
        """

    def get_may_holidays(self, year):
        """
        Return May holidays

        They start at week 18 (or 17) and last for 18 days
        """

    def get_summer_holidays(self, year):
        """
        Return the summer holidays as a list
        """

    def get_variable_days(self, year): ...
