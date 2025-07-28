from _typeshed import Incomplete
from typing import ClassVar

from ..core import ChineseNewYearCalendar, WesternMixin

class HongKong(WesternMixin, ChineseNewYearCalendar):
    """Hong Kong"""

    include_labour_day: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_easter_saturday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    WEEKEND_DAYS: Incomplete
    FIXED_HOLIDAYS: Incomplete
    chinese_new_year_label: ClassVar[str]
    include_chinese_second_day: ClassVar[bool]
    chinese_second_day_label: ClassVar[str]
    include_chinese_third_day: ClassVar[bool]
    chinese_third_day_label: ClassVar[str]
    shift_sunday_holidays: ClassVar[bool]
    shift_start_cny_sunday: ClassVar[bool]
    def get_variable_days(self, year):
        """
        Hong Kong variable days
        """

class HongKongBank(HongKong):
    """Hong Kong Bank"""

    WEEKEND_DAYS: Incomplete
