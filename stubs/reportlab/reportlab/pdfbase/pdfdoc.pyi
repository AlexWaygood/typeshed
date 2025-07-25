"""
The module pdfdoc.py handles the 'outer structure' of PDF documents, ensuring that
all objects are properly cross-referenced and indexed to the nearest byte.  The
'inner structure' - the page descriptions - are presumed to be generated before
each page is saved.
pdfgen.py calls this and provides a 'canvas' object to handle page marking operators.
piddlePDF calls pdfgen and offers a high-level interface.

The classes within this generally mirror structures in the PDF file
and are not part of any public interface.  Instead, canvas and font
classes are made available elsewhere for users to manipulate.
"""

from _typeshed import Incomplete
from collections.abc import Mapping
from typing import Final

__version__: Final[str]

class PDFError(Exception): ...

__InternalName__: Final[str]
__RefOnly__: Final[str]
__Comment__: Final[str]
BasicFonts: Final[str]
Pages: Final[str]
PDF_VERSION_DEFAULT: Final[tuple[int, int]]
PDF_SUPPORT_VERSION: Final[Mapping[str, tuple[int, int]]]

def pdfdocEnc(x): ...
def format(element, document, toplevel: int = 0):
    """Indirection step for formatting.
    Ensures that document parameters alter behaviour
    of formatting for all elements.
    """

def xObjectName(externalname): ...

formName = xObjectName

class NoEncryption:
    def encode(self, t):
        """encode a string, stream, text"""

    def prepare(self, document) -> None: ...
    def register(self, objnum, version) -> None: ...
    def info(self) -> None: ...

class PDFObject: ...

class DummyDoc(PDFObject):
    """used to bypass encryption when required"""

    encrypt: Incomplete

class PDFDocument(PDFObject):
    defaultStreamFilters: Incomplete
    encrypt: Incomplete
    objectcounter: int
    shadingCounter: int
    inObject: Incomplete
    pageCounter: int
    invariant: Incomplete
    idToObjectNumberAndVersion: Incomplete
    idToObject: Incomplete
    idToOffset: Incomplete
    numberToId: Incomplete
    outline: Incomplete
    info: Incomplete
    fontMapping: Incomplete
    delayedFonts: Incomplete
    def __init__(
        self, dummyoutline: int = 0, compression=1, invariant=0, filename=None, pdfVersion=(1, 3), lang=None
    ) -> None: ...
    compression: Incomplete
    def setCompression(self, onoff) -> None: ...
    def ensureMinPdfVersion(self, *keys) -> None:
        """Ensure that the pdf version is greater than or equal to that specified by the keys"""

    def updateSignature(self, thing) -> None:
        """add information to the signature"""

    def ID(self):
        """A unique fingerprint for the file (unless in invariant mode)"""

    def SaveToFile(self, filename, canvas) -> None: ...
    def GetPDFData(self, canvas): ...
    def inPage(self) -> None:
        """specify the current object as a page (enables reference binding and other page features)"""

    def inForm(self) -> None:
        """specify that we are in a form xobject (disable page features, etc)"""

    def getInternalFontName(self, psfontname): ...
    def thisPageName(self): ...
    def thisPageRef(self): ...
    def addPage(self, page) -> None: ...
    def addForm(self, name, form) -> None:
        """add a Form XObject."""

    def annotationName(self, externalname): ...
    def addAnnotation(self, name, annotation) -> None: ...
    def refAnnotation(self, name): ...
    def addShading(self, shading): ...
    def addColor(self, cmyk): ...
    def setTitle(self, title) -> None:
        """embeds in PDF file"""

    def setAuthor(self, author) -> None:
        """embedded in PDF file"""

    def setSubject(self, subject) -> None:
        """embeds in PDF file"""

    def setCreator(self, creator) -> None:
        """embeds in PDF file"""

    def setProducer(self, producer) -> None:
        """embeds in PDF file"""

    def setKeywords(self, keywords) -> None:
        """embeds a string containing keywords in PDF file"""

    def setDateFormatter(self, dateFormatter) -> None: ...
    def getAvailableFonts(self): ...
    __accum__: Incomplete
    def format(self): ...
    def hasForm(self, name):
        """test for existence of named form"""

    def getFormBBox(self, name, boxType: str = "MediaBox"):
        """get the declared bounding box of the form as a list.
        If you specify a different PDF box definition (e.g. the
        ArtBox) and it has one, that's what you'll get.
        """

    def getXObjectName(self, name):
        """Lets canvas find out what form is called internally.
        Never mind whether it is defined yet or not.
        """

    def xobjDict(self, formnames):
        """construct an xobject dict (for inclusion in a resource dict, usually)
        from a list of form names (images not yet supported)
        """

    def Reference(self, obj, name=None): ...

