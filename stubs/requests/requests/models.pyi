"""
requests.models
~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""

import datetime
from _typeshed import Incomplete, MaybeNone, Unused
from collections.abc import Callable, Iterator
from json import JSONDecoder
from typing import Any
from typing_extensions import Self, TypeAlias

from urllib3 import exceptions as urllib3_exceptions, fields, filepost, util
from urllib3.response import HTTPResponse

from . import auth, cookies, exceptions, hooks, status_codes, utils
from .adapters import HTTPAdapter
from .cookies import RequestsCookieJar
from .structures import CaseInsensitiveDict as CaseInsensitiveDict

_JSON: TypeAlias = Any  # any object that can be serialized to JSON

default_hooks = hooks.default_hooks
HTTPBasicAuth = auth.HTTPBasicAuth
cookiejar_from_dict = cookies.cookiejar_from_dict
get_cookie_header = cookies.get_cookie_header
RequestField = fields.RequestField
encode_multipart_formdata = filepost.encode_multipart_formdata
parse_url = util.parse_url
DecodeError = urllib3_exceptions.DecodeError
ReadTimeoutError = urllib3_exceptions.ReadTimeoutError
ProtocolError = urllib3_exceptions.ProtocolError
LocationParseError = urllib3_exceptions.LocationParseError
HTTPError = exceptions.HTTPError
MissingSchema = exceptions.MissingSchema
InvalidURL = exceptions.InvalidURL
ChunkedEncodingError = exceptions.ChunkedEncodingError
ContentDecodingError = exceptions.ContentDecodingError
ConnectionError = exceptions.ConnectionError
StreamConsumedError = exceptions.StreamConsumedError
guess_filename = utils.guess_filename
get_auth_from_url = utils.get_auth_from_url
requote_uri = utils.requote_uri
stream_decode_response_unicode = utils.stream_decode_response_unicode
to_key_val_list = utils.to_key_val_list
parse_header_links = utils.parse_header_links
iter_slices = utils.iter_slices
guess_json_utf = utils.guess_json_utf
super_len = utils.super_len
to_native_string = utils.to_native_string
codes = status_codes.codes

REDIRECT_STATI: Incomplete
DEFAULT_REDIRECT_LIMIT: Incomplete
CONTENT_CHUNK_SIZE: Incomplete
ITER_CHUNK_SIZE: Incomplete

class RequestEncodingMixin:
    @property
    def path_url(self) -> str:
        """Build the path URL to use."""

class RequestHooksMixin:
    def register_hook(self, event, hook):
        """Properly register a hook."""

    def deregister_hook(self, event, hook):
        """Deregister a previously registered hook.
        Returns True if the hook existed, False if not.
        """

class Request(RequestHooksMixin):
    """A user-created :class:`Request <Request>` object.

    Used to prepare a :class:`PreparedRequest <PreparedRequest>`, which is sent to the server.

    :param method: HTTP method to use.
    :param url: URL to send.
    :param headers: dictionary of headers to send.
    :param files: dictionary of {filename: fileobject} files to multipart upload.
    :param data: the body to attach to the request. If a dictionary or
        list of tuples ``[(key, value)]`` is provided, form-encoding will
        take place.
    :param json: json for the body to attach to the request (if files or data is not specified).
    :param params: URL parameters to append to the URL. If a dictionary or
        list of tuples ``[(key, value)]`` is provided, form-encoding will
        take place.
    :param auth: Auth handler or (user, pass) tuple.
    :param cookies: dictionary or CookieJar of cookies to attach to this request.
    :param hooks: dictionary of callback hooks, for internal usage.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'https://httpbin.org/get')
      >>> req.prepare()
      <PreparedRequest [GET]>
    """

    hooks: Incomplete
    method: Incomplete
    url: Incomplete
    headers: Incomplete
    files: Incomplete
    data: Incomplete
    json: _JSON | None
    params: Incomplete
    auth: Incomplete
    cookies: Incomplete
    def __init__(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json: _JSON | None = None,
    ) -> None: ...
    def prepare(self) -> PreparedRequest:
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for transmission and returns it."""

class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    """The fully mutable :class:`PreparedRequest <PreparedRequest>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a :class:`Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import requests
      >>> req = requests.Request('GET', 'https://httpbin.org/get')
      >>> r = req.prepare()
      >>> r
      <PreparedRequest [GET]>

      >>> s = requests.Session()
      >>> s.send(r)
      <Response [200]>
    """

    method: str | None
    url: str | None
    headers: CaseInsensitiveDict[str]
    body: bytes | str | None
    hooks: Incomplete
    def __init__(self) -> None: ...
    def prepare(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    ) -> None:
        """Prepares the entire request with the given parameters."""

    def copy(self) -> PreparedRequest: ...
    def prepare_method(self, method) -> None:
        """Prepares the given HTTP method."""

    def prepare_url(self, url, params) -> None:
        """Prepares the given HTTP URL."""

    def prepare_headers(self, headers) -> None:
        """Prepares the given HTTP headers."""

    def prepare_body(self, data, files, json=None) -> None:
        """Prepares the given HTTP body data."""

    def prepare_content_length(self, body: bytes | str | None) -> None:
        """Prepare Content-Length header based on request method and body"""

    def prepare_auth(self, auth, url="") -> None:
        """Prepares the given HTTP auth data."""

    def prepare_cookies(self, cookies) -> None:
        """Prepares the given HTTP cookie data.

        This function eventually generates a ``Cookie`` header from the
        given cookies using cookielib. Due to cookielib's design, the header
        will not be regenerated if it already exists, meaning this function
        can only be called once for the life of the
        :class:`PreparedRequest <PreparedRequest>` object. Any subsequent calls
        to ``prepare_cookies`` will have no actual effect, unless the "Cookie"
        header is removed beforehand.
        """

    def prepare_hooks(self, hooks) -> None:
        """Prepares the given hooks."""

