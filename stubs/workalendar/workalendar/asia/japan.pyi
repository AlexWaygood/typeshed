from _typeshed import Incomplete

from ..core import Calendar

class Japan(Calendar):
    """Japan"""

    WEEKEND_DAYS: Incomplete
    FIXED_HOLIDAYS: Incomplete
    def get_fixed_holidays(self, year):
        """
        Fixed holidays for Japan.
        """

    def get_variable_days(self, year): ...

class JapanBank(Japan):
    """The Bank of Japan is closed additional days other than
    national holidays.
    https://www.boj.or.jp/en/about/outline/holi.htm/
    """

    FIXED_HOLIDAYS: Incomplete
