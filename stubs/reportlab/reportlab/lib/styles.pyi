"""Classes for ParagraphStyle and similar things.

A style is a collection of attributes, but with some extra features
to allow 'inheritance' from a parent, and to ensure nobody makes
changes after construction.

ParagraphStyle shows all the attributes available for formatting
paragraphs.

getSampleStyleSheet()  returns a stylesheet you can use for initial
development, with a few basic heading and text styles.
"""

from _typeshed import Incomplete
from typing import Any, ClassVar, Literal, TypeVar, overload
from typing_extensions import Self, TypeAlias

from reportlab.lib.colors import Color

_AlignmentEnum: TypeAlias = Literal[0, 1, 2, 4]
# FIXME: There are some places in the code that expect upper-case versions
#        so I'm unsure whether those would work in stylesheets as well
_AlignmentStr: TypeAlias = Literal["left", "center", "centre", "right", "justify"]
_Alignment: TypeAlias = _AlignmentEnum | _AlignmentStr
_T = TypeVar("_T")

class PropertySet:
    defaults: ClassVar[dict[str, Any]]
    name: str
    parent: PropertySet | None
    def __init__(self, name: str, parent: PropertySet | None = None, **kw: Any) -> None:
        """When initialized, it copies the class defaults;
        then takes a copy of the attributes of the parent
        if any.  All the work is done in init - styles
        should cost little to use at runtime.
        """

    def refresh(self) -> None:
        """re-fetches attributes from the parent on demand;
        use if you have been hacking the styles.  This is
        used by __init__
        """

    def listAttrs(self, indent: str = "") -> None: ...
    def clone(self, name: str, parent: PropertySet | None = None, **kwds: Any) -> Self: ...
    # PropertySet can have arbitrary attributes
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...

class ParagraphStyle(PropertySet):
    # NOTE: We list the attributes this has for sure due to defaults
    fontName: str
    fontSize: float
    leading: float
    leftIndent: float
    rightIndent: float
    firstLineIndent: float
    alignment: _Alignment
    spaceBefore: float
    spaceAfter: float
    bulletFontName: str
    bulletFontSize: float
    bulletIndent: float
    textColor: Color
    backColor: Color | None
    wordWrap: Incomplete | None
    borderWidth: float
    borderPadding: float
    borderColor: Color | None
    borderRadius: float | None
    allowWidows: Incomplete
    allowOrphans: Incomplete
    textTransform: Incomplete | None
    endDots: Incomplete | None
    splitLongWords: Incomplete
    underlineWidth: float
    bulletAnchor: Literal["start", "middle", "end"] | float
    justifyLastLine: Incomplete
    justifyBreaks: Incomplete
    spaceShrinkage: float
    strikeWidth: float
    underlineOffset: float
    underlineGap: float
    strikeOffset: float
    strikeGap: float
    linkUnderline: Incomplete
    underlineColor: Color | None
    strikeColor: Color | None
    hyphenationLang: str
    embeddedHyphenation: Incomplete
    uriWasteReduce: float
    # NOTE: We redefine __init__ for the same reason
    def __init__(
        self,
        name: str,
        parent: PropertySet | None = None,
        *,
        fontName: str = ...,
        fontSize: float = ...,
        leading: float = ...,
        leftIndent: float = ...,
        rightIndent: float = ...,
        firstLineIndent: float = ...,
        alignment: _Alignment = ...,
        spaceBefore: float = ...,
        spaceAfter: float = ...,
        bulletFontName: str = ...,
        bulletFontSize: float = ...,
        bulletIndent: float = ...,
        textColor: Color = ...,
        backColor: Color | None = ...,
        wordWrap: Incomplete | None = ...,
        borderWidth: float = ...,
        borderPadding: float = ...,
        borderColor: Color | None = ...,
        borderRadius: float | None = ...,
        allowWidows=...,
        allowOrphans=...,
        textTransform: Incomplete | None = ...,
        endDots: Incomplete | None = ...,
        splitLongWords=...,
        underlineWidth: float = ...,
        bulletAnchor: Literal["start", "middle", "end"] | float = ...,
        justifyLastLine=...,
        justifyBreaks=...,
        spaceShrinkage: float = ...,
        strikeWidth: float = ...,
        underlineOffset: float = ...,
        underlineGap: float = ...,
        strikeOffset: float = ...,
        strikeGap: float = ...,
        linkUnderline=...,
        underlineColor: Color | None = ...,
        strikeColor: Color | None = ...,
        hyphenationLang: str = ...,
        embeddedHyphenation=...,
        uriWasteReduce: float = ...,
        **kw: Any,
    ) -> None:
        """When initialized, it copies the class defaults;
        then takes a copy of the attributes of the parent
        if any.  All the work is done in init - styles
        should cost little to use at runtime.
        """