PDFtrue: str
PDFfalse: str
PDFnull: str

class PDFText(PDFObject):
    t: Incomplete
    enc: Incomplete
    def __init__(self, t, enc: str = "utf-8") -> None: ...
    def format(self, document): ...

def PDFnumber(n): ...

class PDFString(PDFObject):
    unicodeEncValid: bool
    s: Incomplete
    escape: Incomplete
    enc: Incomplete
    def __init__(self, s, escape: int = 1, enc: str = "auto") -> None:
        """s can be unicode/utf8 or a PDFString
        if escape is true then the output will be passed through escape
        if enc is raw then bytes will be left alone
        if enc is auto we'll try and automatically adapt to utf_16_be/utf_16_le if the
        effective string is not entirely in pdfdoc
        if self.unicodeEncValid unicode will use the specifed encoding
        """

    def format(self, document): ...

def PDFName(data, lo="!", hi="~"): ...

class PDFDictionary(PDFObject):
    multiline: bool
    dict: Incomplete
    def __init__(self, dict=None) -> None:
        """dict should be namestring to value eg "a": 122 NOT pdfname to value NOT "/a":122"""

    def __setitem__(self, name, value) -> None: ...
    def __getitem__(self, a): ...
    def __contains__(self, a) -> bool: ...
    def Reference(self, name, document) -> None: ...
    def format(self, document, IND: bytes = b"\n "): ...
    def copy(self): ...
    def normalize(self) -> None: ...

class checkPDFNames:
    names: Incomplete
    def __init__(self, *names) -> None: ...
    def __call__(self, value): ...

def checkPDFBoolean(value): ...

class CheckedPDFDictionary(PDFDictionary):
    validate: Incomplete
    def __init__(self, dict=None, validate=None) -> None: ...
    def __setitem__(self, name, value) -> None: ...

class ViewerPreferencesPDFDictionary(CheckedPDFDictionary):
    validate: Incomplete

class PDFStreamFilterZCompress:
    pdfname: str
    def encode(self, text): ...
    def decode(self, encoded): ...

PDFZCompress: Incomplete

class PDFStreamFilterBase85Encode:
    pdfname: str
    def encode(self, text): ...
    def decode(self, text): ...

PDFBase85Encode: Incomplete

class PDFStream(PDFObject):
    """set dictionary elements explicitly stream.dictionary[name]=value"""

    __RefOnly__: int
    dictionary: Incomplete
    content: Incomplete
    filters: Incomplete
    def __init__(self, dictionary=None, content=None, filters=None) -> None: ...
    def format(self, document): ...

def teststream(content=None): ...

teststreamcontent: str

class PDFArray(PDFObject):
    multiline: bool
    sequence: Incomplete
    def __init__(self, sequence) -> None: ...
    def References(self, document) -> None:
        """make all objects in sequence references"""

    def format(self, document, IND: bytes = b"\n "): ...

class PDFArrayCompact(PDFArray):
    multiline: bool

class PDFIndirectObject(PDFObject):
    __RefOnly__: int
    name: Incomplete
    content: Incomplete
    def __init__(self, name, content) -> None: ...
    def format(self, document): ...

class PDFObjectReference(PDFObject):
    name: Incomplete
    def __init__(self, name) -> None: ...
    def format(self, document): ...

class PDFFile(PDFObject):
    strings: Incomplete
    write: Incomplete
    offset: int
    def __init__(self, pdfVersion=(1, 3)) -> None: ...
    def closeOrReset(self) -> None: ...
    def add(self, s):
        """should be constructed as late as possible, return position where placed"""

    def format(self, document): ...

class PDFCrossReferenceSubsection(PDFObject):
    firstentrynumber: Incomplete
    idsequence: Incomplete
    def __init__(self, firstentrynumber, idsequence) -> None: ...
    def format(self, document):
        """id sequence should represent contiguous object nums else error. free numbers not supported (yet)"""

class PDFCrossReferenceTable(PDFObject):
    sections: Incomplete
    def __init__(self) -> None: ...
    def addsection(self, firstentry, ids) -> None: ...
    def format(self, document): ...

class PDFTrailer(PDFObject):
    startxref: Incomplete
    def __init__(self, startxref, Size=None, Prev=None, Root=None, Info=None, ID=None, Encrypt=None) -> None: ...
    def format(self, document): ...

