from typing import ClassVar

from .core import UnitedStates

class NewYork(UnitedStates):
    """New York"""

    include_lincoln_birthday: ClassVar[bool]
    include_election_day_every_year: ClassVar[bool]
