"""
Maintains the thread local hub.

"""

from gevent._types import _Loop
from gevent.hub import Hub as _Hub

__all__ = ["get_hub", "get_hub_noargs", "get_hub_if_exists"]

Hub: type[_Hub] | None

def get_hub_class() -> type[_Hub] | None:
    """Return the type of hub to use for the current thread.

    If there's no type of hub for the current thread yet, 'gevent.hub.Hub' is used.
    """

def set_default_hub_class(hubtype: type[_Hub]) -> None: ...
def get_hub() -> _Hub:
    """
    Return the hub for the current thread.

    If a hub does not exist in the current thread, a new one is
    created of the type returned by :func:`get_hub_class`.

    .. deprecated:: 1.3b1
       The ``*args`` and ``**kwargs`` arguments are deprecated. They were
       only used when the hub was created, and so were non-deterministic---to be
       sure they were used, *all* callers had to pass them, or they were order-dependent.
       Use ``set_hub`` instead.

    .. versionchanged:: 1.5a3
       The *args* and *kwargs* arguments are now completely ignored.

    .. versionchanged:: 23.7.0
       The long-deprecated ``args`` and ``kwargs`` parameters are no
       longer accepted.
    """

def get_hub_noargs() -> _Hub: ...
def get_hub_if_exists() -> _Hub | None:
    """
    Return the hub for the current thread.

    Return ``None`` if no hub has been created yet.
    """

def set_hub(hub: _Hub) -> None: ...
def get_loop() -> _Loop: ...
def set_loop(loop: _Loop) -> None: ...
