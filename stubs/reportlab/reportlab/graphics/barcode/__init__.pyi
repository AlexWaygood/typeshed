"""Popular barcodes available as reusable widgets"""

def registerWidget(widget) -> None: ...
def getCodes():
    """Returns a dict mapping code names to widgets"""

def getCodeNames():
    """Returns sorted list of supported bar code names"""

def createBarcodeDrawing(codeName, **options):
    """This creates and returns a drawing with a barcode."""

def createBarcodeImageInMemory(codeName, **options):
    """This creates and returns barcode as an image in memory.
    Takes same arguments as createBarcodeDrawing and also an
    optional format keyword which can be anything acceptable
    to Drawing.asString eg gif, pdf, tiff, py ......
    """

__all__ = ("registerWidget", "getCodes", "getCodeNames", "createBarcodeDrawing", "createBarcodeImageInMemory")
