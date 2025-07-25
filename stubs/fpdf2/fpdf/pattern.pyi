"""
Handles the creation of patterns and gradients
"""

from _typeshed import Incomplete
from abc import ABC
from collections.abc import Iterable
from typing import Final, Literal

from .drawing import DeviceCMYK, DeviceGray, DeviceRGB
from .fpdf import FPDF
from .syntax import Name, PDFObject

class Pattern(PDFObject):
    """
    Represents a PDF Pattern object.

    Currently, this class supports only "shading patterns" (pattern_type 2),
    using either a linear or radial gradient. Tiling patterns (pattern_type 1)
    are not yet implemented.
    """

    type: Name
    pattern_type: int
    def __init__(self, shading: LinearGradient | RadialGradient) -> None: ...
    @property
    def shading(self) -> str: ...

class Type2Function(PDFObject):
    """Transition between 2 colors"""

    function_type: Final = 2
    domain: str
    c0: str
    c1: str
    n: int
    def __init__(self, color_1, color_2) -> None: ...

class Type3Function(PDFObject):
    """When multiple colors are used, a type 3 function is necessary to stitch type 2 functions together
    and define the bounds between each color transition
    """

    function_type: Final = 3
    domain: str
    bounds: str
    encode: str
    n: int

    def __init__(self, functions: Iterable[Incomplete], bounds: Iterable[Incomplete]) -> None: ...
    @property
    def functions(self) -> str: ...

class Shading(PDFObject):
    shading_type: Literal[2, 3]
    background: str | None
    color_space: Name
    coords: list[int]
    function: str
    extend: str
    def __init__(
        self,
        shading_type: Literal[2, 3],
        background: DeviceRGB | DeviceGray | DeviceCMYK | None,
        color_space: str,
        coords: list[int],
        function: Type2Function | Type3Function,
        extend_before: bool,
        extend_after: bool,
    ) -> None: ...

class Gradient(ABC):
    color_space: str
    colors: list[Incomplete]
    background: Incomplete | None
    extend_before: Incomplete
    extend_after: Incomplete
    bounds: Incomplete
    functions: Incomplete
    pattern: Pattern
    coords: Incomplete | None
    shading_type: int

    def __init__(self, colors, background, extend_before, extend_after, bounds): ...
    def get_shading_object(self) -> Shading: ...
    def get_pattern(self) -> Pattern: ...

class LinearGradient(Gradient):
    coords: list[str]
    shading_type: int
    def __init__(
        self,
        fpdf: FPDF,
        from_x: float,
        from_y: float,
        to_x: float,
        to_y: float,
        colors: list[Incomplete],
        background=None,
        extend_before: bool = False,
        extend_after: bool = False,
        bounds: list[int] | None = None,
    ) -> None:
        """
        A shading pattern that creates a linear (axial) gradient in a PDF.

        The gradient is defined by two points: (from_x, from_y) and (to_x, to_y),
        along which the specified colors are interpolated. Optionally, you can set
        a background color, extend the gradient beyond its start or end, and
        specify custom color stop positions via `bounds`.

        Args:
            fpdf (FPDF): The FPDF instance used for PDF generation.
            from_x (int or float): The x-coordinate of the starting point of the gradient,
                in user space units.
            from_y (int or float): The y-coordinate of the starting point of the gradient,
                in user space units.
            to_x (int or float): The x-coordinate of the ending point of the gradient,
                in user space units.
            to_y (int or float): The y-coordinate of the ending point of the gradient,
                in user space units.
            colors (List[str or Tuple[int, int, int]]): A list of colors along which the gradient
                will be interpolated. Colors may be given as hex strings (e.g., "#FF0000") or
                (R, G, B) tuples.
            background (str or Tuple[int, int, int], optional): A background color to use
                if the gradient does not fully cover the region it is applied to.
                Defaults to None (no background).
            extend_before (bool, optional): Whether to extend the first color beyond the
                starting point (from_x, from_y). Defaults to False.
            extend_after (bool, optional): Whether to extend the last color beyond the
                ending point (to_x, to_y). Defaults to False.
            bounds (List[float], optional): An optional list of floats in the range (0, 1)
                that represent gradient stops for color transitions. The number of bounds
                should be two less than the number of colors (for multi-color gradients).
                Defaults to None, which evenly distributes color stops.
        """

class RadialGradient(Gradient):
    coords: list[str]
    shading_type: int
    def __init__(
        self,
        fpdf: FPDF,
        start_circle_x: float,
        start_circle_y: float,
        start_circle_radius: float,
        end_circle_x: float,
        end_circle_y: float,
        end_circle_radius: float,
        colors: list[Incomplete],
        background=None,
        extend_before: bool = False,
        extend_after: bool = False,
        bounds: list[int] | None = None,
    ):
        """
        A shading pattern that creates a radial (or circular/elliptical) gradient in a PDF.

        The gradient is defined by two circles (start and end). Colors are blended from the
        start circle to the end circle, forming a radial gradient. You can optionally set a
        background color, extend the gradient beyond its circles, and provide custom color
        stop positions via `bounds`.

        Args:
            fpdf (FPDF): The FPDF instance used for PDF generation.
            start_circle_x (int or float): The x-coordinate of the inner circle's center,
                in user space units.
            start_circle_y (int or float): The y-coordinate of the inner circle's center,
                in user space units.
            start_circle_radius (int or float): The radius of the inner circle, in user space units.
            end_circle_x (int or float): The x-coordinate of the outer circle's center,
                in user space units.
            end_circle_y (int or float): The y-coordinate of the outer circle's center,
                in user space units.
            end_circle_radius (int or float): The radius of the outer circle, in user space units.
            colors (List[str or Tuple[int, int, int]]): A list of colors along which the gradient
                will be interpolated. Colors may be given as hex strings (e.g., "#FF0000") or
                (R, G, B) tuples.
            background (str or Tuple[int, int, int], optional): A background color to display
                if the gradient does not fully cover the region it's applied to. Defaults to None
                (no background).
            extend_before (bool, optional): Whether to extend the gradient beyond the start circle.
                Defaults to False.
            extend_after (bool, optional): Whether to extend the gradient beyond the end circle.
                Defaults to False.
            bounds (List[float], optional): An optional list of floats in the range (0, 1) that
                represent gradient stops for color transitions. The number of bounds should be one
                less than the number of colors (for multi-color gradients). Defaults to None,
                which evenly distributes color stops.
        """
