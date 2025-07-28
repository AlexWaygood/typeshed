from collections.abc import Generator

from consolemenu.console_menu import MenuItem
from consolemenu.format import MenuBorderStyle, MenuMargins, MenuPadding, MenuStyle as MenuStyle

def ansilen(s: str) -> int:
    """
    Return the length of the string minus any ANSI control codes.
    Args:
        s (string): The input string to check.
    Returns:
        int: The string length.
    """

class Dimension:
    """
    The Dimension class encapsulates the height and width of a component.

    Args:
        width (int): the width of the Dimension, in columns.
        height (int): the height of the Dimension, in rows.
        dimension (Dimension, optional): an existing Dimension from which to duplicate the height and width.
    """

    width: int
    height: int
    def __init__(self, width: int = 0, height: int = 0, dimension: Dimension | None = None) -> None: ...

class MenuComponent:
    """
    Base class for a menu component.

    Args:
        menu_style (:obj:`MenuStyle`): the style for this component.
        max_dimension (:obj:`Dimension`): the maximum Dimension (width x height) for the menu. Defaults to width=80
            and height=40 if not specified.

    Raises:
        TypeError: if menu_style is not a :obj:`MenuStyle`.
    """

    def __init__(self, menu_style: MenuStyle, max_dimension: Dimension | None = None) -> None: ...
    @property
    def max_dimension(self) -> Dimension:
        """
        :obj:`Dimension`: The maximum dimension for the menu.
        """

    @property
    def style(self) -> MenuStyle:
        """
        :obj:`consolemenu.format.MenuStyle`: The style for this component.
        """

    @property
    def margins(self) -> MenuMargins:
        """
        :obj:`consolemenu.format.MenuMargins`: The margins for this component.
        """

    @property
    def padding(self) -> MenuPadding:
        """
        :obj:`consolemenu.format.MenuPadding`: The padding for this component.
        """

    @property
    def border_style(self) -> MenuBorderStyle:
        """
        :obj:`consolemenu.format.MenuBorderStyle`: The border style for this component.
        """

    def calculate_border_width(self) -> int:
        """
        Calculate the width of the menu border. This will be the width of the maximum allowable
        dimensions (usually the screen size), minus the left and right margins and the newline character.
        For example, given a maximum width of 80 characters, with left and right margins both
        set to 1, the border width would be 77 (80 - 1 - 1 - 1 = 77).

        Returns:
            int: the menu border width in columns.
        """

    def calculate_content_width(self) -> int:
        """
        Calculate the width of inner content of the border.  This will be the width of the menu borders,
        minus the left and right padding, and minus the two vertical border characters.
        For example, given a border width of 77, with left and right margins each set to 2, the content
        width would be 71 (77 - 2 - 2 - 2 = 71).

        Returns:
            int: the inner content width in columns.
        """

    def generate(self) -> Generator[str, None, None]:
        """
        Generate this component.

        Yields:
            str: The next string of characters for drawing this component.
        """

    def inner_horizontals(self) -> str:
        """
        The string of inner horizontal border characters of the required length for this component (not including
        the menu margins or verticals).

        Returns:
            str: The inner horizontal characters.
        """

    def inner_horizontal_border(self) -> str:
        """
        The complete inner horizontal border section, including the left and right border verticals.

        Returns:
            str: The complete inner horizontal border.
        """

    def outer_horizontals(self) -> str:
        """
        The string of outer horizontal border characters of the required length for this component (not including
        the menu margins or verticals).

        Returns:
            str: The outer horizontal characters.
        """

    def outer_horizontal_border_bottom(self) -> str:
        """
        The complete outer bottom horizontal border section, including left and right margins.

        Returns:
            str: The bottom menu border.
        """

    def outer_horizontal_border_top(self) -> str:
        """
        The complete outer top horizontal border section, including left and right margins.

        Returns:
            str: The top menu border.
        """

    def row(self, content: str = "", align: str = "left", indent_len: int = 0) -> str:
        """
        A row of the menu, which comprises the left and right verticals plus the given content.
        If the content is larger than the alloted space for a single row, the content is wrapped
        onto multiple lines, while also respecting user-included newline characters.

        Returns:
            str: One or more rows of this menu component with the specified content.
        """

class MenuHeader(MenuComponent):
    """
    The menu header section.
    The menu header contains the top margin, menu top, title/subtitle verticals, bottom padding verticals,
    and optionally a bottom border to separate the header from the next section.
    """

    title: str
    title_align: str
    subtitle: str
    subtitle_align: str
    show_bottom_border: bool
    def __init__(
        self,
        menu_style: MenuStyle,
        max_dimension: Dimension | None = None,
        title: str | None = None,
        title_align: str = "left",
        subtitle: str | None = None,
        subtitle_align: str = "left",
        show_bottom_border: bool = False,
    ) -> None: ...
    def generate(self) -> Generator[str, None, None]: ...

class MenuTextSection(MenuComponent):
    """
    The menu text block section.
    A text block section can be used for displaying text to the user above or below the main items section.
    """

    text: str
    text_align: str
    show_top_border: bool
    show_bottom_border: bool
    def __init__(
        self,
        menu_style: MenuStyle,
        max_dimension: Dimension | None = None,
        text: str | None = None,
        text_align: str = "left",
        show_top_border: bool = False,
        show_bottom_border: bool = False,
    ) -> None: ...
    def generate(self) -> Generator[str, None, None]: ...

class MenuItemsSection(MenuComponent):
    """
    The menu section for displaying the menu items.
    """

    items_align: str
    def __init__(
        self,
        menu_style: MenuStyle,
        max_dimension: Dimension | None = None,
        items: list[MenuItem] | None = None,
        items_align: str = "left",
    ) -> None: ...
    @property
    def items(self) -> list[MenuItem]: ...
    @items.setter
    def items(self, items: list[MenuItem]) -> None: ...
    @property
    def items_with_bottom_border(self) -> list[str]:
        """
        Return a list of the names (the item text property) of all items that should show a bottom border.
        :return: a list of item names that should show a bottom border.
        """

    @property
    def items_with_top_border(self) -> list[str]:
        """
        Return a list of the names (the item text property) of all items that should show a top border.
        :return: a list of item names that should show a top border.
        """

    def show_item_bottom_border(self, item_text: str, flag: bool) -> None:
        """
        Sets a flag that will show a bottom border for an item with the specified text.
        :param item_text: the text property of the item
        :param flag: boolean specifying if the border should be shown.
        """

    def show_item_top_border(self, item_text: str, flag: bool) -> None:
        """
        Sets a flag that will show a top border for an item with the specified text.
        :param item_text: the text property of the item
        :param flag: boolean specifying if the border should be shown.
        """

    def generate(self) -> Generator[str, None, None]: ...

class MenuFooter(MenuComponent):
    """
    The menu footer section.
    The menu footer contains the menu bottom, bottom padding verticals, and bottom margin.
    """

    def generate(self) -> Generator[str, None, None]: ...

class MenuPrompt(MenuComponent):
    """
    A string representing the menu prompt for user input.
    """

    def __init__(self, menu_style: MenuStyle, max_dimension: Dimension | None = None, prompt_string: str = ">>") -> None: ...
    @property
    def prompt(self) -> str: ...
    @prompt.setter
    def prompt(self, prompt: str) -> None: ...
    def generate(self) -> Generator[str, None, None]: ...
