from _typeshed import Incomplete
from typing import ClassVar

from ..core import WesternCalendar

class Spain(WesternCalendar):
    """Spain"""

    include_epiphany: ClassVar[bool]
    include_good_friday: ClassVar[bool]
    include_assumption: ClassVar[bool]
    include_all_saints: ClassVar[bool]
    include_immaculate_conception: ClassVar[bool]
    include_labour_day: ClassVar[bool]
    labour_day_label: ClassVar[str]
    FIXED_HOLIDAYS: Incomplete

class Andalusia(Spain):
    """Andalusia"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class Aragon(Spain):
    """Aragon"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class CastileAndLeon(Spain):
    """Castile and León"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class CastillaLaMancha(Spain):
    """Castilla-La Mancha"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class CanaryIslands(Spain):
    """Canary Islands"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class Catalonia(Spain):
    """Catalonia"""

    include_easter_monday: ClassVar[bool]
    include_boxing_day: ClassVar[bool]
    boxing_day_label: ClassVar[str]
    FIXED_HOLIDAYS: Incomplete

class Extremadura(Spain):
    """Extremadura"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class Galicia(Spain):
    """Galicia"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class BalearicIslands(Spain):
    """Balearic Islands"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class LaRioja(Spain):
    """La Rioja"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class CommunityofMadrid(Spain):
    """Community of Madrid"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class Murcia(Spain):
    """Region of Murcia"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class Navarre(Spain):
    """Navarre"""

    include_holy_thursday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Asturias(Spain):
    """Asturias"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class BasqueCountry(Spain):
    """Basque Country"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]
    include_easter_monday: ClassVar[bool]

class Cantabria(Spain):
    """Cantabria"""

    FIXED_HOLIDAYS: Incomplete
    include_holy_thursday: ClassVar[bool]

class ValencianCommunity(Spain):
    """Valencian Community"""

    FIXED_HOLIDAYS: Incomplete
    include_easter_monday: ClassVar[bool]
