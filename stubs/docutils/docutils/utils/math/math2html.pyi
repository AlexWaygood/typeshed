from _typeshed import Incomplete
from collections.abc import Generator
from typing import ClassVar, Final, TextIO, TypeVar

_T = TypeVar("_T")

__version__: Final[str]

class Trace:
    """A tracing class"""

    debugmode: ClassVar[bool]
    quietmode: ClassVar[bool]
    showlinesmode: ClassVar[bool]
    prefix: ClassVar[str | None]
    @classmethod
    def debug(cls, message: str) -> None:
        """Show a debug message"""

    @classmethod
    def message(cls, message: str) -> None:
        """Show a trace message"""

    @classmethod
    def error(cls, message: str) -> None:
        """Show an error message"""

    @classmethod
    def show(cls, message: str, channel: TextIO) -> None:
        """Show a message out of a channel"""

class ContainerConfig:
    """Configuration class from elyxer.config file"""

    extracttext: ClassVar[dict[str, list[str]]]

class EscapeConfig:
    """Configuration class from elyxer.config file"""

    chars: ClassVar[dict[str, str]]
    entities: ClassVar[dict[str, str]]

class FormulaConfig:
    """Configuration class from elyxer.config file"""

    alphacommands: ClassVar[dict[str, str]]
    array: ClassVar[dict[str, str]]
    bigbrackets: ClassVar[dict[str, list[str]]]
    bracketcommands: ClassVar[dict[str, str]]
    combiningfunctions: ClassVar[dict[str, str]]
    commands: ClassVar[dict[str, str]]
    cmddict: ClassVar[dict[str, str]]
    oversetfunctions: ClassVar[dict[str, str]]
    undersetfunctions: ClassVar[dict[str, str]]
    endings: ClassVar[dict[str, str]]
    environments: ClassVar[dict[str, list[str]]]
    fontfunctions: ClassVar[dict[str, str]]
    hybridfunctions: ClassVar[dict[str, list[str]]]
    hybridsizes: ClassVar[dict[str, str]]
    labelfunctions: ClassVar[dict[str, str]]
    limitcommands: ClassVar[dict[str, str]]
    modified: ClassVar[dict[str, str]]
    onefunctions: ClassVar[dict[str, str]]
    spacedcommands: ClassVar[dict[str, str]]
    starts: ClassVar[dict[str, str]]
    symbolfunctions: ClassVar[dict[str, str]]
    textfunctions: ClassVar[dict[str, str]]
    unmodified: ClassVar[dict[str, list[str]]]
    key: str
    value: str

class CommandLineParser:
    """A parser for runtime options"""

    options: Incomplete
    def __init__(self, options) -> None: ...
    def parseoptions(self, args):
        """Parse command line options"""

    def readoption(self, args):
        """Read the key and value for an option"""

    def readquoted(self, args, initial):
        """Read a value between quotes"""

    def readequalskey(self, arg, args):
        """Read a key using equals"""

class Options:
    """A set of runtime options"""

    location: Incomplete
    debug: bool
    quiet: bool
    version: bool
    help: bool
    simplemath: bool
    showlines: bool
    branches: Incomplete
    def parseoptions(self, args) -> None:
        """Parse command line options"""

    def processoptions(self) -> None:
        """Process all options parsed."""

    def usage(self) -> None:
        """Show correct usage"""

    def showoptions(self) -> None:
        """Show all possible options"""

    def showversion(self) -> None:
        """Return the current eLyXer version string"""

class Cloner:
    """An object used to clone other objects."""

    @classmethod
    def clone(cls, original: _T) -> _T:
        """Return an exact copy of an object."""

    @classmethod
    def create(cls, type: type[_T]) -> _T:
        """Create an object of a given class."""

class ContainerExtractor:
    """A class to extract certain containers.

    The config parameter is a map containing three lists:
    allowed, copied and extracted.
    Each of the three is a list of class names for containers.
    Allowed containers are included as is into the result.
    Cloned containers are cloned and placed into the result.
    Extracted containers are looked into.
    All other containers are silently ignored.
    """

    allowed: Incomplete
    extracted: Incomplete
    def __init__(self, config) -> None: ...
    def extract(self, container):
        """Extract a group of selected containers from a container."""

    def process(self, container, list) -> None:
        """Add allowed containers."""

    def safeclone(self, container):
        """Return a new container with contents only in a safe list, recursively."""

