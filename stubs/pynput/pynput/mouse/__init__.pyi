"""
The module containing mouse classes.

See the documentation for more information.
"""

from typing import Any

from pynput import _util

from ._base import Button as Button, Controller as Controller, Listener as Listener

class Events(_util.Events[Any, Listener]):
    """A mouse event listener supporting synchronous iteration over the events.

    Possible events are:

    :class:`Events.Move`
        The mouse was moved.

    :class:`Events.Click`
        A mouse button was pressed or released.

    :class:`Events.Scroll`
        The device was scrolled.
    """

    class Move(_util.Events.Event):
        """A move event."""

        x: int
        y: int
        injected: bool
        def __init__(self, x: int, y: int, injected: bool) -> None: ...

    class Click(_util.Events.Event):
        """A click event."""

        x: int
        y: int
        button: Button
        pressed: bool
        injected: bool
        def __init__(self, x: int, y: int, button: Button, pressed: bool, injected: bool) -> None: ...

    class Scroll(_util.Events.Event):
        """A scroll event."""

        x: int
        y: int
        dx: int
        dy: int
        injected: bool
        def __init__(self, x: int, y: int, dx: int, dy: int, injected: bool) -> None: ...

    def __init__(self) -> None: ...
    def __next__(self) -> Move | Click | Scroll: ...
    def get(self, timeout: float | None = None) -> Move | Click | Scroll | None:
        """Attempts to read the next event.

        :param int timeout: An optional timeout. If this is not provided, this
            method may block infinitely.

        :return: the next event, or ``None`` if the source has been stopped or
            no events were received
        """
