"""
Vector drawing: managing colors, graphics states, paths, transforms...

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

import decimal
from _typeshed import Incomplete
from collections import OrderedDict
from collections.abc import Callable, Generator, Sequence
from contextlib import contextmanager
from re import Pattern
from typing import Any, ClassVar, Literal, NamedTuple, TypeVar, overload
from typing_extensions import Self, TypeAlias

from .syntax import Name, Raw

__pdoc__: dict[str, bool]

_CallableT = TypeVar("_CallableT", bound=Callable[..., Any])

def force_nodocument(item: _CallableT) -> _CallableT:
    """A decorator that forces pdoc not to document the decorated item (class or method)"""

def force_document(item: _CallableT) -> _CallableT:
    """A decorator that forces pdoc to document the decorated item (class or method)"""

Number: TypeAlias = int | float | decimal.Decimal
NumberClass: tuple[type, ...]
WHITESPACE: frozenset[str]
EOL_CHARS: frozenset[str]
DELIMITERS: frozenset[str]
STR_ESC: Pattern[str]
STR_ESC_MAP: dict[str, str]

class GraphicsStateDictRegistry(OrderedDict[Raw, Name]):
    """
    A container providing deduplication of graphics state dictionaries across a PDF.
    """

    def register_style(self, style: GraphicsStyle) -> Name | None: ...

def number_to_str(number) -> str:
    """
    Convert a decimal number to a minimal string representation (no trailing 0 or .).

    Args:
        number (Number): the number to be converted to a string.

    Returns:
        The number's string representation.
    """

def render_pdf_primitive(primitive) -> Raw:
    """
    Render a Python value as a PDF primitive type.

    Container types (tuples/lists and dicts) are rendered recursively. This supports
    values of the type Name, str, bytes, numbers, booleans, list/tuple, and dict.

    Any custom type can be passed in as long as it provides a `serialize` method that
    takes no arguments and returns a string. The primitive object is returned directly
    if it is an instance of the `Raw` class. Otherwise, The existence of the `serialize`
    method is checked before any other type checking is performed, so, for example, a
    `dict` subclass with a `serialize` method would be converted using its `pdf_repr`
    method rather than the built-in `dict` conversion process.

    Args:
        primitive: the primitive value to convert to its PDF representation.

    Returns:
        Raw-wrapped str of the PDF representation.

    Raises:
        ValueError: if a dictionary key is not a Name.
        TypeError: if `primitive` does not have a known conversion to a PDF
            representation.
    """

class _DeviceRGBBase(NamedTuple):
    r: Number
    g: Number
    b: Number
    a: Number | None

class DeviceRGB(_DeviceRGBBase):
    """A class representing a PDF DeviceRGB color."""

    OPERATOR: ClassVar[str]
    def __new__(cls, r: Number, g: Number, b: Number, a: Number | None = None) -> Self: ...
    @property
    def colors(self) -> tuple[Number, Number, Number]:
        """The color components as a tuple in order `(r, g, b)` with alpha omitted, in range 0-1."""

    @property
    def colors255(self) -> tuple[Number, Number, Number]:
        """The color components as a tuple in order `(r, g, b)` with alpha omitted, in range 0-255."""

    def serialize(self) -> str: ...

class _DeviceGrayBase(NamedTuple):
    g: Number
    a: Number | None

class DeviceGray(_DeviceGrayBase):
    """A class representing a PDF DeviceGray color."""

    OPERATOR: ClassVar[str]
    def __new__(cls, g: Number, a: Number | None = None) -> Self: ...
    @property
    def colors(self) -> tuple[Number, Number, Number]:
        """The color components as a tuple in order (r, g, b) with alpha omitted, in range 0-1."""

    @property
    def colors255(self) -> tuple[Number, Number, Number]:
        """The color components as a tuple in order `(r, g, b)` with alpha omitted, in range 0-255."""

    def serialize(self) -> str: ...

class _DeviceCMYKBase(NamedTuple):
    c: Number
    m: Number
    y: Number
    k: Number
    a: Number | None

class DeviceCMYK(_DeviceCMYKBase):
    """A class representing a PDF DeviceCMYK color."""

    OPERATOR: ClassVar[str]
    def __new__(cls, c: Number, m: Number, y: Number, k: Number, a: Number | None = None) -> Self: ...
    @property
    def colors(self) -> tuple[Number, Number, Number, Number]:
        """The color components as a tuple in order (c, m, y, k) with alpha omitted, in range 0-1."""

    def serialize(self) -> str: ...

def rgb8(r, g, b, a=None) -> DeviceRGB:
    """
    Produce a DeviceRGB color from the given 8-bit RGB values.

    Args:
        r (Number): red color component. Must be in the interval [0, 255].
        g (Number): green color component. Must be in the interval [0, 255].
        b (Number): blue color component. Must be in the interval [0, 255].
        a (Optional[Number]): alpha component. Must be `None` or in the interval
            [0, 255]. 0 is fully transparent, 255 is fully opaque

    Returns:
        DeviceRGB color representation.

    Raises:
        ValueError: if any components are not in their valid interval.
    """

def gray8(g, a=None) -> DeviceGray:
    """
    Produce a DeviceGray color from the given 8-bit gray value.

    Args:
        g (Number): gray color component. Must be in the interval [0, 255]. 0 is black,
            255 is white.
        a (Optional[Number]): alpha component. Must be `None` or in the interval
            [0, 255]. 0 is fully transparent, 255 is fully opaque

    Returns:
        DeviceGray color representation.

    Raises:
        ValueError: if any components are not in their valid interval.
    """

@overload
def convert_to_device_color(r: DeviceCMYK) -> DeviceCMYK: ...
@overload
def convert_to_device_color(r: DeviceGray) -> DeviceGray: ...
@overload
def convert_to_device_color(r: DeviceRGB) -> DeviceRGB: ...
@overload
def convert_to_device_color(r: str) -> DeviceRGB: ...
@overload
def convert_to_device_color(r: int, g: Literal[-1] = -1, b: Literal[-1] = -1) -> DeviceGray: ...
@overload
def convert_to_device_color(r: Sequence[int] | int, g: int, b: int) -> DeviceGray | DeviceRGB: ...
def cmyk8(c, m, y, k, a=None) -> DeviceCMYK:
    """
    Produce a DeviceCMYK color from the given 8-bit CMYK values.

    Args:
        c (Number): red color component. Must be in the interval [0, 255].
        m (Number): green color component. Must be in the interval [0, 255].
        y (Number): blue color component. Must be in the interval [0, 255].
        k (Number): blue color component. Must be in the interval [0, 255].
        a (Optional[Number]): alpha component. Must be `None` or in the interval
            [0, 255]. 0 is fully transparent, 255 is fully opaque

    Returns:
        DeviceCMYK color representation.

    Raises:
        ValueError: if any components are not in their valid interval.
    """

def color_from_hex_string(hexstr) -> DeviceRGB:
    """
    Parse an RGB color from a css-style 8-bit hexadecimal color string.

    Args:
        hexstr (str): of the form `#RGB`, `#RGBA`, `#RRGGBB`, or `#RRGGBBAA` (case
            insensitive). Must include the leading octothorp. Forms omitting the alpha
            field are interpreted as not specifying the opacity, so it will not be
            explicitly set.

            An alpha value of `00` is fully transparent and `FF` is fully opaque.

    Returns:
        DeviceRGB representation of the color.
    """

def color_from_rgb_string(rgbstr) -> DeviceRGB:
    """
    Parse an RGB color from a css-style rgb(R, G, B, A) color string.

    Args:
        rgbstr (str): of the form `rgb(R, G, B)` or `rgb(R, G, B, A)`.

    Returns:
        DeviceRGB representation of the color.
    """

class Point(NamedTuple):
    """
    An x-y coordinate pair within the two-dimensional coordinate frame.
    """

    x: Number
    y: Number
    def render(self):
        """Render the point to the string `"x y"` for emitting to a PDF."""

    def dot(self, other):
        """
        Compute the dot product of two points.

        Args:
            other (Point): the point with which to compute the dot product.

        Returns:
            The scalar result of the dot product computation.

        Raises:
            TypeError: if `other` is not a `Point`.
        """

    def angle(self, other):
        """
        Compute the angle between two points (interpreted as vectors from the origin).

        The return value is in the interval (-pi, pi]. Sign is dependent on ordering,
        with clockwise angle travel considered to be positive due to the orientation of
        the coordinate frame basis vectors (i.e. the angle between `(1, 0)` and `(0, 1)`
        is `+pi/2`, the angle between `(1, 0)` and `(0, -1)` is `-pi/2`, and the angle
        between `(0, -1)` and `(1, 0)` is `+pi/2`).

        Args:
            other (Point): the point to compute the angle sweep toward.

        Returns:
            The scalar angle between the two points **in radians**.

        Raises:
            TypeError: if `other` is not a `Point`.
        """

    def mag(self):
        """
        Compute the Cartesian distance from this point to the origin

        This is the same as computing the magnitude of the vector represented by this
        point.

        Returns:
            The scalar result of the distance computation.
        """

    def __add__(self, other):
        """
        Produce the sum of two points.

        Adding two points is the same as translating the source point by interpreting
        the other point's x and y coordinates as distances.

        Args:
            other (Point): right-hand side of the infix addition operation

        Returns:
            A Point which is the sum of the two source points.
        """

    def __sub__(self, other):
        """
        Produce the difference between two points.

        Unlike addition, this is not a commutative operation!

        Args:
            other (Point): right-hand side of the infix subtraction operation

        Returns:
            A Point which is the difference of the two source points.
        """

    def __neg__(self):
        """
        Produce a point by negating this point's coordinates.

        Returns:
            A Point whose coordinates are this points coordinates negated.
        """

    def __mul__(self, other):
        """
        Multiply a point by a scalar value.

        Args:
            other (Number): the scalar value by which to multiply the point's
                coordinates.

        Returns:
            A Point whose coordinates are the result of the multiplication.
        """

    def __rmul__(self, other):
        """
        Multiply a point by a scalar value.

        Args:
            other (Number): the scalar value by which to multiply the point's
                coordinates.

        Returns:
            A Point whose coordinates are the result of the multiplication.
        """

    def __truediv__(self, other):
        """
        Divide a point by a scalar value.

        .. note::

            Because division is not commutative, `Point / scalar` is implemented, but
            `scalar / Point` is nonsensical and not implemented.

        Args:
            other (Number): the scalar value by which to divide the point's coordinates.

        Returns:
            A Point whose coordinates are the result of the division.
        """

    def __floordiv__(self, other):
        """
        Divide a point by a scalar value using integer division.

        .. note::

            Because division is not commutative, `Point // scalar` is implemented, but
            `scalar // Point` is nonsensical and not implemented.

        Args:
            other (Number): the scalar value by which to divide the point's coordinates.

        Returns:
            A Point whose coordinates are the result of the division.
        """

    def __matmul__(self, other):
        """
        Transform a point with the given transform matrix.

        .. note::
            This operator is only implemented for Transforms. This transform is not
            commutative, so `Point @ Transform` is implemented, but `Transform @ Point`
            is not implemented (technically speaking, the current implementation is
            commutative because of the way points and transforms are represented, but
            if that representation were to change this operation could stop being
            commutative)

        Args:
            other (Transform): the transform to apply to the point

        Returns:
            A Point whose coordinates are the result of applying the transform.
        """

class Transform(NamedTuple):
    """
    A representation of an affine transformation matrix for 2D shapes.

    The actual matrix is:

    ```
                        [ a b 0 ]
    [x' y' 1] = [x y 1] [ c d 0 ]
                        [ e f 1 ]
    ```

    Complex transformation operations can be composed via a sequence of simple
    transformations by performing successive matrix multiplication of the simple
    transformations.

    For example, scaling a set of points around a specific center point can be
    represented by a translation-scale-translation sequence, where the first
    translation translates the center to the origin, the scale transform scales the
    points relative to the origin, and the second translation translates the points
    back to the specified center point. Transform multiplication is performed using
    python's dedicated matrix multiplication operator, `@`

    The semantics of this representation mean composed transformations are specified
    left-to-right in order of application (some other systems provide transposed
    representations, in which case the application order is right-to-left).

    For example, to rotate the square `(1,1) (1,3) (3,3) (3,1)` 45 degrees clockwise
    about its center point (which is `(2,2)`) , the translate-rotate-translate
    process described above may be applied:

    ```python
    rotate_centered = (
        Transform.translation(-2, -2)
        @ Transform.rotation_d(45)
        @ Transform.translation(2, 2)
    )
    ```

    Instances of this class provide a chaining API, so the above transform could also be
    constructed as follows:

    ```python
    rotate_centered = Transform.translation(-2, -2).rotate_d(45).translate(2, 2)
    ```

    Or, because the particular operation of performing some transformations about a
    specific point is pretty common,

    ```python
    rotate_centered = Transform.rotation_d(45).about(2, 2)
    ```

    By convention, this class provides class method constructors following noun-ish
    naming (`translation`, `scaling`, `rotation`, `shearing`) and instance method
    manipulations following verb-ish naming (`translate`, `scale`, `rotate`, `shear`).
    """

    a: Number
    b: Number
    c: Number
    d: Number
    e: Number
    f: Number
    @classmethod
    def identity(cls):
        """
        Create a transform representing the identity transform.

        The identity transform is a no-op.
        """

    @classmethod
    def translation(cls, x, y):
        """
        Create a transform that performs translation.

        Args:
            x (Number): distance to translate points along the x (horizontal) axis.
            y (Number): distance to translate points along the y (vertical) axis.

        Returns:
            A Transform representing the specified translation.
        """

    @classmethod
    def scaling(cls, x, y=None):
        """
        Create a transform that performs scaling.

        Args:
            x (Number): scaling ratio in the x (horizontal) axis. A value of 1
                results in no scale change in the x axis.
            y (Number): optional scaling ratio in the y (vertical) axis. A value of 1
                results in no scale change in the y axis. If this value is omitted, it
                defaults to the value provided to the `x` argument.

        Returns:
            A Transform representing the specified scaling.
        """

    @classmethod
    def rotation(cls, theta):
        """
        Create a transform that performs rotation.

        Args:
            theta (Number): the angle **in radians** by which to rotate. Positive
                values represent clockwise rotations.

        Returns:
            A Transform representing the specified rotation.

        """

    @classmethod
    def rotation_d(cls, theta_d):
        """
        Create a transform that performs rotation **in degrees**.

        Args:
            theta_d (Number): the angle **in degrees** by which to rotate. Positive
                values represent clockwise rotations.

        Returns:
            A Transform representing the specified rotation.

        """

    @classmethod
    def shearing(cls, x, y=None):
        """
        Create a transform that performs shearing (not of sheep).

        Args:
            x (Number): The amount to shear along the x (horizontal) axis.
            y (Number): Optional amount to shear along the y (vertical) axis. If omitted,
                this defaults to the value provided to the `x` argument.

        Returns:
            A Transform representing the specified shearing.

        """

    def translate(self, x, y):
        """
        Produce a transform by composing the current transform with a translation.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            x (Number): distance to translate points along the x (horizontal) axis.
            y (Number): distance to translate points along the y (vertical) axis.

        Returns:
            A Transform representing the composed transform.
        """

    def scale(self, x, y=None):
        """
        Produce a transform by composing the current transform with a scaling.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            x (Number): scaling ratio in the x (horizontal) axis. A value of 1
                results in no scale change in the x axis.
            y (Number): optional scaling ratio in the y (vertical) axis. A value of 1
                results in no scale change in the y axis. If this value is omitted, it
                defaults to the value provided to the `x` argument.

        Returns:
            A Transform representing the composed transform.
        """

    def rotate(self, theta):
        """
        Produce a transform by composing the current transform with a rotation.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            theta (Number): the angle **in radians** by which to rotate. Positive
                values represent clockwise rotations.

        Returns:
            A Transform representing the composed transform.
        """

    def rotate_d(self, theta_d):
        """
        Produce a transform by composing the current transform with a rotation
        **in degrees**.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            theta_d (Number): the angle **in degrees** by which to rotate. Positive
                values represent clockwise rotations.

        Returns:
            A Transform representing the composed transform.
        """

    def shear(self, x, y=None):
        """
        Produce a transform by composing the current transform with a shearing.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            x (Number): The amount to shear along the x (horizontal) axis.
            y (Number): Optional amount to shear along the y (vertical) axis. If omitted,
                this defaults to the value provided to the `x` argument.

        Returns:
            A Transform representing the composed transform.
        """

    def about(self, x, y):
        """
        Bracket the given transform in a pair of translations to make it appear about a
        point that isn't the origin.

        This is a useful shorthand for performing a transform like a rotation around the
        center point of an object that isn't centered at the origin.

        .. note::
            Transforms are immutable, so this returns a new transform rather than
            mutating self.

        Args:
            x (Number): the point along the x (horizontal) axis about which to transform.
            y (Number): the point along the y (vertical) axis about which to transform.

        Returns:
            A Transform representing the composed transform.
        """

    def __mul__(self, other):
        """
        Multiply the individual transform parameters by a scalar value.

        Args:
            other (Number): the scalar value by which to multiply the parameters

        Returns:
            A Transform with the modified parameters.
        """

    def __rmul__(self, other):
        """
        Multiply the individual transform parameters by a scalar value.

        Args:
            other (Number): the scalar value by which to multiply the parameters

        Returns:
            A Transform with the modified parameters.
        """

    def __matmul__(self, other):
        """
        Compose two transforms into a single transform.

        Args:
            other (Transform): the right-hand side transform of the infix operator.

        Returns:
            A Transform representing the composed transform.
        """

    def render(self, last_item):
        """
        Render the transform to its PDF output representation.

        Args:
            last_item: the last path element this transform applies to

        Returns:
            A tuple of `(str, last_item)`. `last_item` is returned unchanged.
        """

class GraphicsStyle:
    """
    A class representing various style attributes that determine drawing appearance.

    This class uses the convention that the global Python singleton ellipsis (`...`) is
    exclusively used to represent values that are inherited from the parent style. This
    is to disambiguate the value None which is used for several values to signal an
    explicitly disabled style. An example of this is the fill/stroke color styles,
    which use None as hints to the auto paint style detection code.
    """

    INHERIT: ClassVar[Incomplete]
    MERGE_PROPERTIES: ClassVar[tuple[str, ...]]
    TRANSPARENCY_KEYS: ClassVar[tuple[Name, ...]]
    PDF_STYLE_KEYS: ClassVar[tuple[Name, ...]]
    @classmethod
    def merge(cls, parent, child):
        """
        Merge parent and child into a single GraphicsStyle.

        The result contains the properties of the parent as overridden by any properties
        explicitly set on the child. If both the parent and the child specify to
        inherit a given property, that property will preserve the inherit value.
        """

    def __init__(self) -> None: ...
    def __deepcopy__(self, memo) -> Self: ...
    @property
    def allow_transparency(self): ...
    @allow_transparency.setter
    def allow_transparency(self, new): ...
    @property
    def paint_rule(self):
        """The paint rule to use for this path/group."""

    @paint_rule.setter
    def paint_rule(self, new) -> None: ...
    @property
    def auto_close(self):
        """If True, unclosed paths will be automatically closed before stroking."""

    @auto_close.setter
    def auto_close(self, new) -> None: ...
    @property
    def intersection_rule(self):
        """The desired intersection rule for this path/group."""

    @intersection_rule.setter
    def intersection_rule(self, new) -> None: ...
    @property
    def fill_color(self):
        """
        The desired fill color for this path/group.

        When setting this property, if the color specifies an opacity value, that will
        be used to set the fill_opacity property as well.
        """

    @fill_color.setter
    def fill_color(self, color) -> None: ...
    @property
    def fill_opacity(self):
        """The desired fill opacity for this path/group."""

    @fill_opacity.setter
    def fill_opacity(self, new) -> None: ...
    @property
    def stroke_color(self):
        """
        The desired stroke color for this path/group.

        When setting this property, if the color specifies an opacity value, that will
        be used to set the fill_opacity property as well.
        """

    @stroke_color.setter
    def stroke_color(self, color) -> None: ...
    @property
    def stroke_opacity(self):
        """The desired stroke opacity for this path/group."""

    @stroke_opacity.setter
    def stroke_opacity(self, new) -> None: ...
    @property
    def blend_mode(self):
        """The desired blend mode for this path/group."""

    @blend_mode.setter
    def blend_mode(self, value) -> None: ...
    @property
    def stroke_width(self):
        """The desired stroke width for this path/group."""

    @stroke_width.setter
    def stroke_width(self, width) -> None: ...
    @property
    def stroke_cap_style(self):
        """The desired stroke cap style for this path/group."""

    @stroke_cap_style.setter
    def stroke_cap_style(self, value) -> None: ...
    @property
    def stroke_join_style(self):
        """The desired stroke join style for this path/group."""

    @stroke_join_style.setter
    def stroke_join_style(self, value) -> None: ...
    @property
    def stroke_miter_limit(self):
        """The desired stroke miter limit for this path/group."""

    @stroke_miter_limit.setter
    def stroke_miter_limit(self, value) -> None: ...
    @property
    def stroke_dash_pattern(self):
        """The desired stroke dash pattern for this path/group."""

    @stroke_dash_pattern.setter
    def stroke_dash_pattern(self, value) -> None: ...
    @property
    def stroke_dash_phase(self):
        """The desired stroke dash pattern phase offset for this path/group."""

    @stroke_dash_phase.setter
    def stroke_dash_phase(self, value): ...
    def serialize(self) -> Raw | None:
        """
        Convert this style object to a PDF dictionary with appropriate style keys.

        Only explicitly specified values are emitted.
        """

    def resolve_paint_rule(self):
        """
        Resolve `PathPaintRule.AUTO` to a real paint rule based on this style.

        Returns:
            the resolved `PathPaintRule`.
        """

class Move(NamedTuple):
    """
    A path move element.

    If a path has been created but not yet painted, this will create a new subpath.

    See: `PaintedPath.move_to`
    """

    pt: Point
    @property
    def end_point(self):
        """The end point of this path element."""

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is `self`
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Move.render`.
        """