class Parser:
    """A generic parser"""

    begin: int
    parameters: Incomplete
    def __init__(self) -> None: ...
    def parseheader(self, reader):
        """Parse the header"""

    def parseparameter(self, reader) -> None:
        """Parse a parameter"""

    def parseending(self, reader, process) -> None:
        """Parse until the current ending is found"""

    def parsecontainer(self, reader, contents) -> None: ...

class LoneCommand(Parser):
    """A parser for just one command line"""

    def parse(self, reader):
        """Read nothing"""

class TextParser(Parser):
    """A parser for a command and a bit of text"""

    stack: Incomplete
    ending: Incomplete
    endings: Incomplete
    def __init__(self, container) -> None: ...
    def parse(self, reader):
        """Parse lines as long as they are text"""

    def isending(self, reader):
        """Check if text is ending"""

class ExcludingParser(Parser):
    """A parser that excludes the final line"""

    def parse(self, reader):
        """Parse everything up to (and excluding) the final line"""

class BoundedParser(ExcludingParser):
    """A parser bound by a final line"""

    def parse(self, reader):
        """Parse everything, including the final line"""

class BoundedDummy(Parser):
    """A bound parser that ignores everything"""

    def parse(self, reader):
        """Parse the contents of the container"""

class StringParser(Parser):
    """Parses just a string"""

    begin: Incomplete
    def parseheader(self, reader):
        """Do nothing, just take note"""

    def parse(self, reader):
        """Parse a single line"""

class ContainerOutput:
    """The generic HTML output for a container."""

    def gethtml(self, container) -> None:
        """Show an error."""

    def isempty(self):
        """Decide if the output is empty: by default, not empty."""

class EmptyOutput(ContainerOutput):
    def gethtml(self, container):
        """Return empty HTML code."""

    def isempty(self):
        """This output is particularly empty."""

class FixedOutput(ContainerOutput):
    """Fixed output"""

    def gethtml(self, container):
        """Return constant HTML code"""

class ContentsOutput(ContainerOutput):
    """Outputs the contents converted to HTML"""

    def gethtml(self, container):
        """Return the HTML code"""

class TaggedOutput(ContentsOutput):
    """Outputs an HTML tag surrounding the contents."""

    tag: Incomplete
    breaklines: bool
    empty: bool
    def settag(self, tag, breaklines: bool = False, empty: bool = False):
        """Set the value for the tag and other attributes."""

    def setbreaklines(self, breaklines):
        """Set the value for breaklines."""

    def gethtml(self, container):
        """Return the HTML code."""

    def open(self, container):
        """Get opening line."""

    def close(self, container):
        """Get closing line."""

    def selfclosing(self, container):
        """Get self-closing line."""

    def checktag(self, container):
        """Check that the tag is valid."""

class FilteredOutput(ContentsOutput):
    """Returns the output in the contents, but filtered:"""

    filters: Incomplete
    def __init__(self) -> None:
        """Initialize the filters."""

    def addfilter(self, original, replacement) -> None:
        """Add a new filter: replace the original by the replacement."""

    def gethtml(self, container):
        """Return the HTML code"""

    def filter(self, line):
        """Filter a single line with all available filters."""

class StringOutput(ContainerOutput):
    """Returns a bare string as output"""

    def gethtml(self, container):
        """Return a bare string"""

