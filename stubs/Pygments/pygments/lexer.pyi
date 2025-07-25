"""
pygments.lexer
~~~~~~~~~~~~~~

Base lexer classes.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from collections.abc import Iterable, Iterator, Sequence
from re import RegexFlag
from typing import ClassVar

from pygments.token import _TokenType
from pygments.util import Future

class LexerMeta(type):
    """
    This metaclass automagically converts ``analyse_text`` methods into
    static methods which always return float values.
    """

    def __new__(cls, name, bases, d): ...
    def analyse_text(self, text: str) -> float: ...  # actually defined in class Lexer
    # ClassVars of Lexer, but same situation as with StyleMeta and Style
    name: str
    aliases: Sequence[str]  # not intended mutable
    filenames: Sequence[str]
    alias_filenames: Sequence[str]
    mimetypes: Sequence[str]
    priority: float
    url: str | None

class Lexer(metaclass=LexerMeta):
    """
    Lexer for a specific language.

    See also :doc:`lexerdevelopment`, a high-level guide to writing
    lexers.

    Lexer classes have attributes used for choosing the most appropriate
    lexer based on various criteria.

    .. autoattribute:: name
       :no-value:
    .. autoattribute:: aliases
       :no-value:
    .. autoattribute:: filenames
       :no-value:
    .. autoattribute:: alias_filenames
    .. autoattribute:: mimetypes
       :no-value:
    .. autoattribute:: priority

    Lexers included in Pygments should have two additional attributes:

    .. autoattribute:: url
       :no-value:
    .. autoattribute:: version_added
       :no-value:

    Lexers included in Pygments may have additional attributes:

    .. autoattribute:: _example
       :no-value:

    You can pass options to the constructor. The basic options recognized
    by all lexers and processed by the base `Lexer` class are:

    ``stripnl``
        Strip leading and trailing newlines from the input (default: True).
    ``stripall``
        Strip all leading and trailing whitespace from the input
        (default: False).
    ``ensurenl``
        Make sure that the input ends with a newline (default: True).  This
        is required for some lexers that consume input linewise.

        .. versionadded:: 1.3

    ``tabsize``
        If given and greater than 0, expand tabs in the input (default: 0).
    ``encoding``
        If given, must be an encoding name. This encoding will be used to
        convert the input string to Unicode, if it is not already a Unicode
        string (default: ``'guess'``, which uses a simple UTF-8 / Locale /
        Latin1 detection.  Can also be ``'chardet'`` to use the chardet
        library, if it is installed.
    ``inencoding``
        Overrides the ``encoding`` if given.
    """

    options: Incomplete
    stripnl: Incomplete
    stripall: Incomplete
    ensurenl: Incomplete
    tabsize: Incomplete
    encoding: Incomplete
    filters: Incomplete
    def __init__(self, **options) -> None:
        """
        This constructor takes arbitrary options as keyword arguments.
        Every subclass must first process its own options and then call
        the `Lexer` constructor, since it processes the basic
        options like `stripnl`.

        An example looks like this:

        .. sourcecode:: python

           def __init__(self, **options):
               self.compress = options.get('compress', '')
               Lexer.__init__(self, **options)

        As these options must all be specifiable as strings (due to the
        command line usage), there are various utility functions
        available to help with that, see `Utilities`_.
        """

    def add_filter(self, filter_, **options) -> None:
        """
        Add a new stream filter to this lexer.
        """

    def get_tokens(self, text: str, unfiltered: bool = False) -> Iterator[tuple[_TokenType, str]]:
        """
        This method is the basic interface of a lexer. It is called by
        the `highlight()` function. It must process the text and return an
        iterable of ``(tokentype, value)`` pairs from `text`.

        Normally, you don't need to override this method. The default
        implementation processes the options recognized by all lexers
        (`stripnl`, `stripall` and so on), and then yields all tokens
        from `get_tokens_unprocessed()`, with the ``index`` dropped.

        If `unfiltered` is set to `True`, the filtering mechanism is
        bypassed even if filters are defined.
        """

    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]:
        """
        This method should process the text and return an iterable of
        ``(index, tokentype, value)`` tuples where ``index`` is the starting
        position of the token within the input text.

        It must be overridden by subclasses. It is recommended to
        implement it as a generator to maximize effectiveness.
        """

class DelegatingLexer(Lexer):
    """
    This lexer takes two lexer as arguments. A root lexer and
    a language lexer. First everything is scanned using the language
    lexer, afterwards all ``Other`` tokens are lexed using the root
    lexer.

    The lexers from the ``template`` lexer package use this base lexer.
    """

    root_lexer: Incomplete
    language_lexer: Incomplete
    needle: Incomplete
    def __init__(self, _root_lexer, _language_lexer, _needle=..., **options) -> None: ...
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...

class include(str):
    """
    Indicates that a state should include rules from another state.
    """

class _inherit:
    """
    Indicates the a state should inherit from its superclass.
    """

inherit: Incomplete

class combined(tuple[Incomplete, ...]):
    """
    Indicates a state combined from multiple states.
    """

    def __new__(cls, *args): ...
    def __init__(self, *args) -> None: ...

class _PseudoMatch:
    """
    A pseudo match object constructed from a string.
    """

    def __init__(self, start, text) -> None: ...
    def start(self, arg=None): ...
    def end(self, arg=None): ...
    def group(self, arg=None): ...
    def groups(self): ...
    def groupdict(self): ...

def bygroups(*args):
    """
    Callback that yields multiple actions for each group in the match.
    """

class _This:
    """
    Special singleton used for indicating the caller class.
    Used by ``using``.
    """

this: Incomplete

def using(_other, **kwargs):
    """
    Callback that processes the match with a different lexer.

    The keyword arguments are forwarded to the lexer, except `state` which
    is handled separately.

    `state` specifies the state that the new lexer will start in, and can
    be an enumerable such as ('root', 'inline', 'string') or a simple
    string which is assumed to be on top of the root state.

    Note: For that to work, `_other` must not be an `ExtendedRegexLexer`.
    """

class default:
    """
    Indicates a state or state action (e.g. #pop) to apply.
    For example default('#pop') is equivalent to ('', Token, '#pop')
    Note that state tuples may be used as well.

    .. versionadded:: 2.0
    """

    state: Incomplete
    def __init__(self, state) -> None: ...

class words(Future):
    """
    Indicates a list of literal words that is transformed into an optimized
    regex that matches any of the words.

    .. versionadded:: 2.0
    """

    words: Incomplete
    prefix: Incomplete
    suffix: Incomplete
    def __init__(self, words, prefix: str = "", suffix: str = "") -> None: ...
    def get(self): ...

class RegexLexerMeta(LexerMeta):
    """
    Metaclass for RegexLexer, creates the self._tokens attribute from
    self.tokens on the first instantiation.
    """

    def process_tokendef(cls, name, tokendefs=None):
        """Preprocess a dictionary of token definitions."""

    def get_tokendefs(cls):
        """
        Merge tokens from superclasses in MRO order, returning a single tokendef
        dictionary.

        Any state that is not defined by a subclass will be inherited
        automatically.  States that *are* defined by subclasses will, by
        default, override that state in the superclass.  If a subclass wishes to
        inherit definitions from a superclass, it can use the special value
        "inherit", which will cause the superclass' state definition to be
        included at that point in the state.
        """

    def __call__(cls, *args, **kwds):
        """Instantiate cls after preprocessing its token definitions."""

class RegexLexer(Lexer, metaclass=RegexLexerMeta):
    """
    Base for simple stateful regular expression-based lexers.
    Simplifies the lexing process so that you need only
    provide a list of states and regular expressions.
    """

    flags: ClassVar[RegexFlag]
    tokens: ClassVar[dict[str, list[Incomplete]]]
    def get_tokens_unprocessed(self, text: str, stack: Iterable[str] = ("root",)) -> Iterator[tuple[int, _TokenType, str]]:
        """
        Split ``text`` into (tokentype, text) pairs.

        ``stack`` is the initial stack (default: ``['root']``)
        """

class LexerContext:
    """
    A helper object that holds lexer position data.
    """

    text: Incomplete
    pos: Incomplete
    end: Incomplete
    stack: Incomplete
    def __init__(self, text, pos, stack=None, end=None) -> None: ...

class ExtendedRegexLexer(RegexLexer):
    """
    A RegexLexer that uses a context object to store its state.
    """

    def get_tokens_unprocessed(  # type: ignore[override]
        self, text: str | None = None, context: LexerContext | None = None
    ) -> Iterator[tuple[int, _TokenType, str]]:
        """
        Split ``text`` into (tokentype, text) pairs.
        If ``context`` is given, use this lexer context instead.
        """

class ProfilingRegexLexerMeta(RegexLexerMeta):
    """Metaclass for ProfilingRegexLexer, collects regex timing info."""

class ProfilingRegexLexer(RegexLexer, metaclass=ProfilingRegexLexerMeta):
    """Drop-in replacement for RegexLexer that does profiling of its regexes."""

    def get_tokens_unprocessed(self, text: str, stack: Iterable[str] = ("root",)) -> Iterator[tuple[int, _TokenType, str]]: ...
