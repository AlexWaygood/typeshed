from _typeshed import Incomplete
from typing import ClassVar

from ..core import Calendar

class Israel(Calendar):
    """Israel"""

    include_new_years_day: ClassVar[bool]
    WEEKEND_DAYS: Incomplete
    def get_variable_days(self, year): ...
    def get_hebrew_independence_day(self, jewish_year):
        """
        Returns the independence day eve and independence day dates
        according to the given hebrew year

        :param jewish_year: the specific hebrew year for calculating
                            the independence day dates
        :return: independence day dates
                 in the type of List[Tuple[HebrewDate, str]]
        """
