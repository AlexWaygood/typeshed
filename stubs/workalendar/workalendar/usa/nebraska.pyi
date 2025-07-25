from typing import ClassVar

from .core import UnitedStates

class Nebraska(UnitedStates):
    """Nebraska"""

    include_thanksgiving_friday: ClassVar[bool]
    def get_variable_days(self, year): ...
