"""
Working day tools
"""

from _typeshed import Incomplete
from collections.abc import Generator
from typing import ClassVar

MON: Incomplete
TUE: Incomplete
WED: Incomplete
THU: Incomplete
FRI: Incomplete
SAT: Incomplete
SUN: Incomplete
ISO_MON: Incomplete
ISO_TUE: Incomplete
ISO_WED: Incomplete
ISO_THU: Incomplete
ISO_FRI: Incomplete
ISO_SAT: Incomplete
ISO_SUN: Incomplete

def cleaned_date(day, keep_datetime: bool = False):
    """
    Return a "clean" date type.

    * keep a `date` unchanged
    * convert a datetime into a date,
    * convert any "duck date" type into a date using its `date()` method.
    """

def daterange(start, end) -> Generator[Incomplete, None, None]:
    """
    Yield days from ``start`` to ``end`` including both of them.

    If start and end are in opposite order, they'll be swapped silently.
    """

class ChristianMixin:
    EASTER_METHOD: Incomplete
    include_epiphany: ClassVar[bool]
    include_clean_monday: ClassVar[bool]
    include_annunciation: ClassVar[bool]
    include_fat_tuesday: ClassVar[bool]
    fat_tuesday_label: ClassVar[str | None]
    include_ash_wednesday: ClassVar[bool]
    ash_wednesday_label: ClassVar[str]
    include_palm_sunday: ClassVar[bool]
    include_holy_thursday: ClassVar[bool]
    holy_thursday_label: ClassVar[str]
    include_good_friday: ClassVar[bool]
    good_friday_label: ClassVar[str]
    include_easter_monday: ClassVar[bool]
    include_easter_saturday: ClassVar[bool]
    easter_saturday_label: ClassVar[str]
    include_easter_sunday: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    immaculate_conception_label: ClassVar[str]
    include_christmas: ClassVar[bool]
    christmas_day_label: ClassVar[str]
    include_christmas_eve: ClassVar[bool]
    include_ascension: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_whit_sunday: ClassVar[bool]
    whit_sunday_label: ClassVar[str]
    include_whit_monday: ClassVar[bool]
    whit_monday_label: ClassVar[str]
    include_corpus_christi: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    boxing_day_label: ClassVar[str]
    include_all_souls: ClassVar[bool]
    def get_fat_tuesday(self, year): ...
    def get_ash_wednesday(self, year): ...
    def get_palm_sunday(self, year): ...
    def get_holy_thursday(self, year):
        """Return the date of the last thursday before easter"""

    def get_good_friday(self, year):
        """Return the date of the last friday before easter"""

    def get_clean_monday(self, year):
        """Return the clean monday date"""

    def get_easter_saturday(self, year):
        """Return the Easter Saturday date"""

    def get_easter_sunday(self, year):
        """Return the date of the easter (sunday) -- following the easter method"""

    def get_easter_monday(self, year):
        """Return the date of the monday after easter"""

    def get_ascension_thursday(self, year): ...
    def get_whit_monday(self, year): ...
    def get_whit_sunday(self, year): ...
    def get_corpus_christi(self, year): ...
    def shift_christmas_boxing_days(self, year):
        """When Christmas and/or Boxing Day falls on a weekend, it is rolled
        forward to the next weekday.
        """

    def get_variable_days(self, year):
        """Return the christian holidays list according to the mixin"""

class WesternMixin(ChristianMixin):
    """
    General usage calendar for Western countries.

    (chiefly Europe and Northern America)

    """

    EASTER_METHOD: Incomplete
    WEEKEND_DAYS: Incomplete

class OrthodoxMixin(ChristianMixin):
    EASTER_METHOD: Incomplete
    WEEKEND_DAYS: Incomplete
    include_orthodox_christmas: ClassVar[bool]
    orthodox_christmas_day_label: ClassVar[str]
    def get_fixed_holidays(self, year): ...

class LunarMixin:
    """
    Calendar ready to compute luncar calendar days
    """

    @staticmethod
    def lunar(year, month, day): ...

