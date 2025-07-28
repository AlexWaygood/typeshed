"""
Utilities to parse SVG graphics into fpdf.drawing objects.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete, Unused
from collections.abc import Callable
from logging import Logger
from re import Pattern
from typing import Literal, NamedTuple, overload

from ._fonttools_shims import BasePen, _TTGlyphSet
from .drawing import ClippingPath, PaintedPath
from .fpdf import FPDF
from .image_datastructures import ImageCache

LOGGER: Logger

__pdoc__: dict[str, bool]

def force_nodocument(item):
    """A decorator that forces pdoc not to document the decorated item (class or method)"""

NUMBER_SPLIT: Pattern[str]
TRANSFORM_GETTER: Pattern[str]

class Percent(float):
    """class to represent percentage values"""

unit_splitter: Pattern[str]
relative_length_units: set[str]
absolute_length_units: dict[str, int]
angle_units: dict[str, float]

def resolve_length(length_str, default_unit: str = "pt"):
    """Convert a length unit to our canonical length unit, pt."""

def resolve_angle(angle_str, default_unit: str = "deg"):
    """Convert an angle value to our canonical angle unit, radians"""

def xmlns(space, name):
    """Create an XML namespace string representation for the given tag name."""

def xmlns_lookup(space, *names):
    """Create a lookup for the given name in the given XML namespace."""

def without_ns(qualified_tag: str) -> str:
    """Remove the xmlns namespace from a qualified XML tag name"""

shape_tags: Incomplete

def svgcolor(colorstr): ...
def convert_stroke_width(incoming): ...
def convert_miterlimit(incoming): ...
def clamp_float(min_val, max_val): ...
def inheritable(value, converter=...): ...
def optional(value, converter=...): ...

svg_attr_map: dict[str, Callable[[Incomplete], tuple[str, Incomplete]]]

def apply_styles(stylable, svg_element) -> None:
    """Apply the known styles from `svg_element` to the pdf path/group `stylable`."""

class ShapeBuilder:
    """A namespace within which methods for converting basic shapes can be looked up."""

    @overload
    @staticmethod
    def new_path(tag, clipping_path: Literal[True]) -> ClippingPath:
        """Create a new path with the appropriate styles."""

    @overload
    @staticmethod
    def new_path(tag, clipping_path: Literal[False] = False) -> PaintedPath: ...
    @overload
    @classmethod
    def rect(cls, tag, clipping_path: Literal[True]) -> ClippingPath:
        """Convert an SVG <rect> into a PDF path."""

    @overload
    @classmethod
    def rect(cls, tag, clipping_path: Literal[False] = False) -> PaintedPath: ...
    @overload
    @classmethod
    def circle(cls, tag, clipping_path: Literal[True]) -> ClippingPath:
        """Convert an SVG <circle> into a PDF path."""

    @overload
    @classmethod
    def circle(cls, tag, clipping_path: Literal[False] = False) -> PaintedPath: ...
    @overload
    @classmethod
    def ellipse(cls, tag, clipping_path: Literal[True]) -> ClippingPath:
        """Convert an SVG <ellipse> into a PDF path."""

    @overload
    @classmethod
    def ellipse(cls, tag, clipping_path: Literal[False] = False) -> PaintedPath: ...
    @classmethod
    def line(cls, tag) -> PaintedPath:
        """Convert an SVG <line> into a PDF path."""

    @classmethod
    def polyline(cls, tag) -> PaintedPath:
        """Convert an SVG <polyline> into a PDF path."""

    @overload
    @classmethod
    def polygon(cls, tag, clipping_path: Literal[True]) -> ClippingPath:
        """Convert an SVG <polygon> into a PDF path."""

    @overload
    @classmethod
    def polygon(cls, tag, clipping_path: Literal[False] = False) -> PaintedPath: ...

def convert_transforms(tfstr):
    """Convert SVG/CSS transform functions into PDF transforms."""

class PathPen(BasePen):
    pdf_path: PaintedPath
    last_was_line_to: bool
    first_is_move: bool | None
    def __init__(self, pdf_path: PaintedPath, glyphSet: _TTGlyphSet | None = ...): ...
    def arcTo(self, rx, ry, rotation, arc, sweep, end) -> None: ...

def svg_path_converter(pdf_path: PaintedPath, svg_path: str) -> None: ...

class SVGObject:
    """
    A representation of an SVG that has been converted to a PDF representation.
    """

    image_cache: ImageCache | None

    @classmethod
    def from_file(cls, filename, *args, encoding: str = "utf-8", **kwargs):
        """
        Create an `SVGObject` from the contents of the file at `filename`.

        Args:
            filename (path-like): the path to a file containing SVG data.
            *args: forwarded directly to the SVGObject initializer. For subclass use.
            encoding (str): optional charset encoding to use when reading the file.
            **kwargs: forwarded directly to the SVGObject initializer. For subclass use.

        Returns:
            A converted `SVGObject`.
        """
    cross_references: Incomplete
    def __init__(self, svg_text, image_cache: ImageCache | None = None) -> None: ...
    preserve_ar: Incomplete
    width: Incomplete
    height: Incomplete
    viewbox: Incomplete
    def update_xref(self, key: str | None, referenced) -> None: ...
    def extract_shape_info(self, root_tag) -> None:
        """Collect shape info from the given SVG."""
    base_group: Incomplete
    def convert_graphics(self, root_tag) -> None:
        """Convert the graphics contained in the SVG into the PDF representation."""

    def transform_to_page_viewport(self, pdf, align_viewbox: bool = True):
        """
        Size the converted SVG paths to the page viewport.

        The SVG document size can be specified relative to the rendering viewport
        (e.g. width=50%). If the converted SVG sizes are relative units, then this
        computes the appropriate scale transform to size the SVG to the correct
        dimensions for a page in the current PDF document.

        If the SVG document size is specified in absolute units, then it is not scaled.

        Args:
            pdf (fpdf.FPDF): the pdf to use the page size of.
            align_viewbox (bool): if True, mimic some of the SVG alignment rules if the
                viewbox aspect ratio does not match that of the viewport.

        Returns:
            The same thing as `SVGObject.transform_to_rect_viewport`.
        """

    def transform_to_rect_viewport(self, scale, width, height, align_viewbox: bool = True, ignore_svg_top_attrs: bool = False):
        """
        Size the converted SVG paths to an arbitrarily sized viewport.

        The SVG document size can be specified relative to the rendering viewport
        (e.g. width=50%). If the converted SVG sizes are relative units, then this
        computes the appropriate scale transform to size the SVG to the correct
        dimensions for a page in the current PDF document.

        Args:
            scale (Number): the scale factor from document units to PDF points.
            width (Number): the width of the viewport to scale to in document units.
            height (Number): the height of the viewport to scale to in document units.
            align_viewbox (bool): if True, mimic some of the SVG alignment rules if the
                viewbox aspect ratio does not match that of the viewport.
            ignore_svg_top_attrs (bool): ignore <svg> top attributes like "width", "height"
                or "preserveAspectRatio" when figuring the image dimensions.
                Require width & height to be provided as parameters.

        Returns:
            A tuple of (width, height, `fpdf.drawing.GraphicsContext`), where width and
            height are the resolved width and height (they may be 0. If 0, the returned
            `fpdf.drawing.GraphicsContext` will be empty). The
            `fpdf.drawing.GraphicsContext` contains all of the paths that were
            converted from the SVG, scaled to the given viewport size.
        """

    def draw_to_page(self, pdf: FPDF, x=None, y=None, debug_stream=None) -> None:
        """
        Directly draw the converted SVG to the given PDF's current page.

        The page viewport is used for sizing the SVG.

        Args:
            pdf (fpdf.FPDF): the document to which the converted SVG is rendered.
            x (Number): abscissa of the converted SVG's top-left corner.
            y (Number): ordinate of the converted SVG's top-left corner.
            debug_stream (io.TextIO): the stream to which rendering debug info will be
                written.
        """

    def handle_defs(self, defs) -> None:
        """Produce lookups for groups and paths inside the <defs> tag"""

    def build_xref(self, xref):
        """Resolve a cross-reference to an already-seen SVG element by ID."""

    def build_group(self, group, pdf_group=None):
        """Handle nested items within a group <g> tag."""

    def build_path(self, path):
        """Convert an SVG <path> tag into a PDF path object."""

    def build_shape(self, shape):
        """Convert an SVG shape tag into a PDF path object. Necessary to make xref (because ShapeBuilder doesn't have access to this object.)"""

    def build_clipping_path(self, shape, clip_id): ...
    def apply_clipping_path(self, stylable, svg_element) -> None: ...
    def build_image(self, image) -> SVGImage: ...

class SVGImage(NamedTuple):
    """SVGImage(href, x, y, width, height, svg_obj)"""

    href: str
    x: float
    y: float
    width: float
    height: float
    svg_obj: SVGObject

    def __deepcopy__(self, _memo: Unused) -> SVGImage: ...
    def render(
        self, _gsd_registry: Unused, _style: Unused, last_item, initial_point
    ) -> tuple[Incomplete, Incomplete, Incomplete]: ...
    def render_debug(
        self, gsd_registry: Unused, style: Unused, last_item, initial_point, debug_stream, _pfx: Unused
    ) -> tuple[Incomplete, Incomplete, Incomplete]: ...