def str2alignment(
    v: _AlignmentStr,
    __map__: dict[_AlignmentStr, _AlignmentEnum] = {"centre": 1, "center": 1, "left": 0, "right": 2, "justify": 4},
) -> _AlignmentEnum: ...

class LineStyle(PropertySet):
    # NOTE: We list the attributes this has for sure due to defaults
    width: float
    color: Color
    def prepareCanvas(self, canvas) -> None:
        """You can ask a LineStyle to set up the canvas for drawing
        the lines.
        """
    # NOTE: We redefine __init__ for the same reason
    def __init__(
        self, name: str, parent: PropertySet | None = None, *, width: float = ..., color: Color = ..., **kw: Any
    ) -> None:
        """When initialized, it copies the class defaults;
        then takes a copy of the attributes of the parent
        if any.  All the work is done in init - styles
        should cost little to use at runtime.
        """

class ListStyle(PropertySet):
    # NOTE: We list the attributes this has for sure due to defaults
    leftIndent: float
    rightIndent: float
    bulletAlign: _Alignment
    bulletType: str
    bulletColor: Color
    bulletFontName: str
    bulletFontSize: float
    bulletOffsetY: float
    bulletDedent: Incomplete
    bulletDir: Incomplete
    bulletFormat: Incomplete | None
    start: Incomplete | None
    # NOTE: We redefine __init__ for the same reason
    def __init__(
        self,
        name: str,
        parent: PropertySet | None = None,
        *,
        leftIndent: float = ...,
        rightIndent: float = ...,
        bulletAlign: _Alignment = ...,
        bulletType: str = ...,
        bulletColor: Color = ...,
        bulletFontName: str = ...,
        bulletFontSize: float = ...,
        bulletOffsetY: float = ...,
        bulletDedent=...,
        bulletDir=...,
        bulletFormat: Incomplete | None = ...,
        start: Incomplete | None = ...,
        **kw: Any,
    ) -> None:
        """When initialized, it copies the class defaults;
        then takes a copy of the attributes of the parent
        if any.  All the work is done in init - styles
        should cost little to use at runtime.
        """

class StyleSheet1:
    """
    This may or may not be used.  The idea is to:

    1. slightly simplify construction of stylesheets;

    2. enforce rules to validate styles when added
       (e.g. we may choose to disallow having both
       'heading1' and 'Heading1' - actual rules are
       open to discussion);

    3. allow aliases and alternate style lookup
       mechanisms

    4. Have a place to hang style-manipulation
       methods (save, load, maybe support a GUI
       editor)

    Access is via getitem, so they can be
    compatible with plain old dictionaries.
    """

    byName: dict[str, PropertySet]
    byAlias: dict[str, PropertySet]
    def __init__(self) -> None: ...
    def __getitem__(self, key: str) -> PropertySet: ...
    @overload
    def get(self, key: str) -> PropertySet: ...
    @overload
    def get(self, key: str, default: _T) -> PropertySet | _T: ...
    def __contains__(self, key: str) -> bool: ...
    def has_key(self, key: str) -> bool: ...
    def add(self, style: PropertySet, alias: str | None = None) -> None: ...
    def list(self) -> None: ...

def getSampleStyleSheet() -> StyleSheet1:
    """Returns a stylesheet object"""

__all__ = ("PropertySet", "ParagraphStyle", "str2alignment", "LineStyle", "ListStyle", "StyleSheet1", "getSampleStyleSheet")
