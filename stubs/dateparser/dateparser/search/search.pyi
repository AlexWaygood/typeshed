from collections.abc import Collection
from typing import Any

from ..date import _DetectLanguagesFunction

RELATIVE_REG: Any

def date_is_relative(translation): ...

class _ExactLanguageSearch:
    loader: Any
    language: Any
    def __init__(self, loader) -> None: ...
    def get_current_language(self, shortname) -> None: ...
    def search(self, shortname, text, settings): ...
    @staticmethod
    def set_relative_base(substring, already_parsed): ...
    def choose_best_split(self, possible_parsed_splits, possible_substrings_splits): ...
    def split_by(self, item, original, splitter): ...
    def split_if_not_parsed(self, item, original): ...
    def parse_item(self, parser, item, translated_item, parsed, need_relative_base): ...
    def parse_found_objects(self, parser, to_parse, original, translated, settings): ...
    def search_parse(self, shortname, text, settings): ...

class DateSearchWithDetection:
    """
    Class which executes language detection of string in a natural language, translation of a given string,
    search of substrings which represent date and/or time and parsing of these substrings.

    """

    loader: Any
    available_language_map: Any
    search: Any
    def __init__(self) -> None: ...
    language_detector: Any
    def detect_language(
        self, text, languages, settings=None, detect_languages_function: _DetectLanguagesFunction | None = None
    ): ...
    def search_dates(
        self, text, languages=None, settings=None, detect_languages_function: _DetectLanguagesFunction | None = None
    ):
        """
        Find all substrings of the given string which represent date and/or time and parse them.

        :param text:
            A string in a natural language which may contain date and/or time expressions.
        :type text: str

        :param languages:
            A list of two letters language codes.e.g. ['en', 'es']. If languages are given, it will not attempt
            to detect the language.
        :type languages: list

        :param settings:
               Configure customized behavior using settings defined in :mod:`dateparser.conf.Settings`.
        :type settings: dict

        :param detect_languages_function:
               A function for language detection that takes as input a `text` and a `confidence_threshold`,
               returns a list of detected language codes.
        :type detect_languages_function: function

        :return: a dict mapping keys to two letter language code and a list of tuples of pairs:
                substring representing date expressions and corresponding :mod:`datetime.datetime` object.
            For example:
            {'Language': 'en', 'Dates': [('on 4 October 1957', datetime.datetime(1957, 10, 4, 0, 0))]}
            If language of the string isn't recognised returns:
            {'Language': None, 'Dates': None}
        :raises: ValueError - Unknown Language
        """

    def preprocess_text(self, text: str, languages: Collection[str]) -> str:
        """Preprocess text to handle language-specific quirks."""