class Globable:
    """A bit of text which can be globbed (lumped together in bits).
    Methods current(), skipcurrent(), checkfor() and isout() have to be
    implemented by subclasses.
    """

    leavepending: bool
    endinglist: Incomplete
    def __init__(self) -> None: ...
    def checkbytemark(self) -> None:
        """Check for a Unicode byte mark and skip it."""

    def isout(self):
        """Find out if we are out of the position yet."""

    def current(self):
        """Return the current character."""

    def checkfor(self, string):
        """Check for the given string in the current position."""

    def finished(self):
        """Find out if the current text has finished."""

    def skipcurrent(self):
        """Return the current character and skip it."""

    def glob(self, currentcheck):
        """Glob a bit of text that satisfies a check on the current char."""

    def globalpha(self):
        """Glob a bit of alpha text"""

    def globnumber(self):
        """Glob a row of digits."""

    def isidentifier(self):
        """Return if the current character is alphanumeric or _."""

    def globidentifier(self):
        """Glob alphanumeric and _ symbols."""

    def isvalue(self):
        """Return if the current character is a value character:"""

    def globvalue(self):
        """Glob a value: any symbols but brackets."""

    def skipspace(self):
        """Skip all whitespace at current position."""

    def globincluding(self, magicchar):
        """Glob a bit of text up to (including) the magic char."""

    def globexcluding(self, excluded):
        """Glob a bit of text up until (excluding) any excluded character."""

    def pushending(self, ending, optional: bool = False) -> None:
        """Push a new ending to the bottom"""

    def popending(self, expected=None):
        """Pop the ending found at the current position"""

    def nextending(self):
        """Return the next ending in the queue."""

class EndingList:
    """A list of position endings"""

    endings: Incomplete
    def __init__(self) -> None: ...
    def add(self, ending, optional: bool = False) -> None:
        """Add a new ending to the list"""

    def pickpending(self, pos) -> None:
        """Pick any pending endings from a parse position."""

    def checkin(self, pos):
        """Search for an ending"""

    def pop(self, pos):
        """Remove the ending at the current position"""

    def findending(self, pos):
        """Find the ending at the current position"""

    def checkpending(self) -> None:
        """Check if there are any pending endings"""

class PositionEnding:
    """An ending for a parsing position"""

    ending: Incomplete
    optional: Incomplete
    def __init__(self, ending, optional) -> None: ...
    def checkin(self, pos):
        """Check for the ending"""

class Position(Globable):
    """A position in a text to parse.
    Including those in Globable, functions to implement by subclasses are:
    skip(), identifier(), extract(), isout() and current().
    """

    def __init__(self) -> None: ...
    def skip(self, string) -> None:
        """Skip a string"""

    def identifier(self):
        """Return an identifier for the current position."""

    def extract(self, length) -> None:
        """Extract the next string of the given length, or None if not enough text,"""

    def checkfor(self, string):
        """Check for a string at the given position."""

    def checkforlower(self, string):
        """Check for a string in lower case."""

    def skipcurrent(self):
        """Return the current character and skip it."""

    def __next__(self):
        """Advance the position and return the next character."""

    def checkskip(self, string):
        """Check for a string at the given position; if there, skip it"""

    def error(self, message) -> None:
        """Show an error message and the position identifier."""

class TextPosition(Position):
    """A parse position based on a raw text."""

    pos: int
    text: Incomplete
    def __init__(self, text) -> None:
        """Create the position from some text."""

    def skip(self, string) -> None:
        """Skip a string of characters."""

    def identifier(self):
        """Return a sample of the remaining text."""

    def isout(self):
        """Find out if we are out of the text yet."""

    def current(self):
        """Return the current character, assuming we are not out."""

    def extract(self, length):
        """Extract the next string of the given length, or None if not enough text."""

class Container:
    """A container for text and objects in a lyx file"""

    partkey: Incomplete
    parent: Incomplete
    begin: Incomplete
    contents: Incomplete
    def __init__(self) -> None: ...
    def process(self) -> None:
        """Process contents"""

    def gethtml(self):
        """Get the resulting HTML"""

    def escape(self, line, replacements={"&": "&amp;", "<": "&lt;", ">": "&gt;"}):
        """Escape a line with replacements from a map"""

    def escapeentities(self, line):
        """Escape all Unicode characters to HTML entities."""

    def searchall(self, type):
        """Search for all embedded containers of a given type"""

    def searchremove(self, type):
        """Search for all containers of a type and remove them"""

    def searchprocess(self, type, process):
        """Search for elements of a given type and process them"""

    def locateprocess(self, locate, process) -> None:
        """Search for all embedded containers and process them"""

    def recursivesearch(self, locate, recursive, process) -> None:
        """Perform a recursive search in the container."""

    def extracttext(self):
        """Extract all text from allowed containers."""

    def group(self, index, group, isingroup) -> None:
        """Group some adjoining elements into a group"""

    def remove(self, index) -> None:
        """Remove a container but leave its contents"""

    def tree(self, level: int = 0) -> None:
        """Show in a tree"""

    def getparameter(self, name):
        """Get the value of a parameter, if present."""

    def getparameterlist(self, name):
        """Get the value of a comma-separated parameter as a list."""

    def hasemptyoutput(self):
        """Check if the parent's output is empty."""

