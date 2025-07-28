"""
pygments.lexers.lisp
~~~~~~~~~~~~~~~~~~~~

Lexers for Lispy languages.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from collections.abc import Iterator
from typing import ClassVar

from ..lexer import RegexLexer
from ..token import _TokenType

__all__ = [
    "SchemeLexer",
    "CommonLispLexer",
    "HyLexer",
    "RacketLexer",
    "NewLispLexer",
    "EmacsLispLexer",
    "ShenLexer",
    "CPSALexer",
    "XtlangLexer",
    "FennelLexer",
]

class SchemeLexer(RegexLexer):
    """
    A Scheme lexer.

    This parser is checked with pastes from the LISP pastebin
    at http://paste.lisp.org/ to cover as much syntax as possible.

    It supports the full Scheme syntax as defined in R5RS.
    """

    valid_name: ClassVar[str]
    token_end: ClassVar[str]
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...  # type: ignore[override]
    number_rules: ClassVar[dict[Incomplete, Incomplete]]
    def decimal_cb(self, match) -> Iterator[tuple[Incomplete, Incomplete, Incomplete]]: ...

class CommonLispLexer(RegexLexer):
    """
    A Common Lisp lexer.
    """

    nonmacro: ClassVar[str]
    constituent: ClassVar[str]
    terminated: ClassVar[str]
    symbol: ClassVar[str]
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...  # type: ignore[override]

class HyLexer(RegexLexer):
    """
    Lexer for Hy source code.
    """

    special_forms: ClassVar[tuple[str, ...]]
    declarations: ClassVar[tuple[str, ...]]
    hy_builtins: ClassVar[tuple[str, ...]]
    hy_core: ClassVar[tuple[str, ...]]
    builtins: ClassVar[tuple[str, ...]]
    valid_name: ClassVar[str]

class RacketLexer(RegexLexer):
    """
    Lexer for Racket source code (formerly
    known as PLT Scheme).
    """

class NewLispLexer(RegexLexer):
    """
    For newLISP source code (version 10.3.0).
    """

    builtins: ClassVar[tuple[str, ...]]
    valid_name: ClassVar[str]

class EmacsLispLexer(RegexLexer):
    """
    An ELisp lexer, parsing a stream and outputting the tokens
    needed to highlight elisp code.
    """

    nonmacro: ClassVar[str]
    constituent: ClassVar[str]
    terminated: ClassVar[str]
    symbol: ClassVar[str]
    macros: ClassVar[set[str]]
    special_forms: ClassVar[set[str]]
    builtin_function: ClassVar[set[str]]
    builtin_function_highlighted: ClassVar[set[str]]
    lambda_list_keywords: ClassVar[set[str]]
    error_keywords: ClassVar[set[str]]
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...  # type: ignore[override]

class ShenLexer(RegexLexer):
    """
    Lexer for Shen source code.
    """

    DECLARATIONS: ClassVar[tuple[str, ...]]
    SPECIAL_FORMS: ClassVar[tuple[str, ...]]
    BUILTINS: ClassVar[tuple[str, ...]]
    BUILTINS_ANYWHERE: ClassVar[tuple[str, ...]]
    MAPPINGS: ClassVar[dict[str, Incomplete]]

    valid_symbol_chars: ClassVar[str]
    valid_name: ClassVar[str]
    symbol_name: ClassVar[str]
    variable: ClassVar[str]

    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...  # type: ignore[override]

class CPSALexer(RegexLexer):
    """
    A CPSA lexer based on the CPSA language as of version 2.2.12
    """

    valid_name: ClassVar[str]

class XtlangLexer(RegexLexer):
    """An xtlang lexer for the Extempore programming environment.

    This is a mixture of Scheme and xtlang, really. Keyword lists are
    taken from the Extempore Emacs mode
    (https://github.com/extemporelang/extempore-emacs-mode)
    """

    common_keywords: ClassVar[tuple[str, ...]]
    scheme_keywords: ClassVar[tuple[str, ...]]
    xtlang_bind_keywords: ClassVar[tuple[str, ...]]
    xtlang_keywords: ClassVar[tuple[str, ...]]
    common_functions: ClassVar[tuple[str, ...]]
    scheme_functions: ClassVar[tuple[str, ...]]
    xtlang_functions: ClassVar[tuple[str, ...]]

    valid_scheme_name: ClassVar[str]
    valid_xtlang_name: ClassVar[str]
    valid_xtlang_type: ClassVar[str]

class FennelLexer(RegexLexer):
    """A lexer for the Fennel programming language.

    Fennel compiles to Lua, so all the Lua builtins are recognized as well
    as the special forms that are particular to the Fennel compiler.
    """

    special_forms: ClassVar[tuple[str, ...]]
    declarations: ClassVar[tuple[str, ...]]
    builtins: ClassVar[tuple[str, ...]]
    valid_name: ClassVar[str]
