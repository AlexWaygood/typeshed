"""
A collection of primitives used by the hub, and suitable for
compilation with Cython because of their frequency of use.

"""

from abc import abstractmethod
from typing import Any, NoReturn

from gevent._types import _Loop
from greenlet import greenlet

class TrackedRawGreenlet(greenlet):
    """TrackedRawGreenlet(function, parent)"""

class SwitchOutGreenletWithLoop(TrackedRawGreenlet):
    @property
    @abstractmethod
    def loop(self) -> _Loop:
        """loop: object"""

    @loop.setter
    def loop(self, value: _Loop) -> None: ...
    def switch(self) -> Any:
        """SwitchOutGreenletWithLoop.switch(self)"""

    def switch_out(self) -> NoReturn:
        """SwitchOutGreenletWithLoop.switch_out(self)"""

__all__ = ["TrackedRawGreenlet", "SwitchOutGreenletWithLoop"]
