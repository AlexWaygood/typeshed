"""Diagnostic functions, mainly for use when doing tech support."""

from html.parser import HTMLParser

def diagnose(data) -> None:
    """Diagnostic suite for isolating common problems.

    :param data: A string containing markup that needs to be explained.
    :return: None; diagnostics are printed to standard output.
    """

def lxml_trace(data, html: bool = True, **kwargs) -> None:
    """Print out the lxml events that occur during parsing.

    This lets you see how lxml parses a document when no Beautiful
    Soup code is running. You can use this to determine whether
    an lxml-specific problem is in Beautiful Soup's lxml tree builders
    or in lxml itself.

    :param data: Some markup.
    :param html: If True, markup will be parsed with lxml's HTML parser.
       if False, lxml's XML parser will be used.
    """

class AnnouncingParser(HTMLParser):
    """Subclass of HTMLParser that announces parse events, without doing
    anything else.

    You can use this to get a picture of how html.parser sees a given
    document. The easiest way to do this is to call `htmlparser_trace`.
    """

    def handle_starttag(self, name, attrs) -> None: ...
    def handle_endtag(self, name) -> None: ...
    def handle_data(self, data) -> None: ...
    def handle_charref(self, name) -> None: ...
    def handle_entityref(self, name) -> None: ...
    def handle_comment(self, data) -> None: ...
    def handle_decl(self, data) -> None: ...
    def unknown_decl(self, data) -> None: ...
    def handle_pi(self, data) -> None: ...

def htmlparser_trace(data) -> None:
    """Print out the HTMLParser events that occur during parsing.

    This lets you see how HTMLParser parses a document when no
    Beautiful Soup code is running.

    :param data: Some markup.
    """

def rword(length: int = 5):
    """Generate a random word-like string."""

def rsentence(length: int = 4):
    """Generate a random sentence-like string."""

def rdoc(num_elements: int = 1000):
    """Randomly generate an invalid HTML document."""

def benchmark_parsers(num_elements: int = 100000) -> None:
    """Very basic head-to-head performance benchmark."""

def profile(num_elements: int = 100000, parser: str = "lxml") -> None:
    """Use Python's profiler on a randomly generated document."""
