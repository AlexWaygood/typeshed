"""TCP/SSL server"""

from _socket import _Address as _StrictAddress
from _typeshed import ReadableBuffer, StrOrBytesPath
from collections.abc import Callable
from typing import Any, ClassVar, TypedDict, overload
from typing_extensions import TypeAlias

from gevent.baseserver import BaseServer, _Spawner
from gevent.socket import socket as _GeventSocket
from gevent.ssl import SSLContext, wrap_socket as ssl_wrap_socket

# For simplicity we treat _Address as Any, we could be more strict and use the definition
# from the stdlib _socket.pyi. But that would exclude some potentially valid handlers.
_Address: TypeAlias = Any

class _SSLArguments(TypedDict, total=False):
    keyfile: StrOrBytesPath
    certfile: StrOrBytesPath
    server_side: bool
    cert_reqs: int
    ssl_version: int
    ca_certs: str
    suppress_ragged_eofs: bool
    do_handshake_on_connect: bool
    ciphers: str

class StreamServer(BaseServer[[_GeventSocket, _Address]]):
    """
    A generic TCP server.

    Accepts connections on a listening socket and spawns user-provided
    *handle* function for each connection with 2 arguments: the client
    socket and the client address.

    Note that although the errors in a successfully spawned handler
    will not affect the server or other connections, the errors raised
    by :func:`accept` and *spawn* cause the server to stop accepting
    for a short amount of time. The exact period depends on the values
    of :attr:`min_delay` and :attr:`max_delay` attributes.

    The delay starts with :attr:`min_delay` and doubles with each
    successive error until it reaches :attr:`max_delay`. A successful
    :func:`accept` resets the delay to :attr:`min_delay` again.

    See :class:`~gevent.baseserver.BaseServer` for information on defining the *handle*
    function and important restrictions on it.

    **SSL Support**

    The server can optionally work in SSL mode when given the correct
    keyword arguments. (That is, the presence of any keyword arguments
    will trigger SSL mode.) On Python 2.7.9 and later (any Python
    version that supports the :class:`ssl.SSLContext`), this can be
    done with a configured ``SSLContext``. On any Python version, it
    can be done by passing the appropriate arguments for
    :func:`ssl.wrap_socket`.

    The incoming socket will be wrapped into an SSL socket before
    being passed to the *handle* function.

    If the *ssl_context* keyword argument is present, it should
    contain an :class:`ssl.SSLContext`. The remaining keyword
    arguments are passed to the :meth:`ssl.SSLContext.wrap_socket`
    method of that object. Depending on the Python version, supported arguments
    may include:

    - server_hostname
    - suppress_ragged_eofs
    - do_handshake_on_connect

    .. caution:: When using an SSLContext, it should either be
       imported from :mod:`gevent.ssl`, or the process needs to be monkey-patched.
       If the process is not monkey-patched and you pass the standard library
       SSLContext, the resulting client sockets will not cooperate with gevent.

    Otherwise, keyword arguments are assumed to apply to :func:`ssl.wrap_socket`.
    These keyword arguments may include:

    - keyfile
    - certfile
    - cert_reqs
    - ssl_version
    - ca_certs
    - suppress_ragged_eofs
    - do_handshake_on_connect
    - ciphers

    .. versionchanged:: 1.2a2
       Add support for the *ssl_context* keyword argument.

    """

    backlog: int
    reuse_addr: ClassVar[int | None]
    wrap_socket = ssl_wrap_socket
    ssl_args: _SSLArguments | None
    @overload
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        handle: Callable[[_GeventSocket, _Address], object] | None = None,
        backlog: int | None = None,
        spawn: _Spawner = "default",
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
        handle: Callable[[_GeventSocket, _Address], object] | None = None,
        backlog: int | None = None,
        spawn: _Spawner = "default",
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
    @property
    def ssl_enabled(self) -> bool: ...
    @classmethod
    def get_listener(cls, address: _StrictAddress, backlog: int | None = None, family: int | None = None) -> _GeventSocket: ...
    def do_read(self) -> tuple[_GeventSocket, _Address]: ...
    def do_close(self, sock: _GeventSocket, address: _Address) -> None: ...
    def wrap_socket_and_handle(self, client_socket: _GeventSocket, address: _StrictAddress) -> Any: ...

class DatagramServer(BaseServer[[_GeventSocket, _Address]]):
    """A UDP server"""

    reuse_addr: ClassVar[int | None]
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        handle: Callable[[_GeventSocket, _Address], object] | None = None,
        spawn: _Spawner = "default",
    ) -> None: ...
    @classmethod
    def get_listener(cls, address: _StrictAddress, family: int | None = None) -> _GeventSocket: ...
    def do_read(self) -> tuple[_GeventSocket, _Address]: ...
    @overload
    def sendto(self, data: ReadableBuffer, address: _StrictAddress, /) -> int: ...
    @overload
    def sendto(self, data: ReadableBuffer, flags: int, address: _StrictAddress, /) -> int: ...

__all__ = ["StreamServer", "DatagramServer"]
