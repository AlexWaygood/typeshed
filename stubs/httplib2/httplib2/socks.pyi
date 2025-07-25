"""SocksiPy - Python SOCKS module.

Version 1.00

Copyright 2006 Dan-Haim. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of Dan Haim nor the names of his contributors may be used
   to endorse or promote products derived from this software without specific
   prior written permission.

THIS SOFTWARE IS PROVIDED BY DAN HAIM "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL DAN HAIM OR HIS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA
OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMANGE.

This module provides a standard socket-like interface for Python
for tunneling connections through SOCKS proxies.

Minor modifications made by Christopher Gilbert (http://motomastyle.com/) for
use in PyLoris (http://pyloris.sourceforge.net/).

Minor modifications made by Mario Vilas (http://breakingcode.wordpress.com/)
mainly to merge bug fixes found in Sourceforge.
"""

import socket
from _typeshed import Incomplete, ReadableBuffer
from types import ModuleType
from typing import Final, Literal
from typing_extensions import TypeAlias

_ProxyType: TypeAlias = Literal[1, 2, 3, 4]

PROXY_TYPE_SOCKS4: Final[_ProxyType]
PROXY_TYPE_SOCKS5: Final[_ProxyType]
PROXY_TYPE_HTTP: Final[_ProxyType]
PROXY_TYPE_HTTP_NO_TUNNEL: Final[_ProxyType]

class ProxyError(Exception): ...
class GeneralProxyError(ProxyError): ...
class Socks5AuthError(ProxyError): ...
class Socks5Error(ProxyError): ...
class Socks4Error(ProxyError): ...
class HTTPError(ProxyError): ...

def setdefaultproxy(
    proxytype: _ProxyType | None = None,
    addr: str | None = None,
    port: int | None = None,
    rdns: bool = True,
    username: str | None = None,
    password: str | None = None,
) -> None:
    """setdefaultproxy(proxytype, addr[, port[, rdns[, username[, password]]]])
    Sets a default proxy which all further socksocket objects will use,
    unless explicitly changed.
    """

def wrapmodule(module: ModuleType) -> None:
    """wrapmodule(module)

    Attempts to replace a module's socket library with a SOCKS socket. Must set
    a default proxy using setdefaultproxy(...) first.
    This will only work on modules that import socket directly into the
    namespace;
    most of the Python Standard Library falls into this category.
    """

class socksocket(socket.socket):
    """socksocket([family[, type[, proto]]]) -> socket object
    Open a SOCKS enabled socket. The parameters are the same as
    those of the standard socket init. In order for SOCKS to work,
    you must specify family=AF_INET, type=SOCK_STREAM and proto=0.
    """

    def __init__(
        self,
        family: socket.AddressFamily | int = ...,
        type: socket.SocketKind | int = ...,
        proto: int = 0,
        _sock: int | None = None,
    ) -> None: ...
    def sendall(self, content: ReadableBuffer, flags: int = ...) -> None:  # type: ignore[override]
        """override socket.socket.sendall method to rewrite the header
        for non-tunneling proxies if needed
        """

    def setproxy(
        self,
        proxytype: _ProxyType | None = None,
        addr: str | None = None,
        port: int | None = None,
        rdns: bool = True,
        username: str | None = None,
        password: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """setproxy(proxytype, addr[, port[, rdns[, username[, password]]]])

        Sets the proxy to be used.
        proxytype -    The type of the proxy to be used. Three types
                are supported: PROXY_TYPE_SOCKS4 (including socks4a),
                PROXY_TYPE_SOCKS5 and PROXY_TYPE_HTTP
        addr -        The address of the server (IP or DNS).
        port -        The port of the server. Defaults to 1080 for SOCKS
                servers and 8080 for HTTP proxy servers.
        rdns -        Should DNS queries be preformed on the remote side
                (rather than the local side). The default is True.
                Note: This has no effect with SOCKS4 servers.
        username -    Username to authenticate with to the server.
                The default is no authentication.
        password -    Password to authenticate with to the server.
                Only relevant when username is also provided.
        headers -     Additional or modified headers for the proxy connect
        request.
        """

    def getproxysockname(self) -> tuple[str | bytes, Incomplete] | None:
        """getsockname() -> address info
        Returns the bound IP address and port number at the proxy.
        """

    def getproxypeername(self) -> socket._RetAddress:
        """getproxypeername() -> address info
        Returns the IP and port number of the proxy.
        """

    def getpeername(self) -> tuple[str | bytes, Incomplete] | None:
        """getpeername() -> address info
        Returns the IP address and port number of the destination
        machine (note: getproxypeername returns the proxy)
        """

    def connect(self, destpair: list[str | bytes | int] | tuple[str | bytes, int]) -> None:  # type: ignore[override]
        """connect(self, despair)
        Connects to the specified destination through a proxy.
        destpar - A tuple of the IP/DNS address and the port number.
        (identical to socket's connect).
        To select the proxy server use setproxy().
        """
