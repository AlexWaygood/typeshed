from _typeshed import SupportsItems, SupportsRead
from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from collections.abc import Iterable, Iterator, Sequence
from datetime import timedelta
from typing import IO, Any, Literal, Protocol, TypedDict, TypeVar, overload
from typing_extensions import Self, TypeAlias

from webob._types import AsymmetricProperty, AsymmetricPropertyWithDelete, SymmetricProperty, SymmetricPropertyWithDelete
from webob.byterange import ContentRange
from webob.cachecontrol import CacheControl
from webob.cookies import _SameSitePolicy
from webob.descriptors import _authorization, _ContentRangeParams, _DateProperty, _ListProperty
from webob.headers import ResponseHeaders
from webob.request import Request

__all__ = ["Response"]

_ResponseT = TypeVar("_ResponseT", bound=Response)
_ResponseCacheControl: TypeAlias = CacheControl[Literal["response"]]

class _ResponseCacheExpires(Protocol):
    def __call__(
        self,
        seconds: int | timedelta = 0,
        *,
        public: bool = ...,
        private: Literal[True] | str = ...,
        no_cache: Literal[True] | str = ...,
        no_store: bool = ...,
        no_transform: bool = ...,
        must_revalidate: bool = ...,
        proxy_revalidate: bool = ...,
        max_age: int = ...,
        s_maxage: int = ...,
        s_max_age: int = ...,
        stale_while_revalidate: int = ...,
        stale_if_error: int = ...,
    ) -> None: ...

class _ResponseCacheControlDict(TypedDict, total=False):
    public: bool
    private: Literal[True] | str
    no_cache: Literal[True] | str
    no_store: bool
    no_transform: bool
    must_revalidate: bool
    proxy_revalidate: bool
    max_age: int
    s_maxage: int
    s_max_age: int
    stale_while_revalidate: int
    stale_if_error: int

