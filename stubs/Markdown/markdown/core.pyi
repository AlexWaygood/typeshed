from codecs import _ReadableStream, _WritableStream
from collections.abc import Callable, Mapping, Sequence
from logging import Logger
from typing import Any, ClassVar, Literal
from typing_extensions import Self
from xml.etree.ElementTree import Element

from . import blockparser, inlinepatterns, postprocessors, preprocessors, treeprocessors
from .extensions import Extension
from .util import HtmlStash, Registry

__all__ = ["Markdown", "markdown", "markdownFromFile"]

logger: Logger

class Markdown:
    """
    A parser which converts Markdown to HTML.

    Attributes:
        Markdown.tab_length (int): The number of spaces which correspond to a single tab. Default: `4`.
        Markdown.ESCAPED_CHARS (list[str]): List of characters which get the backslash escape treatment.
        Markdown.block_level_elements (list[str]): List of HTML tags which get treated as block-level elements.
            See [`markdown.util.BLOCK_LEVEL_ELEMENTS`][] for the full list of elements.
        Markdown.registeredExtensions (list[Extension]): List of extensions which have called
            [`registerExtension`][markdown.Markdown.registerExtension] during setup.
        Markdown.doc_tag (str): Element used to wrap document. Default: `div`.
        Markdown.stripTopLevelTags (bool): Indicates whether the `doc_tag` should be removed. Default: 'True'.
        Markdown.references (dict[str, tuple[str, str]]): A mapping of link references found in a parsed document
             where the key is the reference name and the value is a tuple of the URL and title.
        Markdown.htmlStash (util.HtmlStash): The instance of the `HtmlStash` used by an instance of this class.
        Markdown.output_formats (dict[str, Callable[xml.etree.ElementTree.Element]]): A mapping of known output
             formats by name and their respective serializers. Each serializer must be a callable which accepts an
            [`Element`][xml.etree.ElementTree.Element] and returns a `str`.
        Markdown.output_format (str): The output format set by
            [`set_output_format`][markdown.Markdown.set_output_format].
        Markdown.serializer (Callable[xml.etree.ElementTree.Element]): The serializer set by
            [`set_output_format`][markdown.Markdown.set_output_format].
        Markdown.preprocessors (util.Registry): A collection of [`preprocessors`][markdown.preprocessors].
        Markdown.parser (blockparser.BlockParser): A collection of [`blockprocessors`][markdown.blockprocessors].
        Markdown.inlinePatterns (util.Registry): A collection of [`inlinepatterns`][markdown.inlinepatterns].
        Markdown.treeprocessors (util.Registry): A collection of [`treeprocessors`][markdown.treeprocessors].
        Markdown.postprocessors (util.Registry): A collection of [`postprocessors`][markdown.postprocessors].

    """

    preprocessors: Registry[preprocessors.Preprocessor]
    inlinePatterns: Registry[inlinepatterns.Pattern]
    treeprocessors: Registry[treeprocessors.Treeprocessor]
    postprocessors: Registry[postprocessors.Postprocessor]
    parser: blockparser.BlockParser
    htmlStash: HtmlStash
    output_formats: ClassVar[dict[Literal["xhtml", "html"], Callable[[Element], str]]]
    output_format: Literal["xhtml", "html"]
    serializer: Callable[[Element], str]
    tab_length: int
    block_level_elements: list[str]
    registeredExtensions: list[Extension]
    ESCAPED_CHARS: list[str]
    doc_tag: ClassVar[str]
    stripTopLevelTags: bool
    def __init__(
        self,
        *,
        extensions: Sequence[str | Extension] | None = ...,
        extension_configs: Mapping[str, Mapping[str, Any]] | None = ...,
        output_format: Literal["xhtml", "html"] | None = ...,
        tab_length: int | None = ...,
    ) -> None:
        """
        Creates a new Markdown instance.

        Keyword Arguments:
            extensions (list[Extension | str]): A list of extensions.

                If an item is an instance of a subclass of [`markdown.extensions.Extension`][],
                the instance will be used as-is. If an item is of type `str`, it is passed
                to [`build_extension`][markdown.Markdown.build_extension] with its corresponding
                `extension_configs` and the returned instance  of [`markdown.extensions.Extension`][]
                is used.
            extension_configs (dict[str, dict[str, Any]]): Configuration settings for extensions.
            output_format (str): Format of output. Supported formats are:

                * `xhtml`: Outputs XHTML style tags. Default.
                * `html`: Outputs HTML style tags.
            tab_length (int): Length of tabs in the source. Default: `4`

        """

    def build_parser(self) -> Self:
        """
        Build the parser from the various parts.

        Assigns a value to each of the following attributes on the class instance:

        * **`Markdown.preprocessors`** ([`Registry`][markdown.util.Registry]) -- A collection of
          [`preprocessors`][markdown.preprocessors].
        * **`Markdown.parser`** ([`BlockParser`][markdown.blockparser.BlockParser]) -- A collection of
          [`blockprocessors`][markdown.blockprocessors].
        * **`Markdown.inlinePatterns`** ([`Registry`][markdown.util.Registry]) -- A collection of
          [`inlinepatterns`][markdown.inlinepatterns].
        * **`Markdown.treeprocessors`** ([`Registry`][markdown.util.Registry]) -- A collection of
          [`treeprocessors`][markdown.treeprocessors].
        * **`Markdown.postprocessors`** ([`Registry`][markdown.util.Registry]) -- A collection of
          [`postprocessors`][markdown.postprocessors].

        This method could be redefined in a subclass to build a custom parser which is made up of a different
        combination of processors and patterns.

        """

    def registerExtensions(self, extensions: Sequence[Extension | str], configs: Mapping[str, dict[str, Any]]) -> Self:
        """
        Load a list of extensions into an instance of the `Markdown` class.

        Arguments:
            extensions (list[Extension | str]): A list of extensions.

                If an item is an instance of a subclass of [`markdown.extensions.Extension`][],
                the instance will be used as-is. If an item is of type `str`, it is passed
                to [`build_extension`][markdown.Markdown.build_extension] with its corresponding `configs` and the
                returned instance  of [`markdown.extensions.Extension`][] is used.
            configs (dict[str, dict[str, Any]]): Configuration settings for extensions.

        """

    def build_extension(self, ext_name: str, configs: Mapping[str, Any]) -> Extension:
        """
        Build extension from a string name, then return an instance using the given `configs`.

        Arguments:
            ext_name: Name of extension as a string.
            configs: Configuration settings for extension.

        Returns:
            An instance of the extension with the given configuration settings.

        First attempt to load an entry point. The string name must be registered as an entry point in the
        `markdown.extensions` group which points to a subclass of the [`markdown.extensions.Extension`][] class.
        If multiple distributions have registered the same name, the first one found is returned.

        If no entry point is found, assume dot notation (`path.to.module:ClassName`). Load the specified class and
        return an instance. If no class is specified, import the module and call a `makeExtension` function and return
        the [`markdown.extensions.Extension`][] instance returned by that function.
        """

    def registerExtension(self, extension: Extension) -> Self:
        """
        Register an extension as having a resettable state.

        Arguments:
            extension: An instance of the extension to register.

        This should get called once by an extension during setup. A "registered" extension's
        `reset` method is called by [`Markdown.reset()`][markdown.Markdown.reset]. Not all extensions have or need a
        resettable state, and so it should not be assumed that all extensions are "registered."

        """

    def reset(self) -> Self:
        """
        Resets all state variables to prepare the parser instance for new input.

        Called once upon creation of a class instance. Should be called manually between calls
        to [`Markdown.convert`][markdown.Markdown.convert].
        """

    def set_output_format(self, format: Literal["xhtml", "html"]) -> Self:
        """
        Set the output format for the class instance.

        Arguments:
            format: Must be a known value in `Markdown.output_formats`.

        """

    def is_block_level(self, tag: object) -> bool:
        """
        Check if the given `tag` is a block level HTML tag.

        Returns `True` for any string listed in `Markdown.block_level_elements`. A `tag` which is
        not a string always returns `False`.

        """

    def convert(self, source: str) -> str:
        """
        Convert a Markdown string to a string in the specified output format.

        Arguments:
            source: Markdown formatted text as Unicode or ASCII string.

        Returns:
            A string in the specified output format.

        Markdown parsing takes place in five steps:

        1. A bunch of [`preprocessors`][markdown.preprocessors] munge the input text.
        2. A [`BlockParser`][markdown.blockparser.BlockParser] parses the high-level structural elements of the
           pre-processed text into an [`ElementTree`][xml.etree.ElementTree.ElementTree] object.
        3. A bunch of [`treeprocessors`][markdown.treeprocessors] are run against the
           [`ElementTree`][xml.etree.ElementTree.ElementTree] object. One such `treeprocessor`
           ([`markdown.treeprocessors.InlineProcessor`][]) runs [`inlinepatterns`][markdown.inlinepatterns]
           against the [`ElementTree`][xml.etree.ElementTree.ElementTree] object, parsing inline markup.
        4. Some [`postprocessors`][markdown.postprocessors] are run against the text after the
           [`ElementTree`][xml.etree.ElementTree.ElementTree] object has been serialized into text.
        5. The output is returned as a string.

        """

    def convertFile(
        self, input: str | _ReadableStream | None = None, output: str | _WritableStream | None = None, encoding: str | None = None
    ) -> Self:
        """
        Converts a Markdown file and returns the HTML as a Unicode string.

        Decodes the file using the provided encoding (defaults to `utf-8`),
        passes the file content to markdown, and outputs the HTML to either
        the provided stream or the file with provided name, using the same
        encoding as the source file. The
        [`xmlcharrefreplace`](https://docs.python.org/3/library/codecs.html#error-handlers)
        error handler is used when encoding the output.

        **Note:** This is the only place that decoding and encoding of Unicode
        takes place in Python-Markdown.  (All other code is Unicode-in /
        Unicode-out.)

        Arguments:
            input: File object or path. Reads from `stdin` if `None`.
            output: File object or path. Writes to `stdout` if `None`.
            encoding: Encoding of input and output files. Defaults to `utf-8`.

        """

