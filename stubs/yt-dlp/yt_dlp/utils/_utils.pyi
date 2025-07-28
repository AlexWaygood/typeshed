import enum
import html.parser
import json
import netrc
import optparse
import subprocess
import sys
import types
from _typeshed import (
    ExcInfo,
    FileDescriptorLike,
    FileDescriptorOrPath,
    OpenBinaryMode,
    OpenTextMode,
    ReadableBuffer,
    StrOrBytesPath,
    Unused,
)
from collections import deque
from collections.abc import Callable, Collection, Hashable, Iterable, Iterator, Mapping, Sequence
from datetime import date, datetime, timedelta
from functools import cache
from optparse import Values
from os import PathLike
from re import Pattern
from typing import IO, Any, AnyStr, BinaryIO, Generic, NamedTuple, TextIO, TypeVar, overload
from typing_extensions import Self, TypeAlias
from urllib.parse import _QueryType, _QuoteVia
from xml.etree import ElementTree as ET

from yt_dlp.networking import Response

from .. import _Params
from ..extractor.common import InfoExtractor, _InfoDict
from ..options import _YoutubeDLOptionParser
from ..YoutubeDL import YoutubeDL

_T = TypeVar("_T")

class NO_DEFAULT: ...

def IDENTITY(x: _T) -> _T: ...

ENGLISH_MONTH_NAMES: Sequence[str]
MONTH_NAMES: Mapping[str, Sequence[str]]
TIMEZONE_NAMES: Mapping[str, str]
ACCENT_CHARS: Mapping[str, str]
DATE_FORMATS: Sequence[str]
DATE_FORMATS_DAY_FIRST: Sequence[str]
DATE_FORMATS_MONTH_FIRST: Sequence[str]
PACKED_CODES_RE: str
JSON_LD_RE: str
NUMBER_RE: str

@cache
def preferredencoding() -> str:
    """Get preferred encoding.

    Returns the best encoding scheme for the system, based on
    locale.getpreferredencoding() and some further tweaks.
    """

def write_json_file(obj: Any, fn: str) -> None:  # obj passed to json.dump().
    """Encode obj as JSON and write it to fn, atomically if possible"""

def partial_application(func: Callable[..., Any]) -> Callable[..., Any]: ...
def find_xpath_attr(node: ET.ElementTree, xpath: str, key: str, val: str | None = None) -> ET.Element | None:
    """Find the xpath xpath[@key=val]"""

def xpath_with_ns(path: str, ns_map: Mapping[str, str]) -> str: ...
def xpath_element(
    node: ET.ElementTree, xpath: str, name: str | None = None, fatal: bool = False, default: ET.Element | type[NO_DEFAULT] = ...
) -> ET.Element | None: ...
def xpath_text(
    node: ET.ElementTree, xpath: str, name: str | None = None, fatal: bool = False, default: str | type[NO_DEFAULT] = ...
) -> str | None: ...
def xpath_attr(
    node: ET.ElementTree,
    xpath: str,
    key: str,
    name: str | None = None,
    fatal: bool = False,
    default: str | type[NO_DEFAULT] = ...,
) -> str | None: ...
def get_element_by_id(id: str, html: str, *, tag: str, escape_value: bool = True) -> str | None:
    """Return the content of the tag with the specified ID in the passed HTML document"""

def get_element_html_by_id(id: str, html: str, *, tag: str, escape_value: bool = True) -> str | None:
    """Return the html of the tag with the specified ID in the passed HTML document"""

def get_element_by_class(class_name: str, html: str) -> str:
    """Return the content of the first tag with the specified class in the passed HTML document"""

def get_element_html_by_class(class_name: str, html: str) -> str:
    """Return the html of the first tag with the specified class in the passed HTML document"""

def get_element_by_attribute(attribute: str, value: str, html: str, *, tag: str, escape_value: bool = True) -> str: ...
def get_element_html_by_attribute(attribute: str, value: str, html: str, *, tag: str, escape_value: bool = True) -> list[str]: ...
def get_elements_by_class(class_name: str, html: str, **kargs: Unused) -> list[str]:
    """Return the content of all tags with the specified class in the passed HTML document as a list"""

def get_elements_html_by_class(class_name: str, html: str) -> list[str]:
    """Return the html of all tags with the specified class in the passed HTML document as a list"""

def get_elements_by_attribute(attribute: str, value: str, html: str, *, tag: str, escape_value: bool = True) -> list[str]:
    """Return the content of the tag with the specified attribute in the passed HTML document"""

def get_elements_html_by_attribute(
    attribute: str, value: str, html: str, *, tag: str = "[\\w:.-]+", escape_value: bool = True
) -> list[str]:
    """Return the html of the tag with the specified attribute in the passed HTML document"""

def get_elements_text_and_html_by_attribute(
    attribute: str, value: str, html: str, *, tag: str = "[\\w:.-]+", escape_value: bool = True
) -> Iterator[str]:
    """
    Return the text (content) and the html (whole) of the tag with the specified
    attribute in the passed HTML document
    """

class HTMLBreakOnClosingTagParser(html.parser.HTMLParser):
    """
    HTML parser which raises HTMLBreakOnClosingTagException upon reaching the
    closing tag for the first opening tag it has encountered, and can be used
    as a context manager
    """

    class HTMLBreakOnClosingTagException(Exception): ...
    tagstack: deque[Any]
    def __init__(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *_: Unused) -> None: ...
    def close(self) -> None: ...
    def handle_starttag(self, tag: str, _: Unused) -> None: ...
    def handle_endtag(self, tag: str) -> None: ...