class RelativeMove(NamedTuple):
    """
    A path move element with an end point relative to the end of the previous path
    element.

    If a path has been created but not yet painted, this will create a new subpath.

    See: `PaintedPath.move_relative`
    """

    pt: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Move`
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeMove.render`.
        """

class Line(NamedTuple):
    """
    A path line element.

    This draws a straight line from the end point of the previous path element to the
    point specified by `pt`.

    See: `PaintedPath.line_to`
    """

    pt: Point
    @property
    def end_point(self):
        """The end point of this path element."""

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is `self`
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Line.render`.
        """

class RelativeLine(NamedTuple):
    """
    A path line element with an endpoint relative to the end of the previous element.

    This draws a straight line from the end point of the previous path element to the
    point specified by `last_item.end_point + pt`. The absolute coordinates of the end
    point are resolved during the rendering process.

    See: `PaintedPath.line_relative`
    """

    pt: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeLine.render`.
        """

class HorizontalLine(NamedTuple):
    """
    A path line element that takes its ordinate from the end of the previous element.

    See: `PaintedPath.horizontal_line_to`
    """

    x: Number
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `HorizontalLine.render`.
        """

class RelativeHorizontalLine(NamedTuple):
    """
    A path line element that takes its ordinate from the end of the previous element and
    computes its abscissa offset from the end of that element.

    See: `PaintedPath.horizontal_line_relative`
    """

    x: Number
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeHorizontalLine.render`.
        """

class VerticalLine(NamedTuple):
    """
    A path line element that takes its abscissa from the end of the previous element.

    See: `PaintedPath.vertical_line_to`
    """

    y: Number
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `VerticalLine.render`.
        """

