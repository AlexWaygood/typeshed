"""
This module contains the core structure of platypus.

rlatypus constructs documents.  Document styles are determined by DocumentTemplates.

Each DocumentTemplate contains one or more PageTemplates which defines the look of the
pages of the document.

Each PageTemplate has a procedure for drawing the "non-flowing" part of the page
(for example the header, footer, page number, fixed logo graphic, watermark, etcetera) and
a set of Frames which enclose the flowing part of the page (for example the paragraphs,
tables, or non-fixed diagrams of the text).

A document is built when a DocumentTemplate is fed a sequence of Flowables.
The action of the build consumes the flowables in order and places them onto
frames on pages as space allows.  When a frame runs out of space the next frame
of the page is used.  If no frame remains a new page is created.  A new page
can also be created if a page break is forced.

The special invisible flowable NextPageTemplate can be used to specify
the page template for the next page (which by default is the one being used
for the current frame).
"""

from _typeshed import Incomplete
from abc import abstractmethod
from collections.abc import Callable
from typing import IO, Any, Literal, Protocol
from typing_extensions import Self, TypeAlias

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.frames import Frame

__all__ = (
    "ActionFlowable",
    "BaseDocTemplate",
    "CurrentFrameFlowable",
    "FrameActionFlowable",
    "FrameBreak",
    "Indenter",
    "IndexingFlowable",
    "LayoutError",
    "LCActionFlowable",
    "NextFrameFlowable",
    "NextPageTemplate",
    "NotAtTopPageBreak",
    "NullActionFlowable",
    "PageAccumulator",
    "PageBegin",
    "PageTemplate",
    "SimpleDocTemplate",
)

# NOTE: Since we don't know what kind of DocTemplate we will use in a PageTemplate
#       we'll leave the second argument at Any, since the workaround with unbound
#       type vars didn't seem to work for this one
_PageCallback: TypeAlias = Callable[[Canvas, Any], object]

class _CanvasMaker(Protocol):
    # NOTE: This matches a subset of Canvas.__init__
    def __call__(
        self,
        filename: str | IO[bytes],
        /,
        *,
        pagesize=None,
        pageCompression=None,
        invariant=None,
        enforceColorSpace=None,
        initialFontName=None,
        initialFontSize=None,
        initialLeading=None,
        cropBox=None,
        artBox=None,
        trimBox=None,
        bleedBox=None,
        lang=None,
    ) -> Canvas: ...

class LayoutError(Exception): ...

# NOTE: While internal, this is used as sentinel value in PageTemplate
#       and SimpleDocTemplate so in subclasses you may need to use this
def _doNothing(canvas: Canvas, doc: BaseDocTemplate) -> None:
    """Dummy callback for onPage"""

class PTCycle(list[PageTemplate]):
    @property
    def next_value(self) -> PageTemplate: ...
    @property
    def peek(self) -> PageTemplate: ...

class IndexingFlowable(Flowable):
    """Abstract interface definition for flowables which might
    hold references to other pages or themselves be targets
    of cross-references.  XRefStart, XRefDest, Table of Contents,
    Indexes etc.
    """

    def isIndexing(self) -> Literal[1]: ...
    def isSatisfied(self) -> int: ...
    def notify(self, kind: str, stuff: Any) -> None:
        """This will be called by the framework wherever 'stuff' happens.
        'kind' will be a value that can be used to decide whether to
        pay attention or not.
        """

    def beforeBuild(self) -> None:
        """Called by multiBuild before it starts; use this to clear
        old contents
        """

    def afterBuild(self) -> None:
        """Called after build ends but before isSatisfied"""

class ActionFlowable(Flowable):
    """This Flowable is never drawn, it can be used for data driven controls
    For example to change a page template (from one column to two, for example)
    use NextPageTemplate which creates an ActionFlowable.
    """

    # NOTE: Technically action always has to contain a string referencing
    #       a handle_ method on the DocTemplate, while the rest are the args
    #       that should be passed to that method, but since the default arg
    #       on __init__ violates that we might as well keep things simple
    action: tuple[Any, ...]
    def __init__(self, action: list[Any] | tuple[Any, ...] = ()) -> None: ...
    def apply(self, doc: BaseDocTemplate) -> None:
        """
        This is called by the doc.build processing to allow the instance to
        implement its behaviour
        """

    def __call__(self) -> Self: ...

class NullActionFlowable(ActionFlowable): ...

class LCActionFlowable(ActionFlowable):
    locChanger: int
    def draw(self) -> None:
        """Should never be called."""

