from _typeshed import Incomplete
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from consolemenu.console_menu import ConsoleMenu
from consolemenu.items import ExternalItem as ExternalItem

class FunctionItem(ExternalItem):
    """
    A menu item to call a Python function
    """

    function: Callable[..., Any]
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
    return_value: Incomplete | None
    def __init__(
        self,
        text: str,
        function: Callable[..., Any],
        args: Sequence[Any] | None = None,
        kwargs: Mapping[str, Any] | None = None,
        menu: ConsoleMenu | None = None,
        should_exit: bool = False,
        menu_char: str | None = None,
    ) -> None:
        """
        :ivar str text: The text shown for this menu item
        :ivar function: The function to be called
        :ivar list args: An optional list of arguments to be passed to the function
        :ivar dict kwargs: An optional dictionary of keyword arguments to be passed to the function
        :ivar ConsoleMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this item's action is done
        :ivar str menu_char: The character used to select this menu item. Optional - defaults to None.
        """

    def action(self) -> None:
        """
        This class overrides this method
        """

    def clean_up(self) -> None:
        """
        This class overrides this method
        """

    def get_return(self) -> Any | None:
        """
        :return: The return value from the function call
        """
