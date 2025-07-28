"""
Publish/subscribe event infrastructure.

When certain "interesting" things happen during the lifetime of the
process, gevent will "publish" an event (an object). That event is
delivered to interested "subscribers" (functions that take one
parameter, the event object).

Higher level frameworks may take this foundation and build richer
models on it.

:mod:`zope.event` will be used to provide the functionality of
`notify` and `subscribers`. See :mod:`zope.event.classhandler` for a
simple class-based approach to subscribing to a filtered list of
events, and see `zope.component
<https://zopecomponent.readthedocs.io/en/latest/event.html>`_ for a
much higher-level, flexible system. If you are using one of these
systems, you generally will not want to directly modify `subscribers`.

.. versionadded:: 1.3b1

.. versionchanged:: 23.7.0
   Now uses :mod:`importlib.metadata` instead of :mod:`pkg_resources`
   to locate entry points.
"""

import sys
from collections.abc import Callable, Mapping, Sequence
from types import ModuleType
from typing import Any, Protocol, TypeVar
from typing_extensions import TypeAlias

from gevent.hub import Hub
from greenlet import greenlet as greenlet_t

_T = TypeVar("_T")
# FIXME: While it would be nice to import Interface from zope.interface here so the
#        mypy plugin will work correctly for the people that use it, it causes all
#        sorts of issues to reference a module that is not stubbed in typeshed, so
#        for now we punt and just define an alias for Interface and implementer we
#        can get rid of later
Interface: TypeAlias = Any

def implementer(interface: Interface, /) -> Callable[[_T], _T]:
    """
    Declare the interfaces implemented by instances of a class.

    This function is called as a class decorator.

    The arguments are one or more interfaces or interface specifications
    (`~zope.interface.interfaces.IDeclaration` objects).

    The interfaces given (including the interfaces in the specifications) are
    added to any interfaces previously declared, unless the interface is
    already implemented.

    Previous declarations include declarations for base classes unless
    implementsOnly was used.

    This function is provided for convenience. It provides a more convenient
    way to call `classImplements`. For example::

        @implementer(I1)
        class C(object):
            pass

    is equivalent to calling::

        classImplements(C, I1)

    after the class has been created.

    .. seealso:: `classImplements`
       The change history provided there applies to this function too.
    """

# this is copied from types-psutil, it would be nice if we could just import this
# but it doesn't seem like we can...
if sys.platform == "linux":
    from psutil._pslinux import pmem
elif sys.platform == "darwin":
    from psutil._psosx import pmem
elif sys.platform == "win32":
    from psutil._pswindows import pmem
else:
    class pmem(Any): ...

subscribers: list[Callable[[Any], object]]

class _PeriodicMonitorThread(Protocol):
    def add_monitoring_function(self, function: Callable[[Hub], object], period: float | None) -> object: ...

class IPeriodicMonitorThread(Interface):
    """
    The contract for the periodic monitoring thread that is started
    by the hub.
    """

    def add_monitoring_function(function: Callable[[Hub], object], period: float | None) -> object: ...

class IPeriodicMonitorThreadStartedEvent(Interface):
    """
    The event emitted when a hub starts a periodic monitoring thread.

    You can use this event to add additional monitoring functions.
    """

    monitor: IPeriodicMonitorThread

@implementer(IPeriodicMonitorThread)
class PeriodicMonitorThreadStartedEvent:
    """
    The implementation of :class:`IPeriodicMonitorThreadStartedEvent`.

    .. versionchanged:: 24.11.1
       Now actually implements the promised interface.
    """

    ENTRY_POINT_NAME: str
    monitor: _PeriodicMonitorThread
    def __init__(self, monitor: _PeriodicMonitorThread) -> None: ...

class IEventLoopBlocked(Interface):
    """
    The event emitted when the event loop is blocked.

    This event is emitted in the monitor thread.

    .. versionchanged:: 24.11.1
       Add the *hub* attribute.
    """

    greenlet: greenlet_t
    blocking_time: float
    info: Sequence[str]
    hub: Hub | None

@implementer(IEventLoopBlocked)
class EventLoopBlocked:
    """
    The event emitted when the event loop is blocked.

    Implements `IEventLoopBlocked`.
    """

    greenlet: greenlet_t
    blocking_time: float
    info: Sequence[str]
    hub: Hub | None
    def __init__(self, greenlet: greenlet_t, blocking_time: float, info: Sequence[str], *, hub: Hub | None = None) -> None: ...

