"""
Scotland specific module.

The main source of information is:
https://en.wikipedia.org/wiki/Public_and_bank_holidays_in_Scotland

Note on "inheritance":

* Carnoustie and Monifieth area is a subdivision of Angus
* Lanark is part of South Lanarkshire

FIXME:

* Galashiels is part of the Scottish Borders
* Hawick is part of the Scottish Borders
* Kilmarnock is probably part of AyrShire (?)
* Lanark is part of South Lanarkshire
* Linlithgow... part of N/A
* Lochaber... part of N/A
* ...

"""

from _typeshed import Incomplete
from typing import ClassVar

from ...core import WesternCalendar
from .mixins import (
    AutumnHolidayFirstMondayOctober,
    AutumnHolidayLastMondaySeptember,
    AutumnHolidaySecondMondayOctober,
    AutumnHolidayThirdMondayOctober,
    AyrGoldCup,
    BattleStirlingBridge,
    FairHolidayFirstMondayAugust,
    FairHolidayFirstMondayJuly,
    FairHolidayFourthFridayJuly,
    FairHolidayLastMondayJuly,
    FairHolidayLastMondayJune,
    FairHolidaySecondMondayJuly,
    FairHolidayThirdMondayJuly,
    LateSummer,
    SpringHolidayFirstMondayApril,
    SpringHolidayFirstMondayJune,
    SpringHolidayLastMondayMay,
    SpringHolidaySecondMondayApril,
    SpringHolidayTuesdayAfterFirstMondayMay,
    VictoriaDayFirstMondayJune,
    VictoriaDayFourthMondayMay,
    VictoriaDayLastMondayMay,
)

class Scotland(WesternCalendar):
    """Scotland"""

    FIXED_HOLIDAYS: Incomplete
    include_spring_holiday: ClassVar[bool]
    spring_holiday_label: ClassVar[str]
    include_fair_holiday: ClassVar[bool]
    include_autumn_holiday: ClassVar[bool]
    include_saint_andrew: ClassVar[bool]
    include_victoria_day: ClassVar[bool]
    def __init__(self, *args, **kwargs) -> None: ...
    def get_may_day(self, year):
        """
        May Day is the first Monday in May
        """

    def get_spring_holiday(self, year) -> None:
        """
        Return spring holiday date and label.

        You need to implement it as soon as the flag `include_spring_holiday`
        is True.
        """

    def get_fair_holiday(self, year) -> None:
        """
        Return fair holiday date and label.

        You need to implement it as soon as the flag `include_fair_holiday`
        is True.
        """

    def get_autumn_holiday(self, year) -> None:
        """
        Return autumn holiday date and label.

        You need to implement it as soon as the flag `include_autumn_holiday`
        is True.
        """

    def get_victoria_day(self, year) -> None:
        """
        Return Victoria day date and label.

        You need to implement it as soon as the flag `include_victoria_day`
        is True.
        """

    def get_variable_days(self, year): ...
    def get_fixed_holidays(self, year): ...

class Aberdeen(FairHolidaySecondMondayJuly, AutumnHolidayLastMondaySeptember, Scotland):
    """Aberdeen"""

    include_good_friday: ClassVar[bool]

class Angus(SpringHolidaySecondMondayApril, AutumnHolidayLastMondaySeptember, Scotland):
    """Angus"""

    include_saint_andrew: ClassVar[bool]

class Arbroath(FairHolidayThirdMondayJuly, Scotland):
    """Arbroath"""