class ChineseNewYearMixin(LunarMixin):
    """
    Calendar including toolsets to compute the Chinese New Year holidays.
    """

    include_chinese_new_year_eve: ClassVar[bool]
    chinese_new_year_eve_label: ClassVar[str]
    include_chinese_new_year: ClassVar[bool]
    chinese_new_year_label: ClassVar[str]
    include_chinese_second_day: ClassVar[bool]
    chinese_second_day_label: ClassVar[str]
    include_chinese_third_day: ClassVar[bool]
    chinese_third_day_label: ClassVar[str]
    shift_sunday_holidays: ClassVar[bool]
    shift_start_cny_sunday: ClassVar[bool]
    def get_chinese_new_year(self, year):
        """
        Compute Chinese New Year days. To return a list of holidays.

        By default, it'll at least return the Chinese New Year holidays chosen
        using the following options:

        * ``include_chinese_new_year_eve``
        * ``include_chinese_new_year`` (on by default)
        * ``include_chinese_second_day``

        If the ``shift_sunday_holidays`` option is on, the rules are the
        following.

        * If the CNY1 falls on MON-FRI, there's not shift.
        * If the CNY1 falls on SAT, the CNY2 is shifted to the Monday after.
        * If the CNY1 falls on SUN, the CNY1 is shifted to the Monday after,
          and CNY2 is shifted to the Tuesday after.
        """

    def get_variable_days(self, year): ...
    def get_shifted_holidays(self, dates) -> Generator[Incomplete, None, None]:
        """
        Taking a list of existing holidays, yield a list of 'shifted' days if
        the holiday falls on SUN.
        """

    def get_calendar_holidays(self, year):
        """
        Take into account the eventual shift to the next MON if any holiday
        falls on SUN.
        """

class CalverterMixin:
    conversion_method: Incomplete
    ISLAMIC_HOLIDAYS: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def converted(self, year): ...
    def calverted_years(self, year): ...
    def get_islamic_holidays(self): ...
    def get_delta_islamic_holidays(self, year) -> None:
        """
        Return the delta to add/substract according to the year or customs.

        By default, to return None or timedelta(days=0)
        """

    def get_variable_days(self, year): ...

class IslamicMixin(CalverterMixin):
    WEEKEND_DAYS: Incomplete
    conversion_method: Incomplete
    include_prophet_birthday: ClassVar[bool]
    include_day_after_prophet_birthday: ClassVar[bool]
    include_start_ramadan: ClassVar[bool]
    include_eid_al_fitr: ClassVar[bool]
    length_eid_al_fitr: int
    eid_al_fitr_label: ClassVar[str]
    include_eid_al_adha: ClassVar[bool]
    eid_al_adha_label: ClassVar[str]
    length_eid_al_adha: int
    include_day_of_sacrifice: ClassVar[bool]
    day_of_sacrifice_label: ClassVar[str]
    include_islamic_new_year: ClassVar[bool]
    include_laylat_al_qadr: ClassVar[bool]
    include_nuzul_al_quran: ClassVar[bool]
    def get_islamic_holidays(self):
        """Return a list of Islamic (month, day, label) for islamic holidays.
        Please take note that these dates must be expressed using the Islamic
        Calendar
        """

