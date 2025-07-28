from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

QUEENS_BIRTHDAY_EXCEPTIONS: Incomplete

class CaymanIslands(WesternCalendar):
    """Cayman Islands"""

    include_ash_wednesday: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    shift_new_years_day: ClassVar[bool]
    def get_variable_days(self, year): ...
    def get_national_heroes_day(self, year):
        """National Heroes day: Fourth MON in January"""

    def get_discovery_day(self, year):
        """Discovery Day: Third MON in May"""

    def get_queens_birthday(self, year):
        """
        Queen's Birthday: On MON after second SAT in June, with exceptions
        """

    def get_constitution_day(self, year):
        """
        Constitution Day: First MON of July.
        """

    def get_remembrance_day(self, year):
        """
        Remembrance Day: Second MON of November.
        """
