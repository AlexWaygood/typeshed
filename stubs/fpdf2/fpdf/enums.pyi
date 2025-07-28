from enum import Enum, Flag, IntEnum, IntFlag
from typing import Literal
from typing_extensions import Self, TypeAlias

from .syntax import Name

class SignatureFlag(IntEnum):
    SIGNATURES_EXIST = 1
    APPEND_ONLY = 2

class CoerciveEnum(Enum):  # type: ignore[misc]  # Enum with no members
    """An enumeration that provides a helper to coerce strings into enumeration members."""

    @classmethod
    def coerce(cls, value: Self | str, case_sensitive: bool = False) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it as an enumeration value. If
        that fails, attempt to convert it (case insensitively, by upcasing) as an
        enumeration name.

        If all different conversion attempts fail, an exception is raised.

        Args:
            value (Enum, str): the value to be coerced.

        Raises:
            ValueError: if `value` is a string but neither a member by name nor value.
            TypeError: if `value`'s type is neither a member of the enumeration nor a
                string.
        """

class CoerciveIntEnum(IntEnum):  # type: ignore[misc]  # Enum with no members
    """
    An enumeration that provides a helper to coerce strings and integers into
    enumeration members.
    """

    @classmethod
    def coerce(cls, value: Self | str | int) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it (case insensitively, by
        upcasing) as an enumeration name. Otherwise, if it is an int, attempt to
        convert it as an enumeration value.

        Otherwise, an exception is raised.

        Args:
            value (IntEnum, str, int): the value to be coerced.

        Raises:
            ValueError: if `value` is an int but not a member of this enumeration.
            ValueError: if `value` is a string but not a member by name.
            TypeError: if `value`'s type is neither a member of the enumeration nor an
                int or a string.
        """

class CoerciveIntFlag(IntFlag):  # type: ignore[misc]  # Enum with no members
    """
    Enumerated constants that can be combined using the bitwise operators,
    with a helper to coerce strings and integers into enumeration members.
    """

    @classmethod
    def coerce(cls, value: Self | str | int) -> Self:
        """
        Attempt to coerce `value` into a member of this enumeration.

        If value is already a member of this enumeration it is returned unchanged.
        Otherwise, if it is a string, attempt to convert it (case insensitively, by
        upcasing) as an enumeration name. Otherwise, if it is an int, attempt to
        convert it as an enumeration value.
        Otherwise, an exception is raised.

        Args:
            value (IntEnum, str, int): the value to be coerced.

        Raises:
            ValueError: if `value` is an int but not a member of this enumeration.
            ValueError: if `value` is a string but not a member by name.
            TypeError: if `value`'s type is neither a member of the enumeration nor an
                int or a string.
        """

class WrapMode(CoerciveEnum):
    """Defines how to break and wrap lines in multi-line text."""

    WORD = "WORD"
    CHAR = "CHAR"

class CharVPos(CoerciveEnum):
    """Defines the vertical position of text relative to the line."""

    SUP = "SUP"
    SUB = "SUB"
    NOM = "NOM"
    DENOM = "DENOM"
    LINE = "LINE"

class Align(CoerciveEnum):
    """Defines how to render text in a cell"""

    C = "CENTER"
    X = "X_CENTER"
    L = "LEFT"
    R = "RIGHT"
    J = "JUSTIFY"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

_Align: TypeAlias = Align | Literal["CENTER", "X_CENTER", "LEFT", "RIGHT", "JUSTIFY"]  # noqa: Y047

class VAlign(CoerciveEnum):
    """Defines how to vertically render text in a cell.
    Default value is MIDDLE
    """

    M = "MIDDLE"
    T = "TOP"
    B = "BOTTOM"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class TextEmphasis(CoerciveIntFlag):
    """
    Indicates use of bold / italics / underline.

    This enum values can be combined with & and | operators:
        style = B | I
    """

    NONE = 0
    B = 1
    I = 2
    U = 4
    S = 8

    @property
    def style(self) -> str: ...
    def add(self, value: TextEmphasis) -> TextEmphasis: ...
    def remove(self, value: TextEmphasis) -> TextEmphasis: ...

