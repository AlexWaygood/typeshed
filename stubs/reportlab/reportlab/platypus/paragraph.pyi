"""The standard paragraph implementation"""

from reportlab.lib.abag import ABag
from reportlab.lib.styles import ParagraphStyle, PropertySet
from reportlab.pdfgen.textobject import PDFTextObject
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paraparser import ParaFrag

class ParaLines(ABag):
    """
    class ParaLines contains the broken into lines representation of Paragraphs
        kind=0  Simple
        fontName, fontSize, textColor apply to whole Paragraph
        lines   [(extraSpace1,words1),....,(extraspaceN,wordsN)]

        kind==1 Complex
        lines   [FragLine1,...,FragLineN]
    """

class FragLine(ABag):
    """
    class FragLine contains a styled line (ie a line with more than one style)::

        extraSpace  unused space for justification only
        wordCount   1+spaces in line for justification purposes
        words       [ParaFrags] style text lumps to be concatenated together
        fontSize    maximum fontSize seen on the line; not used at present,
                    but could be used for line spacing.
    """

def cleanBlockQuotedText(text: str, joiner: str = " ") -> str:
    """This is an internal utility which takes triple-
    quoted text form within the document and returns
    (hopefully) the paragraph the user intended originally.
    """

class Paragraph(Flowable):
    """Paragraph(text, style, bulletText=None, caseSensitive=1)
    text a string of stuff to go into the paragraph.
    style is a style definition as in reportlab.lib.styles.
    bulletText is an optional bullet defintion.
    caseSensitive set this to 0 if you want the markup tags and their attributes to be case-insensitive.

    This class is a flowable that can format a block of text
    into a paragraph with a given style.

    The paragraph Text can contain XML-like markup including the tags:
    <b> ... </b> - bold
    < u [color="red"] [width="pts"] [offset="pts"]> < /u > - underline
        width and offset can be empty meaning use existing canvas line width
        or with an f/F suffix regarded as a fraction of the font size
    < strike > < /strike > - strike through has the same parameters as underline
    <i> ... </i> - italics
    <u> ... </u> - underline
    <strike> ... </strike> - strike through
    <super> ... </super> - superscript
    <sub> ... </sub> - subscript
    <font name=fontfamily/fontname color=colorname size=float>
    <span name=fontfamily/fontname color=colorname backcolor=colorname size=float style=stylename>
    <onDraw name=callable label="a label"/>
    <index [name="callablecanvasattribute"] label="a label"/>
    <link>link text</link>
        attributes of links
            size/fontSize/uwidth/uoffset=num
            name/face/fontName=name
            fg/textColor/color/ucolor=color
            backcolor/backColor/bgcolor=color
            dest/destination/target/href/link=target
            underline=bool turn on underline
    <a>anchor text</a>
        attributes of anchors
            size/fontSize/uwidth/uoffset=num
            fontName=name
            fg/textColor/color/ucolor=color
            backcolor/backColor/bgcolor=color
            href=href
            underline="yes|no"
    <a name="anchorpoint"/>
    <unichar name="unicode character name"/>
    <unichar value="unicode code point"/>
    <img src="path" width="1in" height="1in" valign="bottom"/>
            width="w%" --> fontSize*w/100   idea from Roberto Alsina
            height="h%" --> linewidth*h/100 <ralsina@netmanagers.com.ar>

    The whole may be surrounded by <para> </para> tags

    The <b> and <i> tags will work for the built-in fonts (Helvetica
    /Times / Courier).  For other fonts you need to register a family
    of 4 fonts using reportlab.pdfbase.pdfmetrics.registerFont; then
    use the addMapping function to tell the library that these 4 fonts
    form a family e.g.
    from reportlab.lib.fonts import addMapping
    addMapping('Vera', 0, 0, 'Vera')    #normal
    addMapping('Vera', 0, 1, 'Vera-Italic')    #italic
    addMapping('Vera', 1, 0, 'Vera-Bold')    #bold
    addMapping('Vera', 1, 1, 'Vera-BoldItalic')    #italic and bold

    It will also be able to handle any MathML specified Greek characters.
    """

    text: str
    frags: list[ParaFrag]
    style: ParagraphStyle
    bulletText: str | None
    caseSensitive: int
    encoding: str
    def __init__(
        self,
        text: str,
        # NOTE: This should be a ParagraphStyle
        style: PropertySet | None = None,
        bulletText: str | None = None,
        frags: list[ParaFrag] | None = None,
        caseSensitive: int = 1,
        encoding: str = "utf8",
    ) -> None: ...
    def minWidth(self) -> float:
        """Attempt to determine a minimum sensible width"""

    def draw(self) -> None: ...
    def breakLines(self, width: float | list[float] | tuple[float, ...]) -> ParaLines | ParaFrag:
        """
        Returns a broken line structure. There are two cases

        A) For the simple case of a single formatting input fragment the output is
            A fragment specifier with
                - kind = 0
                - fontName, fontSize, leading, textColor
                - lines=  A list of lines

                        Each line has two items.

                        1. unused width in points
                        2. word list

        B) When there is more than one input formatting fragment the output is
            A fragment specifier with
               - kind = 1
               - lines=  A list of fragments each having fields
                            - extraspace (needed for justified)
                            - fontSize
                            - words=word list
                                each word is itself a fragment with
                                various settings
            in addition frags becomes a frag word list

        This structure can be used to easily draw paragraphs with the various alignments.
        You can supply either a single width or a list of widths; the latter will have its
        last item repeated until necessary. A 2-element list is useful when there is a
        different first line indent; a longer list could be created to facilitate custom wraps
        around irregular objects.
        """

    def breakLinesCJK(self, maxWidths: float | list[float] | tuple[float, ...]) -> ParaLines | ParaFrag:
        """Initially, the dumbest possible wrapping algorithm.
        Cannot handle font variations.
        """

    def beginText(self, x: float, y: float) -> PDFTextObject: ...
    def drawPara(self, debug: int = 0) -> None:
        """Draws a paragraph according to the given style.
        Returns the final y position at the bottom. Not safe for
        paragraphs without spaces e.g. Japanese; wrapping
        algorithm will go infinite.
        """

    def getPlainText(self, identify: bool | None = None) -> str:
        """Convenience function for templates which want access
        to the raw text, without XML tags.
        """

    def getActualLineWidths0(self) -> list[float]:
        """Convenience function; tells you how wide each line
        actually is.  For justified styles, this will be
        the same as the wrap width; for others it might be
        useful for seeing if paragraphs will fit in spaces.
        """

    @staticmethod
    def dumpFrags(frags, indent: int = 4, full: bool = False) -> str: ...

__all__ = ("Paragraph", "cleanBlockQuotedText", "ParaLines", "FragLine")
