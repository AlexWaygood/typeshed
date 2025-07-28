import re
from _typeshed import Unused
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, Sequence
from functools import cached_property
from json.decoder import JSONDecoder
from typing import Any, Literal, TypedDict, TypeVar, type_check_only
from typing_extensions import Required, TypeAlias
from urllib.request import Request, _DataType
from xml.etree import ElementTree as ET

from ..cache import Cache
from ..cookies import LenientSimpleCookie, YoutubeDLCookieJar
from ..networking.common import Response, _RequestData
from ..networking.impersonate import ImpersonateTarget
from ..utils._utils import NO_DEFAULT, RetryManager as _RetryManager
from ..YoutubeDL import YoutubeDL

@type_check_only
class _InfoDict(TypedDict, total=False):
    age_limit: int
    availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"] | None
    creator: str | None
    comment_count: int | None
    duration: int | None
    formats: list[dict[str, Any]] | None
    id: Required[str]
    like_count: int | None
    tags: list[str] | None
    thumbnail: str | None
    timestamp: int | float | None
    title: str | None
    uploader: str | None
    url: str | None

_StrNoDefaultOrNone: TypeAlias = str | None | type[NO_DEFAULT]
_T = TypeVar("_T")

class InfoExtractor:
    """Information Extractor class.

    Information extractors are the classes that, given a URL, extract
    information about the video (or videos) the URL refers to. This
    information includes the real video URL, the video title, author and
    others. The information is stored in a dictionary which is then
    passed to the YoutubeDL. The YoutubeDL processes this
    information possibly downloading the video to the file system, among
    other possible outcomes.

    The type field determines the type of the result.
    By far the most common value (and the default if _type is missing) is
    "video", which indicates a single video.

    For a video, the dictionaries must include the following fields:

    id:             Video identifier.
    title:          Video title, unescaped. Set to an empty string if video has
                    no title as opposed to "None" which signifies that the
                    extractor failed to obtain a title

    Additionally, it must contain either a formats entry or a url one:

    formats:        A list of dictionaries for each format available, ordered
                    from worst to best quality.

                    Potential fields:
                    * url        The mandatory URL representing the media:
                                   for plain file media - HTTP URL of this file,
                                   for RTMP - RTMP URL,
                                   for HLS - URL of the M3U8 media playlist,
                                   for HDS - URL of the F4M manifest,
                                   for DASH
                                     - HTTP URL to plain file media (in case of
                                       unfragmented media)
                                     - URL of the MPD manifest or base URL
                                       representing the media if MPD manifest
                                       is parsed from a string (in case of
                                       fragmented media)
                                   for MSS - URL of the ISM manifest.
                    * request_data  Data to send in POST request to the URL
                    * manifest_url
                                 The URL of the manifest file in case of
                                 fragmented media:
                                   for HLS - URL of the M3U8 master playlist,
                                   for HDS - URL of the F4M manifest,
                                   for DASH - URL of the MPD manifest,
                                   for MSS - URL of the ISM manifest.
                    * manifest_stream_number  (For internal use only)
                                 The index of the stream in the manifest file
                    * ext        Will be calculated from URL if missing
                    * format     A human-readable description of the format
                                 ("mp4 container with h264/opus").
                                 Calculated from the format_id, width, height.
                                 and format_note fields if missing.
                    * format_id  A short description of the format
                                 ("mp4_h264_opus" or "19").
                                Technically optional, but strongly recommended.
                    * format_note Additional info about the format
                                 ("3D" or "DASH video")
                    * width      Width of the video, if known
                    * height     Height of the video, if known
                    * aspect_ratio  Aspect ratio of the video, if known
                                 Automatically calculated from width and height
                    * resolution Textual description of width and height
                                 Automatically calculated from width and height
                    * dynamic_range The dynamic range of the video. One of:
                                 "SDR" (None), "HDR10", "HDR10+, "HDR12", "HLG, "DV"
                    * tbr        Average bitrate of audio and video in kbps (1000 bits/sec)
                    * abr        Average audio bitrate in kbps (1000 bits/sec)
                    * acodec     Name of the audio codec in use
                    * asr        Audio sampling rate in Hertz
                    * audio_channels  Number of audio channels
                    * vbr        Average video bitrate in kbps (1000 bits/sec)
                    * fps        Frame rate
                    * vcodec     Name of the video codec in use
                    * container  Name of the container format
                    * filesize   The number of bytes, if known in advance
                    * filesize_approx  An estimate for the number of bytes
                    * player_url SWF Player URL (used for rtmpdump).
                    * protocol   The protocol that will be used for the actual
                                 download, lower-case. One of "http", "https" or
                                 one of the protocols defined in downloader.PROTOCOL_MAP
                    * fragment_base_url
                                 Base URL for fragments. Each fragment's path
                                 value (if present) will be relative to
                                 this URL.
                    * fragments  A list of fragments of a fragmented media.
                                 Each fragment entry must contain either an url
                                 or a path. If an url is present it should be
                                 considered by a client. Otherwise both path and
                                 fragment_base_url must be present. Here is
                                 the list of all potential fields:
                                 * "url" - fragment's URL
                                 * "path" - fragment's path relative to
                                            fragment_base_url
                                 * "duration" (optional, int or float)
                                 * "filesize" (optional, int)
                    * hls_media_playlist_data
                                 The M3U8 media playlist data as a string.
                                 Only use if the data must be modified during extraction and
                                 the native HLS downloader should bypass requesting the URL.
                                 Does not apply if ffmpeg is used as external downloader
                    * is_from_start  Is a live format that can be downloaded
                                from the start. Boolean
                    * preference Order number of this format. If this field is
                                 present and not None, the formats get sorted
                                 by this field, regardless of all other values.
                                 -1 for default (order by other properties),
                                 -2 or smaller for less than default.
                                 < -1000 to hide the format (if there is
                                    another one which is strictly better)
                    * language   Language code, e.g. "de" or "en-US".
                    * language_preference  Is this in the language mentioned in
                                 the URL?
                                 10 if it's what the URL is about,
                                 -1 for default (don't know),
                                 -10 otherwise, other values reserved for now.
                    * quality    Order number of the video quality of this
                                 format, irrespective of the file format.
                                 -1 for default (order by other properties),
                                 -2 or smaller for less than default.
                    * source_preference  Order number for this video source
                                  (quality takes higher priority)
                                 -1 for default (order by other properties),
                                 -2 or smaller for less than default.
                    * http_headers  A dictionary of additional HTTP headers
                                 to add to the request.
                    * stretched_ratio  If given and not 1, indicates that the
                                 video's pixels are not square.
                                 width : height ratio as float.
                    * no_resume  The server does not support resuming the
                                 (HTTP or RTMP) download. Boolean.
                    * has_drm    True if the format has DRM and cannot be downloaded.
                                 'maybe' if the format may have DRM and has to be tested before download.
                    * extra_param_to_segment_url  A query string to append to each
                                 fragment's URL, or to update each existing query string
                                 with. If it is an HLS stream with an AES-128 decryption key,
                                 the query paramaters will be passed to the key URI as well,
                                 unless there is an `extra_param_to_key_url` given,
                                 or unless an external key URI is provided via `hls_aes`.
                                 Only applied by the native HLS/DASH downloaders.
                    * extra_param_to_key_url  A query string to append to the URL
                                 of the format's HLS AES-128 decryption key.
                                 Only applied by the native HLS downloader.
                    * hls_aes    A dictionary of HLS AES-128 decryption information
                                 used by the native HLS downloader to override the
                                 values in the media playlist when an '#EXT-X-KEY' tag
                                 is present in the playlist:
                                 * uri  The URI from which the key will be downloaded
                                 * key  The key (as hex) used to decrypt fragments.
                                        If `key` is given, any key URI will be ignored
                                 * iv   The IV (as hex) used to decrypt fragments
                    * impersonate  Impersonate target(s). Can be any of the following entities:
                                * an instance of yt_dlp.networking.impersonate.ImpersonateTarget
                                * a string in the format of CLIENT[:OS]
                                * a list or a tuple of CLIENT[:OS] strings or ImpersonateTarget instances
                                * a boolean value; True means any impersonate target is sufficient
                    * downloader_options  A dictionary of downloader options
                                 (For internal use only)
                                 * http_chunk_size Chunk size for HTTP downloads
                                 * ffmpeg_args     Extra arguments for ffmpeg downloader (input)
                                 * ffmpeg_args_out Extra arguments for ffmpeg downloader (output)
                                 * ws              (NiconicoLiveFD only) WebSocketResponse
                                 * ws_url          (NiconicoLiveFD only) Websockets URL
                                 * max_quality     (NiconicoLiveFD only) Max stream quality string
                    * is_dash_periods  Whether the format is a result of merging
                                 multiple DASH periods.
                    RTMP formats can also have the additional fields: page_url,
                    app, play_path, tc_url, flash_version, rtmp_live, rtmp_conn,
                    rtmp_protocol, rtmp_real_time

    url:            Final video URL.
    ext:            Video filename extension.
    format:         The video format, defaults to ext (used for --get-format)
    player_url:     SWF Player URL (used for rtmpdump).

    The following fields are optional:

    direct:         True if a direct video file was given (must only be set by GenericIE)
    alt_title:      A secondary title of the video.
    display_id:     An alternative identifier for the video, not necessarily
                    unique, but available before title. Typically, id is
                    something like "4234987", title "Dancing naked mole rats",
                    and display_id "dancing-naked-mole-rats"
    thumbnails:     A list of dictionaries, with the following entries:
                        * "id" (optional, string) - Thumbnail format ID
                        * "url"
                        * "ext" (optional, string) - actual image extension if not given in URL
                        * "preference" (optional, int) - quality of the image
                        * "width" (optional, int)
                        * "height" (optional, int)
                        * "resolution" (optional, string "{width}x{height}",
                                        deprecated)
                        * "filesize" (optional, int)
                        * "http_headers" (dict) - HTTP headers for the request
    thumbnail:      Full URL to a video thumbnail image.
    description:    Full video description.
    uploader:       Full name of the video uploader.
    license:        License name the video is licensed under.
    creators:       List of creators of the video.
    timestamp:      UNIX timestamp of the moment the video was uploaded
    upload_date:    Video upload date in UTC (YYYYMMDD).
                    If not explicitly set, calculated from timestamp
    release_timestamp: UNIX timestamp of the moment the video was released.
                    If it is not clear whether to use timestamp or this, use the former
    release_date:   The date (YYYYMMDD) when the video was released in UTC.
                    If not explicitly set, calculated from release_timestamp
    release_year:   Year (YYYY) as integer when the video or album was released.
                    To be used if no exact release date is known.
                    If not explicitly set, calculated from release_date.
    modified_timestamp: UNIX timestamp of the moment the video was last modified.
    modified_date:   The date (YYYYMMDD) when the video was last modified in UTC.
                    If not explicitly set, calculated from modified_timestamp
    uploader_id:    Nickname or id of the video uploader.
    uploader_url:   Full URL to a personal webpage of the video uploader.
    channel:        Full name of the channel the video is uploaded on.
                    Note that channel fields may or may not repeat uploader
                    fields. This depends on a particular extractor.
    channel_id:     Id of the channel.
    channel_url:    Full URL to a channel webpage.
    channel_follower_count: Number of followers of the channel.
    channel_is_verified: Whether the channel is verified on the platform.
    location:       Physical location where the video was filmed.
    subtitles:      The available subtitles as a dictionary in the format
                    {tag: subformats}. "tag" is usually a language code, and
                    "subformats" is a list sorted from lower to higher
                    preference, each element is a dictionary with the "ext"
                    entry and one of:
                        * "data": The subtitles file contents
                        * "url": A URL pointing to the subtitles file
                    It can optionally also have:
                        * "name": Name or description of the subtitles
                        * "http_headers": A dictionary of additional HTTP headers
                                  to add to the request.
                        * "impersonate": Impersonate target(s); same as the "formats" field
                    "ext" will be calculated from URL if missing
    automatic_captions: Like 'subtitles'; contains automatically generated
                    captions instead of normal subtitles
    duration:       Length of the video in seconds, as an integer or float.
    view_count:     How many users have watched the video on the platform.
    concurrent_view_count: How many users are currently watching the video on the platform.
    like_count:     Number of positive ratings of the video
    dislike_count:  Number of negative ratings of the video
    repost_count:   Number of reposts of the video
    average_rating: Average rating given by users, the scale used depends on the webpage
    comment_count:  Number of comments on the video
    comments:       A list of comments, each with one or more of the following
                    properties (all but one of text or html optional):
                        * "author" - human-readable name of the comment author
                        * "author_id" - user ID of the comment author
                        * "author_thumbnail" - The thumbnail of the comment author
                        * "author_url" - The url to the comment author's page
                        * "author_is_verified" - Whether the author is verified
                                                 on the platform
                        * "author_is_uploader" - Whether the comment is made by
                                                 the video uploader
                        * "id" - Comment ID
                        * "html" - Comment as HTML
                        * "text" - Plain text of the comment
                        * "timestamp" - UNIX timestamp of comment
                        * "parent" - ID of the comment this one is replying to.
                                     Set to "root" to indicate that this is a
                                     comment to the original video.
                        * "like_count" - Number of positive ratings of the comment
                        * "dislike_count" - Number of negative ratings of the comment
                        * "is_favorited" - Whether the comment is marked as
                                           favorite by the video uploader
                        * "is_pinned" - Whether the comment is pinned to
                                        the top of the comments
    age_limit:      Age restriction for the video, as an integer (years)
    webpage_url:    The URL to the video webpage, if given to yt-dlp it
                    should allow to get the same result again. (It will be set
                    by YoutubeDL if it's missing)
    categories:     A list of categories that the video falls in, for example
                    ["Sports", "Berlin"]
    tags:           A list of tags assigned to the video, e.g. ["sweden", "pop music"]
    cast:           A list of the video cast
    is_live:        True, False, or None (=unknown). Whether this video is a
                    live stream that goes on instead of a fixed-length video.
    was_live:       True, False, or None (=unknown). Whether this video was
                    originally a live stream.
    live_status:    None (=unknown), 'is_live', 'is_upcoming', 'was_live', 'not_live',
                    or 'post_live' (was live, but VOD is not yet processed)
                    If absent, automatically set from is_live, was_live
    start_time:     Time in seconds where the reproduction should start, as
                    specified in the URL.
    end_time:       Time in seconds where the reproduction should end, as
                    specified in the URL.
    chapters:       A list of dictionaries, with the following entries:
                        * "start_time" - The start time of the chapter in seconds
                        * "end_time" - The end time of the chapter in seconds
                                       (optional: core code can determine this value from
                                       the next chapter's start_time or the video's duration)
                        * "title" (optional, string)
    heatmap:        A list of dictionaries, with the following entries:
                        * "start_time" - The start time of the data point in seconds
                        * "end_time" - The end time of the data point in seconds
                        * "value" - The normalized value of the data point (float between 0 and 1)
    playable_in_embed: Whether this video is allowed to play in embedded
                    players on other sites. Can be True (=always allowed),
                    False (=never allowed), None (=unknown), or a string
                    specifying the criteria for embedability; e.g. 'whitelist'
    availability:   Under what condition the video is available. One of
                    'private', 'premium_only', 'subscriber_only', 'needs_auth',
                    'unlisted' or 'public'. Use 'InfoExtractor._availability'
                    to set it
    media_type:     The type of media as classified by the site, e.g. "episode", "clip", "trailer"
    _old_archive_ids: A list of old archive ids needed for backward
                   compatibility. Use yt_dlp.utils.make_archive_id to generate ids
    _format_sort_fields: A list of fields to use for sorting formats
    __post_extractor: A function to be called just before the metadata is
                    written to either disk, logger or console. The function
                    must return a dict which will be added to the info_dict.
                    This is usefull for additional information that is
                    time-consuming to extract. Note that the fields thus
                    extracted will not be available to output template and
                    match_filter. So, only "comments" and "comment_count" are
                    currently allowed to be extracted via this method.

    The following fields should only be used when the video belongs to some logical
    chapter or section:

    chapter:        Name or title of the chapter the video belongs to.
    chapter_number: Number of the chapter the video belongs to, as an integer.
    chapter_id:     Id of the chapter the video belongs to, as a unicode string.

    The following fields should only be used when the video is an episode of some
    series, programme or podcast:

    series:         Title of the series or programme the video episode belongs to.
    series_id:      Id of the series or programme the video episode belongs to, as a unicode string.
    season:         Title of the season the video episode belongs to.
    season_number:  Number of the season the video episode belongs to, as an integer.
    season_id:      Id of the season the video episode belongs to, as a unicode string.
    episode:        Title of the video episode. Unlike mandatory video title field,
                    this field should denote the exact title of the video episode
                    without any kind of decoration.
    episode_number: Number of the video episode within a season, as an integer.
    episode_id:     Id of the video episode, as a unicode string.

    The following fields should only be used when the media is a track or a part of
    a music album:

    track:          Title of the track.
    track_number:   Number of the track within an album or a disc, as an integer.
    track_id:       Id of the track (useful in case of custom indexing, e.g. 6.iii),
                    as a unicode string.
    artists:        List of artists of the track.
    composers:      List of composers of the piece.
    genres:         List of genres of the track.
    album:          Title of the album the track belongs to.
    album_type:     Type of the album (e.g. "Demo", "Full-length", "Split", "Compilation", etc).
    album_artists:  List of all artists appeared on the album.
                    E.g. ["Ash Borer", "Fell Voices"] or ["Various Artists"].
                    Useful for splits and compilations.
    disc_number:    Number of the disc or other physical medium the track belongs to,
                    as an integer.

    The following fields should only be set for clips that should be cut from the original video:

    section_start:  Start time of the section in seconds
    section_end:    End time of the section in seconds

    The following fields should only be set for storyboards:
    rows:           Number of rows in each storyboard fragment, as an integer
    columns:        Number of columns in each storyboard fragment, as an integer

    The following fields are deprecated and should not be set by new code:
    composer:       Use "composers" instead.
                    Composer(s) of the piece, comma-separated.
    artist:         Use "artists" instead.
                    Artist(s) of the track, comma-separated.
    genre:          Use "genres" instead.
                    Genre(s) of the track, comma-separated.
    album_artist:   Use "album_artists" instead.
                    All artists appeared on the album, comma-separated.
    creator:        Use "creators" instead.
                    The creator of the video.

    Unless mentioned otherwise, the fields should be Unicode strings.

    Unless mentioned otherwise, None is equivalent to absence of information.


    _type "playlist" indicates multiple videos.
    There must be a key "entries", which is a list, an iterable, or a PagedList
    object, each element of which is a valid dictionary by this specification.

    Additionally, playlists can have "id", "title", and any other relevant
    attributes with the same semantics as videos (see above).

    It can also have the following optional fields:

    playlist_count: The total number of videos in a playlist. If not given,
                    YoutubeDL tries to calculate it from "entries"


    _type "multi_video" indicates that there are multiple videos that
    form a single show, for examples multiple acts of an opera or TV episode.
    It must have an entries key like a playlist and contain all the keys
    required for a video at the same time.


    _type "url" indicates that the video must be extracted from another
    location, possibly by a different extractor. Its only required key is:
    "url" - the next URL to extract.
    The key "ie_key" can be set to the class name (minus the trailing "IE",
    e.g. "Youtube") if the extractor class is known in advance.
    Additionally, the dictionary may have any properties of the resolved entity
    known in advance, for example "title" if the title of the referred video is
    known ahead of time.


    _type "url_transparent" entities have the same specification as "url", but
    indicate that the given additional information is more precise than the one
    associated with the resolved URL.
    This is useful when a site employs a video service that hosts the video and
    its technical metadata, but that video service does not embed a useful
    title, description etc.


    Subclasses of this should also be added to the list of extractors and
    should define _VALID_URL as a regexp or a Sequence of regexps, and
    re-define the _real_extract() and (optionally) _real_initialize() methods.

    Subclasses may also override suitable() if necessary, but ensure the function
    signature is preserved and that this function imports everything it needs
    (except other extractors), so that lazy_extractors works correctly.

    Subclasses can define a list of _EMBED_REGEX, which will be searched for in
    the HTML of Generic webpages. It may also override _extract_embed_urls
    or _extract_from_webpage as necessary. While these are normally classmethods,
    _extract_from_webpage is allowed to be an instance method.

    _extract_from_webpage may raise self.StopExtraction to stop further
    processing of the webpage and obtain exclusive rights to it. This is useful
    when the extractor cannot reliably be matched using just the URL,
    e.g. invidious/peertube instances

    Embed-only extractors can be defined by setting _VALID_URL = False.

    To support username + password (or netrc) login, the extractor must define a
    _NETRC_MACHINE and re-define _perform_login(username, password) and
    (optionally) _initialize_pre_login() methods. The _perform_login method will
    be called between _initialize_pre_login and _real_initialize if credentials
    are passed by the user. In cases where it is necessary to have the login
    process as part of the extraction rather than initialization, _perform_login
    can be left undefined.

    _GEO_BYPASS attribute may be set to False in order to disable
    geo restriction bypass mechanisms for a particular extractor.
    Though it won't disable explicit geo restriction bypass based on
    country code provided with geo_bypass_country.

    _GEO_COUNTRIES attribute may contain a list of presumably geo unrestricted
    countries for this extractor. One of these countries will be used by
    geo restriction bypass mechanism right away in order to bypass
    geo restriction, of course, if the mechanism is not disabled.

    _GEO_IP_BLOCKS attribute may contain a list of presumably geo unrestricted
    IP blocks in CIDR notation for this extractor. One of these IP blocks
    will be used by geo restriction bypass mechanism similarly
    to _GEO_COUNTRIES.

    The _ENABLED attribute should be set to False for IEs that
    are disabled by default and must be explicitly enabled.

    The _WORKING attribute should be set to False for broken IEs
    in order to warn the users and skip the tests.
    """

    IE_DESC: str | bool
    SEARCH_KEY: str
    def _login_hint(self, method: _StrNoDefaultOrNone, netrc: str | None = None) -> dict[str, str]: ...
    def __init__(self, downloader: YoutubeDL | None = None) -> None:
        """Constructor. Receives an optional downloader (a YoutubeDL instance).
        If a downloader is not passed during initialization,
        it must be set using "set_downloader()" before "extract()" is called
        """

    @classmethod
    def _match_valid_url(cls, url: str) -> re.Match[str] | None: ...
    @classmethod
    def suitable(cls, url: str) -> re.Match[str] | None:
        """Receives a URL and returns True if suitable for this IE."""

    @classmethod
    def get_temp_id(cls, url: str) -> str | None: ...
    @classmethod
    def working(cls) -> bool:
        """Getter method for _WORKING."""

    @classmethod
    def supports_login(cls) -> bool: ...
    def initialize(self) -> None:
        """Initializes an instance (authentication, etc)."""

    def extract(self, url: str) -> Iterator[_InfoDict]:
        """Extracts URL information and returns it in list of dicts."""

    def set_downloader(self, downloader: YoutubeDL) -> None:
        """Sets a YoutubeDL instance as the downloader for this IE."""

    @property
    def cache(self) -> Cache: ...
    @property
    def cookiejar(self) -> YoutubeDLCookieJar: ...
    def _initialize_pre_login(self) -> None:
        """Initialization before login. Redefine in subclasses."""

    def _perform_login(self, username: str, password: str) -> None:
        """Login with username and password. Redefine in subclasses."""

    def _real_initialize(self) -> None:
        """Real initialization process. Redefine in subclasses."""

    @classmethod
    def ie_key(cls) -> str:
        """A string for getting the InfoExtractor with get_info_extractor"""

    @property
    def IE_NAME(cls) -> str: ...
    def _create_request(
        self,
        url_or_request: str | Request,
        data: _DataType | None = None,
        headers: Mapping[str, str] | None = None,
        query: str | Mapping[str, str] | None = None,
        extensions: Mapping[str, Any] | None = None,
    ) -> Request: ...
    def _download_webpage_handle(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        encoding: str | None = None,
        data: _DataType | None = None,
        headers: Mapping[str, str] | None = None,
        query: str | Mapping[str, str] | None = None,
        expected_status: int | None = None,
        impersonate: ImpersonateTarget | str | bool | Collection[str | ImpersonateTarget] | None = None,
        require_impersonation: bool = False,
    ) -> tuple[str, Response] | Literal[False]:
        """
        Return a tuple (page content as string, URL handle).

        Arguments:
        url_or_request -- plain text URL as a string or
            a yt_dlp.networking.Request object
        video_id -- Video/playlist/item identifier (string)

        Keyword arguments:
        note -- note printed before downloading (string)
        errnote -- note printed in case of an error (string)
        fatal -- flag denoting whether error should be considered fatal,
            i.e. whether it should cause ExtractionError to be raised,
            otherwise a warning will be reported and extraction continued
        encoding -- encoding for a page content decoding, guessed automatically
            when not explicitly specified
        data -- POST data (bytes)
        headers -- HTTP headers (dict)
        query -- URL query (dict)
        expected_status -- allows to accept failed HTTP requests (non 2xx
            status code) by explicitly specifying a set of accepted status
            codes. Can be any of the following entities:
                - an integer type specifying an exact failed status code to
                  accept
                - a list or a tuple of integer types specifying a list of
                  failed status codes to accept
                - a callable accepting an actual failed status code and
                  returning True if it should be accepted
            Note that this argument does not affect success status codes (2xx)
            which are always accepted.
        impersonate -- the impersonate target. Can be any of the following entities:
                - an instance of yt_dlp.networking.impersonate.ImpersonateTarget
                - a string in the format of CLIENT[:OS]
                - a list or a tuple of CLIENT[:OS] strings or ImpersonateTarget instances
                - a boolean value; True means any impersonate target is sufficient
        require_impersonation -- flag to toggle whether the request should raise an error
            if impersonation is not possible (bool, default: False)
        """

    @staticmethod
    def _guess_encoding_from_content(content_type: str, webpage_bytes: bytes) -> str: ...
    def _webpage_read_content(
        self,
        urlh: Response,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        prefix: str | None = None,
        encoding: str | None = None,
        data: _RequestData | None = None,
    ) -> str | Literal[False]: ...
    def _parse_json(
        self,
        json_string: str,
        video_id: str,
        transform_source: Callable[..., str] | None = None,
        fatal: bool = True,
        errnote: str | None = None,
        *,
        cls: type[JSONDecoder] | None = None,
        object_hook: Callable[[dict[Any, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    ) -> Any: ...
    def _parse_socket_response_as_json(
        self,
        data: str,
        video_id: str,
        cls: type[JSONDecoder] | None = None,
        object_hook: Callable[[dict[Any, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    ) -> Any: ...
    def report_warning(self, msg: str, video_id: str | None = None, only_once: bool = False) -> None: ...
    def to_screen(
        self, msg: str, message: str, skip_eol: bool = False, quiet: bool | None = None, only_once: bool = False
    ) -> None:
        """Print msg to screen, prefixing it with '[ie_name]'"""

    def write_debug(self, msg: str, only_once: bool = False) -> None: ...
    # *args and **kwargs are passed to .params.get() where params is normally a mapping but is not required to be.
    def get_param(self, name: str, default: Any = None, *args: Any, **kwargs: Any) -> Any: ...
    def report_drm(self, video_id: str) -> None: ...
    def report_extraction(self, id_or_name: str) -> None:
        """Report information extraction."""

    def report_download_webpage(self, video_id: str) -> None:
        """Report webpage download."""

    def report_age_confirmation(self) -> None:
        """Report attempt to confirm age."""

    def report_login(self) -> None:
        """Report attempt to log in."""

    def raise_login_required(
        self,
        msg: str = "This video is only available for registered users",
        metadata_available: bool = False,
        method: str | type[NO_DEFAULT] = ...,
    ) -> None: ...
    def raise_geo_restricted(
        self, msg: str = ..., countries: Collection[str] | None = None, metadata_available: bool = False
    ) -> None: ...
    def raise_no_formats(self, msg: str, expected: bool = False, video_id: str | None = None) -> None: ...
    @staticmethod
    def url_result(
        url: str,
        ie: InfoExtractor | None = None,
        video_id: str | None = None,
        video_title: str | None = None,
        *,
        url_transparent: bool = False,
        **kwargs: Any,  # Added to the dict return value.
    ) -> dict[str, Any]:
        """Returns a URL that points to a page that should be processed"""

    @classmethod
    def playlist_from_matches(
        cls,
        matches: Sequence[str],
        playlist_id: str | None = None,
        playlist_title: str | None = None,
        getter: Callable[..., Any] = ...,
        ie: InfoExtractor | None = None,
        video_kwargs: Mapping[str, Any] | None = None,
        multi_video: bool = False,
        **kwargs: Any,  # Added to the dict return value.
    ) -> dict[str, Any]: ...
    @staticmethod
    def playlist_result(
        entries: Iterable[_InfoDict],
        playlist_id: str | None = ...,
        playlist_title: str | None = ...,
        playlist_description: str | None = ...,
        *,
        multi_video: bool = ...,
        **kwargs: Any,  # Added to the dict return value.
    ) -> _InfoDict:
        """Returns a playlist"""

    def http_scheme(self) -> str:
        """Either "http:" or "https:", depending on the user's preferences"""

    @classmethod
    def get_testcases(cls, include_onlymatching: bool = False) -> Iterator[dict[str, Any]]: ...
    @classmethod
    def get_webpage_testcases(cls) -> Iterator[dict[str, Any]]: ...
    @property
    def age_limit(cls) -> int:
        """Get age limit from the testcases"""

    @classmethod
    def is_single_video(cls, url: str) -> bool:
        """Returns whether the URL is of a single video, None if unknown"""

    @classmethod
    def is_suitable(cls, age_limit: int) -> bool:
        """Test whether the extractor is generally suitable for the given age limit"""

    @classmethod
    def description(cls, *, markdown: bool = True, search_examples: Sequence[str] | None = None) -> str:
        """Description of the extractor"""
    # Calls _get_subtitles which only raises NotImplementedError here.
    def extract_subtitles(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]: ...
    def _configuration_arg(self, key: str, default: Any = ..., *, ie_key: str | None = ..., casesense: bool = ...) -> Any:
        """
        @returns            A list of values for the extractor argument given by "key"
                            or "default" if no such key is present
        @param default      The default value to return when the key is not present (default: [])
        @param casesense    When false, the values are converted to lower case
        """
    # These are dynamically created.
    def _download_xml_handle(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> tuple[ET.ElementTree, Response]:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    (xml as an xml.etree.ElementTree.Element, URL handle)

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_xml(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> ET.ElementTree:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    xml as an xml.etree.ElementTree.Element

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_socket_json_handle(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> tuple[dict[str, Any], Response]:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    (JSON object as a dict, URL handle)

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_socket_json(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> dict[str, Any]:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    JSON object as a dict

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_json_handle(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> tuple[dict[str, Any], Response]:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    (JSON object as a dict, URL handle)

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_json(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> dict[str, Any]:
        """
        @param transform_source     Apply this transformation before parsing
        @returns                    JSON object as a dict

        See _download_webpage_handle docstring for other arguments specification
        """

    def _download_webpage(
        self,
        url_or_request: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        encoding: str | None = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
        impersonate: str | None = ...,
        require_impersonation: bool = ...,
    ) -> str:
        """
        Return the data of the page as a string.

        Keyword arguments:
        tries -- number of tries
        timeout -- sleep interval between tries

        See _download_webpage_handle docstring for other arguments specification.
        """

    def _parse_xml(
        self,
        xml_string: str,
        video_id: str,
        transform_source: Callable[..., str] | None = ...,
        fatal: bool = ...,
        errnote: str | None = ...,
    ) -> ET.Element: ...
    def _parse_mpd_formats(
        self, mpd_doc: ET.Element, mpd_id: str | None = ..., mpd_base_url: str = ..., mpd_url: str | None = ...
    ) -> list[Any]: ...
    def _real_extract(self, url: str) -> _InfoDict:
        """Real extraction process. Redefine in subclasses."""

    @staticmethod
    def _availability(
        is_private: bool | None = ...,
        needs_premium: bool | None = ...,
        needs_subscription: bool | None = ...,
        needs_auth: bool | None = ...,
        is_unlisted: bool | None = ...,
    ) -> Literal["needs_auth", "premium_only", "private", "public", "subscriber_only", "unlisted"] | None: ...
    def _request_webpage(
        self,
        url_or_req: str | Request,
        video_id: str,
        note: str | None = ...,
        errnote: str | None = ...,
        fatal: bool = ...,
        data: _DataType | None = ...,
        headers: Mapping[str, str] = ...,
        query: Mapping[str, str] = ...,
        expected_status: int | None = ...,
    ) -> Response | Literal[False]:
        """
        Return the response handle.

        See _download_webpage docstring for arguments specification.
        """

    @classmethod
    def _match_id(cls, url: str) -> str: ...
    def _search_regex(
        self,
        pattern: str | re.Pattern[str],
        string: str | None,
        name: str,
        default: _StrNoDefaultOrNone = ...,
        fatal: bool = True,
        flags: int = 0,
        group: tuple[int, ...] | list[int] | None = None,
    ) -> str:
        """
        Perform a regex search on the given string, using a single or a list of
        patterns returning the first matching group.
        In case of failure return a default value or raise a WARNING or a
        RegexNotFoundError, depending on fatal, specifying the field name.
        """

    def _search_json(
        self,
        start_pattern: str | re.Pattern[str],
        string: str | None,
        name: str,
        video_id: str,
        *,
        end_pattern: str | re.Pattern[str] = "",
        contains_pattern: str | re.Pattern[str] = r"{(?s:.+)}",
        fatal: bool = True,
        default: _StrNoDefaultOrNone = ...,
        cls: type[JSONDecoder] | None = None,
        object_hook: Callable[[dict[Any, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    ) -> Any:
        """Searches string for the JSON object specified by start_pattern"""

    def _html_search_regex(
        self,
        pattern: str | re.Pattern[str],
        string: str,
        name: str,
        default: _StrNoDefaultOrNone = ...,
        fatal: bool = True,
        flags: int = 0,
        group: int | None = None,
    ) -> str | tuple[str, ...]:
        """
        Like _search_regex, but strips HTML tags and unescapes entities.
        """

    def _get_netrc_login_info(self, netrc_machine: str | None = None) -> tuple[str | None, str | None]: ...
    def _get_login_info(
        self, username_option: str = "username", password_option: str = "password", netrc_machine: str | None = None
    ) -> tuple[str | None, str | None]:
        """
        Get the login info as (username, password)
        First look for the manually specified credentials using username_option
        and password_option as keys in params dictionary. If no such credentials
        are available try the netrc_cmd if it is defined or look in the
        netrc file using the netrc_machine or _NETRC_MACHINE value.
        If there's no info available, return (None, None)
        """

    def _get_tfa_info(self, note: str = "two-factor verification code") -> str:
        """
        Get the two-factor authentication info
        TODO - asking the user will be required for sms/phone verify
        currently just uses the command line option
        If there's no info available, return None
        """

    @staticmethod
    def _og_regexes(prop: str) -> list[str]: ...
    @staticmethod
    def _meta_regex(prop: str) -> str: ...
    def _og_search_property(
        self, prop: str, html: str, name: str | None = None, *, default: type[NO_DEFAULT] | str = ..., fatal: bool = False
    ) -> str | None: ...
    def _og_search_thumbnail(self, html: str, *, default: type[NO_DEFAULT] | str = ...) -> str | None: ...
    def _og_search_description(self, html: str, *, default: type[NO_DEFAULT] | str = ...) -> str | None: ...
    def _og_search_title(self, html: str, *, fatal: bool = False, default: type[NO_DEFAULT] | str = ...) -> str | None: ...
    def _og_search_video_url(
        self,
        html: str,
        name: str = "video url",
        secure: bool = True,
        *,
        default: type[NO_DEFAULT] | str = ...,
        fatal: bool = False,
    ) -> str | None: ...
    def _og_search_url(self, html: str, *, default: type[NO_DEFAULT] | str = ..., fatal: bool = False) -> str | None: ...
    def _html_extract_title(
        self,
        html: str,
        name: str = "title",
        *,
        default: type[NO_DEFAULT] | str = ...,
        flags: int = 0,
        group: tuple[int, ...] | list[int] | None = None,
        fatal: bool = False,
    ) -> str | None: ...
    def _html_search_meta(
        self,
        name: str,
        html: str,
        display_name: str | None = None,
        fatal: bool = False,
        flags: int = 0,
        group: tuple[int, ...] | list[int] | None = None,
    ) -> str | None: ...
    def _dc_search_uploader(self, html: str) -> str | None: ...
    @staticmethod
    def _rta_search(html: str) -> int: ...
    def _media_rating_search(self, html: str) -> int: ...
    def _family_friendly_search(self, html: str) -> int: ...
    def _twitter_search_player(self, html: str) -> str | None: ...
    def _yield_json_ld(
        self, html: str, video_id: str, *, fatal: bool = True, default: type[NO_DEFAULT] | bool = ...
    ) -> Iterator[dict[str, Any]]:
        """Yield all json ld objects in the html"""

    def _search_json_ld(
        self,
        html: str,
        video_id: str,
        expected_type: Iterable[str] | str | None = None,
        *,
        fatal: bool = True,
        default: type[NO_DEFAULT] | bool = ...,
    ) -> dict[str, Any]:
        """Search for a video in any json ld in the html"""
    # json_ld parameter is passed to json.loads().
    def _json_ld(
        self, json_ld: Any, video_id: str, fatal: bool = True, expected_type: Iterable[str] | str | None = None
    ) -> dict[str, Any]: ...
    def _search_nextjs_data(
        self, webpage: str, video_id: str, *, fatal: bool = True, default: type[NO_DEFAULT] | bool = ..., **kw: Any
    ) -> Any: ...
    def _search_nuxt_data(
        self,
        webpage: str,
        video_id: str,
        context_name: str = "__NUXT__",
        *,
        fatal: bool = True,
        traverse: tuple[str, int] = ("data", 0),
    ) -> Any:
        """Parses Nuxt.js metadata. This works as long as the function __NUXT__ invokes is a pure function"""

    @staticmethod
    def _hidden_inputs(html: str) -> dict[str, Any]: ...
    def _form_hidden_inputs(self, form_id: str, html: str) -> dict[str, Any]: ...
    def _check_formats(self, formats: list[dict[str, Any]], video_id: str) -> None: ...
    @staticmethod
    def _remove_duplicate_formats(formats: list[dict[str, Any]]) -> None: ...
    def _is_valid_url(self, url: str, video_id: str, item: str = "video", headers: Mapping[str, Any] = ...) -> bool: ...
    def _proto_relative_url(self, url: str, scheme: str | None = None) -> str: ...
    def _sleep(self, timeout: float, video_id: str, msg_template: str | None = None) -> None: ...
    def _extract_f4m_formats(
        self,
        manifest_url: str,
        video_id: str,
        preference: Any = None,
        quality: Any = None,
        f4m_id: str | None = None,
        transform_source: Callable[..., str] = ...,
        fatal: bool = True,
        m3u8_id: str | None = None,
        data: str | None = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> list[dict[str, Any]]: ...
    def _parse_f4m_formats(
        self,
        manifest: str,
        manifest_url: str,
        video_id: str,
        preference: Any = None,
        quality: Any = None,
        f4m_id: str | None = None,
        transform_source: Callable[..., str] = ...,
        fatal: bool = True,
        m3u8_id: str | None = None,
    ) -> list[dict[str, Any]]: ...
    def _m3u8_meta_format(
        self, m3u8_url: str, ext: str | None = None, preference: Any = None, quality: Any = None, m3u8_id: str | None = None
    ) -> dict[str, Any]: ...
    def _report_ignoring_subs(self, name: str) -> None: ...
    def _extract_m3u8_formats(
        self,
        m3u8_url: str,
        video_id: str,
        ext: str | None = None,
        entry_protocol: str = "m3u8_native",
        preference: Any = None,
        quality: Any = None,
        m3u8_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        live: bool = False,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> list[dict[str, Any]]: ...
    def _extract_m3u8_formats_and_subtitles(
        self,
        m3u8_url: str,
        video_id: str,
        ext: str | None = None,
        entry_protocol: str = "m3u8_native",
        preference: Any = None,
        quality: Any = None,
        m3u8_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        live: bool = False,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _parse_m3u8_formats_and_subtitles(
        self,
        m3u8_doc: str,
        m3u8_url: str | None = None,
        ext: str | None = None,
        entry_protocol: str = "m3u8_native",
        preference: Any = None,
        quality: Any = None,
        m3u8_id: str | None = None,
        live: bool = False,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
        video_id: str | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _extract_m3u8_vod_duration(
        self,
        m3u8_vod_url: str,
        video_id: str,
        note: str | None = None,
        errnote: str | None = None,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> int | None: ...
    def _parse_m3u8_vod_duration(self, m3u8_vod: str, video_id: str) -> int: ...
    def _extract_mpd_vod_duration(
        self,
        mpd_url: str,
        video_id: str,
        note: str | None = None,
        errnote: str | None = None,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> int | None: ...
    @staticmethod
    def _xpath_ns(path: str, namespace: str | None = None) -> str: ...
    def _extract_smil_formats_and_subtitles(
        self,
        smil_url: str,
        video_id: str,
        fatal: bool = True,
        f4m_params: Mapping[str, Any] | None = None,
        transform_source: Callable[..., str] | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _extract_smil_formats(
        self,
        smil: ET.Element,
        smil_url: str,
        video_id: str,
        namespace: str | None = None,
        f4m_params: Mapping[str, Any] | None = None,
        transform_rtmp_url: Callable[[str, str], tuple[str, str]] | None = None,
    ) -> list[dict[str, Any]]: ...
    def _extract_smil_info(
        self, smil_url: str, video_id: str, fatal: bool = True, f4m_params: Mapping[str, Any] | None = None
    ) -> dict[str, Any]: ...
    def _download_smil(
        self, smil_url: str, video_id: str, fatal: bool = True, transform_source: Callable[..., str] | None = None
    ) -> ET.Element: ...
    def _parse_smil(
        self, smil: ET.Element, smil_url: str, video_id: str, f4m_params: Mapping[str, Any] | None = None
    ) -> dict[str, Any]: ...
    def _parse_smil_namespace(self, smil: str) -> str | None: ...
    def _parse_smil_formats(
        self,
        smil: ET.Element,
        smil_url: str,
        video_id: str,
        namespace: str | None = None,
        f4m_params: Mapping[str, Any] | None = None,
        transform_rtmp_url: Callable[[str, str], tuple[str, str]] | None = None,
    ) -> list[dict[str, Any]]: ...
    def _parse_smil_formats_and_subtitles(
        self,
        smil: ET.Element,
        smil_url: str,
        video_id: str,
        namespace: str | None = None,
        f4m_params: Mapping[str, Any] | None = None,
        transform_rtmp_url: Callable[[str, str], tuple[str, str]] | None = None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _parse_smil_subtitles(
        self, smil: ET.Element, namespace: str | None = None, subtitles_lang: str = "en"
    ) -> list[dict[str, Any]]: ...
    def _extract_xspf_playlist(self, xspf_url: str, playlist_id: str, fatal: bool = True) -> list[dict[str, Any]]: ...
    def _parse_xspf(
        self, xspf_doc: ET.Element, playlist_id: str, xspf_url: str | None = None, xspf_base_url: str | None = None
    ) -> list[dict[str, Any]]: ...
    def _extract_mpd_formats(
        self,
        mpd_url: str,
        video_id: str,
        mpd_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> list[dict[str, Any]]: ...
    def _extract_mpd_formats_and_subtitles(
        self,
        mpd_url: str,
        video_id: str,
        mpd_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _extract_mpd_periods(
        self,
        mpd_url: str,
        video_id: str,
        mpd_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> tuple[list[Any], dict[str, Any]]: ...
    def _parse_mpd_formats_and_subtitles(
        self,
        mpd_url: str,
        video_id: str,
        mpd_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _merge_mpd_periods(self, periods: Iterable[Mapping[str, Any]]) -> tuple[list[Any], dict[str, Any]]:
        """
        Combine all formats and subtitles from an MPD manifest into a single list,
        by concatenate streams with similar formats.
        """

    def _parse_mpd_periods(
        self, mpd_doc: ET.Element, mpd_id: str | None = None, mpd_base_url: str = "", mpd_url: str | None = None
    ) -> tuple[list[Any], dict[str, Any]]:
        """
        Parse formats from MPD manifest.
        References:
         1. MPEG-DASH Standard, ISO/IEC 23009-1:2014(E),
            http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip
         2. https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP
        """

    def _extract_ism_formats(
        self,
        ism_url: str,
        video_id: str,
        ism_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> list[dict[str, Any]]: ...
    def _extract_ism_formats_and_subtitles(
        self,
        ism_url: str,
        video_id: str,
        ism_id: str | None = None,
        note: str | None = None,
        errnote: str | None = None,
        fatal: bool = True,
        data: Any = None,
        headers: Mapping[str, Any] = ...,
        query: Mapping[str, Any] = ...,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _parse_ism_formats_and_subtitles(
        self, ism_doc: str, ism_url: str, ism_id: str | None = None
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Parse formats from ISM manifest.
        References:
         1. [MS-SSTR]: Smooth Streaming Protocol,
            https://msdn.microsoft.com/en-us/library/ff469518.aspx
        """

    def _parse_html5_media_entries(
        self,
        base_url: str,
        webpage: str,
        video_id: str,
        m3u8_id: str | None = None,
        m3u8_entry_protocol: str = "m3u8_native",
        mpd_id: str | None = None,
        preference: Any = None,
        quality: Any = None,
        _headers: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]: ...
    def _extract_akamai_formats(
        self, manifest_url: str, video_id: str, hosts: Mapping[str, Any] = ...
    ) -> list[dict[str, Any]]: ...
    def _extract_akamai_formats_and_subtitles(
        self, manifest_url: str, video_id: str, hosts: Mapping[str, Any] = ...
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...
    def _extract_wowza_formats(
        self, url: str, video_id: str, m3u8_entry_protocol: str = "m3u8_native", skip_protocols: Collection[str] = ...
    ) -> list[dict[str, Any]]: ...
    def _find_jwplayer_data(
        self, webpage: str, video_id: str | None = None, transform_source: Callable[..., str] = ...
    ) -> Any: ...
    def _extract_jwplayer_data(
        self,
        webpage: str,
        video_id: str,
        *args: Any,
        transform_source: Callable[..., str] = ...,
        require_title: bool = True,
        m3u8_id: str | None = None,
        mpd_id: str | None = None,
        rtmp_params: Mapping[str, Any] | None = None,
        base_url: str | None = None,
    ) -> list[dict[str, Any]]: ...
    def _parse_jwplayer_data(
        self,
        jwplayer_data: Mapping[str, Any],
        video_id: str | None = None,
        require_title: bool = True,
        m3u8_id: str | None = None,
        mpd_id: str | None = None,
        rtmp_params: Mapping[str, Any] | None = None,
        base_url: str | None = None,
    ) -> list[dict[str, Any]]: ...
    def _parse_jwplayer_formats(
        self,
        jwplayer_sources_data: Iterable[Mapping[str, Any]],
        video_id: str | None = None,
        m3u8_id: str | None = None,
        mpd_id: str | None = None,
        rtmp_params: Mapping[str, Any] | None = None,
        base_url: str | None = None,
    ) -> list[dict[str, Any]]: ...
    def _int(
        self,
        v: Any,
        name: str,
        fatal: bool = False,
        *,
        scale: int = 1,
        default: int | None = None,
        get_attr: str | None = None,
        invscale: int = 1,
        base: int | None = None,
    ) -> int | None: ...
    def _float(
        self, v: Any, name: str, fatal: bool = False, *, scale: int = 1, invscale: int = 1, default: float | None = None
    ) -> float | None: ...
    def _set_cookie(
        self,
        domain: str,
        name: str,
        value: str,
        expire_time: int | None = None,
        port: int | None = None,
        path: str = "/",
        secure: bool = False,
        discard: bool = False,
        rest: dict[str, Any] = ...,
        **kwargs: Unused,
    ) -> None: ...
    def _live_title(self, name: _T) -> _T: ...
    def _get_cookies(self, url: str) -> LenientSimpleCookie:
        """Return a http.cookies.SimpleCookie with the cookies for the url"""

    def _apply_first_set_cookie_header(self, url_handle: Response, cookie: str) -> None:
        """
        Apply first Set-Cookie header instead of the last. Experimental.

        Some sites (e.g. [1-3]) may serve two cookies under the same name
        in Set-Cookie header and expect the first (old) one to be set rather
        than second (new). However, as of RFC6265 the newer one cookie
        should be set into cookie store what actually happens.
        We will workaround this issue by resetting the cookie to
        the first one manually.
        1. https://new.vk.com/
        2. https://github.com/ytdl-org/youtube-dl/issues/9841#issuecomment-227871201
        3. https://learning.oreilly.com/
        """

    @property
    def _RETURN_TYPE(cls) -> str:
        """What the extractor returns: "video", "playlist", "any", or None (Unknown)"""

    def _get_subtitles(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]: ...  # Not implemented here.
    # Passes *args and **kwargs to _get_comments.
    def extract_comments(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]: ...
    def _get_comments(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]: ...  # Not implemented here.
    @staticmethod
    def _merge_subtitle_items(
        subtitle_list1: Iterable[Mapping[str, Any]], subtitle_list2: Iterable[Mapping[str, Any]]
    ) -> list[dict[str, Any]]:
        """Merge subtitle items for one language. Items with duplicated URLs/data
        will be dropped.
        """

    @classmethod
    def _merge_subtitles(cls, *dicts: dict[str, Any], target: Any = None) -> dict[str, Any]:
        """Merge subtitle dictionaries, language by language."""
    # Calls _get_automatic_captions which only raises NotImplementedError here.
    def extract_automatic_captions(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    @cached_property
    def _cookies_passed(self) -> bool:
        """Whether cookies have been passed to YoutubeDL"""

    def _mark_watched(self, *args: Any, **kwargs: Any) -> Any: ...  # Not implemented here.
    @staticmethod
    def _generic_id(url: str) -> str: ...
    def _generic_title(self, url: str = "", webpage: str = "", *, default: str | None = None) -> str | None: ...
    def _extract_chapters_helper(
        self,
        chapter_list: Iterable[Mapping[str, Any]],
        start_function: Callable[..., Any],
        title_function: Callable[..., Any],
        duration: float,
        strict: bool = True,
    ) -> list[dict[str, int]] | None: ...
    def _extract_chapters_from_description(
        self, description: str | None, duration: str | None
    ) -> list[dict[str, int]] | None: ...
    # Passes *args and **kwargs to _mark_watched which only raises NotImplementedError here.
    def mark_watched(self, *args: Any, **kwargs: Any) -> None: ...
    def geo_verification_headers(self) -> dict[str, str]: ...
    # kwargs passed to _error_callback.
    def RetryManager(self, *, _retries: int | None, _error_callback: Callable[..., Any], **kwargs: Any) -> _RetryManager: ...
    @classmethod
    def extract_from_webpage(cls, ydl: YoutubeDL, url: str, webpage: str) -> Iterator[_InfoDict]: ...
    def _yes_playlist(
        self,
        playlist_id: str,
        video_id: str,
        smuggled_data: Any = None,
        *,
        playlist_label: str = "playlist",
        video_label: str = "video",
    ) -> bool: ...
    def _error_or_warning(self, err: str, _count: int | None = None, _retries: int = 0, *, fatal: bool = True) -> None: ...
    def _extract_generic_embeds(
        self, url: str, *args: Unused, info_dict: _InfoDict = ..., note: str = "Extracting generic embeds", **kwargs: Unused
    ) -> list[dict[str, Any]]: ...
    @classmethod
    def _extract_from_webpage(cls, url: str, webpage: str) -> Iterator[_InfoDict]: ...
    @classmethod
    def _extract_embed_urls(cls, url: str, webpage: str) -> Iterator[str]:
        """@returns all the embed urls on the webpage"""

    @classmethod
    def _extract_url(cls, webpage: str) -> str | None:
        """Only for compatibility with some older extractors"""

    @classmethod
    def __init_subclass__(cls, *, plugin_name: str | None = None, **kwargs: Any) -> None: ...

    class StopExtraction(Exception): ...

    class CommentsDisabled(Exception):
        """Raise in _get_comments if comments are disabled for the video"""

class SearchInfoExtractor(InfoExtractor):
    """
    Base class for paged search queries extractors.
    They accept URLs in the format _SEARCH_KEY(|all|[0-9]):{query}
    Instances should define _SEARCH_KEY and optionally _MAX_RESULTS
    """

    def _real_extract(self, query: str) -> _InfoDict: ...
    def _get_n_results(self, query: str, n: int) -> list[_InfoDict]:
        """Get a specified number of results for a query.
        Either this function or _search_results must be overridden by subclasses
        """

    def _search_results(self, query: str) -> list[_InfoDict]:
        """Returns an iterator of search results"""

class UnsupportedURLIE(InfoExtractor): ...
