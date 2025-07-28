from _typeshed import Incomplete
from typing import ClassVar

from .core import UnitedStates

class Massachusetts(UnitedStates):
    """Massachusetts"""

    include_patriots_day: ClassVar[bool]

class SuffolkCountyMassachusetts(Massachusetts):
    """Suffolk County, Massachusetts"""

    FIXED_HOLIDAYS: Incomplete
