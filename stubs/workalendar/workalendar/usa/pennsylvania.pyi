from typing import ClassVar

from .core import UnitedStates

class Pennsylvania(UnitedStates):
    """Pennsylvania"""

    include_good_friday: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    include_election_day_every_year: ClassVar[bool]
