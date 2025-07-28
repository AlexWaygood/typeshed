from typing import ClassVar

from .core import UnitedStates

class Maine(UnitedStates):
    """Maine"""

    include_thanksgiving_friday: ClassVar[bool]
    include_patriots_day: ClassVar[bool]