class BlackBox(Container):
    """A container that does not output anything"""

    parser: Incomplete
    output: Incomplete
    contents: Incomplete
    def __init__(self) -> None: ...

class StringContainer(Container):
    """A container for a single string"""

    parsed: Incomplete
    parser: Incomplete
    output: Incomplete
    string: str
    def __init__(self) -> None: ...
    def process(self) -> None:
        """Replace special chars from the contents."""

    def replacespecial(self, line):
        """Replace all special chars from a line"""

    def changeline(self, line): ...
    def extracttext(self):
        """Return all text."""

class Constant(StringContainer):
    """A constant string"""

    contents: Incomplete
    string: Incomplete
    output: Incomplete
    def __init__(self, text) -> None: ...

class DocumentParameters:
    """Global parameters for the document."""

    displaymode: bool

class FormulaParser(Parser):
    """Parses a formula"""

    begin: Incomplete
    def parseheader(self, reader):
        """See if the formula is inlined"""

    def parsetype(self, reader):
        """Get the formula type from the first line."""

    def parse(self, reader):
        """Parse the formula until the end"""

    def parseformula(self, reader):
        """Parse the formula contents"""

    def parsesingleliner(self, reader, start, ending):
        """Parse a formula in one line"""

    def parsemultiliner(self, reader, start, ending):
        """Parse a formula in multiple lines"""

class FormulaBit(Container):
    """A bit of a formula"""

    type: str | None
    size: int
    original: str
    contents: Incomplete
    output: Incomplete
    def __init__(self) -> None:
        """The formula bit type can be 'alpha', 'number', 'font'."""
    factory: Incomplete
    def setfactory(self, factory):
        """Set the internal formula factory."""

    def add(self, bit) -> None:
        """Add any kind of formula bit already processed"""

    def skiporiginal(self, string, pos) -> None:
        """Skip a string and add it to the original formula"""

    def computesize(self):
        """Compute the size of the bit as the max of the sizes of all contents."""

    def clone(self):
        """Return a copy of itself."""

class TaggedBit(FormulaBit):
    """A tagged string in a formula"""

    output: Incomplete
    def constant(self, constant, tag):
        """Set the constant and the tag"""
    contents: Incomplete
    def complete(self, contents, tag, breaklines: bool = False):
        """Set the constant and the tag"""

    def selfcomplete(self, tag):
        """Set the self-closing tag, no contents (as in <hr/>)."""

class FormulaConstant(Constant):
    """A constant string in a formula"""

    original: Incomplete
    size: int
    type: str | None
    def __init__(self, string) -> None:
        """Set the constant string"""

    def computesize(self):
        """Compute the size of the constant: always 1."""

    def clone(self):
        """Return a copy of itself."""

class RawText(FormulaBit):
    """A bit of text inside a formula"""

    def detect(self, pos):
        """Detect a bit of raw text"""

    def parsebit(self, pos) -> None:
        """Parse alphabetic text"""

class FormulaSymbol(FormulaBit):
    """A symbol inside a formula"""

    modified: Incomplete
    unmodified: Incomplete
    def detect(self, pos):
        """Detect a symbol"""

    def parsebit(self, pos) -> None:
        """Parse the symbol"""

    def addsymbol(self, symbol, pos) -> None:
        """Add a symbol"""

class FormulaNumber(FormulaBit):
    """A string of digits in a formula"""

    def detect(self, pos):
        """Detect a digit"""

    def parsebit(self, pos):
        """Parse a bunch of digits"""

