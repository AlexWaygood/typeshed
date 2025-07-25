"""
Interactive greenlet-based network console that can be used in any process.

The :class:`BackdoorServer` provides a REPL inside a running process. As
long as the process is monkey-patched, the ``BackdoorServer`` can coexist
with other elements of the process.

.. seealso:: :class:`code.InteractiveConsole`
"""

from _typeshed import StrOrBytesPath
from typing import Any, overload

from gevent.baseserver import _Spawner
from gevent.server import StreamServer, _Address
from gevent.socket import socket as _GeventSocket
from gevent.ssl import SSLContext

class BackdoorServer(StreamServer):
    """
    Provide a backdoor to a program for debugging purposes.

    .. warning:: This backdoor provides no authentication and makes no
          attempt to limit what remote users can do. Anyone that
          can access the server can take any action that the running
          python process can. Thus, while you may bind to any interface, for
          security purposes it is recommended that you bind to one
          only accessible to the local machine, e.g.,
          127.0.0.1/localhost.

    Basic usage::

        from gevent.backdoor import BackdoorServer
        server = BackdoorServer(('127.0.0.1', 5001),
                                banner="Hello from gevent backdoor!",
                                locals={'foo': "From defined scope!"})
        server.serve_forever()

    In a another terminal, connect with...::

        $ telnet 127.0.0.1 5001
        Trying 127.0.0.1...
        Connected to 127.0.0.1.
        Escape character is '^]'.
        Hello from gevent backdoor!
        >> print(foo)
        From defined scope!

    .. versionchanged:: 1.2a1
       Spawned greenlets are now tracked in a pool and killed when the server
       is stopped.
    """

    locals: dict[str, Any]
    banner: str | None
    @overload
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        locals: dict[str, Any] | None = None,
        banner: str | None = None,
        *,
        backlog: int | None = None,
        spawn: _Spawner = "default",
        ssl_context: SSLContext,
        server_side: bool = True,
        do_handshake_on_connect: bool = True,
        suppress_ragged_eofs: bool = True,
    ) -> None:
        """
        :keyword locals: If given, a dictionary of "builtin" values that will be available
            at the top-level.
        :keyword banner: If geven, a string that will be printed to each connecting user.
        """

    @overload
    def __init__(
        self,
        listener: _GeventSocket | tuple[str, int] | str,
        locals: dict[str, Any] | None = None,
        banner: str | None = None,
        *,
        backlog: int | None = None,
        spawn: _Spawner = "default",
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
    def handle(self, conn: _GeventSocket, _address: _Address) -> None:
        """
        Interact with one remote user.

        .. versionchanged:: 1.1b2 Each connection gets its own
            ``locals`` dictionary. Previously they were shared in a
            potentially unsafe manner.
        """

__all__ = ["BackdoorServer"]
