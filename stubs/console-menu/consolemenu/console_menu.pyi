from collections.abc import Callable

from consolemenu.menu_formatter import MenuFormatBuilder as MenuFormatBuilder
from consolemenu.screen import Screen as Screen

class ConsoleMenu:
    """
    A class that displays a menu and allows the user to select an option.

    Args:
        title (str): The title of the menu, or a method reference that returns a string.
        subtitle (str): The subtitle of the menu, or a method reference that returns a string.
        screen (:obj:`consolemenu.screen.Screen`): The screen object associated with this menu.
        formatter (:obj:`MenuFormatBuilder`): The MenuFormatBuilder instance used to format this menu.
        prologue_text (str): Text or method reference to include in the "prologue" section of the menu.
        epilogue_text (str): Text or method reference to include in the "epilogue" section of the menu.
        show_exit_option (bool): Specifies whether this menu should show an exit item by default. Defaults to True.
            Can be overridden when the menu is started.
        exit_option_text (str): Text for the Exit menu item. Defaults to 'Exit'.
        exit_menu_char (str): Character to use for exiting the menu. Defaults to None.
        clear_screen (bool): Set to False to disable clearing of screen between menus

    Attributes:
        cls.currently_active_menu (:obj:`ConsoleMenu`): Class variable that holds the currently active menu or None
            if no menu is currently active (e.g. when switching between menus)
        items (:obj:`list` of :obj:`MenuItem`): The list of MenuItems that the menu will display
        parent (:obj:`ConsoleMenu`): The parent of this menu
        previous_active_menu (:obj:`ConsoleMenu`): the previously active menu to be restored into the class's
            currently active menu
        current_option (int): The currently highlighted menu option
        selected_option (int): The option that the user has most recently selected
    """

    currently_active_menu: ConsoleMenu | None
    screen: Screen
    clear_screen_before_render: bool
    formatter: MenuFormatBuilder
    title: str | Callable[[], str] | None
    subtitle: str | Callable[[], str] | None
    prologue_text: str | Callable[[], str] | None
    epilogue_text: str | Callable[[], str] | None
    highlight: None
    normal: None
    show_exit_option: bool
    items: list[MenuItem]
    parent: ConsoleMenu | None
    exit_item: ExitItem
    current_option: int
    selected_option: int
    returned_value: object
    should_exit: bool
    previous_active_menu: ConsoleMenu | None
    def __init__(
        self,
        title: str | Callable[[], str] | None = None,
        subtitle: str | Callable[[], str] | None = None,
        screen: Screen | None = None,
        formatter: MenuFormatBuilder | None = None,
        prologue_text: str | Callable[[], str] | None = None,
        epilogue_text: str | Callable[[], str] | None = None,
        clear_screen: bool = True,
        show_exit_option: bool = True,
        exit_option_text: str = "Exit",
        exit_menu_char: str | None = None,
    ) -> None: ...
    @property
    def current_item(self) -> MenuItem | None:
        """
        :obj:`consolemenu.items.MenuItem`: The item corresponding to the menu option that is currently highlighted,
            or None.
        """

    @property
    def selected_item(self) -> MenuItem | None:
        """
        :obj:`consolemenu.items.MenuItem`:  The item in :attr:`items` that the user most recently selected, or None.
        """

    def append_item(self, item: MenuItem) -> None:
        """
        Add an item to the end of the menu before the exit item.

        Args:
            item (MenuItem): The item to be added.

        """

    def remove_item(self, item: MenuItem) -> bool:
        """
        Remove the specified item from the menu.

        Args:
            item (MenuItem): the item to be removed.

        Returns:
            bool: True if the item was removed; False otherwise.
        """

    def add_exit(self) -> bool:
        """
        Add the exit item if necessary. Used to make sure there aren't multiple exit items.

        Returns:
            bool: True if item needed to be added, False otherwise.
        """

    def remove_exit(self) -> bool:
        """
        Remove the exit item if necessary. Used to make sure we only remove the exit item, not something else.

        Returns:
            bool: True if item needed to be removed, False otherwise.
        """

    def is_selected_item_exit(self) -> bool:
        """
        Checks to determine if the currently selected item is the Exit Menu item.

        Returns:
            bool: True if the currently selected item is the Exit Menu item; False otherwise.
        """

    def start(self, show_exit_option: bool | None = None) -> None:
        """
        Start the menu in a new thread and allow the user to interact with it.
        The thread is a daemon, so :meth:`join()<consolemenu.ConsoleMenu.join>` should be called if there's a
        possibility that the main thread will exit before the menu is done

        Args:
            show_exit_option (bool): Specify whether the exit item should be shown, defaults to the value
                set in the constructor

        """

    def show(self, show_exit_option: bool | None = None) -> None:
        """
        Calls start and then immediately joins.

        Args:
            show_exit_option (bool):  Specify whether the exit item should be shown, defaults to the value set
                in the constructor

        """

    def draw(self) -> None:
        """
        Refresh the screen and redraw the menu. Should be called whenever something changes that needs to be redrawn.
        """

    def is_running(self) -> bool:
        """
        Check if the menu has been started and is not paused.

        Returns:
            bool: True if the menu is started and hasn't been paused; False otherwise.
        """

    def wait_for_start(self, timeout: float | None = None) -> bool:
        """
        Block until the menu is started.

        Args:
            timeout:  How long to wait before timing out.

        Returns:
            bool: False if timeout is given and operation times out, True otherwise. None before Python 2.7.
        """

    def is_alive(self) -> bool:
        """
        Check whether the thread is stil alive.

        Returns:
            bool: True if the thread is still alive; False otherwise.
        """

    def pause(self) -> None:
        """
        Temporarily pause the menu until resume is called.
        """

    def resume(self) -> None:
        """
        Sets the currently active menu to this one and resumes it.
        """

    def join(self, timeout: float | None = None) -> None:
        """
        Should be called at some point after :meth:`start()<consolemenu.ConsoleMenu.start>` to block until
        the menu exits.

        Args:
            timeout (Number): How long to wait before timing out.

        """

    def get_input(self) -> int:
        """
        Can be overridden to change the input method.
        Called in :meth:`process_user_input()<consolemenu.ConsoleMenu.process_user_input>`

        :return: the ordinal value of a single character
        :rtype: int
        """

    def process_user_input(self) -> int | None:
        """
        Gets the next single character and decides what to do with it
        """

    def go_to(self, option: int) -> None:
        """
        Go to the option entered by the user as a number

        :param option: the option to go to
        :type option: int
        """

    def go_down(self) -> None:
        """
        Go down one, wrap to beginning if necessary
        """

    def go_up(self) -> None:
        """
        Go up one, wrap to end if necessary
        """

    def select(self) -> None:
        """
        Select the current item and run it
        """

    def exit(self) -> None:
        """
        Signal the menu to exit, then block until it's done cleaning up
        """

    def clear_screen(self) -> None:
        """
        Clear the screen belonging to this menu
        """

    def get_title(self) -> str: ...
    def get_subtitle(self) -> str: ...
    def get_prologue_text(self) -> str: ...
    def get_epilogue_text(self) -> str: ...

