from typing import Any

class TreeBuilderRegistry:
    """A way of looking up TreeBuilder subclasses by their name or by desired
    features.
    """

    builders_for_feature: Any
    builders: Any
    def __init__(self) -> None: ...
    def register(self, treebuilder_class) -> None:
        """Register a treebuilder based on its advertised features.

        :param treebuilder_class: A subclass of Treebuilder. its .features
           attribute should list its features.
        """

    def lookup(self, *features):
        """Look up a TreeBuilder subclass with the desired features.

        :param features: A list of features to look for. If none are
            provided, the most recently registered TreeBuilder subclass
            will be used.
        :return: A TreeBuilder subclass, or None if there's no
            registered subclass with all the requested features.
        """

class TreeBuilder:
    """Turn a textual document into a Beautiful Soup object tree."""

    NAME: str
    ALTERNATE_NAMES: Any
    features: Any
    is_xml: bool
    picklable: bool
    empty_element_tags: Any
    DEFAULT_CDATA_LIST_ATTRIBUTES: Any
    DEFAULT_PRESERVE_WHITESPACE_TAGS: Any
    DEFAULT_STRING_CONTAINERS: Any
    USE_DEFAULT: Any
    TRACKS_LINE_NUMBERS: bool
    soup: Any
    cdata_list_attributes: Any
    preserve_whitespace_tags: Any
    store_line_numbers: Any
    string_containers: Any
    def __init__(
        self, multi_valued_attributes=..., preserve_whitespace_tags=..., store_line_numbers=..., string_containers=...
    ) -> None:
        """Constructor.

        :param multi_valued_attributes: If this is set to None, the
         TreeBuilder will not turn any values for attributes like
         'class' into lists. Setting this to a dictionary will
         customize this behavior; look at DEFAULT_CDATA_LIST_ATTRIBUTES
         for an example.

         Internally, these are called "CDATA list attributes", but that
         probably doesn't make sense to an end-user, so the argument name
         is `multi_valued_attributes`.

        :param preserve_whitespace_tags: A list of tags to treat
         the way <pre> tags are treated in HTML. Tags in this list
         are immune from pretty-printing; their contents will always be
         output as-is.

        :param string_containers: A dictionary mapping tag names to
        the classes that should be instantiated to contain the textual
        contents of those tags. The default is to use NavigableString
        for every tag, no matter what the name. You can override the
        default by changing DEFAULT_STRING_CONTAINERS.

        :param store_line_numbers: If the parser keeps track of the
         line numbers and positions of the original markup, that
         information will, by default, be stored in each corresponding
         `Tag` object. You can turn this off by passing
         store_line_numbers=False. If the parser you're using doesn't
         keep track of this information, then setting store_line_numbers=True
         will do nothing.
        """

    def initialize_soup(self, soup) -> None:
        """The BeautifulSoup object has been initialized and is now
        being associated with the TreeBuilder.

        :param soup: A BeautifulSoup object.
        """

    def reset(self) -> None:
        """Do any work necessary to reset the underlying parser
        for a new document.

        By default, this does nothing.
        """

    def can_be_empty_element(self, tag_name):
        """Might a tag with this name be an empty-element tag?

        The final markup may or may not actually present this tag as
        self-closing.

        For instance: an HTMLBuilder does not consider a <p> tag to be
        an empty-element tag (it's not in
        HTMLBuilder.empty_element_tags). This means an empty <p> tag
        will be presented as "<p></p>", not "<p/>" or "<p>".

        The default implementation has no opinion about which tags are
        empty-element tags, so a tag will be presented as an
        empty-element tag if and only if it has no children.
        "<foo></foo>" will become "<foo/>", and "<foo>bar</foo>" will
        be left alone.

        :param tag_name: The name of a markup tag.
        """

    def feed(self, markup) -> None:
        """Run some incoming markup through some parsing process,
        populating the `BeautifulSoup` object in self.soup.

        This method is not implemented in TreeBuilder; it must be
        implemented in subclasses.

        :return: None.
        """

    def prepare_markup(
        self, markup, user_specified_encoding=None, document_declared_encoding=None, exclude_encodings=None
    ) -> None:
        """Run any preliminary steps necessary to make incoming markup
        acceptable to the parser.

        :param markup: Some markup -- probably a bytestring.
        :param user_specified_encoding: The user asked to try this encoding.
        :param document_declared_encoding: The markup itself claims to be
            in this encoding. NOTE: This argument is not used by the
            calling code and can probably be removed.
        :param exclude_encodings: The user asked _not_ to try any of
            these encodings.

        :yield: A series of 4-tuples:
         (markup, encoding, declared encoding,
          has undergone character replacement)

         Each 4-tuple represents a strategy for converting the
         document to Unicode and parsing it. Each strategy will be tried
         in turn.

         By default, the only strategy is to parse the markup
         as-is. See `LXMLTreeBuilderForXML` and
         `HTMLParserTreeBuilder` for implementations that take into
         account the quirks of particular parsers.
        """

    def test_fragment_to_document(self, fragment):
        """Wrap an HTML fragment to make it look like a document.

        Different parsers do this differently. For instance, lxml
        introduces an empty <head> tag, and html5lib
        doesn't. Abstracting this away lets us write simple tests
        which run HTML fragments through the parser and compare the
        results against other HTML fragments.

        This method should not be used outside of tests.

        :param fragment: A string -- fragment of HTML.
        :return: A string -- a full HTML document.
        """

    def set_up_substitutions(self, tag):
        """Set up any substitutions that will need to be performed on
        a `Tag` when it's output as a string.

        By default, this does nothing. See `HTMLTreeBuilder` for a
        case where this is used.

        :param tag: A `Tag`
        :return: Whether or not a substitution was performed.
        """