class PDFCatalog(PDFObject):
    __Comment__: str
    __RefOnly__: int
    __Defaults__: Incomplete
    __NoDefault__: Incomplete
    __Refs__ = __NoDefault__
    def format(self, document): ...
    def showOutline(self) -> None: ...
    def showFullScreen(self) -> None: ...
    PageLayout: Incomplete
    def setPageLayout(self, layout) -> None: ...
    PageMode: Incomplete
    def setPageMode(self, mode) -> None: ...
    def check_format(self, document) -> None:
        """for use in subclasses"""

class PDFPages(PDFCatalog):
    """PAGES TREE WITH ONE INTERNAL NODE, FOR "BALANCING" CHANGE IMPLEMENTATION"""

    __Comment__: str
    __RefOnly__: int
    __Defaults__: Incomplete
    __NoDefault__: Incomplete
    __Refs__: Incomplete
    pages: Incomplete
    def __init__(self) -> None: ...
    def __getitem__(self, item): ...
    def addPage(self, page) -> None: ...
    Kids: Incomplete
    Count: Incomplete
    def check_format(self, document) -> None: ...

class PDFPage(PDFCatalog):
    __Comment__: str
    Override_default_compilation: int
    __RefOnly__: int
    __Defaults__: Incomplete
    __NoDefault__: Incomplete
    __Refs__: Incomplete
    pagewidth: int
    pageheight: int
    stream: Incomplete
    hasImages: int
    compression: int
    XObjects: Incomplete
    Trans: Incomplete
    def __init__(self) -> None: ...
    def setCompression(self, onoff) -> None: ...
    def setStream(self, code) -> None: ...
    def setPageTransition(self, tranDict) -> None: ...
    MediaBox: Incomplete
    Annots: Incomplete
    Contents: Incomplete
    Resources: Incomplete
    Parent: Incomplete
    def check_format(self, document) -> None: ...

class DuplicatePageLabelPage(Exception): ...

class PDFPageLabels(PDFCatalog):
    __comment__: Incomplete
    __RefOnly__: int
    __Defaults__: Incomplete
    __NoDefault__: Incomplete
    __Refs__: Incomplete
    labels: Incomplete
    def __init__(self) -> None: ...
    def addPageLabel(self, page, label) -> None:
        """Adds a new PDFPageLabel to this catalog.
        The 'page' argument, an integer, is the page number in the PDF document
        with which the 'label' should be associated. Page numbering in the PDF
        starts at zero! Thus, to change the label on the first page, '0' should be
        provided as an argument, and to change the 6th page, '5' should be provided
        as the argument.

        The 'label' argument should be a PDFPageLabel instance, which describes the
        format of the labels starting on page 'page' in the PDF and continuing
        until the next encounter of a PDFPageLabel.

        The order in which labels are added is not important.
        """
    Nums: Incomplete
    def format(self, document): ...

class PDFPageLabel(PDFCatalog):
    __Comment__: Incomplete
    __RefOnly__: int
    __Defaults__: Incomplete
    __NoDefault__: Incomplete
    __convertible__: str
    ARABIC: str
    ROMAN_UPPER: str
    ROMAN_LOWER: str
    LETTERS_UPPER: str
    LETTERS_LOWER: str
    S: Incomplete
    St: Incomplete
    P: Incomplete
    def __init__(self, style=None, start=None, prefix=None) -> None:
        """
        A PDFPageLabel changes the style of page numbering as displayed in a PDF
        viewer. PDF page labels have nothing to do with 'physical' page numbers
        printed on a canvas, but instead influence the 'logical' page numbers
        displayed by PDF viewers. However, when using roman numerals (i, ii,
        iii...) or page prefixes for appendecies (A.1, A.2...) on the physical
        pages PDF page labels are necessary to change the logical page numbers
        displayed by the PDF viewer to match up with the physical numbers. A
        PDFPageLabel changes the properties of numbering at the page on which it
        appears (see the class 'PDFPageLabels' for specifying where a PDFPageLabel
        is associated) and all subsequent pages, until a new PDFPageLabel is
        encountered.

        The arguments to this initialiser determine the properties of all
        subsequent page labels. 'style' determines the numberings style, arabic,
        roman, letters; 'start' specifies the starting number; and 'prefix' any
        prefix to be applied to the page numbers. All these arguments can be left
        out or set to None.

        * style:

            - None:                       No numbering, can be used to display the prefix only.
            - PDFPageLabel.ARABIC:        Use arabic numbers: 1, 2, 3, 4...
            - PDFPageLabel.ROMAN_UPPER:   Use upper case roman numerals: I, II, III...
            - PDFPageLabel.ROMAN_LOWER:   Use lower case roman numerals: i, ii, iii...
            - PDFPageLabel.LETTERS_UPPER: Use upper case letters: A, B, C, D...
            - PDFPageLabel.LETTERS_LOWER: Use lower case letters: a, b, c, d...

        * start:

            -   An integer specifying the starting number for this PDFPageLabel. This
                can be used when numbering style changes to reset the page number back
                to one, ie from roman to arabic, or from arabic to appendecies. Can be
                any positive integer or None. I'm not sure what the effect of
                specifying None is, probably that page numbering continues with the
                current sequence, I'd have to check the spec to clarify though.

        * prefix:

            -   A string which is prefixed to the page numbers. Can be used to display
                appendecies in the format: A.1, A.2, ..., B.1, B.2, ... where a
                PDFPageLabel is used to set the properties for the first page of each
                appendix to restart the page numbering at one and set the prefix to the
                appropriate letter for current appendix. The prefix can also be used to
                display text only, if the 'style' is set to None. This can be used to
                display strings such as 'Front', 'Back', or 'Cover' for the covers on
                books.

        """

    def __lt__(self, oth): ...

