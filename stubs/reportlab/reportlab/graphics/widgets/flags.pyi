"""This file is a collection of flag graphics as widgets.

All flags are represented at the ratio of 1:2, even where the official ratio for the flag is something else
(such as 3:5 for the German national flag). The only exceptions are for where this would look _very_ wrong,
such as the Danish flag whose (ratio is 28:37), or the Swiss flag (which is square).

Unless otherwise stated, these flags are all the 'national flags' of the countries, rather than their
state flags, naval flags, ensigns or any other variants. (National flags are the flag flown by civilians
of a country and the ones usually used to represent a country abroad. State flags are the variants used by
the government and by diplomatic missions overseas).

To check on how close these are to the 'official' representations of flags, check the World Flag Database at
http://www.flags.ndirect.co.uk/

The flags this file contains are:

EU Members:
United Kingdom, Austria, Belgium, Denmark, Finland, France, Germany, Greece, Ireland, Italy, Luxembourg,
Holland (The Netherlands), Spain, Sweden

Others:
USA, Czech Republic, European Union, Switzerland, Turkey, Brazil

(Brazilian flag contributed by Publio da Costa Melo [publio@planetarium.com.br]).
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgets.signsandsymbols import _Symbol
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]
validFlag: Incomplete

class Star(_Symbol):
    """This draws a 5-pointed star.

    possible attributes:
    'x', 'y', 'size', 'fillColor', 'strokeColor'

    """

    size: int
    fillColor: Incomplete
    strokeColor: Incomplete
    angle: int
    def __init__(self) -> None: ...
    def demo(self): ...
    def draw(self): ...

class Flag(_Symbol):
    """This is a generic flag class that all the flags in this file use as a basis.

    This class basically provides edges and a tidy-up routine to hide any bits of
    line that overlap the 'outside' of the flag

    possible attributes:
    'x', 'y', 'size', 'fillColor'
    """

    kind: Incomplete
    size: int
    fillColor: Incomplete
    border: int
    def __init__(self, **kw) -> None: ...
    def availableFlagNames(self):
        """return a list of the things we can display"""

    def draw(self): ...
    def clone(self): ...
    def demo(self): ...

def makeFlag(name): ...
def test() -> None:
    """This function produces three pdf files with examples of all the signs and symbols from this file."""
