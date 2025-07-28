from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Argentina(WesternCalendar):
    """Argentina"""

    include_labour_day: ClassVar[bool]
    labour_day_label: ClassVar[str]
    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str]
    include_good_friday: ClassVar[bool]
    include_easter_saturday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_christmas: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    immaculate_conception_label: ClassVar[str]
    FIXED_HOLIDAYS: Incomplete
    def get_general_guemes_day(self, year):
        """
        Día Paso a la Inmortalidad del General Martín Miguel de Güemes.

        Happens on June 17th, except:

        * if it happens on a THU, it's shifted to the next MON.
        * if it happens on a WED, it's shifted to the MON before this date.
        """

    def get_general_martin_day(self, year):
        """
        Día Paso a la Inmortalidad del Gral. José de San Martín

        Third MON of August.
        """

    def get_soberania_day(self, year):
        """
        Día de la Soberanía Nacional

        Happens on the 3rd MON of November after the first Friday.
        """

    def get_diversidad_day(self, year):
        """
        Día del Respeto a la Diversidad Cultural

        The pivot date is the 12th of October.

        * If it happens on a TUE, it's shifter on the 11th of Oct.
        * If it happens on a WED, THU, FRI or SAT, it's shifted on the first
          MON after this date.
        * Else, it's on the 12th of October.
        """

    def get_malvinas_day(self, year):
        """
        Día de las Malvinas

        In honour of the Veterans and the Fallen of the Malvinas war.
        https://en.wikipedia.org/wiki/Malvinas_Day

        In 2020, it was shifted to March 31st because of
        the coronavirus crisis.
        """

    def get_variable_days(self, year): ...
