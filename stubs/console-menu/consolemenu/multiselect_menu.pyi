from consolemenu import ConsoleMenu as ConsoleMenu
from consolemenu.console_menu import MenuItem
from consolemenu.items import SubmenuItem as SubmenuItem
from consolemenu.menu_formatter import MenuFormatBuilder

class MultiSelectMenu(ConsoleMenu):
    """
    Console menu that allows the selection of multiple menu items at a single prompt.

    Args:
        title: The menu title.
        subtitle: The menu subtitle.
        formatter: The menu formatter instance for styling the menu.
        prologue_text: The text to display in the prologue section of the menu.
        epilogue_text: The text to display in the epilogue section of the menu.
        show_exit_option (bool): Determines if the exit item should be displayed.
        exit_option_text (str): Text for the Exit menu item. Defaults to 'Exit'.
        clear_screen (bool): Set to False to disable clearing of screen between menus
    """

    ack_item_completion: bool
    def __init__(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        formatter: MenuFormatBuilder | None = None,
        prologue_text: str | None = None,
        epilogue_text: str | None = None,
        ack_item_completion: bool = True,
        show_exit_option: bool = True,
        exit_option_text: str = "Exit",
        clear_screen: bool = True,
    ) -> None: ...
    def append_item(self, item: MenuItem) -> None:
        """
        Add an item to the end of the menu before the exit item.

        Note that Multi-Select Menus will not allow a SubmenuItem to be added, as multi-select menus
        are expected to be used only for executing multiple actions.

        Args:
            item (:obj:`MenuItem`): The item to be added

        Raises:
            TypeError: If the specified MenuIem is a SubmenuItem.
        """
    current_option: int
    def process_user_input(self) -> None:
        """
        This overrides the method in ConsoleMenu to allow for comma-delimited and range inputs.

        Examples:
            All of the following inputs would have the same result:
                * 1,2,3,4
                * 1-4
                * 1-2,3-4
                * 1 - 4
                * 1, 2, 3, 4
        Raises:
            ValueError: If the input cannot be correctly parsed.
        """
