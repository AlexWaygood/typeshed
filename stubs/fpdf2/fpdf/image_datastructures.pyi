from _typeshed import Incomplete
from dataclasses import dataclass
from typing import Any, Literal
from typing_extensions import TypeAlias

from fpdf.enums import Align

from .image_parsing import _ImageFilter

_AlignLiteral: TypeAlias = Literal[
    "",
    "CENTER",
    "X_CENTER",
    "LEFT",
    "RIGHT",
    "JUSTIFY",
    "center",
    "x_center",
    "left",
    "right",
    "justify",
    "C",
    "X",
    "L",
    "R",
    "J",
    "c",
    "x",
    "l",
    "r",
    "j",
]
_TextAlign: TypeAlias = Align | _AlignLiteral  # noqa: Y047

class ImageInfo(dict[str, Any]):
    """Information about an image used in the PDF document (base class).
    We subclass this to distinguish between raster and vector images.
    """

    @property
    def width(self) -> int:
        """Intrinsic image width"""

    @property
    def height(self) -> int:
        """Intrinsic image height"""

    @property
    def rendered_width(self) -> int:
        """Only available if the image has been placed on the document"""

    @property
    def rendered_height(self) -> int:
        """Only available if the image has been placed on the document"""

    def scale_inside_box(self, x: float, y: float, w: float, h: float) -> tuple[float, float, float, float]:
        """
        Make an image fit within a bounding box, maintaining its proportions.
        In the reduced dimension it will be centered within the available space.
        """

class RasterImageInfo(ImageInfo):
    """Information about a raster image used in the PDF document"""

    def size_in_document_units(self, w: float, h: float, scale=1) -> tuple[float, float]: ...

class VectorImageInfo(ImageInfo):
    """Information about a vector image used in the PDF document"""

@dataclass
class ImageCache:
    """ImageCache(images: Dict[str, dict] = <factory>, icc_profiles: Dict[bytes, int] = <factory>, image_filter: str = 'AUTO')"""

    images: dict[str, dict[Incomplete, Incomplete]] = ...
    icc_profiles: dict[bytes, int] = ...
    image_filter: _ImageFilter = "AUTO"

    def reset_usages(self) -> None: ...
