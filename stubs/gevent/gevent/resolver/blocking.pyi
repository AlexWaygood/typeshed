from gevent._types import _AddrinfoResult, _NameinfoResult, _SockAddr
from gevent.hub import Hub

class Resolver:
    """
    A resolver that directly uses the system's resolver functions.

    .. caution::

        This resolver is *not* cooperative.

    This resolver has the lowest overhead of any resolver and
    typically approaches the speed of the unmodified :mod:`socket`
    functions. However, it is not cooperative, so if name resolution
    blocks, the entire thread and all its greenlets will be blocked.

    This can be useful during debugging, or it may be a good choice if
    your operating system provides a good caching resolver (such as
    macOS's Directory Services) that is usually very fast and
    functionally non-blocking.

    .. versionchanged:: 1.3a2
       This was previously undocumented and existed in :mod:`gevent.socket`.

    """

    def __init__(self, hub: Hub | None = None) -> None: ...
    def close(self) -> None: ...
    def gethostbyname(self, hostname: str, family: int = 2) -> str:
        """gethostbyname(host) -> address

        Return the IP address (a string of the form '255.255.255.255') for a host.
        """

    def gethostbyname_ex(self, hostname: str, family: int = 2) -> tuple[str, list[str], list[str]]:
        """gethostbyname_ex(host) -> (name, aliaslist, addresslist)

        Return the true host name, a list of aliases, and a list of IP addresses,
        for a host.  The host argument is a string giving a host name or IP number.
        """

    def getaddrinfo(
        self, host: str, port: int, family: int = 0, socktype: int = 0, proto: int = 0, flags: int = 0
    ) -> _AddrinfoResult:
        """getaddrinfo(host, port [, family, type, proto, flags])
            -> list of (family, type, proto, canonname, sockaddr)

        Resolve host and port into addrinfo struct.
        """

    def gethostbyaddr(self, ip_address: str) -> tuple[str, list[str], list[str]]:
        """gethostbyaddr(host) -> (name, aliaslist, addresslist)

        Return the true host name, a list of aliases, and a list of IP addresses,
        for a host.  The host argument is a string giving a host name or IP number.
        """

    def getnameinfo(self, sockaddr: _SockAddr, flags: int) -> _NameinfoResult:
        """getnameinfo(sockaddr, flags) --> (host, port)

        Get host and port for a sockaddr.
        """

__all__ = ["Resolver"]
