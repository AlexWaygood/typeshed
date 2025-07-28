from typing import ClassVar

from .core import UnitedStates

class Alabama(UnitedStates):
    """Alabama"""

    include_confederation_day: ClassVar[bool]
    martin_luther_king_label: ClassVar[str]
    presidents_day_label: ClassVar[str]
    columbus_day_label: ClassVar[str]
    include_jefferson_davis_birthday: ClassVar[bool]

class AlabamaBaldwinCounty(Alabama):
    """Baldwin County, Alabama"""

    include_fat_tuesday: ClassVar[bool]

class AlabamaMobileCounty(Alabama):
    """Mobile County, Alabama"""

    include_fat_tuesday: ClassVar[bool]

class AlabamaPerryCounty(Alabama):
    """Mobile Perry, Alabama"""

    def get_obama_day(self, year):
        """
        Obama Day happens on the 2nd MON of November.
        """

    def get_variable_days(self, year): ...
