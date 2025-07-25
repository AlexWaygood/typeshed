"""
A pure-Python, gevent-friendly WSGI server implementing HTTP/1.1.

The server is provided in :class:`WSGIServer`, but most of the actual
WSGI work is handled by :class:`WSGIHandler` --- a new instance is
created for each request. The server can be customized to use
different subclasses of :class:`WSGIHandler`.

.. important::

   This server is intended primarily for development and testing, and
   secondarily for other "safe" scenarios where it will not be exposed to
   potentially malicious input. The code has not been security audited,
   and is not intended for direct exposure to the public Internet. For production
   usage on the Internet, either choose a production-strength server such as
   gunicorn, or put a reverse proxy between gevent and the Internet.

.. versionchanged:: 23.9.0

   Complies more closely with the HTTP specification for chunked transfer encoding.
   In particular, we are much stricter about trailers, and trailers that
   are invalid (too long or featuring disallowed characters) forcibly close
   the connection to the client *after* the results have been sent.

   Trailers otherwise continue to be ignored and are not available to the
   WSGI application.

"""

from _typeshed import OptExcInfo, StrOrBytesPath, SupportsWrite
from _typeshed.wsgi import WSGIApplication, WSGIEnvironment
from collections.abc import Callable, Container, Iterable, Iterator
from http.client import HTTPMessage
from io import BufferedIOBase, BufferedReader
from logging import Logger
from types import TracebackType
from typing import Any, ClassVar, Literal, Protocol, TypeVar, overload
from typing_extensions import Self

from gevent.baseserver import _Spawner
from gevent.server import StreamServer
from gevent.socket import socket as _GeventSocket
from gevent.ssl import SSLContext

__all__ = ["WSGIServer", "WSGIHandler", "LoggingLogAdapter", "Environ", "SecureEnviron", "WSGISecureEnviron"]

_T = TypeVar("_T")

class _LogOutputStream(SupportsWrite[str], Protocol):
    def writelines(self, lines: Iterable[str], /) -> None: ...
    def flush(self) -> None: ...

class Input:
    rfile: BufferedReader
    content_length: int | None
    socket: _GeventSocket | None
    position: int
    chunked_input: bool
    chunk_length: int
    send_100_continue_enabled: bool
    def __init__(
        self, rfile: BufferedReader, content_length: int | None, socket: _GeventSocket | None = None, chunked_input: bool = False
    ) -> None: ...
    def read(self, length: int | None = None) -> bytes: ...
    def readline(self, size: int | None = None) -> bytes: ...
    def readlines(self, hint: object | None = None) -> list[bytes]: ...
    def __iter__(self) -> Self: ...
    def next(self) -> bytes: ...
    __next__ = next

class OldMessage(HTTPMessage):
    status: str
    def __init__(self) -> None: ...
    @overload
    def getheader(self, name: str, default: None = None) -> str | None: ...
    @overload
    def getheader(self, name: str, default: _T) -> str | _T: ...
    @property
    def headers(self) -> Iterator[str]: ...
    @property
    def typeheader(self) -> str | None: ...

