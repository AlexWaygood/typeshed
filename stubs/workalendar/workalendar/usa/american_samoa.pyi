from typing import ClassVar

from .core import UnitedStates

class AmericanSamoa(UnitedStates):
    """American Samoa"""

    include_boxing_day: ClassVar[bool]
    boxing_day_label: ClassVar[str]
    def get_flag_day(self, year):
        """
        Flag day is on April 17th
        """

    def get_variable_days(self, year): ...
