from _typeshed import Incomplete
from typing import ClassVar

from .core import UnitedStates

class Hawaii(UnitedStates):
    """Hawaii"""

    include_good_friday: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
    include_election_day_even: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def get_statehood_day(self, year):
        """
        Statehood Day: 3rd Friday in August.
        """

    def get_variable_days(self, year): ...
