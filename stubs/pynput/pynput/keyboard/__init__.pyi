"""
The module containing keyboard classes.

See the documentation for more information.
"""

from _typeshed import SupportsItems
from collections.abc import Callable
from typing import Any

from pynput import _util

from ._base import Controller as Controller, Key as Key, KeyCode as KeyCode, Listener as Listener

class Events(_util.Events[Any, Listener]):
    """A keyboard event listener supporting synchronous iteration over the
    events.

    Possible events are:

    :class:`Events.Press`
        A key was pressed.

    :class:`Events.Release`
        A key was released.
    """

    class Press(_util.Events.Event):
        """A key press event."""

        key: Key | KeyCode | None
        injected: bool
        def __init__(self, key: Key | KeyCode | None, injected: bool) -> None: ...

    class Release(_util.Events.Event):
        """A key release event."""

        key: Key | KeyCode | None
        injected: bool
        def __init__(self, key: Key | KeyCode | None, injected: bool) -> None: ...

    def __init__(self) -> None: ...
    def __next__(self) -> Press | Release: ...
    def get(self, timeout: float | None = None) -> Press | Release | None:
        """Attempts to read the next event.

        :param int timeout: An optional timeout. If this is not provided, this
            method may block infinitely.

        :return: the next event, or ``None`` if the source has been stopped or
            no events were received
        """

class HotKey:
    """A combination of keys acting as a hotkey.

    This class acts as a container of hotkey state for a keyboard listener.

    :param set keys: The collection of keys that must be pressed for this
        hotkey to activate. Please note that a common limitation of the
        hardware is that at most three simultaneously pressed keys are
        supported, so using more keys may not work.

    :param callable on_activate: The activation callback.
    """

    def __init__(self, keys: list[KeyCode], on_activate: Callable[[], object]) -> None: ...
    @staticmethod
    def parse(keys: str) -> list[KeyCode]:
        """Parses a key combination string.

        Key combination strings are sequences of key identifiers separated by
        ``'+'``. Key identifiers are either single characters representing a
        keyboard key, such as ``'a'``, or special key names identified by names
        enclosed by brackets, such as ``'<ctrl>'``.

        Keyboard keys are case-insensitive.

        :raises ValueError: if a part of the keys string is invalid, or if it
            contains multiple equal parts
        """

    def press(self, key: Key | KeyCode) -> None:
        """Updates the hotkey state for a pressed key.

        If the key is not currently pressed, but is the last key for the full
        combination, the activation callback will be invoked.

        Please note that the callback will only be invoked once.

        :param key: The key being pressed.
        :type key: Key or KeyCode
        """

    def release(self, key: Key | KeyCode) -> None:
        """Updates the hotkey state for a released key.

        :param key: The key being released.
        :type key: Key or KeyCode
        """

class GlobalHotKeys(Listener):
    """A keyboard listener supporting a number of global hotkeys.

    This is a convenience wrapper to simplify registering a number of global
    hotkeys.

    :param dict hotkeys: A mapping from hotkey description to hotkey action.
        Keys are strings passed to :meth:`HotKey.parse`.

    :raises ValueError: if any hotkey description is invalid
    """

    def __init__(self, hotkeys: SupportsItems[str, Callable[[], None]], *args: Any, **kwargs: Any) -> None: ...
