"""
pygments.regexopt
~~~~~~~~~~~~~~~~~

An algorithm that generates optimized regexes for matching long lists of
literal strings.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any

CS_ESCAPE: Any
FIRST_ELEMENT: Any

def make_charset(letters): ...
def regex_opt_inner(strings, open_paren):
    """Return a regex that matches any string in the sorted list of strings."""

def regex_opt(strings, prefix: str = "", suffix: str = ""):
    """Return a compiled regex that matches any string in the given list.

    The strings to match must be literal strings, not regexes.  They will be
    regex-escaped.

    *prefix* and *suffix* are pre- and appended to the final regex.
    """
