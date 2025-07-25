"""
This module processes Python exceptions that relate to HTTP exceptions
by defining a set of exceptions, all subclasses of HTTPException.
Each exception, in addition to being a Python exception that can be
raised and caught, is also a WSGI application and ``webob.Response``
object.

This module defines exceptions according to RFC 2068 [1]_ : codes with
100-300 are not really errors; 400's are client errors, and 500's are
server errors.  According to the WSGI specification [2]_ , the application
can call ``start_response`` more then once only under two conditions:
(a) the response has not yet been sent, or (b) if the second and
subsequent invocations of ``start_response`` have a valid ``exc_info``
argument obtained from ``sys.exc_info()``.  The WSGI specification then
requires the server or gateway to handle the case where content has been
sent and then an exception was encountered.

Exception
  HTTPException
    HTTPOk
      * 200 - :class:`HTTPOk`
      * 201 - :class:`HTTPCreated`
      * 202 - :class:`HTTPAccepted`
      * 203 - :class:`HTTPNonAuthoritativeInformation`
      * 204 - :class:`HTTPNoContent`
      * 205 - :class:`HTTPResetContent`
      * 206 - :class:`HTTPPartialContent`
    HTTPRedirection
      * 300 - :class:`HTTPMultipleChoices`
      * 301 - :class:`HTTPMovedPermanently`
      * 302 - :class:`HTTPFound`
      * 303 - :class:`HTTPSeeOther`
      * 304 - :class:`HTTPNotModified`
      * 305 - :class:`HTTPUseProxy`
      * 307 - :class:`HTTPTemporaryRedirect`
      * 308 - :class:`HTTPPermanentRedirect`
    HTTPError
      HTTPClientError
        * 400 - :class:`HTTPBadRequest`
        * 401 - :class:`HTTPUnauthorized`
        * 402 - :class:`HTTPPaymentRequired`
        * 403 - :class:`HTTPForbidden`
        * 404 - :class:`HTTPNotFound`
        * 405 - :class:`HTTPMethodNotAllowed`
        * 406 - :class:`HTTPNotAcceptable`
        * 407 - :class:`HTTPProxyAuthenticationRequired`
        * 408 - :class:`HTTPRequestTimeout`
        * 409 - :class:`HTTPConflict`
        * 410 - :class:`HTTPGone`
        * 411 - :class:`HTTPLengthRequired`
        * 412 - :class:`HTTPPreconditionFailed`
        * 413 - :class:`HTTPRequestEntityTooLarge`
        * 414 - :class:`HTTPRequestURITooLong`
        * 415 - :class:`HTTPUnsupportedMediaType`
        * 416 - :class:`HTTPRequestRangeNotSatisfiable`
        * 417 - :class:`HTTPExpectationFailed`
        * 422 - :class:`HTTPUnprocessableEntity`
        * 423 - :class:`HTTPLocked`
        * 424 - :class:`HTTPFailedDependency`
        * 428 - :class:`HTTPPreconditionRequired`
        * 429 - :class:`HTTPTooManyRequests`
        * 431 - :class:`HTTPRequestHeaderFieldsTooLarge`
        * 451 - :class:`HTTPUnavailableForLegalReasons`
      HTTPServerError
        * 500 - :class:`HTTPInternalServerError`
        * 501 - :class:`HTTPNotImplemented`
        * 502 - :class:`HTTPBadGateway`
        * 503 - :class:`HTTPServiceUnavailable`
        * 504 - :class:`HTTPGatewayTimeout`
        * 505 - :class:`HTTPVersionNotSupported`
        * 511 - :class:`HTTPNetworkAuthenticationRequired`

Usage notes
-----------

The HTTPException class is complicated by 4 factors:

  1. The content given to the exception may either be plain-text or
     as html-text.

  2. The template may want to have string-substitutions taken from
     the current ``environ`` or values from incoming headers. This
     is especially troublesome due to case sensitivity.

  3. The final output may either be text/plain or text/html
     mime-type as requested by the client application.

  4. Each exception has a default explanation, but those who
     raise exceptions may want to provide additional detail.

Subclass attributes and call parameters are designed to provide an easier path
through the complications.

Attributes:

   ``code``
       the HTTP status code for the exception

   ``title``
       remainder of the status line (stuff after the code)

   ``explanation``
       a plain-text explanation of the error message that is
       not subject to environment or header substitutions;
       it is accessible in the template via %(explanation)s

   ``detail``
       a plain-text message customization that is not subject
       to environment or header substitutions; accessible in
       the template via %(detail)s

   ``body_template``
       a content fragment (in HTML) used for environment and
       header substitution; the default template includes both
       the explanation and further detail provided in the
       message

Parameters:

   ``detail``
     a plain-text override of the default ``detail``

   ``headers``
     a list of (k,v) header pairs

   ``comment``
     a plain-text additional information which is
     usually stripped/hidden for end-users

   ``body_template``
     a string.Template object containing a content fragment in HTML
     that frames the explanation and further detail

To override the template (which is HTML content) or the plain-text
explanation, one must subclass the given exception; or customize it
after it has been created.  This particular breakdown of a message
into explanation, detail and template allows both the creation of
plain-text and html messages for various clients as well as
error-free substitution of environment variables and headers.


The subclasses of :class:`~_HTTPMove`
(:class:`~HTTPMultipleChoices`, :class:`~HTTPMovedPermanently`,
:class:`~HTTPFound`, :class:`~HTTPSeeOther`, :class:`~HTTPUseProxy` and
:class:`~HTTPTemporaryRedirect`) are redirections that require a ``Location``
field. Reflecting this, these subclasses have two additional keyword arguments:
``location`` and ``add_slash``.

Parameters:

    ``location``
      to set the location immediately

    ``add_slash``
      set to True to redirect to the same URL as the request, except with a
      ``/`` appended

Relative URLs in the location will be resolved to absolute.

References:

.. [1] https://www.python.org/dev/peps/pep-0333/#error-handling
.. [2] https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5


"""

