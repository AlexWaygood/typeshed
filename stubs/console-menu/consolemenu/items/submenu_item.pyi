from collections.abc import Callable

from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import MenuItem as MenuItem

class SubmenuItem(MenuItem):
    """
    A menu item to open a submenu
    """

    submenu: ConsoleMenu
    def __init__(
        self,
        text: str | Callable[[], str],
        submenu: ConsoleMenu,
        menu: ConsoleMenu | None = None,
        should_exit: bool = False,
        menu_char: str | None = None,
    ) -> None:
        """
        :ivar str text: The text shown for this menu item
        :ivar ConsoleMenu submenu: The submenu to be opened when this item is selected
        :ivar ConsoleMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this item's action is done
        :ivar str menu_char: The character used to select this menu item. Optional - defaults to None.
        """
    menu: ConsoleMenu
    def set_menu(self, menu: ConsoleMenu) -> None:
        """
        Sets the menu of this item.
        Should be used instead of directly accessing the menu attribute for this class.

        :param ConsoleMenu menu: the menu
        """

    def set_up(self) -> None:
        """
        This class overrides this method
        """

    def action(self) -> None:
        """
        This class overrides this method
        """

    def clean_up(self) -> None:
        """
        This class overrides this method
        """

    def get_return(self) -> object:
        """
        :return: The returned value in the submenu
        """

    def get_submenu(self) -> ConsoleMenu:
        """
        We unwrap the submenu variable in case it is a reference to a method that returns a submenu
        """
