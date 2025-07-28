from _typeshed import ReadableBuffer
from collections.abc import Callable, Iterable, Iterator
from re import Pattern
from typing import Any, Literal, TypeVar, overload
from typing_extensions import Self, TypeAlias

from . import BeautifulSoup
from .builder import TreeBuilder
from .formatter import Formatter, _EntitySubstitution

DEFAULT_OUTPUT_ENCODING: str
nonwhitespace_re: Pattern[str]
whitespace_re: Pattern[str]
PYTHON_SPECIFIC_ENCODINGS: set[str]

class NamespacedAttribute(str):
    """A namespaced string (e.g. 'xml:lang') that remembers the namespace
    ('xml') and the name ('lang') that were used to create it.
    """

    def __new__(cls, prefix: str, name: str | None = None, namespace: str | None = None) -> Self: ...

class AttributeValueWithCharsetSubstitution(str):
    """A stand-in object for a character encoding specified in HTML."""

class CharsetMetaAttributeValue(AttributeValueWithCharsetSubstitution):
    """A generic stand-in for the value of a meta tag's 'charset' attribute.

    When Beautiful Soup parses the markup '<meta charset="utf8">', the
    value of the 'charset' attribute will be one of these objects.
    """

    def __new__(cls, original_value): ...
    def encode(self, encoding: str) -> str:  # type: ignore[override]  # incompatible with str
        """When an HTML document is being encoded to a given encoding, the
        value of a meta tag's 'charset' is the name of the encoding.
        """

class ContentMetaAttributeValue(AttributeValueWithCharsetSubstitution):
    """A generic stand-in for the value of a meta tag's 'content' attribute.

    When Beautiful Soup parses the markup:
     <meta http-equiv="content-type" content="text/html; charset=utf8">

    The value of the 'content' attribute will be one of these objects.
    """

    CHARSET_RE: Pattern[str]
    def __new__(cls, original_value): ...
    def encode(self, encoding: str) -> str: ...  # type: ignore[override]  # incompatible with str

_T = TypeVar("_T")
_PageElementT = TypeVar("_PageElementT", bound=PageElement)
_SimpleStrainable: TypeAlias = str | bool | None | bytes | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
_Strainable: TypeAlias = _SimpleStrainable | Iterable[_SimpleStrainable]
_SimpleNormalizedStrainable: TypeAlias = str | bool | None | Pattern[str] | Callable[[str], bool] | Callable[[Tag], bool]
_NormalizedStrainable: TypeAlias = _SimpleNormalizedStrainable | Iterable[_SimpleNormalizedStrainable]

