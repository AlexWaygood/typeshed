"""
pygments.util
~~~~~~~~~~~~~

Utility functions.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from io import TextIOWrapper
from typing import Any

split_path_re: Any
doctype_lookup_re: Any
tag_re: Any
xml_decl_re: Any

class ClassNotFound(ValueError):
    """Raised if one of the lookup functions didn't find a matching class."""

class OptionError(Exception):
    """
    This exception will be raised by all option processing functions if
    the type or value of the argument is not correct.
    """

def get_choice_opt(options, optname, allowed, default=None, normcase: bool = False):
    """
    If the key `optname` from the dictionary is not in the sequence
    `allowed`, raise an error, otherwise return it.
    """

def get_bool_opt(options, optname, default=None):
    """
    Intuitively, this is `options.get(optname, default)`, but restricted to
    Boolean value. The Booleans can be represented as string, in order to accept
    Boolean value from the command line arguments. If the key `optname` is
    present in the dictionary `options` and is not associated with a Boolean,
    raise an `OptionError`. If it is absent, `default` is returned instead.

    The valid string values for ``True`` are ``1``, ``yes``, ``true`` and
    ``on``, the ones for ``False`` are ``0``, ``no``, ``false`` and ``off``
    (matched case-insensitively).
    """

def get_int_opt(options, optname, default=None):
    """As :func:`get_bool_opt`, but interpret the value as an integer."""

def get_list_opt(options, optname, default=None):
    """
    If the key `optname` from the dictionary `options` is a string,
    split it at whitespace and return it. If it is already a list
    or a tuple, it is returned as a list.
    """

def docstring_headline(obj): ...
def make_analysator(f):
    """Return a static text analyser function that returns float values."""

def shebang_matches(text, regex):
    """Check if the given regular expression matches the last part of the
    shebang if one exists.

        >>> from pygments.util import shebang_matches
        >>> shebang_matches('#!/usr/bin/env python', r'python(2\\.\\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python2.4', r'python(2\\.\\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python-ruby', r'python(2\\.\\d)?')
        False
        >>> shebang_matches('#!/usr/bin/python/ruby', r'python(2\\.\\d)?')
        False
        >>> shebang_matches('#!/usr/bin/startsomethingwith python',
        ...                 r'python(2\\.\\d)?')
        True

    It also checks for common windows executable file extensions::

        >>> shebang_matches('#!C:\\\\Python2.4\\\\Python.exe', r'python(2\\.\\d)?')
        True

    Parameters (``'-f'`` or ``'--foo'`` are ignored so ``'perl'`` does
    the same as ``'perl -e'``)

    Note that this method automatically searches the whole string (eg:
    the regular expression is wrapped in ``'^$'``)
    """

def doctype_matches(text, regex):
    """Check if the doctype matches a regular expression (if present).

    Note that this method only checks the first part of a DOCTYPE.
    eg: 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
    """

def html_doctype_matches(text):
    """Check if the file looks like it has a html doctype."""

def looks_like_xml(text):
    """Check if a doctype exists or if we have some tags."""

def surrogatepair(c):
    """Given a unicode character code with length greater than 16 bits,
    return the two 16 bit surrogate pair.
    """

def format_lines(var_name, seq, raw: bool = False, indent_level: int = 0):
    """Formats a sequence of strings for output."""

def duplicates_removed(it, already_seen=()):
    """
    Returns a list with duplicates removed from the iterable `it`.

    Order is preserved.
    """

class Future:
    """Generic class to defer some work.

    Handled specially in RegexLexerMeta, to support regex string construction at
    first use.
    """

    def get(self) -> None: ...

def guess_decode(text):
    """Decode *text* with guessed encoding.

    First try UTF-8; this should fail for non-UTF-8 encodings.
    Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """

def guess_decode_from_terminal(text, term):
    """Decode *text* coming from terminal *term*.

    First try the terminal encoding, if given.
    Then try UTF-8.  Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """

def terminal_encoding(term):
    """Return our best guess of encoding for the given *term*."""

class UnclosingTextIOWrapper(TextIOWrapper):
    def close(self) -> None: ...
