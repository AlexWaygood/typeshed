import io
from _typeshed import SupportsWrite
from collections.abc import Iterable, Mapping
from typing import Any
from xml.etree.ElementTree import Element

from .fragment import FragmentFD

class DataTruncatedError(Exception): ...

class FlvReader(io.BytesIO):
    """
    Reader for Flv files
    The file format is documented in https://www.adobe.com/devnet/f4v.html
    """

    def read_bytes(self, n: int) -> bytes: ...
    def read_unsigned_long_long(self) -> int: ...
    def read_unsigned_int(self) -> int: ...
    def read_unsigned_char(self) -> str: ...
    def read_string(self) -> bytes: ...
    def read_box_info(self) -> tuple[int, bytes, bytes]:
        """
        Read a box and return the info as a tuple: (box_size, box_type, box_data)
        """

    def read_asrt(self) -> dict[str, Any]: ...
    def read_afrt(self) -> dict[str, Any]: ...
    def read_abst(self) -> dict[str, Any]: ...
    def read_bootstrap_info(self) -> dict[str, Any]: ...

def read_bootstrap_info(bootstrap_bytes: bytes) -> dict[str, Any]: ...
def build_fragments_list(boot_info: Mapping[str, Any]) -> list[tuple[Any, int]]:
    """Return a list of (segment, fragment) for each fragment in the video"""

def write_unsigned_int(stream: SupportsWrite[bytes], val: int) -> None: ...
def write_unsigned_int_24(stream: SupportsWrite[bytes], val: int) -> None: ...
def write_flv_header(stream: SupportsWrite[bytes]) -> None:
    """Writes the FLV header to stream"""

def write_metadata_tag(stream: SupportsWrite[bytes], metadata: bytes) -> None:
    """Writes optional metadata tag to stream"""

def remove_encrypted_media(media: Iterable[Element]) -> list[Any]: ...
def get_base_url(manifest: str) -> str | None: ...

class F4mFD(FragmentFD):
    """
    A downloader for f4m manifests or AdobeHDS.
    """