class RelativeVerticalLine(NamedTuple):
    """
    A path line element that takes its abscissa from the end of the previous element and
    computes its ordinate offset from the end of that element.

    See: `PaintedPath.vertical_line_relative`
    """

    y: Number
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeVerticalLine.render`.
        """

class BezierCurve(NamedTuple):
    """
    A cubic Bézier curve path element.

    This draws a Bézier curve parameterized by the end point of the previous path
    element, two off-curve control points, and an end point.

    See: `PaintedPath.curve_to`
    """

    c1: Point
    c2: Point
    end: Point
    @property
    def end_point(self):
        """The end point of this path element."""

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is `self`
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `BezierCurve.render`.
        """

class RelativeBezierCurve(NamedTuple):
    """
    A cubic Bézier curve path element whose points are specified relative to the end
    point of the previous path element.

    See: `PaintedPath.curve_relative`
    """

    c1: Point
    c2: Point
    end: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `BezierCurve`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeBezierCurve.render`.
        """

class QuadraticBezierCurve(NamedTuple):
    """
    A quadratic Bézier curve path element.

    This draws a Bézier curve parameterized by the end point of the previous path
    element, one off-curve control point, and an end point.

    See: `PaintedPath.quadratic_curve_to`
    """

    ctrl: Point
    end: Point
    @property
    def end_point(self):
        """The end point of this path element."""

    def to_cubic_curve(self, start_point): ...
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is `self`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `QuadraticBezierCurve.render`.
        """