class CoreCalendar:
    FIXED_HOLIDAYS: Incomplete
    WEEKEND_DAYS: Incomplete
    def __init__(self) -> None: ...
    def name(cls): ...
    def get_fixed_holidays(self, year):
        """Return the fixed days according to the FIXED_HOLIDAYS class property"""

    def get_variable_days(self, year): ...
    def get_calendar_holidays(self, year):
        """Get calendar holidays.
        If you want to override this, please make sure that it **must** return
        a list of tuples (date, holiday_name).
        """

    def holidays(self, year=None):
        """Computes holidays (non-working days) for a given year.
        Return a 2-item tuple, composed of the date and a label.
        """

    def get_holiday_label(self, day):
        """Return the label of the holiday, if the date is a holiday"""

    def holidays_set(self, year=None):
        """Return a quick date index (set)"""

    def get_weekend_days(self):
        """Return a list (or a tuple) of weekdays that are *not* working days.

        e.g: return (SAT, SUN,)

        """

    def is_working_day(self, day, extra_working_days=None, extra_holidays=None):
        """Return True if it's a working day.
        In addition to the regular holidays, you can add exceptions.

        By providing ``extra_working_days``, you'll state that these dates
        **are** working days.

        By providing ``extra_holidays``, you'll state that these dates **are**
        holidays, even if not in the regular calendar holidays (or weekends).

        Please note that the ``extra_working_days`` list has priority over the
        ``extra_holidays`` list.

        """

    def is_holiday(self, day, extra_holidays=None):
        """Return True if it's an holiday.
        In addition to the regular holidays, you can add exceptions.

        By providing ``extra_holidays``, you'll state that these dates **are**
        holidays, even if not in the regular calendar holidays (or weekends).

        """

    def add_working_days(self, day, delta, extra_working_days=None, extra_holidays=None, keep_datetime: bool = False):
        """Add `delta` working days to the date.

        You can provide either a date or a datetime to this function that will
        output a ``date`` result. You can alter this behaviour using the
        ``keep_datetime`` option set to ``True``.

        the ``delta`` parameter might be positive or negative. If it's
        negative, you may want to use the ``sub_working_days()`` method with
        a positive ``delta`` argument.

        By providing ``extra_working_days``, you'll state that these dates
        **are** working days.

        By providing ``extra_holidays``, you'll state that these dates **are**
        holidays, even if not in the regular calendar holidays (or weekends).

        Please note that the ``extra_working_days`` list has priority over the
        ``extra_holidays`` list.
        """

    def sub_working_days(self, day, delta, extra_working_days=None, extra_holidays=None, keep_datetime: bool = False):
        """
        Substract `delta` working days to the date.

        This method is a shortcut / helper. Users may want to use either::

            cal.add_working_days(my_date, -7)
            cal.sub_working_days(my_date, 7)

        The other parameters are to be used exactly as in the
        ``add_working_days`` method.

        A negative ``delta`` argument will be converted into its absolute
        value. Hence, the two following calls are equivalent::

            cal.sub_working_days(my_date, -7)
            cal.sub_working_days(my_date, 7)

        As in ``add_working_days()`` you can set the parameter
        ``keep_datetime`` to ``True`` to make sure that if your ``day``
        argument is a ``datetime``, the returned date will also be a
        ``datetime`` object.

        """

    def find_following_working_day(self, day):
        """Looks for the following working day, if not already a working day.

        **WARNING**: this function doesn't take into account the calendar
        holidays, only the days of the week and the weekend days parameters.
        """

    @staticmethod
    def get_nth_weekday_in_month(year, month, weekday, n: int = 1, start=None):
        """Get the nth weekday in a given month. e.g:

        >>> # the 1st monday in Jan 2013
        >>> Calendar.get_nth_weekday_in_month(2013, 1, MON)
        datetime.date(2013, 1, 7)
        >>> # The 2nd monday in Jan 2013
        >>> Calendar.get_nth_weekday_in_month(2013, 1, MON, 2)
        datetime.date(2013, 1, 14)
        """

    @staticmethod
    def get_last_weekday_in_month(year, month, weekday):
        """Get the last weekday in a given month. e.g:

        >>> # the last monday in Jan 2013
        >>> Calendar.get_last_weekday_in_month(2013, 1, MON)
        datetime.date(2013, 1, 28)
        """

    @staticmethod
    def get_iso_week_date(year, week_nb, weekday=1):
        """
        Return the date of the weekday of the week number (ISO definition).

        **Warning:** in the ISO definition, the weeks start on MON, not SUN.

        By default, if you don't provide the ``weekday`` argument, it'll return
        the date of the MON of this week number.

        Example:

            >>> Calendar.get_iso_week_date(2021, 44)
            datetime.date(2021, 11, 1)

        For your convenience, the ISO weekdays are available via the
        ``workalendar.core`` module, like this:

            from workalendar.core import ISO_MON, ISO_TUE  # etc.

        i.e.: if you need to get the FRI of the week 44 of the year 2020,
        you'll have to use:

            from workalendar.core import ISO_FRI
            Calendar.get_iso_week_date(2020, 44, ISO_FRI)

        """

    @staticmethod
    def get_first_weekday_after(day, weekday):
        """Get the first weekday after a given day. If the day is the same
        weekday, the same day will be returned.

        >>> # the first monday after Apr 1 2015
        >>> Calendar.get_first_weekday_after(date(2015, 4, 1), MON)
        datetime.date(2015, 4, 6)

        >>> # the first tuesday after Apr 14 2015
        >>> Calendar.get_first_weekday_after(date(2015, 4, 14), TUE)
        datetime.date(2015, 4, 14)
        """

    def get_working_days_delta(self, start, end, include_start: bool = False, extra_working_days=None, extra_holidays=None):
        """
        Return the number of working day between two given dates.
        The order of the dates provided doesn't matter.

        In the following example, there are 5 days, because of the week-end:

        >>> cal = WesternCalendar()  # does not include easter monday
        >>> day1 = date(2018, 3, 29)
        >>> day2 = date(2018, 4, 5)
        >>> cal.get_working_days_delta(day1, day2)
        5

        In France, April 1st 2018 is a holiday because it's Easter monday:

        >>> cal = France()
        >>> cal.get_working_days_delta(day1, day2)
        4

        This method should even work if your ``start`` and ``end`` arguments
        are datetimes.

        By default, if the day after you start is not a working day,
        the count will start at 0. If include_start is set to true,
        this day will be taken into account.

        Example:

        >>> from dateutil.parser import parse
        >>> cal = France()
        >>> day1 = parse('09/05/2018 00:01', dayfirst=True)
        >>> day2 = parse('10/05/2018 19:01', dayfirst=True) # holiday in france
        >>> cal.get_working_days_delta(day1, day2)
        0

        >>> cal.get_working_days_delta(day1, day2, include_start=True)
        1

        As in many other methods, you can use the ``extra_holidays`` and
        ``extra_working_days`` to exclude
        """

    def export_to_ical(self, period=[2000, 2030], target_path=None):
        """
        Export the calendar to iCal (RFC 5545) format.

        Parameters
        ----------
        period: [int, int]
            start and end year (inclusive) of calendar
            Default is [2000, 2030]

        target_path: str or pathlib.Path
            the name or path of the exported file. If this argument is missing,
            the function will return the ical content.

        """

class Calendar(CoreCalendar):
    """
    The cornerstone of Earth calendars.

    Take care of the New Years Day, which is almost a worldwide holiday.
    """

    include_new_years_day: ClassVar[bool]
    include_new_years_eve: ClassVar[bool]
    shift_new_years_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    labour_day_label: ClassVar[str]
    def __init__(self, **kwargs) -> None: ...
    def get_fixed_holidays(self, year): ...
    def get_variable_days(self, year): ...

class WesternCalendar(WesternMixin, Calendar):
    """
    A Christian calendar using Western definition for Easter.
    """

class OrthodoxCalendar(OrthodoxMixin, Calendar):
    """
    A Christian calendar using Orthodox definition for Easter.
    """

class ChineseNewYearCalendar(ChineseNewYearMixin, Calendar):
    """
    Chinese Calendar, using Chinese New Year computation.
    """

    WEEKEND_DAYS: Incomplete

class IslamicCalendar(IslamicMixin, Calendar):
    """
    Islamic calendar
    """

class IslamoWesternCalendar(IslamicMixin, WesternMixin, Calendar):
    """
    Mix of Islamic and Western calendars.

    When countries have both Islamic and Western-Christian holidays.
    """

    FIXED_HOLIDAYS: Incomplete
