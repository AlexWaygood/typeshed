from _typeshed import Incomplete

from reportlab.platypus.flowables import Flowable

class Barcode(Flowable):
    """Abstract Base for barcodes. Includes implementations of
    some methods suitable for the more primitive barcode types
    """

    fontName: str
    fontSize: int
    humanReadable: int
    value: Incomplete
    gap: Incomplete
    def __init__(self, value: str = "", **kwd) -> None: ...
    valid: int
    validated: Incomplete
    def validate(self) -> None: ...
    encoded: Incomplete
    def encode(self) -> None: ...
    decomposed: Incomplete
    def decompose(self) -> None: ...
    barHeight: Incomplete
    def computeSize(self, *args) -> None: ...
    @property
    def width(self): ...
    @width.setter
    def width(self, v) -> None: ...
    @property
    def height(self): ...
    @height.setter
    def height(self, v) -> None: ...
    def draw(self) -> None: ...
    def drawHumanReadable(self) -> None: ...
    def rect(self, x, y, w, h) -> None: ...
    def annotate(self, x, y, text, fontName, fontSize, anchor: str = "middle") -> None: ...

class MultiWidthBarcode(Barcode):
    """Base for variable-bar-width codes like Code93 and Code128"""

    barHeight: Incomplete
    def computeSize(self, *args) -> None: ...
    def draw(self) -> None: ...

class I2of5(Barcode):
    """
    Interleaved 2 of 5 is a numeric-only barcode.  It encodes an even
    number of digits; if an odd number is given, a 0 is prepended.

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
            Whether to compute and include the check digit

        bearers (float, in units of barWidth. default 3.0):
            Height of bearer bars (horizontal bars along the top and
            bottom of the barcode). Default is 3 x-dimensions.
            Set to zero for no bearer bars. (Bearer bars help detect
            misscans, so it is suggested to leave them on).

        bearerBox (bool default False)
            if true draw a  true rectangle of width bearers around the barcode.

        quiet (bool, default 1):
            Whether to include quiet zones in the symbol.

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or .15 times the symbol's
            length.

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

        stop (bool, default 1):
            Whether to include start/stop symbols.

    Sources of Information on Interleaved 2 of 5:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/i_25.html
    http://www.adams1.com/pub/russadam/i25code.html

    Official Spec, "ANSI/AIM BC2-1995, USS" is available for US$45 from
    http://www.aimglobal.org/aimstore/
    """

    patterns: Incomplete
    barHeight: Incomplete
    barWidth: Incomplete
    ratio: float
    checksum: int
    bearers: float
    bearerBox: bool
    quiet: int
    lquiet: Incomplete
    rquiet: Incomplete
    stop: int
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...

class MSI(Barcode):
    """
    MSI is a numeric-only barcode.

    Options that may be passed to constructor:

        value (int, or numeric string required.):
            The value to encode.

        barWidth (float, default .0075):
            X-Dimension, or width of the smallest element

        ratio (float, default 2.2):
            The ratio of wide elements to narrow elements.

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

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or 10 barWidths.

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

        stop (bool, default 1):
            Whether to include start/stop symbols.

    Sources of Information on MSI Bar Code:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/msi_code.html
    http://www.adams1.com/pub/russadam/plessy.html
    """

    patterns: Incomplete
    stop: int
    barHeight: Incomplete
    barWidth: Incomplete
    ratio: float
    checksum: int
    bearers: float
    quiet: int
    lquiet: Incomplete
    rquiet: Incomplete
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...

class Codabar(Barcode):
    """
    Codabar is a numeric plus some puntuation ("-$:/.+") barcode
    with four start/stop characters (A, B, C, and D).

    Options that may be passed to constructor:

        value (string required.):
            The value to encode.

        barWidth (float, default .0065):
            X-Dimension, or width of the smallest element
            minimum is 6.5 mils (.0065 inch)

        ratio (float, default 2.0):
            The ratio of wide elements to narrow elements.

        gap (float or None, default None):
            width of intercharacter gap. None means "use barWidth".

        barHeight (float, see default below):
            Height of the symbol.  Default is the height of the two
            bearer bars (if they exist) plus the greater of .25 inch
            or .15 times the symbol's length.

        checksum (bool, default 0):
            Whether to compute and include the check digit

        bearers (float, in units of barWidth. default 0):
            Height of bearer bars (horizontal bars along the top and
            bottom of the barcode). Default is 0 (no bearers).

        quiet (bool, default 1):
            Whether to include quiet zones in the symbol.

        stop (bool, default 1):
            Whether to include start/stop symbols.

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or 10 barWidth

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

    Sources of Information on Codabar

    http://www.semiconductor.agilent.com/barcode/sg/Misc/codabar.html
    http://www.barcodeman.com/codabar.html

    Official Spec, "ANSI/AIM BC3-1995, USS" is available for US$45 from
    http://www.aimglobal.org/aimstore/
    """

    patterns: Incomplete
    values: Incomplete
    chars: Incomplete
    stop: int
    barHeight: Incomplete
    barWidth: Incomplete
    ratio: float
    checksum: int
    bearers: float
    quiet: int
    lquiet: Incomplete
    rquiet: Incomplete
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    Valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...

class Code11(Barcode):
    """
    Code 11 is an almost-numeric barcode. It encodes the digits 0-9 plus
    dash ("-"). 11 characters total, hence the name.

        value (int or string required.):
            The value to encode.

        barWidth (float, default .0075):
            X-Dimension, or width of the smallest element

        ratio (float, default 2.2):
            The ratio of wide elements to narrow elements.

        gap (float or None, default None):
            width of intercharacter gap. None means "use barWidth".

        barHeight (float, see default below):
            Height of the symbol.  Default is the height of the two
            bearer bars (if they exist) plus the greater of .25 inch
            or .15 times the symbol's length.

        checksum (0 none, 1 1-digit, 2 2-digit, -1 auto, default -1):
            How many checksum digits to include. -1 ("auto") means
            1 if the number of digits is 10 or less, else 2.

        bearers (float, in units of barWidth. default 0):
            Height of bearer bars (horizontal bars along the top and
            bottom of the barcode). Default is 0 (no bearers).

        quiet (bool, default 1):
            Wether to include quiet zones in the symbol.

        lquiet (float, see default below):
            Quiet zone size to left of code, if quiet is true.
            Default is the greater of .25 inch, or 10 barWidth

        rquiet (float, defaults as above):
            Quiet zone size to right left of code, if quiet is true.

    Sources of Information on Code 11:

    http://www.cwi.nl/people/dik/english/codes/barcodes.html
    """

    chars: str
    patterns: Incomplete
    values: Incomplete
    stop: int
    barHeight: Incomplete
    barWidth: Incomplete
    ratio: float
    checksum: int
    bearers: float
    quiet: int
    lquiet: Incomplete
    rquiet: Incomplete
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    Valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self) -> None: ...
    decomposed: Incomplete
    def decompose(self): ...
