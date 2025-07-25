"""
Adds code/syntax highlighting to standard Python-Markdown code blocks.

See the [documentation](https://Python-Markdown.github.io/extensions/code_hilite)
for details.
"""

from typing import Any

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

pygments: bool

def parse_hl_lines(expr: str) -> list[int]:
    """Support our syntax for emphasizing certain lines of code.

    `expr` should be like '1 2' to emphasize lines 1 and 2 of a code block.
    Returns a list of integers, the line numbers to emphasize.
    """

class CodeHilite:
    """
    Determine language of source code, and pass it on to the Pygments highlighter.

    Usage:

    ```python
    code = CodeHilite(src=some_code, lang='python')
    html = code.hilite()
    ```

    Arguments:
        src: Source string or any object with a `.readline` attribute.

    Keyword arguments:
        lang (str): String name of Pygments lexer to use for highlighting. Default: `None`.
        guess_lang (bool): Auto-detect which lexer to use.
            Ignored if `lang` is set to a valid value. Default: `True`.
        use_pygments (bool): Pass code to Pygments for code highlighting. If `False`, the code is
            instead wrapped for highlighting by a JavaScript library. Default: `True`.
        pygments_formatter (str): The name of a Pygments formatter or a formatter class used for
            highlighting the code blocks. Default: `html`.
        linenums (bool): An alias to Pygments `linenos` formatter option. Default: `None`.
        css_class (str): An alias to Pygments `cssclass` formatter option. Default: 'codehilite'.
        lang_prefix (str): Prefix prepended to the language. Default: "language-".

    Other Options:

    Any other options are accepted and passed on to the lexer and formatter. Therefore,
    valid options include any options which are accepted by the `html` formatter or
    whichever lexer the code's language uses. Note that most lexers do not have any
    options. However, a few have very useful options, such as PHP's `startinline` option.
    Any invalid options are ignored without error.

    * **Formatter options**: <https://pygments.org/docs/formatters/#HtmlFormatter>
    * **Lexer Options**: <https://pygments.org/docs/lexers/>

    Additionally, when Pygments is enabled, the code's language is passed to the
    formatter as an extra option `lang_str`, whose value being `{lang_prefix}{lang}`.
    This option has no effect to the Pygments' builtin formatters.

    Advanced Usage:

    ```python
    code = CodeHilite(
        src = some_code,
        lang = 'php',
        startinline = True,      # Lexer option. Snippet does not start with `<?php`.
        linenostart = 42,        # Formatter option. Snippet starts on line 42.
        hl_lines = [45, 49, 50], # Formatter option. Highlight lines 45, 49, and 50.
        linenos = 'inline'       # Formatter option. Avoid alignment problems.
    )
    html = code.hilite()
    ```

    """

    src: str
    lang: str | None
    guess_lang: bool
    use_pygments: bool
    lang_prefix: str
    pygments_formatter: Any
    options: dict[str, Any]
    def __init__(
        self,
        src: str,
        *,
        linenums: bool | None = None,
        guess_lang: bool = ...,
        css_class: str = ...,
        lang: str | None = ...,
        style: str = ...,
        noclasses: bool = ...,
        tab_length: int = ...,
        hl_lines: list[int] = ...,
        use_pygments: bool = ...,
        **options: Any,
    ) -> None: ...
    def hilite(self, shebang: bool = True) -> str:
        """
        Pass code to the [Pygments](https://pygments.org/) highlighter with
        optional line numbers. The output should then be styled with CSS to
        your liking. No styles are applied by default - only styling hooks
        (i.e.: `<span class="k">`).

        returns : A string of html.

        """

class HiliteTreeprocessor(Treeprocessor):
    """Highlight source code in code blocks."""

    config: dict[str, Any]
    def code_unescape(self, text: str) -> str:
        """Unescape code."""

class CodeHiliteExtension(Extension):
    """Add source code highlighting to markdown code blocks."""

    def __init__(self, **kwargs) -> None: ...

def makeExtension(**kwargs) -> CodeHiliteExtension: ...