def get_element_text_and_html_by_tag(tag: str, html: str) -> str:
    """
    For the first element with the specified tag in the passed HTML document
    return its' content (text) and the whole element (html)
    """

class HTMLAttributeParser(html.parser.HTMLParser):
    """Trivial HTML parser to gather the attributes for a single element"""

    attrs: dict[str, str | None]
    def __init__(self) -> None: ...
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None: ...

class HTMLListAttrsParser(html.parser.HTMLParser):
    """HTML parser to gather the attributes for the elements of a list"""

    items: list[dict[str, str | None]]
    def __init__(self) -> None: ...
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None: ...
    def handle_endtag(self, tag: str) -> None: ...

def extract_attributes(html_element: str) -> dict[str, str]:
    """Given a string for an HTML element such as
    <el
         a="foo" B="bar" c="&98;az" d=boz
         empty= noval entity="&amp;"
         sq='"' dq="'"
    >
    Decode and return a dictionary of attributes.
    {
        'a': 'foo', 'b': 'bar', c: 'baz', d: 'boz',
        'empty': '', 'noval': None, 'entity': '&',
        'sq': '"', 'dq': '''
    }.
    """

def parse_list(webpage: str) -> list[dict[str, str | None]]:
    """Given a string for an series of HTML <li> elements,
    return a dictionary of their attributes
    """

def clean_html(html: str | None) -> str | None:
    """Clean an HTML snippet into a readable string"""

