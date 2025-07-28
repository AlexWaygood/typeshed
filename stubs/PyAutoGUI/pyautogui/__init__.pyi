import contextlib
from _typeshed import ConvertibleToInt
from collections.abc import Callable, Iterable, Sequence
from datetime import datetime
from typing import Final, NamedTuple, SupportsIndex, SupportsInt, TypeVar
from typing_extensions import ParamSpec, TypeAlias

from pyscreeze import (
    center as center,
    locate as locate,
    locateAll as locateAll,
    locateAllOnScreen as locateAllOnScreen,
    locateCenterOnScreen as locateCenterOnScreen,
    locateOnScreen as locateOnScreen,
    locateOnWindow as locateOnWindow,
    pixel as pixel,
    pixelMatchesColor as pixelMatchesColor,
    screenshot as screenshot,
)

_P = ParamSpec("_P")
_R = TypeVar("_R")
# Explicitly mentioning str despite being in the ConvertibleToInt Alias because it has a different meaning (filename on screen)
# Specifying non-None Y arg when X is a string or sequence raises an error
# TODO: This could be better represented through overloads
_NormalizeableXArg: TypeAlias = str | ConvertibleToInt | Sequence[ConvertibleToInt]

# Constants
KEY_NAMES: list[str]
KEYBOARD_KEYS: list[str]
LEFT: Final = "left"
MIDDLE: Final = "middle"
RIGHT: Final = "right"
PRIMARY: Final = "primary"
SECONDARY: Final = "secondary"
G_LOG_SCREENSHOTS_FILENAMES: list[str]
# Implementation details
QWERTY: Final[str]
QWERTZ: Final[str]
MINIMUM_SLEEP: Final[float]

# These are meant to be overridable
LOG_SCREENSHOTS: bool
LOG_SCREENSHOTS_LIMIT: int | None
# https://pyautogui.readthedocs.io/en/latest/index.html#fail-safes
FAILSAFE: bool
PAUSE: float
DARWIN_CATCH_UP_TIME: float
FAILSAFE_POINTS: list[tuple[int, int]]
# https://pyautogui.readthedocs.io/en/latest/mouse.htmln#mouse-movement
MINIMUM_DURATION: float

class PyAutoGUIException(Exception):
    """
    PyAutoGUI code will raise this exception class for any invalid actions. If PyAutoGUI raises some other exception,
    you should assume that this is caused by a bug in PyAutoGUI itself. (Including a failure to catch potential
    exceptions raised by PyAutoGUI.)
    """

class FailSafeException(PyAutoGUIException):
    """
    This exception is raised by PyAutoGUI functions when the user puts the mouse cursor into one of the "failsafe
    points" (by default, one of the four corners of the primary monitor). This exception shouldn't be caught; it's
    meant to provide a way to terminate a misbehaving script.
    """

class ImageNotFoundException(PyAutoGUIException):
    """
    This exception is the PyAutoGUI version of PyScreeze's `ImageNotFoundException`, which is raised when a locate*()
    function call is unable to find an image.

    Ideally, `pyscreeze.ImageNotFoundException` should never be raised by PyAutoGUI.
    """