class MethodReturnValue(CoerciveIntFlag):
    """
    Defines the return value(s) of a FPDF content-rendering method.

    This enum values can be combined with & and | operators:
        PAGE_BREAK | LINES
    """

    PAGE_BREAK = 1
    LINES = 2
    HEIGHT = 4

class TableBordersLayout(CoerciveEnum):
    """Defines how to render table borders"""

    ALL = "ALL"
    NONE = "NONE"
    INTERNAL = "INTERNAL"
    MINIMAL = "MINIMAL"
    HORIZONTAL_LINES = "HORIZONTAL_LINES"
    NO_HORIZONTAL_LINES = "NO_HORIZONTAL_LINES"
    SINGLE_TOP_LINE = "SINGLE_TOP_LINE"

class CellBordersLayout(CoerciveIntFlag):
    """Defines how to render cell borders in table

    The integer value of `border` determines which borders are applied. Below are some common examples:

    - border=1 (LEFT): Only the left border is enabled.
    - border=3 (LEFT | RIGHT): Both the left and right borders are enabled.
    - border=5 (LEFT | TOP): The left and top borders are enabled.
    - border=12 (TOP | BOTTOM): The top and bottom borders are enabled.
    - border=15 (ALL): All borders (left, right, top, bottom) are enabled.
    - border=16 (INHERIT): Inherit the border settings from the parent element.

    Using `border=3` will combine LEFT and RIGHT borders, as it represents the
    bitwise OR of `LEFT (1)` and `RIGHT (2)`.
    """

    NONE = 0
    LEFT = 1
    RIGHT = 2
    TOP = 4
    BOTTOM = 8
    ALL = 15
    INHERIT = 16

class TableCellFillMode(CoerciveEnum):
    """Defines which table cells to fill"""

    NONE = "NONE"
    ALL = "ALL"
    ROWS = "ROWS"
    COLUMNS = "COLUMNS"
    EVEN_ROWS = "EVEN_ROWS"
    EVEN_COLUMNS = "EVEN_COLUMNS"

    def should_fill_cell(self, i: int, j: int) -> bool: ...
    @classmethod
    def coerce(cls, value: Self | str) -> Self:  # type: ignore[override]
        """Any class that has a .should_fill_cell() method is considered a valid 'TableCellFillMode' (duck-typing)"""

class TableSpan(CoerciveEnum):
    ROW = "ROW"
    COL = "COL"

class TableHeadingsDisplay(CoerciveIntEnum):
    """Defines how the table headings should be displayed"""

    NONE = 0
    ON_TOP_OF_EVERY_PAGE = 1

class RenderStyle(CoerciveEnum):
    """Defines how to render shapes"""

    D = "DRAW"
    F = "FILL"
    DF = "DRAW_FILL"
    @property
    def operator(self) -> str: ...
    @property
    def is_draw(self) -> bool: ...
    @property
    def is_fill(self) -> bool: ...
    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class TextMode(CoerciveIntEnum):
    """Values described in PDF spec section 'Text Rendering Mode'"""

    FILL = 0
    STROKE = 1
    FILL_STROKE = 2
    INVISIBLE = 3
    FILL_CLIP = 4
    STROKE_CLIP = 5
    FILL_STROKE_CLIP = 6
    CLIP = 7

class XPos(CoerciveEnum):
    """Positional values in horizontal direction for use after printing text."""

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    START = "START"
    END = "END"
    WCONT = "WCONT"
    CENTER = "CENTER"
    LMARGIN = "LMARGIN"
    RMARGIN = "RMARGIN"

class YPos(CoerciveEnum):
    """Positional values in vertical direction for use after printing text"""

    TOP = "TOP"
    LAST = "LAST"
    NEXT = "NEXT"
    TMARGIN = "TMARGIN"
    BMARGIN = "BMARGIN"

class Angle(CoerciveIntEnum):
    """Direction values used for mirror transformations specifying the angle of mirror line"""

    NORTH = 90
    EAST = 0
    SOUTH = 270
    WEST = 180
    NORTHEAST = 45
    SOUTHEAST = 315
    SOUTHWEST = 225
    NORTHWEST = 135