class Comment(FormulaBit):
    """A LaTeX comment: % to the end of the line."""

    start: Incomplete
    def detect(self, pos):
        """Detect the %."""

    def parsebit(self, pos) -> None:
        """Parse to the end of the line."""

class WhiteSpace(FormulaBit):
    """Some white space inside a formula."""

    def detect(self, pos):
        """Detect the white space."""

    def parsebit(self, pos) -> None:
        """Parse all whitespace."""

class Bracket(FormulaBit):
    """A {} bracket inside a formula"""

    start: Incomplete
    ending: Incomplete
    inner: Incomplete
    def __init__(self) -> None:
        """Create a (possibly literal) new bracket"""

    def detect(self, pos):
        """Detect the start of a bracket"""

    def parsebit(self, pos):
        """Parse the bracket"""

    def parsetext(self, pos):
        """Parse a text bracket"""

    def parseliteral(self, pos):
        """Parse a literal bracket"""

    def parsecomplete(self, pos, innerparser) -> None:
        """Parse the start and end marks"""

    def innerformula(self, pos) -> None:
        """Parse a whole formula inside the bracket"""

    def innertext(self, pos) -> None:
        """Parse some text inside the bracket, following textual rules."""
    literal: str
    def innerliteral(self, pos) -> None:
        """Parse a literal inside the bracket, which does not generate HTML."""

class SquareBracket(Bracket):
    """A [] bracket inside a formula"""

    start: Incomplete
    ending: Incomplete
    def clone(self):
        """Return a new square bracket with the same contents."""

class MathsProcessor:
    """A processor for a maths construction inside the FormulaProcessor."""

    def process(self, contents, index) -> None:
        """Process an element inside a formula."""

class FormulaProcessor:
    """A processor specifically for formulas."""

    processors: Incomplete
    def process(self, bit) -> None:
        """Process the contents of every formula bit, recursively."""

    def processcontents(self, bit) -> None:
        """Process the contents of a formula bit."""

    def processinsides(self, bit) -> None:
        """Process the insides (limits, brackets) in a formula bit."""

    def traversewhole(self, formula) -> None:
        """Traverse over the contents to alter variables and space units."""

    def traverse(self, bit) -> Generator[Incomplete, Incomplete]:
        """Traverse a formula and yield a flattened structure of (bit, list) pairs."""

    def italicize(self, bit, contents) -> None:
        """Italicize the given bit of text."""

class Formula(Container):
    """A LaTeX formula"""

    parser: Incomplete
    output: Incomplete
    def __init__(self) -> None: ...
    def process(self) -> None:
        """Convert the formula to tags"""
    contents: Incomplete
    def classic(self) -> None:
        """Make the contents using classic output generation with XHTML and CSS."""

    def parse(self, pos):
        """Parse using a parse position instead of self.parser."""
    header: Incomplete
    def parsedollarinline(self, pos) -> None:
        """Parse a $...$ formula."""

    def parsedollarblock(self, pos) -> None:
        """Parse a $$...$$ formula."""
    parsed: Incomplete
    def parsedollar(self, pos) -> None:
        """Parse to the next $."""

    def parseinlineto(self, pos, limit) -> None:
        """Parse a \\(...\\) formula."""

    def parseblockto(self, pos, limit) -> None:
        """Parse a \\[...\\] formula."""

    def parseupto(self, pos, limit):
        """Parse a formula that ends with the given command."""

class WholeFormula(FormulaBit):
    """Parse a whole formula"""

    def detect(self, pos):
        """Not outside the formula is enough."""

    def parsebit(self, pos) -> None:
        """Parse with any formula bit"""

class FormulaFactory:
    """Construct bits of formula"""

    types: Incomplete
    skippedtypes: Incomplete
    defining: bool
    instances: Incomplete
    def __init__(self) -> None:
        """Initialize the map of instances."""

    def detecttype(self, type, pos):
        """Detect a bit of a given type."""

    def instance(self, type):
        """Get an instance of the given type."""

    def create(self, type):
        """Create a new formula bit of the given type."""

    def clearskipped(self, pos) -> None:
        """Clear any skipped types."""

    def skipany(self, pos):
        """Skip any skipped types."""

    def parseany(self, pos):
        """Parse any formula bit at the current location."""

    def parsetype(self, type, pos):
        """Parse the given type and return it."""

    def parseformula(self, formula):
        """Parse a string of text that contains a whole formula."""

