"""At its heart, Python can be viewed as an extension of the C
programming language. Springing from the most popular systems
programming language has made Python itself a great language for
systems programming. One key to success in this domain is Python's
very serviceable :mod:`socket` module and its :class:`socket.socket`
type.

The ``socketutils`` module provides natural next steps to the ``socket``
builtin: straightforward, tested building blocks for higher-level
protocols.

The :class:`BufferedSocket` wraps an ordinary socket, providing a
layer of intuitive buffering for both sending and receiving. This
facilitates parsing messages from streams, i.e., all sockets with type
``SOCK_STREAM``. The BufferedSocket enables receiving until the next
relevant token, up to a certain size, or until the connection is
closed. For all of these, it provides consistent APIs to size
limiting, as well as timeouts that are compatible with multiple
concurrency paradigms. Use it to parse the next one-off text or binary
socket protocol you encounter.

This module also provides the :class:`NetstringSocket`, a pure-Python
implementation of `the Netstring protocol`_, built on top of the
:class:`BufferedSocket`, serving as a ready-made, production-grade example.

Special thanks to `Kurt Rose`_ for his original authorship and all his
contributions on this module. Also thanks to `Daniel J. Bernstein`_, the
original author of `Netstring`_.

.. _the Netstring protocol: https://en.wikipedia.org/wiki/Netstring
.. _Kurt Rose: https://github.com/doublereedkurt
.. _Daniel J. Bernstein: https://cr.yp.to/
.. _Netstring: https://cr.yp.to/proto/netstrings.txt

"""

import socket
from _typeshed import ReadableBuffer, SliceableBuffer

DEFAULT_TIMEOUT: int
DEFAULT_MAXSIZE: int