class NextFrameFlowable(ActionFlowable):
    locChanger: int
    def __init__(self, ix: int | str, resume: int = 0) -> None: ...

class CurrentFrameFlowable(LCActionFlowable):
    def __init__(self, ix: int | str, resume: int = 0) -> None: ...

class _FrameBreak(LCActionFlowable):
    """
    A special ActionFlowable that allows setting doc._nextFrameIndex

    eg story.append(FrameBreak('mySpecialFrame'))
    """

    def __call__(self, ix: int | str | None = None, resume: int = 0) -> Self: ...
    def apply(self, doc: BaseDocTemplate) -> None: ...

FrameBreak: _FrameBreak
PageBegin: LCActionFlowable

class FrameActionFlowable(Flowable):
    @abstractmethod
    def __init__(self, *arg: Any, **kw: Any) -> None: ...
    @abstractmethod
    def frameAction(self, frame: Frame) -> None: ...

class Indenter(FrameActionFlowable):
    """Increases or decreases left and right margins of frame.

    This allows one to have a 'context-sensitive' indentation
    and makes nested lists way easier.
    """

    width: float
    height: float
    left: float
    right: float
    def __init__(self, left: float | str = 0, right: float | str = 0) -> None: ...
    def frameAction(self, frame: Frame) -> None: ...

class NotAtTopPageBreak(FrameActionFlowable):
    locChanger: int
    nextTemplate: Incomplete
    def __init__(self, nextTemplate=None) -> None: ...
    def frameAction(self, frame: Frame) -> None: ...

class NextPageTemplate(ActionFlowable):
    locChanger: int
    def __init__(self, pt: str | int | list[str] | tuple[str, ...]) -> None: ...

