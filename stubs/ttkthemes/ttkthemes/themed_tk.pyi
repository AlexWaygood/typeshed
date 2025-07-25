"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""

import tkinter
from typing import Any

from ._widget import ThemedWidget

class ThemedTk(tkinter.Tk, ThemedWidget):
    """
    Tk child class that supports the themes supplied in this package

    A theme can be set upon initialization or during runtime. Can be
    used as a drop-in replacement for the normal Tk class. Additional
    options:

    - Initial theme ``theme``:
      Sets the initial theme to the theme specified. If the theme is
      not available, fails silently (there is no indication that the
      theme is not set other than it not appearing to the user).

    - Toplevel background color ``toplevel``:
      Hooks into the Toplevel.__init__ function to set a default window
      background color in the options passed. The hook is not removed
      after the window is destroyed, which is by design because creating
      multiple Tk instances should not be done in the first place.

    - Tk background color ``themebg``:
      Set the default background color of a Tk window to the default
      theme background color. For example: The background of windows
      may take on a dark color for dark themes. Backwards-compatible
      with the ``background`` keyword argument of v2.3.0 and earlier.

    - GIF theme override ``gif_override``:
      Forces ttkthemes to load the GIF version of themes that also
      provide a PNG version even if the PNG version can be loaded. Can
      only be set at object initialization. GIF themes may provide a
      higher UI performance than other themes.
    """

    def __init__(
        self,
        # non-keyword-only args copied from tkinter.Tk
        screenName: str | None = ...,
        baseName: str | None = ...,
        className: str = ...,
        useTk: bool = ...,
        sync: bool = ...,
        use: str | None = ...,
        *,
        theme: str | None = ...,
        # fonts argument does nothing
        toplevel: bool | None = ...,
        themebg: bool | None = ...,
        background: bool | None = ...,  # old alias for themebg
        gif_override: bool = ...,
    ) -> None:
        """
        :param theme: Theme to set upon initialization. If theme is not
            available, fails silently.
        :param toplevel: Control Toplevel background color option,
            see class documentation for details.
        :param themebg: Control Tk background color option, see
            class documentation for details.
        :param fonts: Whether to enable the automatic change of default
            font selected for a theme
        """

    def set_theme(self, theme_name: str, toplevel: bool | None = None, themebg: bool | None = None) -> None:
        """Redirect the set_theme call to also set Tk background color"""
    # Keep this in sync with tkinter.Tk
    def config(  # type: ignore[override]
        self,
        kw: dict[str, Any] | None = None,
        *,
        themebg: bool | None = ...,
        toplevel: bool | None = ...,
        theme: str | None = ...,
        background: str = ...,
        bd: tkinter._ScreenUnits = ...,
        bg: str = ...,
        border: tkinter._ScreenUnits = ...,
        borderwidth: tkinter._ScreenUnits = ...,
        cursor: tkinter._Cursor = ...,
        height: tkinter._ScreenUnits = ...,
        highlightbackground: str = ...,
        highlightcolor: str = ...,
        highlightthickness: tkinter._ScreenUnits = ...,
        menu: tkinter.Menu = ...,
        padx: tkinter._ScreenUnits = ...,
        pady: tkinter._ScreenUnits = ...,
        relief: tkinter._Relief = ...,
        takefocus: tkinter._TakeFocusValue = ...,
        width: tkinter._ScreenUnits = ...,
    ) -> dict[str, tuple[str, str, str, Any, Any]] | None:
        """configure redirect to support additional options"""

    def cget(self, k: str) -> Any:
        """cget redirect to support additional options"""

    def configure(  # type: ignore[override]
        self,
        kw: dict[str, Any] | None = None,
        *,
        themebg: bool | None = ...,
        toplevel: bool | None = ...,
        theme: str | None = ...,
        background: str = ...,
        bd: tkinter._ScreenUnits = ...,
        bg: str = ...,
        border: tkinter._ScreenUnits = ...,
        borderwidth: tkinter._ScreenUnits = ...,
        cursor: tkinter._Cursor = ...,
        height: tkinter._ScreenUnits = ...,
        highlightbackground: str = ...,
        highlightcolor: str = ...,
        highlightthickness: tkinter._ScreenUnits = ...,
        menu: tkinter.Menu = ...,
        padx: tkinter._ScreenUnits = ...,
        pady: tkinter._ScreenUnits = ...,
        relief: tkinter._Relief = ...,
        takefocus: tkinter._TakeFocusValue = ...,
        width: tkinter._ScreenUnits = ...,
    ) -> dict[str, tuple[str, str, str, Any, Any]] | None: ...
    def __getitem__(self, k: str) -> Any: ...
    def __setitem__(self, k: str, v: Any) -> None: ...
