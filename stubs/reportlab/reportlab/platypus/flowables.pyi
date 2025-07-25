"""
A flowable is a "floating element" in a document whose exact position is determined by the
other elements that precede it, such as a paragraph, a diagram interspersed between paragraphs,
a section header, etcetera.  Examples of non-flowables include page numbering annotations,
headers, footers, fixed diagrams or logos, among others.

Flowables are defined here as objects which know how to determine their size and which
can draw themselves onto a page with respect to a relative "origin" position determined
at a higher level. The object's draw() method should assume that (0,0) corresponds to the
bottom left corner of the enclosing rectangle that will contain the object. The attributes
vAlign and hAlign may be used by 'packers' as hints as to how the object should be placed.

Some Flowables also know how to "split themselves".  For example a
long paragraph might split itself between one page and the next.

Packers should set the canv attribute during wrap, split & draw operations to allow
the flowable to work out sizes etc in the proper context.

The "text" of a document usually consists mainly of a sequence of flowables which
flow into a document from top to bottom (with column and page breaks controlled by
higher level components).
"""

from _typeshed import Incomplete, SupportsRead, Unused
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Literal, NoReturn, Protocol
from typing_extensions import Self, TypeAlias

from reportlab.lib.colors import Color
from reportlab.lib.styles import ListStyle, ParagraphStyle, PropertySet
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen.textobject import _Color
from reportlab.platypus.paragraph import Paragraph

__all__ = [
    "AnchorFlowable",
    "BalancedColumns",
    "BulletDrawer",
    "CallerMacro",
    "CondPageBreak",
    "DDIndenter",
    "DocAssert",
    "DocAssign",
    "DocExec",
    "DocIf",
    "DocPara",
    "DocWhile",
    "FailOnDraw",
    "FailOnWrap",
    "Flowable",
    "FrameBG",
    "FrameSplitter",
    "HRFlowable",
    "Image",
    "ImageAndFlowables",
    "KeepInFrame",
    "KeepTogether",
    "LIIndenter",
    "ListFlowable",
    "ListItem",
    "Macro",
    "NullDraw",
    "PTOContainer",
    "PageBreak",
    "PageBreakIfNotEmpty",
    "ParagraphAndImage",
    "Preformatted",
    "SetPageTopFlowables",
    "SetTopFlowables",
    "SlowPageBreak",
    "Spacer",
    "TopPadder",
    "TraceInfo",
    "UseUpSpace",
    "XBox",
    "splitLine",
    "splitLines",
    "PlacedStory",
]

_HAlignment: TypeAlias = Literal["LEFT", "CENTER", "CENTRE", "RIGHT", 0, 1, 2]
_VAlignment: TypeAlias = Literal["BOTTOM", "MIDDLE", "TOP"]
# FIXME: Consider using Sequence[Flowable] for covariance on list, even though
#        that will give false negatives for non list or tuple sequences, it also
#        would reduce type safety, since flowables don't copy the list
_FlowableSublist: TypeAlias = Flowable | list[Flowable] | tuple[Flowable, ...]
# NOTE: Technically can only be list or tuple, but would be annoying for variance
_NestedFlowable: TypeAlias = Flowable | Sequence[_NestedFlowable]

class _StyledFlowableFactory(Protocol):
    # NOTE: We leave style at Any so people can specify a specifc property set
    def __call__(self, value: str, /, *, style: Any) -> Flowable: ...

class TraceInfo:
    """Holder for info about where an object originated"""

    srcFile: str
    startLineNo: int
    startLinePos: int
    endLineNo: int
    endLinePos: int
    def __init__(self) -> None: ...

