import datetime
import io
from _typeshed import OptExcInfo, SupportsKeysAndGetItem, SupportsNoArgReadline, SupportsRead, WriteableBuffer
from _typeshed.wsgi import WSGIApplication, WSGIEnvironment
from collections.abc import Iterable, Mapping
from re import Pattern
from typing import IO, Any, ClassVar, Literal, Protocol, TypedDict, TypeVar, overload
from typing_extensions import Self, TypeAlias

from webob._types import AsymmetricProperty, AsymmetricPropertyWithDelete, SymmetricProperty, SymmetricPropertyWithDelete
from webob.acceptparse import _AcceptCharsetProperty, _AcceptEncodingProperty, _AcceptLanguageProperty, _AcceptProperty
from webob.byterange import Range
from webob.cachecontrol import CacheControl
from webob.client import SendRequest
from webob.compat import cgi_FieldStorage
from webob.cookies import RequestCookies
from webob.descriptors import _authorization, _DateProperty
from webob.etag import IfRange, IfRangeDate, _ETagProperty
from webob.headers import EnvironHeaders
from webob.multidict import GetDict, MultiDict, NestedMultiDict, NoVars
from webob.response import Response

__all__ = ["BaseRequest", "Request", "LegacyRequest"]

_T = TypeVar("_T")
_HTTPMethod: TypeAlias = Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
_ListOrTuple: TypeAlias = list[_T] | tuple[_T, ...]
_RequestCacheControl: TypeAlias = CacheControl[Literal["request"]]

class _SupportsReadAndNoArgReadline(SupportsRead[str | bytes], SupportsNoArgReadline[str | bytes], Protocol): ...

class _RequestCacheControlDict(TypedDict, total=False):
    max_stale: int
    min_stale: int
    only_if_cached: bool
    no_cache: Literal[True] | str
    no_store: bool
    no_transform: bool
    max_age: int

_FieldStorageWithFile = cgi_FieldStorage

class _NoDefault: ...

NoDefault: _NoDefault

