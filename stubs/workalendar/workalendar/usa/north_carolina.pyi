from typing import ClassVar

from .core import UnitedStates

class NorthCarolina(UnitedStates):
    """North Carolina"""

    include_good_friday: ClassVar[bool]
    include_christmas_eve: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    include_federal_presidents_day: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
    def get_christmas_shifts(self, year):
        """
        Return Specific Christmas days extra shifts.
        There must be 3 holidays in a row: Christmas Eve, Christmas Day and
        Boxing Day. If one or the other falls on SUN/SAT, extra days must be
        added.
        """

    def get_variable_days(self, year): ...
