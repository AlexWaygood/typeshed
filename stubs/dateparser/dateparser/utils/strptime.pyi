import re
from datetime import datetime
from typing import Any, Final

TIME_MATCHER: Final[re.Pattern[str]]
MS_SEARCHER: Final[re.Pattern[str]]

def patch_strptime() -> Any:
    """Monkey patching _strptime to avoid problems related with non-english
    locale changes on the system.

    For example, if system's locale is set to fr_FR. Parser won't recognize
    any date since all languages are translated to english dates.
    """

def strptime(date_string, format) -> datetime: ...
