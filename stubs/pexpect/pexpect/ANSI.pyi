"""This implements an ANSI (VT100) terminal emulator as a subclass of screen.

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

from . import screen

def DoEmit(fsm) -> None: ...
def DoStartNumber(fsm) -> None: ...
def DoBuildNumber(fsm) -> None: ...
def DoBackOne(fsm) -> None: ...
def DoBack(fsm) -> None: ...
def DoDownOne(fsm) -> None: ...
def DoDown(fsm) -> None: ...
def DoForwardOne(fsm) -> None: ...
def DoForward(fsm) -> None: ...
def DoUpReverse(fsm) -> None: ...
def DoUpOne(fsm) -> None: ...
def DoUp(fsm) -> None: ...
def DoHome(fsm) -> None: ...
def DoHomeOrigin(fsm) -> None: ...
def DoEraseDown(fsm) -> None: ...
def DoErase(fsm) -> None: ...
def DoEraseEndOfLine(fsm) -> None: ...
def DoEraseLine(fsm) -> None: ...
def DoEnableScroll(fsm) -> None: ...
def DoCursorSave(fsm) -> None: ...
def DoCursorRestore(fsm) -> None: ...
def DoScrollRegion(fsm) -> None: ...
def DoMode(fsm) -> None: ...
def DoLog(fsm) -> None: ...

class term(screen.screen):
    """This class is an abstract, generic terminal.
    This does nothing. This is a placeholder that
    provides a common base class for other terminals
    such as an ANSI terminal.
    """

    def __init__(self, r: int = 24, c: int = 80, *args, **kwargs) -> None: ...

class ANSI(term):
    """This class implements an ANSI (VT100) terminal.
    It is a stream filter that recognizes ANSI terminal
    escape sequences and maintains the state of a screen object.
    """

    state: Incomplete
    def __init__(self, r: int = 24, c: int = 80, *args, **kwargs) -> None: ...
    def process(self, c) -> None:
        """Process a single character. Called by :meth:`write`."""

    def process_list(self, l) -> None: ...
    def write(self, s) -> None:
        """Process text, writing it to the virtual screen while handling
        ANSI escape codes.
        """

    def flush(self) -> None: ...
    def write_ch(self, ch) -> None:
        """This puts a character at the current cursor position. The cursor
        position is moved forward with wrap-around, but no scrolling is done if
        the cursor hits the lower-right corner of the screen.
        """

    def do_sgr(self, fsm) -> None:
        """Select Graphic Rendition, e.g. color."""

    def do_decsca(self, fsm) -> None:
        """Select character protection attribute."""

    def do_modecrap(self, fsm) -> None:
        """Handler for \x1b[?<number>h and \x1b[?<number>l. If anyone
        wanted to actually use these, they'd need to add more states to the
        FSM rather than just improve or override this method.
        """
