"""
.h1 Welcome to YAML!
YAML is "Yet Another Markup Language" - a markup language
which is easier to type in than XML, yet gives us a
reasonable selection of formats.

The general rule is that if a line begins with a '.',
it requires special processing. Otherwise lines
are concatenated to paragraphs, and blank lines
separate paragraphs.

If the line ".foo bar bletch" is encountered,
it immediately ends and writes out any current
paragraph.

It then looks for a parser method called 'foo';
if found, it is called with arguments (bar, bletch).

If this is not found, it assumes that 'foo' is a
paragraph style, and the text for the first line
of the paragraph is 'bar bletch'.  It would be
up to the formatter to decide whether on not 'foo'
was a valid paragraph.

Special commands understood at present are:
dot image filename
- adds the image to the document
dot beginPre Code
- begins a Preformatted object in style 'Code'
dot endPre
- ends a preformatted object.
"""

from typing import Final

__version__: Final[str]
PLAIN: int
PREFORMATTED: int
BULLETCHAR: str

class BaseParser:
    """ "Simplest possible parser with only the most basic options.

    This defines the line-handling abilities and basic mechanism.
    The class YAMLParser includes capabilities for a fairly rich
    story.
    """

    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def parseFile(self, filename): ...
    def parseText(self, textBlock):
        """Parses the a possible multi-line text block"""

    def readLine(self, line) -> None: ...
    def endPara(self) -> None: ...
    def beginPre(self, stylename) -> None: ...
    def endPre(self) -> None: ...
    def image(self, filename) -> None: ...

class Parser(BaseParser):
    """This adds a basic set of "story" components compatible with HTML & PDF.

    Images, spaces
    """

    def vSpace(self, points) -> None:
        """Inserts a vertical spacer"""

    def pageBreak(self) -> None:
        """Inserts a frame break"""

    def custom(self, moduleName, funcName) -> None:
        """Goes and gets the Python object and adds it to the story"""

    def nextPageTemplate(self, templateName) -> None: ...

def parseFile(filename): ...
def parseText(textBlock): ...
