"""
pygments.formatters.html
~~~~~~~~~~~~~~~~~~~~~~~~

Formatter for HTML output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Any, TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

class HtmlFormatter(Formatter[_T]):
    """
    Format tokens as HTML 4 ``<span>`` tags. By default, the content is enclosed
    in a ``<pre>`` tag, itself wrapped in a ``<div>`` tag (but see the `nowrap` option).
    The ``<div>``'s CSS class can be set by the `cssclass` option.

    If the `linenos` option is set to ``"table"``, the ``<pre>`` is
    additionally wrapped inside a ``<table>`` which has one row and two
    cells: one containing the line numbers and one containing the code.
    Example:

    .. sourcecode:: html

        <div class="highlight" >
        <table><tr>
          <td class="linenos" title="click to toggle"
            onclick="with (this.firstChild.style)
                     { display = (display == '') ? 'none' : '' }">
            <pre>1
            2</pre>
          </td>
          <td class="code">
            <pre><span class="Ke">def </span><span class="NaFu">foo</span>(bar):
              <span class="Ke">pass</span>
            </pre>
          </td>
        </tr></table></div>

    (whitespace added to improve clarity).

    A list of lines can be specified using the `hl_lines` option to make these
    lines highlighted (as of Pygments 0.11).

    With the `full` option, a complete HTML 4 document is output, including
    the style definitions inside a ``<style>`` tag, or in a separate file if
    the `cssfile` option is given.

    When `tagsfile` is set to the path of a ctags index file, it is used to
    generate hyperlinks from names to their definition.  You must enable
    `lineanchors` and run ctags with the `-n` option for this to work.  The
    `python-ctags` module from PyPI must be installed to use this feature;
    otherwise a `RuntimeError` will be raised.

    The `get_style_defs(arg='')` method of a `HtmlFormatter` returns a string
    containing CSS rules for the CSS classes used by the formatter. The
    argument `arg` can be used to specify additional CSS selectors that
    are prepended to the classes. A call `fmter.get_style_defs('td .code')`
    would result in the following CSS classes:

    .. sourcecode:: css

        td .code .kw { font-weight: bold; color: #00FF00 }
        td .code .cm { color: #999999 }
        ...

    If you have Pygments 0.6 or higher, you can also pass a list or tuple to the
    `get_style_defs()` method to request multiple prefixes for the tokens:

    .. sourcecode:: python

        formatter.get_style_defs(['div.syntax pre', 'pre.syntax'])

    The output would then look like this:

    .. sourcecode:: css

        div.syntax pre .kw,
        pre.syntax .kw { font-weight: bold; color: #00FF00 }
        div.syntax pre .cm,
        pre.syntax .cm { color: #999999 }
        ...

    Additional options accepted:

    `nowrap`
        If set to ``True``, don't add a ``<pre>`` and a ``<div>`` tag
        around the tokens. This disables most other options (default: ``False``).

    `full`
        Tells the formatter to output a "full" document, i.e. a complete
        self-contained document (default: ``False``).

    `title`
        If `full` is true, the title that should be used to caption the
        document (default: ``''``).

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``). This option has no effect if the `cssfile`
        and `noclobber_cssfile` option are given and the file specified in
        `cssfile` exists.

    `noclasses`
        If set to true, token ``<span>`` tags (as well as line number elements)
        will not use CSS classes, but inline styles. This is not recommended
        for larger pieces of code since it increases output size by quite a bit
        (default: ``False``).

    `classprefix`
        Since the token types use relatively short class names, they may clash
        with some of your own class names. In this case you can use the
        `classprefix` option to give a string to prepend to all Pygments-generated
        CSS class names for token types.
        Note that this option also affects the output of `get_style_defs()`.

    `cssclass`
        CSS class for the wrapping ``<div>`` tag (default: ``'highlight'``).
        If you set this option, the default selector for `get_style_defs()`
        will be this class.

        .. versionadded:: 0.9
           If you select the ``'table'`` line numbers, the wrapping table will
           have a CSS class of this string plus ``'table'``, the default is
           accordingly ``'highlighttable'``.

    `cssstyles`
        Inline CSS styles for the wrapping ``<div>`` tag (default: ``''``).

    `prestyles`
        Inline CSS styles for the ``<pre>`` tag (default: ``''``).

        .. versionadded:: 0.11

    `cssfile`
        If the `full` option is true and this option is given, it must be the
        name of an external file. If the filename does not include an absolute
        path, the file's path will be assumed to be relative to the main output
        file's path, if the latter can be found. The stylesheet is then written
        to this file instead of the HTML file.

        .. versionadded:: 0.6

    `noclobber_cssfile`
        If `cssfile` is given and the specified file exists, the css file will
        not be overwritten. This allows the use of the `full` option in
        combination with a user specified css file. Default is ``False``.

        .. versionadded:: 1.1

    `linenos`
        If set to ``'table'``, output line numbers as a table with two cells,
        one containing the line numbers, the other the whole code.  This is
        copy-and-paste-friendly, but may cause alignment problems with some
        browsers or fonts.  If set to ``'inline'``, the line numbers will be
        integrated in the ``<pre>`` tag that contains the code (that setting
        is *new in Pygments 0.8*).

        For compatibility with Pygments 0.7 and earlier, every true value
        except ``'inline'`` means the same as ``'table'`` (in particular, that
        means also ``True``).

        The default value is ``False``, which means no line numbers at all.

        **Note:** with the default ("table") line number mechanism, the line
        numbers and code can have different line heights in Internet Explorer
        unless you give the enclosing ``<pre>`` tags an explicit ``line-height``
        CSS property (you get the default line spacing with ``line-height:
        125%``).

    `hl_lines`
        Specify a list of lines to be highlighted. The line numbers are always
        relative to the input (i.e. the first line is line 1) and are
        independent of `linenostart`.

        .. versionadded:: 0.11

    `linenostart`
        The line number for the first line (default: ``1``).

    `linenostep`
        If set to a number n > 1, only every nth line number is printed.

    `linenospecial`
        If set to a number n > 0, every nth line number is given the CSS
        class ``"special"`` (default: ``0``).

    `nobackground`
        If set to ``True``, the formatter won't output the background color
        for the wrapping element (this automatically defaults to ``False``
        when there is no wrapping element [eg: no argument for the
        `get_syntax_defs` method given]) (default: ``False``).

        .. versionadded:: 0.6

    `lineseparator`
        This string is output between lines of code. It defaults to ``"\\n"``,
        which is enough to break a line inside ``<pre>`` tags, but you can
        e.g. set it to ``"<br>"`` to get HTML line breaks.

        .. versionadded:: 0.7

    `lineanchors`
        If set to a nonempty string, e.g. ``foo``, the formatter will wrap each
        output line in an anchor tag with an ``id`` (and `name`) of ``foo-linenumber``.
        This allows easy linking to certain lines.

        .. versionadded:: 0.9

    `linespans`
        If set to a nonempty string, e.g. ``foo``, the formatter will wrap each
        output line in a span tag with an ``id`` of ``foo-linenumber``.
        This allows easy access to lines via javascript.

        .. versionadded:: 1.6

    `anchorlinenos`
        If set to `True`, will wrap line numbers in <a> tags. Used in
        combination with `linenos` and `lineanchors`.

    `tagsfile`
        If set to the path of a ctags file, wrap names in anchor tags that
        link to their definitions. `lineanchors` should be used, and the
        tags file should specify line numbers (see the `-n` option to ctags).
        The tags file is assumed to be encoded in UTF-8.

        .. versionadded:: 1.6

    `tagurlformat`
        A string formatting pattern used to generate links to ctags definitions.
        Available variables are `%(path)s`, `%(fname)s` and `%(fext)s`.
        Defaults to an empty string, resulting in just `#prefix-number` links.

        .. versionadded:: 1.6

    `filename`
        A string used to generate a filename when rendering ``<pre>`` blocks,
        for example if displaying source code. If `linenos` is set to
        ``'table'`` then the filename will be rendered in an initial row
        containing a single `<th>` which spans both columns.

        .. versionadded:: 2.1

    `wrapcode`
        Wrap the code inside ``<pre>`` blocks using ``<code>``, as recommended
        by the HTML5 specification.

        .. versionadded:: 2.4

    `debug_token_types`
        Add ``title`` attributes to all token ``<span>`` tags that show the
        name of the token.

        .. versionadded:: 2.10


    **Subclassing the HTML formatter**

    .. versionadded:: 0.7

    The HTML formatter is now built in a way that allows easy subclassing, thus
    customizing the output HTML code. The `format()` method calls
    `self._format_lines()` which returns a generator that yields tuples of ``(1,
    line)``, where the ``1`` indicates that the ``line`` is a line of the
    formatted source code.

    If the `nowrap` option is set, the generator is the iterated over and the
    resulting HTML is output.

    Otherwise, `format()` calls `self.wrap()`, which wraps the generator with
    other generators. These may add some HTML code to the one generated by
    `_format_lines()`, either by modifying the lines generated by the latter,
    then yielding them again with ``(1, line)``, and/or by yielding other HTML
    code before or after the lines, with ``(0, html)``. The distinction between
    source lines and other code makes it possible to wrap the generator multiple
    times.

    The default `wrap()` implementation adds a ``<div>`` and a ``<pre>`` tag.

    A custom `HtmlFormatter` subclass could look like this:

    .. sourcecode:: python

        class CodeHtmlFormatter(HtmlFormatter):

            def wrap(self, source, *, include_div):
                return self._wrap_code(source)

            def _wrap_code(self, source):
                yield 0, '<code>'
                for i, t in source:
                    if i == 1:
                        # it's a line of formatted code
                        t += '<br>'
                    yield i, t
                yield 0, '</code>'

    This results in wrapping the formatted lines with a ``<code>`` tag, where the
    source lines are broken using ``<br>`` tags.

    After calling `wrap()`, the `format()` method also adds the "line numbers"
    and/or "full document" wrappers if the respective options are set. Then, all
    HTML yielded by the wrapped generator is output.
    """

    name: str
    aliases: Any
    filenames: Any
    title: Any
    nowrap: Any
    noclasses: Any
    classprefix: Any
    cssclass: Any
    cssstyles: Any
    prestyles: Any
    cssfile: Any
    noclobber_cssfile: Any
    tagsfile: Any
    tagurlformat: Any
    filename: Any
    wrapcode: Any
    span_element_openers: Any
    linenos: int
    linenostart: Any
    linenostep: Any
    linenospecial: Any
    nobackground: Any
    lineseparator: Any
    lineanchors: Any
    linespans: Any
    anchorlinenos: Any
    hl_lines: Any
    def get_style_defs(self, arg=None):
        """
        Return CSS style definitions for the classes produced by the current
        highlighting style. ``arg`` can be a string or list of selectors to
        insert before the token type classes.
        """

    def get_token_style_defs(self, arg=None): ...
    def get_background_style_defs(self, arg=None): ...
    def get_linenos_style_defs(self): ...
    def get_css_prefix(self, arg): ...
    def wrap(self, source):
        """
        Wrap the ``source``, which is a generator yielding
        individual lines, in custom generators. See docstring
        for `format`. Can be overridden.
        """

    def format_unencoded(self, tokensource, outfile) -> None:
        """
        The formatting process uses several nested generators; which of
        them are used is determined by the user's options.

        Each generator should take at least one argument, ``inner``,
        and wrap the pieces of text generated by this.

        Always yield 2-tuples: (code, text). If "code" is 1, the text
        is part of the original tokensource being highlighted, if it's
        0, the text is some piece of wrapping. This makes it possible to
        use several different wrappers that process the original source
        linewise, e.g. line number generators.
        """
