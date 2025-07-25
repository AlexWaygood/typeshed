"""
pygments.lexers
~~~~~~~~~~~~~~~

Pygments lexers.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import FileDescriptorOrPath, StrPath
from collections.abc import Iterator
from typing import Any

from pygments.lexer import Lexer, LexerMeta

def get_all_lexers(plugins: bool = True) -> Iterator[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]]:
    """Return a generator of tuples in the form ``(name, aliases,
    filenames, mimetypes)`` of all know lexers.

    If *plugins* is true (the default), plugin lexers supplied by entrypoints
    are also returned.  Otherwise, only builtin ones are considered.
    """

def find_lexer_class(name: str) -> LexerMeta | None:
    """
    Return the `Lexer` subclass that with the *name* attribute as given by
    the *name* argument.
    """

def find_lexer_class_by_name(_alias: str) -> LexerMeta:
    """
    Return the `Lexer` subclass that has `alias` in its aliases list, without
    instantiating it.

    Like `get_lexer_by_name`, but does not instantiate the class.

    Will raise :exc:`pygments.util.ClassNotFound` if no lexer with that alias is
    found.

    .. versionadded:: 2.2
    """

def get_lexer_by_name(_alias: str, **options: Any) -> Lexer:
    """
    Return an instance of a `Lexer` subclass that has `alias` in its
    aliases list. The lexer is given the `options` at its
    instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no lexer with that alias is
    found.
    """

def load_lexer_from_file(filename: FileDescriptorOrPath, lexername: str = "CustomLexer", **options: Any) -> Lexer:
    """Load a lexer from a file.

    This method expects a file located relative to the current working
    directory, which contains a Lexer class. By default, it expects the
    Lexer to be name CustomLexer; you can specify your own class name
    as the second argument to this function.

    Users should be very careful with the input, because this method
    is equivalent to running eval on the input file.

    Raises ClassNotFound if there are any problems importing the Lexer.

    .. versionadded:: 2.2
    """

def find_lexer_class_for_filename(_fn: StrPath, code: str | bytes | None = None) -> LexerMeta | None:
    """Get a lexer for a filename.

    If multiple lexers match the filename pattern, use ``analyse_text()`` to
    figure out which one is more appropriate.

    Returns None if not found.
    """

def get_lexer_for_filename(_fn: StrPath, code: str | bytes | None = None, **options: Any) -> Lexer:
    """Get a lexer for a filename.

    Return a `Lexer` subclass instance that has a filename pattern
    matching `fn`. The lexer is given the `options` at its
    instantiation.

    Raise :exc:`pygments.util.ClassNotFound` if no lexer for that filename
    is found.

    If multiple lexers match the filename pattern, use their ``analyse_text()``
    methods to figure out which one is more appropriate.
    """

def get_lexer_for_mimetype(_mime: str, **options: Any) -> Lexer:
    """
    Return a `Lexer` subclass instance that has `mime` in its mimetype
    list. The lexer is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if not lexer for that mimetype
    is found.
    """

def guess_lexer_for_filename(_fn: StrPath, _text: str, **options: Any) -> Lexer:
    """
    As :func:`guess_lexer()`, but only lexers which have a pattern in `filenames`
    or `alias_filenames` that matches `filename` are taken into consideration.

    :exc:`pygments.util.ClassNotFound` is raised if no lexer thinks it can
    handle the content.
    """

def guess_lexer(_text: str | bytes, **options: Any) -> Lexer:
    """
    Return a `Lexer` subclass instance that's guessed from the text in
    `text`. For that, the :meth:`.analyse_text()` method of every known lexer
    class is called with the text as argument, and the lexer which returned the
    highest value will be instantiated and returned.

    :exc:`pygments.util.ClassNotFound` is raised if no lexer thinks it can
    handle the content.
    """

# Having every lexer class here doesn't seem to be worth it
def __getattr__(name: str): ...  # incomplete module
