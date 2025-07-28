from typing import ClassVar

from .core import UnitedStates

class Indiana(UnitedStates):
    """Indiana"""

    include_good_friday: ClassVar[bool]
    include_thanksgiving_friday: ClassVar[bool]
    thanksgiving_friday_label: ClassVar[str]
    include_federal_presidents_day: ClassVar[bool]
    label_washington_birthday_december: ClassVar[str]
    include_election_day_even: ClassVar[bool]
    election_day_label: ClassVar[str]
    def get_washington_birthday_december(self, year):
        """
        Washington birthday observance
        Similar to Christmas Eve, but with special rules.
        It's only observed in Georgia.
        """

    def get_primary_election_day(self, year):
        """
        Return the Primary Election Day

        FIXME: Wikipedia says it's a floating MON, but other sources say it's
        "the first Tuesday after the first Monday of May and every two years
        thereafter".
        """

    def get_variable_days(self, year): ...
