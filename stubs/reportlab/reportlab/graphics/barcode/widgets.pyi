from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.charts.areas import PlotArea
from reportlab.lib.colors import black

class _BarcodeWidget(PlotArea):
    textColor = black
    barFillColor = black
    barStrokeColor: Incomplete
    barStrokeWidth: int
    x: int
    def __init__(self, _value: str = "", **kw) -> None: ...
    def rect(self, x, y, w, h, **kw) -> None: ...
    canv: Incomplete
    def draw(self): ...
    def annotate(self, x, y, text, fontName, fontSize, anchor: str = "middle") -> None: ...

class BarcodeI2of5(_BarcodeWidget):
    """Interleaved 2 of 5 is used in distribution and warehouse industries.

    It encodes an even-numbered sequence of numeric digits. There is an optional
    module 10 check digit; if including this, the total length must be odd so that
    it becomes even after including the check digit.  Otherwise the length must be
    even. Since the check digit is optional, our library does not check it.
    """

    codeName: Final = "I2of5"
    def __init__(self, **kw) -> None: ...

class BarcodeCode128(_BarcodeWidget):
    """Code 128 encodes any number of characters in the ASCII character set."""

    codeName: Final = "Code128"
    def __init__(self, **kw) -> None: ...

class BarcodeStandard93(_BarcodeWidget):
    """This is a compressed form of Code 39"""

    codeName: Final = "Standard93"
    def __init__(self, **kw) -> None: ...

class BarcodeExtended93(_BarcodeWidget):
    """This is a compressed form of Code 39, allowing the full ASCII charset"""

    codeName: Final = "Extended93"
    def __init__(self, **kw) -> None: ...

class BarcodeStandard39(_BarcodeWidget):
    """Code39 is widely used in non-retail, especially US defence and health.
    Allowed characters are 0-9, A-Z (caps only), space, and -.$/+%*.
    """

    codeName: Final = "Standard39"
    def __init__(self, **kw) -> None: ...

class BarcodeExtended39(_BarcodeWidget):
    """Extended 39 encodes the full ASCII character set by encoding
    characters as pairs of Code 39 characters; $, /, % and + are used as
    shift characters.
    """

    codeName: Final = "Extended39"
    def __init__(self, **kw) -> None: ...

class BarcodeMSI(_BarcodeWidget):
    """MSI is used for inventory control in retail applications.

    There are several methods for calculating check digits so we
    do not implement one.
    """

    codeName: Final = "MSI"
    def __init__(self, **kw) -> None: ...

class BarcodeCodabar(_BarcodeWidget):
    """Used in blood banks, photo labs and FedEx labels.
    Encodes 0-9, -$:/.+, and four start/stop characters A-D.
    """

    codeName: Final = "Codabar"
    def __init__(self, **kw) -> None: ...

class BarcodeCode11(_BarcodeWidget):
    """Used mostly for labelling telecommunications equipment.
    It encodes numeric digits.
    """

    codeName: Final = "Code11"
    def __init__(self, **kw) -> None: ...

class BarcodeFIM(_BarcodeWidget):
    """
    FIM was developed as part of the POSTNET barcoding system.
    FIM (Face Identification Marking) is used by the cancelling machines
    to sort mail according to whether or not they have bar code
    and their postage requirements. There are four types of FIM
    called FIM A, FIM B, FIM C, and FIM D.

    The four FIM types have the following meanings:
        FIM A- Postage required pre-barcoded
        FIM B - Postage pre-paid, no bar code exists
        FIM C- Postage prepaid prebarcoded
        FIM D- Postage required, no bar code exists
    """

    codeName: Final = "FIM"
    def __init__(self, **kw) -> None: ...

class BarcodePOSTNET(_BarcodeWidget):
    codeName: Final = "POSTNET"
    def __init__(self, **kw) -> None: ...

class BarcodeUSPS_4State(_BarcodeWidget):
    codeName: Final = "USPS_4State"
    def __init__(self, **kw) -> None: ...

__all__ = (
    "BarcodeI2of5",
    "BarcodeCode128",
    "BarcodeStandard93",
    "BarcodeExtended93",
    "BarcodeStandard39",
    "BarcodeExtended39",
    "BarcodeMSI",
    "BarcodeCodabar",
    "BarcodeCode11",
    "BarcodeFIM",
    "BarcodePOSTNET",
    "BarcodeUSPS_4State",
)
