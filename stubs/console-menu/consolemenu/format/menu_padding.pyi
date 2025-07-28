class MenuPadding:
    """
    Class for menu padding. Padding is the area between the menu border and the content of the menu.

    Args:
        top (int): The top padding.
        left (int):  The left padding.
        bottom (int): The bottom padding.
        right (int): The right padding.
    """

    def __init__(self, top: int = 1, left: int = 2, bottom: int = 1, right: int = 2) -> None: ...
    @property
    def left(self) -> int:
        """
        The left padding.

        Returns:
            int: The left padding.
        """

    @left.setter
    def left(self, left: int) -> None: ...
    @property
    def right(self) -> int:
        """
        The right padding.

        Returns:
            int: The right padding.
        """

    @right.setter
    def right(self, right: int) -> None: ...
    @property
    def top(self) -> int:
        """
        The top padding.

        Returns:
            int: The top padding.
        """

    @top.setter
    def top(self, top: int) -> None: ...
    @property
    def bottom(self) -> int:
        """
        The bottom padding.

        Returns:
            int: The bottom padding.
        """

    @bottom.setter
    def bottom(self, bottom: int) -> None: ...
