from _typeshed import Incomplete

from reportlab.graphics.barcode.common import Barcode

class _Code39Base(Barcode):
    barWidth: Incomplete
    lquiet: Incomplete
    rquiet: Incomplete
    quiet: int
    gap: Incomplete
    barHeight: Incomplete
    ratio: float
    checksum: int
    bearers: float
    stop: int
    def __init__(self, value: str = "", **args) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...

class Standard39(_Code39Base):
    """
    Options that may be passed to constructor:

        value (int, or numeric string required.):
            The value to encode.

        barWidth (float, default .0075):
            X-Dimension, or width of the smallest element
            Minumum is .0075 inch (7.5 mils).

        ratio (float, default 2.2):
            The ratio of wide elements to narrow elements.
            Must be between 2.0 and 3.0 (or 2.2 and 3.0 if the
            barWidth is greater than 20 mils (.02 inch))

        gap (float or None, default None):
            width of intercharacter gap. None means "use barWidth".

        barHeight (float, see default below):
            Height of the symbol.  Default is the height of the two
            bearer bars (if they exist) plus the greater of .25 inch
            or .15 times the symbol's length.

        checksum (bool, default 1):
            Wether to compute and include the check digit

        bearers (float, in units of barWidth. default 0):
            Height of bearer bars (horizontal bars along the top and
            bottom of the barcode). Default is 0 (no bearers).

        quiet (bool, default 1):
            Wether to include quiet zones in the symbol.

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or .15 times the symbol's
            length.

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

        stop (bool, default 1):
            Whether to include start/stop symbols.

    Sources of Information on Code 39:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/code_39.html
    http://www.adams1.com/pub/russadam/39code.html
    http://www.barcodeman.com/c39_1.html

    Official Spec, "ANSI/AIM BC1-1995, USS" is available for US$45 from
    http://www.aimglobal.org/aimstore/
    """

    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self): ...

class Extended39(_Code39Base):
    """
    Extended Code 39 is a convention for encoding additional characters
    not present in stanmdard Code 39 by using pairs of characters to
    represent the characters missing in Standard Code 39.

    See Standard39 for arguments.

    Sources of Information on Extended Code 39:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/xcode_39.html
    http://www.barcodeman.com/c39_ext.html
    """

    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: str
    def encode(self): ...
