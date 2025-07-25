import datetime
from typing import Literal, TypedDict
from typing_extensions import TypeAlias

from .date import DateDataParser, _DetectLanguagesFunction

__version__: str

_default_parser: DateDataParser

_Part: TypeAlias = Literal["day", "month", "year"]
_ParserKind: TypeAlias = Literal["timestamp", "relative-time", "custom-formats", "absolute-time", "no-spaces-time"]

class _Settings(TypedDict, total=False):
    DATE_ORDER: str
    PREFER_LOCALE_DATE_ORDER: bool
    TIMEZONE: str
    TO_TIMEZONE: str
    RETURN_AS_TIMEZONE_AWARE: bool
    PREFER_DAY_OF_MONTH: Literal["current", "first", "last"]
    PREFER_DATES_FROM: Literal["current_period", "future", "past"]
    RELATIVE_BASE: datetime.datetime
    STRICT_PARSING: bool
    REQUIRE_PARTS: list[_Part]
    SKIP_TOKENS: list[str]
    NORMALIZE: bool
    RETURN_TIME_AS_PERIOD: bool
    PARSERS: list[_ParserKind]

def parse(
    date_string: str,
    date_formats: list[str] | tuple[str, ...] | set[str] | None = None,
    languages: list[str] | tuple[str, ...] | set[str] | None = None,
    locales: list[str] | tuple[str, ...] | set[str] | None = None,
    region: str | None = None,
    settings: _Settings | None = None,
    detect_languages_function: _DetectLanguagesFunction | None = None,
) -> datetime.datetime | None:
    """Parse date and time from given date string.

    :param date_string:
        A string representing date and/or time in a recognizably valid format.
    :type date_string: str

    :param date_formats:
        A list of format strings using directives as given
        `here <https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior>`_.
        The parser applies formats one by one, taking into account the detected languages/locales.
    :type date_formats: list

    :param languages:
        A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
        If locales are not given, languages and region are used to construct locales for translation.
    :type languages: list

    :param locales:
        A list of locale codes, e.g. ['fr-PF', 'qu-EC', 'af-NA'].
        The parser uses only these locales to translate date string.
    :type locales: list

    :param region:
        A region code, e.g. 'IN', '001', 'NE'.
        If locales are not given, languages and region are used to construct locales for translation.
    :type region: str

    :param settings:
        Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
    :type settings: dict

    :param detect_languages_function:
        A function for language detection that takes as input a string (the `date_string`) and
        a `confidence_threshold`, and returns a list of detected language codes.
        Note: this function is only used if ``languages`` and ``locales`` are not provided.
    :type detect_languages_function: function

    :return: Returns :class:`datetime <datetime.datetime>` representing parsed date if successful, else returns None
    :rtype: :class:`datetime <datetime.datetime>`.
    :raises:
        ``ValueError``: Unknown Language, ``TypeError``: Languages argument must be a list,
        ``SettingValidationError``: A provided setting is not valid.
    """
