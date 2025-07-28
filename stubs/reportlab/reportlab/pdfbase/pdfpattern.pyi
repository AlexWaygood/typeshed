"""helper for importing pdf structures into a ReportLab generated document"""

from _typeshed import Incomplete
from collections.abc import Generator

from reportlab.pdfbase.pdfdoc import PDFObject

class PDFPattern(PDFObject):
    __RefOnly__: int
    pattern: Incomplete
    arguments: Incomplete
    def __init__(self, pattern_sequence, **keywordargs) -> None:
        """
        Description of a kind of PDF object using a pattern.

        Pattern sequence should contain strings, singletons of form [string] or
        PDFPatternIf objects.
        Strings are literal strings to be used in the object.
        Singletons are names of keyword arguments to include.
        PDFpatternIf objects allow some conditionality.
        Keyword arguments can be non-instances which are substituted directly in string conversion,
        or they can be object instances in which case they should be pdfdoc.* style
        objects with a x.format(doc) method.
        Keyword arguments may be set on initialization or subsequently using __setitem__, before format.
        "constant object" instances can also be inserted in the patterns.
        """

    def __setitem__(self, item, value) -> None: ...
    def __getitem__(self, item): ...
    def eval(self, L) -> Generator[Incomplete, None, None]: ...
    def format(self, document): ...
    def clone(self): ...

class PDFPatternIf:
    """cond will be evaluated as [cond] in PDFpattern eval.
    It should evaluate to a list with value 0/1 etc etc.
    thenPart is a list to be evaluated if the cond evaulates true,
    elsePart is the false sequence.
    """

    cond: Incomplete
    thenPart: Incomplete
    elsePart: Incomplete
    def __init__(self, cond, thenPart=[], elsePart=[]) -> None: ...
