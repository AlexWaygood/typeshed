from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Germany(WesternCalendar):
    """Germany"""

    include_labour_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    include_easter_monday: ClassVar[bool]
    include_ascension: ClassVar[bool]
    include_whit_monday: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    boxing_day_label: ClassVar[str]
    all_time_include_reformation_day: ClassVar[bool]
    include_reformation_day_2018: ClassVar[bool]
    def include_reformation_day(self, year):
        """
        Return True if the Reformation Day is a holiday.
        """

    def get_reformation_day(self, year):
        """
        Reformation Day is a fixed date.

        It's handled via the variable_days because it can be activated
        depending on the Länder or the year (see #150).
        """

    def get_variable_days(self, year): ...

class BadenWurttemberg(Germany):
    """Baden-Wuerttemberg"""

    include_epiphany: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_all_saints: ClassVar[bool]

class Bavaria(Germany):
    """Bavaria"""

    include_epiphany: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_assumption: ClassVar[bool]

class Berlin(Germany):
    """Berlin"""

    def get_international_womens_day(self, year): ...
    def get_liberation_day(self, year): ...
    def get_variable_days(self, year): ...

class Brandenburg(Germany):
    """Brandenburg"""

    include_easter_sunday: ClassVar[bool]
    all_time_include_reformation_day: ClassVar[bool]

class Bremen(Germany):
    """Bremen"""

    include_reformation_day_2018: ClassVar[bool]

class Hamburg(Germany):
    """Hamburg"""

    include_reformation_day_2018: ClassVar[bool]

class Hesse(Germany):
    """Hesse"""

    include_corpus_christi: ClassVar[bool]

class MecklenburgVorpommern(Germany):
    """Mecklenburg-Western Pomerania"""

    all_time_include_reformation_day: ClassVar[bool]

class LowerSaxony(Germany):
    """Lower Saxony"""

    include_reformation_day_2018: ClassVar[bool]

class NorthRhineWestphalia(Germany):
    """North Rhine-Westphalia"""

    include_corpus_christi: ClassVar[bool]
    include_all_saints: ClassVar[bool]

class RhinelandPalatinate(Germany):
    """Rhineland-Palatinate"""

    include_corpus_christi: ClassVar[bool]
    include_all_saints: ClassVar[bool]

class Saarland(Germany):
    """Saarland"""

    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]

class Saxony(Germany):
    """Saxony"""

    all_time_include_reformation_day: ClassVar[bool]
    def get_repentance_day(self, year):
        """Wednesday before November 23"""

    def get_variable_days(self, year): ...

class SaxonyAnhalt(Germany):
    """Saxony-Anhalt"""

    include_epiphany: ClassVar[bool]
    all_time_include_reformation_day: ClassVar[bool]

class SchleswigHolstein(Germany):
    """Schleswig-Holstein"""

    include_reformation_day_2018: ClassVar[bool]

class Thuringia(Germany):
    """Thuringia"""

    all_time_include_reformation_day: ClassVar[bool]
