import re
from collections import OrderedDict
from collections.abc import Iterator
from typing import Any, Final

from .locale import Locale

LOCALE_SPLIT_PATTERN: Final[re.Pattern[str]]

class LocaleDataLoader:
    """Class that handles loading of locale instances."""

    def get_locale_map(
        self,
        languages: list[str] | None = None,
        locales: list[str] | None = None,
        region: str | None = None,
        use_given_order: bool = False,
        allow_conflicting_locales: bool = False,
    ) -> OrderedDict[str, list[Any] | str | int]:
        """
        Get an ordered mapping with locale codes as keys
        and corresponding locale instances as values.

        :param languages:
            A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
            If locales are not given, languages and region are
            used to construct locales to load.
        :type languages: list

        :param locales:
            A list of codes of locales which are to be loaded,
            e.g. ['fr-PF', 'qu-EC', 'af-NA']
        :type locales: list

        :param region:
            A region code, e.g. 'IN', '001', 'NE'.
            If locales are not given, languages and region are
            used to construct locales to load.
        :type region: str

        :param use_given_order:
            If True, the returned mapping is ordered in the order locales are given.
        :type use_given_order: bool

        :param allow_conflicting_locales:
            if True, locales with same language and different region can be loaded.
        :type allow_conflicting_locales: bool

        :return: ordered locale code to locale instance mapping
        """

    def get_locales(
        self,
        languages: list[str] | None = None,
        locales: list[str] | None = None,
        region: str | None = None,
        use_given_order: bool = False,
        allow_conflicting_locales: bool = False,
    ) -> Iterator[Locale]:
        """
        Yield locale instances.

        :param languages:
            A list of language codes, e.g. ['en', 'es', 'zh-Hant'].
            If locales are not given, languages and region are
            used to construct locales to load.
        :type languages: list

        :param locales:
            A list of codes of locales which are to be loaded,
            e.g. ['fr-PF', 'qu-EC', 'af-NA']
        :type locales: list

        :param region:
            A region code, e.g. 'IN', '001', 'NE'.
            If locales are not given, languages and region are
            used to construct locales to load.
        :type region: str

        :param use_given_order:
            If True, the returned mapping is ordered in the order locales are given.
        :type use_given_order: bool

        :param allow_conflicting_locales:
            if True, locales with same language and different region can be loaded.
        :type allow_conflicting_locales: bool

        :yield: locale instances
        """

    def get_locale(self, shortname: str) -> Locale:
        """
        Get a locale instance.

        :param shortname:
            A locale code, e.g. 'fr-PF', 'qu-EC', 'af-NA'.
        :type shortname: str

        :return: locale instance
        """

default_loader: LocaleDataLoader
