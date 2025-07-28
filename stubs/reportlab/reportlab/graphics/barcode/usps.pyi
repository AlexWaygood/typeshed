from _typeshed import Incomplete

from reportlab.graphics.barcode.common import Barcode

class FIM(Barcode):
    """
    FIM (Facing ID Marks) encode only one letter.
    There are currently four defined:

    A   Courtesy reply mail with pre-printed POSTNET
    B   Business reply mail without pre-printed POSTNET
    C   Business reply mail with pre-printed POSTNET
    D   OCR Readable mail without pre-printed POSTNET

    Options that may be passed to constructor:

        value (single character string from the set A - D. required.):
            The value to encode.

        quiet (bool, default 0):
            Whether to include quiet zones in the symbol.

    The following may also be passed, but doing so will generate nonstandard
    symbols which should not be used. This is mainly documented here to
    show the defaults:

        barHeight (float, default 5/8 inch):
            Height of the code. This might legitimately be overriden to make
            a taller symbol that will 'bleed' off the edge of the paper,
            leaving 5/8 inch remaining.

        lquiet (float, default 1/4 inch):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or .15 times the symbol's
            length.

        rquiet (float, default 15/32 inch):
            Quiet zone size to right left of code, if quiet is true.

    Sources of information on FIM:

    USPS Publication 25, A Guide to Business Mail Preparation
    http://new.usps.com/cpim/ftp/pubs/pub25.pdf
    """

    barWidth: Incomplete
    spaceWidth: Incomplete
    barHeight: Incomplete
    rquiet: Incomplete
    lquiet: Incomplete
    quiet: int
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    validated: str
    def validate(self): ...
    decomposed: str
    def decompose(self): ...
    def computeSize(self) -> None: ...
    def draw(self) -> None: ...

class POSTNET(Barcode):
    """
    POSTNET is used in the US to encode "zip codes" (postal codes) on
    mail. It can encode 5, 9, or 11 digit codes. I've read that it's
    pointless to do 5 digits, since USPS will just have to re-print
    them with 9 or 11 digits.

    Sources of information on POSTNET:

    USPS Publication 25, A Guide to Business Mail Preparation
    http://new.usps.com/cpim/ftp/pubs/pub25.pdf
    """

    quiet: int
    shortHeight: Incomplete
    barHeight: Incomplete
    barWidth: Incomplete
    spaceWidth: Incomplete
    def __init__(self, value: str = "", **args) -> None: ...
    validated: str
    valid: int
    def validate(self): ...
    encoded: str
    def encode(self): ...
    decomposed: str
    def decompose(self): ...
    def computeSize(self) -> None: ...
    def draw(self) -> None: ...