class BufferedSocket:
    """Mainly provides recv_until and recv_size. recv, send, sendall, and
    peek all function as similarly as possible to the built-in socket
    API.

    This type has been tested against both the built-in socket type as
    well as those from gevent and eventlet. It also features support
    for sockets with timeouts set to 0 (aka nonblocking), provided the
    caller is prepared to handle the EWOULDBLOCK exceptions.

    Args:
        sock (socket): The connected socket to be wrapped.
        timeout (float): The default timeout for sends and recvs, in
            seconds. Set to ``None`` for no timeout, and 0 for
            nonblocking. Defaults to *sock*'s own timeout if already set,
            and 10 seconds otherwise.
        maxsize (int): The default maximum number of bytes to be received
            into the buffer before it is considered full and raises an
            exception. Defaults to 32 kilobytes.
        recvsize (int): The number of bytes to recv for every
            lower-level :meth:`socket.recv` call. Defaults to *maxsize*.

    *timeout* and *maxsize* can both be overridden on individual socket
    operations.

    All ``recv`` methods return bytestrings (:class:`bytes`) and can
    raise :exc:`socket.error`. :exc:`Timeout`,
    :exc:`ConnectionClosed`, and :exc:`MessageTooLong` all inherit
    from :exc:`socket.error` and exist to provide better error
    messages. Received bytes are always buffered, even if an exception
    is raised. Use :meth:`BufferedSocket.getrecvbuffer` to retrieve
    partial recvs.

    BufferedSocket does not replace the built-in socket by any
    means. While the overlapping parts of the API are kept parallel to
    the built-in :class:`socket.socket`, BufferedSocket does not
    inherit from socket, and most socket functionality is only
    available on the underlying socket. :meth:`socket.getpeername`,
    :meth:`socket.getsockname`, :meth:`socket.fileno`, and others are
    only available on the underlying socket that is wrapped. Use the
    ``BufferedSocket.sock`` attribute to access it. See the examples
    for more information on how to use BufferedSockets with built-in
    sockets.

    The BufferedSocket is threadsafe, but consider the semantics of
    your protocol before accessing a single socket from multiple
    threads. Similarly, once the BufferedSocket is constructed, avoid
    using the underlying socket directly. Only use it for operations
    unrelated to messages, e.g., :meth:`socket.getpeername`.

    """

    sock: socket.socket
    rbuf: bytes
    sbuf: list[SliceableBuffer]
    maxsize: int
    timeout: int
    def __init__(self, sock: socket.socket, timeout: int = ..., maxsize: int = 32768, recvsize: int = ...) -> None: ...
    def settimeout(self, timeout: float) -> None:
        """Set the default *timeout* for future operations, in seconds."""

    def gettimeout(self) -> float: ...
    def setblocking(self, blocking: bool) -> None: ...
    def setmaxsize(self, maxsize) -> None:
        """Set the default maximum buffer size *maxsize* for future
        operations, in bytes. Does not truncate the current buffer.
        """

    def getrecvbuffer(self) -> bytes:
        """Returns the receive buffer bytestring (rbuf)."""

    def getsendbuffer(self) -> bytes:
        """Returns a copy of the send buffer list."""

    def recv(self, size: int, flags: int = 0, timeout: float = ...) -> bytes:
        """Returns **up to** *size* bytes, using the internal buffer before
        performing a single :meth:`socket.recv` operation.

        Args:
            size (int): The maximum number of bytes to receive.
            flags (int): Kept for API compatibility with sockets. Only
                the default, ``0``, is valid.
            timeout (float): The timeout for this operation. Can be
                ``0`` for nonblocking and ``None`` for no
                timeout. Defaults to the value set in the constructor
                of BufferedSocket.

        If the operation does not complete in *timeout* seconds, a
        :exc:`Timeout` is raised. Much like the built-in
        :class:`socket.socket`, if this method returns an empty string,
        then the socket is closed and recv buffer is empty. Further
        calls to recv will raise :exc:`socket.error`.

        """

    def peek(self, size: int, timeout: float = ...) -> bytes:
        """Returns *size* bytes from the socket and/or internal buffer. Bytes
        are retained in BufferedSocket's internal recv buffer. To only
        see bytes in the recv buffer, use :meth:`getrecvbuffer`.

        Args:
            size (int): The exact number of bytes to peek at
            timeout (float): The timeout for this operation. Can be 0 for
                nonblocking and None for no timeout. Defaults to the value
                set in the constructor of BufferedSocket.

        If the appropriate number of bytes cannot be fetched from the
        buffer and socket before *timeout* expires, then a
        :exc:`Timeout` will be raised. If the connection is closed, a
        :exc:`ConnectionClosed` will be raised.
        """

    def recv_close(self, timeout: float = ..., maxsize: int = ...) -> bytes:
        """Receive until the connection is closed, up to *maxsize* bytes. If
        more than *maxsize* bytes are received, raises :exc:`MessageTooLong`.
        """

    def recv_until(
        self, delimiter: ReadableBuffer, timeout: float = ..., maxsize: int = ..., with_delimiter: bool = False
    ) -> bytes:
        """Receive until *delimiter* is found, *maxsize* bytes have been read,
        or *timeout* is exceeded.

        Args:
            delimiter (bytes): One or more bytes to be searched for
                in the socket stream.
            timeout (float): The timeout for this operation. Can be 0 for
                nonblocking and None for no timeout. Defaults to the value
                set in the constructor of BufferedSocket.
            maxsize (int): The maximum size for the internal buffer.
                Defaults to the value set in the constructor.
            with_delimiter (bool): Whether or not to include the
                delimiter in the output. ``False`` by default, but
                ``True`` is useful in cases where one is simply
                forwarding the messages.

        ``recv_until`` will raise the following exceptions:

          * :exc:`Timeout` if more than *timeout* seconds expire.
          * :exc:`ConnectionClosed` if the underlying socket is closed
            by the sending end.
          * :exc:`MessageTooLong` if the delimiter is not found in the
            first *maxsize* bytes.
          * :exc:`socket.error` if operating in nonblocking mode
            (*timeout* equal to 0), or if some unexpected socket error
            occurs, such as operating on a closed socket.

        """

    def recv_size(self, size: int, timeout: float = ...) -> bytes:
        """Read off of the internal buffer, then off the socket, until
        *size* bytes have been read.

        Args:
            size (int): number of bytes to read before returning.
            timeout (float): The timeout for this operation. Can be 0 for
                nonblocking and None for no timeout. Defaults to the value
                set in the constructor of BufferedSocket.

        If the appropriate number of bytes cannot be fetched from the
        buffer and socket before *timeout* expires, then a
        :exc:`Timeout` will be raised. If the connection is closed, a
        :exc:`ConnectionClosed` will be raised.
        """

    def send(self, data: SliceableBuffer, flags: int = 0, timeout: float = ...) -> str:
        """Send the contents of the internal send buffer, as well as *data*,
        to the receiving end of the connection. Returns the total
        number of bytes sent. If no exception is raised, all of *data* was
        sent and the internal send buffer is empty.

        Args:
            data (bytes): The bytes to send.
            flags (int): Kept for API compatibility with sockets. Only
                the default 0 is valid.
            timeout (float): The timeout for this operation. Can be 0 for
                nonblocking and None for no timeout. Defaults to the value
                set in the constructor of BufferedSocket.

        Will raise :exc:`Timeout` if the send operation fails to
        complete before *timeout*. In the event of an exception, use
        :meth:`BufferedSocket.getsendbuffer` to see which data was
        unsent.
        """

    def sendall(self, data: SliceableBuffer, flags: int = 0, timeout: float = ...) -> str:
        """A passthrough to :meth:`~BufferedSocket.send`, retained for
        parallelism to the :class:`socket.socket` API.
        """

    def flush(self) -> None:
        """Send the contents of the internal send buffer."""

    def buffer(self, data: SliceableBuffer) -> None:
        """Buffer *data* bytes for the next send operation."""

    def getsockname(self) -> str:
        """Convenience function to return the wrapped socket's own address.
        See :meth:`socket.getsockname` for more details.
        """

    def getpeername(self) -> str:
        """Convenience function to return the remote address to which the
        wrapped socket is connected.  See :meth:`socket.getpeername`
        for more details.
        """

    def getsockopt(self, level: int, optname: int, buflen: int | None = None) -> bytes | int:
        """Convenience function passing through to the wrapped socket's
        :meth:`socket.getsockopt`.
        """

    def setsockopt(self, level: int, optname: int, value: int | ReadableBuffer | None) -> bytes | int:
        """Convenience function passing through to the wrapped socket's
        :meth:`socket.setsockopt`.
        """

    @property
    def type(self) -> int:
        """A passthrough to the wrapped socket's type. Valid usages should
        only ever see :data:`socket.SOCK_STREAM`.
        """

    @property
    def family(self) -> int:
        """A passthrough to the wrapped socket's family. BufferedSocket
        supports all widely-used families, so this read-only attribute
        can be one of :data:`socket.AF_INET` for IP,
        :data:`socket.AF_INET6` for IPv6, and :data:`socket.AF_UNIX`
        for UDS.
        """

    @property
    def proto(self) -> int:
        """A passthrough to the wrapped socket's protocol. The ``proto``
        attribute is very rarely used, so it's always 0, meaning "the
        default" protocol. Pretty much all the practical information
        is in :attr:`~BufferedSocket.type` and
        :attr:`~BufferedSocket.family`, so you can go back to never
        thinking about this.
        """

    def fileno(self) -> int:
        """Returns the file descriptor of the wrapped socket. -1 if it has
        been closed on this end.

        Note that this makes the BufferedSocket selectable, i.e.,
        usable for operating system event loops without any external
        libraries. Keep in mind that the operating system cannot know
        about data in BufferedSocket's internal buffer. Exercise
        discipline with calling ``recv*`` functions.
        """
    rbuf_unconsumed: bytes
    def close(self) -> None:
        """Closes the wrapped socket, and empties the internal buffers. The
        send buffer is not flushed automatically, so if you have been
        calling :meth:`~BufferedSocket.buffer`, be sure to call
        :meth:`~BufferedSocket.flush` before calling this
        method. After calling this method, future socket operations
        will raise :exc:`socket.error`.
        """

    def shutdown(self, how: int) -> None:
        """Convenience method which passes through to the wrapped socket's
        :meth:`~socket.shutdown`. Semantics vary by platform, so no
        special internal handling is done with the buffers. This
        method exists to facilitate the most common usage, wherein a
        full ``shutdown`` is followed by a
        :meth:`~BufferedSocket.close`. Developers requiring more
        support, please open `an issue`_.

        .. _an issue: https://github.com/mahmoud/boltons/issues
        """