class FormulaCommand(FormulaBit):
    """A LaTeX command inside a formula"""

    types: Incomplete
    start: Incomplete
    commandmap: ClassVar[dict[str, str] | dict[str, list[str]] | None]
    def detect(self, pos):
        """Find the current command."""
    output: Incomplete
    def parsebit(self, pos):
        """Parse the command."""

    def parsewithcommand(self, command, pos):
        """Parse the command type once we have the command."""

    def parsecommandtype(self, command, type, pos):
        """Parse a given command type."""

    def extractcommand(self, pos):
        """Extract the command from the current position."""

    def emptycommand(self, pos):
        """Check for an empty command: look for command disguised as ending.
        Special case against '{ \\{ \\} }' situation.
        """

    def parseupgreek(self, command, pos):
        """Parse the Greek \\up command.."""

class CommandBit(FormulaCommand):
    """A formula bit that includes a command"""

    command: Incomplete
    translated: Incomplete
    def setcommand(self, command) -> None:
        """Set the command in the bit"""

    def parseparameter(self, pos):
        """Parse a parameter at the current position"""

    def parsesquare(self, pos):
        """Parse a square bracket"""

    def parseliteral(self, pos):
        """Parse a literal bracket."""

    def parsesquareliteral(self, pos):
        """Parse a square bracket literally."""

    def parsetext(self, pos):
        """Parse a text parameter."""

class EmptyCommand(CommandBit):
    """An empty command (without parameters)"""

    commandmap: ClassVar[dict[str, str]]
    contents: Incomplete
    def parsebit(self, pos) -> None:
        """Parse a command without parameters"""

class SpacedCommand(CommandBit):
    """An empty command which should have math spacing in formulas."""

    commandmap: ClassVar[dict[str, str]]
    contents: Incomplete
    def parsebit(self, pos) -> None:
        """Place as contents the command translated and spaced."""

class AlphaCommand(EmptyCommand):
    """A command without parameters whose result is alphabetical."""

    commandmap: ClassVar[dict[str, str]]
    greek_capitals: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the command and set type to alpha"""

class OneParamFunction(CommandBit):
    """A function of one parameter"""

    commandmap: ClassVar[dict[str, str]]
    simplified: bool
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse a function with one parameter"""
    html: Incomplete
    def simplifyifpossible(self) -> None:
        """Try to simplify to a single character."""

class SymbolFunction(CommandBit):
    """Find a function which is represented by a symbol (like _ or ^)"""

    commandmap: ClassVar[dict[str, str]]
    def detect(self, pos):
        """Find the symbol"""
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the symbol"""

class TextFunction(CommandBit):
    """A function where parameters are read as text."""

    commandmap: ClassVar[dict[str, str]]
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse a text parameter"""

    def process(self) -> None:
        """Set the type to font"""

class FontFunction(OneParamFunction):
    """A function of one parameter that changes the font."""

    commandmap: ClassVar[dict[str, str]]
    def process(self) -> None:
        """Simplify if possible using a single character."""

class BigBracket:
    """A big bracket generator."""

    size: Incomplete
    original: Incomplete
    alignment: Incomplete
    pieces: Incomplete
    def __init__(self, size, bracket, alignment: str = "l") -> None:
        """Set the size and symbol for the bracket."""

    def getpiece(self, index):
        """Return the nth piece for the bracket."""

    def getpiece1(self, index):
        """Return the only piece for a single-piece bracket."""

    def getpiece3(self, index):
        """Get the nth piece for a 3-piece bracket: parenthesis or square bracket."""

    def getpiece4(self, index):
        """Get the nth piece for a 4-piece bracket: curly bracket."""

    def getcell(self, index):
        """Get the bracket piece as an array cell."""

    def getcontents(self):
        """Get the bracket as an array or as a single bracket."""

    def getsinglebracket(self):
        """Return the bracket as a single sign."""