from _typeshed import SupportsItems, SupportsKeysAndGetItem
from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment
from collections.abc import Iterable
from string import Template
from typing import Any, Literal, Protocol
from typing_extensions import Self, TypeAlias

from webob.response import Response

__all__ = [
    "HTTPAccepted",
    "HTTPBadGateway",
    "HTTPBadRequest",
    "HTTPClientError",
    "HTTPConflict",
    "HTTPCreated",
    "HTTPError",
    "HTTPExpectationFailed",
    "HTTPFailedDependency",
    "HTTPForbidden",
    "HTTPFound",
    "HTTPGatewayTimeout",
    "HTTPGone",
    "HTTPInsufficientStorage",
    "HTTPInternalServerError",
    "HTTPLengthRequired",
    "HTTPLocked",
    "HTTPMethodNotAllowed",
    "HTTPMovedPermanently",
    "HTTPMultipleChoices",
    "HTTPNetworkAuthenticationRequired",
    "HTTPNoContent",
    "HTTPNonAuthoritativeInformation",
    "HTTPNotAcceptable",
    "HTTPNotFound",
    "HTTPNotImplemented",
    "HTTPNotModified",
    "HTTPOk",
    "HTTPPartialContent",
    "HTTPPaymentRequired",
    "HTTPPermanentRedirect",
    "HTTPPreconditionFailed",
    "HTTPPreconditionRequired",
    "HTTPProxyAuthenticationRequired",
    "HTTPRedirection",
    "HTTPRequestEntityTooLarge",
    "HTTPRequestHeaderFieldsTooLarge",
    "HTTPRequestRangeNotSatisfiable",
    "HTTPRequestTimeout",
    "HTTPRequestURITooLong",
    "HTTPResetContent",
    "HTTPSeeOther",
    "HTTPServerError",
    "HTTPServiceUnavailable",
    "HTTPTemporaryRedirect",
    "HTTPTooManyRequests",
    "HTTPUnauthorized",
    "HTTPUnavailableForLegalReasons",
    "HTTPUnprocessableEntity",
    "HTTPUnsupportedMediaType",
    "HTTPUseProxy",
    "HTTPVersionNotSupported",
    "WSGIHTTPException",
    "HTTPException",
    "HTTPExceptionMiddleware",
    "status_map",
]

