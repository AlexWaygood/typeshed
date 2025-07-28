from typing import Literal

def fp_str(*a):
    """convert separate arguments (or single sequence arg) into space separated numeric strings"""

def unicode2T1(utext, fonts):
    """return a list of (font,string) pairs representing the unicode text"""

def instanceStringWidthT1(self, text: str, size: float, encoding: str = "utf8") -> float:
    """This is the "purist" approach to width"""

def instanceStringWidthTTF(self, text: str, size: float, encoding: str = "utf8") -> float:
    """Calculate text width"""

def hex32(i) -> str: ...
def add32(x: int, y: int) -> int:
    """Calculate (x + y) modulo 2**32"""

def calcChecksum(data: str | bytes) -> int:
    """Calculates TTF-style checksums"""

def escapePDF(s): ...
def asciiBase85Encode(input: str) -> str:
    """Encodes input using ASCII-Base85 coding.

    This is a compact encoding used for binary data within
    a PDF file.  Four bytes of binary data become five bytes of
    ASCII.  This is the default method used for encoding images.
    """

def asciiBase85Decode(input):
    """Decodes input using ASCII-Base85 coding.

    This is not normally used - Acrobat Reader decodes for you
    - but a round trip is essential for testing.
    """

def sameFrag(f, g) -> bool | Literal[0]: ...

__all__ = [
    "fp_str",
    "unicode2T1",
    "instanceStringWidthT1",
    "instanceStringWidthTTF",
    "asciiBase85Encode",
    "asciiBase85Decode",
    "escapePDF",
    "sameFrag",
    "calcChecksum",
    "add32",
    "hex32",
]
