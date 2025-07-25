from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Colombia(WesternCalendar):
    """Colombia"""

    FIXED_HOLIDAYS: Incomplete
    include_labour_day: ClassVar[bool]
    include_palm_sunday: ClassVar[bool]
    include_holy_thursday: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    def get_epiphany(self, year):
        """
        Epiphany is shifted in Colombia
        """

    def get_saint_joseph(self, year): ...
    def get_ascension(self, year): ...
    def get_corpus_christi(self, year): ...
    def get_sacred_heart(self, year): ...
    def get_saint_peter_and_saint_paul(self, year): ...
    def get_assumption(self, year): ...
    def get_day_of_the_races(self, year):
        """
        Return Day of the Races and Hispanity

        a.k.a. "Día de la Raza"
        Fixed to the next MON after October 12th (Columbus Day)
        """

    def get_all_saints(self, year): ...
    def get_cartagena_independence(self, year):
        """
        Cartagena independance day

        Fixed to the next MON after November 11th.
        """

    def get_variable_days(self, year):
        """
        Return variable holidays for Colombia

        The following days are set to "the next MON after the 'true' date".

        * Epiphany,
        * Saint Joseph,
        * Ascension,
        * Corpus Christi,
        * Sacred Heart,
        * Saint Peter & Saint Paul
        * Assumption
        * Columbus Day / Race Day
        * All Saints
        * Cartagena Independance
        """
