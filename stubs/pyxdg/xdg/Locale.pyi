"""
Helper Module for Locale settings

This module is based on a ROX module (LGPL):

http://cvs.sourceforge.net/viewcvs.py/rox/ROX-Lib2/python/rox/i18n.py?rev=1.3&view=log
"""

from collections.abc import Iterable

regex: str

def expand_languages(languages: Iterable[str] | None = None) -> list[str]: ...
def update(language: str | None = None) -> None: ...

langs: list[str]