class WSGIHandler:
    """
    Handles HTTP requests from a socket, creates the WSGI environment, and
    interacts with the WSGI application.

    This is the default value of :attr:`WSGIServer.handler_class`.
    This class may be subclassed carefully, and that class set on a
    :class:`WSGIServer` instance through a keyword argument at
    construction time.

    Instances are constructed with the same arguments as passed to the
    server's :meth:`WSGIServer.handle` method followed by the server
    itself. The application and environment are obtained from the server.

    """

    protocol_version: str
    def MessageClass(self, fp: BufferedIOBase) -> OldMessage: ...
    status: str | None
    response_headers: list[tuple[str, str]] | None
    code: int | None
    provided_date: str | None
    provided_content_length: str | None
    close_connection: bool
    time_start: float
    time_finish: float
    headers_sent: bool
    response_use_chunked: bool
    connection_upgraded: bool
    environ: WSGIEnvironment | None
    application: WSGIApplication | None
    requestline: str | None
    response_length: int
    result: Iterable[bytes] | None
    wsgi_input: Input | None
    content_length: int
    headers: OldMessage
    request_version: str | None
    command: str | None
    path: str | None
    socket: _GeventSocket
    client_address: str
    server: WSGIServer
    rfile: BufferedReader
    def __init__(self, sock: _GeventSocket, address: str, server: WSGIServer) -> None: ...
    def handle(self) -> None:
        """
        The main request handling method, called by the server.

        This method runs a request handling loop, calling
        :meth:`handle_one_request` until all requests on the
        connection have been handled (that is, it implements
        keep-alive).
        """

    def read_request(self, raw_requestline: str) -> OldMessage:
        """
        Parse the incoming request.

        Parses various headers into ``self.headers`` using
        :attr:`MessageClass`. Other attributes that are set upon a successful
        return of this method include ``self.content_length`` and ``self.close_connection``.

        :param str raw_requestline: A native :class:`str` representing
           the request line. A processed version of this will be stored
           into ``self.requestline``.

        :raises ValueError: If the request is invalid. This error will
           not be logged as a traceback (because it's a client issue, not a server problem).
        :return: A boolean value indicating whether the request was successfully parsed.
           This method should either return a true value or have raised a ValueError
           with details about the parsing error.

        .. versionchanged:: 1.1b6
           Raise the previously documented :exc:`ValueError` in more cases instead of returning a
           false value; this allows subclasses more opportunity to customize behaviour.
        """

    def log_error(self, msg: str, *args: object) -> None: ...
    def read_requestline(self) -> str:
        """
        Read and return the HTTP request line.

        Under both Python 2 and 3, this should return the native
        ``str`` type; under Python 3, this probably means the bytes read
        from the network need to be decoded (using the ISO-8859-1 charset, aka
        latin-1).
        """

    def handle_one_request(self) -> tuple[str, bytes] | Literal[True] | None:
        """
        Handles one HTTP request using ``self.socket`` and ``self.rfile``.

        Each invocation of this method will do several things, including (but not limited to):

        - Read the request line using :meth:`read_requestline`;
        - Read the rest of the request, including headers, with :meth:`read_request`;
        - Construct a new WSGI environment in ``self.environ`` using :meth:`get_environ`;
        - Store the application in ``self.application``, retrieving it from the server;
        - Handle the remainder of the request, including invoking the application,
          with :meth:`handle_one_response`

        There are several possible return values to indicate the state
        of the client connection:

        - ``None``
            The client connection is already closed or should
            be closed because the WSGI application or client set the
            ``Connection: close`` header. The request handling
            loop should terminate and perform cleanup steps.
        - (status, body)
            An HTTP status and body tuple. The request was in error,
            as detailed by the status and body. The request handling
            loop should terminate, close the connection, and perform
            cleanup steps. Note that the ``body`` is the complete contents
            to send to the client, including all headers and the initial
            status line.
        - ``True``
            The literal ``True`` value. The request was successfully handled
            and the response sent to the client by :meth:`handle_one_response`.
            The connection remains open to process more requests and the connection
            handling loop should call this method again. This is the typical return
            value.

        .. seealso:: :meth:`handle`

        .. versionchanged:: 1.1b6
           Funnel exceptions having to do with invalid HTTP requests through
           :meth:`_handle_client_error` to allow subclasses to customize. Note that
           this is experimental and may change in the future.
        """

    def finalize_headers(self) -> None: ...
    ApplicationError: type[AssertionError]
    def write(self, data: bytes) -> None: ...
    def start_response(
        self, status: str, headers: list[tuple[str, str]], exc_info: OptExcInfo | None = None
    ) -> Callable[[bytes], None]:
        """
        .. versionchanged:: 1.2a1
           Avoid HTTP header injection by raising a :exc:`ValueError`
           if *status* or any *header* name or value contains a carriage
           return or newline.
        .. versionchanged:: 1.1b5
           Pro-actively handle checking the encoding of the status line
           and headers during this method. On Python 2, avoid some
           extra encodings.
        """

    def log_request(self) -> None: ...
    def format_request(self) -> str: ...
    def process_result(self) -> None: ...
    def run_application(self) -> None: ...
    ignored_socket_errors: tuple[int, ...]
    def handle_one_response(self) -> None:
        """
        Invoke the application to produce one response.

        This is called by :meth:`handle_one_request` after all the
        state for the request has been established. It is responsible
        for error handling.
        """

    def handle_error(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None: ...
    def get_environ(self) -> WSGIEnvironment:
        """
        Construct and return a new WSGI environment dictionary for a specific request.

        This should begin with asking the server for the base environment
        using :meth:`WSGIServer.get_environ`, and then proceed to add the
        request specific values.

        By the time this method is invoked the request line and request shall have
        been parsed and ``self.headers`` shall be populated.
        """

class LoggingLogAdapter:
    """
    An adapter for :class:`logging.Logger` instances
    to let them be used with :class:`WSGIServer`.

    .. warning:: Unless the entire process is monkey-patched at a very
        early part of the lifecycle (before logging is configured),
        loggers are likely to not be gevent-cooperative. For example,
        the socket and syslog handlers use the socket module in a way
        that can block, and most handlers acquire threading locks.

    .. warning:: It *may* be possible for the logging functions to be
       called in the :class:`gevent.Hub` greenlet. Code running in the
       hub greenlet cannot use any gevent blocking functions without triggering
       a ``LoopExit``.

    .. versionadded:: 1.1a3

    .. versionchanged:: 1.1b6
       Attributes not present on this object are proxied to the underlying
       logger instance. This permits using custom :class:`~logging.Logger`
       subclasses (or indeed, even duck-typed objects).

    .. versionchanged:: 1.1
       Strip trailing newline characters on the message passed to :meth:`write`
       because log handlers will usually add one themselves.
    """

    def __init__(self, logger: Logger, level: int = 20) -> None:
        """
        Write information to the *logger* at the given *level* (default to INFO).
        """

    def write(self, msg: str) -> None: ...
    def flush(self) -> None:
        """No-op; required to be a file-like object"""

    def writelines(self, lines: Iterable[str]) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: object) -> None: ...
    def __delattr__(self, name: str) -> None: ...

