from collections.abc import Callable, Iterable, Sequence
from re import Pattern
from types import FunctionType, MethodType
from typing import Any, Literal, TypedDict, overload
from typing_extensions import TypeAlias

from Xlib import error
from Xlib._typing import ErrorHandler
from Xlib.protocol import display, request, rq
from Xlib.xobject import colormap, cursor, drawable, fontable, resource

_ResourceBaseClass: TypeAlias = (
    resource.Resource
    | drawable.Drawable
    | drawable.Window
    | drawable.Pixmap
    | fontable.Fontable
    | fontable.Font
    | fontable.GC
    | colormap.Colormap
    | cursor.Cursor
)

# Is the type of the `_resource_baseclasses` variable, defined in this file at runtime
class _ResourceBaseClassesType(TypedDict):  # noqa: Y049
    resource: type[resource.Resource]
    drawable: type[drawable.Drawable]
    window: type[drawable.Window]
    pixmap: type[drawable.Pixmap]
    fontable: type[fontable.Fontable]
    font: type[fontable.Font]
    gc: type[fontable.GC]
    colormap: type[colormap.Colormap]
    cursor: type[cursor.Cursor]

class _BaseDisplay(display.Display):
    def __init__(self, display: str | None = None) -> None: ...
    def get_atom(self, atomname: str, only_if_exists: bool = False) -> int: ...