_Headers: TypeAlias = SupportsItems[str, str] | SupportsKeysAndGetItem[str, str] | Iterable[tuple[str, str]]

class _JSONFormatter(Protocol):
    def __call__(self, *, body: str, status: str, title: str, environ: WSGIEnvironment) -> Any: ...

class HTTPException(Exception):
    wsgi_response: Response
    def __init__(self, message: str, wsgi_response: Response) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

class WSGIHTTPException(Response, HTTPException):
    code: int
    title: str
    explanation: str
    body_template_obj: Template
    plain_template_obj: Template
    html_template_obj: Template
    empty_body: bool
    detail: str | None
    comment: str | None
    def __init__(
        self,
        detail: str | None = None,
        headers: _Headers | None = None,
        comment: str | None = None,
        body_template: str | None = None,
        json_formatter: _JSONFormatter | None = None,
        **kw: Any,
    ) -> None: ...
    def plain_body(self, environ: WSGIEnvironment) -> str: ...
    def html_body(self, environ: WSGIEnvironment) -> str: ...
    def json_formatter(self, body: str, status: str, title: str, environ: WSGIEnvironment) -> Any: ...
    def json_body(self, environ: WSGIEnvironment) -> str: ...  # type: ignore[override]
    def generate_response(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...
    @property
    def wsgi_response(self) -> Self: ...  # type: ignore[override]
    def __str__(self) -> str: ...  # type: ignore[override]  # noqa: Y029

class HTTPError(WSGIHTTPException):
    """
    base class for status codes in the 400's and 500's

    This is an exception which indicates that an error has occurred,
    and that any work in progress should not be committed.  These are
    typically results in the 400's and 500's.
    """

class HTTPRedirection(WSGIHTTPException):
    """
    base class for 300's status code (redirections)

    This is an abstract base class for 3xx redirection.  It indicates
    that further action needs to be taken by the user agent in order
    to fulfill the request.  It does not necessarly signal an error
    condition.
    """

class HTTPOk(WSGIHTTPException):
    """
    Base class for the 200's status code (successful responses)

    code: 200, title: OK
    """

class HTTPCreated(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that request has been fulfilled and resulted in a new
    resource being created.

    code: 201, title: Created
    """

class HTTPAccepted(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that the request has been accepted for processing, but the
    processing has not been completed.

    code: 202, title: Accepted
    """

class HTTPNonAuthoritativeInformation(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that the returned metainformation in the entity-header is
    not the definitive set as available from the origin server, but is
    gathered from a local or a third-party copy.

    code: 203, title: Non-Authoritative Information
    """

class HTTPNoContent(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that the server has fulfilled the request but does
    not need to return an entity-body, and might want to return updated
    metainformation.

    code: 204, title: No Content
    """

    empty_body: Literal[True]

class HTTPResetContent(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that the the server has fulfilled the request and
    the user agent SHOULD reset the document view which caused the
    request to be sent.

    code: 205, title: Reset Content
    """

    empty_body: Literal[True]

class HTTPPartialContent(HTTPOk):
    """
    subclass of :class:`~HTTPOk`

    This indicates that the server has fulfilled the partial GET
    request for the resource.

    code: 206, title: Partial Content
    """

class _HTTPMove(HTTPRedirection):
    """
    redirections which require a Location field

    Since a 'Location' header is a required attribute of 301, 302, 303,
    305, 307 and 308 (but not 304), this base class provides the mechanics to
    make this easy.

    You can provide a location keyword argument to set the location
    immediately.  You may also give ``add_slash=True`` if you want to
    redirect to the same URL as the request, except with a ``/`` added
    to the end.

    Relative URLs in the location will be resolved to absolute.
    """

    explanation: str
    add_slash: bool
    def __init__(
        self,
        detail: str | None = None,
        headers: _Headers | None = None,
        comment: str | None = None,
        body_template: str | None = None,
        location: str | None = None,
        add_slash: bool = False,
    ) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

class HTTPMultipleChoices(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource corresponds to any one
    of a set of representations, each with its own specific location,
    and agent-driven negotiation information is being provided so that
    the user can select a preferred representation and redirect its
    request to that location.

    code: 300, title: Multiple Choices
    """

class HTTPMovedPermanently(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource has been assigned a new
    permanent URI and any future references to this resource SHOULD use
    one of the returned URIs.

    code: 301, title: Moved Permanently
    """

class HTTPFound(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource resides temporarily under
    a different URI.

    code: 302, title: Found
    """

class HTTPSeeOther(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the response to the request can be found under
    a different URI and SHOULD be retrieved using a GET method on that
    resource.

    code: 303, title: See Other
    """

class HTTPNotModified(HTTPRedirection):
    """
    subclass of :class:`~HTTPRedirection`

    This indicates that if the client has performed a conditional GET
    request and access is allowed, but the document has not been
    modified, the server SHOULD respond with this status code.

    code: 304, title: Not Modified
    """

    empty_body: Literal[True]

class HTTPUseProxy(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource MUST be accessed through
    the proxy given by the Location field.

    code: 305, title: Use Proxy
    """

class HTTPTemporaryRedirect(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource resides temporarily
    under a different URI.

    code: 307, title: Temporary Redirect
    """

class HTTPPermanentRedirect(_HTTPMove):
    """
    subclass of :class:`~_HTTPMove`

    This indicates that the requested resource resides permanently
    under a different URI.

    code: 308, title: Permanent Redirect
    """

class HTTPClientError(HTTPError):
    """
    base class for the 400's, where the client is in error

    This is an error condition in which the client is presumed to be
    in-error.  This is an expected problem, and thus is not considered
    a bug.  A server-side traceback is not warranted.  Unless specialized,
    this is a '400 Bad Request'

    code: 400, title: Bad Request
    """

class HTTPBadRequest(HTTPClientError): ...

class HTTPUnauthorized(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the request requires user authentication.

    code: 401, title: Unauthorized
    """

class HTTPPaymentRequired(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    code: 402, title: Payment Required
    """

class HTTPForbidden(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server understood the request, but is
    refusing to fulfill it.

    code: 403, title: Forbidden
    """

class HTTPNotFound(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server did not find anything matching the
    Request-URI.

    code: 404, title: Not Found
    """

class HTTPMethodNotAllowed(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the method specified in the Request-Line is
    not allowed for the resource identified by the Request-URI.

    code: 405, title: Method Not Allowed
    """

class HTTPNotAcceptable(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates the resource identified by the request is only
    capable of generating response entities which have content
    characteristics not acceptable according to the accept headers
    sent in the request.

    code: 406, title: Not Acceptable
    """

class HTTPProxyAuthenticationRequired(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This is similar to 401, but indicates that the client must first
    authenticate itself with the proxy.

    code: 407, title: Proxy Authentication Required
    """

class HTTPRequestTimeout(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the client did not produce a request within
    the time that the server was prepared to wait.

    code: 408, title: Request Timeout
    """

class HTTPConflict(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the request could not be completed due to a
    conflict with the current state of the resource.

    code: 409, title: Conflict
    """

class HTTPGone(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the requested resource is no longer available
    at the server and no forwarding address is known.

    code: 410, title: Gone
    """

class HTTPLengthRequired(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the the server refuses to accept the request
    without a defined Content-Length.

    code: 411, title: Length Required
    """

class HTTPPreconditionFailed(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the precondition given in one or more of the
    request-header fields evaluated to false when it was tested on the
    server.

    code: 412, title: Precondition Failed
    """

class HTTPRequestEntityTooLarge(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is refusing to process a request
    because the request entity is larger than the server is willing or
    able to process.

    code: 413, title: Request Entity Too Large
    """

class HTTPRequestURITooLong(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is refusing to service the request
    because the Request-URI is longer than the server is willing to
    interpret.

    code: 414, title: Request-URI Too Long
    """

class HTTPUnsupportedMediaType(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is refusing to service the request
    because the entity of the request is in a format not supported by
    the requested resource for the requested method.

    code: 415, title: Unsupported Media Type
    """

class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    The server SHOULD return a response with this status code if a
    request included a Range request-header field, and none of the
    range-specifier values in this field overlap the current extent
    of the selected resource, and the request did not include an
    If-Range request-header field.

    code: 416, title: Request Range Not Satisfiable
    """

class HTTPExpectationFailed(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indidcates that the expectation given in an Expect
    request-header field could not be met by this server.

    code: 417, title: Expectation Failed
    """

class HTTPUnprocessableEntity(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is unable to process the contained
    instructions.

    code: 422, title: Unprocessable Entity
    """

class HTTPLocked(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the resource is locked.

    code: 423, title: Locked
    """

class HTTPFailedDependency(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the method could not be performed because the
    requested action depended on another action and that action failed.

    code: 424, title: Failed Dependency
    """

class HTTPPreconditionRequired(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the origin server requires the request to be
    conditional.  From RFC 6585, "Additional HTTP Status Codes".

    code: 428, title: Precondition Required
    """

class HTTPTooManyRequests(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the client has sent too many requests in a
    given amount of time.  Useful for rate limiting.

    From RFC 6585, "Additional HTTP Status Codes".

    code: 429, title: Too Many Requests
    """

class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is unwilling to process the request
    because its header fields are too large. The request may be resubmitted
    after reducing the size of the request header fields.

    From RFC 6585, "Additional HTTP Status Codes".

    code: 431, title: Request Header Fields Too Large
    """

class HTTPUnavailableForLegalReasons(HTTPClientError):
    """
    subclass of :class:`~HTTPClientError`

    This indicates that the server is unable to process the request
    because of legal reasons, e.g. censorship or government-mandated
    blocked access.

    From the draft "A New HTTP Status Code for Legally-restricted Resources"
    by Tim Bray:

    https://tools.ietf.org/html/draft-tbray-http-legally-restricted-status-00

    code: 451, title: Unavailable For Legal Reasons
    """

class HTTPServerError(HTTPError):
    """
    base class for the 500's, where the server is in-error

    This is an error condition in which the server is presumed to be
    in-error.  This is usually unexpected, and thus requires a traceback;
    ideally, opening a support ticket for the customer. Unless specialized,
    this is a '500 Internal Server Error'
    """

class HTTPInternalServerError(HTTPServerError): ...

class HTTPNotImplemented(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server does not support the functionality
    required to fulfill the request.

    code: 501, title: Not Implemented
    """

class HTTPBadGateway(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server, while acting as a gateway or proxy,
    received an invalid response from the upstream server it accessed
    in attempting to fulfill the request.

    code: 502, title: Bad Gateway
    """

class HTTPServiceUnavailable(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server is currently unable to handle the
    request due to a temporary overloading or maintenance of the server.

    code: 503, title: Service Unavailable
    """

class HTTPGatewayTimeout(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server, while acting as a gateway or proxy,
    did not receive a timely response from the upstream server specified
    by the URI (e.g. HTTP, FTP, LDAP) or some other auxiliary server
    (e.g. DNS) it needed to access in attempting to complete the request.

    code: 504, title: Gateway Timeout
    """

class HTTPVersionNotSupported(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server does not support, or refuses to
    support, the HTTP protocol version that was used in the request
    message.

    code: 505, title: HTTP Version Not Supported
    """

class HTTPInsufficientStorage(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the server does not have enough space to save
    the resource.

    code: 507, title: Insufficient Storage
    """

class HTTPNetworkAuthenticationRequired(HTTPServerError):
    """
    subclass of :class:`~HTTPServerError`

    This indicates that the client needs to authenticate to gain
    network access.  From RFC 6585, "Additional HTTP Status Codes".

    code: 511, title: Network Authentication Required
    """

class HTTPExceptionMiddleware:
    """
    Middleware that catches exceptions in the sub-application.  This
    does not catch exceptions in the app_iter; only during the initial
    calling of the application.

    This should be put *very close* to applications that might raise
    these exceptions.  This should not be applied globally; letting
    *expected* exceptions raise through the WSGI stack is dangerous.
    """

    application: WSGIApplication
    def __init__(self, application: WSGIApplication) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

status_map: dict[int, type[HTTPOk | HTTPRedirection | HTTPClientError | HTTPServerError]]
