"""This implements a virtual screen. This is used to support ANSI terminal
emulation. The screen representation and state is implemented in this class.
Most of the methods are inspired by ANSI screen control codes. The
:class:`~pexpect.ANSI.ANSI` class extends this class to add parsing of ANSI
escape codes.

PEXPECT LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2012, Noah Spurrier <noah@noah.org>
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""

from _typeshed import Incomplete

NUL: int
ENQ: int
BEL: int
BS: int
HT: int
LF: int
VT: int
FF: int
CR: int
SO: int
SI: int
XON: int
XOFF: int
CAN: int
SUB: int
ESC: int
DEL: int
SPACE: str
PY3: Incomplete
unicode = str

def constrain(n, min, max):
    """This returns a number, n constrained to the min and max bounds."""

class screen:
    """This object maintains the state of a virtual text screen as a
    rectangular array. This maintains a virtual cursor position and handles
    scrolling as characters are added. This supports most of the methods needed
    by an ANSI text screen. Row and column indexes are 1-based (not zero-based,
    like arrays).

    Characters are represented internally using unicode. Methods that accept
    input characters, when passed 'bytes' (which in Python 2 is equivalent to
    'str'), convert them from the encoding specified in the 'encoding'
    parameter to the constructor. Methods that return screen contents return
    unicode strings, with the exception of __str__() under Python 2. Passing
    ``encoding=None`` limits the API to only accept unicode input, so passing
    bytes in will raise :exc:`TypeError`.
    """

    rows: Incomplete
    cols: Incomplete
    encoding: Incomplete
    encoding_errors: Incomplete
    decoder: Incomplete
    cur_r: int
    cur_c: int
    cur_saved_r: int
    cur_saved_c: int
    scroll_row_start: int
    scroll_row_end: Incomplete
    w: Incomplete
    def __init__(self, r: int = 24, c: int = 80, encoding: str = "latin-1", encoding_errors: str = "replace") -> None:
        """This initializes a blank screen of the given dimensions."""

    def dump(self):
        """This returns a copy of the screen as a unicode string. This is similar to
        __str__/__unicode__ except that lines are not terminated with line
        feeds.
        """

    def pretty(self):
        """This returns a copy of the screen as a unicode string with an ASCII
        text box around the screen border. This is similar to
        __str__/__unicode__ except that it adds a box.
        """

    def fill(self, ch=" ") -> None: ...
    def fill_region(self, rs, cs, re, ce, ch=" ") -> None: ...
    def cr(self) -> None:
        """This moves the cursor to the beginning (col 1) of the current row."""

    def lf(self) -> None:
        """This moves the cursor down with scrolling."""

    def crlf(self) -> None:
        """This advances the cursor with CRLF properties.
        The cursor will line wrap and the screen may scroll.
        """

    def newline(self) -> None:
        """This is an alias for crlf()."""

    def put_abs(self, r, c, ch) -> None:
        """Screen array starts at 1 index."""

    def put(self, ch) -> None:
        """This puts a characters at the current cursor position."""

    def insert_abs(self, r, c, ch) -> None:
        """This inserts a character at (r,c). Everything under
        and to the right is shifted right one character.
        The last character of the line is lost.
        """

    def insert(self, ch) -> None: ...
    def get_abs(self, r, c): ...
    def get(self) -> None: ...
    def get_region(self, rs, cs, re, ce):
        """This returns a list of lines representing the region."""

    def cursor_constrain(self) -> None:
        """This keeps the cursor within the screen area."""

    def cursor_home(self, r: int = 1, c: int = 1) -> None: ...
    def cursor_back(self, count: int = 1) -> None: ...
    def cursor_down(self, count: int = 1) -> None: ...
    def cursor_forward(self, count: int = 1) -> None: ...
    def cursor_up(self, count: int = 1) -> None: ...
    def cursor_up_reverse(self) -> None: ...
    def cursor_force_position(self, r, c) -> None:
        """Identical to Cursor Home."""

    def cursor_save(self) -> None:
        """Save current cursor position."""

    def cursor_unsave(self) -> None:
        """Restores cursor position after a Save Cursor."""

    def cursor_save_attrs(self) -> None:
        """Save current cursor position."""

    def cursor_restore_attrs(self) -> None:
        """Restores cursor position after a Save Cursor."""

    def scroll_constrain(self) -> None:
        """This keeps the scroll region within the screen region."""

    def scroll_screen(self) -> None:
        """Enable scrolling for entire display."""

    def scroll_screen_rows(self, rs, re) -> None:
        """Enable scrolling from row {start} to row {end}."""

    def scroll_down(self) -> None:
        """Scroll display down one line."""

    def scroll_up(self) -> None:
        """Scroll display up one line."""

    def erase_end_of_line(self) -> None:
        """Erases from the current cursor position to the end of the current
        line.
        """

    def erase_start_of_line(self) -> None:
        """Erases from the current cursor position to the start of the current
        line.
        """

    def erase_line(self) -> None:
        """Erases the entire current line."""

    def erase_down(self) -> None:
        """Erases the screen from the current line down to the bottom of the
        screen.
        """

    def erase_up(self) -> None:
        """Erases the screen from the current line up to the top of the
        screen.
        """

    def erase_screen(self) -> None:
        """Erases the screen with the background color."""

    def set_tab(self) -> None:
        """Sets a tab at the current position."""

    def clear_tab(self) -> None:
        """Clears tab at the current position."""

    def clear_all_tabs(self) -> None:
        """Clears all tabs."""
