from ..extractor.common import _InfoDict
from .fragment import FragmentFD

class HlsFD(FragmentFD):
    """
    Download segments in a m3u8 manifest. External downloaders can take over
    the fragment downloads by supporting the 'm3u8_frag_urls' protocol and
    re-defining 'supports_manifest' function
    """

    FD_NAME: str
    @classmethod
    def can_download(cls, manifest: str, info_dict: _InfoDict, allow_unplayable_formats: bool = False) -> bool: ...