class BaseRequest:
    request_body_tempfile_limit: ClassVar[int]
    environ: WSGIEnvironment
    def __init__(self, environ: WSGIEnvironment, **kw: Any) -> None: ...
    @overload
    def encget(self, key: str, default: _T, encattr: str | None = None) -> str | _T: ...
    @overload
    def encget(self, key: str, *, encattr: str | None = None) -> str: ...
    def encset(self, key: str, val: str, encattr: str | None = None) -> None: ...
    @property
    def charset(self) -> str | None: ...
    def decode(self, charset: str | None = None, errors: str = "strict") -> Self: ...
    @property
    def body_file(self) -> SupportsRead[bytes]:
        """
        Input stream of the request (wsgi.input).
        Setting this property resets the content_length and seekable flag
        (unlike setting req.body_file_raw).
        """

    @body_file.setter
    def body_file(self, value: SupportsRead[bytes]) -> None: ...
    @body_file.deleter
    def body_file(self) -> None: ...
    content_length: SymmetricPropertyWithDelete[int | None]
    body_file_raw: SymmetricProperty[SupportsRead[bytes]]
    is_body_seekable: bool
    @property
    def body_file_seekable(self) -> IO[bytes]:
        """
        Get the body of the request (wsgi.input) as a seekable file-like
        object. Middleware and routing applications should use this
        attribute over .body_file.

        If you access this value, CONTENT_LENGTH will also be updated.
        """
    url_encoding: AsymmetricPropertyWithDelete[str, str | None]
    scheme: SymmetricProperty[str]
    method: AsymmetricPropertyWithDelete[_HTTPMethod, _HTTPMethod | None]
    http_version: SymmetricProperty[str]
    remote_user: SymmetricPropertyWithDelete[str | None]
    remote_host: SymmetricPropertyWithDelete[str | None]
    remote_addr: SymmetricPropertyWithDelete[str | None]
    query_string: AsymmetricPropertyWithDelete[str, str | None]
    server_name: SymmetricProperty[str]
    server_port: SymmetricProperty[int]
    script_name: AsymmetricPropertyWithDelete[str, str | None]
    path_info: SymmetricProperty[str]
    uscript_name = script_name  # bw compat
    upath_info = path_info  # bw compat
    content_type: AsymmetricPropertyWithDelete[str, str | None]
    headers: AsymmetricProperty[EnvironHeaders, SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]]]
    @property
    def client_addr(self) -> str | None:
        """
        The effective client IP address as a string.  If the
        ``HTTP_X_FORWARDED_FOR`` header exists in the WSGI environ, this
        attribute returns the client IP address present in that header
        (e.g. if the header value is ``192.168.1.1, 192.168.1.2``, the value
        will be ``192.168.1.1``). If no ``HTTP_X_FORWARDED_FOR`` header is
        present in the environ at all, this attribute will return the value
        of the ``REMOTE_ADDR`` header.  If the ``REMOTE_ADDR`` header is
        unset, this attribute will return the value ``None``.

        .. warning::

           It is possible for user agents to put someone else's IP or just
           any string in ``HTTP_X_FORWARDED_FOR`` as it is a normal HTTP
           header. Forward proxies can also provide incorrect values (private
           IP addresses etc).  You cannot "blindly" trust the result of this
           method to provide you with valid data unless you're certain that
           ``HTTP_X_FORWARDED_FOR`` has the correct values.  The WSGI server
           must be behind a trusted proxy for this to be true.
        """

    @property
    def host_port(self) -> str:
        """
        The effective server port number as a string.  If the ``HTTP_HOST``
        header exists in the WSGI environ, this attribute returns the port
        number present in that header. If the ``HTTP_HOST`` header exists but
        contains no explicit port number: if the WSGI url scheme is "https" ,
        this attribute returns "443", if the WSGI url scheme is "http", this
        attribute returns "80" .  If no ``HTTP_HOST`` header is present in
        the environ at all, this attribute will return the value of the
        ``SERVER_PORT`` header (which is guaranteed to be present).
        """

    @property
    def host_url(self) -> str:
        """
        The URL through the host (no path)
        """

    @property
    def application_url(self) -> str:
        """
        The URL including SCRIPT_NAME (no PATH_INFO or query string)
        """

    @property
    def path_url(self) -> str:
        """
        The URL including SCRIPT_NAME and PATH_INFO, but not QUERY_STRING
        """

    @property
    def path(self) -> str:
        """
        The path of the request, without host or query string
        """

    @property
    def path_qs(self) -> str:
        """
        The path of the request, without host but with query string
        """

    @property
    def url(self) -> str:
        """
        The full request URL, including QUERY_STRING
        """

    def relative_url(self, other_url: str, to_application: bool = False) -> str:
        """
        Resolve other_url relative to the request URL.

        If ``to_application`` is True, then resolve it relative to the
        URL with only SCRIPT_NAME
        """

    def path_info_pop(self, pattern: Pattern[str] | None = None) -> str | None:
        """
        'Pops' off the next segment of PATH_INFO, pushing it onto
        SCRIPT_NAME, and returning the popped segment.  Returns None if
        there is nothing left on PATH_INFO.

        Does not return ``''`` when there's an empty segment (like
        ``/path//path``); these segments are just ignored.

        Optional ``pattern`` argument is a regexp to match the return value
        before returning. If there is no match, no changes are made to the
        request and None is returned.
        """

    def path_info_peek(self) -> str | None:
        """
        Returns the next segment on PATH_INFO, or None if there is no
        next segment.  Doesn't modify the environment.
        """
    urlvars: SymmetricPropertyWithDelete[dict[str, str]]
    urlargs: SymmetricPropertyWithDelete[tuple[str, ...]]
    @property
    def is_xhr(self) -> bool:
        """Is X-Requested-With header present and equal to ``XMLHttpRequest``?

        Note: this isn't set by every XMLHttpRequest request, it is
        only set if you are using a Javascript library that sets it
        (or you set the header yourself manually).  Currently
        Prototype and jQuery are known to set this header.
        """
    host: SymmetricPropertyWithDelete[str]
    @property
    def domain(self) -> str:
        """Returns the domain portion of the host value.  Equivalent to:

        .. code-block:: python

           domain = request.host
           if ':' in domain and domain[-1] != ']': # Check for ] because of IPv6
               domain = domain.rsplit(':', 1)[0]

        This will be equivalent to the domain portion of the ``HTTP_HOST``
        value in the environment if it exists, or the ``SERVER_NAME`` value in
        the environment if it doesn't.  For example, if the environment
        contains an ``HTTP_HOST`` value of ``foo.example.com:8000``,
        ``request.domain`` will return ``foo.example.com``.

        Note that this value cannot be *set* on the request.  To set the host
        value use :meth:`webob.request.Request.host` instead.
        """

    @property
    def body(self) -> bytes:
        """
        Return the content of the request body.
        """

    @body.setter
    def body(self, value: bytes | None) -> None: ...
    @body.deleter
    def body(self) -> None: ...
    json: SymmetricPropertyWithDelete[Any]
    json_body: SymmetricPropertyWithDelete[Any]
    text: SymmetricPropertyWithDelete[str]
    @property
    def POST(self) -> MultiDict[str, str | _FieldStorageWithFile] | NoVars:
        """
        Return a MultiDict containing all the variables from a form
        request. Returns an empty dict-like object for non-form requests.

        Form requests are typically POST requests, however any other
        requests with an appropriate Content-Type are also supported.
        """

    @property
    def GET(self) -> GetDict:
        """
        Return a MultiDict containing all the variables from the
        QUERY_STRING.
        """

    @property
    def params(self) -> NestedMultiDict[str, str | _FieldStorageWithFile]:
        """
        A dictionary-like object containing both the parameters from
        the query string and request body.
        """
    cookies: AsymmetricProperty[RequestCookies, SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]]]
    def copy(self) -> Self:
        """
        Copy the request and environment object.

        This only does a shallow copy, except of wsgi.input
        """

    def copy_get(self) -> Self:
        """
        Copies the request and environment object, but turning this request
        into a GET along the way.  If this was a POST request (or any other
        verb) then it becomes GET, and the request body is thrown away.
        """

    @property
    def is_body_readable(self) -> bool:
        """
        webob.is_body_readable is a flag that tells us that we can read the
        input stream even though CONTENT_LENGTH is missing.
        """

    @is_body_readable.setter
    def is_body_readable(self, flag: bool) -> None: ...
    def make_body_seekable(self) -> None:
        """
        This forces ``environ['wsgi.input']`` to be seekable.
        That means that, the content is copied into a BytesIO or temporary
        file and flagged as seekable, so that it will not be unnecessarily
        copied again.

        After calling this method the .body_file is always seeked to the
        start of file and .content_length is not None.

        The choice to copy to BytesIO is made from
        ``self.request_body_tempfile_limit``
        """

    def copy_body(self) -> None:
        """
        Copies the body, in cases where it might be shared with another request
        object and that is not desired.

        This copies the body either into a BytesIO object (through setting
        req.body) or a temporary file.
        """

    def make_tempfile(self) -> io.BufferedRandom:
        """
        Create a tempfile to store big request body.
        This API is not stable yet. A 'size' argument might be added.
        """

    def remove_conditional_headers(
        self, remove_encoding: bool = True, remove_range: bool = True, remove_match: bool = True, remove_modified: bool = True
    ) -> None:
        """
        Remove headers that make the request conditional.

        These headers can cause the response to be 304 Not Modified,
        which in some cases you may not want to be possible.

        This does not remove headers like If-Match, which are used for
        conflict detection.
        """
    accept: _AcceptProperty
    accept_charset: _AcceptCharsetProperty
    accept_encoding: _AcceptEncodingProperty
    accept_language: _AcceptLanguageProperty
    authorization: AsymmetricPropertyWithDelete[_authorization | None, tuple[str, str | dict[str, str]] | list[Any] | str | None]
    cache_control: AsymmetricPropertyWithDelete[
        _RequestCacheControl, _RequestCacheControl | _RequestCacheControlDict | str | None
    ]
    if_match: _ETagProperty
    if_none_match: _ETagProperty
    date: _DateProperty
    if_modified_since: _DateProperty
    if_unmodified_since: _DateProperty
    if_range: AsymmetricPropertyWithDelete[
        IfRange | IfRangeDate, IfRange | IfRangeDate | datetime.datetime | datetime.date | str | None
    ]
    max_forwards: SymmetricPropertyWithDelete[int | None]
    pragma: SymmetricPropertyWithDelete[str | None]
    range: AsymmetricPropertyWithDelete[Range | None, tuple[int, int | None] | list[int | None] | list[int] | str | None]
    referer: SymmetricPropertyWithDelete[str | None]
    referrer = referer
    user_agent: SymmetricPropertyWithDelete[str | None]
    def as_bytes(self, skip_body: bool = False) -> bytes:
        """
        Return HTTP bytes representing this request.
        If skip_body is True, exclude the body.
        If skip_body is an integer larger than one, skip body
        only if its length is bigger than that number.
        """

    def as_text(self) -> str: ...
    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        """
        Create a request from HTTP bytes data. If the bytes contain
        extra data after the request, raise a ValueError.
        """

    @classmethod
    def from_text(cls, s: str) -> Self: ...
    @classmethod
    def from_file(cls, fp: _SupportsReadAndNoArgReadline) -> Self:
        """Read a request from a file-like object (it must implement
        ``.read(size)`` and ``.readline()``).

        It will read up to the end of the request, not the end of the
        file (unless the request is a POST or PUT and has no
        Content-Length, in that case, the entire file is read).

        This reads the request as represented by ``str(req)``; it may
        not read every valid HTTP request properly.
        """

    @overload
    def call_application(
        self, application: WSGIApplication, catch_exc_info: Literal[False] = False
    ) -> tuple[str, list[tuple[str, str]], Iterable[bytes]]:
        """
        Call the given WSGI application, returning ``(status_string,
        headerlist, app_iter)``

        Be sure to call ``app_iter.close()`` if it's there.

        If catch_exc_info is true, then returns ``(status_string,
        headerlist, app_iter, exc_info)``, where the fourth item may
        be None, but won't be if there was an exception.  If you don't
        do this and there was an exception, the exception will be
        raised directly.
        """

    @overload
    def call_application(
        self, application: WSGIApplication, catch_exc_info: Literal[True]
    ) -> tuple[str, list[tuple[str, str]], Iterable[bytes], OptExcInfo | None]: ...
    @overload
    def call_application(
        self, application: WSGIApplication, catch_exc_info: bool
    ) -> (
        tuple[str, list[tuple[str, str]], Iterable[bytes], OptExcInfo | None] | tuple[str, list[tuple[str, str]], Iterable[bytes]]
    ): ...
    ResponseClass: type[Response]
    def send(self, application: WSGIApplication | None = None, catch_exc_info: bool = False) -> Response:
        """
        Like ``.call_application(application)``, except returns a
        response object with ``.status``, ``.headers``, and ``.body``
        attributes.

        This will use ``self.ResponseClass`` to figure out the class
        of the response object to return.

        If ``application`` is not given, this will send the request to
        ``self.make_default_send_app()``
        """
    get_response = send
    def make_default_send_app(self) -> SendRequest: ...
    @classmethod
    def blank(
        cls,
        path: str,
        environ: dict[str, None] | None = None,
        base_url: str | None = None,
        headers: Mapping[str, str] | None = None,
        POST: str | bytes | Mapping[Any, Any] | Mapping[Any, _ListOrTuple[Any]] | None = None,
        **kw: Any,
    ) -> Self:
        """
        Create a blank request environ (and Request wrapper) with the
        given path (path should be urlencoded), and any keys from
        environ.

        The path will become path_info, with any query string split
        off and used.

        All necessary keys will be added to the environ, but the
        values you pass in will take precedence.  If you pass in
        base_url then wsgi.url_scheme, HTTP_HOST, and SCRIPT_NAME will
        be filled in from that value.

        Any extra keyword will be passed to ``__init__``.
        """

