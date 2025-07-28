from logging import Logger
from typing import Any, Literal

from ._types import Reader, TagDict

logger: Logger

class IfdTag:
    """
    Eases dealing with tags.
    """

    printable: str
    tag: int
    field_type: int
    field_offset: int
    field_length: int
    values: Any  # either string, bytes or list of data items
    def __init__(self, printable: str, tag: int, field_type: int, values: Any, field_offset: int, field_length: int) -> None: ...

class ExifHeader:
    """
    Handle an EXIF header.
    """

    file_handle: Reader
    endian: Literal["I", "M"]
    offset: int
    fake_exif: bool
    strict: bool
    debug: bool
    detailed: bool
    truncate_tags: bool
    tags: dict[str, Any]
    def __init__(
        self,
        file_handle: Reader,
        endian: Literal["I", "M"],
        offset: int,
        fake_exif: bool,
        strict: bool,
        debug: bool = False,
        detailed: bool = True,
        truncate_tags: bool = True,
    ) -> None: ...
    def s2n(self, offset: int, length: int, signed: bool = False) -> int:
        """
        Convert slice to integer, based on sign and endian flags.

        Usually this offset is assumed to be relative to the beginning of the
        start of the EXIF information.
        For some cameras that use relative tags, this offset may be relative
        to some other starting point.
        """

    def n2b(self, offset: int, length: int) -> bytes:
        """Convert offset to bytes."""

    def list_ifd(self) -> list[int]:
        """Return the list of IFDs in the header."""

    def dump_ifd(
        self, ifd: int, ifd_name: str, tag_dict: TagDict | None = None, relative: int = 0, stop_tag: str = "UNDEF"
    ) -> None:
        """
        Return a list of entries in the given IFD.
        """

    def extract_tiff_thumbnail(self, thumb_ifd: int) -> None:
        """
        Extract uncompressed TIFF thumbnail.

        Take advantage of the pre-existing layout in the thumbnail IFD as
        much as possible
        """

    def extract_jpeg_thumbnail(self) -> None:
        """
        Extract JPEG thumbnail.

        (Thankfully the JPEG data is stored as a unit.)
        """

    def decode_maker_note(self) -> None:
        """
        Decode all the camera-specific MakerNote formats

        Note is the data that comprises this MakerNote.
        The MakerNote will likely have pointers in it that point to other
        parts of the file. We'll use self.offset as the starting point for
        most of those pointers, since they are relative to the beginning
        of the file.
        If the MakerNote is in a newer format, it may use relative addressing
        within the MakerNote. In that case we'll use relative addresses for
        the pointers.
        As an aside: it's not just to be annoying that the manufacturers use
        relative offsets.  It's so that if the makernote has to be moved by the
        picture software all of the offsets don't have to be adjusted.  Overall,
        this is probably the right strategy for makernotes, though the spec is
        ambiguous.
        The spec does not appear to imagine that makernotes would
        follow EXIF format internally.  Once they did, it's ambiguous whether
        the offsets should be from the header at the start of all the EXIF info,
        or from the header at the start of the makernote.

        TODO: look into splitting this up
        """

    def parse_xmp(self, xmp_bytes: bytes) -> None:
        """Adobe's Extensible Metadata Platform, just dump the pretty XML."""
