from typing import ClassVar

from .core import UnitedStates

class NorthDakota(UnitedStates):
    """North Dakota"""

    include_columbus_day: ClassVar[bool]
    include_good_friday: ClassVar[bool]