class PageElement:
    """Contains the navigational information for some part of the page:
    that is, its current location in the parse tree.

    NavigableString, Tag, etc. are all subclasses of PageElement.
    """

    parent: Tag | None
    previous_element: PageElement | None
    next_element: PageElement | None
    next_sibling: PageElement | None
    previous_sibling: PageElement | None
    def setup(
        self,
        parent: Tag | None = None,
        previous_element: PageElement | None = None,
        next_element: PageElement | None = None,
        previous_sibling: PageElement | None = None,
        next_sibling: PageElement | None = None,
    ) -> None:
        """Sets up the initial relations between this element and
        other elements.

        :param parent: The parent of this element.

        :param previous_element: The element parsed immediately before
            this one.

        :param next_element: The element parsed immediately before
            this one.

        :param previous_sibling: The most recently encountered element
            on the same level of the parse tree as this one.

        :param previous_sibling: The next element to be encountered
            on the same level of the parse tree as this one.
        """

    def format_string(self, s: str, formatter: Formatter | str | None) -> str:
        """Format the given string using the given formatter.

        :param s: A string.
        :param formatter: A Formatter object, or a string naming one of the standard formatters.
        """

    def formatter_for_name(self, formatter: Formatter | str | _EntitySubstitution):
        """Look up or create a Formatter for the given identifier,
        if necessary.

        :param formatter: Can be a Formatter object (used as-is), a
            function (used as the entity substitution hook for an
            XMLFormatter or HTMLFormatter), or a string (used to look
            up an XMLFormatter or HTMLFormatter in the appropriate
            registry.
        """
    nextSibling: PageElement | None
    previousSibling: PageElement | None
    @property
    def stripped_strings(self) -> Iterator[str]:
        """Yield all strings in this PageElement, stripping them first.

        :yield: A sequence of stripped strings.
        """

    def get_text(self, separator: str = "", strip: bool = False, types: tuple[type[NavigableString], ...] = ...) -> str:
        """Get all child strings of this PageElement, concatenated using the
        given separator.

        :param separator: Strings will be concatenated using this separator.

        :param strip: If True, strings will be stripped before being
            concatenated.

        :param types: A tuple of NavigableString subclasses. Any
            strings of a subclass not found in this list will be
            ignored. Although there are exceptions, the default
            behavior in most cases is to consider only NavigableString
            and CData objects. That means no comments, processing
            instructions, etc.

        :return: A string.
        """
    getText = get_text
    @property
    def text(self) -> str:
        """Get all child strings of this PageElement, concatenated using the
        given separator.

        :param separator: Strings will be concatenated using this separator.

        :param strip: If True, strings will be stripped before being
            concatenated.

        :param types: A tuple of NavigableString subclasses. Any
            strings of a subclass not found in this list will be
            ignored. Although there are exceptions, the default
            behavior in most cases is to consider only NavigableString
            and CData objects. That means no comments, processing
            instructions, etc.

        :return: A string.
        """

    def replace_with(self, *args: PageElement | str) -> Self:
        """Replace this PageElement with one or more PageElements, keeping the
        rest of the tree the same.

        :param args: One or more PageElements.
        :return: `self`, no longer part of the tree.
        """
    replaceWith = replace_with
    def unwrap(self) -> Self:
        """Replace this PageElement with its contents.

        :return: `self`, no longer part of the tree.
        """
    replace_with_children = unwrap
    replaceWithChildren = unwrap
    def wrap(self, wrap_inside: _PageElementT) -> _PageElementT:
        """Wrap this PageElement inside another one.

        :param wrap_inside: A PageElement.
        :return: `wrap_inside`, occupying the position in the tree that used
           to be occupied by `self`, and with `self` inside it.
        """

    def extract(self, _self_index: int | None = None) -> Self:
        """Destructively rips this element out of the tree.

        :param _self_index: The location of this element in its parent's
           .contents, if known. Passing this in allows for a performance
           optimization.

        :return: `self`, no longer part of the tree.
        """

    def insert(self, position: int, new_child: PageElement | str) -> None:
        """Insert a new PageElement in the list of this PageElement's children.

        This works the same way as `list.insert`.

        :param position: The numeric position that should be occupied
           in `self.children` by the new PageElement.
        :param new_child: A PageElement.
        """

    def append(self, tag: PageElement | str) -> None:
        """Appends the given PageElement to the contents of this one.

        :param tag: A PageElement.
        """

    def extend(self, tags: Iterable[PageElement | str]) -> None:
        """Appends the given PageElements to this one's contents.

        :param tags: A list of PageElements. If a single Tag is
            provided instead, this PageElement's contents will be extended
            with that Tag's contents.
        """

    def insert_before(self, *args: PageElement | str) -> None:
        """Makes the given element(s) the immediate predecessor of this one.

        All the elements will have the same parent, and the given elements
        will be immediately before this one.

        :param args: One or more PageElements.
        """

    def insert_after(self, *args: PageElement | str) -> None:
        """Makes the given element(s) the immediate successor of this one.

        The elements will have the same parent, and the given elements
        will be immediately after this one.

        :param args: One or more PageElements.
        """

    def find_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> Tag | NavigableString | None:
        """Find the first PageElement that matches the given criteria and
        appears later in the document than this PageElement.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findNext = find_next
    def find_all_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[PageElement]:
        """Find all PageElements that match the given criteria and appear
        later in the document than this PageElement.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet containing PageElements.
        """
    findAllNext = find_all_next
    def find_next_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> Tag | NavigableString | None:
        """Find the closest sibling to this PageElement that matches the
        given criteria and appears later in the document.

        All find_* methods take a common set of arguments. See the
        online documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findNextSibling = find_next_sibling
    def find_next_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[PageElement]:
        """Find all siblings of this PageElement that match the given criteria
        and appear later in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
    findNextSiblings = find_next_siblings
    fetchNextSiblings = find_next_siblings
    def find_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> Tag | NavigableString | None:
        """Look backwards in the document from this PageElement and find the
        first PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findPrevious = find_previous
    def find_all_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[PageElement]:
        """Look backwards in the document from this PageElement and find all
        PageElements that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
    findAllPrevious = find_all_previous
    fetchPrevious = find_all_previous
    def find_previous_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> Tag | NavigableString | None:
        """Returns the closest sibling to this PageElement that matches the
        given criteria and appears earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findPreviousSibling = find_previous_sibling
    def find_previous_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[PageElement]:
        """Returns all siblings to this PageElement that match the
        given criteria and appear earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
    findPreviousSiblings = find_previous_siblings
    fetchPreviousSiblings = find_previous_siblings
    def find_parent(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        **kwargs: _Strainable,
    ) -> Tag | None:
        """Find the closest parent of this PageElement that matches the given
        criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :kwargs: A dictionary of filters on attribute values.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findParent = find_parent
    def find_parents(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[Tag]:
        """Find all parents of this PageElement that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findParents = find_parents
    fetchParents = find_parents
    @property
    def next(self) -> Tag | NavigableString | None:
        """The PageElement, if any, that was parsed just after this one.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """

    @property
    def previous(self) -> Tag | NavigableString | None:
        """The PageElement, if any, that was parsed just before this one.

        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """

    @property
    def next_elements(self) -> Iterable[PageElement]:
        """All PageElements that were parsed after this one.

        :yield: A sequence of PageElements.
        """

    @property
    def next_siblings(self) -> Iterable[PageElement]:
        """All PageElements that are siblings of this one but were parsed
        later.

        :yield: A sequence of PageElements.
        """

    @property
    def previous_elements(self) -> Iterable[PageElement]:
        """All PageElements that were parsed before this one.

        :yield: A sequence of PageElements.
        """

    @property
    def previous_siblings(self) -> Iterable[PageElement]:
        """All PageElements that are siblings of this one but were parsed
        earlier.

        :yield: A sequence of PageElements.
        """

    @property
    def parents(self) -> Iterable[Tag]:
        """All PageElements that are parents of this PageElement.

        :yield: A sequence of PageElements.
        """

    @property
    def decomposed(self) -> bool:
        """Check whether a PageElement has been decomposed.

        :rtype: bool
        """

    def nextGenerator(self) -> Iterable[PageElement]: ...
    def nextSiblingGenerator(self) -> Iterable[PageElement]: ...
    def previousGenerator(self) -> Iterable[PageElement]: ...
    def previousSiblingGenerator(self) -> Iterable[PageElement]: ...
    def parentGenerator(self) -> Iterable[Tag]: ...

class NavigableString(str, PageElement):
    """A Python Unicode string that is part of a parse tree.

    When Beautiful Soup parses the markup <b>penguin</b>, it will
    create a NavigableString for the string "penguin".
    """

    PREFIX: str
    SUFFIX: str
    known_xml: bool | None
    def __new__(cls, value: str | ReadableBuffer) -> Self:
        """Create a new NavigableString.

        When unpickling a NavigableString, this method is called with
        the string in DEFAULT_OUTPUT_ENCODING. That encoding needs to be
        passed in to the superclass's __new__ or the superclass won't know
        how to handle non-ASCII characters.
        """

    def __copy__(self) -> Self:
        """A copy of a NavigableString can only be a deep copy, because
        only one PageElement can occupy a given place in a parse tree.
        """

    def __getnewargs__(self) -> tuple[str]: ...
    def output_ready(self, formatter: Formatter | str | None = "minimal") -> str:
        """Run the string through the provided formatter.

        :param formatter: A Formatter object, or a string naming one of the standard formatters.
        """

    @property
    def name(self) -> None:
        """Since a NavigableString is not a Tag, it has no .name.

        This property is implemented so that code like this doesn't crash
        when run on a mixture of Tag and NavigableString objects:
            [x.name for x in tag.children]
        """

    @property
    def strings(self) -> Iterable[str]:
        """Yield all strings of certain classes, possibly stripping them.

        This makes it easy for NavigableString to implement methods
        like get_text() as conveniences, creating a consistent
        text-extraction API across all PageElements.

        :param strip: If True, all strings will be stripped before being
            yielded.

        :param types: A tuple of NavigableString subclasses. If this
            NavigableString isn't one of those subclasses, the
            sequence will be empty. By default, the subclasses
            considered are NavigableString and CData objects. That
            means no comments, processing instructions, etc.

        :yield: A sequence that either contains this string, or is empty.

        """

class PreformattedString(NavigableString):
    """A NavigableString not subject to the normal formatting rules.

    This is an abstract class used for special kinds of strings such
    as comments (the Comment class) and CDATA blocks (the CData
    class).
    """

    PREFIX: str
    SUFFIX: str
    def output_ready(self, formatter: Formatter | str | None = None) -> str:
        """Make this string ready for output by adding any subclass-specific
            prefix or suffix.

        :param formatter: A Formatter object, or a string naming one
            of the standard formatters. The string will be passed into the
            Formatter, but only to trigger any side effects: the return
            value is ignored.

        :return: The string, with any subclass-specific prefix and
           suffix added on.
        """

class CData(PreformattedString):
    """A CDATA block."""

    PREFIX: str
    SUFFIX: str

class ProcessingInstruction(PreformattedString):
    """A SGML processing instruction."""

    PREFIX: str
    SUFFIX: str

class XMLProcessingInstruction(ProcessingInstruction):
    """An XML processing instruction."""

    PREFIX: str
    SUFFIX: str

class Comment(PreformattedString):
    """An HTML or XML comment."""

    PREFIX: str
    SUFFIX: str

class Declaration(PreformattedString):
    """An XML declaration."""

    PREFIX: str
    SUFFIX: str

class Doctype(PreformattedString):
    """A document type declaration."""

    @classmethod
    def for_name_and_ids(cls, name: str | None, pub_id: str, system_id: str) -> Doctype:
        """Generate an appropriate document type declaration for a given
        public ID and system ID.

        :param name: The name of the document's root element, e.g. 'html'.
        :param pub_id: The Formal Public Identifier for this document type,
            e.g. '-//W3C//DTD XHTML 1.1//EN'
        :param system_id: The system identifier for this document type,
            e.g. 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'

        :return: A Doctype.
        """
    PREFIX: str
    SUFFIX: str

class Stylesheet(NavigableString):
    """A NavigableString representing an stylesheet (probably
    CSS).

    Used to distinguish embedded stylesheets from textual content.
    """

class Script(NavigableString):
    """A NavigableString representing an executable script (probably
    Javascript).

    Used to distinguish executable code from textual content.
    """

class TemplateString(NavigableString):
    """A NavigableString representing a string found inside an HTML
    template embedded in a larger document.

    Used to distinguish such strings from the main body of the document.
    """

class Tag(PageElement):
    """Represents an HTML or XML tag that is part of a parse tree, along
    with its attributes and contents.

    When Beautiful Soup parses the markup <b>penguin</b>, it will
    create a Tag object representing the <b> tag.
    """

    parser_class: type[BeautifulSoup] | None
    name: str
    namespace: str | None
    prefix: str | None
    sourceline: int | None
    sourcepos: int | None
    known_xml: bool | None
    attrs: dict[str, str | Any]
    contents: list[PageElement]
    hidden: bool
    can_be_empty_element: bool | None
    cdata_list_attributes: list[str] | None
    preserve_whitespace_tags: list[str] | None
    def __init__(
        self,
        parser: BeautifulSoup | None = None,
        builder: TreeBuilder | None = None,
        name: str | None = None,
        namespace: str | None = None,
        prefix: str | None = None,
        attrs: dict[str, str] | None = None,
        parent: Tag | None = None,
        previous: PageElement | None = None,
        is_xml: bool | None = None,
        sourceline: int | None = None,
        sourcepos: int | None = None,
        can_be_empty_element: bool | None = None,
        cdata_list_attributes: list[str] | None = None,
        preserve_whitespace_tags: list[str] | None = None,
        interesting_string_types: type[NavigableString] | tuple[type[NavigableString], ...] | None = None,
        namespaces: dict[str, str] | None = None,
    ) -> None:
        """Basic constructor.

        :param parser: A BeautifulSoup object.
        :param builder: A TreeBuilder.
        :param name: The name of the tag.
        :param namespace: The URI of this Tag's XML namespace, if any.
        :param prefix: The prefix for this Tag's XML namespace, if any.
        :param attrs: A dictionary of this Tag's attribute values.
        :param parent: The PageElement to use as this Tag's parent.
        :param previous: The PageElement that was parsed immediately before
            this tag.
        :param is_xml: If True, this is an XML tag. Otherwise, this is an
            HTML tag.
        :param sourceline: The line number where this tag was found in its
            source document.
        :param sourcepos: The character position within `sourceline` where this
            tag was found.
        :param can_be_empty_element: If True, this tag should be
            represented as <tag/>. If False, this tag should be represented
            as <tag></tag>.
        :param cdata_list_attributes: A list of attributes whose values should
            be treated as CDATA if they ever show up on this tag.
        :param preserve_whitespace_tags: A list of tag names whose contents
            should have their whitespace preserved.
        :param interesting_string_types: This is a NavigableString
            subclass or a tuple of them. When iterating over this
            Tag's strings in methods like Tag.strings or Tag.get_text,
            these are the types of strings that are interesting enough
            to be considered. The default is to consider
            NavigableString and CData the only interesting string
            subtypes.
        :param namespaces: A dictionary mapping currently active
            namespace prefixes to URIs. This can be used later to
            construct CSS selectors.
        """
    parserClass: type[BeautifulSoup] | None
    def __copy__(self) -> Self:
        """A copy of a Tag must always be a deep copy, because a Tag's
        children can only have one parent at a time.
        """

    @property
    def is_empty_element(self) -> bool:
        """Is this tag an empty-element tag? (aka a self-closing tag)

        A tag that has contents is never an empty-element tag.

        A tag that has no contents may or may not be an empty-element
        tag. It depends on the builder used to create the tag. If the
        builder has a designated list of empty-element tags, then only
        a tag whose name shows up in that list is considered an
        empty-element tag.

        If the builder has no designated list of empty-element tags,
        then any tag with no contents is an empty-element tag.
        """

    @property
    def isSelfClosing(self) -> bool:
        """Is this tag an empty-element tag? (aka a self-closing tag)

        A tag that has contents is never an empty-element tag.

        A tag that has no contents may or may not be an empty-element
        tag. It depends on the builder used to create the tag. If the
        builder has a designated list of empty-element tags, then only
        a tag whose name shows up in that list is considered an
        empty-element tag.

        If the builder has no designated list of empty-element tags,
        then any tag with no contents is an empty-element tag.
        """

    @property
    def string(self) -> str | None:
        """Convenience property to get the single string within this
        PageElement.

        TODO It might make sense to have NavigableString.string return
        itself.

        :return: If this element has a single string child, return
         value is that string. If this element has one child tag,
         return value is the 'string' attribute of the child tag,
         recursively. If this element is itself a string, has no
         children, or has more than one child, return value is None.
        """

    @string.setter
    def string(self, string: str) -> None: ...
    DEFAULT_INTERESTING_STRING_TYPES: tuple[type[NavigableString], ...]
    @property
    def strings(self) -> Iterable[str]:
        """Yield all strings of certain classes, possibly stripping them.

        :param strip: If True, all strings will be stripped before being
            yielded.

        :param types: A tuple of NavigableString subclasses. Any strings of
            a subclass not found in this list will be ignored. By
            default, the subclasses considered are the ones found in
            self.interesting_string_types. If that's not specified,
            only NavigableString and CData objects will be
            considered. That means no comments, processing
            instructions, etc.

        :yield: A sequence of strings.

        """

    def decompose(self) -> None:
        """Recursively destroys this PageElement and its children.

        This element will be removed from the tree and wiped out; so
        will everything beneath it.

        The behavior of a decomposed PageElement is undefined and you
        should never use one for anything, but if you need to _check_
        whether an element has been decomposed, you can use the
        `decomposed` property.
        """

    def clear(self, decompose: bool = False) -> None:
        """Wipe out all children of this PageElement by calling extract()
           on them.

        :param decompose: If this is True, decompose() (a more
            destructive method) will be called instead of extract().
        """

    def smooth(self) -> None:
        """Smooth out this element's children by consolidating consecutive
        strings.

        This makes pretty-printed output look more natural following a
        lot of operations that modified the tree.
        """

    def index(self, element: PageElement) -> int:
        """Find the index of a child by identity, not value.

        Avoids issues with tag.contents.index(element) getting the
        index of equal elements.

        :param element: Look for this PageElement in `self.contents`.
        """

    @overload
    def get(self, key: str, default: None = None) -> str | list[str] | None:
        """Returns the value of the 'key' attribute for the tag, or
        the value given for 'default' if it doesn't have that
        attribute.
        """

    @overload
    def get(self, key: str, default: _T) -> str | list[str] | _T: ...
    @overload
    def get_attribute_list(self, key: str, default: None = None) -> list[str | None]:
        """The same as get(), but always returns a list.

        :param key: The attribute to look for.
        :param default: Use this value if the attribute is not present
            on this PageElement.
        :return: A list of values, probably containing only a single
            value.
        """

    @overload
    def get_attribute_list(self, key: str, default: list[_T]) -> list[str | _T]: ...
    @overload
    def get_attribute_list(self, key: str, default: _T) -> list[str | _T]: ...
    def has_attr(self, key: str) -> bool:
        """Does this PageElement have an attribute with the given name?"""

    def __hash__(self) -> int: ...
    def __getitem__(self, key: str) -> str | list[str]:
        """tag[key] returns the value of the 'key' attribute for the Tag,
        and throws an exception if it's not there.
        """

    def __iter__(self) -> Iterator[PageElement]:
        """Iterating over a Tag iterates over its contents."""

    def __len__(self) -> int:
        """The length of a Tag is the length of its list of contents."""

    def __contains__(self, x: object) -> bool: ...
    def __bool__(self) -> bool:
        """A tag is non-None even if it has no contents."""

    def __setitem__(self, key: str, value: str | list[str]) -> None:
        """Setting tag[key] sets the value of the 'key' attribute for the
        tag.
        """

    def __delitem__(self, key: str) -> None:
        """Deleting tag[key] deletes all 'key' attributes for the tag."""

    def __getattr__(self, tag: str) -> Tag | None:
        """Calling tag.subtag is the same as calling tag.find(name="subtag")"""

    def __eq__(self, other: object) -> bool:
        """Returns true iff this Tag has the same name, the same attributes,
        and the same contents (recursively) as `other`.
        """

    def __ne__(self, other: object) -> bool:
        """Returns true iff this Tag is not identical to `other`,
        as defined in __eq__.
        """

    def __unicode__(self) -> str:
        """Renders this PageElement as a Unicode string."""

    def encode(
        self,
        encoding: str = "utf-8",
        indent_level: int | None = None,
        formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal",
        errors: str = "xmlcharrefreplace",
    ) -> bytes:
        """Render a bytestring representation of this PageElement and its
        contents.

        :param encoding: The destination encoding.
        :param indent_level: Each line of the rendering will be
           indented this many levels. (The formatter decides what a
           'level' means in terms of spaces or other characters
           output.) Used internally in recursive calls while
           pretty-printing.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :param errors: An error handling strategy such as
            'xmlcharrefreplace'. This value is passed along into
            encode() and its value should be one of the constants
            defined by Python.
        :return: A bytestring.

        """

    def decode(
        self,
        indent_level: int | None = None,
        eventual_encoding: str = "utf-8",
        formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal",
        iterator: Iterator[PageElement] | None = None,
    ) -> str: ...
    @overload
    def prettify(self, encoding: str, formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal") -> bytes:
        """Pretty-print this PageElement as a string.

        :param encoding: The eventual encoding of the string. If this is None,
            a Unicode string will be returned.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :return: A Unicode string (if encoding==None) or a bytestring
            (otherwise).
        """

    @overload
    def prettify(
        self, encoding: None = None, formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal"
    ) -> str: ...
    def decode_contents(
        self,
        indent_level: int | None = None,
        eventual_encoding: str = "utf-8",
        formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal",
    ) -> str:
        """Renders the contents of this tag as a Unicode string.

        :param indent_level: Each line of the rendering will be
           indented this many levels. (The formatter decides what a
           'level' means in terms of spaces or other characters
           output.) Used internally in recursive calls while
           pretty-printing.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. decode_contents() is _not_
           responsible for performing that encoding. This information
           is passed in so that it can be substituted in if the
           document contains a <META> tag that mentions the document's
           encoding.

        :param formatter: A Formatter object, or a string naming one of
            the standard Formatters.

        """

    def encode_contents(
        self,
        indent_level: int | None = None,
        encoding: str = "utf-8",
        formatter: Literal["html", "html5", "minimal"] | Formatter | None = "minimal",
    ) -> bytes:
        """Renders the contents of this PageElement as a bytestring.

        :param indent_level: Each line of the rendering will be
           indented this many levels. (The formatter decides what a
           'level' means in terms of spaces or other characters
           output.) Used internally in recursive calls while
           pretty-printing.

        :param eventual_encoding: The bytestring will be in this encoding.

        :param formatter: A Formatter object, or a string naming one of
            the standard Formatters.

        :return: A bytestring.
        """

    def renderContents(self, encoding: str = "utf-8", prettyPrint: bool = False, indentLevel: int = 0) -> bytes:
        """Deprecated method for BS3 compatibility."""

    def find(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> Tag | NavigableString | None:
        """Look in the children of this PageElement and find the first
        PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A PageElement.
        :rtype: bs4.element.Tag | bs4.element.NavigableString
        """
    findChild = find
    def find_all(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> ResultSet[Any]:
        """Look in the children of this PageElement and find all
        PageElements that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param recursive: If this is True, find_all() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :kwargs: A dictionary of filters on attribute values.
        :return: A ResultSet of PageElements.
        :rtype: bs4.element.ResultSet
        """
    __call__ = find_all
    findAll = find_all
    findChildren = find_all
    @property
    def children(self) -> Iterable[PageElement]:
        """Iterate over all direct children of this PageElement.

        :yield: A sequence of PageElements.
        """

    @property
    def descendants(self) -> Iterable[PageElement]:
        """Iterate over all children of this PageElement in a
        breadth-first sequence.

        :yield: A sequence of PageElements.
        """

    def select_one(self, selector: str, namespaces=None, *, flags: int = ..., custom: dict[str, str] | None = ...) -> Tag | None:
        """Perform a CSS selection operation on the current element.

        :param selector: A CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param kwargs: Keyword arguments to be passed into Soup Sieve's
           soupsieve.select() method.

        :return: A Tag.
        :rtype: bs4.element.Tag
        """

    def select(
        self, selector: str, namespaces=None, limit: int | None = None, *, flags: int = ..., custom: dict[str, str] | None = ...
    ) -> ResultSet[Tag]:
        """Perform a CSS selection operation on the current element.

        This uses the SoupSieve library.

        :param selector: A string containing a CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param limit: After finding this number of results, stop looking.

        :param kwargs: Keyword arguments to be passed into SoupSieve's
           soupsieve.select() method.

        :return: A ResultSet of Tags.
        :rtype: bs4.element.ResultSet
        """

    def childGenerator(self) -> Iterable[PageElement]:
        """Deprecated generator."""

    def recursiveChildGenerator(self) -> Iterable[PageElement]:
        """Deprecated generator."""

    def has_key(self, key: str) -> bool:
        """Deprecated method. This was kind of misleading because has_key()
        (attributes) was different from __in__ (contents).

        has_key() is gone in Python 3, anyway.
        """

class SoupStrainer:
    """Encapsulates a number of ways of matching a markup element (tag or
    string).

    This is primarily used to underpin the find_* methods, but you can
    create one yourself and pass it in as `parse_only` to the
    `BeautifulSoup` constructor, to parse a subset of a large
    document.
    """

    name: _NormalizedStrainable
    attrs: dict[str, _NormalizedStrainable]
    string: _NormalizedStrainable
    def __init__(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> None:
        """Constructor.

        The SoupStrainer constructor takes the same arguments passed
        into the find_* methods. See the online documentation for
        detailed explanations.

        :param name: A filter on tag name.
        :param attrs: A dictionary of filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: A dictionary of filters on attribute values.
        """

    def search_tag(self, markup_name: Tag | str | None = None, markup_attrs={}):
        """Check whether a Tag with the given name and attributes would
        match this SoupStrainer.

        Used prospectively to decide whether to even bother creating a Tag
        object.

        :param markup_name: A tag name as found in some markup.
        :param markup_attrs: A dictionary of attributes as found in some markup.

        :return: True if the prospective tag would match this SoupStrainer;
            False otherwise.
        """
    searchTag = search_tag
    def search(self, markup: PageElement | Iterable[PageElement]):
        """Find all items in `markup` that match this SoupStrainer.

        Used by the core _find_all() method, which is ultimately
        called by all find_* methods.

        :param markup: A PageElement or a list of them.
        """

class ResultSet(list[_PageElementT]):
    """A ResultSet is just a list that keeps track of the SoupStrainer
    that created it.
    """

    source: SoupStrainer
    @overload
    def __init__(self, source: SoupStrainer) -> None:
        """Constructor.

        :param source: A SoupStrainer.
        :param result: A list of PageElements.
        """

    @overload
    def __init__(self, source: SoupStrainer, result: Iterable[_PageElementT]) -> None: ...
