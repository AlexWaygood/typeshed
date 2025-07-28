from typing import Literal

from ..extractor.common import _InfoDict
from .fragment import FragmentFD

class DashSegmentsFD(FragmentFD):
    """
    Download segments in a DASH manifest. External downloaders can take over
    the fragment downloads by supporting the 'dash_frag_urls' protocol
    """

    FD_NAME: Literal["dashsegments"]
    def real_download(self, filename: str, info_dict: _InfoDict) -> bool: ...
