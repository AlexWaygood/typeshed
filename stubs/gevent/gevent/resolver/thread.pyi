"""
Native thread-based hostname resolver.
"""

from gevent._types import _AddrinfoResult, _NameinfoResult, _SockAddr
from gevent.hub import Hub
from gevent.threadpool import ThreadPool

class Resolver:
    """
    Implementation of the resolver API using native threads and native resolution
    functions.

    Using the native resolution mechanisms ensures the highest
    compatibility with what a non-gevent program would return
    including good support for platform specific configuration
    mechanisms. The use of native (non-greenlet) threads ensures that
    a caller doesn't block other greenlets.

    This implementation also has the benefit of being very simple in comparison to
    :class:`gevent.resolver_ares.Resolver`.

    .. tip::

        Most users find this resolver to be quite reliable in a
        properly monkey-patched environment. However, there have been
        some reports of long delays, slow performance or even hangs,
        particularly in long-lived programs that make many, many DNS
        requests. If you suspect that may be happening to you, try the
        dnspython or ares resolver (and submit a bug report).
    """

    pool: ThreadPool
    def __init__(self, hub: Hub | None = None) -> None: ...
    def close(self) -> None: ...
    def gethostbyname(self, hostname: str, family: int = 2) -> str: ...
    def gethostbyname_ex(self, hostname: str, family: int = 2) -> tuple[str, list[str], list[str]]: ...
    def getaddrinfo(
        self, host: str, port: int, family: int = 0, socktype: int = 0, proto: int = 0, flags: int = 0
    ) -> _AddrinfoResult: ...
    def gethostbyaddr(self, ip_address: str) -> tuple[str, list[str], list[str]]: ...
    def getnameinfo(self, sockaddr: _SockAddr, flags: int) -> _NameinfoResult: ...

__all__ = ["Resolver"]
