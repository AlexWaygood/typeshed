from collections.abc import Callable, Collection, Mapping, Sequence
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any

from ..extractor.common import _InfoDict
from .common import FileDownloader
from .http import HttpFD

class HttpQuietDownloader(HttpFD):
    def to_screen(self, *args: Any, **kargs: Any) -> None: ...  # This method is a no-op.
    to_console_title = to_screen

class FragmentFD(FileDownloader):
    """
    A base file downloader class for fragmented media (e.g. f4m/m3u8 manifests).

    Available options:

    fragment_retries:   Number of times to retry a fragment for HTTP error
                        (DASH and hlsnative only). Default is 0 for API, but 10 for CLI
    skip_unavailable_fragments:
                        Skip unavailable fragments (DASH and hlsnative only)
    keep_fragments:     Keep downloaded fragments on disk after downloading is
                        finished
    concurrent_fragment_downloads:  The number of threads to use for native hls and dash downloads
    _no_ytdl_file:      Don't use .ytdl file

    For each incomplete fragment download yt-dlp keeps on disk a special
    bookkeeping file with download state and metadata (in future such files will
    be used for any incomplete download handled by yt-dlp). This file is
    used to properly handle resuming, check download file consistency and detect
    potential errors. The file has a .ytdl extension and represents a standard
    JSON file of the following format:

    extractor:
        Dictionary of extractor related data. TBD.

    downloader:
        Dictionary of downloader related data. May contain following data:
            current_fragment:
                Dictionary with current (being downloaded) fragment data:
                index:  0-based index of current fragment among all fragments
            fragment_count:
                Total count of fragments

    This feature is experimental and file format may change in future.
    """

    def report_retry_fragment(self, err: str, frag_index: int, count: int, retries: int) -> None: ...
    def report_skip_fragment(self, frag_index: int, err: str | None = None) -> None: ...
    def decrypter(self, info_dict: _InfoDict) -> Callable[[Mapping[str, Any], bytes], bytes]: ...
    def download_and_append_fragments_multiple(
        self,
        *args: tuple[Mapping[str, Any], Collection[Mapping[str, Any]], _InfoDict],
        is_fatal: Callable[[int], bool] = ...,
        pack_func: Callable[[str, int], bytes] = ...,
        finish_func: Callable[[], Any] | None = None,
        tpe: ThreadPoolExecutor | None = None,
        interrupt_trigger: Sequence[bool] = (True,),
    ) -> bool:
        """
        @params (ctx1, fragments1, info_dict1), (ctx2, fragments2, info_dict2), ...
                all args must be either tuple or list
        """

    def download_and_append_fragments(
        self,
        ctx: Mapping[str, Any],
        fragments: Collection[Mapping[str, Any]],
        info_dict: _InfoDict,
        *,
        is_fatal: Callable[[int], bool] = ...,
        pack_func: Callable[[str, int], bytes] = ...,
        finish_func: Callable[[], object] | None = None,
        tpe: ThreadPoolExecutor | None = None,
        interrupt_trigger: Sequence[bool] = (True,),
    ) -> bool: ...