class Response:
    """The :class:`Response <Response>` object, which contains a
    server's response to an HTTP request.
    """

    __attrs__: Incomplete
    _content: bytes | None  # undocumented
    status_code: int
    headers: CaseInsensitiveDict[str]
    raw: HTTPResponse | MaybeNone
    url: str
    encoding: str | None
    history: list[Response]
    reason: str
    cookies: RequestsCookieJar
    elapsed: datetime.timedelta
    request: PreparedRequest
    connection: HTTPAdapter
    def __init__(self) -> None: ...
    def __bool__(self) -> bool:
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """

    def __nonzero__(self) -> bool:
        """Returns True if :attr:`status_code` is less than 400.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code, is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """

    def __iter__(self) -> Iterator[bytes]:
        """Allows you to use a response as an iterator."""

    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused) -> None: ...
    @property
    def next(self) -> PreparedRequest | None:
        """Returns a PreparedRequest for the next request in a redirect chain, if there is one."""

    @property
    def ok(self) -> bool:
        """Returns True if :attr:`status_code` is less than 400, False if not.

        This attribute checks if the status code of the response is between
        400 and 600 to see if there was a client error or a server error. If
        the status code is between 200 and 400, this will return True. This
        is **not** a check to see if the response code is ``200 OK``.
        """

    @property
    def is_redirect(self) -> bool:
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """

    @property
    def is_permanent_redirect(self) -> bool:
        """True if this Response one of the permanent versions of redirect."""

    @property
    def apparent_encoding(self) -> str:
        """The apparent encoding, provided by the charset_normalizer or chardet libraries."""

    def iter_content(self, chunk_size: int | None = 1, decode_unicode: bool = False) -> Iterator[Incomplete]:
        """Iterates over the response data.  When stream=True is set on the
        request, this avoids reading the content at once into memory for
        large responses.  The chunk size is the number of bytes it should
        read into memory.  This is not necessarily the length of each item
        returned as decoding can take place.

        chunk_size must be of type int or None. A value of None will
        function differently depending on the value of `stream`.
        stream=True will read data as it arrives in whatever size the
        chunks are received. If stream=False, data is returned as
        a single chunk.

        If decode_unicode is True, content will be decoded using the best
        available encoding based on the response.
        """

    def iter_lines(
        self, chunk_size: int | None = 512, decode_unicode: bool = False, delimiter: str | bytes | None = None
    ) -> Iterator[Incomplete]:
        """Iterates over the response data, one line at a time.  When
        stream=True is set on the request, this avoids reading the
        content at once into memory for large responses.

        .. note:: This method is not reentrant safe.
        """

    @property
    def content(self) -> bytes | MaybeNone:
        """Content of the response, in bytes."""

    @property
    def text(self) -> str:
        """Content of the response, in unicode.

        If Response.encoding is None, encoding will be guessed using
        ``charset_normalizer`` or ``chardet``.

        The encoding of the response content is determined based solely on HTTP
        headers, following RFC 2616 to the letter. If you can take advantage of
        non-HTTP knowledge to make a better guess at the encoding, you should
        set ``r.encoding`` appropriately before accessing this property.
        """

    def json(
        self,
        *,
        cls: type[JSONDecoder] | None = ...,
        object_hook: Callable[[dict[Any, Any]], Any] | None = ...,
        parse_float: Callable[[str], Any] | None = ...,
        parse_int: Callable[[str], Any] | None = ...,
        parse_constant: Callable[[str], Any] | None = ...,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = ...,
        **kwds: Any,
    ) -> Any:
        """Decodes the JSON response body (if any) as a Python object.

        This may return a dictionary, list, etc. depending on what is in the response.

        :param \\*\\*kwargs: Optional arguments that ``json.loads`` takes.
        :raises requests.exceptions.JSONDecodeError: If the response body does not
            contain valid json.
        """

    @property
    def links(self) -> dict[Incomplete, Incomplete]:
        """Returns the parsed header links of the response, if any."""

    def raise_for_status(self) -> None:
        """Raises :class:`HTTPError`, if one occurred."""

    def close(self) -> None:
        """Releases the connection back to the pool. Once this method has been
        called the underlying ``raw`` object must not be accessed again.

        *Note: Should not normally need to be called explicitly.*
        """
