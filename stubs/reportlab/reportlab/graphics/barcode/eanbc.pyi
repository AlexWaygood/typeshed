from _typeshed import Incomplete

from reportlab.graphics.charts.areas import PlotArea
from reportlab.lib.attrmap import *

class Ean13BarcodeWidget(PlotArea):
    codeName: str
    barHeight: Incomplete
    barWidth: Incomplete
    humanReadable: int
    quiet: int
    rquiet: Incomplete
    lquiet: Incomplete
    fontSize: int
    fontName: str
    textColor: Incomplete
    barFillColor: Incomplete
    barStrokeColor: Incomplete
    barStrokeWidth: int
    x: int
    y: int
    value: Incomplete
    def __init__(self, value: str = "123456789012", **kw) -> None: ...
    @property
    def width(self): ...  # type: ignore[override]
    def wrap(self, aW, aH): ...
    def draw(self): ...

class Ean8BarcodeWidget(Ean13BarcodeWidget):
    codeName: str

class UPCA(Ean13BarcodeWidget):
    codeName: str

class Ean5BarcodeWidget(Ean13BarcodeWidget):
    """
    EAN-5 barcodes can print the human readable price, set:
        price=True
    """

    codeName: str
    def draw(self): ...

class ISBNBarcodeWidget(Ean13BarcodeWidget):
    """
    ISBN Barcodes optionally print the EAN-5 supplemental price
    barcode (with the price in dollars or pounds). Set price to a string
    that follows the EAN-5 for ISBN spec:

        leading digit 0, 1 = GBP
                      3    = AUD
                      4    = NZD
                      5    = USD
                      6    = CAD
        next 4 digits = price between 00.00 and 99.98, i.e.:

        price='52499' # $24.99 USD
    """

    codeName: str
    def draw(self): ...

__all__ = ("Ean13BarcodeWidget", "Ean8BarcodeWidget", "UPCA", "Ean5BarcodeWidget", "ISBNBarcodeWidget")