class Flowable:
    """Abstract base class for things to be drawn.  Key concepts:

    1. It knows its size
    2. It draws in its own coordinate system (this requires the
       base API to provide a translate() function.

    """

    width: float
    height: float
    wrapped: int
    hAlign: _HAlignment
    vAlign: _VAlignment
    encoding: str | None
    # NOTE: this only exists during drawing, splitting and wrapping
    canv: Canvas
    # NOTE: The following attributes will not exist on all flowables, but
    #       they need to be settable on individual instances
    keepWithNext: Incomplete
    spaceAfter: float
    spaceBefore: float
    def __init__(self) -> None: ...
    # NOTE: We pretend the optional internal _sW argument does not exist
    #       since not all flowables support it and we'd have to deal with
    #       a bunch of LSP errors. Conversely we will get type errors in
    #       subclasses that rely on the argument existing when called through
    #       super() inside their own implementation, so we can't really
    #       make everyone happy here, sigh...
    def drawOn(self, canvas: Canvas, x: float, y: float) -> None:
        """Tell it to draw itself on the canvas.  Do not override"""

    def wrapOn(self, canv: Canvas, aW: float, aH: float) -> tuple[float, float]:
        """intended for use by packers allows setting the canvas on
        during the actual wrap
        """

    def wrap(self, aW: float, aH: float) -> tuple[float, float]:
        """This will be called by the enclosing frame before objects
        are asked their size, drawn or whatever.  It returns the
        size actually used.
        """

    def minWidth(self) -> float:
        """This should return the minimum required width"""

    def splitOn(self, canv: Canvas, aW: float, aH: float) -> list[Flowable]:
        """intended for use by packers allows setting the canvas on
        during the actual split
        """

    def split(self, aW: float, aH: float, /) -> list[Flowable]:
        """This will be called by more sophisticated frames when
        wrap fails. Stupid flowables should return []. Clever flowables
        should split themselves and return a list of flowables.
        If they decide that nothing useful can be fitted in the
        available space (e.g. if you have a table and not enough
        space for the first row), also return []
        """

    def getKeepWithNext(self):
        """returns boolean determining whether the next flowable should stay with this one"""

    def getSpaceAfter(self) -> float:
        """returns how much space should follow this item if another item follows on the same page."""

    def getSpaceBefore(self) -> float:
        """returns how much space should precede this item if another item precedess on the same page."""

    def isIndexing(self) -> int:
        """Hook for IndexingFlowables - things which have cross references"""

    def identity(self, maxLen: int | None = None) -> str:
        """
        This method should attempt to return a string that can be used to identify
        a particular flowable uniquely. The result can then be used for debugging
        and or error printouts
        """

class XBox(Flowable):
    """Example flowable - a box with an x through it and a caption.
    This has a known size, so does not need to respond to wrap().
    """

    text: str
    def __init__(self, width: float, height: float, text: str = "A Box") -> None: ...
    def draw(self) -> None: ...

def splitLines(lines, maximum_length, split_characters, new_line_characters): ...
def splitLine(line_to_split, lines_splitted, maximum_length, split_characters, new_line_characters) -> None: ...

class Preformatted(Flowable):
    """This is like the HTML <PRE> tag.
    It attempts to display text exactly as you typed it in a fixed width "typewriter" font.
    By default the line breaks are exactly where you put them, and it will not be wrapped.
    You can optionally define a maximum line length and the code will be wrapped; and
    extra characters to be inserted at the beginning of each wrapped line (e.g. '> ').
    """

    style: ParagraphStyle
    bulletText: str | None
    lines: list[str]
    def __init__(
        self,
        text: str,
        # NOTE: Technically has to be a ParagraphStyle, but that would
        #       conflict with stylesheet["Style"] usage
        style: PropertySet,
        bulletText: str | None = None,
        dedent: int = 0,
        maxLineLength: int | None = None,
        splitChars: str | None = None,
        newLineChars: str = "",
    ) -> None:
        """text is the text to display. If dedent is set then common leading space
        will be chopped off the front (for example if the entire text is indented
        6 spaces or more then each line will have 6 spaces removed from the front).
        """

    def draw(self) -> None: ...

class Image(Flowable):
    """an image (digital picture).  Formats supported by PIL/Java 1.4 (the Python/Java Imaging Library
    are supported. Images as flowables may be aligned horizontally in the
    frame with the hAlign parameter - accepted values are 'CENTER',
    'LEFT' or 'RIGHT' with 'CENTER' being the default.
    We allow for two kinds of lazyness to allow for many images in a document
    which could lead to file handle starvation.
    lazy=1 don't open image until required.
    lazy=2 open image when required then shut it.
    """

    filename: str
    # these are lazy, but __getattr__ ensures the image gets loaded
    # as soon as these attributes are accessed
    imageWidth: int
    imageHeight: int
    drawWidth: float
    drawHeight: float
    def __init__(
        self,
        # TODO: I think this might also accept a PIL.Image and other
        #       kinds of path represenations, should be kept in sync
        #       with reportlab.lib.utils.ImageReader, except for the
        #       potential PIL.Image shortcut
        filename: str | SupportsRead[bytes] | Incomplete,
        width: float | None = None,
        height: float | None = None,
        kind: str = "direct",
        mask: str = "auto",
        lazy: int = 1,
        hAlign: _HAlignment = "CENTER",
        useDPI: bool = False,
    ) -> None:
        """If size to draw at not specified, get it from the image."""

    def draw(self) -> None: ...

