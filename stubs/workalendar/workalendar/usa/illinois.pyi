from typing import ClassVar

from .core import UnitedStates

class Illinois(UnitedStates):
    """Illinois"""

    include_thanksgiving_friday: ClassVar[bool]
    include_lincoln_birthday: ClassVar[bool]
    include_election_day_even: ClassVar[bool]

class ChicagoIllinois(Illinois):
    """Chicago, Illinois"""

    include_thanksgiving_friday: ClassVar[bool]
    def get_pulaski_day(self, year):
        """
        Return Casimir Pulaski Day.

        Defined on the first MON of March.
        ref: https://en.wikipedia.org/wiki/Casimir_Pulaski_Day
        """

    def get_variable_days(self, year): ...