class PageTemplate:
    """
    essentially a list of Frames and an onPage routine to call at the start
    of a page when this is selected. onPageEnd gets called at the end.
    derived classes can also implement beforeDrawPage and afterDrawPage if they want
    """

    id: str | None
    frames: list[Frame]
    onPage: _PageCallback
    onPageEnd: _PageCallback
    pagesize: tuple[float, float]
    autoNextPageTemplate: Incomplete
    cropBox: Incomplete
    artBox: Incomplete
    trimBox: Incomplete
    bleedBox: Incomplete
    def __init__(
        self,
        id: str | None = None,
        frames: list[Frame] | Frame = [],
        onPage: _PageCallback = ...,
        onPageEnd: _PageCallback = ...,
        pagesize: tuple[float, float] | None = None,
        autoNextPageTemplate=None,
        cropBox=None,
        artBox=None,
        trimBox=None,
        bleedBox=None,
    ) -> None: ...
    def beforeDrawPage(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """Override this if you want additional functionality or prefer
        a class based page routine.  Called before any flowables for
        this page are processed.
        """

    def checkPageSize(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """This gets called by the template framework
        If canv size != template size then the canv size is set to
        the template size or if that's not available to the
        doc size.
        """

    def afterDrawPage(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """This is called after the last flowable for the page has
        been processed.  You might use this if the page header or
        footer needed knowledge of what flowables were drawn on
        this page.
        """

class onDrawStr(str):
    onDraw: Callable[[Canvas, str | None, str], object]
    kind: str | None
    label: str
    def __new__(
        cls, value: object, onDraw: Callable[[Canvas, str | None, str], object], label: str, kind: str | None = None
    ) -> Self: ...
    def __getnewargs__(self) -> tuple[str, Callable[[Canvas, str | None, str], object], str, str | None]: ...  # type: ignore[override]

class PageAccumulator:
    """gadget to accumulate information in a page
    and then allow it to be interrogated at the end
    of the page
    """

    name: str
    data: list[tuple[Any, ...]]
    def __init__(self, name: str | None = None) -> None: ...
    def reset(self) -> None: ...
    def add(self, *args) -> None: ...
    def onDrawText(self, *args) -> str: ...
    def __call__(self, canv: Canvas, kind: str | None, label: str) -> None: ...
    def attachToPageTemplate(self, pt: PageTemplate) -> None: ...
    def onPage(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """this will be called at the start of the page"""

    def onPageEnd(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """this will be called at the end of a page"""

    def pageEndAction(self, canv: Canvas, doc: BaseDocTemplate) -> None:
        """this should be overridden to do something useful"""

    def onDrawStr(self, value: object, *args) -> onDrawStr: ...

class BaseDocTemplate:
    """
    First attempt at defining a document template class.

    The basic idea is simple.

    1)  The document has a list of data associated with it
        this data should derive from flowables. We'll have
        special classes like PageBreak, FrameBreak to do things
        like forcing a page end etc.

    2)  The document has one or more page templates.

    3)  Each page template has one or more frames.

    4)  The document class provides base methods for handling the
        story events and some reasonable methods for getting the
        story flowables into the frames.

    5)  The document instances can override the base handler routines.

    Most of the methods for this class are not called directly by the user,
    but in some advanced usages they may need to be overridden via subclassing.

    EXCEPTION: doctemplate.build(...) must be called for most reasonable uses
    since it builds a document using the page template.

    Each document template builds exactly one document into a file specified
    by the filename argument on initialization.

    Possible keyword arguments for the initialization:

    - pageTemplates: A list of templates.  Must be nonempty.  Names
      assigned to the templates are used for referring to them so no two used
      templates should have the same name.  For example you might want one template
      for a title page, one for a section first page, one for a first page of
      a chapter and two more for the interior of a chapter on odd and even pages.
      If this argument is omitted then at least one pageTemplate should be provided
      using the addPageTemplates method before the document is built.
    - pageSize: a 2-tuple or a size constant from reportlab/lib/pagesizes.pu.
      Used by the SimpleDocTemplate subclass which does NOT accept a list of
      pageTemplates but makes one for you; ignored when using pageTemplates.

    - showBoundary: if set draw a box around the frame boundaries.
    - leftMargin:
    - rightMargin:
    - topMargin:
    - bottomMargin:  Margin sizes in points (default 1 inch).  These margins may be
      overridden by the pageTemplates.  They are primarily of interest for the
      SimpleDocumentTemplate subclass.

    - allowSplitting:  If set flowables (eg, paragraphs) may be split across frames or pages
      (default: 1)
    - title: Internal title for document (does not automatically display on any page)
    - author: Internal author for document (does not automatically display on any page)
    """

    filename: Incomplete
    pagesize: Incomplete
    pageTemplates: list[PageTemplate]
    showBoundary: Incomplete
    width: float
    height: float
    leftMargin: float
    rightMargin: float
    topMargin: float
    bottomMargin: float
    allowSplitting: Incomplete
    title: Incomplete | None
    author: Incomplete | None
    subject: Incomplete | None
    creator: Incomplete | None
    producer: Incomplete | None
    keywords: list[Incomplete]
    invariant: Incomplete | None
    pageCompression: Incomplete | None
    rotation: Incomplete
    encrypt: Incomplete | None
    cropMarks: Incomplete | None
    enforceColorSpace: Incomplete | None
    displayDocTitle: Incomplete | None
    lang: Incomplete | None
    initialFontName: Incomplete | None
    initialFontSize: Incomplete | None
    initialLeading: Incomplete | None
    cropBox: Incomplete | None
    artBox: Incomplete | None
    trimBox: Incomplete | None
    bleedBox: Incomplete | None
    keepTogetherClass: type[Flowable]
    hideToolbar: Incomplete | None
    hideMenubar: Incomplete | None
    hideWindowUI: Incomplete | None
    fitWindow: Incomplete | None
    centerWindow: Incomplete | None
    nonFullScreenPageMode: Incomplete | None
    direction: Incomplete | None
    viewArea: Incomplete | None
    viewClip: Incomplete | None
    printArea: Incomplete | None
    printClip: Incomplete | None
    printScaling: Incomplete | None
    duplex: Incomplete | None
    # NOTE: The following attributes only exist while/after pages are rendered
    pageTemplate: PageTemplate
    page: int
    frame: Frame
    canv: Canvas
    # TODO: Use TypedDict with Unpack for **kw
    def __init__(self, filename: str | IO[bytes], **kw) -> None:
        """create a document template bound to a filename (see class documentation for keyword arguments)"""

    def setPageCallBack(self, func: Callable[[int], object] | None) -> None:
        """Simple progress monitor - func(pageNo) called on each new page"""

    def setProgressCallBack(self, func: Callable[[str, int], object] | None) -> None:
        """Cleverer progress monitor - func(typ, value) called regularly"""

    def clean_hanging(self) -> None:
        """handle internal postponed actions"""

    def addPageTemplates(self, pageTemplates: list[PageTemplate] | tuple[PageTemplate, ...] | PageTemplate) -> None:
        """add one or a sequence of pageTemplates"""

    def handle_documentBegin(self) -> None:
        """implement actions at beginning of document"""

    def handle_pageBegin(self) -> None:
        """Perform actions required at beginning of page.
        shouldn't normally be called directly
        """

    def handle_pageEnd(self) -> None:
        """show the current page
        check the next page template
        hang a page begin
        """

    def handle_pageBreak(self, slow: bool | None = None) -> None:
        """some might choose not to end all the frames"""

    def handle_frameBegin(self, resume: int = 0, pageTopFlowables=None) -> None:
        """What to do at the beginning of a frame"""

    def handle_frameEnd(self, resume: int = 0) -> None:
        """Handles the semantics of the end of a frame. This includes the selection of
        the next frame or if this is the last frame then invoke pageEnd.
        """

    def handle_nextPageTemplate(self, pt: str | int | list[str] | tuple[str, ...]) -> None:
        """On endPage change to the page template with name or index pt"""

    def handle_nextFrame(self, fx: str | int, resume: int = 0) -> None:
        """On endFrame change to the frame with name or index fx"""

    def handle_currentFrame(self, fx: str | int, resume: int = 0) -> None:
        """change to the frame with name or index fx"""

    def handle_breakBefore(self, flowables: list[Flowable]) -> None:
        """preprocessing step to allow pageBreakBefore and frameBreakBefore attributes"""

    def handle_keepWithNext(self, flowables: list[Flowable]) -> None:
        """implements keepWithNext"""

    def handle_flowable(self, flowables: list[Flowable]) -> None:
        """try to handle one flowable from the front of list flowables."""

    def build(self, flowables: list[Flowable], filename: str | None = None, canvasmaker: _CanvasMaker = ...) -> None:
        """Build the document from a list of flowables.
        If the filename argument is provided then that filename is used
        rather than the one provided upon initialization.
        If the canvasmaker argument is provided then it will be used
        instead of the default.  For example a slideshow might use
        an alternate canvas which places 6 slides on a page (by
        doing translations, scalings and redefining the page break
        operations).
        """

    def notify(self, kind: str, stuff: Any) -> None:
        """Forward to any listeners"""

    def pageRef(self, label: str) -> None:
        """hook to register a page number"""

    def multiBuild(self, story: list[Flowable], maxPasses: int = 10, **buildKwds: Any) -> int:
        """Makes multiple passes until all indexing flowables
        are happy.

        Returns number of passes
        """

    def afterInit(self) -> None:
        """This is called after initialisation of the base class."""

    def beforeDocument(self) -> None:
        """This is called before any processing is
        done on the document.
        """

    def beforePage(self) -> None:
        """This is called at the beginning of page
        processing, and immediately before the
        beforeDrawPage method of the current page
        template.
        """

    def afterPage(self) -> None:
        """This is called after page processing, and
        immediately after the afterDrawPage method
        of the current page template.
        """

    def filterFlowables(self, flowables: list[Flowable]) -> None:
        """called to filter flowables at the start of the main handle_flowable method.
        Upon return if flowables[0] has been set to None it is discarded and the main
        method returns.
        """

    def afterFlowable(self, flowable: Flowable) -> None:
        """called after a flowable has been rendered"""

    def docAssign(self, var: str, expr: object, lifetime: str) -> None: ...
    def docExec(self, stmt: str, lifetime: str) -> None: ...
    def docEval(self, expr: str) -> Any: ...

class SimpleDocTemplate(BaseDocTemplate):
    """A special case document template that will handle many simple documents.
    See documentation for BaseDocTemplate.  No pageTemplates are required
    for this special case.   A page templates are inferred from the
    margin information and the onFirstPage, onLaterPages arguments to the build method.

    A document which has all pages with the same look except for the first
    page may can be built using this special approach.
    """

    def handle_pageBegin(self) -> None:
        """override base method to add a change of page template after the firstpage."""

    def build(  # type: ignore[override]
        self,
        flowables: list[Flowable],
        onFirstPage: _PageCallback = ...,
        onLaterPages: _PageCallback = ...,
        canvasmaker: _CanvasMaker = ...,
    ) -> None:
        """build the document using the flowables.  Annotate the first page using the onFirstPage
        function and later pages using the onLaterPages function.  The onXXX pages should follow
        the signature

           def myOnFirstPage(canvas, document):
               # do annotations and modify the document
               ...

        The functions can do things like draw logos, page numbers,
        footers, etcetera. They can use external variables to vary
        the look (for example providing page numbering or section names).
        """
