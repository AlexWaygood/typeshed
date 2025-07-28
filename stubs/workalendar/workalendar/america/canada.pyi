from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Canada(WesternCalendar):
    """Canada"""

    FIXED_HOLIDAYS: Incomplete
    shift_new_years_day: ClassVar[bool]
    def get_variable_days(self, year): ...

class LateFamilyDayMixin:
    """3rd Monday of February"""

    def get_family_day(self, year, label: str = "Family Day"): ...

class VictoriaDayMixin:
    """Monday preceding the 25th of May"""

    def get_victoria_day(self, year): ...

class AugustCivicHolidayMixin:
    """1st Monday of August; different names depending on location"""

    def get_civic_holiday(self, year, label: str = "Civic Holiday"): ...

class ThanksgivingMixin:
    """2nd Monday of October"""

    def get_thanksgiving(self, year): ...

class BoxingDayMixin:
    """26th of December; shift to next working day"""

    def get_boxing_day(self, year): ...

class StJeanBaptisteMixin:
    """24th of June; shift to next working day"""

    def get_st_jean(self, year): ...

class RemembranceDayShiftMixin:
    """11th of November; shift to next day"""

    def get_remembrance_day(self, year): ...

class Ontario(BoxingDayMixin, ThanksgivingMixin, VictoriaDayMixin, LateFamilyDayMixin, AugustCivicHolidayMixin, Canada):
    """Ontario"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class Quebec(VictoriaDayMixin, StJeanBaptisteMixin, ThanksgivingMixin, Canada):
    """Quebec"""

    include_easter_monday: ClassVar[bool]
    def get_variable_days(self, year): ...

class BritishColumbia(VictoriaDayMixin, AugustCivicHolidayMixin, ThanksgivingMixin, Canada):
    """British Columbia"""

    include_good_friday: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def get_family_day(self, year):
        """
        Return Family Day for British Columbia.

        From 2013 to 2018, Family Day was on 2nd MON of February
        As of 2019, Family Day happens on 3rd MON of February
        """

    def get_variable_days(self, year): ...

class Alberta(LateFamilyDayMixin, VictoriaDayMixin, ThanksgivingMixin, Canada):
    """Alberta"""

    include_good_friday: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def get_variable_days(self, year): ...

class Saskatchewan(
    LateFamilyDayMixin, VictoriaDayMixin, RemembranceDayShiftMixin, AugustCivicHolidayMixin, ThanksgivingMixin, Canada
):
    """Saskatchewan"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class Manitoba(LateFamilyDayMixin, VictoriaDayMixin, AugustCivicHolidayMixin, ThanksgivingMixin, Canada):
    """Manitoba"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class NewBrunswick(AugustCivicHolidayMixin, Canada):
    """New Brunswick"""

    FIXED_HOLIDAYS: Incomplete
    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class NovaScotia(RemembranceDayShiftMixin, LateFamilyDayMixin, Canada):
    """Nova Scotia"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class PrinceEdwardIsland(LateFamilyDayMixin, RemembranceDayShiftMixin, Canada):
    """Prince Edward Island"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class Newfoundland(Canada):
    """Newfoundland and Labrador"""

    include_good_friday: ClassVar[bool]

class Yukon(VictoriaDayMixin, ThanksgivingMixin, Canada):
    """Yukon"""

    FIXED_HOLIDAYS: Incomplete
    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class NorthwestTerritories(RemembranceDayShiftMixin, VictoriaDayMixin, ThanksgivingMixin, Canada):
    """Northwest Territories"""

    FIXED_HOLIDAYS: Incomplete
    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...

class Nunavut(VictoriaDayMixin, ThanksgivingMixin, RemembranceDayShiftMixin, Canada):
    """Nunavut"""

    include_good_friday: ClassVar[bool]
    def get_variable_days(self, year): ...