class FormulaEquation(CommandBit):
    """A simple numbered equation."""

    piece: str
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the array"""

class FormulaCell(FormulaCommand):
    """An array cell inside a row"""

    alignment: Incomplete
    output: Incomplete
    def setalignment(self, alignment): ...
    def parsebit(self, pos) -> None: ...

class FormulaRow(FormulaCommand):
    """An array row inside an array"""

    cellseparator: Incomplete
    alignments: Incomplete
    output: Incomplete
    def setalignments(self, alignments): ...
    def parsebit(self, pos) -> None:
        """Parse a whole row"""

    def createcell(self, index):
        """Create the cell that corresponds to the given index."""

class MultiRowFormula(CommandBit):
    """A formula with multiple rows."""

    rows: Incomplete
    size: Incomplete
    def parserows(self, pos) -> None:
        """Parse all rows, finish when no more row ends"""

    def iteraterows(self, pos) -> Generator[Incomplete]:
        """Iterate over all rows, end when no more row ends"""

    def addempty(self) -> None:
        """Add an empty row."""

    def addrow(self, row) -> None:
        """Add a row to the contents and to the list of rows."""

class FormulaArray(MultiRowFormula):
    """An array within a formula"""

    piece: str
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the array"""
    valign: str
    alignments: Incomplete
    def parsealignments(self, pos) -> None:
        """Parse the different alignments"""

class FormulaMatrix(MultiRowFormula):
    """A matrix (array with center alignment)."""

    piece: str
    output: Incomplete
    valign: str
    alignments: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the matrix, set alignments to 'c'."""

class FormulaCases(MultiRowFormula):
    """A cases statement"""

    piece: str
    output: Incomplete
    alignments: Incomplete
    contents: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the cases"""

class EquationEnvironment(MultiRowFormula):
    """A \\begin{}...\\end equation environment with rows and cells."""

    output: Incomplete
    alignments: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the whole environment."""

class BeginCommand(CommandBit):
    """A \\begin{}...\\end command and what it entails (array, cases, aligned)"""

    commandmap: ClassVar[dict[str, str]]
    types: Incomplete
    size: Incomplete
    def parsebit(self, pos) -> None:
        """Parse the begin command"""

    def findbit(self, piece):
        """Find the command bit corresponding to the \\begin{piece}"""

class CombiningFunction(OneParamFunction):
    commandmap: ClassVar[dict[str, str]]
    def parsebit(self, pos) -> None:
        """Parse a combining function."""

    def parsesingleparameter(self, pos):
        """Parse a parameter, or a single letter."""

class OversetFunction(OneParamFunction):
    """A function that decorates some bit of text with an overset."""

    commandmap: ClassVar[dict[str, str]]
    symbol: Incomplete
    parameter: Incomplete
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse an overset-function"""

class UndersetFunction(OneParamFunction):
    """A function that decorates some bit of text with an underset."""

    commandmap: ClassVar[dict[str, str]]
    symbol: Incomplete
    parameter: Incomplete
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse an underset-function"""

class LimitCommand(EmptyCommand):
    """A command which accepts limits above and below, in display mode."""

    commandmap: ClassVar[dict[str, str]]
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Parse a limit command."""

class LimitPreviousCommand(LimitCommand):
    """A command to limit the previous command."""

    commandmap: ClassVar[None]  # type: ignore[assignment]
    output: Incomplete
    def parsebit(self, pos) -> None:
        """Do nothing."""

class LimitsProcessor(MathsProcessor):
    """A processor for limits inside an element."""

    def process(self, contents, index) -> None:
        """Process the limits for an element."""

    def checklimits(self, contents, index):
        """Check if the current position has a limits command."""

    def limitsahead(self, contents, index) -> None:
        """Limit the current element based on the next."""

    def modifylimits(self, contents, index) -> None:
        """Modify a limits commands so that the limits appear above and below."""

    def getlimit(self, contents, index):
        """Get the limit for a limits command."""

    def modifyscripts(self, contents, index) -> None:
        """Modify the super- and subscript to appear vertically aligned."""

    def checkscript(self, contents, index):
        """Check if the current element is a sub- or superscript."""

    def checkcommand(self, contents, index, type):
        """Check for the given type as the current element."""

    def getscript(self, contents, index):
        """Get the sub- or superscript."""

