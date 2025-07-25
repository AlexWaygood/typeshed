"""
This module contains the base implementation.

The actual interface to keyboard classes is defined here, but the
implementation is located in a platform dependent module.
"""

import contextlib
import enum
import sys
from collections.abc import Callable, Generator, Iterable, Iterator
from typing import Any, ClassVar, cast
from typing_extensions import Self

from pynput._util import AbstractListener

class KeyCode:
    """
    A :class:`KeyCode` represents the description of a key code used by the
    operating system.
    """

    _PLATFORM_EXTENSIONS: ClassVar[Iterable[str]]  # undocumented
    vk: int | None
    char: str | None
    is_dead: bool | None
    combining: str | None
    def __init__(self, vk: str | None = None, char: str | None = None, is_dead: bool = False, **kwargs: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def join(self, key: Self) -> Self:
        """Applies this dead key to another key and returns the result.

        Joining a dead key with space (``' '``) or itself yields the non-dead
        version of this key, if one exists; for example,
        ``KeyCode.from_dead('~').join(KeyCode.from_char(' '))`` equals
        ``KeyCode.from_char('~')`` and
        ``KeyCode.from_dead('~').join(KeyCode.from_dead('~'))``.

        :param KeyCode key: The key to join with this key.

        :return: a key code

        :raises ValueError: if the keys cannot be joined
        """

    @classmethod
    def from_vk(cls, vk: int, **kwargs: Any) -> Self:
        """Creates a key from a virtual key code.

        :param vk: The virtual key code.

        :param kwargs: Any other parameters to pass.

        :return: a key code
        """

    @classmethod
    def from_char(cls, char: str, **kwargs: Any) -> Self:
        """Creates a key from a character.

        :param str char: The character.

        :return: a key code
        """

    @classmethod
    def from_dead(cls, char: str, **kwargs: Any) -> Self:
        """Creates a dead key.

        :param char: The dead key. This should be the unicode character
            representing the stand alone character, such as ``'~'`` for
            *COMBINING TILDE*.

        :return: a key code
        """

class Key(enum.Enum):
    """A class representing various buttons that may not correspond to
    letters. This includes modifier keys and function keys.

    The actual values for these items differ between platforms. Some platforms
    may have additional buttons, but these are guaranteed to be present
    everywhere.
    """

    alt = cast(KeyCode, ...)
    alt_l = cast(KeyCode, ...)
    alt_r = cast(KeyCode, ...)
    alt_gr = cast(KeyCode, ...)
    backspace = cast(KeyCode, ...)
    caps_lock = cast(KeyCode, ...)
    cmd = cast(KeyCode, ...)
    cmd_l = cast(KeyCode, ...)
    cmd_r = cast(KeyCode, ...)
    ctrl = cast(KeyCode, ...)
    ctrl_l = cast(KeyCode, ...)
    ctrl_r = cast(KeyCode, ...)
    delete = cast(KeyCode, ...)
    down = cast(KeyCode, ...)
    end = cast(KeyCode, ...)
    enter = cast(KeyCode, ...)
    esc = cast(KeyCode, ...)
    f1 = cast(KeyCode, ...)
    f2 = cast(KeyCode, ...)
    f3 = cast(KeyCode, ...)
    f4 = cast(KeyCode, ...)
    f5 = cast(KeyCode, ...)
    f6 = cast(KeyCode, ...)
    f7 = cast(KeyCode, ...)
    f8 = cast(KeyCode, ...)
    f9 = cast(KeyCode, ...)
    f10 = cast(KeyCode, ...)
    f11 = cast(KeyCode, ...)
    f12 = cast(KeyCode, ...)
    f13 = cast(KeyCode, ...)
    f14 = cast(KeyCode, ...)
    f15 = cast(KeyCode, ...)
    f16 = cast(KeyCode, ...)
    f17 = cast(KeyCode, ...)
    f18 = cast(KeyCode, ...)
    f19 = cast(KeyCode, ...)
    f20 = cast(KeyCode, ...)
    if sys.platform == "win32":
        f21 = cast(KeyCode, ...)
        f22 = cast(KeyCode, ...)
        f23 = cast(KeyCode, ...)
        f24 = cast(KeyCode, ...)
    home = cast(KeyCode, ...)
    left = cast(KeyCode, ...)
    page_down = cast(KeyCode, ...)
    page_up = cast(KeyCode, ...)
    right = cast(KeyCode, ...)
    shift = cast(KeyCode, ...)
    shift_l = cast(KeyCode, ...)
    shift_r = cast(KeyCode, ...)
    space = cast(KeyCode, ...)
    tab = cast(KeyCode, ...)
    up = cast(KeyCode, ...)
    media_play_pause = cast(KeyCode, ...)
    media_stop = cast(KeyCode, ...)
    media_volume_mute = cast(KeyCode, ...)
    media_volume_down = cast(KeyCode, ...)
    media_volume_up = cast(KeyCode, ...)
    media_previous = cast(KeyCode, ...)
    media_next = cast(KeyCode, ...)
    if sys.platform == "darwin":
        media_eject = cast(KeyCode, ...)
    insert = cast(KeyCode, ...)
    menu = cast(KeyCode, ...)
    num_lock = cast(KeyCode, ...)
    pause = cast(KeyCode, ...)
    print_screen = cast(KeyCode, ...)
    scroll_lock = cast(KeyCode, ...)

class Controller:
    """A controller for sending virtual keyboard events to the system."""

    _KeyCode: ClassVar[type[KeyCode]]  # undocumented
    _Key: ClassVar[type[Key]]  # undocumented

    if sys.platform == "linux":
        CTRL_MASK: ClassVar[int]
        SHIFT_MASK: ClassVar[int]

    class InvalidKeyException(Exception):
        """The exception raised when an invalid ``key`` parameter is passed to
        either :meth:`Controller.press` or :meth:`Controller.release`.

        Its first argument is the ``key`` parameter.
        """

    class InvalidCharacterException(Exception):
        """The exception raised when an invalid character is encountered in
        the string passed to :meth:`Controller.type`.

        Its first argument is the index of the character in the string, and the
        second the character.
        """

    def __init__(self) -> None: ...
    def press(self, key: str | Key | KeyCode) -> None:
        """Presses a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to press.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """

    def release(self, key: str | Key | KeyCode) -> None:
        """Releases a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to release. If this is a string, it is passed to
            :meth:`touches` and the returned releases are used.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """

    def tap(self, key: str | Key | KeyCode) -> None:
        """Presses and releases a key.

        This is equivalent to the following code::

            controller.press(key)
            controller.release(key)

        :param key: The key to press.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """

    def touch(self, key: str | Key | KeyCode, is_press: bool) -> None:
        """Calls either :meth:`press` or :meth:`release` depending on the value
        of ``is_press``.

        :param key: The key to press or release.

        :param bool is_press: Whether to press the key.

        :raises InvalidKeyException: if the key is invalid
        """

    @contextlib.contextmanager
    def pressed(self, *args: str | Key | KeyCode) -> Generator[None]:
        """Executes a block with some keys pressed.

        :param keys: The keys to keep pressed.
        """

    def type(self, string: str) -> None:
        """Types a string.

        This method will send all key presses and releases necessary to type
        all characters in the string.

        :param str string: The string to type.

        :raises InvalidCharacterException: if an untypable character is
            encountered
        """

    @property
    def modifiers(self) -> contextlib.AbstractContextManager[Iterator[set[Key]]]:
        """The currently pressed modifier keys.

        Please note that this reflects only the internal state of this
        controller, and not the state of the operating system keyboard buffer.
        This property cannot be used to determine whether a key is physically
        pressed.

        Only the generic modifiers will be set; when pressing either
        :attr:`Key.shift_l`, :attr:`Key.shift_r` or :attr:`Key.shift`, only
        :attr:`Key.shift` will be present.

        Use this property within a context block thus::

            with controller.modifiers as modifiers:
                with_block()

        This ensures that the modifiers cannot be modified by another thread.
        """

    @property
    def alt_pressed(self) -> bool:
        """Whether any *alt* key is pressed.

        Please note that this reflects only the internal state of this
        controller. See :attr:`modifiers` for more information.
        """

    @property
    def alt_gr_pressed(self) -> bool:
        """Whether *altgr* is pressed.

        Please note that this reflects only the internal state of this
        controller. See :attr:`modifiers` for more information.
        """

    @property
    def ctrl_pressed(self) -> bool:
        """Whether any *ctrl* key is pressed.

        Please note that this reflects only the internal state of this
        controller. See :attr:`modifiers` for more information.
        """

    @property
    def shift_pressed(self) -> bool:
        """Whether any *shift* key is pressed, or *caps lock* is toggled.

        Please note that this reflects only the internal state of this
        controller. See :attr:`modifiers` for more information.
        """

class Listener(AbstractListener):
    """A listener for keyboard events.

    Instances of this class can be used as context managers. This is equivalent
    to the following code::

        listener.start()
        try:
            listener.wait()
            with_statements()
        finally:
            listener.stop()

    This class inherits from :class:`threading.Thread` and supports all its
    methods. It will set :attr:`daemon` to ``True`` when created.

    All callback arguments are optional; a callback may take less arguments
    than actually passed, but not more, unless they are optional.

    :param callable on_press: The callback to call when a button is pressed.

        It will be called with the arguments ``(key, injected)``, where ``key``
        is a :class:`KeyCode`, a :class:`Key` or ``None`` if the key is
        unknown, and ``injected`` whether the event was injected and thus not
        generated by an actual input device.

        Please note that not all backends support ``injected`` and will always
        set it to ``False``.

    :param callable on_release: The callback to call when a button is released.

        It will be called with the arguments ``(key, injected)``, where ``key``
        is a :class:`KeyCode`, a :class:`Key` or ``None`` if the key is
        unknown, and ``injected`` whether the event was injected and thus not
        generated by an actual input device.

        Please note that not all backends support ``injected`` and will always
        set it to ``False``.

    :param bool suppress: Whether to suppress events. Setting this to ``True``
        will prevent the input events from being passed to the rest of the
        system.

    :param kwargs: Any non-standard platform dependent options. These should be
        prefixed with the platform name thus: ``darwin_``, ``uinput_``,
        ``xorg_`` or ``win32_``.

        Supported values are:

        ``darwin_intercept``
            A callable taking the arguments ``(event_type, event)``, where
            ``event_type`` is ``Quartz.kCGEventKeyDown`` or
            ``Quartz.kCGEventKeyUp``, and ``event`` is a ``CGEventRef``.

            This callable can freely modify the event using functions like
            ``Quartz.CGEventSetIntegerValueField``. If this callable does not
            return the event, the event is suppressed system wide.

        ``uinput_device_paths``
            A list of device paths.

            If this is specified, *pynput* will limit the number of devices
            checked for the capabilities needed to those passed, otherwise all
            system devices will be used. Passing this might be required if an
            incorrect device is chosen.

        ``win32_event_filter``
            A callable taking the arguments ``(msg, data)``, where ``msg`` is
            the current message, and ``data`` associated data as a
            `KBDLLHOOKSTRUCT <https://docs.microsoft.com/en-gb/windows/win32/api/winuser/ns-winuser-kbdllhookstruct>`_.

            If this callback returns ``False``, the event will not be
            propagated to the listener callback.

            If ``self.suppress_event()`` is called, the event is suppressed
            system wide.
    """

    def __init__(
        self,
        on_press: Callable[[Key | KeyCode | None], None] | None = None,
        on_release: Callable[[Key | KeyCode | None], None] | None = None,
        suppress: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def canonical(self, key: Key | KeyCode) -> Key | KeyCode:
        """Performs normalisation of a key.

        This method attempts to convert key events to their canonical form, so
        that events will equal regardless of modifier state.

        This method will convert upper case keys to lower case keys, convert
        any modifiers with a right and left version to the same value, and may
        slow perform additional platform dependent normalisation.

        :param key: The key to normalise.
        :type key: Key or KeyCode

        :return: a key
        :rtype: Key or KeyCode
        """
