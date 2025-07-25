"""Use the HTMLParser library to parse HTML files that aren't too bad."""

from html.parser import HTMLParser
from typing import Any

from bs4.builder import HTMLTreeBuilder

class BeautifulSoupHTMLParser(HTMLParser):
    """A subclass of the Python standard library's HTMLParser class, which
    listens for HTMLParser events and translates them into calls
    to Beautiful Soup's tree construction API.
    """

    IGNORE: str
    REPLACE: str
    on_duplicate_attribute: Any
    already_closed_empty_element: Any
    def __init__(self, *args, **kwargs) -> None:
        """Constructor.

        :param on_duplicate_attribute: A strategy for what to do if a
            tag includes the same attribute more than once. Accepted
            values are: REPLACE (replace earlier values with later
            ones, the default), IGNORE (keep the earliest value
            encountered), or a callable. A callable must take three
            arguments: the dictionary of attributes already processed,
            the name of the duplicate attribute, and the most recent value
            encountered.
        """

    def handle_startendtag(self, name, attrs) -> None:
        """Handle an incoming empty-element tag.

        This is only called when the markup looks like <tag/>.

        :param name: Name of the tag.
        :param attrs: Dictionary of the tag's attributes.
        """

    def handle_starttag(self, name, attrs, handle_empty_element: bool = True) -> None:
        """Handle an opening tag, e.g. '<tag>'

        :param name: Name of the tag.
        :param attrs: Dictionary of the tag's attributes.
        :param handle_empty_element: True if this tag is known to be
            an empty-element tag (i.e. there is not expected to be any
            closing tag).
        """

    def handle_endtag(self, name, check_already_closed: bool = True) -> None:
        """Handle a closing tag, e.g. '</tag>'

        :param name: A tag name.
        :param check_already_closed: True if this tag is expected to
           be the closing portion of an empty-element tag,
           e.g. '<tag></tag>'.
        """

    def handle_data(self, data) -> None:
        """Handle some textual data that shows up between tags."""

    def handle_charref(self, name) -> None:
        """Handle a numeric character reference by converting it to the
        corresponding Unicode character and treating it as textual
        data.

        :param name: Character number, possibly in hexadecimal.
        """

    def handle_entityref(self, name) -> None:
        """Handle a named entity reference by converting it to the
        corresponding Unicode character(s) and treating it as textual
        data.

        :param name: Name of the entity reference.
        """

    def handle_comment(self, data) -> None:
        """Handle an HTML comment.

        :param data: The text of the comment.
        """

    def handle_decl(self, data) -> None:
        """Handle a DOCTYPE declaration.

        :param data: The text of the declaration.
        """

    def unknown_decl(self, data) -> None:
        """Handle a declaration of unknown type -- probably a CDATA block.

        :param data: The text of the declaration.
        """

    def handle_pi(self, data) -> None:
        """Handle a processing instruction.

        :param data: The text of the instruction.
        """

class HTMLParserTreeBuilder(HTMLTreeBuilder):
    """A Beautiful soup `TreeBuilder` that uses the `HTMLParser` parser,
    found in the Python standard library.
    """

    is_xml: bool
    picklable: bool
    NAME: Any
    features: Any
    TRACKS_LINE_NUMBERS: bool
    parser_args: Any
    def __init__(self, parser_args=None, parser_kwargs=None, **kwargs) -> None:
        """Constructor.

        :param parser_args: Positional arguments to pass into
            the BeautifulSoupHTMLParser constructor, once it's
            invoked.
        :param parser_kwargs: Keyword arguments to pass into
            the BeautifulSoupHTMLParser constructor, once it's
            invoked.
        :param kwargs: Keyword arguments for the superclass constructor.
        """

    def prepare_markup(
        self, markup, user_specified_encoding=None, document_declared_encoding=None, exclude_encodings=None
    ) -> None:
        """Run any preliminary steps necessary to make incoming markup
        acceptable to the parser.

        :param markup: Some markup -- probably a bytestring.
        :param user_specified_encoding: The user asked to try this encoding.
        :param document_declared_encoding: The markup itself claims to be
            in this encoding.
        :param exclude_encodings: The user asked _not_ to try any of
            these encodings.

        :yield: A series of 4-tuples:
         (markup, encoding, declared encoding,
          has undergone character replacement)

         Each 4-tuple represents a strategy for converting the
         document to Unicode and parsing it. Each strategy will be tried
         in turn.
        """

    def feed(self, markup) -> None:
        """Run some incoming markup through some parsing process,
        populating the `BeautifulSoup` object in self.soup.
        """
