import logging

class MenuBorderStyle:
    """
    Base class for console menu border. Each property should be overridden by a subclass.
    """

    @property
    def bottom_left_corner(self) -> str:
        """The outer, bottom left corner of the menu."""

    @property
    def bottom_right_corner(self) -> str:
        """The outer, bottom right corner of the menu."""

    @property
    def inner_horizontal(self) -> str:
        """The character for inner horizontal section lines."""

    @property
    def inner_vertical(self) -> str:
        """The character for inner vertical section lines."""

    @property
    def intersection(self) -> str:
        """The character for intersecting inner vertical and inner horizontal lines (a "+" shape)."""

    @property
    def outer_horizontal(self) -> str:
        """The character for outer, horizontal lines (the top and bottom lines of the menu)."""

    @property
    def outer_horizontal_inner_down(self) -> str:
        """The character for a top horizontal line with a downward inner line (a "T" shape)."""

    @property
    def outer_horizontal_inner_up(self) -> str:
        """The character for a bottom horizontal line with an upward inner line (an inverted "T" shape)."""

    @property
    def outer_vertical(self) -> str:
        """The character for an outer vertical line of the menu (the left and right sides of the menu)."""

    @property
    def outer_vertical_inner_left(self) -> str:
        """The character for an outer vertical line, with a protruding inner line to the left."""

    @property
    def outer_vertical_inner_right(self) -> str:
        """The character for an outer vertical line, with a protruding inner line to the right."""

    @property
    def top_left_corner(self) -> str:
        """The top left corner of the menu."""

    @property
    def top_right_corner(self) -> str:
        """The top right corner of the menu."""

class AsciiBorderStyle(MenuBorderStyle):
    """
    A Menu Border Style using only ASCII characters.
    """

    @property
    def bottom_left_corner(self) -> str: ...
    @property
    def bottom_right_corner(self) -> str: ...
    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...
    @property
    def top_left_corner(self) -> str: ...
    @property
    def top_right_corner(self) -> str: ...

class LightBorderStyle(MenuBorderStyle):
    """
    MenuBorderStyle class using Unicode "light" box drawing characters.
    """

    @property
    def bottom_left_corner(self) -> str: ...
    @property
    def bottom_right_corner(self) -> str: ...
    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...
    @property
    def top_left_corner(self) -> str: ...
    @property
    def top_right_corner(self) -> str: ...

class HeavyBorderStyle(MenuBorderStyle):
    """
    MenuBorderStyle class using Unicode "heavy" box drawing characters.
    """

    @property
    def bottom_left_corner(self) -> str: ...
    @property
    def bottom_right_corner(self) -> str: ...
    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...
    @property
    def top_left_corner(self) -> str: ...
    @property
    def top_right_corner(self) -> str: ...

class HeavyOuterLightInnerBorderStyle(HeavyBorderStyle):
    """
    MenuBorderStyle class using Unicode "heavy" box drawing characters for the outer borders, and
    "light" box drawing characters for the inner borders.
    """

    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...

class DoubleLineBorderStyle(MenuBorderStyle):
    """
    MenuBorderStyle class using "double-line" box drawing characters.
    """

    @property
    def bottom_left_corner(self) -> str: ...
    @property
    def bottom_right_corner(self) -> str: ...
    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...
    @property
    def top_left_corner(self) -> str: ...
    @property
    def top_right_corner(self) -> str: ...

class DoubleLineOuterLightInnerBorderStyle(DoubleLineBorderStyle):
    """
    MenuBorderStyle class using Unicode "double-line" box drawing characters for the outer borders, and
    "light" box drawing characters for the inner borders.
    """

    @property
    def inner_horizontal(self) -> str: ...
    @property
    def inner_vertical(self) -> str: ...
    @property
    def intersection(self) -> str: ...
    @property
    def outer_horizontal_inner_down(self) -> str: ...
    @property
    def outer_horizontal_inner_up(self) -> str: ...
    @property
    def outer_vertical_inner_left(self) -> str: ...
    @property
    def outer_vertical_inner_right(self) -> str: ...

