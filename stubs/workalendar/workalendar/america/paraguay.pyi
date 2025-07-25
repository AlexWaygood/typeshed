from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Paraguay(WesternCalendar):
    """Paraguay"""

    FIXED_HOLIDAYS: Incomplete
    include_labour_day: ClassVar[bool]
    include_holy_thursday: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_easter_saturday: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    immaculate_conception_label: ClassVar[str]
    def get_heroes_day(self, year):
        """
        Heroes Day is a fixed holidays.

        In 2017, it has been moved to February 27th ; otherwise, it happens on
        March 1st.

        ref: https://en.wikipedia.org/wiki/Public_holidays_in_Paraguay
        """

    def get_founding_of_asuncion(self, year):
        """
        Return the Founding of Asunción.

        In 2017, it has been moved to August 14th ; otherwise it happens on
        August 15th.
        """

    def get_boqueron_battle_victory_day(self, year):
        """
        Return Boqueron Battle Victory Day.

        In 2017, it has been moved to October 2nd ; otherwise it happens on
        September 29th.
        """

    def get_fixed_holidays(self, year):
        """
        Return fixed holidays for Paraguay.
        """
