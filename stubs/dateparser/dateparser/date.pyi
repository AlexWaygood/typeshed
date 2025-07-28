import collections
from collections.abc import Callable, Iterable, Iterator
from datetime import datetime, tzinfo
from re import Pattern
from typing import ClassVar, Final, Literal, overload
from typing_extensions import TypeAlias

from dateparser import _Settings
from dateparser.conf import Settings
from dateparser.languages.loader import LocaleDataLoader
from dateparser.languages.locale import Locale

_DetectLanguagesFunction: TypeAlias = Callable[[str, float], list[str]]
_Period: TypeAlias = Literal["time", "day", "week", "month", "year"]

APOSTROPHE_LOOK_ALIKE_CHARS: Final[list[str]]
RE_NBSP: Final[Pattern[str]]
RE_SPACES: Final[Pattern[str]]
RE_TRIM_SPACES: Final[Pattern[str]]
RE_TRIM_COLONS: Final[Pattern[str]]
RE_SANITIZE_SKIP: Final[Pattern[str]]
RE_SANITIZE_RUSSIAN: Final[Pattern[str]]
RE_SANITIZE_PERIOD: Final[Pattern[str]]
RE_SANITIZE_ON: Final[Pattern[str]]
RE_SANITIZE_APOSTROPHE: Final[Pattern[str]]
RE_SEARCH_TIMESTAMP: Final[Pattern[str]]
RE_SANITIZE_CROATIAN: Final[Pattern[str]]
RE_SEARCH_NEGATIVE_TIMESTAMP: Final[Pattern[str]]

def sanitize_spaces(date_string: str) -> str: ...
def date_range(begin: datetime, end: datetime, **kwargs) -> None: ...
def get_intersecting_periods(low: datetime, high: datetime, period: str = "day") -> None: ...
def sanitize_date(date_string: str) -> str: ...
def get_date_from_timestamp(date_string: str, settings: Settings, negative: bool = False) -> datetime | None: ...
def parse_with_formats(date_string: str, date_formats: Iterable[str], settings: Settings) -> DateData:
    """Parse with formats and return a dictionary with 'period' and 'obj_date'.

    :returns: :class:`datetime.datetime`, dict or None

    """

class _DateLocaleParser:
    locale: Locale
    date_string: str
    date_formats: list[str] | tuple[str, ...] | set[str] | None
    def __init__(
        self,
        locale: Locale,
        date_string: str,
        date_formats: list[str] | tuple[str, ...] | set[str] | None,
        settings: Settings | None = None,
    ) -> None: ...
    @classmethod
    def parse(
        cls,
        locale: Locale,
        date_string: str,
        date_formats: list[str] | tuple[str, ...] | set[str] | None = None,
        settings: Settings | None = None,
    ) -> DateData: ...
    def _parse(self) -> DateData | None: ...
    def _try_timestamp(self) -> DateData: ...
    def _try_freshness_parser(self) -> DateData | None: ...
    def _try_absolute_parser(self) -> DateData | None: ...
    def _try_nospaces_parser(self) -> DateData | None: ...
    def _try_parser(self, parse_method: Callable[[str, Settings, tzinfo | None], tuple[datetime, str]]) -> DateData | None: ...
    def _try_given_formats(self) -> DateData | None: ...
    def _get_translated_date(self) -> str: ...
    def _get_translated_date_with_formatting(self) -> str: ...
    def _is_valid_date_data(self, date_data: DateData) -> bool: ...

class DateData:
    """
    Class that represents the parsed data with useful information.
    It can be accessed with square brackets like a dict object.
    """

    date_obj: datetime | None
    locale: str | None
    period: _Period | None
    def __init__(self, *, date_obj: datetime | None = None, period: _Period | None = None, locale: str | None = None) -> None: ...
    @overload
    def __getitem__(self, k: Literal["date_obj"]) -> datetime | None: ...
    @overload
    def __getitem__(self, k: Literal["locale"]) -> str | None: ...
    @overload
    def __getitem__(self, k: Literal["period"]) -> _Period | None: ...
    @overload
    def __setitem__(self, k: Literal["date_obj"], v: datetime) -> None: ...
    @overload
    def __setitem__(self, k: Literal["locale"], v: str) -> None: ...
    @overload
    def __setitem__(self, k: Literal["period"], v: _Period) -> None: ...