class Display:
    display: _BaseDisplay
    keysym_translations: dict[int, str]
    extensions: list[str]
    class_extension_dicts: dict[str, dict[str, FunctionType]]
    display_extension_methods: dict[str, Callable[..., Any]]
    extension_event: rq.DictWrapper
    def __init__(self, display: str | None = None) -> None: ...
    def get_display_name(self) -> str:
        """Returns the name used to connect to the server, either
        provided when creating the Display object, or fetched from the
        environmental variable $DISPLAY.
        """

    def fileno(self) -> int:
        """Returns the file descriptor number of the underlying socket.
        This method is provided to allow Display objects to be passed
        select.select().
        """

    def close(self) -> None:
        """Close the display, freeing the resources that it holds."""

    def set_error_handler(self, handler: ErrorHandler[object] | None) -> None:
        """Set the default error handler which will be called for all
        unhandled errors. handler should take two arguments as a normal
        request error handler, but the second argument (the request) will
        be None.  See section Error Handling.
        """

    def flush(self) -> None:
        """Flush the request queue, building and sending the queued
        requests. This can be necessary in applications that never wait
        for events, and in threaded applications.
        """

    def sync(self) -> None:
        """Flush the queue and wait until the server has processed all
        the queued requests. Use this e.g. when it is important that
        errors caused by a certain request is trapped.
        """

    def next_event(self) -> rq.Event:
        """Return the next event. If there are no events queued, it will
        block until the next event is fetched from the server.
        """

    def pending_events(self) -> int:
        """Return the number of events queued, i.e. the number of times
        that Display.next_event() can be called without blocking.
        """

    def has_extension(self, extension: str) -> bool:
        """Check if both the server and the client library support the X
        extension named extension.
        """

    @overload
    def create_resource_object(self, type: Literal["resource"], id: int) -> resource.Resource:
        """Create a resource object of type for the integer id. type
        should be one of the following strings:

        resource
        drawable
        window
        pixmap
        fontable
        font
        gc
        colormap
        cursor

        This function can be used when a resource ID has been fetched
        e.g. from an resource or a command line argument. Resource
        objects should never be created by instantiating the appropriate
        class directly, since any X extensions dynamically added by the
        library will not be available.
        """

    @overload
    def create_resource_object(self, type: Literal["drawable"], id: int) -> drawable.Drawable: ...
    @overload
    def create_resource_object(self, type: Literal["window"], id: int) -> drawable.Window: ...
    @overload
    def create_resource_object(self, type: Literal["pixmap"], id: int) -> drawable.Pixmap: ...
    @overload
    def create_resource_object(self, type: Literal["fontable"], id: int) -> fontable.Fontable: ...
    @overload
    def create_resource_object(self, type: Literal["font"], id: int) -> fontable.Font: ...
    @overload
    def create_resource_object(self, type: Literal["gc"], id: int) -> fontable.GC: ...
    @overload
    def create_resource_object(self, type: Literal["colormap"], id: int) -> colormap.Colormap: ...
    @overload
    def create_resource_object(self, type: Literal["cursor"], id: int) -> cursor.Cursor: ...
    @overload
    def create_resource_object(self, type: str, id: int) -> resource.Resource: ...
    def __getattr__(self, attr: str) -> MethodType: ...
    def screen(self, sno: int | None = None) -> rq.Struct: ...
    def screen_count(self) -> int:
        """Return the total number of screens on the display."""

    def get_default_screen(self) -> int:
        """Return the number of the default screen, extracted from the
        display name.
        """

    def extension_add_method(self, object: str, name: str, function: Callable[..., Any]) -> None:
        """extension_add_method(object, name, function)

        Add an X extension module method.  OBJECT is the type of
        object to add the function to, a string from this list:

            display
            resource
            drawable
            window
            pixmap
            fontable
            font
            gc
            colormap
            cursor

        NAME is the name of the method, a string.  FUNCTION is a
        normal function whose first argument is a 'self'.
        """

    def extension_add_event(self, code: int, evt: type, name: str | None = None) -> None:
        """extension_add_event(code, evt, [name])

        Add an extension event.  CODE is the numeric code, and EVT is
        the event class.  EVT will be cloned, and the attribute _code
        of the new event class will be set to CODE.

        If NAME is omitted, it will be set to the name of EVT.  This
        name is used to insert an entry in the DictWrapper
        extension_event.
        """

    def extension_add_subevent(self, code: int, subcode: int | None, evt: type[rq.Event], name: str | None = None) -> None:
        """extension_add_subevent(code, evt, [name])

        Add an extension subevent.  CODE is the numeric code, subcode
        is the sub-ID of this event that shares the code ID with other
        sub-events and EVT is the event class.  EVT will be cloned, and
        the attribute _code of the new event class will be set to CODE.

        If NAME is omitted, it will be set to the name of EVT.  This
        name is used to insert an entry in the DictWrapper
        extension_event.
        """

    def extension_add_error(self, code: int, err: type[error.XError]) -> None:
        """extension_add_error(code, err)

        Add an extension error.  CODE is the numeric code, and ERR is
        the error class.
        """

    def keycode_to_keysym(self, keycode: int, index: int) -> int:
        """Convert a keycode to a keysym, looking in entry index.
        Normally index 0 is unshifted, 1 is shifted, 2 is alt grid, and 3
        is shift+alt grid. If that key entry is not bound, X.NoSymbol is
        returned.
        """

    def keysym_to_keycode(self, keysym: int) -> int:
        """Look up the primary keycode that is bound to keysym. If
        several keycodes are found, the one with the lowest index and
        lowest code is returned. If keysym is not bound to any key, 0 is
        returned.
        """

    def keysym_to_keycodes(self, keysym: int) -> Iterable[tuple[int, int]]:
        """Look up all the keycodes that is bound to keysym. A list of
        tuples (keycode, index) is returned, sorted primarily on the
        lowest index and secondarily on the lowest keycode.
        """

    def refresh_keyboard_mapping(self, evt: rq.Event) -> None:
        """This method should be called once when a MappingNotify event
        is received, to update the keymap cache. evt should be the event
        object.
        """

    def lookup_string(self, keysym: int) -> str | None:
        """Return a string corresponding to KEYSYM, or None if no
        reasonable translation is found.
        """

    def rebind_string(self, keysym: int, newstring: str | None) -> None:
        """Change the translation of KEYSYM to NEWSTRING.
        If NEWSTRING is None, remove old translation if any.
        """

    def intern_atom(self, name: str, only_if_exists: bool = False) -> int:
        """Intern the string name, returning its atom number. If
        only_if_exists is true and the atom does not already exist, it
        will not be created and X.NONE is returned.
        """

    def get_atom(self, atom: str, only_if_exists: bool = False) -> int:
        """Alias for intern_atom, using internal cache"""

    def get_atom_name(self, atom: int) -> str:
        """Look up the name of atom, returning it as a string. Will raise
        BadAtom if atom does not exist.
        """

    def get_selection_owner(self, selection: int) -> int:
        """Return the window that owns selection (an atom), or X.NONE if
        there is no owner for the selection. Can raise BadAtom.
        """

    def send_event(
        self,
        destination: int,
        event: rq.Event,
        event_mask: int = 0,
        propagate: bool = False,
        onerror: ErrorHandler[object] | None = None,
    ) -> None:
        """Send a synthetic event to the window destination which can be
        a window object, or X.PointerWindow or X.InputFocus. event is the
        event object to send, instantiated from one of the classes in
        protocol.events. See XSendEvent(3X11) for details.

        There is also a Window.send_event() method.
        """

    def ungrab_pointer(self, time: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Release a grabbed pointer and any queued events. See
        XUngrabPointer(3X11).
        """

    def change_active_pointer_grab(
        self, event_mask: int, cursor: cursor.Cursor, time: int, onerror: ErrorHandler[object] | None = None
    ) -> None:
        """Change the dynamic parameters of a pointer grab. See
        XChangeActivePointerGrab(3X11).
        """

    def ungrab_keyboard(self, time: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Ungrab a grabbed keyboard and any queued events. See
        XUngrabKeyboard(3X11).
        """

    def allow_events(self, mode: int, time: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Release some queued events. mode should be one of
        X.AsyncPointer, X.SyncPointer, X.AsyncKeyboard, X.SyncKeyboard,
        X.ReplayPointer, X.ReplayKeyboard, X.AsyncBoth, or X.SyncBoth.
        time should be a timestamp or X.CurrentTime.
        """

    def grab_server(self, onerror: ErrorHandler[object] | None = None) -> None:
        """Disable processing of requests on all other client connections
        until the server is ungrabbed. Server grabbing should be avoided
        as much as possible.
        """

    def ungrab_server(self, onerror: ErrorHandler[object] | None = None) -> None:
        """Release the server if it was previously grabbed by this client."""

    def warp_pointer(
        self,
        x: int,
        y: int,
        src_window: int = 0,
        src_x: int = 0,
        src_y: int = 0,
        src_width: int = 0,
        src_height: int = 0,
        onerror: ErrorHandler[object] | None = None,
    ) -> None:
        """Move the pointer relative its current position by the offsets
        (x, y). However, if src_window is a window the pointer is only
        moved if the specified rectangle in src_window contains it. If
        src_width is 0 it will be replaced with the width of src_window -
        src_x. src_height is treated in a similar way.

        To move the pointer to absolute coordinates, use Window.warp_pointer().
        """

    def set_input_focus(self, focus: int, revert_to: int, time: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Set input focus to focus, which should be a window,
        X.PointerRoot or X.NONE. revert_to specifies where the focus
        reverts to if the focused window becomes not visible, and should
        be X.RevertToParent, RevertToPointerRoot, or RevertToNone. See
        XSetInputFocus(3X11) for details.

        There is also a Window.set_input_focus().
        """

    def get_input_focus(self) -> request.GetInputFocus:
        """Return an object with the following attributes:

        focus
            The window which currently holds the input
            focus, X.NONE or X.PointerRoot.
        revert_to
            Where the focus will revert, one of X.RevertToParent,
            RevertToPointerRoot, or RevertToNone.
        """

    def query_keymap(self) -> bytes:  # TODO: Validate if this is correct
        """Return a bit vector for the logical state of the keyboard,
        where each bit set to 1 indicates that the corresponding key is
        currently pressed down. The vector is represented as a list of 32
        integers. List item N contains the bits for keys 8N to 8N + 7
        with the least significant bit in the byte representing key 8N.
        """

    def open_font(self, name: str) -> _ResourceBaseClass | None:
        """Open the font identifed by the pattern name and return its
        font object. If name does not match any font, None is returned.
        """

    def list_fonts(self, pattern: Pattern[str] | str, max_names: int) -> list[str]:
        """Return a list of font names matching pattern. No more than
        max_names will be returned.
        """

    def list_fonts_with_info(self, pattern: Pattern[str] | str, max_names: int) -> request.ListFontsWithInfo:
        """Return a list of fonts matching pattern. No more than
        max_names will be returned. Each list item represents one font
        and has the following properties:

        name
            The name of the font.
        min_bounds
        max_bounds
        min_char_or_byte2
        max_char_or_byte2
        default_char
        draw_direction
        min_byte1
        max_byte1
        all_chars_exist
        font_ascent
        font_descent
        replies_hint
            See the description of XFontStruct in XGetFontProperty(3X11)
            for details on these values.
        properties
            A list of properties. Each entry has two attributes:

            name
                The atom identifying this property.
            value
                A 32-bit unsigned value.
        """

    def set_font_path(self, path: Sequence[str], onerror: ErrorHandler[object] | None = None) -> None:
        """Set the font path to path, which should be a list of strings.
        If path is empty, the default font path of the server will be
        restored.
        """

    def get_font_path(self) -> list[str]:
        """Return the current font path as a list of strings."""

    def query_extension(self, name: str) -> request.QueryExtension | None:
        """Ask the server if it supports the extension name. If it is
        supported an object with the following attributes is returned:

        major_opcode
            The major opcode that the requests of this extension uses.
        first_event
            The base event code if the extension have additional events, or 0.
        first_error
            The base error code if the extension have additional errors, or 0.

        If the extension is not supported, None is returned.
        """

    def list_extensions(self) -> list[str]:
        """Return a list of all the extensions provided by the server."""

    def change_keyboard_mapping(
        self, first_keycode: int, keysyms: Sequence[Sequence[int]], onerror: ErrorHandler[object] | None = None
    ) -> None:
        """Modify the keyboard mapping, starting with first_keycode.
        keysyms is a list of tuples of keysyms. keysyms[n][i] will be
        assigned to keycode first_keycode+n at index i.
        """

    def get_keyboard_mapping(self, first_keycode: int, count: int) -> list[tuple[int, ...]]:
        """Return the current keyboard mapping as a list of tuples,
        starting at first_keycount and no more than count.
        """

    def change_keyboard_control(self, onerror: ErrorHandler[object] | None = None, **keys: object) -> None:
        """Change the parameters provided as keyword arguments:

        key_click_percent
            The volume of key clicks between 0 (off) and 100 (load).
            -1 will restore default setting.
        bell_percent
            The base volume of the bell, coded as above.
        bell_pitch
            The pitch of the bell in Hz, -1 restores the default.
        bell_duration
            The duration of the bell in milliseconds, -1 restores
            the default.
        led

        led_mode
            led_mode should be X.LedModeOff or X.LedModeOn. If led is
            provided, it should be a 32-bit mask listing the LEDs that
            should change. If led is not provided, all LEDs are changed.
        key

        auto_repeat_mode
            auto_repeat_mode should be one of X.AutoRepeatModeOff,
            X.AutoRepeatModeOn, or X.AutoRepeatModeDefault. If key is
            provided, that key will be modified, otherwise the global
            state for the entire keyboard will be modified.
        """

    def get_keyboard_control(self) -> request.GetKeyboardControl:
        """Return an object with the following attributes:

        global_auto_repeat
            X.AutoRepeatModeOn or X.AutoRepeatModeOff.

        auto_repeats
            A list of 32 integers. List item N contains the bits for keys
            8N to 8N + 7 with the least significant bit in the byte
            representing key 8N. If a bit is on, autorepeat is enabled
            for the corresponding key.

        led_mask
            A 32-bit mask indicating which LEDs are on.

        key_click_percent
            The volume of key click, from 0 to 100.

        bell_percent

        bell_pitch

        bell_duration
            The volume, pitch and duration of the bell.
        """

    def bell(self, percent: int = 0, onerror: ErrorHandler[object] | None = None) -> None:
        """Ring the bell at the volume percent which is relative the base
        volume. See XBell(3X11).
        """

    def change_pointer_control(
        self, accel: tuple[int, int] | None = None, threshold: int | None = None, onerror: ErrorHandler[object] | None = None
    ) -> None:
        """To change the pointer acceleration, set accel to a tuple (num,
        denum). The pointer will then move num/denum times the normal
        speed if it moves beyond the threshold number of pixels at once.
        To change the threshold, set it to the number of pixels. -1
        restores the default.
        """

    def get_pointer_control(self) -> request.GetPointerControl:
        """Return an object with the following attributes:

        accel_num

        accel_denom
            The acceleration as numerator/denumerator.

        threshold
            The number of pixels the pointer must move before the
            acceleration kicks in.
        """

    def set_screen_saver(
        self, timeout: int, interval: int, prefer_blank: int, allow_exposures: int, onerror: ErrorHandler[object] | None = None
    ) -> None:
        """See XSetScreenSaver(3X11)."""

    def get_screen_saver(self) -> request.GetScreenSaver:
        """Return an object with the attributes timeout, interval,
        prefer_blanking, allow_exposures. See XGetScreenSaver(3X11) for
        details.
        """

    def change_hosts(
        self,
        mode: int,
        host_family: int,
        host: Sequence[int] | Sequence[bytes],  # TODO: validate
        onerror: ErrorHandler[object] | None = None,
    ) -> None:
        """mode is either X.HostInsert or X.HostDelete. host_family is
        one of X.FamilyInternet, X.FamilyDECnet, X.FamilyChaos,
        X.FamilyServerInterpreted or X.FamilyInternetV6.

        host is a list of bytes. For the Internet family, it should be the
        four bytes of an IPv4 address.
        """

    def list_hosts(self) -> request.ListHosts:
        """Return an object with the following attributes:

        mode
            X.EnableAccess if the access control list is used, X.DisableAccess otherwise.
        hosts
            The hosts on the access list. Each entry has the following attributes:

            family
                X.FamilyInternet, X.FamilyDECnet, X.FamilyChaos, X.FamilyServerInterpreted or X.FamilyInternetV6.
            name
                A list of byte values, the coding depends on family. For the Internet family, it is the 4 bytes of an IPv4 address.

        """

    def set_access_control(self, mode: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Enable use of access control lists at connection setup if mode
        is X.EnableAccess, disable if it is X.DisableAccess.
        """

    def set_close_down_mode(self, mode: int, onerror: ErrorHandler[object] | None = None) -> None:
        """Control what will happen with the client's resources at
        connection close. The default is X.DestroyAll, the other values
        are X.RetainPermanent and X.RetainTemporary.
        """

    def force_screen_saver(self, mode: int, onerror: ErrorHandler[object] | None = None) -> None:
        """If mode is X.ScreenSaverActive the screen saver is activated.
        If it is X.ScreenSaverReset, the screen saver is deactivated as
        if device input had been received.
        """

    def set_pointer_mapping(self, map: Sequence[int]) -> int:
        """Set the mapping of the pointer buttons. map is a list of
        logical button numbers. map must be of the same length as the
        list returned by Display.get_pointer_mapping().

        map[n] sets the
        logical number for the physical button n+1. Logical number 0
        disables the button. Two physical buttons cannot be mapped to the
        same logical number.

        If one of the buttons to be altered are
        logically in the down state, X.MappingBusy is returned and the
        mapping is not changed. Otherwise the mapping is changed and
        X.MappingSuccess is returned.
        """

    def get_pointer_mapping(self) -> list[int]:
        """Return a list of the pointer button mappings. Entry N in the
        list sets the logical button number for the physical button N+1.
        """

    def set_modifier_mapping(self, keycodes: rq._ModifierMappingList8Elements) -> int:
        """Set the keycodes for the eight modifiers X.Shift, X.Lock,
        X.Control, X.Mod1, X.Mod2, X.Mod3, X.Mod4 and X.Mod5. keycodes
        should be a eight-element list where each entry is a list of the
        keycodes that should be bound to that modifier.

        If any changed
        key is logically in the down state, X.MappingBusy is returned and
        the mapping is not changed. If the mapping violates some server
        restriction, X.MappingFailed is returned. Otherwise the mapping
        is changed and X.MappingSuccess is returned.
        """

    def get_modifier_mapping(self) -> Sequence[Sequence[int]]:
        """Return a list of eight lists, one for each modifier. The list
        can be indexed using X.ShiftMapIndex, X.Mod1MapIndex, and so on.
        The sublists list the keycodes bound to that modifier.
        """

    def no_operation(self, onerror: ErrorHandler[object] | None = None) -> None:
        """Do nothing but send a request to the server."""