class Response:
    """
    Represents a WSGI response.

    If no arguments are passed, creates a :class:`~Response` that uses a
    variety of defaults. The defaults may be changed by sub-classing the
    :class:`~Response`. See the :ref:`sub-classing notes
    <response_subclassing_notes>`.

    :cvar ~Response.body: If ``body`` is a ``text_type``, then it will be
        encoded using either ``charset`` when provided or ``default_encoding``
        when ``charset`` is not provided if the ``content_type`` allows for a
        ``charset``. This argument is mutually  exclusive with ``app_iter``.

    :vartype ~Response.body: bytes or text_type

    :cvar ~Response.status: Either an :class:`int` or a string that is
        an integer followed by the status text. If it is an integer, it will be
        converted to a proper status that also includes the status text.  Any
        existing status text will be kept. Non-standard values are allowed.

    :vartype ~Response.status: int or str

    :cvar ~Response.headerlist: A list of HTTP headers for the response.

    :vartype ~Response.headerlist: list

    :cvar ~Response.app_iter: An iterator that is used as the body of the
        response. Should conform to the WSGI requirements and should provide
        bytes. This argument is mutually exclusive with ``body``.

    :vartype ~Response.app_iter: iterable

    :cvar ~Response.content_type: Sets the ``Content-Type`` header. If no
        ``content_type`` is provided, and there is no ``headerlist``, the
        ``default_content_type`` will be automatically set. If ``headerlist``
        is provided then this value is ignored.

    :vartype ~Response.content_type: str or None

    :cvar conditional_response: Used to change the behavior of the
        :class:`~Response` to check the original request for conditional
        response headers. See :meth:`~Response.conditional_response_app` for
        more information.

    :vartype conditional_response: bool

    :cvar ~Response.charset: Adds a ``charset`` ``Content-Type`` parameter. If
        no ``charset`` is provided and the ``Content-Type`` is text, then the
        ``default_charset`` will automatically be added.  Currently the only
        ``Content-Type``'s that allow for a ``charset`` are defined to be
        ``text/*``, ``application/xml``, and ``*/*+xml``. Any other
        ``Content-Type``'s will not have a ``charset`` added. If a
        ``headerlist`` is provided this value is ignored.

    :vartype ~Response.charset: str or None

    All other response attributes may be set on the response by providing them
    as keyword arguments. A :exc:`TypeError` will be raised for any unexpected
    keywords.

    .. _response_subclassing_notes:

    **Sub-classing notes:**

    * The ``default_content_type`` is used as the default for the
      ``Content-Type`` header that is returned on the response. It is
      ``text/html``.

    * The ``default_charset`` is used as the default character set to return on
      the ``Content-Type`` header, if the ``Content-Type`` allows for a
      ``charset`` parameter. Currently the only ``Content-Type``'s that allow
      for a ``charset`` are defined to be: ``text/*``, ``application/xml``, and
      ``*/*+xml``. Any other ``Content-Type``'s will not have a ``charset``
      added.

    * The ``unicode_errors`` is set to ``strict``, and access on a
      :attr:`~Response.text` will raise an error if it fails to decode the
      :attr:`~Response.body`.

    * ``default_conditional_response`` is set to ``False``. This flag may be
      set to ``True`` so that all ``Response`` objects will attempt to check
      the original request for conditional response headers. See
      :meth:`~Response.conditional_response_app` for more information.

    * ``default_body_encoding`` is set to 'UTF-8' by default. It exists to
      allow users to get/set the ``Response`` object using ``.text``, even if
      no ``charset`` has been set for the ``Content-Type``.
    """

    default_content_type: str
    default_charset: str
    unicode_errors: str
    default_conditional_response: bool
    default_body_encoding: str
    request: Request | None
    environ: WSGIEnvironment | None
    status: AsymmetricProperty[str, int | str | bytes]
    conditional_response: bool
    def __init__(
        self,
        body: bytes | str | None = None,
        status: int | str | bytes | None = None,
        headerlist: list[tuple[str, str]] | None = None,
        app_iter: Iterable[bytes] | None = None,
        content_type: str | None = None,
        conditional_response: bool | None = None,
        charset: str = ...,
        **kw: Any,
    ) -> None: ...
    @classmethod
    def from_file(cls, fp: IO[str] | IO[bytes]) -> Response:
        """Reads a response from a file-like object (it must implement
        ``.read(size)`` and ``.readline()``).

        It will read up to the end of the response, not the end of the
        file.

        This reads the response as represented by ``str(resp)``; it
        may not read every valid HTTP response properly.  Responses
        must have a ``Content-Length``.
        """

    def copy(self) -> Response:
        """Makes a copy of the response."""
    status_code: SymmetricProperty[int]
    status_int: SymmetricProperty[int]
    headerlist: AsymmetricPropertyWithDelete[list[tuple[str, str]], Iterable[tuple[str, str]] | SupportsItems[str, str]]
    headers: AsymmetricProperty[ResponseHeaders, SupportsItems[str, str] | Iterable[tuple[str, str]]]
    body: SymmetricPropertyWithDelete[bytes]
    json: SymmetricPropertyWithDelete[Any]
    json_body: SymmetricPropertyWithDelete[Any]
    @property
    def has_body(self) -> bool:
        """
        Determine if the the response has a :attr:`~Response.body`. In
        contrast to simply accessing :attr:`~Response.body`, this method
        will **not** read the underlying :attr:`~Response.app_iter`.
        """
    text: SymmetricPropertyWithDelete[str]
    unicode_body: SymmetricPropertyWithDelete[str]  # deprecated
    ubody: SymmetricPropertyWithDelete[str]  # deprecated
    body_file: AsymmetricPropertyWithDelete[ResponseBodyFile, SupportsRead[bytes]]
    content_length: AsymmetricPropertyWithDelete[int | None, int | str | bytes | None]
    def write(self, text: str | bytes) -> int: ...
    app_iter: SymmetricPropertyWithDelete[Iterable[bytes]]
    allow: _ListProperty
    vary: _ListProperty
    content_encoding: SymmetricPropertyWithDelete[str | None]
    content_language: SymmetricPropertyWithDelete[str | None]
    content_location: SymmetricPropertyWithDelete[str | None]
    content_md5: SymmetricPropertyWithDelete[str | None]
    content_disposition: SymmetricPropertyWithDelete[str | None]
    accept_ranges: SymmetricPropertyWithDelete[str | None]
    content_range: AsymmetricPropertyWithDelete[ContentRange | None, _ContentRangeParams]
    date: _DateProperty
    expires: _DateProperty
    last_modified: _DateProperty
    etag: AsymmetricPropertyWithDelete[str | None, tuple[str, bool] | str | None]
    @property
    def etag_strong(self) -> str | None: ...
    location: SymmetricPropertyWithDelete[str | None]
    pragma: SymmetricPropertyWithDelete[str | None]
    age: SymmetricPropertyWithDelete[int | None]
    retry_after: _DateProperty
    server: SymmetricPropertyWithDelete[str | None]
    www_authenticate: AsymmetricPropertyWithDelete[
        _authorization | None, tuple[str, str | dict[str, str]] | list[Any] | str | None
    ]
    charset: SymmetricPropertyWithDelete[str | None]
    content_type: SymmetricPropertyWithDelete[str | None]
    content_type_params: AsymmetricPropertyWithDelete[dict[str, str], SupportsItems[str, str] | None]
    def set_cookie(
        self,
        name: str | bytes,
        value: str | bytes | None = "",
        max_age: int | timedelta | None = None,
        path: str = "/",
        domain: str | None = None,
        secure: bool = False,
        httponly: bool = False,
        comment: str | None = None,
        overwrite: bool = False,
        samesite: _SameSitePolicy | None = None,
    ) -> None:
        """
        Set (add) a cookie for the response.

        Arguments are:

        ``name``

           The cookie name.

        ``value``

           The cookie value, which should be a string or ``None``.  If
           ``value`` is ``None``, it's equivalent to calling the
           :meth:`webob.response.Response.unset_cookie` method for this
           cookie key (it effectively deletes the cookie on the client).

        ``max_age``

           An integer representing a number of seconds, ``datetime.timedelta``,
           or ``None``. This value is used as the ``Max-Age`` of the generated
           cookie.  If ``expires`` is not passed and this value is not
           ``None``, the ``max_age`` value will also influence the ``Expires``
           value of the cookie (``Expires`` will be set to ``now`` +
           ``max_age``).  If this value is ``None``, the cookie will not have a
           ``Max-Age`` value (unless ``expires`` is set). If both ``max_age``
           and ``expires`` are set, this value takes precedence.

        ``path``

           A string representing the cookie ``Path`` value.  It defaults to
           ``/``.

        ``domain``

           A string representing the cookie ``Domain``, or ``None``.  If
           domain is ``None``, no ``Domain`` value will be sent in the
           cookie.

        ``secure``

           A boolean.  If it's ``True``, the ``secure`` flag will be sent in
           the cookie, if it's ``False``, the ``secure`` flag will not be
           sent in the cookie.

        ``httponly``

           A boolean.  If it's ``True``, the ``HttpOnly`` flag will be sent
           in the cookie, if it's ``False``, the ``HttpOnly`` flag will not
           be sent in the cookie.

        ``samesite``

          A string representing the ``SameSite`` attribute of the cookie or
          ``None``. If samesite is ``None`` no ``SameSite`` value will be sent
          in the cookie. Should only be ``"strict"``, ``"lax"``, or ``"none"``.

        ``comment``

           A string representing the cookie ``Comment`` value, or ``None``.
           If ``comment`` is ``None``, no ``Comment`` value will be sent in
           the cookie.

        ``expires``

           A ``datetime.timedelta`` object representing an amount of time,
           ``datetime.datetime`` or ``None``. A non-``None`` value is used to
           generate the ``Expires`` value of the generated cookie. If
           ``max_age`` is not passed, but this value is not ``None``, it will
           influence the ``Max-Age`` header. If this value is ``None``, the
           ``Expires`` cookie value will be unset (unless ``max_age`` is set).
           If ``max_age`` is set, it will be used to generate the ``expires``
           and this value is ignored.

           If a ``datetime.datetime`` is provided it has to either be timezone
           aware or be based on UTC. ``datetime.datetime`` objects that are
           local time are not supported. Timezone aware ``datetime.datetime``
           objects are converted to UTC.

           This argument will be removed in future versions of WebOb (version
           1.9).

        ``overwrite``

           If this key is ``True``, before setting the cookie, unset any
           existing cookie.

        """

    def delete_cookie(self, name: str | bytes, path: str = "/", domain: str | None = None) -> None:
        """
        Delete a cookie from the client.  Note that ``path`` and ``domain``
        must match how the cookie was originally set.

        This sets the cookie to the empty string, and ``max_age=0`` so
        that it should expire immediately.
        """

    def unset_cookie(self, name: str | bytes, strict: bool = True) -> None:
        """
        Unset a cookie with the given name (remove it from the response).
        """

    @overload
    def merge_cookies(self, resp: _ResponseT) -> _ResponseT:
        """Merge the cookies that were set on this response with the
        given ``resp`` object (which can be any WSGI application).

        If the ``resp`` is a :class:`webob.Response` object, then the
        other object will be modified in-place.
        """

    @overload
    def merge_cookies(self, resp: WSGIApplication) -> WSGIApplication: ...
    cache_control: AsymmetricProperty[_ResponseCacheControl, _ResponseCacheControl | _ResponseCacheControlDict | str | None]
    cache_expires: AsymmetricProperty[_ResponseCacheExpires, timedelta | int | bool | None]
    def encode_content(self, encoding: Literal["gzip", "identity"] = "gzip", lazy: bool = False) -> None:
        """
        Encode the content with the given encoding (only ``gzip`` and
        ``identity`` are supported).
        """

    def decode_content(self) -> None: ...
    def md5_etag(self, body: bytes | None = None, set_content_md5: bool = False) -> None:
        """
        Generate an etag for the response object using an MD5 hash of
        the body (the ``body`` parameter, or ``self.body`` if not given).

        Sets ``self.etag``.

        If ``set_content_md5`` is ``True``, sets ``self.content_md5`` as well.
        """

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        """
        WSGI application interface
        """

    def conditional_response_app(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        """
        Like the normal ``__call__`` interface, but checks conditional headers:

            * ``If-Modified-Since``   (``304 Not Modified``; only on ``GET``,
              ``HEAD``)
            * ``If-None-Match``       (``304 Not Modified``; only on ``GET``,
              ``HEAD``)
            * ``Range``               (``406 Partial Content``; only on ``GET``,
              ``HEAD``)
        """

    def app_iter_range(self, start: int, stop: int | None) -> AppIterRange:
        """
        Return a new ``app_iter`` built from the response ``app_iter``, that
        serves up only the given ``start:stop`` range.
        """

    def __str__(self, skip_body: bool = False) -> str: ...

class ResponseBodyFile:
    mode: Literal["wb"]
    closed: Literal[False]
    response: Response
    def __init__(self, response: Response) -> None:
        """
        Represents a :class:`~Response` as a file like object.
        """

    @property
    def encoding(self) -> str | None:
        """The encoding of the file (inherited from response.charset)"""
    # NOTE: Technically this is an instance attribute and not a method
    def write(self, text: str | bytes) -> int: ...
    def writelines(self, seq: Sequence[str | bytes]) -> None:
        """
        Write a sequence of lines to the response.
        """

    def flush(self) -> None: ...
    def tell(self) -> int:
        """
        Provide the current location where we are going to start writing.
        """

class AppIterRange:
    """
    Wraps an ``app_iter``, returning just a range of bytes.
    """

    app_iter: Iterator[bytes]
    start: int
    stop: int | None
    def __init__(self, app_iter: Iterable[bytes], start: int, stop: int | None) -> None: ...
    def __iter__(self) -> Self: ...
    def next(self) -> bytes: ...
    __next__ = next
    def close(self) -> None: ...

class EmptyResponse:
    """
    An empty WSGI response.

    An iterator that immediately stops. Optionally provides a close
    method to close an underlying ``app_iter`` it replaces.
    """

    def __init__(self, app_iter: Iterable[bytes] | None = None) -> None: ...
    def __iter__(self) -> Self: ...
    def __len__(self) -> Literal[0]: ...
    def next(self) -> bytes: ...
    __next__ = next