class PageLayout(CoerciveEnum):
    """Specify the page layout shall be used when the document is opened"""

    SINGLE_PAGE = Name("SinglePage")
    ONE_COLUMN = Name("OneColumn")
    TWO_COLUMN_LEFT = Name("TwoColumnLeft")
    TWO_COLUMN_RIGHT = Name("TwoColumnRight")
    TWO_PAGE_LEFT = Name("TwoPageLeft")
    TWO_PAGE_RIGHT = Name("TwoPageRight")

class PageMode(CoerciveEnum):
    """Specifying how to display the document on exiting full-screen mode"""

    USE_NONE = Name("UseNone")
    USE_OUTLINES = Name("UseOutlines")
    USE_THUMBS = Name("UseThumbs")
    FULL_SCREEN = Name("FullScreen")
    USE_OC = Name("UseOC")
    USE_ATTACHMENTS = Name("UseAttachments")

class TextMarkupType(CoerciveEnum):
    """Subtype of a text markup annotation"""

    HIGHLIGHT = Name("Highlight")
    UNDERLINE = Name("Underline")
    SQUIGGLY = Name("Squiggly")
    STRIKE_OUT = Name("StrikeOut")

class BlendMode(CoerciveEnum):
    """An enumeration of the named standard named blend functions supported by PDF."""

    NORMAL = Name("Normal")
    MULTIPLY = Name("Multiply")
    SCREEN = Name("Screen")
    OVERLAY = Name("Overlay")
    DARKEN = Name("Darken")
    LIGHTEN = Name("Lighten")
    COLOR_DODGE = Name("ColorDodge")
    COLOR_BURN = Name("ColorBurn")
    HARD_LIGHT = Name("HardLight")
    SOFT_LIGHT = Name("SoftLight")
    DIFFERENCE = Name("Difference")
    EXCLUSION = Name("Exclusion")
    HUE = Name("Hue")
    SATURATION = Name("Saturation")
    COLOR = Name("Color")
    LUMINOSITY = Name("Luminosity")

class AnnotationFlag(CoerciveIntEnum):
    INVISIBLE = 1
    HIDDEN = 2
    PRINT = 4
    NO_ZOOM = 8
    NO_ROTATE = 16
    NO_VIEW = 32
    READ_ONLY = 64
    LOCKED = 128
    TOGGLE_NO_VIEW = 256
    LOCKED_CONTENTS = 512

class AnnotationName(CoerciveEnum):
    """The name of an icon that shall be used in displaying the annotation"""

    NOTE = Name("Note")
    COMMENT = Name("Comment")
    HELP = Name("Help")
    PARAGRAPH = Name("Paragraph")
    NEW_PARAGRAPH = Name("NewParagraph")
    INSERT = Name("Insert")

class FileAttachmentAnnotationName(CoerciveEnum):
    """The name of an icon that shall be used in displaying the annotation"""

    PUSH_PIN = Name("PushPin")
    GRAPH_PUSH_PIN = Name("GraphPushPin")
    PAPERCLIP_TAG = Name("PaperclipTag")

class IntersectionRule(CoerciveEnum):
    """
    An enumeration representing the two possible PDF intersection rules.

    The intersection rule is used by the renderer to determine which points are
    considered to be inside the path and which points are outside the path. This
    primarily affects fill rendering and clipping paths.
    """

    NONZERO = "nonzero"
    EVENODD = "evenodd"

class PathPaintRule(CoerciveEnum):
    """
    An enumeration of the PDF drawing directives that determine how the renderer should
    paint a given path.
    """

    STROKE = "S"
    FILL_NONZERO = "f"
    FILL_EVENODD = "f*"
    STROKE_FILL_NONZERO = "B"
    STROKE_FILL_EVENODD = "B*"
    DONT_PAINT = "n"
    AUTO = "auto"

class ClippingPathIntersectionRule(CoerciveEnum):
    """An enumeration of the PDF drawing directives that define a path as a clipping path."""

    NONZERO = "W"
    EVENODD = "W*"

