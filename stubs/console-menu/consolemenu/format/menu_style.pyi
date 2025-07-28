from consolemenu.format.menu_borders import MenuBorderStyle as MenuBorderStyle, MenuBorderStyleFactory as MenuBorderStyleFactory
from consolemenu.format.menu_margins import MenuMargins as MenuMargins
from consolemenu.format.menu_padding import MenuPadding as MenuPadding

class MenuStyle:
    """
    Class for specifying all menu styling, such as margins, padding, and border style.

    Args:
        margins (:obj:`MenuMargins`): The menu margin settings.
        padding (:obj:`MenuPadding`): The menu padding.
        border_style (:obj:MenuBorderStyle`): The menu border style. Takes precedence over `border_style_type` if both
            are specified.
        border_style_type (int): The border style type as defined by :obj:`MenuBorderStyleType`.
        border_style_factory (:obj:`MenuBorderStyleFactory`): The factory instance to use to create the borders.
    """

    def __init__(
        self,
        margins: MenuMargins | None = None,
        padding: MenuPadding | None = None,
        border_style: MenuBorderStyle | None = None,
        border_style_type: int | None = None,
        border_style_factory: MenuBorderStyleFactory | None = None,
    ) -> None: ...
    @property
    def margins(self) -> MenuMargins:
        """
        The margins instance.

        Returns:
            :obj:`MenuMargins`: The MenuMargins instance.
        """

    @margins.setter
    def margins(self, margins: MenuMargins) -> None: ...
    @property
    def padding(self) -> MenuPadding:
        """
        The padding instance.

        Returns:
            :obj:`MenuPadding`: The MenuPadding instance.
        """

    @padding.setter
    def padding(self, padding: MenuPadding) -> None: ...
    @property
    def border_style(self) -> MenuBorderStyle:
        """
        The border style instance.

        Returns:
            :obj:`MenuBorderStyle`: The MenuBorderStyle instance.
        """

    @border_style.setter
    def border_style(self, border_style: MenuBorderStyle) -> None: ...
    @property
    def border_style_factory(self) -> MenuBorderStyleFactory:
        """
        The border style factory instance.

        Returns:
            :obj:`MenuBorderStyleFactory`: The MenuBorderStyleFactory instance.

        """

    @border_style_factory.setter
    def border_style_factory(self, border_style_factory: MenuBorderStyleFactory) -> None: ...
