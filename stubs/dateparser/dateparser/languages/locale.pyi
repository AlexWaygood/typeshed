from re import Pattern
from typing import Final

from dateparser.conf import Settings

NUMERAL_PATTERN: Final[Pattern[str]]

class Locale:
    """
    Class that deals with applicability and translation from a locale.

    :param shortname:
        A locale code, e.g. 'fr-PF', 'qu-EC', 'af-NA'.
    :type shortname: str

    :param language_info:
        Language info (translation data) of the language the locale belongs to.
    :type language_info: dict

    :return: A Locale instance
    """

    shortname: str
    def __init__(self, shortname: str, language_info) -> None: ...
    def is_applicable(self, date_string: str, strip_timezone: bool = False, settings: Settings | None = None) -> bool:
        """
        Check if the locale is applicable to translate date string.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param strip_timezone:
            If True, timezone is stripped from date string.
        :type strip_timezone: bool

        :return: boolean value representing if the locale is applicable for the date string or not.
        """

    def count_applicability(self, text: str, strip_timezone: bool = False, settings: Settings | None = None): ...
    @staticmethod
    def clean_dictionary(dictionary, threshold: int = 2): ...
    def translate(self, date_string: str, keep_formatting: bool = False, settings: Settings | None = None) -> str:
        """
        Translate the date string to its English equivalent.

        :param date_string:
            A string representing date and/or time in a recognizably valid format.
        :type date_string: str

        :param keep_formatting:
            If True, retain formatting of the date string after translation.
        :type keep_formatting: bool

        :return: translated date string.
        """

    def translate_search(self, search_string, settings: Settings | None = None): ...
    def get_wordchars_for_detection(self, settings): ...
    def to_parserinfo(self, base_cls=...): ...
