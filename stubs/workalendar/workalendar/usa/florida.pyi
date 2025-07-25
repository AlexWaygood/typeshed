from _typeshed import Incomplete
from typing import ClassVar

from .core import UnitedStates

class HebrewHolidays:
    hebrew_calendars: Incomplete
    @classmethod
    def get_hebrew_calendar(cls, gregorian_year):
        """
        Build and cache the Hebrew calendar for the given Gregorian Year.
        """

    @classmethod
    def search_hebrew_calendar(cls, gregorian_year, hebrew_month, hebrew_day):
        """
        Search for a specific Hebrew month and day in the Hebrew calendar.
        """

    @classmethod
    def get_rosh_hashanah(cls, year):
        """
        Return the gregorian date of the first day of Rosh Hashanah
        """

    @classmethod
    def get_yom_kippur(cls, year):
        """
        Return the gregorian date of Yom Kippur.
        """

class Florida(UnitedStates):
    """Florida"""

    include_thanksgiving_friday: ClassVar[bool]
    thanksgiving_friday_label: ClassVar[str]
    include_columbus_day: ClassVar[bool]
    include_federal_presidents_day: ClassVar[bool]

class FloridaLegal(Florida):
    """Florida Legal Holidays"""

    FIXED_HOLIDAYS: Incomplete
    include_fat_tuesday: ClassVar[bool]
    include_lincoln_birthday: ClassVar[bool]
    include_federal_presidents_day: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_confederation_day: ClassVar[bool]
    include_jefferson_davis_birthday: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
    columbus_day_label: ClassVar[str]
    include_election_day_every_year: ClassVar[bool]
    def __init__(self, *args, **kwargs) -> None: ...
    def get_confederate_day(self, year):
        """
        Confederation memorial day is on the April 26th for Florida Legal.
        """

    def get_jefferson_davis_birthday(self, year):
        """
        Jefferson Davis Birthday appears to be a fixed holiday (June 3rd)
        """

class FloridaCircuitCourts(HebrewHolidays, Florida):
    """Florida Circuits Courts"""

    include_federal_presidents_day: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class FloridaMiamiDade(Florida):
    """Miami-Dade, Florida"""

    include_federal_presidents_day: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
