from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Australia(WesternCalendar):
    """Australia"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_labour_day_october: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    shift_anzac_day: ClassVar[bool]
    ANZAC_SHIFT_DAYS: Incomplete
    FIXED_HOLIDAYS: Incomplete
    def get_canberra_day(self, year): ...
    def get_queens_birthday(self, year): ...
    def get_labour_day_october(self, year): ...
    def get_anzac_day(self, year): ...
    def get_variable_days(self, year): ...

class AustralianCapitalTerritory(Australia):
    """Australian Capital Territory"""

    include_easter_saturday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_labour_day_october: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    def get_family_community_day(self, year):
        """
        Return Family & Community Day.

        see: https://en.wikipedia.org/wiki/Family_Day#Australia
        """

    def get_reconciliation_day(self, year):
        """
        Return Reconciliaton Day.

        As of 2018, it replaces Family & Community Day.
        """

    def get_variable_days(self, year): ...

class NewSouthWales(Australia):
    """New South Wales"""

    include_queens_birthday: ClassVar[bool]
    include_easter_saturday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_labour_day_october: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    ANZAC_SHIFT_DAYS: Incomplete

class NorthernTerritory(Australia):
    """Northern Territory"""

    include_easter_saturday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    ANZAC_SHIFT_DAYS: Incomplete
    def get_may_day(self, year): ...
    def get_picnic_day(self, year): ...
    def get_variable_days(self, year): ...

class Queensland(Australia):
    """Queensland"""

    include_easter_saturday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    ANZAC_SHIFT_DAYS: Incomplete
    def get_labour_day_may(self, year): ...
    def get_variable_days(self, year): ...

class SouthAustralia(Australia):
    """South Australia"""

    include_easter_saturday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_labour_day_october: ClassVar[bool]
    ANZAC_SHIFT_DAYS: Incomplete
    def get_adelaides_cup(self, year): ...
    def get_proclamation_day(self, year): ...
    def get_variable_days(self, year): ...

class Tasmania(Australia):
    """Tasmania"""

    include_queens_birthday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    shift_anzac_day: ClassVar[bool]
    @property
    def has_recreation_day(self): ...
    def get_eight_hours_day(self, year): ...
    def get_recreation_day(self, year): ...
    def get_variable_days(self, year): ...

class Hobart(Tasmania):
    """Hobart"""

    @property
    def has_recreation_day(self): ...
    def get_hobart(self, year): ...
    def get_variable_days(self, year): ...

class Victoria(Australia):
    """Victoria"""

    include_easter_saturday: ClassVar[bool]
    include_queens_birthday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    shift_anzac_day: ClassVar[bool]
    def get_labours_day_in_march(self, year): ...
    def get_melbourne_cup(self, year): ...
    def get_variable_days(self, year): ...

class WesternAustralia(Australia):
    """Western Australia"""

    include_boxing_day: ClassVar[bool]
    def get_labours_day_in_march(self, year): ...
    def get_western_australia_day(self, year): ...
    def get_variable_days(self, year): ...
