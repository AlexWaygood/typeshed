from collections.abc import Callable
from typing_extensions import TypeAlias

from .dammit import EntitySubstitution as EntitySubstitution

_EntitySubstitution: TypeAlias = Callable[[str], str]

class Formatter(EntitySubstitution):
    """Describes a strategy to use when outputting a parse tree to a string.

    Some parts of this strategy come from the distinction between
    HTML4, HTML5, and XML. Others are configurable by the user.

    Formatters are passed in as the `formatter` argument to methods
    like `PageElement.encode`. Most people won't need to think about
    formatters, and most people who need to think about them can pass
    in one of these predefined strings as `formatter` rather than
    making a new Formatter object:

    For HTML documents:
     * 'html' - HTML entity substitution for generic HTML documents. (default)
     * 'html5' - HTML entity substitution for HTML5 documents, as
                 well as some optimizations in the way tags are rendered.
     * 'minimal' - Only make the substitutions necessary to guarantee
                   valid HTML.
     * None - Do not perform any substitution. This will be faster
              but may result in invalid markup.

    For XML documents:
     * 'html' - Entity substitution for XHTML documents.
     * 'minimal' - Only make the substitutions necessary to guarantee
                   valid XML. (default)
     * None - Do not perform any substitution. This will be faster
              but may result in invalid markup.
    """

    HTML: str
    XML: str
    HTML_DEFAULTS: dict[str, set[str]]
    language: str | None
    entity_substitution: _EntitySubstitution
    void_element_close_prefix: str | None
    cdata_containing_tags: list[str]
    empty_attributes_are_booleans: bool
    def __init__(
        self,
        language: str | None = None,
        entity_substitution: _EntitySubstitution | None = None,
        void_element_close_prefix: str | None = "/",
        cdata_containing_tags: list[str] | None = None,
        empty_attributes_are_booleans: bool = False,
        indent: int = 1,
    ) -> None:
        """Constructor.

        :param language: This should be Formatter.XML if you are formatting
           XML markup and Formatter.HTML if you are formatting HTML markup.

        :param entity_substitution: A function to call to replace special
           characters with XML/HTML entities. For examples, see
           bs4.dammit.EntitySubstitution.substitute_html and substitute_xml.
        :param void_element_close_prefix: By default, void elements
           are represented as <tag/> (XML rules) rather than <tag>
           (HTML rules). To get <tag>, pass in the empty string.
        :param cdata_containing_tags: The list of tags that are defined
           as containing CDATA in this dialect. For example, in HTML,
           <script> and <style> tags are defined as containing CDATA,
           and their contents should not be formatted.
        :param blank_attributes_are_booleans: Render attributes whose value
            is the empty string as HTML-style boolean attributes.
            (Attributes whose value is None are always rendered this way.)

        :param indent: If indent is a non-negative integer or string,
            then the contents of elements will be indented
            appropriately when pretty-printing. An indent level of 0,
            negative, or "" will only insert newlines. Using a
            positive integer indent indents that many spaces per
            level. If indent is a string (such as "\\t"), that string
            is used to indent each level. The default behavior is to
            indent one space per level.
        """

    def substitute(self, ns: str) -> str:
        """Process a string that needs to undergo entity substitution.
        This may be a string encountered in an attribute value or as
        text.

        :param ns: A string.
        :return: A string with certain characters replaced by named
           or numeric entities.
        """

    def attribute_value(self, value: str) -> str:
        """Process the value of an attribute.

        :param ns: A string.
        :return: A string with certain characters replaced by named
           or numeric entities.
        """

    def attributes(self, tag):
        """Reorder a tag's attributes however you want.

        By default, attributes are sorted alphabetically. This makes
        behavior consistent between Python 2 and Python 3, and preserves
        backwards compatibility with older versions of Beautiful Soup.

        If `empty_boolean_attributes` is True, then attributes whose
        values are set to the empty string will be treated as boolean
        attributes.
        """

class HTMLFormatter(Formatter):
    """A generic Formatter for HTML."""

    REGISTRY: dict[str, HTMLFormatter]
    def __init__(
        self,
        entity_substitution: _EntitySubstitution | None = ...,
        void_element_close_prefix: str | None = ...,
        cdata_containing_tags: list[str] | None = ...,
        empty_attributes_are_booleans: bool = False,
        indent: int = 1,
    ) -> None: ...

class XMLFormatter(Formatter):
    """A generic Formatter for XML."""

    REGISTRY: dict[str, XMLFormatter]
    def __init__(
        self,
        entity_substitution: _EntitySubstitution | None = ...,
        void_element_close_prefix: str | None = ...,
        cdata_containing_tags: list[str] | None = ...,
        empty_attributes_are_booleans: bool = False,
        indent: int = 1,
    ) -> None: ...
