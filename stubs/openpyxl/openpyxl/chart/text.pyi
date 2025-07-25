from _typeshed import Incomplete, Unused
from typing import ClassVar, Literal

from openpyxl.chart.data_source import StrRef
from openpyxl.descriptors.base import Alias, Typed
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.drawing.text import ListStyle, RichTextProperties
from openpyxl.xml.functions import Element

class RichText(Serialisable):
    """
    From the specification: 21.2.2.216

    This element specifies text formatting. The lstStyle element is not supported.
    """

    tagname: ClassVar[str]
    bodyPr: Typed[RichTextProperties, Literal[False]]
    properties: Alias
    lstStyle: Typed[ListStyle, Literal[True]]
    p: Incomplete
    paragraphs: Alias
    __elements__: ClassVar[tuple[str, ...]]
    def __init__(self, bodyPr: RichTextProperties | None = None, lstStyle: ListStyle | None = None, p=None) -> None: ...

class Text(Serialisable):
    """
    The value can be either a cell reference or a text element
    If both are present then the reference will be used.
    """

    tagname: ClassVar[str]
    strRef: Typed[StrRef, Literal[True]]
    rich: Typed[RichText, Literal[True]]
    __elements__: ClassVar[tuple[str, ...]]
    def __init__(self, strRef: StrRef | None = None, rich: RichText | None = None) -> None: ...
    def to_tree(self, tagname: str | None = None, idx: Unused = None, namespace: str | None = None) -> Element: ...
