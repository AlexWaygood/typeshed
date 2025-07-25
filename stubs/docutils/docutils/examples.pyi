"""
This module contains practical examples of Docutils client code.

Importing this module from client code is not recommended; its contents are
subject to change in future Docutils releases.  Instead, it is recommended
that you copy and paste the parts you need into your own code, modifying as
necessary.
"""

from _typeshed import Incomplete
from typing import Literal, overload
from typing_extensions import TypeAlias

from docutils.core import Publisher
from docutils.io import FileInput, StringInput
from docutils.nodes import document
from docutils.writers import _WriterParts

_HTMLHeaderLevel: TypeAlias = Literal[1, 2, 3, 4, 5, 6]

def html_parts(
    input_string: str,
    source_path=None,
    destination_path=None,
    input_encoding: str = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> _WriterParts:
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """

@overload
def html_body(
    input_string: str,
    source_path=None,
    destination_path=None,
    input_encoding: str = "unicode",
    output_encoding: Literal["unicode"] = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> str:
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """

@overload
def html_body(
    input_string: str,
    source_path=None,
    destination_path=None,
    input_encoding: str = "unicode",
    output_encoding: str = "unicode",
    doctitle: bool = True,
    initial_header_level: _HTMLHeaderLevel = 1,
) -> str | bytes: ...
def internals(
    input_string,
    source_path: FileInput | StringInput | None = None,
    destination_path: FileInput | StringInput | None = None,
    input_encoding: str = "unicode",
    settings_overrides: dict[str, Incomplete] | None = None,
) -> tuple[document | None, Publisher]:
    """
    Return the document tree and publisher, for exploring Docutils internals.

    Parameters: see `html_parts()`.
    """
