from typing import ClassVar

from .core import UnitedStates

class Georgia(UnitedStates):
    """Georgia"""

    include_confederation_day: ClassVar[bool]
    include_federal_presidents_day: ClassVar[bool]
    label_washington_birthday_december: ClassVar[str]
    thanksgiving_friday_label: ClassVar[str]
    def get_washington_birthday_december(self, year):
        """
        Washington birthday observance
        Similar to Christmas Eve, but with special rules.
        It's only observed in Georgia.
        """

    def get_confederate_day(self, year):
        """
        Confederate memorial day is on the 4th MON of April.

        Exception: Year 2020, when it happened on April 10th.
        """

    def get_robert_lee_birthday(self, year):
        """
        Robert E. Lee's birthday.

        Happens on the day after Thanksgiving.
        """

    def get_variable_days(self, year): ...
