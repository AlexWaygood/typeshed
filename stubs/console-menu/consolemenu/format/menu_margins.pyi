class MenuMargins:
    """
    Class for menu margins. A margin is the area between the maximum specified dimensions (which is usually
    the width and height of the screen) and the menu border.

    Args:
        top (int): The top margin.
        left (int):  The left margin.
        bottom (int): The bottom margin.
        right (int): The right margin.
    """

    def __init__(self, top: int = 1, left: int = 2, bottom: int = 0, right: int = 2) -> None: ...
    @property
    def left(self) -> int:
        """
        The left margin.

        Returns:
            int: The left margin.

        """

    @left.setter
    def left(self, left: int) -> None: ...
    @property
    def right(self) -> int:
        """
        The right margin.

        Returns:
            int: The right margin.
        """

    @right.setter
    def right(self, right: int) -> None: ...
    @property
    def top(self) -> int:
        """
        The top margin.

        Returns:
            int: The top margin.
        """

    @top.setter
    def top(self, top: int) -> None: ...
    @property
    def bottom(self) -> int:
        """
        The bottom margin.

        Returns:
            int: The bottom margin.
        """

    @bottom.setter
    def bottom(self, bottom: int) -> None: ...
