from collections.abc import Iterable
from dataclasses import dataclass
from io import BytesIO
from logging import Logger
from types import TracebackType
from typing import Any, Final, Literal
from typing_extensions import TypeAlias

from PIL import Image

from .image_datastructures import ImageCache, ImageInfo, VectorImageInfo
from .svg import SVGObject

_ImageFilter: TypeAlias = Literal["AUTO", "FlateDecode", "DCTDecode", "JPXDecode", "LZWDecode"]

RESAMPLE: Image.Resampling

@dataclass
class ImageSettings:
    """ImageSettings(compression_level: int = -1)"""

    compression_level: int = -1

LOGGER: Logger
SUPPORTED_IMAGE_FILTERS: tuple[_ImageFilter, ...]
SETTINGS: ImageSettings

TIFFBitRevTable: list[int]

LZW_CLEAR_TABLE_MARKER: Final = 256
LZW_EOD_MARKER: Final = 257
LZW_INITIAL_BITS_PER_CODE: Final = 9
LZW_MAX_BITS_PER_CODE: Final = 12

def preload_image(
    image_cache: ImageCache, name: str | BytesIO | Image.Image, dims: tuple[float, float] | None = None
) -> tuple[str, BytesIO | Image.Image | None, ImageInfo]:
    """
    Read an image and load it into memory.

    For raster images: following this call, the image is inserted in `image_cache.images`,
    and following calls to `FPDF.image()` will re-use the same cached values, without re-reading the image.

    For vector images: the data is loaded and the metadata extracted.

    Args:
        image_cache: an `ImageCache` instance, usually the `.image_cache` attribute of a `FPDF` instance.
        name: either a string representing a file path to an image, an URL to an image,
            an io.BytesIO, or a instance of `PIL.Image.Image`.
        dims (Tuple[float]): optional dimensions as a tuple (width, height) to resize the image
            (raster only) before storing it in the PDF.

    Returns: A tuple, consisting of 3 values: the name, the image data,
        and an instance of a subclass of `ImageInfo`.
    """

def load_image(filename):
    """
    This method is used to load external resources, such as images.
    It is automatically called when resource added to document by `fpdf.FPDF.image()`.
    It always return a BytesIO buffer.
    """

def is_iccp_valid(iccp, filename) -> bool:
    """Checks the validity of an ICC profile"""

def get_svg_info(filename: str, img: BytesIO, image_cache: ImageCache) -> tuple[str, SVGObject, VectorImageInfo]: ...

# Returned dict could be typed as a TypedDict.
def get_img_info(
    filename, img: BytesIO | Image.Image | None = None, image_filter: _ImageFilter = "AUTO", dims=None
) -> dict[str, Any]:
    """
    Args:
        filename: in a format that can be passed to load_image
        img: optional `bytes`, `BytesIO` or `PIL.Image.Image` instance
        image_filter (str): one of the SUPPORTED_IMAGE_FILTERS
    """

class temp_attr:
    """
    temporary change the attribute of an object using a context manager
    """

    obj: Any
    field: str
    value: Any
    exists: bool  # defined after __enter__ is called
    def __init__(self, obj: Any, field: str, value: Any) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self, exctype: type[BaseException] | None, excinst: BaseException | None, exctb: TracebackType | None
    ) -> None: ...

def ccitt_payload_location_from_pil(img: Image.Image) -> tuple[int, int]:
    """
    returns the byte offset and length of the CCITT payload in the original TIFF data
    """

def transcode_monochrome(img: Image.Image):
    """
    Convert the open PIL.Image imgdata to compressed CCITT Group4 data.

    """

def pack_codes_into_bytes(codes: Iterable[int]) -> bytes:
    """
    Convert the list of result codes into a continuous byte stream, with codes packed as per the code bit-width.
    The bit-width starts at 9 bits and expands as needed.

    """

def clear_table() -> tuple[dict[bytes, int], int, int, int]:
    """
    Reset the encoding table and coding state to initial conditions.

    """