class Ayr(SpringHolidayLastMondayMay, AyrGoldCup, Scotland):
    """Ayr"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class CarnoustieMonifieth(SpringHolidayFirstMondayApril, AutumnHolidayFirstMondayOctober, Scotland):
    """Carnoustie & Monifieth"""

class Clydebank(SpringHolidayTuesdayAfterFirstMondayMay, Scotland):
    """Clydebank"""

class DumfriesGalloway(Scotland):
    """Dumfries & Galloway"""

    include_good_friday: ClassVar[bool]

class Dundee(
    SpringHolidayFirstMondayApril, VictoriaDayLastMondayMay, FairHolidayLastMondayJuly, AutumnHolidayFirstMondayOctober, Scotland
):
    """Dundee"""

class EastDunbartonshire(SpringHolidayLastMondayMay, FairHolidayThirdMondayJuly, AutumnHolidayLastMondaySeptember, Scotland):
    """East Dunbartonshire"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Edinburgh(Scotland):
    """Edinburgh"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_spring_holiday: ClassVar[bool]
    include_victoria_day: ClassVar[bool]
    include_autumn_holiday: ClassVar[bool]
    def get_spring_holiday(self, year):
        """
        Return Spring Holiday for Edinburgh.

        Set to the 3rd Monday of April, unless it falls on Easter Monday, then
        it's shifted to previous week.
        """

    def get_victoria_day(self, year):
        """
        Return Victoria Day for Edinburgh.

        Set to the Monday strictly before May 24th. It means that if May 24th
        is a Monday, it's shifted to the week before.
        """

    def get_autumn_holiday(self, year):
        """
        Return Autumn Holiday for Edinburgh.

        Set to the third Monday in September. Since it's the only region to
        follow this rule, we won't have a Mixin associated to it.
        """

class Elgin(SpringHolidaySecondMondayApril, FairHolidayLastMondayJune, LateSummer, AutumnHolidayThirdMondayOctober, Scotland):
    """Elgin"""

class Falkirk(FairHolidayFirstMondayJuly, BattleStirlingBridge, Scotland):
    """Falkirk"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Fife(VictoriaDayFirstMondayJune, FairHolidayThirdMondayJuly, AutumnHolidayThirdMondayOctober, Scotland):
    """Fife"""

    include_saint_andrew: ClassVar[bool]
    def get_variable_days(self, year): ...

class Galashiels(SpringHolidayFirstMondayJune, Scotland):
    """Galashiels"""

    def get_variable_days(self, year): ...

class Glasgow(SpringHolidayLastMondayMay, FairHolidayThirdMondayJuly, AutumnHolidayLastMondaySeptember, Scotland):
    """Glasgow"""

    include_easter_monday: ClassVar[bool]

class Hawick(Scotland):
    """Hawick"""

    def get_variable_days(self, year): ...

class Inverclyde(LateSummer, Scotland):
    """Inverclyde"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    def get_variable_days(self, year): ...

class Inverness(SpringHolidayFirstMondayApril, FairHolidayFirstMondayJuly, AutumnHolidayFirstMondayOctober, Scotland):
    """Inverness"""

    def get_variable_days(self, year): ...

class Kilmarnock(AyrGoldCup, Scotland):
    """Kilmarnock"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Lanark(Scotland):
    """Lanark"""

    def get_variable_days(self, year): ...

class Linlithgow(Scotland):
    """Linlithgow"""

    def get_variable_days(self, year): ...

class Lochaber(Scotland):
    """Lochaber"""

    def get_variable_days(self, year): ...

class NorthLanarkshire(SpringHolidayLastMondayMay, FairHolidayThirdMondayJuly, AutumnHolidayLastMondaySeptember, Scotland):
    """North Lanarkshire"""

    include_easter_monday: ClassVar[bool]

class Paisley(VictoriaDayLastMondayMay, FairHolidayFirstMondayAugust, AutumnHolidayLastMondaySeptember, Scotland):
    """Paisley"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Perth(
    SpringHolidayFirstMondayApril, VictoriaDayFourthMondayMay, BattleStirlingBridge, AutumnHolidayFirstMondayOctober, Scotland
):
    """Perth"""

class ScottishBorders(SpringHolidayFirstMondayApril, FairHolidayFourthFridayJuly, AutumnHolidaySecondMondayOctober, Scotland):
    """Scottish Borders"""

    include_saint_andrew: ClassVar[bool]

class SouthLanarkshire(SpringHolidayLastMondayMay, FairHolidayThirdMondayJuly, AutumnHolidayLastMondaySeptember, Scotland):
    """South Lanarkshire"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Stirling(SpringHolidayTuesdayAfterFirstMondayMay, BattleStirlingBridge, Scotland):
    """Stirling"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class WestDunbartonshire(AutumnHolidayLastMondaySeptember, Scotland):
    """West Dunbartonshire"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