class BracketCommand(OneParamFunction):
    """A command which defines a bracket."""

    commandmap: ClassVar[dict[str, str]]
    def parsebit(self, pos) -> None:
        """Parse the bracket."""
    original: Incomplete
    command: Incomplete
    contents: Incomplete
    def create(self, direction, character):
        """Create the bracket for the given character."""

class BracketProcessor(MathsProcessor):
    """A processor for bracket commands."""

    def process(self, contents, index):
        """Convert the bracket using Unicode pieces, if possible."""

    def processleft(self, contents, index) -> None:
        """Process a left bracket."""

    def checkleft(self, contents, index):
        """Check if the command at the given index is left."""

    def checkright(self, contents, index):
        """Check if the command at the given index is right."""

    def checkdirection(self, bit, command):
        """Check if the given bit is the desired bracket command."""

    def findright(self, contents, index):
        """Find the right bracket starting at the given index, or 0."""

    def findmax(self, contents, leftindex, rightindex):
        """Find the max size of the contents between the two given indices."""

    def resize(self, command, size) -> None:
        """Resize a bracket command to the given size."""

class ParameterDefinition:
    """The definition of a parameter in a hybrid function."""

    parambrackets: ClassVar[list[tuple[str, str]]]
    name: str
    literal: bool
    optional: bool
    value: Incomplete
    literalvalue: Incomplete
    def __init__(self) -> None: ...
    def parse(self, pos):
        """Parse a parameter definition: [$0], {$x}, {$1!}..."""

    def read(self, pos, function) -> None:
        """Read the parameter itself using the definition."""

class ParameterFunction(CommandBit):
    """A function with a variable number of parameters defined in a template."""

    params: Incomplete
    def readparams(self, readtemplate, pos) -> None:
        """Read the params according to the template."""

    def paramdefs(self, readtemplate) -> Generator[Incomplete]:
        """Read each param definition in the template"""

    def getparam(self, name):
        """Get a parameter as parsed."""

    def getvalue(self, name):
        """Get the value of a parameter."""

    def getliteralvalue(self, name):
        """Get the literal value of a parameter."""

class HybridFunction(ParameterFunction):
    """
    A parameter function where the output is also defined using a template.
    The template can use a number of functions; each function has an associated
    tag.
    Example: [f0{$1},span class="fbox"] defines a function f0 which corresponds
    to a span of class fbox, yielding <span class="fbox">$1</span>.
    Literal parameters can be used in tags definitions:
      [f0{$1},span style="color: $p;"]
    yields <span style="color: $p;">$1</span>, where $p is a literal parameter.
    Sizes can be specified in hybridsizes, e.g. adding parameter sizes. By
    default the resulting size is the max of all arguments. Sizes are used
    to generate the right parameters.
    A function followed by a single / is output as a self-closing XHTML tag:
      [f0/,hr]
    will generate <hr/>.
    """

    commandmap: ClassVar[dict[str, list[str]]]
    contents: Incomplete
    def parsebit(self, pos) -> None:
        """Parse a function with [] and {} parameters"""

    def writeparams(self, writetemplate):
        """Write all params according to the template"""

    def writepos(self, pos):
        """Write all params as read in the parse position."""

    def writeparam(self, pos):
        """Write a single param of the form $0, $x..."""

    def writefunction(self, pos):
        """Write a single function f0,...,fn."""

    def readtag(self, pos):
        """Get the tag corresponding to the given index. Does parameter substitution."""

    def writebracket(self, direction, character):
        """Return a new bracket looking at the given direction."""
    size: Incomplete
    def computehybridsize(self) -> None:
        """Compute the size of the hybrid function."""

class HybridSize:
    """The size associated with a hybrid function."""

    configsizes: ClassVar[dict[str, str]]
    def getsize(self, function):
        """Read the size for a function and parse it."""

def math2html(formula):
    """Convert some TeX math to HTML."""

def main() -> None:
    """Main function, called if invoked from the command line"""