def markdown(
    text: str,
    *,
    extensions: Sequence[str | Extension] | None = ...,
    extension_configs: Mapping[str, Mapping[str, Any]] | None = ...,
    output_format: Literal["xhtml", "html"] | None = ...,
    tab_length: int | None = ...,
) -> str:
    """
    Convert a markdown string to HTML and return HTML as a Unicode string.

    This is a shortcut function for [`Markdown`][markdown.Markdown] class to cover the most
    basic use case.  It initializes an instance of [`Markdown`][markdown.Markdown], loads the
    necessary extensions and runs the parser on the given text.

    Arguments:
        text: Markdown formatted text as Unicode or ASCII string.

    Keyword arguments:
        **kwargs: Any arguments accepted by the Markdown class.

    Returns:
        A string in the specified output format.

    """

def markdownFromFile(
    *,
    input: str | _ReadableStream | None = ...,
    output: str | _WritableStream | None = ...,
    encoding: str | None = ...,
    extensions: Sequence[str | Extension] | None = ...,
    extension_configs: Mapping[str, Mapping[str, Any]] | None = ...,
    output_format: Literal["xhtml", "html"] | None = ...,
    tab_length: int | None = ...,
) -> None:
    """
    Read Markdown text from a file and write output to a file or a stream.

    This is a shortcut function which initializes an instance of [`Markdown`][markdown.Markdown],
    and calls the [`convertFile`][markdown.Markdown.convertFile] method rather than
    [`convert`][markdown.Markdown.convert].

    Keyword arguments:
        input (str | BinaryIO): A file name or readable object.
        output (str | BinaryIO): A file name or writable object.
        encoding (str): Encoding of input and output.
        **kwargs: Any arguments accepted by the `Markdown` class.

    """