class NullDraw(Flowable):
    def draw(self) -> None: ...

class Spacer(NullDraw):
    """A spacer just takes up space and doesn't draw anything - it guarantees
    a gap between objects.
    """

    # NOTE: This may actually be a bug, it seems likely that Spacer is meant
    #       to set spaceBefore in the isGlue case.
    spacebefore: float
    def __init__(self, width: float, height: float, isGlue: bool = False) -> None: ...

class UseUpSpace(NullDraw): ...

class PageBreak(UseUpSpace):
    locChanger: int
    nextTemplate: str | None
    def __init__(self, nextTemplate: str | None = None) -> None: ...

class SlowPageBreak(PageBreak): ...
class PageBreakIfNotEmpty(PageBreak): ...

class CondPageBreak(Spacer):
    locChanger: int
    def __init__(self, height: float) -> None: ...

class _ContainerSpace:
    def getSpaceBefore(self) -> float: ...
    def getSpaceAfter(self) -> float: ...

class KeepTogether(_ContainerSpace, Flowable):
    splitAtTop: bool
    # TODO: Consider using Sequence[Flowable] for covariance, even if reportlab
    #       only supports list/tuple
    def __init__(self, flowables: _FlowableSublist | None, maxHeight=None) -> None: ...

class KeepTogetherSplitAtTop(KeepTogether):
    """
    Same as KeepTogether, but it will split content immediately if it cannot
    fit at the top of a frame.
    """

    splitAtTop: bool

class Macro(Flowable):
    """This is not actually drawn (i.e. it has zero height)
    but is executed when it would fit in the frame.  Allows direct
    access to the canvas through the object 'canvas'
    """

    command: str
    def __init__(self, command: str) -> None: ...
    def draw(self) -> None: ...

class CallerMacro(Flowable):
    """
    like Macro, but with callable command(s)
    drawCallable(self)
    wrapCallable(self,aW,aH)
    """

    def __init__(
        self,
        drawCallable: Callable[[CallerMacro, float, float], object] | None = None,
        wrapCallable: Callable[[CallerMacro, float, float], object] | None = None,
    ) -> None: ...
    def draw(self) -> None: ...

class ParagraphAndImage(Flowable):
    """combine a Paragraph and an Image"""

    P: Paragraph
    I: Image
    xpad: float
    ypad: float
    def __init__(self, P: Paragraph, I: Image, xpad: float = 3, ypad: float = 3, side: str = "right") -> None: ...
    def draw(self) -> None: ...

class FailOnWrap(NullDraw):
    def wrap(self, aW: float, aH: float) -> NoReturn: ...

class FailOnDraw(Flowable):
    def draw(self) -> NoReturn: ...

class HRFlowable(Flowable):
    """Like the hr tag"""

    width: float | str  # type: ignore[assignment]
    lineWidth: float
    lineCap: str
    color: _Color
    dash: Incomplete | None
    def __init__(
        self,
        width: float | str = "80%",
        thickness: float = 1,
        lineCap: str = "round",
        color: _Color = ...,
        spaceBefore: float = 1,
        spaceAfter: float = 1,
        hAlign: _HAlignment = "CENTER",
        vAlign: _VAlignment = "BOTTOM",
        dash=None,
    ) -> None: ...
    def draw(self) -> None: ...

class _Container(_ContainerSpace):
    def drawOn(self, canv: Canvas, x: float, y: float) -> None:
        """we simulate being added to a frame"""

    def copyContent(self, content: _FlowableSublist | None = None) -> None: ...

class PTOContainer(_Container, Flowable):
    """PTOContainer(contentList,trailerList,headerList)

    A container for flowables decorated with trailer & header lists.
    If the split operation would be called then the trailer and header
    lists are injected before and after the split. This allows specialist
    "please turn over" and "continued from previous" like behaviours.
    """

    def __init__(
        self, content: _FlowableSublist | None, trailer: _FlowableSublist | None = None, header: _FlowableSublist | None = None
    ) -> None: ...

