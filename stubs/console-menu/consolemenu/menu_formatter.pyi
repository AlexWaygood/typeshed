from consolemenu.console_menu import MenuItem
from consolemenu.format import MenuBorderStyleType
from consolemenu.format.menu_borders import MenuBorderStyle as MenuBorderStyle, MenuBorderStyleFactory as MenuBorderStyleFactory
from consolemenu.format.menu_style import MenuStyle as MenuStyle
from consolemenu.menu_component import (
    Dimension as Dimension,
    MenuFooter as MenuFooter,
    MenuHeader as MenuHeader,
    MenuItemsSection as MenuItemsSection,
    MenuPrompt as MenuPrompt,
    MenuTextSection as MenuTextSection,
)

class MenuFormatBuilder:
    """
    Builder class for generating the menu format.
    """

    def __init__(self, max_dimension: Dimension | None = None) -> None: ...
    def set_border_style(self, border_style: MenuBorderStyle) -> MenuFormatBuilder:
        """
        Set the border style using the specified MenuBorderStyle instance.
        :param border_style: the instance of MenuBorderStyle to use for border style formatting.
        """

    def set_border_style_type(self, border_style_type: MenuBorderStyleType) -> MenuFormatBuilder:
        """
        Set the border style using the specified border style type. The border style type should be an
        integer value recognized by the border style factory for this formatter instance.
        The built-in border style types are provided by the `MenuBorderStyleType` class, or custom
        border style types can be provided if using a custom border style factory.
        :param border_style_type: an integer value representing the border style type.
        """

    def set_border_style_factory(self, border_style_factory: MenuBorderStyleFactory) -> MenuFormatBuilder:
        """
        Set the instance of MenuBorderStyleFactory to use for generating border styles.
        Typically, this method will never need to be used, unless the default MenuBorderStyleFactory
        has been subclassed to provide custom border styles.
        :param border_style_factory: an instance of MenuBorderStyleFactory.
        """

    def set_bottom_margin(self, bottom_margin: int) -> MenuFormatBuilder:
        """
        Set the bottom margin of the menu. This will determine the number of console lines appear between the
        bottom of the menu border and the menu input prompt.
        :param bottom_margin: an integer value
        """

    def set_left_margin(self, left_margin: int) -> MenuFormatBuilder:
        """
        Set the left margin of the menu.  This will determine the number of spaces between the left edge of the
        screen and the left menu border.
        :param left_margin: an integer value
        """

    def set_right_margin(self, right_margin: int) -> MenuFormatBuilder:
        """
        Set the right margin of the menu.  This will determine the number of spaces between the right edge of the
        screen and the right menu border.
        :param right_margin: an integer value
        """

    def set_top_margin(self, top_margin: int) -> MenuFormatBuilder:
        """
        Set the top margin of the menu.  This will determine the number of console lines between the top edge
        of the screen and the top menu border.
        :param top_margin: an integer value
        """

    def set_title_align(self, align: str = "left") -> MenuFormatBuilder: ...
    def set_subtitle_align(self, align: str = "left") -> MenuFormatBuilder: ...
    def set_header_left_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_header_right_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_header_bottom_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_header_top_padding(self, x: int) -> MenuFormatBuilder: ...
    def show_header_bottom_border(self, flag: bool) -> MenuFormatBuilder: ...
    def set_footer_left_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_footer_right_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_footer_bottom_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_footer_top_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_items_left_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_items_right_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_items_bottom_padding(self, x: int) -> MenuFormatBuilder: ...
    def set_items_top_padding(self, x: int) -> MenuFormatBuilder: ...
    def show_item_bottom_border(self, item_text: str, flag: bool) -> MenuFormatBuilder: ...
    def show_item_top_border(self, item_text: str, flag: bool) -> MenuFormatBuilder: ...
    def set_prologue_text_align(self, align: str = "left") -> MenuFormatBuilder: ...
    def show_prologue_top_border(self, flag: bool) -> MenuFormatBuilder: ...
    def show_prologue_bottom_border(self, flag: bool) -> MenuFormatBuilder: ...
    def set_epilogue_text_align(self, align: str = "left") -> MenuFormatBuilder: ...
    def show_epilogue_top_border(self, flag: bool) -> MenuFormatBuilder: ...
    def show_epilogue_bottom_border(self, flag: bool) -> MenuFormatBuilder: ...
    def set_prompt(self, prompt: MenuPrompt) -> MenuFormatBuilder: ...
    def clear_data(self) -> None:
        """
        Clear menu data from previous menu generation.
        """

    def format(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        prologue_text: str | None = None,
        epilogue_text: str | None = None,
        items: list[MenuItem] | None = None,
    ) -> str:
        """
        Format the menu and return as a string.
        :return:  a string representation of the formatted menu.
        """
