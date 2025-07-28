"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""

import tkinter
from tkinter import ttk

from ._widget import ThemedWidget

class ThemedStyle(ttk.Style, ThemedWidget):
    """
    Style that supports setting the theme for a Tk instance. Can be
    used as a drop-in replacement for normal ttk.Style instances.
    Supports the themes provided by this package.
    """

    def __init__(self, master: tkinter.Misc | None = ..., *, theme: str | None = None, gif_override: bool | None = False) -> None:
        """
        :param theme: Theme to set up initialization completion. If the
                      theme is not available, fails silently.
        """
    # theme_use() can't return None (differs from ttk.Style)
    def theme_use(self, theme_name: str | None = None) -> str:  # type: ignore[override]
        """
        Set a new theme to use or return current theme name

        :param theme_name: name of theme to use
        :returns: active theme name
        """

    def theme_names(self) -> list[str]:  # type: ignore[override]
        """
        Alias of get_themes() to allow for a drop-in replacement of the
        normal ttk.Style instance.

        :returns: Result of get_themes()
        """