def raisePyAutoGUIImageNotFoundException(wrappedFunction: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    A decorator that wraps PyScreeze locate*() functions so that the PyAutoGUI user sees them raise PyAutoGUI's
    ImageNotFoundException rather than PyScreeze's ImageNotFoundException. This is because PyScreeze should be
    invisible to PyAutoGUI users.
    """

def mouseInfo() -> None:
    """
    Launches the MouseInfo app. This application provides mouse coordinate information which can be useful when
    planning GUI automation tasks. This function blocks until the application is closed.
    """

def useImageNotFoundException(value: bool | None = None) -> None:
    """
    When called with no arguments, PyAutoGUI will raise ImageNotFoundException when the PyScreeze locate*() functions
    can't find the image it was told to locate. The default behavior is to return None. Call this function with no
    arguments (or with True as the argument) to have exceptions raised, which is a better practice.

    You can also disable raising exceptions by passing False for the argument.
    """

def isShiftCharacter(character: str) -> bool:
    """
    Returns True if the ``character`` is a keyboard key that would require the shift key to be held down, such as
    uppercase letters or the symbols on the keyboard's number row.
    """

class Point(NamedTuple):
    """Point(x, y)"""

    x: int
    y: int

class Size(NamedTuple):
    """Size(width, height)"""

    width: int
    height: int

def getPointOnLine(x1: float, y1: float, x2: float, y2: float, n: float) -> tuple[float, float]:
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """

def linear(n: float) -> float:
    """
    Returns ``n``, where ``n`` is the float argument between ``0.0`` and ``1.0``. This function is for the default
    linear tween for mouse moving functions.

    This function was copied from PyTweening module, so that it can be called even if PyTweening is not installed.
    """

def position(x: int | None = None, y: int | None = None) -> Point:
    """
    Returns the current xy coordinates of the mouse cursor as a two-integer tuple.

    Args:
      x (int, None, optional) - If not None, this argument overrides the x in
        the return value.
      y (int, None, optional) - If not None, this argument overrides the y in
        the return value.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.

    NOTE: The position() function doesn't check for failsafe.
    """

def size() -> Size:
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """

resolution = size

def onScreen(x: _NormalizeableXArg | None, y: SupportsInt | None = None) -> bool:
    """Returns whether the given xy coordinates are on the primary screen or not.

    Note that this function doesn't work for secondary screens.

    Args:
      Either the arguments are two separate values, first arg for x and second
        for y, or there is a single argument of a sequence with two values, the
        first x and the second y.
        Example: onScreen(x, y) or onScreen([x, y])

    Returns:
      bool: True if the xy coordinates are on the screen at its current
        resolution, otherwise False.
    """

def mouseDown(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "primary",
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs pressing a mouse button down (but not up).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        mouse down happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        mouse down happens. None by default.
      button (str, int, optional): The mouse button pressed down. TODO

    Returns:
      None

    Raises:
      PyAutoGUIException: If button is not one of 'left', 'middle', 'right', 1, 2, or 3
    """

def mouseUp(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "primary",
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs releasing a mouse button up (but not down beforehand).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        mouse up happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        mouse up happens. None by default.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      PyAutoGUIException: If button is not one of 'left', 'middle', 'right', 1, 2, or 3
    """

def click(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    clicks: SupportsIndex = 1,
    interval: float = 0.0,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "primary",
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """
    Performs pressing a mouse button down and then immediately releasing it. Returns ``None``.

    When no arguments are passed, the primary mouse button is clicked at the mouse cursor's current location.

    If integers for ``x`` and ``y`` are passed, the click will happen at that XY coordinate. If ``x`` is a string, the
    string is an image filename that PyAutoGUI will attempt to locate on the screen and click the center of. If ``x``
    is a sequence of two coordinates, those coordinates will be used for the XY coordinate to click on.

    The ``clicks`` argument is an int of how many clicks to make, and defaults to ``1``.

    The ``interval`` argument is an int or float of how many seconds to wait in between each click, if ``clicks`` is
    greater than ``1``. It defaults to ``0.0`` for no pause in between clicks.

    The ``button`` argument is one of the constants ``LEFT``, ``MIDDLE``, ``RIGHT``, ``PRIMARY``, or ``SECONDARY``.
    It defaults to ``PRIMARY`` (which is the left mouse button, unless the operating system has been set for
    left-handed users.)

    If ``x`` and ``y`` are specified, and the click is not happening at the mouse cursor's current location, then
    the ``duration`` argument is an int or float of how many seconds it should take to move the mouse to the XY
    coordinates. It defaults to ``0`` for an instant move.

    If ``x`` and ``y`` are specified and ``duration`` is not ``0``, the ``tween`` argument is a tweening function
    that specifies the movement pattern of the mouse cursor as it moves to the XY coordinates. The default is a
    simple linear tween. See the PyTweening module documentation for more details.

    The ``pause`` parameter is deprecated. Call the ``pyautogui.sleep()`` function to implement a pause.

    Raises:
      PyAutoGUIException: If button is not one of 'left', 'middle', 'right', 1, 2, 3
    """

def leftClick(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    interval: float = 0.0,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a left mouse button click.

    This is a wrapper function for click('left', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.

    Returns:
      None
    """

def rightClick(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    interval: float = 0.0,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a right mouse button click.

    This is a wrapper function for click('right', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.

    Returns:
      None
    """

def middleClick(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    interval: float = 0.0,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a middle mouse button click.

    This is a wrapper function for click('middle', x, y).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """

def doubleClick(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    interval: float = 0.0,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "left",
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a double click.

    This is a wrapper function for click('left', x, y, 2, interval).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      PyAutoGUIException: If button is not one of 'left', 'middle', 'right', 1, 2, 3, 4,
        5, 6, or 7
    """

def tripleClick(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    interval: float = 0.0,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "left",
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a triple click.

    This is a wrapper function for click('left', x, y, 3, interval).

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      interval (float, optional): The number of seconds in between each click,
        if the number of clicks is greater than 1. 0.0 by default, for no
        pause in between clicks.
      button (str, int, optional): The mouse button released. TODO

    Returns:
      None

    Raises:
      PyAutoGUIException: If button is not one of 'left', 'middle', 'right', 1, 2, 3, 4,
        5, 6, or 7
    """

def scroll(
    clicks: float,
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a scroll of the mouse scroll wheel.

    Whether this is a vertical or horizontal scroll depends on the underlying
    operating system.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """

def hscroll(
    clicks: float,
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs an explicitly horizontal scroll of the mouse scroll wheel,
    if this is supported by the operating system. (Currently just Linux.)

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """

def vscroll(
    clicks: float,
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs an explicitly vertical scroll of the mouse scroll wheel,
    if this is supported by the operating system. (Currently just Linux.)

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      clicks (int, float): The amount of scrolling to perform.
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.

    Returns:
      None
    """

def moveTo(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool = False,
    _pause: bool = True,
) -> None:
    """Moves the mouse cursor to a point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): The x position on the screen where the
        click happens. None by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): The y position on the screen where the
        click happens. None by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.

    Returns:
      None
    """

def moveRel(
    xOffset: _NormalizeableXArg | None = None,
    yOffset: SupportsInt | None = None,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    logScreenshot: bool = False,
    _pause: bool = True,
) -> None:
    """Moves the mouse cursor to a point on the screen, relative to its current
    position.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for x and y.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.

    Returns:
      None
    """

move = moveRel

def dragTo(
    x: _NormalizeableXArg | None = None,
    y: SupportsInt | None = None,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "primary",
    logScreenshot: bool | None = None,
    _pause: bool = True,
    mouseDownUp: bool = True,
) -> None:
    """Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for x and y.
        If x is a str, it's considered a filename of an image to find on
        the screen with locateOnScreen() and click the center of.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.
      button (str, int, optional): The mouse button released. TODO
      mouseDownUp (True, False): When true, the mouseUp/Down actions are not performed.
        Which allows dragging over multiple (small) actions. 'True' by default.

    Returns:
      None
    """

def dragRel(
    xOffset: _NormalizeableXArg | None = 0,
    yOffset: SupportsInt | None = 0,
    duration: float = 0.0,
    tween: Callable[[float], float] = ...,
    # Docstring says `button` can also be `int`, but `.lower()` is called unconditionally in `_normalizeButton()`
    button: str = "primary",
    logScreenshot: bool | None = None,
    _pause: bool = True,
    mouseDownUp: bool = True,
) -> None:
    """Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen, relative to its current position.

    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.

    Args:
      x (int, float, None, tuple, optional): How far left (for negative values) or
        right (for positive values) to move the cursor. 0 by default. If tuple, this is used for xOffset and yOffset.
      y (int, float, None, optional): How far up (for negative values) or
        down (for positive values) to move the cursor. 0 by default.
      duration (float, optional): The amount of time it takes to move the mouse
        cursor to the new xy coordinates. If 0, then the mouse cursor is moved
        instantaneously. 0.0 by default.
      tween (func, optional): The tweening function used if the duration is not
        0. A linear tween is used by default.
      button (str, int, optional): The mouse button released. TODO
      mouseDownUp (True, False): When true, the mouseUp/Down actions are not performed.
        Which allows dragging over multiple (small) actions. 'True' by default.

    Returns:
      None
    """

drag = dragRel

def isValidKey(key: str) -> bool:
    """Returns a Boolean value if the given key is a valid value to pass to
    PyAutoGUI's keyboard-related functions for the current platform.

    This function is here because passing an invalid value to the PyAutoGUI
    keyboard functions currently is a no-op that does not raise an exception.

    Some keys are only valid on some platforms. For example, while 'esc' is
    valid for the Escape key on all platforms, 'browserback' is only used on
    Windows operating systems.

    Args:
      key (str): The key value.

    Returns:
      bool: True if key is a valid value, False if not.
    """

def keyDown(key: str, logScreenshot: bool | None = None, _pause: bool = True) -> None:
    """Performs a keyboard key press without the release. This will put that
    key in a held down state.

    NOTE: For some reason, this does not seem to cause key repeats like would
    happen if a keyboard key was held down on a text field.

    Args:
      key (str): The key to be pressed down. The valid names are listed in
      KEYBOARD_KEYS.

    Returns:
      None
    """

def keyUp(key: str, logScreenshot: bool | None = None, _pause: bool = True) -> None:
    """Performs a keyboard key release (without the press down beforehand).

    Args:
      key (str): The key to be released up. The valid names are listed in
      KEYBOARD_KEYS.

    Returns:
      None
    """

def press(
    keys: str | Iterable[str],
    presses: SupportsIndex = 1,
    interval: float = 0.0,
    logScreenshot: bool | None = None,
    _pause: bool = True,
) -> None:
    """Performs a keyboard key press down, followed by a release.

    Args:
      key (str, list): The key to be pressed. The valid names are listed in
      KEYBOARD_KEYS. Can also be a list of such strings.
      presses (integer, optional): The number of press repetitions.
      1 by default, for just one press.
      interval (float, optional): How many seconds between each press.
      0.0 by default, for no pause between presses.
      pause (float, optional): How many seconds in the end of function process.
      None by default, for no pause in the end of function process.
    Returns:
      None
    """

def hold(
    keys: str | Iterable[str], logScreenshot: bool | None = None, _pause: bool = True
) -> contextlib._GeneratorContextManager[None]:
    """Context manager that performs a keyboard key press down upon entry,
    followed by a release upon exit.

    Args:
      key (str, list): The key to be pressed. The valid names are listed in
      KEYBOARD_KEYS. Can also be a list of such strings.
      pause (float, optional): How many seconds in the end of function process.
      None by default, for no pause in the end of function process.
    Returns:
      None
    """

def typewrite(
    message: str | Sequence[str], interval: float = 0.0, logScreenshot: bool | None = None, _pause: bool = True
) -> None:
    """Performs a keyboard key press down, followed by a release, for each of
    the characters in message.

    The message argument can also be list of strings, in which case any valid
    keyboard name can be used.

    Since this performs a sequence of keyboard presses and does not hold down
    keys, it cannot be used to perform keyboard shortcuts. Use the hotkey()
    function for that.

    Args:
      message (str, list): If a string, then the characters to be pressed. If a
        list, then the key names of the keys to press in order. The valid names
        are listed in KEYBOARD_KEYS.
      interval (float, optional): The number of seconds in between each press.
        0.0 by default, for no pause in between presses.

    Returns:
      None
    """

write = typewrite

def hotkey(*args: str, logScreenshot: bool | None = None, interval: float = 0.0) -> None:
    """Performs key down presses on the arguments passed in order, then performs
    key releases in reverse order.

    The effect is that calling hotkey('ctrl', 'shift', 'c') would perform a
    "Ctrl-Shift-C" hotkey/keyboard shortcut press.

    Args:
      key(s) (str): The series of keys to press, in order. This can also be a
        list of key strings to press.
      interval (float, optional): The number of seconds in between each press.
        0.0 by default, for no pause in between presses.

    Returns:
      None
    """

shortcut = hotkey

def failSafeCheck() -> None: ...
def displayMousePosition(xOffset: float = 0, yOffset: float = 0) -> None:
    """This function is meant to be run from the command line. It will
    automatically display the location and RGB of the mouse cursor.
    """

def sleep(seconds: float) -> None: ...
def countdown(seconds: SupportsIndex) -> None: ...
def run(commandStr: str, _ssCount: Sequence[int] | None = None) -> None:
    """Run a series of PyAutoGUI function calls according to a mini-language
    made for this function. The `commandStr` is composed of character
    commands that represent PyAutoGUI function calls.

    For example, `run('ccg-20,+0c')` clicks the mouse twice, then makes
    the mouse cursor go 20 pixels to the left, then click again.

    Whitespace between commands and arguments is ignored. Command characters
    must be lowercase. Quotes must be single quotes.

    For example, the previous call could also be written as `run('c c g -20, +0 c')`.

    The character commands and their equivalents are here:

    `c` => `click(button=PRIMARY)`
    `l` => `click(button=LEFT)`
    `m` => `click(button=MIDDLE)`
    `r` => `click(button=RIGHT)`
    `su` => `scroll(1) # scroll up`
    `sd` => `scroll(-1) # scroll down`
    `ss` => `screenshot('screenshot1.png') # filename number increases on its own`

    `gX,Y` => `moveTo(X, Y)`
    `g+X,-Y` => `move(X, Y) # The + or - prefix is the difference between move() and moveTo()`
    `dX,Y` => `dragTo(X, Y)`
    `d+X,-Y` => `drag(X, Y) # The + or - prefix is the difference between drag() and dragTo()`

    `k'key'` => `press('key')`
    `w'text'` => `write('text')`
    `h'key,key,key'` => `hotkey(*'key,key,key'.replace(' ', '').split(','))`
    `a'hello'` => `alert('hello')`

    `sN` => `sleep(N) # N can be an int or float`
    `pN` => `PAUSE = N # N can be an int or float`

    `fN(commands)` => for i in range(N): run(commands)

    Note that any changes to `PAUSE` with the `p` command will be undone when
    this function returns. The original `PAUSE` setting will be reset.

    TODO - This function is under development.
    """

def printInfo(dontPrint: bool = False) -> str: ...
def getInfo() -> tuple[str, str, str, str, Size, datetime]: ...