class KeepInFrame(_Container, Flowable):
    name: str
    maxWidth: float
    maxHeight: float
    mode: Literal["error", "continue", "shrink", "truncate"]
    mergespace: Incomplete | None
    fakeWidth: bool | None
    def __init__(
        self,
        maxWidth: float,
        maxHeight: float,
        content: list[Flowable] = [],
        mergeSpace: Incomplete | None = 1,
        mode: Literal["error", "continue", "shrink", "truncate"] = "shrink",
        name: str = "",
        hAlign: str = "LEFT",
        vAlign: str = "BOTTOM",
        fakeWidth: bool | None = None,
    ) -> None:
        """mode describes the action to take when overflowing
        error       raise an error in the normal way
        continue    ignore ie just draw it and report maxWidth, maxHeight
        shrink      shrinkToFit
        truncate    fit as much as possible
        set fakeWidth to False to make _listWrapOn do the 'right' thing
        """

class PlacedStory(Flowable):
    def __init__(
        self,
        x,
        y,
        maxWidth: float,
        maxHeight: float,
        content: list[Flowable] = [],
        mergeSpace: Incomplete | None = 1,
        mode: Literal["error", "continue", "shrink", "truncate"] = "shrink",
        name: str = "",
        anchor: str = "sw",
        fakeWidth: bool | None = None,
        hAlign: str = "LEFT",
        vAlign: str = "BOTTOM",
        showBoundary=None,
        origin="page",
    ) -> None: ...
    def wrap(self, _aW: Unused, _aH: Unused) -> tuple[Literal[0], Literal[0]]: ...
    def drawOn(self, canv: Canvas, lx: float, ly: float, _sW=0) -> None: ...

class _FindSplitterMixin: ...

class ImageAndFlowables(_Container, _FindSplitterMixin, Flowable):
    """combine a list of flowables and an Image"""

    imageHref: str | None
    def __init__(
        self,
        I: Image,
        F: _FlowableSublist | None,
        imageLeftPadding: float = 0,
        imageRightPadding: float = 3,
        imageTopPadding: float = 0,
        imageBottomPadding: float = 3,
        imageSide: str = "right",
        imageHref: str | None = None,
    ) -> None: ...
    def deepcopy(self) -> Self: ...

class BalancedColumns(_FindSplitterMixin, NullDraw):
    """combine a list of flowables and an Image"""

    name: str
    showBoundary: Incomplete | None
    endSlack: float
    def __init__(
        self,
        F: _FlowableSublist | None,
        nCols: int = 2,
        needed: float = 72,
        spaceBefore: float = 0,
        spaceAfter: float = 0,
        showBoundary=None,
        leftPadding: float | None = None,
        innerPadding: float | None = None,
        rightPadding: float | None = None,
        topPadding: float | None = None,
        bottomPadding: float | None = None,
        name: str = "",
        endSlack: float = 0.1,
        boxStrokeColor: Color | None = None,
        boxStrokeWidth: float = 0,
        boxFillColor: Color | None = None,
        boxMargin: tuple[int, int, int, int] | tuple[int, int, int] | tuple[int, int] | tuple[int] | None = None,
        vLinesStrokeColor: Color | None = None,
        vLinesStrokeWidth: float | None = None,
    ) -> None: ...

class AnchorFlowable(Spacer):
    """create a bookmark in the pdf"""

    def __init__(self, name: str) -> None: ...

class FrameBG(AnchorFlowable):
    """Start or stop coloring the frame background
    left & right are distances from the edge of the frame to start stop colouring.
    if start in ('frame','frame-permanent') then the background is filled from here to the bottom of the frame and immediately discarded
    for the frame case.
    """

    start: bool
    left: float
    right: float
    color: Color
    strokeWidth: float
    strokeColor: Color
    strokeDashArray: list[float] | tuple[float, ...] | None
    def __init__(
        self,
        color: Color | None = None,
        left: float | str = 0,
        right: float | str = 0,
        start: bool = True,
        strokeWidth: float | None = None,
        strokeColor: Color | None = None,
        strokeDashArray: list[float] | tuple[float, ...] | None = None,
    ) -> None: ...

class FrameSplitter(NullDraw):
    """When encountered this flowable should either switch directly to nextTemplate
    if remaining space in the current frame is less than gap+required or it should
    temporarily modify the current template to have the frames from nextTemplate
    that are listed in nextFrames and switch to the first of those frames.
    """

    nextTemplate: str
    nextFrames: list[str]
    gap: float
    required: float
    adjustHeight: bool
    def __init__(
        self,
        nextTemplate: str,
        nextFrames: list[str] | None = [],
        gap: float = 10,
        required: float = 72,
        adjustHeight: bool = True,
    ) -> None: ...

