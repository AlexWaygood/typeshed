"""Very simple and fast XML parser, used for intra-paragraph text.

Devised by Aaron Watters in the bad old days before Python had fast
parsers available.  Constructs the lightest possible in-memory
representation; parses most files we have seen in pure python very
quickly.

The output structure is the same as the one produced by pyRXP,
our validating C-based parser, which was written later.  It will
use pyRXP if available.

This is used to parse intra-paragraph markup.

Example parse::

    <this type="xml">text <b>in</b> xml</this>

    ( "this",
      {"type": "xml"},
      [ "text ",
        ("b", None, ["in"], None),
        " xml"
        ]
       None )

    { 0: "this"
      "type": "xml"
      1: ["text ",
          {0: "b", 1:["in"]},
          " xml"]
    }

Ie, xml tag translates to a tuple:
 (name, dictofattributes, contentlist, miscellaneousinfo)

where miscellaneousinfo can be anything, (but defaults to None)
(with the intention of adding, eg, line number information)

special cases: name of "" means "top level, no containing tag".
Top level parse always looks like this::

    ("", list, None, None)

 contained text of None means <simple_tag/>

In order to support stuff like::

    <this></this><one></one>

AT THE MOMENT &amp; ETCETERA ARE IGNORED. THEY MUST BE PROCESSED
IN A POST-PROCESSING STEP.

PROLOGUES ARE NOT UNDERSTOOD.  OTHER STUFF IS PROBABLY MISSING.
"""

from _typeshed import Incomplete

RequirePyRXP: int
simpleparse: int

class _smartDecode:
    @staticmethod
    def __call__(s): ...

smartDecode: _smartDecode
NONAME: str
NAMEKEY: int
CONTENTSKEY: int
CDATAMARKER: str
LENCDATAMARKER: Incomplete
CDATAENDMARKER: str
replacelist: Incomplete

def unEscapeContentList(contentList): ...
def parsexmlSimple(xmltext, oneOutermostTag: int = 0, eoCB=None, entityReplacer=...):
    """official interface: discard unused cursor info"""

parsexml = parsexmlSimple

def parseFile(filename): ...

verbose: int

def skip_prologue(text, cursor):
    """skip any prologue found after cursor, return index of rest of text"""

def parsexml0(xmltext, startingat: int = 0, toplevel: int = 1, entityReplacer=...):
    """simple recursive descent xml parser...
    return (dictionary, endcharacter)
    special case: comment returns (None, endcharacter)
    """

def pprettyprint(parsedxml):
    """pretty printer mainly for testing"""

def testparse(s, dump: int = 0) -> None: ...
def test(dump: int = 0) -> None: ...
