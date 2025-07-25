from _typeshed import Incomplete

from reportlab.graphics.barcode.common import MultiWidthBarcode

starta: Incomplete
startb: Incomplete
startc: Incomplete
stop: Incomplete
seta: Incomplete
setb: Incomplete
setc: Incomplete
setmap: Incomplete
cStarts: Incomplete
tos: Incomplete

class Code128(MultiWidthBarcode):
    """
    Code 128 is a very compact symbology that can encode the entire
    128 character ASCII set, plus 4 special control codes,
    (FNC1-FNC4, expressed in the input string as ñ to ô).
    Code 128 can also encode digits at double density (2 per byte)
    and has a mandatory checksum.  Code 128 is well supported and
    commonly used -- for example, by UPS for tracking labels.

    Because of these qualities, Code 128 is probably the best choice
    for a linear symbology today (assuming you have a choice).

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

    Sources of Information on Code 128:

    http://www.semiconductor.agilent.com/barcode/sg/Misc/code_128.html
    http://www.adams1.com/pub/russadam/128code.html
    http://www.barcodeman.com/c128.html

    Official Spec, "ANSI/AIM BC4-1999, ISS" is available for US$45 from
    http://www.aimglobal.org/aimstore/
    """

    barWidth: Incomplete
    lquiet: Incomplete
    rquiet: Incomplete
    quiet: int
    barHeight: Incomplete
    def __init__(self, value: str = "", **args) -> None: ...
    valid: int
    validated: Incomplete
    def validate(self): ...
    encoded: Incomplete
    def encode(self): ...
    decomposed: Incomplete
    def decompose(self): ...

class Code128Auto(Code128):
    """contributed by https://bitbucket.org/kylemacfarlane/
    see https://bitbucket.org/rptlab/reportlab/issues/69/implementations-of-code-128-auto-and-data
    """

    encoded: Incomplete
    def encode(self): ...
