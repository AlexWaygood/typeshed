"""Utilities to associate bold and italic versions of fonts into families

Bold, italic and plain fonts are usually implemented in separate disk files;
but non-trivial apps want <b>this</b> to do the right thing.   We therefore
need to keep 'mappings' between the font family name and the right group
of up to 4 implementation fonts to use.

Most font-handling code lives in pdfbase, and this probably should too.

"""

from typing import Final, Literal
from typing_extensions import TypeAlias

_BoolInt: TypeAlias = Literal[0, 1]

__version__: Final[str]

def ps2tt(psfn: str) -> tuple[str, _BoolInt, _BoolInt]:
    """ps fontname to family name, bold, italic"""

def tt2ps(fn: str, b: _BoolInt, i: _BoolInt) -> str:
    """family name + bold & italic to ps font name"""

def addMapping(face: str, bold: _BoolInt, italic: _BoolInt, psname: str) -> None:
    """allow a custom font to be put in the mapping"""
