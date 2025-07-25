from typing import Any

from gevent.hub import Hub
from gevent.resolver import AbstractResolver

class Resolver(AbstractResolver):
    """
    An *experimental* resolver that uses `dnspython`_.

    This is typically slower than the default threaded resolver
    (unless there's a cache hit, in which case it can be much faster).
    It is usually much faster than the c-ares resolver. It tends to
    scale well as more concurrent resolutions are attempted.

    Under Python 2, if the ``idna`` package is installed, this
    resolver can resolve Unicode host names that the system resolver
    cannot.

    .. note::

        This **does not** use dnspython's default resolver object, or share any
        classes with ``import dns``. A separate copy of the objects is imported to
        be able to function in a non monkey-patched process. The documentation for the resolver
        object still applies.

        The resolver that we use is available as the :attr:`resolver` attribute
        of this object (typically ``gevent.get_hub().resolver.resolver``).

    .. caution::

        Many of the same caveats about DNS results apply here as are documented
        for :class:`gevent.resolver.ares.Resolver`. In addition, the handling of
        symbolic scope IDs in IPv6 addresses passed to ``getaddrinfo`` exhibits
        some differences.

        On PyPy, ``getnameinfo`` can produce results when CPython raises
        ``socket.error``, and gevent's DNSPython resolver also
        raises ``socket.error``.

    .. caution::

        This resolver is experimental. It may be removed or modified in
        the future. As always, feedback is welcome.

    .. versionadded:: 1.3a2

    .. versionchanged:: 20.5.0
       The errors raised are now much more consistent with those
       raised by the standard library resolvers.

       Handling of localhost and broadcast names is now more consistent.

    .. _dnspython: http://www.dnspython.org
    """

    def __init__(self, hub: Hub | None = ...) -> None: ...
    @property
    def resolver(self) -> Any:  # this is a custom dnspython Resolver
        """
        The dnspython resolver object we use.

        This object has several useful attributes that can be used to
        adjust the behaviour of the DNS system:

        * ``cache`` is a :class:`dns.resolver.LRUCache`. Its maximum size
          can be configured by calling :meth:`resolver.cache.set_max_size`
        * ``nameservers`` controls which nameservers to talk to
        * ``lifetime`` configures a timeout for each individual query.
        """

__all__ = ["Resolver"]
