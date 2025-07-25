from _typeshed import Incomplete
from typing import Literal, overload
from xml.etree.ElementTree import Element

from ._inputstream import _InputStream
from ._tokenizer import HTMLTokenizer
from .treebuilders.base import TreeBuilder

@overload
def parse(doc: _InputStream, treebuilder: Literal["etree"] = "etree", namespaceHTMLElements: bool = True, **kwargs) -> Element:
    """Parse an HTML document as a string or file-like object into a tree

    :arg doc: the document to parse as a string or file-like object

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5parser import parse
    >>> parse('<html><body><p>This is a doc</p></body></html>')
    <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

    """

@overload
def parse(doc: _InputStream, treebuilder: str, namespaceHTMLElements: bool = True, **kwargs): ...
def parseFragment(
    doc: _InputStream, container: str = "div", treebuilder: str = "etree", namespaceHTMLElements: bool = True, **kwargs
):
    """Parse an HTML fragment as a string or file-like object into a tree

    :arg doc: the fragment to parse as a string or file-like object

    :arg container: the container context to parse the fragment in

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5libparser import parseFragment
    >>> parseFragment('<b>this is a fragment</b>')
    <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

    """

def method_decorator_metaclass(function): ...

class HTMLParser:
    """HTML parser

    Generates a tree structure from a stream of (possibly malformed) HTML.

    """

    strict: bool
    tree: Incomplete
    errors: list[Incomplete]
    phases: Incomplete
    def __init__(
        self,
        tree: str | type[TreeBuilder] | None = None,
        strict: bool = False,
        namespaceHTMLElements: bool = True,
        debug: bool = False,
    ) -> None:
        """
        :arg tree: a treebuilder class controlling the type of tree that will be
            returned. Built in treebuilders can be accessed through
            html5lib.treebuilders.getTreeBuilder(treeType)

        :arg strict: raise an exception when a parse error is encountered

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        :arg debug: whether or not to enable debug mode which logs things

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()                     # generates parser with etree builder
        >>> parser = HTMLParser('lxml', strict=True)  # generates parser with lxml builder which is strict

        """
    firstStartTag: bool
    log: Incomplete
    compatMode: str
    container: str
    innerHTML: Incomplete
    phase: Incomplete
    lastPhase: Incomplete
    beforeRCDataPhase: Incomplete
    framesetOK: bool
    tokenizer: HTMLTokenizer
    def reset(self) -> None: ...
    @property
    def documentEncoding(self) -> str | None:
        """Name of the character encoding that was used to decode the input stream, or
        :obj:`None` if that is not determined yet

        """

    def isHTMLIntegrationPoint(self, element: Element) -> bool: ...
    def isMathMLTextIntegrationPoint(self, element: Element) -> bool: ...
    def mainLoop(self) -> None: ...
    def parse(self, stream: _InputStream, scripting: bool = ..., **kwargs):
        """Parse a HTML document into a well-formed tree

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element).

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parse('<html><body><p>This is a doc</p></body></html>')
        <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

        """

    def parseFragment(self, stream: _InputStream, *args, **kwargs):
        """Parse a HTML fragment into a well-formed tree fragment

        :arg container: name of the element we're setting the innerHTML
            property if set to None, default to 'div'

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element)

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5libparser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parseFragment('<b>this is a fragment</b>')
        <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

        """

    def parseError(self, errorcode: str = "XXX-undefined-error", datavars=None) -> None: ...
    def adjustMathMLAttributes(self, token) -> None: ...
    def adjustSVGAttributes(self, token) -> None: ...
    def adjustForeignAttributes(self, token) -> None: ...
    def reparseTokenNormal(self, token) -> None: ...
    def resetInsertionMode(self) -> None: ...
    originalPhase: Incomplete
    def parseRCDataRawtext(self, token, contentType) -> None: ...

def getPhases(debug): ...
def adjust_attributes(token, replacements) -> None: ...
def impliedTagToken(name, type: str = "EndTag", attributes=None, selfClosing: bool = False): ...

class ParseError(Exception):
    """Error in parsed document"""