class LenientJSONDecoder(json.JSONDecoder):
    def __init__(
        self,
        *args: Unused,
        transform_source: Callable[[str], str] | None = None,
        ignore_extra: bool = False,
        close_objects: int = 0,
        object_hook: Callable[[dict[str, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        strict: bool = True,
        object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None,
    ) -> None: ...
    def decode(self, s: str) -> Any: ...  # type: ignore[override]

@overload
def sanitize_open(filename: FileDescriptorOrPath, open_mode: OpenBinaryMode) -> BinaryIO:
    """Try to open the given filename, and slightly tweak it if this fails.

    Attempts to open the given filename. If this fails, it tries to change
    the filename slightly, step by step, until it's either able to open it
    or it fails and raises a final exception, like the standard open()
    function.

    It returns the tuple (stream, definitive_file_name).
    """

@overload
def sanitize_open(filename: FileDescriptorOrPath, open_mode: OpenTextMode) -> TextIO: ...
def timeconvert(timestr: str) -> str:
    """Convert RFC 2822 defined time string into system timestamp"""

def sanitize_filename(s: str, restricted: bool = False, is_id: bool | type[NO_DEFAULT] = ...) -> str:
    """Sanitizes a string so it could be used as part of a filename.
    @param restricted   Use a stricter subset of allowed characters
    @param is_id        Whether this is an ID that should be kept unchanged if possible.
                        If unset, yt-dlp's new sanitization rules are in effect
    """

def sanitize_path(s: str, force: bool = False) -> str:
    """Sanitizes and normalizes path on Windows"""

def sanitize_url(url: str, *, scheme: str = "http") -> str: ...
def extract_basic_auth(url: str) -> tuple[str, str | None]: ...
def expand_path(s: str) -> str:
    """Expand shell variables and ~"""

def orderedSet(iterable: Iterable[_T], *, lazy: bool = False) -> Iterator[_T]:
    """Remove all duplicates from the input iterable"""

def unescapeHTML(s: str | None) -> str | None: ...
def escapeHTML(text: str) -> str: ...

class netrc_from_content(netrc.netrc):
    def __init__(self, content: str) -> None: ...

def encodeArgument(s: str) -> str: ...

class _timetuple(NamedTuple):
    """Time(hours, minutes, seconds, milliseconds)"""

    hours: tuple[int, int]
    minutes: tuple[int, int]
    seconds: tuple[int, int]
    milliseconds: tuple[int, int]

def timetuple_from_msec(msec: int) -> _timetuple: ...
def formatSeconds(secs: int, delim: str = ":", msec: bool = False) -> str: ...
def bug_reports_message(before: str = ";") -> None: ...

class YoutubeDLError(Exception):
    """Base exception for YoutubeDL errors."""

    msg: str | None
    def __init__(self, msg: str | None = None) -> None: ...

class ExtractorError(YoutubeDLError):
    """Error during info extraction."""

    orig_msg: Any
    traceback: types.TracebackType | None
    expected: Any
    cause: Exception | str | None
    video_id: str
    ie: InfoExtractor
    exc_info: ExcInfo
    def __init__(
        self,
        msg: str,
        tb: types.TracebackType | None = None,
        expected: bool = False,
        cause: Exception | str | None = None,
        video_id: str | None = None,
        ie: InfoExtractor | None = None,
    ) -> None:
        """tb, if given, is the original traceback (so that it can be printed out).
        If expected is set, this is a normal error message and most likely not a bug in yt-dlp.
        """

    def format_traceback(self) -> str: ...
    msg: str | None
    args: tuple[Any, ...]
    def __setattr__(self, name: str, value: Any) -> None: ...

class UnsupportedError(ExtractorError):
    url: str
    def __init__(self, url: str) -> None: ...

class RegexNotFoundError(ExtractorError):
    """Error when a regex didn't match"""

class GeoRestrictedError(ExtractorError):
    """Geographic restriction Error exception.

    This exception may be thrown when a video is not available from your
    geographic location due to geographic restrictions imposed by a website.
    """

    countries: str | None
    def __init__(
        self,
        msg: str,
        countries: str | None = None,
        *,
        tb: types.TracebackType | None = None,
        expected: bool = False,
        cause: Exception | str | None = None,
        video_id: str | None = None,
        ie: InfoExtractor | None = None,
    ) -> None: ...

class UserNotLive(ExtractorError):
    """Error when a channel/user is not live"""

    def __init__(
        self,
        msg: str | None = None,
        *,
        tb: types.TracebackType | None = None,
        expected: bool = False,
        cause: Exception | str | None = None,
        video_id: str | None = None,
        ie: InfoExtractor | None = None,
    ) -> None: ...

class DownloadError(YoutubeDLError):
    """Download Error exception.

    This exception may be thrown by FileDownloader objects if they are not
    configured to continue on errors. They will contain the appropriate
    error message.
    """

    exc_info: ExcInfo
    def __init__(self, msg: str, exc_info: ExcInfo | None = None) -> None:
        """exc_info, if given, is the original exception that caused the trouble (as returned by sys.exc_info())."""

class EntryNotInPlaylist(YoutubeDLError):
    """Entry not in playlist exception.

    This exception will be thrown by YoutubeDL when a requested entry
    is not found in the playlist info_dict
    """

    msg: str

class SameFileError(YoutubeDLError):
    """Same File exception.

    This exception will be thrown by FileDownloader objects if they detect
    multiple files would have to be downloaded to the same file on disk.
    """

    msg: str
    def __init__(self, filename: str | None = None) -> None: ...

class PostProcessingError(YoutubeDLError):
    """Post Processing exception.

    This exception may be raised by PostProcessor's .run() method to
    indicate an error in the postprocessing task.
    """

class DownloadCancelled(YoutubeDLError):
    """Exception raised when the download queue should be interrupted"""

    msg: str

class ExistingVideoReached(DownloadCancelled):
    """--break-on-existing triggered"""

    msg: str

class RejectedVideoReached(DownloadCancelled):
    """--break-match-filter triggered"""

    msg: str

class MaxDownloadsReached(DownloadCancelled):
    """--max-downloads limit has been reached."""

    msg: str

class ReExtractInfo(YoutubeDLError):
    """Video info needs to be re-extracted."""

    expected: bool
    def __init__(self, msg: str, expected: bool = False) -> None: ...

class ThrottledDownload(ReExtractInfo):
    """Download speed below --throttled-rate."""

    msg: str
    def __init__(self) -> None: ...

class UnavailableVideoError(YoutubeDLError):
    """Unavailable Format exception.

    This exception will be thrown when a video is requested
    in a format that is not available for that video.
    """

    msg: str
    def __init__(self, err: str | None = None) -> None: ...

class ContentTooShortError(YoutubeDLError):
    """Content Too Short exception.

    This exception may be raised by FileDownloader objects when a file they
    download is too small for what the server announced first, indicating
    the connection was probably interrupted.
    """

    downloaded: int
    expected: int
    def __init__(self, downloaded: int, expected: int) -> None: ...

class XAttrMetadataError(YoutubeDLError):
    code: str | None
    msg: str | None
    reason: str
    def __init__(self, code: str | None = None, msg: str = "Unknown error") -> None: ...

class XAttrUnavailableError(YoutubeDLError): ...

def is_path_like(f: Any) -> bool: ...  # Type checker.
def extract_timezone(date_str: str, default: Any = None) -> tuple[timedelta, str]: ...  # Any or type[NO_DEFAULT]
def parse_iso8601(date_str: str, delimiter: str = "T", timezone: type[NO_DEFAULT] | Any | None = None) -> int:
    """Return a UNIX timestamp from the given date"""

def date_formats(day_first: bool = True) -> list[str]: ...
def unified_strdate(date_str: str, day_first: bool = True) -> str:
    """Return a string with the date in the format YYYYMMDD"""

def unified_timestamp(date_str: str, day_first: bool = True) -> int: ...
def determine_ext(url: str, default_ext: str = "unknown_video") -> str: ...
def subtitles_filename(filename: str, sub_lang: str, sub_format: str, expected_real_ext: str | None = None) -> str: ...
def datetime_from_str(date_str: str, precision: str = "auto", format: str = "%Y%m%d") -> datetime:
    """
    Return a datetime object from a string.
    Supported format:
        (now|today|yesterday|DATE)([+-]\\d+(microsecond|second|minute|hour|day|week|month|year)s?)?

    @param format       strftime format of DATE
    @param precision    Round the datetime object: auto|microsecond|second|minute|hour|day
                        auto: round to the unit provided in date_str (if applicable).
    """

def date_from_str(date_str: str, format: str = "%Y%m%d", strict: bool = False) -> date:
    """
    Return a date object from a string using datetime_from_str

    @param strict  Restrict allowed patterns to "YYYYMMDD" and
                   (now|today|yesterday)(-\\d+(day|week|month|year)s?)?
    """

def datetime_add_months(dt_: datetime, months: int) -> datetime:
    """Increment/Decrement a datetime object by months."""

def datetime_round(dt_: datetime, precision: str = "day") -> datetime:
    """
    Round a datetime object's time to a specific precision
    """

def hyphenate_date(date_str: str) -> str:
    """
    Convert a date in 'YYYYMMDD' format to 'YYYY-MM-DD' format
    """

class DateRange:
    """Represents a time interval between two dates"""

    start: date
    end: date
    def __init__(self, start: date | None = None, end: date | None = None) -> None:
        """start and end must be strings in the format accepted by date"""

    @classmethod
    def day(cls, day: date) -> Self:
        """Returns a range that only contains the given day"""

    def __contains__(self, date: date) -> bool:
        """Check if the date is in the range"""

    def __eq__(self, other: object) -> bool: ...

def system_identifier() -> str: ...
def get_windows_version() -> tuple[str, ...]:
    """Get Windows version. returns () if it's not running on Windows"""

def write_string(s: str, out: TextIO | None = None, encoding: str | None = None) -> None: ...
def deprecation_warning(
    msg: str, *, printer: Callable[..., Any] | None = None, stacklevel: int = 0, **kwargs: Any  # kwargs are passed to printer.
) -> None: ...

class LockingUnsupportedError(OSError):
    msg: str
    def __init__(self) -> None: ...

class locked_file:
    locked: bool
    f: TextIO
    def __init__(
        self, filename: AnyStr, mode: OpenTextMode | OpenBinaryMode, block: bool = True, encoding: str | None = None
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def unlock(self) -> None: ...
    def __exit__(self, *_: Unused) -> None: ...
    open = __enter__
    close = __exit__
    def __getattr__(self, attr: str) -> Any: ...
    def __iter__(self) -> str: ...

def get_filesystem_encoding() -> str: ...
def shell_quote(args: str | Collection[str], *, shell: bool = False) -> str: ...
def smuggle_url(url: str, data: Any) -> str:  # data may be anything JSON serializable.
    """Pass additional data in a URL for internal use."""

# default is simply returned if #__youtubedl_smuggle is present.
def unsmuggle_url(smug_url: str, default: Any | None = None) -> tuple[str, Any]: ...
def format_decimal_suffix(num: float, fmt: str = "%d%s", *, factor: int = 1000) -> str:
    """Formats numbers with decimal sufixes like K, M, etc"""

def format_bytes(bytes: int) -> str: ...
def lookup_unit_table(unit_table: Mapping[str, int], s: str, strict: bool = False) -> float: ...
def parse_bytes(s: str) -> int:
    """Parse a string indicating a byte quantity into an integer"""

def parse_filesize(s: str | None) -> int | None: ...
def parse_count(s: str | None) -> str | None: ...
def parse_resolution(s: str, *, lenient: bool = False) -> dict[str, int]: ...
def parse_bitrate(s: str) -> int: ...
def month_by_name(name: str, lang: str = "en") -> str | None:
    """Return the number of a month by (locale-independently) English name"""

def month_by_abbreviation(abbrev: str) -> str | None:
    """Return the number of a month by (locale-independently) English
    abbreviations
    """

def fix_xml_ampersands(xml_str: str) -> str:
    """Replace all the '&' by '&amp;' in XML"""

def setproctitle(title: str) -> None: ...
def remove_start(s: str, start: str) -> str: ...
def remove_end(s: str, end: str) -> str: ...
def remove_quotes(s: str) -> str: ...
def get_domain(url: str) -> str | None:
    """
    This implementation is inconsistent, but is kept for compatibility.
    Use this only for "webpage_url_domain"
    """

def url_basename(url: str) -> str: ...
def base_url(url: str) -> str: ...
def urljoin(base: str, path: str) -> str: ...
def int_or_none(
    v: Any, scale: int = 1, default: int | None = None, get_attr: str | None = None, invscale: int = 1, base: int | None = None
) -> int | None: ...
def str_or_none(v: Any, default: str | None = None) -> str: ...
def str_to_int(int_str: str) -> int:
    """A more relaxed version of int_or_none"""

def float_or_none(v: Any, scale: int = 1, invscale: int = 1, default: float | None = None) -> float | None: ...
def bool_or_none(v: Any, default: bool | None = None) -> bool | None: ...
def strip_or_none(v: Any, default: str | None = None) -> str | None: ...
def url_or_none(url: Any) -> str | None: ...
def strftime_or_none(timestamp: int, date_format: str = "%Y%m%d", default: str | None = None) -> str | None: ...
def parse_duration(s: str | None) -> float: ...
def prepend_extension(filename: str, ext: str, expected_real_ext: str | None = None) -> str:
    """Create a new function with partial application of the given arguments
    and keywords.
    """

def replace_extension(filename: str, ext: str, expected_real_ext: str | None = None) -> str:
    """Create a new function with partial application of the given arguments
    and keywords.
    """

def check_executable(exe: str, args: Iterable[str] = ...) -> str | None:
    """Checks if the given binary is installed somewhere in PATH, and returns its name.
    args can be a list of arguments for a short output (like -version)
    """

def detect_exe_version(output: str, version_re: str | Pattern[str] | None = None, unrecognized: str = "present") -> str: ...
def get_exe_version(
    exe: str,
    args: Iterable[str] = ["--version"],
    version_re: str | None = None,
    unrecognized: Iterable[str] = ("present", "broken"),
) -> str:
    """Returns the version of the specified executable,
    or False if the executable is not present
    """

def frange(start: int = 0, stop: int | None = None, step: int = 1) -> Iterator[float]:
    """Float range"""

class LazyList(Sequence[_T]):
    """Lazy immutable list from an iterable
    Note that slices of a LazyList are lists and not LazyList
    """

    def __init__(self, iterable: Iterable[_T], *, reverse: bool = False, _cache: list[Any] | None = None) -> None: ...
    def __iter__(self) -> Iterator[_T]: ...
    def exhaust(self) -> list[_T]:
        """Evaluate the entire iterable"""

    @overload
    def __getitem__(self, idx: int, /) -> _T: ...
    @overload
    def __getitem__(self, idx: slice, /) -> list[_T]: ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Iterator[_T]: ...
    def __copy__(self) -> Self: ...

class PagedList:
    def __len__(self) -> int: ...
    def __init__(self, pagefunc: Callable[[int], Iterator[Any]], pagesize: int, use_cache: bool = True) -> None: ...
    def getpage(self, pagenum: int) -> list[Any]: ...
    def getslice(self, start: int = 0, end: int | None = None) -> list[Any]: ...
    @overload
    def __getitem__(self, idx: int, /) -> Any: ...
    @overload
    def __getitem__(self, idx: slice, /) -> list[Any]: ...
    def __bool__(self) -> bool: ...

class OnDemandPagedList(PagedList):
    """Download pages until a page with less than maximum results"""

class InAdvancePagedList(PagedList):
    """PagedList with total number of pages known in advance"""

    def __init__(self, pagefunc: Callable[[int], Iterator[Any]], pagecount: int, pagesize: int) -> None: ...

class PlaylistEntries:
    MissingEntry: Any
    is_exhausted: bool
    ydl: YoutubeDL
    is_incomplete: bool
    def __init__(self, ydl: YoutubeDL, info_dict: _InfoDict) -> None: ...
    PLAYLIST_ITEMS_RE: Pattern[str]
    @classmethod
    def parse_playlist_items(cls, string: str) -> slice | int: ...
    def get_requested_items(self) -> Iterator[tuple[int, Any]]: ...
    def get_full_count(self) -> int | None: ...
    def __getitem__(self, idx: int) -> Iterator[tuple[int, Any]]: ...
    def __len__(self) -> int: ...

_K = TypeVar("_K")
_V = TypeVar("_V")

def uppercase_escape(s: str) -> str: ...
def lowercase_escape(s: str) -> str: ...
def parse_qs(
    url: str,
    *,
    keep_blank_values: bool = False,
    strict_parsing: bool = False,
    encoding: str = "utf-8",
    errors: str = "replace",
    max_num_fields: int | None = None,
    separator: str = "&",
) -> dict[AnyStr, list[AnyStr]]: ...
def read_batch_urls(batch_fd: FileDescriptorLike) -> list[str]: ...
def urlencode_postdata(
    query: _QueryType,
    doseq: bool = False,
    safe: str | bytes = "",
    encoding: str | None = None,
    errors: str | None = None,
    quote_via: _QuoteVia = ...,
) -> bytes: ...

# Passes kwargs to NamedTuple._replace().
def update_url(url: str, *, query_update: Mapping[str, str] | None = None, **kwargs: Any) -> str:
    """Replace URL components specified by kwargs
    @param url           str or parse url tuple
    @param query_update  update query
    @returns             str
    """

def update_url_query(url: str, query: Mapping[str, str]) -> str: ...
def multipart_encode(data: Mapping[AnyStr, AnyStr], boundary: str | None = None) -> tuple[bytes, str]:
    """
    Encode a dict to RFC 7578-compliant form-data

    data:
        A dict where keys and values can be either Unicode or bytes-like
        objects.
    boundary:
        If specified a Unicode object, it's used as the boundary. Otherwise
        a random boundary is generated.

    Reference: https://tools.ietf.org/html/rfc7578
    """

def is_iterable_like(
    x: Any, allowed_types: Collection[type[Any]] = ..., blocked_types: Collection[type[Any]] | type[NO_DEFAULT] = ...
) -> bool: ...
def variadic(x: _T, allowed_types: Collection[type[Any]] | type[NO_DEFAULT] = ...) -> _T | tuple[_T]: ...
def try_call(
    *funcs: Callable[..., _T],
    expected_type: type[_T] | None = None,
    args: Iterable[Any] = ...,
    kwargs: Mapping[Hashable, Any] = ...,
) -> _T | None: ...
def try_get(src: Any, getter: Callable[..., _T] | Collection[Callable[..., _T]], expected_type: type[_T] | None = None) -> _T: ...
def filter_dict(dct: Mapping[_K, _V], cndn: Callable[[_K, _V], bool] = ...) -> dict[_K, _V]: ...
def merge_dicts(*dicts: Mapping[Hashable, Any]) -> dict[Hashable, Any]: ...
def encode_compat_str(string: str, encoding: str = ..., errors: str = "strict") -> str: ...

US_RATINGS: Mapping[str, int]
TV_PARENTAL_GUIDELINES: Mapping[str, int]

def parse_age_limit(s: int) -> int | None: ...
def strip_jsonp(code: str) -> str: ...
def js_to_json(code: str, vars: Mapping[str, Any] = ..., *, strict: bool = False) -> str: ...
def qualities(quality_ids: Sequence[int]) -> Callable[[int], int]:
    """Get a numeric quality value out of a list of possible values"""

POSTPROCESS_WHEN: tuple[str, ...]
DEFAULT_OUTTMPL: Mapping[str, str]
OUTTMPL_TYPES: Mapping[str, str | None]
STR_FORMAT_RE_TMPL: str
STR_FORMAT_TYPES: str

def limit_length(s: str, length: int) -> str:
    """Add ellipses to overly long strings"""

def version_tuple(v: str) -> tuple[int, ...]: ...
def is_outdated_version(version: str, limit: str, assume_new: bool = True) -> bool: ...
def ytdl_is_updateable() -> bool:
    """Returns if yt-dlp can be updated with -U"""

def args_to_str(args: str | Collection[str]) -> str: ...
def error_to_str(err: BaseException) -> str: ...
def mimetype2ext(mt: str, default: str | type[NO_DEFAULT] = ...) -> str: ...
def ext2mimetype(ext_or_url: str | None) -> str: ...
def parse_codecs(codecs_str: str) -> dict[str, str]: ...
def get_compatible_ext(
    *,
    vcodecs: Collection[str],
    acodecs: Collection[str],
    vexts: Collection[str],
    aexts: Collection[str],
    preferences: Sequence[str] | None = None,
) -> str: ...
def urlhandle_detect_ext(url_handle: Response, default: str | type[NO_DEFAULT] = ...) -> str | None: ...
def encode_data_uri(data: ReadableBuffer, mime_type: str) -> str: ...
def age_restricted(content_limit: int | None, age_limit: int | None) -> bool:
    """Returns True iff the content should be blocked"""

BOMS: Collection[tuple[bytes, str]]

def is_html(first_bytes: bytes) -> bool:
    """Detect whether a file contains HTML by examining its first bytes."""

def determine_protocol(info_dict: _InfoDict) -> str: ...
def render_table(
    header_row: Iterable[str], data: Iterable[str], delim: bool = False, extra_gap: int = 0, hide_empty: bool = False
) -> str:
    """Render a list of rows, each as a list of values.
    Text after a         will be right aligned
    """

def match_str(filter_str: str, dct: Mapping[str, Any], incomplete: bool = False) -> bool:
    """Filter a dictionary with a simple string syntax.
    @returns           Whether the filter passes
    @param incomplete  Set of keys that is expected to be missing from dct.
                       Can be True/False to indicate all/none of the keys may be missing.
                       All conditions on incomplete keys pass if the key is missing
    """

def match_filter_func(
    filters: Collection[str] | str, breaking_filters: Collection[str] | str | None = None
) -> Callable[..., str | type[NO_DEFAULT] | None]: ...

class download_range_func:
    def __init__(
        self, chapters: Iterable[str | Pattern[str]], ranges: Iterable[tuple[int, int]], from_info: bool = False
    ) -> None: ...
    def __call__(self, info_dict: _InfoDict, ydl: YoutubeDL) -> Iterator[dict[str, Any]]: ...
    def __eq__(self, other: object) -> bool: ...

def parse_dfxp_time_expr(time_expr: str | None) -> int | None: ...
def srt_subtitles_timecode(seconds: float) -> str: ...
def ass_subtitles_timecode(seconds: float) -> str: ...
def dfxp2srt(dfxp_data: bytes) -> str:
    """
    @param dfxp_data A bytes-like object containing DFXP data
    @returns A unicode object containing converted SRT data
    """

def cli_option(params: _Params, command_option: str, param: str, separator: str | None = None) -> Any: ...
def cli_bool_option(
    params: _Params,
    command_option: str,
    param: bool | None,
    true_value: str = "true",
    false_value: str = "false",
    separator: str | None = None,
) -> Any: ...
def cli_valueless_option(params: _Params, command_option: str, param: str, expected_value: bool = True) -> Any: ...
def cli_configuration_args(argdict: dict[str, Any], keys: Iterable[str], default: Any = ..., use_compat: bool = True) -> Any: ...

class ISO639Utils:
    @classmethod
    def short2long(cls, code: str) -> str | None:
        """Convert language code from ISO 639-1 to ISO 639-2/T"""

    @classmethod
    def long2short(cls, code: str) -> str | None:
        """Convert language code from ISO 639-2/T to ISO 639-1"""

class ISO3166Utils:
    @classmethod
    def short2full(cls, code: str) -> str | None:
        """Convert an ISO 3166-2 country code to the corresponding full name"""

class GeoUtils:
    @classmethod
    def random_ipv4(cls, code_or_block: str) -> str | None: ...

def long_to_bytes(n: int, blocksize: int = 0) -> bytes:
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """

def bytes_to_long(s: bytes) -> int:
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.

    This is (essentially) the inverse of long_to_bytes().
    """

def ohdave_rsa_encrypt(data: ReadableBuffer, exponent: float, modulus: float | None) -> str:
    """
    Implement OHDave's RSA algorithm. See http://www.ohdave.com/rsa/

    Input:
        data: data to encrypt, bytes-like object
        exponent, modulus: parameter e and N of RSA algorithm, both integer
    Output: hex string of encrypted data

    Limitation: supports one block encryption only
    """

def pkcs1pad(data: Sequence[int], length: int) -> list[int]:
    """
    Padding input data with PKCS#1 scheme

    @param {int[]} data        input data
    @param {int}   length      target length
    @returns {int[]}           padded data
    """

def encode_base_n(num: int, n: int | None = None, table: str | None = None) -> str:
    """Convert given int to a base-n string"""

def decode_base_n(string: str, n: int | None = None, table: str | None = None) -> int:
    """Convert given base-n string to int"""

def decode_packed_codes(code: str) -> str: ...
def caesar(s: str, alphabet: str, shift: int) -> str: ...
def rot47(s: str) -> str: ...
def parse_m3u8_attributes(attrib: str) -> dict[str, str]: ...
def urshift(val: int, n: int) -> int: ...
def write_xattr(path: FileDescriptorOrPath, key: str, value: str) -> None: ...
def random_birthday(year_field: Hashable, month_field: Hashable, day_field: Hashable) -> dict[Hashable, str]: ...
def find_available_port(interface: str = "") -> Any | None: ...

DOT_URL_LINK_TEMPLATE: str
DOT_WEBLOC_LINK_TEMPLATE: str
DOT_DESKTOP_LINK_TEMPLATE: str
LINK_TEMPLATES: Mapping[str, str]

def iri_to_uri(iri: str) -> str:
    """
    Converts an IRI (Internationalized Resource Identifier, allowing Unicode characters) to a URI (Uniform Resource Identifier, ASCII-only).

    The function doesn't add an additional layer of escaping; e.g., it doesn't escape `%3C` as `%253C`. Instead, it percent-escapes characters with an underlying UTF-8 encoding *besides* those already escaped, leaving the URI intact.
    """

def to_high_limit_path(path: PathLike[AnyStr]) -> str: ...
def format_field(
    obj: Mapping[str, Any] | Sequence[Any],
    field: str | Collection[str] | None = None,
    template: str = "%s",
    ignore: type[NO_DEFAULT] | str | Collection[str] = ...,
    default: str = "",
    func: Callable[[Any], Any] = ...,
) -> str: ...
def clean_podcast_url(url: str) -> str: ...
def random_uuidv4() -> str: ...
def make_dir(path: PathLike[AnyStr], to_screen: Callable[[str], Any] | None = None) -> bool: ...
def get_executable_path() -> str: ...
def get_user_config_dirs(package_name: str) -> Iterator[str]: ...
def get_system_config_dirs(package_name: str) -> Iterator[str]: ...
def time_seconds(**kwargs: float) -> int:
    """
    Returns TZ-aware time in seconds since the epoch (1970-01-01T00:00:00Z)
    """

def jwt_encode_hs256(payload_data: Any, key: str, headers: Mapping[str, Any] = ...) -> bytes: ...  # Passed to json.dumps().
def jwt_decode_hs256(jwt: str) -> Any: ...  # Returns json.loads() output.

WINDOWS_VT_MODE: bool | None

def supports_terminal_sequences(stream: IO[Any]) -> bool: ...
def windows_enable_vt_mode() -> None:
    """Ref: https://bugs.python.org/issue30075"""

def remove_terminal_sequences(string: str) -> str: ...
def number_of_digits(number: int) -> int: ...
def join_nonempty(*values: str, delim: str = "-", from_dict: Mapping[str, Any] | None = None) -> str: ...
def scale_thumbnails_to_max_format_width(
    formats: Iterable[Mapping[str, Any]], thumbnails: Iterable[Mapping[str, Any]], url_width_re: str | Pattern[str]
) -> list[dict[str, Any]]:
    """
    Find the largest format dimensions in terms of video width and, for each thumbnail:
    * Modify the URL: Match the width with the provided regex and replace with the former width
    * Update dimensions

    This function is useful with video services that scale the provided thumbnails on demand
    """

def parse_http_range(range: str | None) -> tuple[int | None, int | None, int | None]:
    """Parse value of "Range" or "Content-Range" HTTP header into tuple."""

def read_stdin(what: str) -> TextIO | Any: ...
def determine_file_encoding(data: bytes) -> tuple[str | None, int]:
    """
    Detect the text encoding used
    @returns (encoding, bytes to skip)
    """

class Config:
    own_args: Sequence[str] | None
    parsed_args: tuple[Values, list[str]] | None
    filename: str | None
    def __init__(self, parser: _YoutubeDLOptionParser, label: str | None = None) -> None: ...
    def init(self, args: Sequence[str] | None = None, filename: str | None = None) -> bool: ...
    def load_configs(self) -> bool: ...
    @staticmethod
    def read_file(filename: FileDescriptorOrPath, default: list[str] = []) -> list[str]: ...
    @staticmethod
    def hide_login_info(opts: Iterable[str]) -> list[str]: ...
    def append_config(self, args: Sequence[str] | None, filename: str | None, *, label: str | None = None) -> None: ...
    @property
    def all_args(self) -> Iterator[str]: ...
    def parse_known_args(self, *, values: optparse.Values | None = None, strict: bool = True) -> tuple[Values, list[str]]: ...
    def parse_args(self) -> tuple[Values, list[str]]: ...

def merge_headers(*dicts: dict[str, Any]) -> dict[str, Any]:
    """Merge dicts of http headers case insensitively, prioritizing the latter ones"""

def cached_method(f: Callable[..., Any]) -> Callable[..., Any]:
    """Cache a method"""

class function_with_repr(Generic[_T]):
    def __init__(self, func: Callable[..., _T], repr_: str | None = None) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...  # Arbitrary arguments.
    @classmethod
    def set_repr(cls, repr_: str) -> Callable[..., Any]: ...

class Namespace(types.SimpleNamespace):
    """Immutable namespace"""

    def __iter__(self) -> Iterator[Any]: ...
    @property
    def items_(self) -> dict[str, Any]: ...

MEDIA_EXTENSIONS: Namespace
KNOWN_EXTENSIONS: tuple[str, ...]

class _UnsafeExtensionError(Exception):
    """
    Mitigation exception for uncommon/malicious file extensions
    This should be caught in YoutubeDL.py alongside a warning

    Ref: https://github.com/yt-dlp/yt-dlp/security/advisories/GHSA-79w7-vh3h-8g4j
    """

    ALLOWED_EXTENSIONS: frozenset[str]
    extension: str
    def __init__(self, extension: str, /) -> None: ...
    @classmethod
    def sanitize_extension(cls, extension: str, /, *, prepend: bool = False) -> str: ...

class RetryManager:
    """Usage:
    for retry in RetryManager(...):
        try:
            ...
        except SomeException as err:
            retry.error = err
            continue
    """

    attempt: int
    retries: int
    error_callback: Callable[[BaseException, int, int], Any]
    def __init__(
        self, _retries: int | None, _error_callback: Callable[..., Any], **kwargs: Any  # kwargs passed to _error_callback.
    ) -> None: ...
    @property
    def error(self) -> None: ...
    @error.setter
    def error(self, value: type[NO_DEFAULT] | BaseException) -> None: ...
    def __iter__(self) -> Self: ...
    @staticmethod
    def report_retry(
        e: BaseException,
        count: int,
        retries: int,
        *,
        sleep_func: Callable[..., float | None],
        info: Callable[[str], Any],
        warn: Callable[[str], Any],
        error: Callable[[str], Any] | None = None,
        suffix: str | None = None,
    ) -> None:
        """Utility function for reporting retries"""

def make_archive_id(ie: InfoExtractor, video_id: str) -> str: ...
def truncate_string(s: str, left: int, right: int = 0) -> str: ...
def orderedSet_from_options(
    options: Sequence[str], alias_dict: dict[str, Sequence[str]], *, use_regex: bool = False, start: Iterable[Any] | None = None
) -> Iterator[Any]: ...

class FormatSorter:
    regex: str
    default: tuple[str, ...]
    ytdl_default: tuple[str, ...]
    settings: dict[str, Any]
    ydl: YoutubeDL
    def __init__(self, ydl: YoutubeDL, field_preference: _Params) -> None: ...
    def evaluate_params(self, params: _Params, sort_extractor: Collection[str]) -> None: ...
    def print_verbose_info(self, write_debug: Callable[..., None]) -> None: ...
    def calculate_preference(self, format: dict[str, Any]) -> tuple[int, ...]: ...

@overload
def filesize_from_tbr(tbr: None, duration: None) -> None:
    """
    @param tbr:      Total bitrate in kbps (1000 bits/sec)
    @param duration: Duration in seconds
    @returns         Filesize in bytes
    """

@overload
def filesize_from_tbr(tbr: int, duration: None) -> None: ...
@overload
def filesize_from_tbr(tbr: None, duration: int) -> None: ...
@overload
def filesize_from_tbr(tbr: int | None, duration: int | None) -> int | None: ...

class _YDLLogger:
    def __init__(self, ydl: YoutubeDL | None = None) -> None: ...
    def debug(self, message: str) -> None: ...
    def info(self, message: str) -> None: ...
    def warning(self, message: str, *, once: bool = False) -> None: ...
    def error(self, message: str, *, is_error: bool = True) -> None: ...
    def stdout(self, message: str) -> None: ...
    def stderr(self, message: str) -> None: ...

class _ProgressState(enum.Enum):
    """
    Represents a state for a progress bar.

    See: https://conemu.github.io/en/AnsiEscapeCodes.html#ConEmu_specific_OSC
    """

    HIDDEN = 0
    INDETERMINATE = 3
    VISIBLE = 1
    WARNING = 4
    ERROR = 2
    @classmethod
    def from_dict(cls, s: dict[str, Any], /) -> _ProgressState: ...
    def get_ansi_escape(self, /, percent: int | None = None) -> str: ...

if sys.platform == "win32":
    _ENV: TypeAlias = Mapping[str, str]
else:
    _ENV: TypeAlias = Mapping[bytes, StrOrBytesPath] | Mapping[str, StrOrBytesPath]

class Popen(subprocess.Popen[AnyStr]):
    def __init__(
        self,
        args: StrOrBytesPath | Sequence[StrOrBytesPath],
        *remaining: Any,  # Passed to subprocess.Popen.__init__().
        env: _ENV | None = None,
        text: bool = False,
        shell: bool = False,
        **kwargs: Any,  # Passed to subprocess.Popen.__init__().
    ) -> None: ...
    def communicate_or_kill(self, input: AnyStr | None = None, timeout: float | None = None) -> tuple[AnyStr, AnyStr]: ...
    def kill(self, *, timeout: int = 0) -> None: ...
    # kwargs passed to cls.__init__().
    @classmethod
    def run(cls, *args: Any, timeout: int | None = None, **kwargs: Any) -> tuple[AnyStr, AnyStr]: ...

class classproperty:
    """property access for class methods with optional caching"""

    # args passed to func().
    def __new__(cls, func: Callable[..., Any] | None = None, *args: Any, cache: bool = False) -> Self: ...
    def __init__(  # pyright: ignore[reportInconsistentConstructor]
        self, func: Callable[..., Any], *, cache: bool = False
    ) -> None: ...
    def __get__(self, _: Unused, cls: type[Any]) -> Any: ...
