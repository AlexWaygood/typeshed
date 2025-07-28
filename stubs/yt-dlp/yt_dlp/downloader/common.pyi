from _typeshed import OpenBinaryMode, OpenTextMode
from collections.abc import Callable, Mapping
from typing import IO, Any, AnyStr, TypedDict, type_check_only

from ..extractor.common import _InfoDict
from ..utils._utils import NO_DEFAULT, Namespace
from ..YoutubeDL import YoutubeDL

@type_check_only
class _FileDownloaderParams(TypedDict):
    buffersize: int
    continuedl: bool
    external_downloader_args: dict[str, list[str]] | list[str] | None
    file_access_retries: int
    hls_use_mpegts: bool
    http_chunk_size: int | None
    max_filesize: int | None
    min_filesize: int | None
    nopart: bool
    noprogress: bool
    noresizebuffer: bool
    progress_delta: float | None
    progress_template: dict[str, str]
    quiet: bool
    ratelimit: int | None
    retries: int
    retry_sleep_functions: dict[str, Callable[..., object]]
    test: bool
    throttledratelimit: int | None
    updatetime: bool
    verbose: bool
    xattr_set_filesize: bool

class FileDownloader:
    """File Downloader class.

    File downloader objects are the ones responsible of downloading the
    actual video file and writing it to disk.

    File downloaders accept a lot of parameters. In order not to saturate
    the object constructor with arguments, it receives a dictionary of
    options instead.

    Available options:

    verbose:            Print additional info to stdout.
    quiet:              Do not print messages to stdout.
    ratelimit:          Download speed limit, in bytes/sec.
    throttledratelimit: Assume the download is being throttled below this speed (bytes/sec)
    retries:            Number of times to retry for expected network errors.
                        Default is 0 for API, but 10 for CLI
    file_access_retries:   Number of times to retry on file access error (default: 3)
    buffersize:         Size of download buffer in bytes.
    noresizebuffer:     Do not automatically resize the download buffer.
    continuedl:         Try to continue downloads if possible.
    noprogress:         Do not print the progress bar.
    nopart:             Do not use temporary .part files.
    updatetime:         Use the Last-modified header to set output file timestamps.
    test:               Download only first bytes to test the downloader.
    min_filesize:       Skip files smaller than this size
    max_filesize:       Skip files larger than this size
    xattr_set_filesize: Set ytdl.filesize user xattribute with expected size.
    progress_delta:     The minimum time between progress output, in seconds
    external_downloader_args:  A dictionary of downloader keys (in lower case)
                        and a list of additional command-line arguments for the
                        executable. Use 'default' as the name for arguments to be
                        passed to all downloaders. For compatibility with youtube-dl,
                        a single list of args can also be used
    hls_use_mpegts:     Use the mpegts container for HLS videos.
    http_chunk_size:    Size of a chunk for chunk-based HTTP downloading. May be
                        useful for bypassing bandwidth throttling imposed by
                        a webserver (experimental)
    progress_template:  See YoutubeDL.py
    retry_sleep_functions: See YoutubeDL.py

    Subclasses of this one must re-define the real_download method.
    """

    params: _FileDownloaderParams | None
    def __init__(self, ydl: YoutubeDL, params: _FileDownloaderParams) -> None:
        """Create a FileDownloader object with the given options."""

    def to_screen(self, message: str, skip_eol: bool = False, quiet: bool | None = None, only_once: bool = False) -> None: ...
    @property
    def FD_NAME(cls) -> str: ...
    @staticmethod
    def format_seconds(seconds: int | None) -> str: ...
    @classmethod
    def format_eta(cls, seconds: int | None) -> str: ...
    @staticmethod
    def calc_percent(byte_counter: float, data_len: float | None) -> float: ...
    @staticmethod
    def format_percent(percent: float | None) -> str: ...
    @classmethod
    def calc_eta(
        cls,
        start_or_rate: int | None,
        now_or_remaining: float | None,
        total: int | type[NO_DEFAULT] = ...,
        current: int | type[NO_DEFAULT] = ...,
    ) -> float | int | None: ...
    @staticmethod
    def calc_speed(start: float, now: float, bytes: int) -> float | None: ...
    @staticmethod
    def format_speed(speed: int | None) -> str: ...
    @staticmethod
    def format_retries(retries: int) -> float | int: ...
    @staticmethod
    def filesize_or_none(unencoded_filename: AnyStr) -> int | None: ...
    @staticmethod
    def best_block_size(elapsed_time: float, bytes: int) -> int: ...
    def slow_down(self, start_time: float, now: float, byte_counter: int) -> None:
        """Sleep if the download speed is over the rate limit."""

    def temp_name(self, filename: str) -> str:
        """Returns a temporary filename for the given filename."""

    def undo_temp_name(self, filename: str) -> str: ...
    def ytdl_filename(self, filename: str) -> str: ...
    # Wrapper that can accept arbitrary function.
    def wrap_file_access(action: str, *, fatal: bool = False) -> Any: ...  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
    def sanitize_open(self, filename: str, open_mode: OpenTextMode | OpenBinaryMode) -> tuple[IO[Any], str]:
        """Method descriptor with partial application of the given arguments
        and keywords.

        Supports wrapping existing descriptors and handles non-descriptor
        callables as instance methods.
        """

    def try_remove(self, filename: str) -> None:
        """Method descriptor with partial application of the given arguments
        and keywords.

        Supports wrapping existing descriptors and handles non-descriptor
        callables as instance methods.
        """

    def try_rename(self, old_filename: str, new_filename: str) -> None:
        """Method descriptor with partial application of the given arguments
        and keywords.

        Supports wrapping existing descriptors and handles non-descriptor
        callables as instance methods.
        """

    def try_utime(self, filename: str, last_modified_hdr: str | None) -> int | None:
        """Try to set the last-modified time of the given file."""

    def report_destination(self, filename: str) -> None:
        """Report destination filename."""
    ProgressStyles: Namespace
    def report_progress(self, s: Mapping[str, Any]) -> None: ...
    def report_resuming_byte(self, resume_len: int) -> None:
        """Report attempt to resume at given byte."""

    def report_retry(
        self, err: str, count: int, retries: int, frag_index: int | type[NO_DEFAULT] = ..., fatal: bool = True
    ) -> None:
        """Report retry"""

    def report_unable_to_resume(self) -> None:
        """Report it was impossible to resume download."""

    @staticmethod
    def supports_manifest(manifest: str) -> bool:
        """Whether the downloader can download the fragments from the manifest.
        Redefine in subclasses if needed.
        """

    def download(self, filename: str, info_dict: _InfoDict, subtitle: bool = False) -> bool:
        """Download to a filename using the info from info_dict
        Return True on success and False otherwise
        """

    def real_download(self, filename: str, info_dict: _InfoDict) -> bool | None:
        """Real download process. Redefine in subclasses."""

    def add_progress_hook(self, ph: Callable[[str], object]) -> None: ...
