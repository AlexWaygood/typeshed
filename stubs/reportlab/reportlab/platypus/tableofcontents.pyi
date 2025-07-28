"""Experimental class to generate Tables of Contents easily

This module defines a single TableOfContents() class that can be used to
create automatically a table of tontents for Platypus documents like
this:

    story = []
    toc = TableOfContents()
    story.append(toc)
    # some heading paragraphs here...
    doc = MyTemplate(path)
    doc.multiBuild(story)

The data needed to create the table is a list of (level, text, pageNum)
triplets, plus some paragraph styles for each level of the table itself.
The triplets will usually be created in a document template's method
like afterFlowable(), making notification calls using the notify()
method with appropriate data like this:

    (level, text, pageNum) = ...
    self.notify('TOCEntry', (level, text, pageNum))

Optionally the list can contain four items in which case the last item
is a destination key which the entry should point to. A bookmark
with this key needs to be created first like this:

    key = 'ch%s' % self.seq.nextf('chapter')
    self.canv.bookmarkPage(key)
    self.notify('TOCEntry', (level, text, pageNum, key))

As the table of contents need at least two passes over the Platypus
story which is why the multiBuild() method must be called.

The level<NUMBER>ParaStyle variables are the paragraph styles used
to format the entries in the table of contents. Their indentation
is calculated like this: each entry starts at a multiple of some
constant named delta. If one entry spans more than one line, all
lines after the first are indented by the same constant named
epsilon.
"""

from _typeshed import Unused
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Final, Literal, TypedDict, TypeVar, overload
from typing_extensions import TypeAlias, Unpack

from reportlab.lib.styles import ParagraphStyle, PropertySet
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.doctemplate import IndexingFlowable, _CanvasMaker
from reportlab.platypus.tables import TableStyle

_T = TypeVar("_T")
_Entry: TypeAlias = tuple[int, str, int] | tuple[int, str, int, str | None] | Sequence[int | str | None]
_SequencerFormat: TypeAlias = Literal["I", "i", "123", "ABC", "abc"]

class _TableOfContentsKwargs(TypedDict, total=False):
    rightColumnWidth: float
    levelStyles: list[PropertySet]  # should be ParagraphStyle
    tableStyle: TableStyle
    dotsMinLevel: int
    formatter: Callable[[int], str] | None

class _SimpleIndexKwargs(TypedDict, total=False):
    style: Iterable[PropertySet] | PropertySet | None  # should be ParagraphStyle
    dot: str | None
    tableStyle: TableStyle | None
    headers: bool
    name: str | None
    format: _SequencerFormat
    offset: int

__version__: Final[str]

def unquote(txt: str) -> str: ...
def drawPageNumbers(
    canvas: Canvas,
    style: PropertySet,  # should be ParagraphStyle
    pages: Iterable[tuple[int | str, Unused]],
    availWidth: float,
    availHeight: float,
    dot: str = " . ",
    formatter: Unused | None = None,
) -> None:
    """
    Draws pagestr on the canvas using the given style.
    If dot is None, pagestr is drawn at the current position in the canvas.
    If dot is a string, pagestr is drawn right-aligned. If the string is not empty,
    the gap is filled with it.
    """

delta: float
epsilon: float
defaultLevelStyles: list[ParagraphStyle]
defaultTableStyle: TableStyle