class IMemoryUsageThresholdExceeded(Interface):
    """
    The event emitted when the memory usage threshold is exceeded.

    This event is emitted only while memory continues to grow
    above the threshold. Only if the condition or stabilized is corrected (memory
    usage drops) will the event be emitted in the future.

    This event is emitted in the monitor thread.
    """

    mem_usage: int
    max_allowed: int
    memory_info: pmem

class _AbstractMemoryEvent:
    mem_usage: int
    max_allowed: int
    memory_info: pmem
    def __init__(self, mem_usage: int, max_allowed: int, memory_info: pmem) -> None: ...

@implementer(IMemoryUsageThresholdExceeded)
class MemoryUsageThresholdExceeded(_AbstractMemoryEvent):
    """
    Implementation of `IMemoryUsageThresholdExceeded`.
    """

class IMemoryUsageUnderThreshold(Interface):
    """
    The event emitted when the memory usage drops below the
    threshold after having previously been above it.

    This event is emitted only the first time memory usage is detected
    to be below the threshold after having previously been above it.
    If memory usage climbs again, a `IMemoryUsageThresholdExceeded`
    event will be broadcast, and then this event could be broadcast again.

    This event is emitted in the monitor thread.
    """

    mem_usage: int
    max_allowed: int
    max_memory_usage: int
    memory_info: pmem

@implementer(IMemoryUsageUnderThreshold)
class MemoryUsageUnderThreshold(_AbstractMemoryEvent):
    """
    Implementation of `IMemoryUsageUnderThreshold`.
    """

    max_memory_usage: int
    def __init__(self, mem_usage: int, max_allowed: int, memory_info: pmem, max_usage: int) -> None: ...

class IGeventPatchEvent(Interface):
    """
    The root for all monkey-patch events gevent emits.
    """

    source: object
    target: object

@implementer(IGeventPatchEvent)
class GeventPatchEvent:
    """
    Implementation of `IGeventPatchEvent`.
    """

    source: object
    target: object
    def __init__(self, source: object, target: object) -> None: ...

class IGeventWillPatchEvent(IGeventPatchEvent):
    """
    An event emitted *before* gevent monkey-patches something.

    If a subscriber raises `DoNotPatch`, then patching this particular
    item will not take place.
    """

class DoNotPatch(BaseException):
    """
    Subscribers to will-patch events can raise instances
    of this class to tell gevent not to patch that particular item.
    """

@implementer(IGeventWillPatchEvent)
class GeventWillPatchEvent(GeventPatchEvent):
    """
    Implementation of `IGeventWillPatchEvent`.
    """

class IGeventDidPatchEvent(IGeventPatchEvent):
    """
    An event emitted *after* gevent has patched something.
    """

@implementer(IGeventWillPatchEvent)
class GeventDidPatchEvent(GeventPatchEvent):
    """
    Implementation of `IGeventDidPatchEvent`.
    """

class IGeventWillPatchModuleEvent(IGeventWillPatchEvent):
    """
    An event emitted *before* gevent begins patching a specific module.

    Both *source* and *target* attributes are module objects.
    """

    source: ModuleType
    target: ModuleType
    module_name: str
    target_item_names: list[str]

@implementer(IGeventWillPatchModuleEvent)
class GeventWillPatchModuleEvent(GeventWillPatchEvent):
    """
    Implementation of `IGeventWillPatchModuleEvent`.
    """

    ENTRY_POINT_NAME: str
    source: ModuleType
    target: ModuleType
    module_name: str
    target_item_names: list[str]
    def __init__(self, module_name: str, source: ModuleType, target: ModuleType, items: list[str]) -> None: ...

class IGeventDidPatchModuleEvent(IGeventDidPatchEvent):
    """
    An event emitted *after* gevent has completed patching a specific
    module.
    """

    source: ModuleType
    target: ModuleType
    module_name: str