def testpage(document) -> None: ...

DUMMYOUTLINE: str

class PDFOutlines0(PDFObject):
    __Comment__: str
    text: Incomplete
    __RefOnly__: int
    def format(self, document): ...

class OutlineEntryObject(PDFObject):
    """an entry in an outline"""

    Title: Incomplete
    Dest: Incomplete
    Parent: Incomplete
    Prev: Incomplete
    Next: Incomplete
    First: Incomplete
    Last: Incomplete
    Count: Incomplete
    def format(self, document): ...

class PDFOutlines(PDFObject):
    """
    takes a recursive list of outline destinations like::

        out = PDFOutline1()
        out.setNames(canvas, # requires canvas for name resolution
        "chapter1dest",
        ("chapter2dest",
        ["chapter2section1dest",
        "chapter2section2dest",
        "chapter2conclusiondest"]
        ), # end of chapter2 description
        "chapter3dest",
        ("chapter4dest", ["c4s1", "c4s2"])
        )

    Higher layers may build this structure incrementally. KISS at base level.
    """

    mydestinations: Incomplete
    ready: Incomplete
    counter: int
    currentlevel: int
    destinationnamestotitles: Incomplete
    destinationstotitles: Incomplete
    levelstack: Incomplete
    buildtree: Incomplete
    closedict: Incomplete
    def __init__(self) -> None: ...
    def addOutlineEntry(self, destinationname, level: int = 0, title=None, closed=None) -> None:
        """destinationname of None means "close the tree" """

    def setDestinations(self, destinationtree) -> None: ...
    def format(self, document): ...
    def setNames(self, canvas, *nametree) -> None: ...
    def setNameList(self, canvas, nametree) -> None:
        """Explicit list so I don't need to do in the caller"""

    def translateNames(self, canvas, object):
        """recursively translate tree of names into tree of destinations"""
    first: Incomplete
    count: int
    def prepare(self, document, canvas) -> None:
        """prepare all data structures required for save operation (create related objects)"""

    def maketree(self, document, destinationtree, Parent=None, toplevel: int = 0): ...

def count(tree, closedict=None):
    """utility for outline: recursively count leaves in a tuple/list tree"""

class PDFInfo(PDFObject):
    """PDF documents can have basic information embedded, viewable from
    File | Document Info in Acrobat Reader.  If this is wrong, you get
    Postscript errors while printing, even though it does not print.
    """

    producer: Incomplete
    creator: str
    title: str
    author: str
    subject: str
    keywords: str
    trapped: str
    def __init__(self) -> None: ...
    def digest(self, md5object) -> None: ...
    def format(self, document): ...
    def copy(self):
        """shallow copy - useful in pagecatchering"""

class Annotation(PDFObject):
    """superclass for all annotations."""

    defaults: Incomplete
    required: Incomplete
    permitted: Incomplete
    def cvtdict(self, d, escape: int = 1):
        """transform dict args from python form to pdf string rep as needed"""

    def AnnotationDict(self, **kw): ...
    def Dict(self) -> None: ...
    def format(self, document): ...

