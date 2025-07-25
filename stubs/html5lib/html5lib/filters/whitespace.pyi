import re

from . import base

spaceCharacters: str
SPACES_REGEX: re.Pattern[str]

class Filter(base.Filter):
    """Collapses whitespace except in pre, textarea, and script elements"""

    spacePreserveElements: frozenset[str]
    def __iter__(self): ...

def collapse_spaces(text: str) -> str: ...
