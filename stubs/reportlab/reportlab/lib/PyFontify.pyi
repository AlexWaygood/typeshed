"""
Module to analyze Python source code; for syntax coloring tools.

Interface::

    tags = fontify(pytext, searchfrom, searchto)

 - The 'pytext' argument is a string containing Python source code.
 - The (optional) arguments 'searchfrom' and 'searchto' may contain a slice in pytext.
 - The returned value is a list of tuples, formatted like this::
    [('keyword', 0, 6, None), ('keyword', 11, 17, None), ('comment', 23, 53, None), etc. ]

 - The tuple contents are always like this::
    (tag, startindex, endindex, sublist)

 - tag is one of 'keyword', 'string', 'comment' or 'identifier'
 - sublist is not used, hence always None.
"""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

def replace(src, sep, rep): ...

keywordsList: Incomplete
commentPat: str
pat: str
quotePat: Incomplete
tripleQuotePat: Incomplete
nonKeyPat: str
keyPat: Incomplete
matchPat: Incomplete
matchRE: Incomplete
idKeyPat: str
idRE: Incomplete

def fontify(pytext, searchfrom: int = 0, searchto=None): ...
def test(path) -> None: ...