class Error(socket.error):
    """A subclass of :exc:`socket.error` from which all other
    ``socketutils`` exceptions inherit.

    When using :class:`BufferedSocket` and other ``socketutils``
    types, generally you want to catch one of the specific exception
    types below, or :exc:`socket.error`.
    """

class ConnectionClosed(Error):
    """Raised when receiving and the connection is unexpectedly closed
    from the sending end. Raised from :class:`BufferedSocket`'s
    :meth:`~BufferedSocket.peek`, :meth:`~BufferedSocket.recv_until`,
    and :meth:`~BufferedSocket.recv_size`, and never from its
    :meth:`~BufferedSocket.recv` or
    :meth:`~BufferedSocket.recv_close`.
    """

class MessageTooLong(Error):
    """Raised from :meth:`BufferedSocket.recv_until` and
    :meth:`BufferedSocket.recv_closed` when more than *maxsize* bytes are
    read without encountering the delimiter or a closed connection,
    respectively.
    """

    def __init__(self, bytes_read: int | None = None, delimiter: str | None = None) -> None: ...

class Timeout(socket.timeout, Error):
    """Inheriting from :exc:`socket.timeout`, Timeout is used to indicate
    when a socket operation did not complete within the time
    specified. Raised from any of :class:`BufferedSocket`'s ``recv``
    methods.
    """

    def __init__(self, timeout: float, extra: str = "") -> None: ...