class MenuBorderStyleType:
    """
    Defines the various menu border styles, as expected by the border factory.
    """

    ASCII_BORDER: int
    LIGHT_BORDER: int
    HEAVY_BORDER: int
    DOUBLE_LINE_BORDER: int
    HEAVY_OUTER_LIGHT_INNER_BORDER: int
    DOUBLE_LINE_OUTER_LIGHT_INNER_BORDER: int

class MenuBorderStyleFactory:
    """
    Factory class for creating  MenuBorderStyle instances.
    """

    logger: logging.Logger
    def __init__(self) -> None: ...
    def create_border(self, border_style_type: MenuBorderStyleType) -> MenuBorderStyle:
        """
        Create a new MenuBorderStyle instance based on the given border style type.

        Args:
            border_style_type (int):  an integer value from :obj:`MenuBorderStyleType`.

        Returns:
            :obj:`MenuBorderStyle`: a new MenuBorderStyle instance of the specified style.

        """

    def create_ascii_border(self) -> AsciiBorderStyle:
        """
        Create an ASCII border style.

        Returns:
            :obj:`AsciiBorderStyle`:  a new instance of AsciiBorderStyle.
        """

    def create_light_border(self) -> LightBorderStyle:
        """
        Create a border style using "light" box drawing characters.

        Returns:
            :obj:`LightBorderStyle`: a new instance of LightBorderStyle
        """

    def create_heavy_border(self) -> HeavyBorderStyle:
        """
        Create a border style using "heavy" box drawing characters.

        NOTE: The Heavy border style will work on Windows ONLY when using Python 3.6 or later. If on Windows and
        using an earlier version of Python, the heavy border will be substituted with the DOUBLE_LINE_BORDER.

        Returns:
            :obj:`HeavyBorderStyle` or :obj:`DoubleLineBorderStyle`: a new instance of HeavyBorderStyle, unless on
            Windows and pre-Python 3.5, in which case a new instance of DoubleLineBorderStyle will be returned.
        """

    def create_heavy_outer_light_inner_border(self) -> HeavyOuterLightInnerBorderStyle:
        """
        Create a border style using "heavy" box drawing characters for outer border elements, and "light"
        box drawing characters for inner border elements.

        NOTE: The Heavy border style will work on Windows ONLY when using Python 3.6 or later. If on Windows and
        using an earlier version of Python, the heavy border will be substituted with the DOUBLE_LINE_BORDER.

        Returns:
            :obj:`HeavyOuterLightInnerBorderStyle` or :obj:`DoubleLineOuterLightInnerBorderStyle`: a new instance of
            HeavyOuterLightInnerBorderStyle, unless on Windows and pre-Python 3.5, in which case a new instance of
            DoubleLineOuterLightInnerBorderStyle will be returned.
        """

    def create_doubleline_border(self) -> DoubleLineBorderStyle:
        """
        Create a border style using "double-line" box drawing characters.

        Returns:
            :obj:`DoubleLineBorderStyle`: a new instance of DoubleLineBorderStyle.
        """

    def create_doubleline_outer_light_inner_border(self) -> DoubleLineOuterLightInnerBorderStyle:
        """
        Create a border style using "double-line" box drawing characters for outer border elements, and "light"
        box drawing characters for inner border elements.

        Returns:
            :obj:`DoubleLineOuterLightInnerBorderStyle`: a new instance of DoubleLineOuterLightInnerBorderStyle
        """

    @staticmethod
    def is_win_python35_or_earlier() -> bool:
        """
        Convenience method to determine if the current platform is Windows and Python version 3.5 or earlier.

        Returns:
            bool: True if the current platform is Windows and the Python interpreter is 3.5 or earlier; False otherwise.

        """