class RelativeQuadraticBezierCurve(NamedTuple):
    """
    A quadratic Bézier curve path element whose points are specified relative to the end
    point of the previous path element.

    See: `PaintedPath.quadratic_curve_relative`
    """

    ctrl: Point
    end: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is the resolved
            `QuadraticBezierCurve`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeQuadraticBezierCurve.render`.
        """

class Arc(NamedTuple):
    """
    An elliptical arc path element.

    The arc is drawn from the end of the current path element to its specified end point
    using a number of parameters to determine how it is constructed.

    See: `PaintedPath.arc_to`
    """

    radii: Point
    rotation: Number
    large: bool
    sweep: bool
    end: Point
    @staticmethod
    def subdivde_sweep(sweep_angle) -> Generator[Incomplete, None, None]:
        """
        A generator that subdivides a swept angle into segments no larger than a quarter
        turn.

        Any sweep that is larger than a quarter turn is subdivided into as many equally
        sized segments as necessary to prevent any individual segment from being larger
        than a quarter turn.

        This is used for approximating a circular curve segment using cubic Bézier
        curves. This computes the parameters used for the Bézier approximation up
        front, as well as the transform necessary to place the segment in the correct
        position.

        Args:
            sweep_angle (Number): the angle to subdivide.

        Yields:
            A tuple of (ctrl1, ctrl2, end) representing the control and end points of
            the cubic Bézier curve approximating the segment as a unit circle centered
            at the origin.
        """

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is a resolved
            `BezierCurve`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Arc.render`.
        """

class RelativeArc(NamedTuple):
    """
    An elliptical arc path element.

    The arc is drawn from the end of the current path element to its specified end point
    using a number of parameters to determine how it is constructed.

    See: `PaintedPath.arc_relative`
    """

    radii: Point
    rotation: Number
    large: bool
    sweep: bool
    end: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is a resolved
            `BezierCurve`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RelativeArc.render`.
        """

