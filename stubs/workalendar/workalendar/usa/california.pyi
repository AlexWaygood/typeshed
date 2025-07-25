from _typeshed import Incomplete
from typing import ClassVar

from .core import UnitedStates

class California(UnitedStates):
    """California"""

    include_thanksgiving_friday: ClassVar[bool]
    include_cesar_chavez_day: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
    shift_exceptions: Incomplete
    def get_cesar_chavez_days(self, year):
        """
        Special shift rules for Cesar Chavez Day in California
        """

class CaliforniaEducation(California):
    """California Education

    This administration holds its own calendar. In order to respect the goal
    of workalendar (to compute (non)working days), we've decided to only retain
    days when the schools are closed.
    """

    def get_variable_days(self, year): ...

class CaliforniaBerkeley(California):
    """
    Berkeley, California
    """

    FIXED_HOLIDAYS: Incomplete
    include_cesar_chavez_day: ClassVar[bool]
    include_lincoln_birthday: ClassVar[bool]
    include_columbus_day: ClassVar[bool]
    columbus_day_label: ClassVar[str]

class CaliforniaSanFrancisco(California):
    """
    San Francisco, California
    """

    include_cesar_chavez_day: ClassVar[bool]
    include_columbus_day: ClassVar[bool]

class CaliforniaWestHollywood(California):
    """
    West Hollywood, California
    """

    FIXED_HOLIDAYS: Incomplete
    include_cesar_chavez_day: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