class MenuItem:
    """
    A generic menu item
    """

    text: str
    menu: ConsoleMenu | None
    should_exit: bool
    index_item_separator: str
    menu_char: str | None
    def __init__(
        self,
        text: str | Callable[[], str],
        menu: ConsoleMenu | None = None,
        should_exit: bool = False,
        menu_char: str | None = None,
    ) -> None:
        """
        :ivar str text: The text shown for this menu item
        :ivar ConsoleMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this item's action is done
        :ivar str menu_char: The character used to select this menu item. Optional - defaults to None.
        """

    def show(self, index: int) -> str:
        """
        How this item should be displayed in the menu. Can be overridden, but should keep the same signature.

        Default is:

            1 - Item 1

            2 - Another Item

        :param int index: The index of the item in the items list of the menu
        :return: The representation of the item to be shown in a menu
        :rtype: str
        """

    def set_up(self) -> None:
        """
        Override to add any setup actions necessary for the item
        """

    def action(self) -> None:
        """
        Override to carry out the main action for this item.
        """

    def clean_up(self) -> None:
        """
        Override to add any cleanup actions necessary for the item
        """

    def get_return(self) -> object:
        """
        Override to change what the item returns.
        Otherwise just returns the same value the last selected item did.
        """

    def __eq__(self, o: MenuItem) -> bool: ...  # type: ignore[override]
    def get_text(self) -> str: ...

class ExitItem(MenuItem):
    """
    Used to exit the current menu. Handled by :class:`consolemenu.ConsoleMenu`
    """

    def __init__(
        self, text: str | Callable[[], str] = "Exit", menu: ConsoleMenu | None = None, menu_char: str | None = None
    ) -> None: ...
    def show(self, index: int, available_width: None = None) -> str:
        """
        ExitItem overrides this method to display appropriate Exit or Return text.
        """

def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal: cls on windows, reset otherwise
    """