class Environ(WSGIEnvironment):
    """
    A base class that can be used for WSGI environment objects.

    Provisional API.

    .. versionadded:: 1.2a1
    """

class SecureEnviron(Environ):
    """
    An environment that does not print its keys and values
    by default.

    Provisional API.

    This is intended to keep potentially sensitive information like
    HTTP authorization and cookies from being inadvertently printed
    or logged.

    For debugging, each instance can have its *secure_repr* attribute
    set to ``False``, which will cause it to print like a normal dict.

    When *secure_repr* is ``True`` (the default), then the value of
    the *whitelist_keys* attribute is consulted; if this value is
    true-ish, it should be a container (something that responds to
    ``in``) of key names (typically a list or set). Keys and values in
    this dictionary that are in *whitelist_keys* will then be printed,
    while all other values will be masked. These values may be
    customized on the class by setting the *default_secure_repr* and
    *default_whitelist_keys*, respectively::

        >>> environ = SecureEnviron(key='value')
        >>> environ # doctest: +ELLIPSIS
        <pywsgi.SecureEnviron dict (keys: 1) at ...

    If we whitelist the key, it gets printed::

        >>> environ.whitelist_keys = {'key'}
        >>> environ
        {'key': 'value'}

    A non-whitelisted key (*only*, to avoid doctest issues) is masked::

        >>> environ['secure'] = 'secret'; del environ['key']
        >>> environ
        {'secure': '<MASKED>'}

    We can turn it off entirely for the instance::

        >>> environ.secure_repr = False
        >>> environ
        {'secure': 'secret'}

    We can also customize it at the class level (here we use a new
    class to be explicit and to avoid polluting the true default
    values; we would set this class to be the ``environ_class`` of the
    server)::

        >>> class MyEnviron(SecureEnviron):
        ...    default_whitelist_keys = ('key',)
        ...
        >>> environ = MyEnviron({'key': 'value'})
        >>> environ
        {'key': 'value'}

    .. versionadded:: 1.2a1
    """

    default_secure_repr: ClassVar[bool]
    default_whitelist_keys: ClassVar[Container[str]]
    default_print_masked_keys: ClassVar[bool]
    secure_repr: bool
    whitelist_keys: Container[str]
    print_masked_keys: bool