class FreeTextAnnotation(Annotation):
    permitted: Incomplete
    Rect: Incomplete
    Contents: Incomplete
    DA: Incomplete
    otherkw: Incomplete
    def __init__(self, Rect, Contents, DA, **kw) -> None: ...
    def Dict(self): ...

class LinkAnnotation(Annotation):
    permitted: Incomplete
    Border: Incomplete
    Rect: Incomplete
    Contents: Incomplete
    Destination: Incomplete
    otherkw: Incomplete
    def __init__(self, Rect, Contents, Destination, Border: str = "[0 0 1]", **kw) -> None: ...
    def dummyDictString(self): ...
    def Dict(self): ...

class HighlightAnnotation(Annotation):
    """
    HighlightAnnotation is an annotation that highlights the selected area.

    Rect is the mouseover area that will show the contents.

    QuadPoints is a list of points to highlight, you can have many groups of
    four QuadPoints to allow highlighting many lines.
    """

    permitted: Incomplete
    Rect: Incomplete
    Contents: Incomplete
    otherkw: Incomplete
    QuadPoints: Incomplete
    Color: Incomplete
    def __init__(self, Rect, Contents, QuadPoints, Color=[0.83, 0.89, 0.95], **kw) -> None: ...
    def cvtdict(self, d, escape: int = 1):
        """transform dict args from python form to pdf string rep as needed"""

    def Dict(self): ...

class TextAnnotation(HighlightAnnotation):
    permitted: Incomplete
    def __init__(self, Rect, Contents, **kw) -> None: ...
    def Dict(self): ...

def rect_to_quad(Rect):
    """
    Utility method to convert a Rect to a QuadPoint
    """

class PDFRectangle(PDFObject):
    def __init__(self, llx, lly, urx, ury) -> None: ...
    def format(self, document): ...

class PDFDate(PDFObject):
    dateFormatter: Incomplete
    def __init__(self, ts=None, dateFormatter=None) -> None: ...
    def format(self, doc): ...

class Destination(PDFObject):
    """

    not a PDFObject!  This is a placeholder that can delegates
    to a pdf object only after it has been defined by the methods
    below.

    EG a Destination can refer to Appendix A before it has been
    defined, but only if Appendix A is explicitly noted as a destination
    and resolved before the document is generated...

    For example the following sequence causes resolution before doc generation.
        d = Destination()
        d.fit() # or other format defining method call
        d.setPage(p)
        (at present setPageRef is called on generation of the page).
    """

    representation: None
    page: None
    name: Incomplete
    fmt: Incomplete
    def __init__(self, name) -> None: ...
    def format(self, document): ...
    def xyz(self, left, top, zoom) -> None: ...
    def fit(self) -> None: ...
    def fitb(self) -> None: ...
    def fith(self, top) -> None: ...
    def fitv(self, left) -> None: ...
    def fitbh(self, top) -> None: ...
    def fitbv(self, left) -> None: ...
    def fitr(self, left, bottom, right, top) -> None: ...
    def setPage(self, page) -> None: ...

class PDFDestinationXYZ(PDFObject):
    typename: str
    page: Incomplete
    top: Incomplete
    zoom: Incomplete
    left: Incomplete
    def __init__(self, page, left, top, zoom) -> None: ...
    def format(self, document): ...

class PDFDestinationFit(PDFObject):
    typename: str
    page: Incomplete
    def __init__(self, page) -> None: ...
    def format(self, document): ...

class PDFDestinationFitB(PDFDestinationFit):
    typename: str

class PDFDestinationFitH(PDFObject):
    typename: str
    page: Incomplete
    top: Incomplete
    def __init__(self, page, top) -> None: ...
    def format(self, document): ...

class PDFDestinationFitBH(PDFDestinationFitH):
    typename: str

class PDFDestinationFitV(PDFObject):
    typename: str
    page: Incomplete
    left: Incomplete
    def __init__(self, page, left) -> None: ...
    def format(self, document): ...

class PDFDestinationFitBV(PDFDestinationFitV):
    typename: str

class PDFDestinationFitR(PDFObject):
    typename: str
    page: Incomplete
    left: Incomplete
    bottom: Incomplete
    right: Incomplete
    top: Incomplete
    def __init__(self, page, left, bottom, right, top) -> None: ...
    def format(self, document): ...

