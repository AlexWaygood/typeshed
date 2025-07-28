from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import ExternalItem as ExternalItem

class CommandItem(ExternalItem):
    """
    A menu item to execute a console command
    """

    command: str
    arguments: list[str]
    exit_status: int | None
    def __init__(
        self,
        text: str,
        command: str,
        arguments: list[str] | None = None,
        menu: ConsoleMenu | None = None,
        should_exit: bool = False,
        menu_char: str | None = None,
    ) -> None:
        """
        :ivar str text: The text shown for this menu item
        :ivar str command: The console command to be executed
        :ivar list[str] arguments: An optional list of string arguments to be passed to the command
        :ivar ConsoleMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this item's action is done
        :ivar str menu_char: The character used to select this menu item. Optional - defaults to None.
        """

    def action(self) -> None:
        """
        This class overrides this method
        """

    def get_return(self) -> int:
        """
        :return: the exit status of the command
        :rtype: int
        """
