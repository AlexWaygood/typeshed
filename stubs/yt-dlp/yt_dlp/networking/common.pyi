import abc
import enum
import io
from _typeshed import Unused
from collections.abc import Callable, Iterable, Mapping
from email.message import Message
from logging import Logger
from typing import IO, Any
from typing_extensions import Self, TypeAlias

from ..cookies import YoutubeDLCookieJar
from ..utils._utils import _YDLLogger
from ..utils.networking import HTTPHeaderDict

DEFAULT_TIMEOUT: int
_RequestData: TypeAlias = bytes | Iterable[bytes] | IO[Any] | None
_Preference: TypeAlias = Callable[[RequestHandler, Request], int]

def register_preference(*handlers: type[RequestHandler]) -> Callable[..., object]: ...

class RequestDirector:
    """RequestDirector class

    Helper class that, when given a request, forward it to a RequestHandler that supports it.

    Preference functions in the form of func(handler, request) -> int
    can be registered into the `preferences` set. These are used to sort handlers
    in order of preference.

    @param logger: Logger instance.
    @param verbose: Print debug request information to stdout.
    """

    handlers: dict[str, RequestHandler]
    preferences: set[_Preference]
    logger: Logger
    verbose: bool
    def __init__(self, logger: Logger, verbose: bool = False) -> None: ...
    def close(self) -> None: ...
    def add_handler(self, handler: RequestHandler) -> None:
        """Add a handler. If a handler of the same RH_KEY exists, it will overwrite it"""

    def send(self, request: Request) -> Response:
        """
        Passes a request onto a suitable RequestHandler
        """

def register_rh(handler: RequestHandler) -> RequestHandler:
    """Register a RequestHandler class"""

class Features(enum.Enum):
    ALL_PROXY = 1
    NO_PROXY = 2

class RequestHandler(abc.ABC, metaclass=abc.ABCMeta):
    """Request Handler class

    Request handlers are class that, given a Request,
    process the request from start to finish and return a Response.

    Concrete subclasses need to redefine the _send(request) method,
    which handles the underlying request logic and returns a Response.

    RH_NAME class variable may contain a display name for the RequestHandler.
    By default, this is generated from the class name.

    The concrete request handler MUST have "RH" as the suffix in the class name.

    All exceptions raised by a RequestHandler should be an instance of RequestError.
    Any other exception raised will be treated as a handler issue.

    If a Request is not supported by the handler, an UnsupportedRequest
    should be raised with a reason.

    By default, some checks are done on the request in _validate() based on the following class variables:
    - `_SUPPORTED_URL_SCHEMES`: a tuple of supported url schemes.
        Any Request with an url scheme not in this list will raise an UnsupportedRequest.

    - `_SUPPORTED_PROXY_SCHEMES`: a tuple of support proxy url schemes. Any Request that contains
        a proxy url with an url scheme not in this list will raise an UnsupportedRequest.

    - `_SUPPORTED_FEATURES`: a tuple of supported features, as defined in Features enum.

    The above may be set to None to disable the checks.

    Parameters:
    @param logger: logger instance
    @param headers: HTTP Headers to include when sending requests.
    @param cookiejar: Cookiejar to use for requests.
    @param timeout: Socket timeout to use when sending requests.
    @param proxies: Proxies to use for sending requests.
    @param source_address: Client-side IP address to bind to for requests.
    @param verbose: Print debug request and traffic information to stdout.
    @param prefer_system_certs: Whether to prefer system certificates over other means (e.g. certifi).
    @param client_cert: SSL client certificate configuration.
            dict with {client_certificate, client_certificate_key, client_certificate_password}
    @param verify: Verify SSL certificates
    @param legacy_ssl_support: Enable legacy SSL options such as legacy server connect and older cipher support.

    Some configuration options may be available for individual Requests too. In this case,
    either the Request configuration option takes precedence or they are merged.

    Requests may have additional optional parameters defined as extensions.
     RequestHandler subclasses may choose to support custom extensions.

    If an extension is supported, subclasses should extend _check_extensions(extensions)
    to pop and validate the extension.
    - Extensions left in `extensions` are treated as unsupported and UnsupportedRequest will be raised.

    The following extensions are defined for RequestHandler:
    - `cookiejar`: Cookiejar to use for this request.
    - `timeout`: socket timeout to use for this request.
    - `legacy_ssl`: Enable legacy SSL options for this request. See legacy_ssl_support.
    - `keep_header_casing`: Keep the casing of headers when sending the request.
    To enable these, add extensions.pop('<extension>', None) to _check_extensions

    Apart from the url protocol, proxies dict may contain the following keys:
    - `all`: proxy to use for all protocols. Used as a fallback if no proxy is set for a specific protocol.
    - `no`: comma seperated list of hostnames (optionally with port) to not use a proxy for.
    Note: a RequestHandler may not support these, as defined in `_SUPPORTED_FEATURES`.

    """

    headers: HTTPHeaderDict | dict[str, str]
    cookiejar: YoutubeDLCookieJar | None
    timeout: float | int
    proxies: Mapping[str, Any] | dict[str, Any]
    source_address: str | None
    verbose: bool
    prefer_system_certs: bool
    verify: bool
    legacy_ssl_support: bool
    def __init__(
        self,
        *,
        logger: _YDLLogger,
        headers: HTTPHeaderDict | Mapping[str, str] | None = None,
        cookiejar: YoutubeDLCookieJar | None = None,
        timeout: float | None = None,
        proxies: Mapping[str, Any] | None = None,
        source_address: str | None = None,
        verbose: bool = False,
        prefer_system_certs: bool = False,
        client_cert: dict[str, str | None] | None = None,
        verify: bool = True,
        legacy_ssl_support: bool = False,
        **_: Unused,
    ) -> None: ...
    def validate(self, request: Request) -> None: ...
    def send(self, request: Request) -> Response: ...
    def close(self) -> None: ...
    @property
    def RH_NAME(cls) -> str: ...
    @property
    def RH_KEY(cls) -> str: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...