@implementer(IGeventDidPatchModuleEvent)
class GeventDidPatchModuleEvent(GeventDidPatchEvent):
    """
    Implementation of `IGeventDidPatchModuleEvent`.
    """

    ENTRY_POINT_NAME: str
    source: ModuleType
    target: ModuleType
    module_name: str
    def __init__(self, module_name: str, source: ModuleType, target: ModuleType) -> None: ...

class IGeventWillPatchAllEvent(IGeventWillPatchEvent):
    """
    An event emitted *before* gevent begins patching the system.

    Following this event will be a series of
    `IGeventWillPatchModuleEvent` and `IGeventDidPatchModuleEvent` for
    each patched module.

    Once the gevent builtin modules have been processed,
    `IGeventDidPatchBuiltinModulesEvent` will be emitted. Processing
    this event is an ideal time for third-party modules to be imported
    and patched (which may trigger its own will/did patch module
    events).

    Finally, a `IGeventDidPatchAllEvent` will be sent.

    If a subscriber to this event raises `DoNotPatch`, no patching
    will be done.

    The *source* and *target* attributes have undefined values.
    """

    patch_all_arguments: Mapping[str, Any]
    patch_all_kwargs: Mapping[str, Any]
    def will_patch_module(module_name: str) -> bool: ...

class _PatchAllMixin:
    def __init__(self, patch_all_arguments: Mapping[str, Any], patch_all_kwargs: Mapping[str, Any]) -> None: ...
    @property
    def patch_all_arguments(self) -> dict[str, Any]: ...  # safe to mutate, it's a copy
    @property
    def patch_all_kwargs(self) -> dict[str, Any]: ...  # safe to mutate, it's a copy

@implementer(IGeventWillPatchAllEvent)
class GeventWillPatchAllEvent(_PatchAllMixin, GeventWillPatchEvent):
    """
    Implementation of `IGeventWillPatchAllEvent`.
    """

    ENTRY_POINT_NAME: str
    def will_patch_module(self, module_name: str) -> bool: ...

class IGeventDidPatchBuiltinModulesEvent(IGeventDidPatchEvent):
    """
    Event emitted *after* the builtin modules have been patched.

    If you're going to monkey-patch a third-party library, this is
    usually the event to listen for.

    The values of the *source* and *target* attributes are undefined.
    """

    patch_all_arguments: Mapping[str, Any]
    patch_all_kwargs: Mapping[str, Any]

@implementer(IGeventDidPatchBuiltinModulesEvent)
class GeventDidPatchBuiltinModulesEvent(_PatchAllMixin, GeventDidPatchEvent):
    """
    Implementation of `IGeventDidPatchBuiltinModulesEvent`.
    """

    ENTRY_POINT_NAME: str

class IGeventDidPatchAllEvent(IGeventDidPatchEvent):
    """
    Event emitted after gevent has patched all modules, both builtin
    and those provided by plugins/subscribers.

    The values of the *source* and *target* attributes are undefined.
    """

@implementer(IGeventDidPatchAllEvent)
class GeventDidPatchAllEvent(_PatchAllMixin, GeventDidPatchEvent):
    """
    Implementation of `IGeventDidPatchAllEvent`.
    """

    ENTRY_POINT_NAME: str

__all__ = [
    "subscribers",
    # monitor thread
    "IEventLoopBlocked",
    "EventLoopBlocked",
    "IMemoryUsageThresholdExceeded",
    "MemoryUsageThresholdExceeded",
    "IMemoryUsageUnderThreshold",
    "MemoryUsageUnderThreshold",
    # Hub
    "IPeriodicMonitorThread",
    "IPeriodicMonitorThreadStartedEvent",
    "PeriodicMonitorThreadStartedEvent",
    # monkey
    "IGeventPatchEvent",
    "GeventPatchEvent",
    "IGeventWillPatchEvent",
    "DoNotPatch",
    "GeventWillPatchEvent",
    "IGeventDidPatchEvent",
    "IGeventWillPatchModuleEvent",
    "GeventWillPatchModuleEvent",
    "IGeventDidPatchModuleEvent",
    "GeventDidPatchModuleEvent",
    "IGeventWillPatchAllEvent",
    "GeventWillPatchAllEvent",
    "IGeventDidPatchBuiltinModulesEvent",
    "GeventDidPatchBuiltinModulesEvent",
    "IGeventDidPatchAllEvent",
    "GeventDidPatchAllEvent",
]