class WSGISecureEnviron(SecureEnviron):
    """
    Specializes the default list of whitelisted keys to a few
    common WSGI variables.

    Example::

       >>> environ = WSGISecureEnviron(REMOTE_ADDR='::1', HTTP_AUTHORIZATION='secret')
       >>> environ
       {'REMOTE_ADDR': '::1', (hidden keys: 1)}
       >>> import pprint
       >>> pprint.pprint(environ)
       {'REMOTE_ADDR': '::1', (hidden keys: 1)}
       >>> print(pprint.pformat(environ))
       {'REMOTE_ADDR': '::1', (hidden keys: 1)}
    """

class WSGIServer(StreamServer):
    """
    A WSGI server based on :class:`StreamServer` that supports HTTPS.


    :keyword log: If given, an object with a ``write`` method to which
        request (access) logs will be written. If not given, defaults
        to :obj:`sys.stderr`. You may pass ``None`` to disable request
        logging. You may use a wrapper, around e.g., :mod:`logging`,
        to support objects that don't implement a ``write`` method.
        (If you pass a :class:`~logging.Logger` instance, or in
        general something that provides a ``log`` method but not a
        ``write`` method, such a wrapper will automatically be created
        and it will be logged to at the :data:`~logging.INFO` level.)

    :keyword error_log: If given, a file-like object with ``write``,
        ``writelines`` and ``flush`` methods to which error logs will
        be written. If not given, defaults to :obj:`sys.stderr`. You
        may pass ``None`` to disable error logging (not recommended).
        You may use a wrapper, around e.g., :mod:`logging`, to support
        objects that don't implement the proper methods. This
        parameter will become the value for ``wsgi.errors`` in the
        WSGI environment (if not already set). (As with *log*,
        wrappers for :class:`~logging.Logger` instances and the like
        will be created automatically and logged to at the :data:`~logging.ERROR`
        level.)

    .. seealso::

        :class:`LoggingLogAdapter`
            See important warnings before attempting to use :mod:`logging`.

    .. versionchanged:: 1.1a3
        Added the ``error_log`` parameter, and set ``wsgi.errors`` in the WSGI
        environment to this value.
    .. versionchanged:: 1.1a3
        Add support for passing :class:`logging.Logger` objects to the ``log`` and
        ``error_log`` arguments.
    .. versionchanged:: 20.6.0
        Passing a ``handle`` kwarg to the constructor is now officially deprecated.
    """

    handler_class: type[WSGIHandler]
    log: _LogOutputStream
    error_log: _LogOutputStream
    environ_class: type[WSGIEnvironment]
    secure_environ_class: type[SecureEnviron]
    base_env: WSGIEnvironment
    application: WSGIApplication
    @overload
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        application: WSGIApplication | None = None,
        backlog: int | None = None,
        spawn: _Spawner = "default",
        log: str | Logger | _LogOutputStream | None = "default",
        error_log: str | Logger | _LogOutputStream | None = "default",
        handler_class: type[WSGIHandler] | None = None,
        environ: WSGIEnvironment | None = None,
        *,
        ssl_context: SSLContext,
        server_side: bool = True,
        do_handshake_on_connect: bool = True,
        suppress_ragged_eofs: bool = True,
    ) -> None: ...
    @overload
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        application: WSGIApplication | None = None,
        backlog: int | None = None,
        spawn: _Spawner = "default",
        log: str | Logger | _LogOutputStream | None = "default",
        error_log: str | Logger | _LogOutputStream | None = "default",
        handler_class: type[WSGIHandler] | None = None,
        environ: WSGIEnvironment | None = None,
        *,
        keyfile: StrOrBytesPath = ...,
        certfile: StrOrBytesPath = ...,
        server_side: bool = True,
        cert_reqs: int = ...,
        ssl_version: int = ...,
        ca_certs: str = ...,
        do_handshake_on_connect: bool = True,
        suppress_ragged_eofs: bool = True,
        ciphers: str = ...,
    ) -> None: ...
    environ: WSGIEnvironment
    def set_environ(self, environ: WSGIEnvironment | None = None) -> None: ...
    max_accept: int
    def set_max_accept(self) -> None: ...
    def get_environ(self) -> WSGIEnvironment: ...
    def init_socket(self) -> None: ...
    def update_environ(self) -> None:
        """
        Called before the first request is handled to fill in WSGI environment values.

        This includes getting the correct server name and port.
        """

    def handle(self, sock: _GeventSocket, address: str) -> None:
        """
        Create an instance of :attr:`handler_class` to handle the request.

        This method blocks until the handler returns.
        """
