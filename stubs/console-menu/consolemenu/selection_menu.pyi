from collections.abc import Iterable

from consolemenu import ConsoleMenu as ConsoleMenu
from consolemenu.items import SelectionItem as SelectionItem
from consolemenu.menu_formatter import MenuFormatBuilder
from consolemenu.screen import Screen

class SelectionMenu(ConsoleMenu):
    """
    A menu that simplifies item creation, just give it a list of strings and it builds the menu for you

    Args:
        strings (:obj:`list` of :obj:`str`):  The list of strings this menu should be built from.
        title (str): The title of the menu.
        subtitle (str): The subtitle of the menu.
        screen (:obj:`consolemenu.screen.Screen`): The screen object associated with this menu.
        formatter (:obj:`MenuFormatBuilder`): The MenuFormatBuilder instance used to format this menu.
        prologue_text (str): Text to include in the "prologue" section of the menu.
        epilogue_text (str): Text to include in the "epilogue" section of the menu.
        show_exit_option (bool): Specifies whether this menu should show an exit item by default. Defaults to True.
            Can be overridden when the menu is started.
        exit_option_text (str): Text for the Exit menu item. Defaults to 'Exit'.
        clear_screen (bool): Set to False to disable clearing of screen between menus
    """

    def __init__(
        self,
        strings: Iterable[str],
        title: str | None = None,
        subtitle: str | None = None,
        screen: Screen | None = None,
        formatter: MenuFormatBuilder | None = None,
        prologue_text: str | None = None,
        epilogue_text: str | None = None,
        show_exit_option: bool = True,
        exit_option_text: str = "Exit",
        clear_screen: bool = True,
    ) -> None: ...
    @classmethod
    def get_selection(
        cls,
        strings: Iterable[str],
        title: str = "Select an option",
        subtitle: str | None = None,
        show_exit_option: bool = True,
        _menu: ConsoleMenu | None = None,
    ) -> int:
        """
        Single-method way of getting a selection out of a list of strings.

        Args:
            strings (:obj:`list` of :obj:`str`):  The list of strings this menu should be built from.
            title (str): The title of the menu.
            subtitle (str): The subtitle of the menu.
            show_exit_option (bool): Specifies whether this menu should show an exit item by default. Defaults to True.
            _menu: Should probably only be used for testing, pass in a list and the created menu used internally by
                the method will be appended to it

        Returns:
            int: The index of the selected option.

        """

    def append_string(self, string: str) -> None: ...
