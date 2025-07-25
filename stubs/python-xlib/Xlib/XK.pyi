from Xlib.keysymdef.latin1 import *
from Xlib.keysymdef.miscellany import *
from Xlib.X import NoSymbol as NoSymbol

def string_to_keysym(keysym: str) -> int:
    """Return the (16 bit) numeric code of keysym.

    Given the name of a keysym as a string, return its numeric code.
    Don't include the 'XK_' prefix, just use the base, i.e. 'Delete'
    instead of 'XK_Delete'.
    """

def load_keysym_group(group: str) -> None:
    """Load all the keysyms in group.

    Given a group name such as 'latin1' or 'katakana' load the keysyms
    defined in module 'Xlib.keysymdef.group-name' into this XK module.
    """

def keysym_to_string(keysym: int) -> str | None:
    """Translate a keysym (16 bit number) into a python string.

    This will pass 0 to 0xff as well as XK_BackSpace, XK_Tab, XK_Clear,
    XK_Return, XK_Pause, XK_Scroll_Lock, XK_Escape, XK_Delete. For other
    values it returns None.
    """
