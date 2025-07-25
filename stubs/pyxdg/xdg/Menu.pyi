"""
Implementation of the XDG Menu Specification
http://standards.freedesktop.org/menu-spec/

Example code:

from xdg.Menu import parse, Menu, MenuEntry

def print_menu(menu, tab=0):
  for submenu in menu.Entries:
    if isinstance(submenu, Menu):
      print ("  " * tab) + unicode(submenu)
      print_menu(submenu, tab+1)
    elif isinstance(submenu, MenuEntry):
      print ("  " * tab) + unicode(submenu.DesktopEntry)

print_menu(parse())
"""

import ast
import xml.dom
from _typeshed import Unused
from collections.abc import Collection, Iterable, Iterator
from types import CodeType
from typing import Literal

from .DesktopEntry import DesktopEntry

DELETED: Literal["Deleted"] = "Deleted"
NO_DISPLAY: Literal["NoDisplay"] = "NoDisplay"
HIDDEN: Literal["Hidden"] = "Hidden"
EMPTY: Literal["Empty"] = "Empty"
NOT_SHOW_IN: Literal["NotShowIn"] = "NotShowIn"
NO_EXEC: Literal["NoExec"] = "NoExec"

class Menu:
    """Menu containing sub menus under menu.Entries

    Contains both Menu and MenuEntry items.
    """

    Name: str
    Directory: Menu | None
    Entries: list[str]
    Doc: str
    Filename: str
    Depth: int
    Parent: Menu | None
    NotInXml: bool
    Show: bool
    Visible: int
    AppDirs: list[str]
    DefaultLayout: str | None
    Deleted: bool | None
    Directories: list[str]
    DirectoryDirs: list[Menu]
    Layout: Layout
    MenuEntries: list[MenuEntry | Menu | Separator]
    Moves: list[Move]
    OnlyUnallocated: bool | None
    Rules: list[Rule]
    Submenus: list[Menu]
    def __init__(self) -> None: ...
    def __add__(self, other: Menu) -> Menu: ...
    def __cmp__(self, other: Menu) -> int: ...
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def getEntries(self, show_hidden: bool = False) -> Iterator[str]:
        """Interator for a list of Entries visible to the user."""

    def getMenuEntry(self, desktopfileid: int, deep: bool = False) -> MenuEntry:
        """Searches for a MenuEntry with a given DesktopFileID."""

    def getMenu(self, path: str) -> Menu:
        """Searches for a Menu with a given path."""

    def getPath(self, org: bool = False, toplevel: bool = False) -> str:
        """Returns this menu's path in the menu structure."""

    def getName(self) -> str:
        """Returns the menu's localised name."""

    def getGenericName(self) -> str:
        """Returns the menu's generic name."""

    def getComment(self) -> str:
        """Returns the menu's comment text."""

    def getIcon(self) -> str:
        """Returns the menu's icon, filename or simple name"""

    def sort(self) -> None: ...
    def addSubmenu(self, newmenu: Menu) -> None: ...
    def merge_inline(self, submenu: Menu) -> None:
        """Appends a submenu's entries to this menu
        See the <Menuname> section of the spec about the "inline" attribute
        """

class Move:
    """A move operation"""

    Old: str
    New: str
    def __init__(self, old: str = "", new: str = "") -> None: ...
    def __cmp__(self, other: Move) -> int: ...

class Layout:
    """Menu Layout class"""

    show_empty: bool
    inline: bool
    inline_limit: int
    inline_header: bool
    inline_alias: bool
    def __init__(
        self,
        show_empty: bool = False,
        inline: bool = False,
        inline_limit: int = 4,
        inline_header: bool = True,
        inline_alias: bool = False,
    ) -> None: ...
    @property
    def order(self) -> list[list[str]]: ...
    @order.setter
    def order(self, order: list[list[str]]) -> None: ...

class Rule:
    """Include / Exclude Rules Class"""

    TYPE_INCLUDE: Literal[0]
    TYPE_EXCLUDE: Literal[1]
    @classmethod
    def fromFilename(cls, type: Literal[0, 1], filename: str) -> Rule: ...
    Type: Literal[0, 1]
    expression: ast.Expression
    code: CodeType
    def __init__(self, type: Literal[0, 1], expression: str) -> None: ...
    def apply(self, menuentries: Iterable[MenuEntry], run: int) -> Iterable[MenuEntry]: ...