class StrokeCapStyle(CoerciveIntEnum):
    """
    An enumeration of values defining how the end of a stroke should be rendered.

    This affects the ends of the segments of dashed strokes, as well.
    """

    BUTT = 0
    ROUND = 1
    SQUARE = 2

class StrokeJoinStyle(CoerciveIntEnum):
    """
    An enumeration of values defining how the corner joining two path components should
    be rendered.
    """

    MITER = 0
    ROUND = 1
    BEVEL = 2

class PDFStyleKeys(Enum):
    """An enumeration of the graphics state parameter dictionary keys."""

    FILL_ALPHA = Name("ca")
    BLEND_MODE = Name("BM")
    STROKE_ALPHA = Name("CA")
    STROKE_ADJUSTMENT = Name("SA")
    STROKE_WIDTH = Name("LW")
    STROKE_CAP_STYLE = Name("LC")
    STROKE_JOIN_STYLE = Name("LJ")
    STROKE_MITER_LIMIT = Name("ML")
    STROKE_DASH_PATTERN = Name("D")

class Corner(CoerciveEnum):
    TOP_RIGHT = "TOP_RIGHT"
    TOP_LEFT = "TOP_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"

class FontDescriptorFlags(Flag):
    """An enumeration of the flags for the unsigned 32-bit integer entry in the font descriptor specifying various
    characteristics of the font. Bit positions are numbered from 1 (low-order) to 32 (high-order).
    """

    FIXED_PITCH = 1
    SYMBOLIC = 4
    ITALIC = 64
    FORCE_BOLD = 262144

class AccessPermission(IntFlag):
    """Permission flags will translate as an integer on the encryption dictionary"""

    PRINT_LOW_RES = 4
    MODIFY = 8
    COPY = 16
    ANNOTATION = 32
    FILL_FORMS = 256
    COPY_FOR_ACCESSIBILITY = 512
    ASSEMBLE = 1024
    PRINT_HIGH_RES = 2048
    @classmethod
    def all(cls) -> int:
        """All flags enabled"""

    @classmethod
    def none(cls) -> Literal[0]:
        """All flags disabled"""

class EncryptionMethod(Enum):
    """Algorithm to be used to encrypt the document"""

    NO_ENCRYPTION = 0
    RC4 = 1
    AES_128 = 2
    AES_256 = 3

class TextDirection(CoerciveEnum):
    """Text rendering direction for text shaping"""

    LTR = "LTR"
    RTL = "RTL"
    TTB = "TTB"
    BTT = "BTT"

class OutputIntentSubType(CoerciveEnum):
    """Definition for Output Intent Subtypes"""

    PDFX = "GTS_PDFX"
    PDFA = "GTS_PDFA1"
    ISOPDF = "ISO_PDFE1"

class PageLabelStyle(CoerciveEnum):
    """Style of the page label"""

    NUMBER = "D"
    UPPER_ROMAN = "R"
    LOWER_ROMAN = "r"
    UPPER_LETTER = "A"
    LOWER_LETTER = "a"
    NONE = None

class Duplex(CoerciveEnum):
    """The paper handling option that shall be used when printing the file from the print dialog."""

    SIMPLEX = "Simplex"
    DUPLEX_FLIP_SHORT_EDGE = "DuplexFlipShortEdge"
    DUPLEX_FLIP_LONG_EDGE = "DuplexFlipLongEdge"

class PageBoundaries(CoerciveEnum):
    ART_BOX = "ArtBox"
    BLEED_BOX = "BleedBox"
    CROP_BOX = "CropBox"
    MEDIA_BOX = "MediaBox"
    TRIM_BOX = "TrimBox"

class PageOrientation(CoerciveEnum):
    PORTRAIT = "P"
    LANDSCAPE = "L"

    @classmethod
    def coerce(cls, value: Self | str) -> Self: ...  # type: ignore[override]

class PDFResourceType(Enum):
    EXT_G_STATE = "ExtGState"
    COLOR_SPACE = "ColorSpace"
    PATTERN = "Pattern"
    SHADDING = "Shading"
    X_OBJECT = "XObject"
    FONT = "Font"
    PROC_SET = "ProcSet"
    PROPERTIES = "Properties"
