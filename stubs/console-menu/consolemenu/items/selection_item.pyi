from collections.abc import Callable

from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import MenuItem as MenuItem

class SelectionItem(MenuItem):
    """
    The item type used in :class:`consolemenu.SelectionMenu`
    """

    index: int
    def __init__(
        self, text: str | Callable[[], str], index: int, menu: ConsoleMenu | None = None, menu_char: str | None = None
    ) -> None:
        """
        :ivar str text: The text shown for this menu item
        :ivar int index: The index of this item in the list used to initialize the :class:`consolemenu.SelectionMenu`
        :ivar ConsoleMenu menu: The menu to which this item belongs
        :ivar str menu_char: The character used to select this menu item. Optional - defaults to None.
        """

    def get_return(self) -> int:
        """
        :return: The index of this item in the list of strings
        :rtype: int
        """