class MenuEntry:
    """Wrapper for 'Menu Style' Desktop Entries"""

    TYPE_USER: Literal["User"]
    TYPE_SYSTEM: Literal["System"]
    TYPE_BOTH: Literal["Both"]
    DesktopEntry: DesktopEntry
    Show: Literal[True, False, "Deleted", "NoDisplay", "Hidden", "Empty", "NotShowIn", "NoExec"]
    Visible: Literal[1, 0, "Deleted", "NoDisplay", "Hidden", "Empty", "NotShowIn", "NoExec"]
    Original: MenuEntry | None
    Parents: list[Menu]
    Allocated: bool
    Add: bool
    MatchedInclude: bool
    Categories: list[str]
    def __init__(self, filename: str, dir: str = "", prefix: str = "") -> None: ...
    def save(self) -> None:
        """Save any changes to the desktop entry."""

    def getDir(self) -> str:
        """Return the directory containing the desktop entry file."""

    def getType(self) -> Literal["User", "System", "Both"]:
        """Return the type of MenuEntry, System/User/Both"""
    Filename: str
    Prefix: str
    DesktopFileID: str
    def setAttributes(self, filename: str, dir: str = "", prefix: str = "") -> None: ...
    def updateAttributes(self) -> None: ...
    def __cmp__(self, other: MenuEntry) -> int: ...
    def __lt__(self, other: MenuEntry) -> bool: ...
    def __eq__(self, other: object) -> bool: ...

class Separator:
    """Just a dummy class for Separators"""

    Parent: Menu
    Show: bool
    def __init__(self, parent: Menu) -> None: ...

class Header:
    """Class for Inline Headers"""

    Name: str
    GenericName: str
    Comment: str
    def __init__(self, name: str, generic_name: str, comment: str) -> None: ...

TYPE_DIR: Literal[0] = 0
TYPE_FILE: Literal[1] = 1

class XMLMenuBuilder:
    debug: bool
    def __init__(self, debug: bool = False) -> None: ...
    cache: MenuEntryCache
    def parse(self, filename: str | None = None) -> Menu:
        """Load an applications.menu file.

        filename : str, optional
          The default is ``$XDG_CONFIG_DIRS/menus/${XDG_MENU_PREFIX}applications.menu``.
        """

    def parse_menu(self, node: xml.dom.Node, filename: str) -> Menu: ...
    def parse_node(self, node: xml.dom.Node, filename: str, parent: Menu | None = None) -> None: ...
    def parse_layout(self, node: xml.dom.Node) -> Layout: ...
    def parse_move(self, node: xml.dom.Node) -> Move: ...
    def parse_rule(self, node: xml.dom.Node) -> Rule: ...
    def parse_bool_op(self, node: xml.dom.Node, operator: ast.And | ast.Or) -> ast.BoolOp | ast.UnaryOp | ast.Compare | None: ...
    def parse_rule_node(self, node: xml.dom.Node) -> ast.BoolOp | ast.UnaryOp | ast.Compare | None: ...
    def parse_app_dir(self, value: str, filename: str, parent: str) -> None: ...
    def parse_default_app_dir(self, filename: str, parent: str) -> None: ...
    def parse_directory_dir(self, value: str, filename: str, parent: str) -> None: ...
    def parse_default_directory_dir(self, filename: str, parent: str) -> None: ...
    def parse_merge_file(self, value: str, child: Menu | MenuEntry, filename: str, parent: str) -> None: ...
    def parse_merge_dir(self, value: str, child: Menu | MenuEntry, filename: str, parent: str) -> None: ...
    def parse_default_merge_dirs(self, child: Menu | MenuEntry, filename: str, parent: str) -> None: ...
    def merge_file(self, filename: str, child: Unused, parent: Menu) -> None: ...
    def parse_legacy_dir(self, dir_: str, prefix: str, filename: str, parent: str) -> None: ...
    def merge_legacy_dir(self, dir_: str, prefix: str, filename: str, parent: str) -> Menu: ...
    def parse_kde_legacy_dirs(self, filename: str, parent: str) -> None: ...
    def post_parse(self, menu: Menu) -> None: ...
    def generate_not_only_allocated(self, menu: Menu) -> None: ...
    def generate_only_allocated(self, menu: Menu) -> None: ...
    def handle_moves(self, menu: Menu) -> None: ...

class MenuEntryCache:
    """Class to cache Desktop Entries"""

    cacheEntries: dict[str, list[MenuEntry]]
    cache: dict[str, list[MenuEntry]]
    def __init__(self) -> None: ...
    def add_menu_entries(self, dirs: Iterable[str], prefix: str = "", legacy: bool = False) -> None: ...
    def get_menu_entries(self, dirs: Collection[str], legacy: bool = True) -> list[MenuEntry]: ...

def parse(filename: str | None = None, debug: bool = False) -> XMLMenuBuilder:
    """Helper function.
    Equivalent to calling xdg.Menu.XMLMenuBuilder().parse(filename)
    """
