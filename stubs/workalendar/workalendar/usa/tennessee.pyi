from typing import ClassVar

from .core import UnitedStates

class Tennessee(UnitedStates):
    """Tennessee"""

    include_columbus_day: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_christmas_eve: ClassVar[bool]