class BulletDrawer:
    value: str
    def __init__(
        self,
        value: str = "0",
        bulletAlign: str = "left",
        bulletType: str = "1",
        bulletColor: str = "black",
        bulletFontName: str = "Helvetica",
        bulletFontSize: int = 12,
        bulletOffsetY: int = 0,
        bulletDedent: int = 0,
        bulletDir: str = "ltr",
        bulletFormat=None,
    ) -> None: ...
    def drawOn(self, indenter: DDIndenter, canv: Canvas, x: float, y: float) -> None: ...

class DDIndenter(Flowable):
    def __init__(self, flowable: Flowable, leftIndent: float = 0, rightIndent: float = 0) -> None: ...

class LIIndenter(DDIndenter):
    def __init__(
        self,
        flowable: Flowable,
        leftIndent: float = 0,
        rightIndent: float = 0,
        bullet=None,
        spaceBefore: float | None = None,
        spaceAfter: float | None = None,
    ) -> None: ...

class ListItem:
    # NOTE: style has to be a ListStyle, but this will be annoying with sheet["ul"]
    # TODO: Use Unpack for kwds with the ListStyle properties + value/spaceBefore/spaceAfter
    def __init__(self, flowables: _FlowableSublist, style: PropertySet | None = None, **kwds) -> None: ...

class ListFlowable(_Container, Flowable):
    style: ListStyle
    # NOTE: style has to be a ListStyle, but this will be annoying with sheet["ul"]
    # TODO: Use Unpack for kwds with the ListStyle properties + spaceBefore/spaceAfter
    def __init__(self, flowables: Iterable[_NestedFlowable], start=None, style: PropertySet | None = None, **kwds) -> None: ...

class TopPadder(Flowable):
    """wrap a single flowable so that its first bit will be
    padded to fill out the space so that it appears at the
    bottom of its frame
    """

    # NOTE: TopPadder is mostly a transparent wrapper, we may consider trying
    #       something using __new__ in the future
    def __init__(self, f: Flowable) -> None: ...
    def __setattr__(self, a: str, v: Any) -> None: ...
    def __getattr__(self, a: str) -> Any: ...
    def __delattr__(self, a: str) -> None: ...

class DocAssign(NullDraw):
    """At wrap time this flowable evaluates var=expr in the doctemplate namespace"""

    args: tuple[Any, ...]
    def __init__(self, var: str, expr: object, life: str = "forever") -> None: ...
    def funcWrap(self, aW: float, aH: float) -> None: ...
    def func(self) -> None: ...

class DocExec(DocAssign):
    """at wrap time exec stmt in doc._nameSpace"""

    def __init__(self, stmt: str, lifetime: str = "forever") -> None: ...

class DocPara(DocAssign):
    """at wrap time create a paragraph with the value of expr as text
    if format is specified it should use %(__expr__)s for string interpolation
    of the expression expr (if any). It may also use %(name)s interpolations
    for other variables in the namespace.
    suitable defaults will be used if style and klass are None
    """

    expr: object
    format: str | None
    style: PropertySet | None
    klass: Incomplete
    escape: bool
    def __init__(
        self,
        expr: object,
        format: str | None = None,
        style: PropertySet | None = None,
        klass: _StyledFlowableFactory | None = None,
        escape: bool = True,
    ) -> None: ...
    def funcWrap(self, aW: float, aH: float) -> Any: ...
    def func(self) -> Any: ...
    def add_content(self, *args: Flowable) -> None: ...
    def get_value(self, aW: float, aH: float) -> str: ...

class DocAssert(DocPara):
    def __init__(self, cond: object, format: str | None = None) -> None: ...

class DocIf(DocPara):
    blocks: tuple[_FlowableSublist, _FlowableSublist]
    def __init__(self, cond: object, thenBlock: _FlowableSublist, elseBlock: _FlowableSublist = []) -> None: ...
    def checkBlock(self, block: _FlowableSublist) -> list[Flowable] | tuple[Flowable, ...]: ...

class DocWhile(DocIf):
    block: _FlowableSublist
    def __init__(self, cond: object, whileBlock: _FlowableSublist) -> None: ...

class SetTopFlowables(NullDraw):
    def __init__(self, F: list[Flowable], show: bool = False) -> None: ...

class SetPageTopFlowables(NullDraw):
    def __init__(self, F: list[Flowable], show: bool = False) -> None: ...
