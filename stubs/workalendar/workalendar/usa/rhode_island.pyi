from typing import ClassVar

from .core import UnitedStates

class RhodeIsland(UnitedStates):
    """Rhode Island"""

    include_federal_presidents_day: ClassVar[bool]
    include_election_day_even: ClassVar[bool]
    def get_variable_days(self, year): ...