class TableOfContents(IndexingFlowable):
    """This creates a formatted table of contents.

    It presumes a correct block of data is passed in.
    The data block contains a list of (level, text, pageNumber)
    triplets.  You can supply a paragraph style for each level
    (starting at zero).
    Set dotsMinLevel to determine from which level on a line of
    dots should be drawn between the text and the page number.
    If dotsMinLevel is set to a negative value, no dotted lines are drawn.
    """

    rightColumnWidth: float
    levelStyles: list[ParagraphStyle]
    tableStyle: TableStyle
    dotsMinLevel: int
    formatter: Callable[[int], str] | None
    def __init__(self, **kwds: Unpack[_TableOfContentsKwargs]) -> None: ...
    def isIndexing(self) -> Literal[1]: ...
    def isSatisfied(self) -> bool: ...
    def clearEntries(self) -> None: ...
    def getLevelStyle(self, n: int) -> ParagraphStyle:
        """Returns the style for level n, generating and caching styles on demand if not present."""

    def addEntry(self, level: int, text: str, pageNum: int, key: str | None = None) -> None:
        """Adds one entry to the table of contents.

        This allows incremental buildup by a doctemplate.
        Requires that enough styles are defined.
        """

    def addEntries(self, listOfEntries: Iterable[_Entry]) -> None:
        """Bulk creation of entries in the table of contents.

        If you knew the titles but not the page numbers, you could
        supply them to get sensible output on the first run.
        """

@overload
def makeTuple(x: tuple[_T, ...]) -> tuple[_T, ...]: ...
@overload
def makeTuple(x: list[_T]) -> tuple[_T, ...]: ...
@overload
def makeTuple(x: _T) -> tuple[_T, ...]: ...

class SimpleIndex(IndexingFlowable):
    """Creates multi level indexes.
    The styling can be cutomized and alphabetic headers turned on and off.
    """

    # NOTE: Will be a list after getLevelStyle is called
    textStyle: ParagraphStyle | Iterable[ParagraphStyle] | list[ParagraphStyle]
    tableStyle: TableStyle
    dot: str | None
    headers: bool
    name: str
    formatFunc: Callable[[int], str]
    offset: float
    def __init__(self, **kwargs: Unpack[_SimpleIndexKwargs]) -> None:
        """
        Constructor of SimpleIndex.
        Accepts the same arguments as the setup method.
        """

    def getFormatFunc(self, formatName): ...
    def setup(
        self,
        style: PropertySet | None = None,  # should be ParagraphStyle
        dot: str | None = None,
        tableStyle: TableStyle | None = None,
        headers: bool = True,
        name: str | None = None,
        format: _SequencerFormat = "123",
        offset: float = 0,
    ) -> None:
        """
        This method makes it possible to change styling and other parameters on an existing object.

        style is the paragraph style to use for index entries.
        dot can either be None or a string. If it's None, entries are immediatly followed by their
            corresponding page numbers. If it's a string, page numbers are aligned on the right side
            of the document and the gap filled with a repeating sequence of the string.
        tableStyle is the style used by the table which the index uses to draw itself. Use this to
            change properties like spacing between elements.
        headers is a boolean. If it is True, alphabetic headers are displayed in the Index when the first
        letter changes. If False, we just output some extra space before the next item
        name makes it possible to use several indexes in one document. If you want this use this
            parameter to give each index a unique name. You can then index a term by refering to the
            name of the index which it should appear in:

                <index item="term" name="myindex" />

        format can be 'I', 'i', '123',  'ABC', 'abc'
        """

    def __call__(self, canv: Canvas, kind: str | None, label: str) -> None: ...
    def getCanvasMaker(self, canvasmaker: _CanvasMaker = ...) -> _CanvasMaker: ...
    def isIndexing(self) -> Literal[1]: ...
    def isSatisfied(self) -> bool: ...
    def clearEntries(self) -> None: ...
    def addEntry(self, text: str, pageNum: tuple[int, str], key: str | None = None) -> None:
        """Allows incremental buildup"""

    def draw(self) -> None: ...
    def getLevelStyle(self, n: int) -> ParagraphStyle:
        """Returns the style for level n, generating and caching styles on demand if not present."""

AlphabeticIndex = SimpleIndex

def listdiff(l1: list[Any], l2: list[_T]) -> tuple[int, list[_T]]: ...

class ReferenceText(IndexingFlowable):
    """Fakery to illustrate how a reference would work if we could
    put it in a paragraph.
    """

    textPattern: str
    target: str
    paraStyle: ParagraphStyle
    def __init__(self, textPattern: str, targetKey: str) -> None: ...