class SAXTreeBuilder(TreeBuilder):
    """A Beautiful Soup treebuilder that listens for SAX events.

    This is not currently used for anything, but it demonstrates
    how a simple TreeBuilder would work.
    """

    def feed(self, markup) -> None: ...
    def close(self) -> None: ...
    def startElement(self, name, attrs) -> None: ...
    def endElement(self, name) -> None: ...
    def startElementNS(self, nsTuple, nodeName, attrs) -> None: ...
    def endElementNS(self, nsTuple, nodeName) -> None: ...
    def startPrefixMapping(self, prefix, nodeValue) -> None: ...
    def endPrefixMapping(self, prefix) -> None: ...
    def characters(self, content) -> None: ...
    def startDocument(self) -> None: ...
    def endDocument(self) -> None: ...

class HTMLTreeBuilder(TreeBuilder):
    """This TreeBuilder knows facts about HTML.

    Such as which tags are empty-element tags.
    """

    empty_element_tags: Any
    block_elements: Any
    DEFAULT_STRING_CONTAINERS: Any
    DEFAULT_CDATA_LIST_ATTRIBUTES: Any
    DEFAULT_PRESERVE_WHITESPACE_TAGS: Any
    def set_up_substitutions(self, tag):
        """Replace the declared encoding in a <meta> tag with a placeholder,
        to be substituted when the tag is output to a string.

        An HTML document may come in to Beautiful Soup as one
        encoding, but exit in a different encoding, and the <meta> tag
        needs to be changed to reflect this.

        :param tag: A `Tag`
        :return: Whether or not a substitution was performed.
        """

class ParserRejectedMarkup(Exception):
    """An Exception to be raised when the underlying parser simply
    refuses to parse the given markup.
    """

    def __init__(self, message_or_exception) -> None:
        """Explain why the parser rejected the given markup, either
        with a textual explanation or another exception.
        """

class XMLParsedAsHTMLWarning(UserWarning):
    """The warning issued when an HTML parser is used to parse
    XML that is not XHTML.
    """