class LegacyRequest(BaseRequest):
    @property  # type: ignore[override]
    def uscript_name(self) -> str:
        """upath_property('SCRIPT_NAME')"""

    @uscript_name.setter
    def uscript_name(self, value: str) -> None: ...
    @property  # type:ignore[override]
    def upath_info(self) -> str:
        """upath_property('PATH_INFO')"""

    @upath_info.setter
    def upath_info(self, value: str) -> None: ...
    def encget(self, key: str, default: Any = ..., encattr: str | None = None) -> Any: ...

class AdhocAttrMixin:
    def __setattr__(self, attr: str, value: Any) -> None: ...
    def __getattr__(self, attr: str) -> Any: ...
    def __delattr__(self, attr: str) -> None: ...

class Request(AdhocAttrMixin, BaseRequest):
    """The default request implementation"""

    # this is so Request doesn't count as callable, it's not very pretty
    # but we run into trouble with overlapping overloads in wsgify if we
    # don't exclude __call__ from arbitrary attribute access
    __call__: None

class DisconnectionError(IOError): ...

def environ_from_url(path: str) -> WSGIEnvironment: ...
def environ_add_POST(
    env: WSGIEnvironment,
    data: str | bytes | Mapping[Any, Any] | Mapping[Any, _ListOrTuple[Any]] | None,
    content_type: str | None = None,
) -> None: ...

class LimitedLengthFile(io.RawIOBase):
    file: SupportsRead[bytes]
    maxlen: int
    remaining: int
    def __init__(self, file: SupportsRead[bytes], maxlen: int) -> None: ...
    def fileno(self) -> int: ...
    @staticmethod
    def readable() -> Literal[True]: ...
    def readinto(self, buff: WriteableBuffer) -> int: ...

class Transcoder:
    charset: str
    errors: str
    def __init__(self, charset: str, errors: str = "strict") -> None: ...
    def transcode_query(self, q: str) -> str: ...
    def transcode_fs(self, fs: cgi_FieldStorage, content_type: str) -> io.BytesIO: ...
