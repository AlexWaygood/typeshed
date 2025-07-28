"""
Image functionality sliced out of canvas.py for generalization
"""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

class PDFImage:
    """Wrapper around different "image sources".  You can make images
    from a PIL Image object, a filename (in which case it uses PIL),
    an image we previously cached (optimisation, hardly used these
    days) or a JPEG (which PDF supports natively).
    """

    image: Incomplete
    x: Incomplete
    y: Incomplete
    width: Incomplete
    height: Incomplete
    filename: Incomplete
    imageCaching: Incomplete
    colorSpace: str
    bitsPerComponent: int
    filters: Incomplete
    source: Incomplete
    def __init__(self, image, x, y, width=None, height=None, caching: int = 0) -> None: ...
    def jpg_imagedata(self): ...
    def cache_imagedata(self): ...
    def PIL_imagedata(self): ...
    def non_jpg_imagedata(self, image): ...
    imageData: Incomplete
    imgwidth: Incomplete
    imgheight: Incomplete
    def getImageData(self, preserveAspectRatio: bool = False) -> None:
        """Gets data, height, width - whatever type of image"""

    def drawInlineImage(
        self,
        canvas,
        preserveAspectRatio: bool = False,
        anchor: str = "sw",
        anchorAtXY: bool = False,
        showBoundary: bool = False,
        extraReturn=None,
    ):
        """Draw an Image into the specified rectangle.  If width and
        height are omitted, they are calculated from the image size.
        Also allow file names as well as images.  This allows a
        caching mechanism
        """

    def format(self, document):
        """Allow it to be used within pdfdoc framework.  This only
        defines how it is stored, not how it is drawn later.
        """