class DateDataParser:
    """
    Class which handles language detection, translation and subsequent generic parsing of
    string representing date and/or time.

    :param languages:
        A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
        If locales are not given, languages and region are
        used to construct locales for translation.
    :type languages: list

    :param locales:
        A list of locale codes, e.g. ['fr-PF', 'qu-EC', 'af-NA'].
        The parser uses only these locales to translate date string.
    :type locales: list

    :param region:
        A region code, e.g. 'IN', '001', 'NE'.
        If locales are not given, languages and region are
        used to construct locales for translation.
    :type region: str

    :param try_previous_locales:
        If True, locales previously used to translate date are tried first.
    :type try_previous_locales: bool

    :param use_given_order:
        If True, locales are tried for translation of date string
        in the order in which they are given.
    :type use_given_order: bool

    :param settings:
        Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
    :type settings: dict

    :param detect_languages_function:
        A function for language detection that takes as input a `text` and a `confidence_threshold`,
        and returns a list of detected language codes.
        Note: this function is only used if ``languages`` and ``locales`` are not provided.
    :type detect_languages_function: function

    :return: A parser instance

    :raises:
         ``ValueError``: Unknown Language, ``TypeError``: Languages argument must be a list,
         ``SettingValidationError``: A provided setting is not valid.
    """

    _settings: Settings
    locale_loader: ClassVar[LocaleDataLoader | None]
    try_previous_locales: bool
    use_given_order: bool
    languages: list[str] | None
    locales: list[str] | tuple[str, ...] | set[str] | None
    region: str
    detect_languages_function: _DetectLanguagesFunction | None
    previous_locales: collections.OrderedDict[Locale, None]
    def __init__(
        self,
        languages: list[str] | tuple[str, ...] | set[str] | None = None,
        locales: list[str] | tuple[str, ...] | set[str] | None = None,
        region: str | None = None,
        try_previous_locales: bool = False,
        use_given_order: bool = False,
        settings: _Settings | None = None,
        detect_languages_function: _DetectLanguagesFunction | None = None,
    ) -> None: ...
    def get_date_data(self, date_string: str, date_formats: list[str] | tuple[str, ...] | set[str] | None = None) -> DateData:
        """
        Parse string representing date and/or time in recognizable localized formats.
        Supports parsing multiple languages and timezones.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str
        :param date_formats:
            A list of format strings using directives as given
            `here <https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior>`_.
            The parser applies formats one by one, taking into account the detected languages.
        :type date_formats: list

        :return: a ``DateData`` object.

        :raises: ValueError - Unknown Language

        .. note:: *Period* values can be a 'day' (default), 'week', 'month', 'year', 'time'.

        *Period* represents the granularity of date parsed from the given string.

        In the example below, since no day information is present, the day is assumed to be current
        day ``16`` from *current date* (which is June 16, 2015, at the moment of writing this).
        Hence, the level of precision is ``month``:

            >>> DateDataParser().get_date_data('March 2015')
            DateData(date_obj=datetime.datetime(2015, 3, 16, 0, 0), period='month', locale='en')

        Similarly, for date strings with no day and month information present, level of precision
        is ``year`` and day ``16`` and month ``6`` are from *current_date*.

            >>> DateDataParser().get_date_data('2014')
            DateData(date_obj=datetime.datetime(2014, 6, 16, 0, 0), period='year', locale='en')

        Dates with time zone indications or UTC offsets are returned in UTC time unless
        specified using `Settings <https://dateparser.readthedocs.io/en/latest/settings.html#settings>`__.

            >>> DateDataParser().get_date_data('23 March 2000, 1:21 PM CET')
            DateData(date_obj=datetime.datetime(2000, 3, 23, 13, 21, tzinfo=<StaticTzInfo 'CET'>),
            period='day', locale='en')

        """

    def get_date_tuple(self, date_string: str, date_formats: list[str] | tuple[str, ...] | set[str] | None = ...): ...
    def _get_applicable_locales(self, date_string: str) -> Iterator[Locale]: ...
    def _is_applicable_locale(self, locale: Locale, date_string: str) -> bool: ...
    @classmethod
    def _get_locale_loader(cls: type[DateDataParser]) -> LocaleDataLoader: ...
