from _typeshed import SupportsWrite

from ..extractor.common import _InfoDict
from .common import FileDownloader

class FFmpegSinkFD(FileDownloader):
    """A sink to ffmpeg for downloading fragments in any form"""

    def real_download(self, filename: str, info_dict: _InfoDict) -> bool: ...
    async def real_connection(self, sink: SupportsWrite[bytes], info_dict: _InfoDict) -> None:
        """Override this in subclasses"""

class WebSocketFragmentFD(FFmpegSinkFD):
    async def real_connection(self, sink: SupportsWrite[bytes], info_dict: _InfoDict) -> None: ...