class PDFResourceDictionary(PDFObject):
    """each element *could* be reset to a reference if desired"""

    ProcSet: Incomplete
    def __init__(self, **kwds) -> None: ...
    stdprocs: Incomplete
    dict_attributes: Incomplete
    def allProcs(self) -> None: ...
    def basicProcs(self) -> None: ...
    Font: Incomplete
    def basicFonts(self) -> None: ...
    def setColorSpace(self, colorsUsed) -> None: ...
    def setShading(self, shadingUsed) -> None: ...
    def format(self, document): ...

class PDFType1Font(PDFObject):
    """no init: set attributes explicitly"""

    __RefOnly__: int
    name_attributes: Incomplete
    Type: str
    Subtype: str
    local_attributes: Incomplete
    def format(self, document): ...

class PDFTrueTypeFont(PDFType1Font):
    Subtype: str

class PDFFormXObject(PDFObject):
    XObjects: Incomplete
    Annots: Incomplete
    BBox: Incomplete
    Matrix: Incomplete
    Contents: Incomplete
    stream: Incomplete
    Resources: Incomplete
    hasImages: int
    compression: int
    lowerx: Incomplete
    lowery: Incomplete
    upperx: Incomplete
    uppery: Incomplete
    def __init__(self, lowerx, lowery, upperx, uppery) -> None: ...
    def setStreamList(self, data) -> None: ...
    def BBoxList(self):
        """get the declared bounding box for the form as a list"""

    def format(self, document): ...

class PDFPostScriptXObject(PDFObject):
    """For embedding PD (e.g. tray commands) in PDF"""

    content: Incomplete
    def __init__(self, content=None) -> None: ...
    def format(self, document): ...

class PDFImageXObject(PDFObject):
    name: Incomplete
    width: int
    height: int
    bitsPerComponent: int
    colorSpace: str
    streamContent: str
    mask: Incomplete
    def __init__(self, name, source=None, mask=None) -> None: ...
    def loadImageFromA85(self, source): ...
    def loadImageFromJPEG(self, imageFile): ...
    def loadImageFromRaw(self, source): ...
    def loadImageFromSRC(self, im) -> None:
        """Extracts the stream, width and height"""

    def format(self, document): ...

class PDFSeparationCMYKColor:
    cmyk: Incomplete
    def __init__(self, cmyk) -> None: ...
    def value(self): ...

class PDFFunction(PDFObject):
    """superclass for all function types."""

    defaults: Incomplete
    required: Incomplete
    permitted: Incomplete
    def FunctionDict(self, **kw): ...
    def Dict(self, document) -> None: ...
    def format(self, document): ...

class PDFExponentialFunction(PDFFunction):
    defaults: Incomplete
    required: Incomplete
    permitted: Incomplete
    C0: Incomplete
    C1: Incomplete
    N: Incomplete
    otherkw: Incomplete
    def __init__(self, C0, C1, N, **kw) -> None: ...
    def Dict(self, document): ...

class PDFStitchingFunction(PDFFunction):
    required: Incomplete
    permitted: Incomplete
    Functions: Incomplete
    Bounds: Incomplete
    Encode: Incomplete
    otherkw: Incomplete
    def __init__(self, Functions, Bounds, Encode, **kw) -> None: ...
    def Dict(self, document): ...

class PDFShading(PDFObject):
    """superclass for all shading types."""

    required: Incomplete
    permitted: Incomplete
    def ShadingDict(self, **kw): ...
    def Dict(self, document) -> None: ...
    def format(self, document): ...

class PDFFunctionShading(PDFShading):
    required: Incomplete
    permitted: Incomplete
    Function: Incomplete
    ColorSpace: Incomplete
    otherkw: Incomplete
    def __init__(self, Function, ColorSpace, **kw) -> None: ...
    def Dict(self, document): ...

class PDFAxialShading(PDFShading):
    required: Incomplete
    permitted: Incomplete
    Coords: Incomplete
    Function: Incomplete
    ColorSpace: Incomplete
    otherkw: Incomplete
    def __init__(self, x0, y0, x1, y1, Function, ColorSpace, **kw) -> None: ...
    def Dict(self, document): ...

class PDFRadialShading(PDFShading):
    required: Incomplete
    permitted: Incomplete
    Coords: Incomplete
    Function: Incomplete
    ColorSpace: Incomplete
    otherkw: Incomplete
    def __init__(self, x0, y0, r0, x1, y1, r1, Function, ColorSpace, **kw) -> None: ...
    def Dict(self, document): ...

class XMP(PDFStream):
    def __init__(self, path=None, creator=None) -> None: ...
    def makeContent(self, doc): ...
    # Param name is changed from the base class:
    def format(self, doc): ...
