"""
Complete implementation of the XDG Icon Spec
http://standards.freedesktop.org/icon-theme-spec/
"""

from _typeshed import StrPath
from collections.abc import Collection

from xdg.IniFile import IniFile

class IconTheme(IniFile):
    """Class to parse and validate IconThemes"""

    def __init__(self) -> None: ...
    dir: str
    name: str
    comment: str
    directories: list[str]
    type: str
    def parse(self, file: StrPath) -> None: ...  # type: ignore[override]
    def getDir(self) -> str: ...
    def getName(self) -> str: ...
    def getComment(self) -> str: ...
    def getInherits(self) -> list[str]: ...
    def getDirectories(self) -> list[str]: ...
    def getScaledDirectories(self) -> list[str]: ...
    def getHidden(self) -> bool: ...
    def getExample(self) -> str: ...
    def getSize(self, directory: StrPath) -> int: ...
    def getContext(self, directory: StrPath) -> str: ...
    def getType(self, directory: StrPath) -> str: ...
    def getMaxSize(self, directory: StrPath) -> int: ...
    def getMinSize(self, directory: StrPath) -> int: ...
    def getThreshold(self, directory: StrPath) -> int: ...
    def getScale(self, directory: StrPath) -> int: ...
    def checkExtras(self) -> None: ...
    def checkGroup(self, group: str) -> None: ...
    def checkKey(self, key: str, value: str, group: str) -> None: ...

class IconData(IniFile):
    """Class to parse and validate IconData Files"""

    def __init__(self) -> None: ...
    def parse(self, file: StrPath) -> None: ...  # type: ignore[override]
    def getDisplayName(self) -> str:
        """Retrieve the display name from the icon data, if one is specified."""

    def getEmbeddedTextRectangle(self) -> list[int]:
        """Retrieve the embedded text rectangle from the icon data as a list of
        numbers (x0, y0, x1, y1), if it is specified.
        """

    def getAttachPoints(self) -> list[tuple[int, int]]:
        """Retrieve the anchor points for overlays & emblems from the icon data,
        as a list of co-ordinate pairs, if they are specified.
        """

    def checkExtras(self) -> None: ...
    def checkGroup(self, group: str) -> None: ...
    def checkKey(self, key: str, value: str, group: str) -> None: ...

icondirs: list[str]
themes: list[IconTheme]
theme_cache: dict[str, IconTheme]
dir_cache: dict[str, tuple[str, float, float]]
icon_cache: dict[tuple[str, int, str, tuple[str, ...]], tuple[float, str]]

def getIconPath(
    iconname: str, size: int | None = None, theme: str | None = None, extensions: Collection[str] = ["png", "svg", "xpm"]
) -> str:
    """Get the path to a specified icon.

    size :
      Icon size in pixels. Defaults to ``xdg.Config.icon_size``.
    theme :
      Icon theme name. Defaults to ``xdg.Config.icon_theme``. If the icon isn't
      found in the specified theme, it will be looked up in the basic 'hicolor'
      theme.
    extensions :
      List of preferred file extensions.

    Example::

        >>> getIconPath("inkscape", 32)
        '/usr/share/icons/hicolor/32x32/apps/inkscape.png'
    """

def getIconData(path: str) -> IconData:
    """Retrieve the data from the .icon file corresponding to the given file. If
    there is no .icon file, it returns None.

    Example::

        getIconData("/usr/share/icons/Tango/scalable/places/folder.svg")
    """

def LookupIcon(iconname: str, size: int, theme: str, extensions: Collection[str]) -> str: ...
def DirectoryMatchesSize(subdir: str, iconsize: int, theme: str) -> bool: ...
def DirectorySizeDistance(subdir: str, iconsize: int, theme: str) -> int: ...