class Request:
    """
    Represents a request to be made.
    Partially backwards-compatible with urllib.request.Request.

    @param url: url to send. Will be sanitized.
    @param data: payload data to send. Must be bytes, iterable of bytes, a file-like object or None
    @param headers: headers to send.
    @param proxies: proxy dict mapping of proto:proxy to use for the request and any redirects.
    @param query: URL query parameters to update the url with.
    @param method: HTTP method to use. If no method specified, will use POST if payload data is present else GET
    @param extensions: Dictionary of Request extensions to add, as supported by handlers.
    """

    proxies: Mapping[str, Any] | dict[str, Any]
    extensions: Mapping[str, Any] | dict[str, Any]
    def __init__(
        self,
        url: str,
        data: _RequestData | None = None,
        headers: HTTPHeaderDict | Mapping[str, str] | None = None,
        proxies: Mapping[str, Any] | None = None,
        query: Mapping[str, str] | None = None,
        method: str | None = None,
        extensions: Mapping[str, Any] | None = None,
    ) -> None: ...
    @property
    def url(self) -> str: ...
    @url.setter
    def url(self, url: str) -> None: ...
    @property
    def method(self) -> str: ...
    @method.setter
    def method(self, method: str) -> None: ...
    @property
    def data(self) -> _RequestData | io.IOBase: ...
    @data.setter
    def data(self, data: _RequestData) -> None: ...
    @property
    def headers(self) -> HTTPHeaderDict | dict[str, str]: ...
    @headers.setter
    def headers(self, new_headers: Mapping[str, str] | HTTPHeaderDict) -> None: ...
    def update(
        self,
        url: str | None = None,
        data: str | None = None,
        headers: HTTPHeaderDict | Mapping[str, str] | None = None,
        query: Mapping[str, str] | None = None,
        extensions: Mapping[str, Any] | None = None,
    ) -> None: ...
    def copy(self) -> Self: ...

def HEADRequest(
    url: str,
    data: _RequestData | None = None,
    headers: HTTPHeaderDict | Mapping[str, str] | None = None,
    proxies: Mapping[str, Any] | None = None,
    query: Mapping[str, str] | None = None,
    *,
    method: str = "HEAD",
    extensions: Mapping[str, Any] | None = None,
) -> Request:
    """Create a new function with partial application of the given arguments
    and keywords.
    """

def PATCHRequest(
    url: str,
    data: _RequestData | None = None,
    headers: HTTPHeaderDict | Mapping[str, str] | None = None,
    proxies: Mapping[str, Any] | None = None,
    query: Mapping[str, str] | None = None,
    *,
    method: str = "PATCH",
    extensions: Mapping[str, Any] | None = None,
) -> Request:
    """Create a new function with partial application of the given arguments
    and keywords.
    """

def PUTRequest(
    url: str,
    data: _RequestData | None = None,
    headers: HTTPHeaderDict | Mapping[str, str] | None = None,
    proxies: Mapping[str, Any] | None = None,
    query: Mapping[str, str] | None = None,
    *,
    method: str = "PUT",
    extensions: Mapping[str, Any] | None = None,
) -> Request:
    """Create a new function with partial application of the given arguments
    and keywords.
    """

class Response(io.IOBase):
    """
    Base class for HTTP response adapters.

    By default, it provides a basic wrapper for a file-like response object.

    Interface partially backwards-compatible with addinfourl and http.client.HTTPResponse.

    @param fp: Original, file-like, response.
    @param url: URL that this is a response of.
    @param headers: response headers.
    @param status: Response HTTP status code. Default is 200 OK.
    @param reason: HTTP status reason. Will use built-in reasons based on status code if not provided.
    @param extensions: Dictionary of handler-specific response extensions.
    """

    fp: io.IOBase
    headers: Message
    status: int
    url: str
    reason: str | None
    extensions: Mapping[str, Any] | dict[str, Any]
    def __init__(
        self,
        fp: io.IOBase,
        url: str,
        headers: Mapping[str, str],
        status: int = 200,
        reason: str | None = None,
        extensions: Mapping[str, Any] | dict[str, Any] | None = None,
    ) -> None: ...
    def readable(self) -> bool: ...
    def read(self, amt: int | None = None) -> bytes: ...
    def close(self) -> None: ...
    def get_header(self, name: str, default: str | None = None) -> str | None:
        """Get header for name.
        If there are multiple matching headers, return all seperated by comma.
        """
