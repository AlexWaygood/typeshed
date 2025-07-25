from _typeshed import Incomplete

from reportlab.graphics.barcode.common import MultiWidthBarcode

class _Code93Base(MultiWidthBarcode):
    barWidth: Incomplete
    lquiet: Incomplete
    rquiet: Incomplete
    quiet: int
    barHeight: Incomplete
    stop: int
    def __init__(self, value: str = "", **args) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...

class Standard93(_Code93Base):
    """
    Code 93 is a Uppercase alphanumeric symbology with some punctuation.
    See Extended Code 93 for a variant that can represent the entire
    128 characrter ASCII set.

    Options that may be passed to constructor:

        value (int, or numeric string. required.):
            The value to encode.

        barWidth (float, default .0075):
            X-Dimension, or width of the smallest element
            Minumum is .0075 inch (7.5 mils).

        barHeight (float, see default below):
            Height of the symbol.  Default is the height of the two
            bearer bars (if they exist) plus the greater of .25 inch
            or .15 times the symbol's length.

        quiet (bool, default 1):
            Wether to include quiet zones in the symbol.

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or 10 barWidth

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

        stop (bool, default 1):
            Whether to include start/stop symbols.

    Sources of Information on Code 93:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/code_93.html

    Official Spec, "NSI/AIM BC5-1995, USS" is available for US$45 from
    http://www.aimglobal.org/aimstore/
    """

    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self): ...

class Extended93(_Code93Base):
    """
    Extended Code 93 is a convention for encoding the entire 128 character
    set using pairs of characters to represent the characters missing in
    Standard Code 93. It is very much like Extended Code 39 in that way.

    See Standard93 for arguments.
    """

    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: str
    def encode(self): ...