class Rectangle(NamedTuple):
    """A pdf primitive rectangle."""

    org: Point
    size: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is a `Line` back to
            the rectangle's origin.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Rectangle.render`.
        """

class RoundedRectangle(NamedTuple):
    """
    A rectangle with rounded corners.

    See: `PaintedPath.rectangle`
    """

    org: Point
    size: Point
    corner_radii: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is a resolved
            `Line`.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `RoundedRectangle.render`.
        """

class Ellipse(NamedTuple):
    """
    An ellipse.

    See: `PaintedPath.ellipse`
    """

    radii: Point
    center: Point
    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is a resolved
            `Move` to the center of the ellipse.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Ellipse.render`.
        """

class ImplicitClose(NamedTuple):
    """
    A path close element that is conditionally rendered depending on the value of
    `GraphicsStyle.auto_close`.
    """

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is whatever the old
            last_item was.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `ImplicitClose.render`.
        """

class Close(NamedTuple):
    """
    A path close element.

    Instructs the renderer to draw a straight line from the end of the last path element
    to the start of the current path.

    See: `PaintedPath.close`
    """

    def render(self, gsd_registry, style, last_item, initial_point):
        """
        Render this path element to its PDF representation.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command

        Returns:
            a tuple of `(str, new_last_item)`, where `new_last_item` is whatever the old
            last_item was.
        """

    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `Close.render`.
        """

class DrawingContext:
    """
    Base context for a drawing in a PDF

    This context is not stylable and is mainly responsible for transforming path
    drawing coordinates into user coordinates (i.e. it ensures that the output drawing
    is correctly scaled).
    """

    def __init__(self) -> None: ...
    def add_item(self, item, _copy: bool = True) -> None:
        """
        Append an item to this drawing context

        Args:
            item (GraphicsContext, PaintedPath): the item to be appended.
            _copy (bool): if true (the default), the item will be copied before being
                appended. This prevents modifications to a referenced object from
                "retroactively" altering its style/shape and should be disabled with
                caution.
        """

    def render(self, gsd_registry, first_point, scale, height, starting_style):
        """
        Render the drawing context to PDF format.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the parent document's graphics
                state registry.
            first_point (Point): the starting point to use if the first path element is
                a relative element.
            scale (Number): the scale factor to convert from PDF pt units into the
                document's semantic units (e.g. mm or in).
            height (Number): the page height. This is used to remap the coordinates to
                be from the top-left corner of the page (matching fpdf's behavior)
                instead of the PDF native behavior of bottom-left.
            starting_style (GraphicsStyle): the base style for this drawing context,
                derived from the document's current style defaults.

        Returns:
            A string composed of the PDF representation of all the paths and groups in
            this context (an empty string is returned if there are no paths or groups)
        """

    def render_debug(self, gsd_registry, first_point, scale, height, starting_style, debug_stream):
        """
        Render the drawing context to PDF format.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the parent document's graphics
                state registry.
            first_point (Point): the starting point to use if the first path element is
                a relative element.
            scale (Number): the scale factor to convert from PDF pt units into the
                document's semantic units (e.g. mm or in).
            height (Number): the page height. This is used to remap the coordinates to
                be from the top-left corner of the page (matching fpdf's behavior)
                instead of the PDF native behavior of bottom-left.
            starting_style (GraphicsStyle): the base style for this drawing context,
                derived from the document's current style defaults.
            debug_stream (TextIO): a text stream to which a debug representation of the
                drawing structure will be written.

        Returns:
            A string composed of the PDF representation of all the paths and groups in
            this context (an empty string is returned if there are no paths or groups)
        """

class PaintedPath:
    """
    A path to be drawn by the PDF renderer.

    A painted path is defined by a style and an arbitrary sequence of path elements,
    which include the primitive path elements (`Move`, `Line`, `BezierCurve`, ...) as
    well as arbitrarily nested `GraphicsContext` containing their own sequence of
    primitive path elements and `GraphicsContext`.
    """

    def __init__(self, x: int = 0, y: int = 0) -> None: ...
    def __deepcopy__(self, memo) -> Self: ...
    @property
    def style(self):
        """The `GraphicsStyle` applied to all elements of this path."""

    @property
    def transform(self):
        """The `Transform` that applies to all of the elements of this path."""

    @transform.setter
    def transform(self, tf) -> None: ...
    @property
    def auto_close(self):
        """If true, the path should automatically close itself before painting."""

    @auto_close.setter
    def auto_close(self, should) -> None: ...
    @property
    def paint_rule(self):
        """Manually specify the `PathPaintRule` to use for rendering the path."""

    @paint_rule.setter
    def paint_rule(self, style) -> None: ...
    @property
    def clipping_path(self):
        """Set the clipping path for this path."""

    @clipping_path.setter
    def clipping_path(self, new_clipath) -> None: ...
    @contextmanager
    def transform_group(self, transform) -> Generator[Self]:
        """
        Apply the provided `Transform` to all points added within this context.
        """

    def add_path_element(self, item, _copy: bool = True) -> None:
        """
        Add the given element as a path item of this path.

        Args:
            item: the item to add to this path.
            _copy (bool): if true (the default), the item will be copied before being
                appended. This prevents modifications to a referenced object from
                "retroactively" altering its style/shape and should be disabled with
                caution.
        """

    def remove_last_path_element(self) -> None: ...
    def rectangle(self, x, y, w, h, rx: int = 0, ry: int = 0) -> Self:
        """
        Append a rectangle as a closed subpath to the current path.

        If the width or the height are 0, the rectangle will be collapsed to a line
        (unless they're both 0, in which case it's collapsed to nothing).

        Args:
            x (Number): the abscissa of the starting corner of the rectangle.
            y (Number): the ordinate of the starting corner of the rectangle.
            w (Number): the width of the rectangle (if 0, the rectangle will be
                rendered as a vertical line).
            h (Number): the height of the rectangle (if 0, the rectangle will be
                rendered as a horizontal line).
            rx (Number): the x-radius of the rectangle rounded corner (if 0 the corners
                will not be rounded).
            ry (Number): the y-radius of the rectangle rounded corner (if 0 the corners
                will not be rounded).

        Returns:
            The path, to allow chaining method calls.
        """

    def circle(self, cx, cy, r) -> Self:
        """
        Append a circle as a closed subpath to the current path.

        Args:
            cx (Number): the abscissa of the circle's center point.
            cy (Number): the ordinate of the circle's center point.
            r (Number): the radius of the circle.

        Returns:
            The path, to allow chaining method calls.
        """

    def ellipse(self, cx, cy, rx, ry) -> Self:
        """
        Append an ellipse as a closed subpath to the current path.

        Args:
            cx (Number): the abscissa of the ellipse's center point.
            cy (Number): the ordinate of the ellipse's center point.
            rx (Number): the x-radius of the ellipse.
            ry (Number): the y-radius of the ellipse.

        Returns:
            The path, to allow chaining method calls.
        """

    def move_to(self, x, y) -> Self:
        """
        Start a new subpath or move the path starting point.

        If no path elements have been added yet, this will change the path starting
        point. If path elements have been added, this will insert an implicit close in
        order to start a new subpath.

        Args:
            x (Number): abscissa of the (sub)path starting point.
            y (Number): ordinate of the (sub)path starting point.

        Returns:
            The path, to allow chaining method calls.
        """

    def move_relative(self, x, y) -> Self:
        """
        Start a new subpath or move the path start point relative to the previous point.

        If no path elements have been added yet, this will change the path starting
        point. If path elements have been added, this will insert an implicit close in
        order to start a new subpath.

        This will overwrite an absolute move_to as long as no non-move path items have
        been appended. The relative position is resolved from the previous item when
        the path is being rendered, or from 0, 0 if it is the first item.

        Args:
            x (Number): abscissa of the (sub)path starting point relative to the.
            y (Number): ordinate of the (sub)path starting point relative to the.
        """

    def line_to(self, x, y) -> Self:
        """
        Append a straight line to this path.

        Args:
            x (Number): abscissa the line's end point.
            y (Number): ordinate of the line's end point.

        Returns:
            The path, to allow chaining method calls.
        """

    def line_relative(self, dx, dy) -> Self:
        """
        Append a straight line whose end is computed as an offset from the end of the
        previous path element.

        Args:
            x (Number): abscissa the line's end point relative to the end point of the
                previous path element.
            y (Number): ordinate of the line's end point relative to the end point of
                the previous path element.

        Returns:
            The path, to allow chaining method calls.
        """

    def horizontal_line_to(self, x) -> Self:
        """
        Append a straight horizontal line to the given abscissa. The ordinate is
        retrieved from the end point of the previous path element.

        Args:
            x (Number): abscissa of the line's end point.

        Returns:
            The path, to allow chaining method calls.
        """

    def horizontal_line_relative(self, dx) -> Self:
        """
        Append a straight horizontal line to the given offset from the previous path
        element. The ordinate is retrieved from the end point of the previous path
        element.

        Args:
            x (Number): abscissa of the line's end point relative to the end point of
                the previous path element.

        Returns:
            The path, to allow chaining method calls.
        """

    def vertical_line_to(self, y) -> Self:
        """
        Append a straight vertical line to the given ordinate. The abscissa is
        retrieved from the end point of the previous path element.

        Args:
            y (Number): ordinate of the line's end point.

        Returns:
            The path, to allow chaining method calls.
        """

    def vertical_line_relative(self, dy) -> Self:
        """
        Append a straight vertical line to the given offset from the previous path
        element. The abscissa is retrieved from the end point of the previous path
        element.

        Args:
            y (Number): ordinate of the line's end point relative to the end point of
                the previous path element.

        Returns:
            The path, to allow chaining method calls.
        """

    def curve_to(self, x1, y1, x2, y2, x3, y3) -> Self:
        """
        Append a cubic Bézier curve to this path.

        Args:
            x1 (Number): abscissa of the first control point
            y1 (Number): ordinate of the first control point
            x2 (Number): abscissa of the second control point
            y2 (Number): ordinate of the second control point
            x3 (Number): abscissa of the end point
            y3 (Number): ordinate of the end point

        Returns:
            The path, to allow chaining method calls.
        """

    def curve_relative(self, dx1, dy1, dx2, dy2, dx3, dy3) -> Self:
        """
        Append a cubic Bézier curve whose points are expressed relative to the
        end point of the previous path element.

        E.g. with a start point of (0, 0), given (1, 1), (2, 2), (3, 3), the output
        curve would have the points:

        (0, 0) c1 (1, 1) c2 (3, 3) e (6, 6)

        Args:
            dx1 (Number): abscissa of the first control point relative to the end point
                of the previous path element
            dy1 (Number): ordinate of the first control point relative to the end point
                of the previous path element
            dx2 (Number): abscissa offset of the second control point relative to the
                end point of the previous path element
            dy2 (Number): ordinate offset of the second control point relative to the
                end point of the previous path element
            dx3 (Number): abscissa offset of the end point relative to the end point of
                the previous path element
            dy3 (Number): ordinate offset of the end point relative to the end point of
                the previous path element

        Returns:
            The path, to allow chaining method calls.
        """

    def quadratic_curve_to(self, x1, y1, x2, y2) -> Self:
        """
        Append a cubic Bézier curve mimicking the specified quadratic Bézier curve.

        Args:
            x1 (Number): abscissa of the control point
            y1 (Number): ordinate of the control point
            x2 (Number): abscissa of the end point
            y2 (Number): ordinate of the end point

        Returns:
            The path, to allow chaining method calls.
        """

    def quadratic_curve_relative(self, dx1, dy1, dx2, dy2) -> Self:
        """
        Append a cubic Bézier curve mimicking the specified quadratic Bézier curve.

        Args:
            dx1 (Number): abscissa of the control point relative to the end point of
                the previous path element
            dy1 (Number): ordinate of the control point relative to the end point of
                the previous path element
            dx2 (Number): abscissa offset of the end point relative to the end point of
                the previous path element
            dy2 (Number): ordinate offset of the end point relative to the end point of
                the previous path element

        Returns:
            The path, to allow chaining method calls.
        """

    def arc_to(self, rx, ry, rotation, large_arc, positive_sweep, x, y) -> Self:
        """
        Append an elliptical arc from the end of the previous path point to the
        specified end point.

        The arc is approximated using Bézier curves, so it is not perfectly accurate.
        However, the error is small enough to not be noticeable at any reasonable
        (and even most unreasonable) scales, with a worst-case deviation of around 3‱.

        Notes:
            - The signs of the radii arguments (`rx` and `ry`) are ignored (i.e. their
              absolute values are used instead).
            - If either radius is 0, then a straight line will be emitted instead of an
              arc.
            - If the radii are too small for the arc to reach from the current point to
              the specified end point (`x` and `y`), then they will be proportionally
              scaled up until they are big enough, which will always result in a
              half-ellipse arc (i.e. an 180 degree sweep)

        Args:
            rx (Number): radius in the x-direction.
            ry (Number): radius in the y-direction.
            rotation (Number): angle (in degrees) that the arc should be rotated
                clockwise from the principle axes. This parameter does not have
                a visual effect in the case that `rx == ry`.
            large_arc (bool): if True, the arc will cover a sweep angle of at least 180
                degrees. Otherwise, the sweep angle will be at most 180 degrees.
            positive_sweep (bool): if True, the arc will be swept over a positive angle,
                i.e. clockwise. Otherwise, the arc will be swept over a negative
                angle.
            x (Number): abscissa of the arc's end point.
            y (Number): ordinate of the arc's end point.
        """

    def arc_relative(self, rx, ry, rotation, large_arc, positive_sweep, dx, dy) -> Self:
        """
        Append an elliptical arc from the end of the previous path point to an offset
        point.

        The arc is approximated using Bézier curves, so it is not perfectly accurate.
        However, the error is small enough to not be noticeable at any reasonable
        (and even most unreasonable) scales, with a worst-case deviation of around 3‱.

        Notes:
            - The signs of the radii arguments (`rx` and `ry`) are ignored (i.e. their
              absolute values are used instead).
            - If either radius is 0, then a straight line will be emitted instead of an
              arc.
            - If the radii are too small for the arc to reach from the current point to
              the specified end point (`x` and `y`), then they will be proportionally
              scaled up until they are big enough, which will always result in a
              half-ellipse arc (i.e. an 180 degree sweep)

        Args:
            rx (Number): radius in the x-direction.
            ry (Number): radius in the y-direction.
            rotation (Number): angle (in degrees) that the arc should be rotated
                clockwise from the principle axes. This parameter does not have
                a visual effect in the case that `rx == ry`.
            large_arc (bool): if True, the arc will cover a sweep angle of at least 180
                degrees. Otherwise, the sweep angle will be at most 180 degrees.
            positive_sweep (bool): if True, the arc will be swept over a positive angle,
                i.e. clockwise. Otherwise, the arc will be swept over a negative
                angle.
            dx (Number): abscissa of the arc's end point relative to the end point of
                the previous path element.
            dy (Number): ordinate of the arc's end point relative to the end point of
                the previous path element.
        """

    def close(self) -> None:
        """
        Explicitly close the current (sub)path.
        """

    def render(self, gsd_registry, style, last_item, initial_point, debug_stream=None, pfx=None): ...
    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `PaintedPath.render`.
        """

class ClippingPath(PaintedPath):
    """
    The PaintedPath API but to be used to create clipping paths.

    .. warning::
        Unless you really know what you're doing, changing attributes of the clipping
        path style is likely to produce unexpected results. This is because the
        clipping path styles override implicit style inheritance of the `PaintedPath`
        it applies to.

        For example, `clippath.style.stroke_width = 2` can unexpectedly override
        `paintpath.style.stroke_width = GraphicsStyle.INHERIT` and cause the painted
        path to be rendered with a stroke of 2 instead of what it would have normally
        inherited. Because a `ClippingPath` can be painted like a normal `PaintedPath`,
        it would be overly restrictive to remove the ability to style it, so instead
        this warning is here.
    """

    paint_rule: Incomplete
    def __init__(self, x: int = 0, y: int = 0) -> None: ...
    def render(self, gsd_registry, style, last_item, initial_point, debug_stream=None, pfx=None): ...
    def render_debug(self, gsd_registry, style, last_item, initial_point, debug_stream, pfx):
        """
        Render this path element to its PDF representation and produce debug
        information.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).

        Returns:
            The same tuple as `ClippingPath.render`.
        """

class GraphicsContext:
    style: GraphicsStyle
    path_items: list[Incomplete]
    def __init__(self) -> None: ...
    def __deepcopy__(self, memo) -> Self: ...
    @property
    def transform(self) -> Transform | None: ...
    @transform.setter
    def transform(self, tf) -> None: ...
    @property
    def clipping_path(self) -> ClippingPath | None:
        """The `ClippingPath` for this graphics context."""

    @clipping_path.setter
    def clipping_path(self, new_clipath) -> None: ...
    def add_item(self, item, _copy: bool = True) -> None:
        """
        Add a path element to this graphics context.

        Args:
            item: the path element to add. May be a primitive element or another
                `GraphicsContext` or a `PaintedPath`.
            _copy (bool): if true (the default), the item will be copied before being
                appended. This prevents modifications to a referenced object from
                "retroactively" altering its style/shape and should be disabled with
                caution.
        """

    def remove_last_item(self) -> None: ...
    def merge(self, other_context) -> None:
        """Copy another `GraphicsContext`'s path items into this one."""

    def build_render_list(
        self, gsd_registry, style, last_item, initial_point, debug_stream=None, pfx=None, _push_stack: bool = True
    ):
        """
        Build a list composed of all all the individual elements rendered.

        This is used by `PaintedPath` and `ClippingPath` to reuse the `GraphicsContext`
        rendering process while still being able to inject some path specific items
        (e.g. the painting directive) before the render is collapsed into a single
        string.

        Args:
            gsd_registry (GraphicsStateDictRegistry): the owner's graphics state
                dictionary registry.
            style (GraphicsStyle): the current resolved graphics style
            last_item: the previous path element.
            initial_point: last position set by a "M" or "m" command
            debug_stream (io.TextIO): the stream to which the debug output should be
                written. This is not guaranteed to be seekable (e.g. it may be stdout or
                stderr).
            pfx (str): the current debug output prefix string (only needed if emitting
                more than one line).
            _push_stack (bool): if True, wrap the resulting render list in a push/pop
                graphics stack directive pair.

        Returns:
            `tuple[list[str], last_item]` where `last_item` is the past path element in
            this `GraphicsContext`
        """

    def render(
        self, gsd_registry, style: DrawingContext, last_item, initial_point, debug_stream=None, pfx=None, _push_stack: bool = True
    ): ...
    def render_debug(
        self, gsd_registry, style: DrawingContext, last_item, initial_point, debug_stream, pfx, _push_stack: bool = True
    ): ...