class NetstringSocket:
    """
    Reads and writes using the netstring protocol.

    More info: https://en.wikipedia.org/wiki/Netstring
    Even more info: http://cr.yp.to/proto/netstrings.txt
    """

    bsock: BufferedSocket
    timeout: float
    maxsize: int
    def __init__(self, sock: socket.socket, timeout: float = 10, maxsize: int = 32768) -> None: ...
    def fileno(self) -> int: ...
    def settimeout(self, timeout: float) -> None: ...
    def setmaxsize(self, maxsize: int) -> None: ...
    def read_ns(self, timeout: float = ..., maxsize: int = ...): ...
    def write_ns(self, payload: bytes) -> None: ...

class NetstringProtocolError(Error):
    """Base class for all of socketutils' Netstring exception types."""

class NetstringInvalidSize(NetstringProtocolError):
    """NetstringInvalidSize is raised when the ``:``-delimited size prefix
    of the message does not contain a valid integer.

    Message showing valid size::

      5:hello,

    Here the ``5`` is the size. Anything in this prefix position that
    is not parsable as a Python integer (i.e., :class:`int`) will raise
    this exception.
    """

    def __init__(self, msg: str) -> None: ...

class NetstringMessageTooLong(NetstringProtocolError):
    """NetstringMessageTooLong is raised when the size prefix contains a
    valid integer, but that integer is larger than the
    :class:`NetstringSocket`'s configured *maxsize*.

    When this exception is raised, it's recommended to simply close
    the connection instead of trying to recover.
    """

    def __init__(self, size: int, maxsize: int) -> None: ...
