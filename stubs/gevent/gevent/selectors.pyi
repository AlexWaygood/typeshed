"""
This module provides :class:`GeventSelector`, a high-level IO
multiplexing mechanism. This is aliased to :class:`DefaultSelector`.

This module provides the same API as the selectors defined in :mod:`selectors`.

On Python 2, this module is only available if the `selectors2
<https://pypi.org/project/selectors2/>`_ backport is installed.

.. versionadded:: 20.6.0
"""

from _typeshed import FileDescriptorLike
from collections.abc import Mapping
from selectors import BaseSelector, SelectorKey
from typing import Any
from typing_extensions import TypeAlias

from gevent._util import Lazy
from gevent.hub import Hub

__all__ = ["DefaultSelector", "GeventSelector"]

_EventMask: TypeAlias = int

# technically this derives from _BaseSelectorImpl, which does not have type annotations
# but in terms of type checking the only difference is, that we need to add get_map since
# GeventSelector does not override it
class GeventSelector(BaseSelector):
    """
    A selector implementation using gevent primitives.

    This is a type of :class:`selectors.BaseSelector`, so the documentation
    for that class applies here.

    .. caution::
       As the base class indicates, it is critically important to
       unregister file objects before closing them. (Or close the selector
       they are registered with before closing them.) Failure to do so
       may crash the process or have other unintended results.
    """

    def __init__(self, hub: Hub | None = None) -> None: ...
    @Lazy
    def hub(self) -> Hub: ...
    def register(self, fileobj: FileDescriptorLike, events: _EventMask, data: Any = None) -> SelectorKey: ...
    def unregister(self, fileobj: FileDescriptorLike) -> SelectorKey: ...
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, _EventMask]]:
        """
        Poll for I/O.

        Note that, like the built-in selectors, this will block
        indefinitely if no timeout is given and no files have been
        registered.
        """

    def close(self) -> None: ...
    def get_map(self) -> Mapping[FileDescriptorLike, SelectorKey]: ...

DefaultSelector = GeventSelector
