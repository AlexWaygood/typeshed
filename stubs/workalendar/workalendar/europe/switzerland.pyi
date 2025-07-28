from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Switzerland(WesternCalendar):
    """Switzerland"""

    include_good_friday: ClassVar[bool]
    include_easter_sunday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_ascension: ClassVar[bool]
    include_whit_sunday: ClassVar[bool]
    include_whit_monday: ClassVar[bool]
    include_christmas: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    include_epiphany: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    include_berchtolds_day: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def has_berchtolds_day(self, year): ...
    def get_federal_thanksgiving_monday(self, year):
        """Monday following the 3rd sunday of September"""

    def get_variable_days(self, year): ...

class Aargau(Switzerland):
    """Aargau"""

    include_berchtolds_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class AppenzellInnerrhoden(Switzerland):
    """Appenzell Innerrhoden"""

    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class AppenzellAusserrhoden(Switzerland):
    """Appenzell Ausserrhoden"""

    include_labour_day: ClassVar[bool]

class Bern(Switzerland):
    """Bern"""

    include_berchtolds_day: ClassVar[bool]

class BaselLandschaft(Switzerland):
    """Basel-Landschaft"""

    include_labour_day: ClassVar[bool]

class BaselStadt(Switzerland):
    """Basel-Stadt"""

    include_labour_day: ClassVar[bool]

class Fribourg(Switzerland):
    """Fribourg"""

    include_berchtolds_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Geneva(Switzerland):
    """Geneva"""

    include_boxing_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def get_genevan_fast(self, year):
        """Thursday following the first Sunday of September"""

    def get_variable_days(self, year): ...

class Glarus(Switzerland):
    """Glarus (Glaris)"""

    include_berchtolds_day: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete

class Graubunden(Switzerland):
    """Graubünden (Grisons)"""

    include_epiphany: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Jura(Switzerland):
    """Jura"""

    include_berchtolds_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete

class Luzern(Switzerland):
    """Luzern"""

    include_berchtolds_day: ClassVar[bool]
    include_epiphany: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Neuchatel(Switzerland):
    """Neuchâtel"""

    include_boxing_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete
    def has_berchtolds_day(self, year): ...
    def get_variable_days(self, year): ...

class Nidwalden(Switzerland):
    """Nidwalden"""

    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Obwalden(Switzerland):
    """Obwalden"""

    include_berchtolds_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete

class StGallen(Switzerland):
    """St. Gallen"""

    include_all_saints: ClassVar[bool]

class Schaffhausen(Switzerland):
    """Schaffhausen"""

    include_berchtolds_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]

class Solothurn(Switzerland):
    """Solothurn"""

    include_berchtolds_day: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Schwyz(Switzerland):
    """Schwyz"""

    include_epiphany: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Thurgau(Switzerland):
    """Thurgau"""

    include_berchtolds_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]

class Ticino(Switzerland):
    """Ticino"""

    include_good_friday: ClassVar[bool]
    include_epiphany: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    FIXED_HOLIDAYS: Incomplete

class Uri(Switzerland):
    """Uri"""

    include_epiphany: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Vaud(Switzerland):
    """Vaud"""

    include_berchtolds_day: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    def get_variable_days(self, year): ...

class Valais(Switzerland):
    """Valais"""

    include_good_friday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]
    include_whit_monday: ClassVar[bool]
    include_st_josephs_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    include_boxing_day: ClassVar[bool]

class Zug(Switzerland):
    """Zug"""

    include_berchtolds_day: ClassVar[bool]
    include_corpus_christi: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]

class Zurich(Switzerland):
    """Zürich"""

    include_berchtolds_day: ClassVar[bool]
    include_labour_day: ClassVar[bool]
