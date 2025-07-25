"""Composite extension, allowing windows to be rendered to off-screen
storage.

For detailed description, see the protocol specification at
http://freedesktop.org/wiki/Software/CompositeExt

By itself this extension is not very useful, it is intended to be used
together with the DAMAGE and XFIXES extensions.  Typically you would
also need RENDER or glX or some similar method of creating fancy
graphics.
"""

from _typeshed import Unused
from collections.abc import Callable
from typing import Any, Final
from typing_extensions import TypeAlias

from Xlib._typing import ErrorHandler
from Xlib.display import Display
from Xlib.protocol import rq
from Xlib.xobject import drawable, resource

_Update: TypeAlias = Callable[[rq.DictWrapper | dict[str, Any]], object]

extname: Final = "Composite"
RedirectAutomatic: Final = 0
RedirectManual: Final = 1

class QueryVersion(rq.ReplyRequest): ...

def query_version(self: Display | resource.Resource) -> QueryVersion: ...

class RedirectWindow(rq.Request): ...

def redirect_window(self: drawable.Window, update: _Update, onerror: ErrorHandler[object] | None = None) -> None:
    """Redirect the hierarchy starting at this window to off-screen
    storage.
    """

class RedirectSubwindows(rq.Request): ...

def redirect_subwindows(self: drawable.Window, update: _Update, onerror: ErrorHandler[object] | None = None) -> None:
    """Redirect the hierarchies starting at all current and future
    children to this window to off-screen storage.
    """

class UnredirectWindow(rq.Request): ...

def unredirect_window(self: drawable.Window, update: _Update, onerror: ErrorHandler[object] | None = None) -> None:
    """Stop redirecting this window hierarchy."""

class UnredirectSubindows(rq.Request): ...

def unredirect_subwindows(self: drawable.Window, update: _Update, onerror: ErrorHandler[object] | None = None) -> None:
    """Stop redirecting the hierarchies of children to this window."""

class CreateRegionFromBorderClip(rq.Request): ...

def create_region_from_border_clip(self: drawable.Window, onerror: ErrorHandler[object] | None = None) -> int:
    """Create a region of the border clip of the window, i.e. the area
    that is not clipped by the parent and any sibling windows.
    """

class NameWindowPixmap(rq.Request): ...

def name_window_pixmap(self: Display | resource.Resource, onerror: ErrorHandler[object] | None = None) -> drawable.Pixmap:
    """Create a new pixmap that refers to the off-screen storage of
    the window, including its border.

    This pixmap will remain allocated until freed whatever happens
    with the window.  However, the window will get a new off-screen
    pixmap every time it is mapped or resized, so to keep track of the
    contents you must listen for these events and get a new pixmap
    after them.
    """

class GetOverlayWindow(rq.ReplyRequest): ...

def get_overlay_window(self: Display) -> GetOverlayWindow:
    """Return the overlay window of the root window."""

def init(disp: Display, info: Unused) -> None: ...
