"""Provides support for the test suite.

The test suite as a whole, and individual tests, need to share
certain support functions.  We have to put these in here so they
can always be imported, and so that individual tests need to import
nothing more than "reportlab.whatever..."
"""

import unittest
from _typeshed import Incomplete
from configparser import ConfigParser
from typing import Final, Literal

__version__: Final[str]

def haveRenderPM(): ...
def isWritable(D): ...

RL_HOME: Incomplete
testsFolder: Incomplete

DEJAVUSANS: tuple[
    Literal["DejaVuSans"], Literal["DejaVuSans-Bold"], Literal["DejaVuSans-Oblique"], Literal["DejaVuSans-BoldOblique"]
] = ...

def haveDejaVu() -> bool: ...
def setOutDir(name):
    """Is it a writable file system distro being invoked within
    test directory?  If so, can write test output here.  If not,
    it had better go in a temp directory.  Only do this once per
    process
    """

def mockUrlRead(name): ...
def outputfile(fn):
    """This works out where to write test output.  If running
    code in a locked down file system, this will be a
    temp directory; otherwise, the output of 'test_foo.py' will
    normally be a file called 'test_foo.pdf', next door.
    """

def printLocation(depth: int = 1) -> None: ...
def makeSuiteForClasses(*classes, testMethodPrefix=None):
    """Return a test suite with tests loaded from provided classes."""

def getCVSEntries(folder, files: int = 1, folders: int = 0):
    """Returns a list of filenames as listed in the CVS/Entries file.

    'folder' is the folder that should contain the CVS subfolder.
    If there is no such subfolder an empty list is returned.
    'files' is a boolean; 1 and 0 means to return files or not.
    'folders' is a boolean; 1 and 0 means to return folders or not.
    """

class ExtConfigParser(ConfigParser):
    """A slightly extended version to return lists of strings."""

    pat: Incomplete
    def getstringlist(self, section, option):
        """Coerce option to a list of strings or return unchanged if that fails."""

class GlobDirectoryWalker:
    """A forward iterator that traverses files in a directory tree."""

    index: int
    pattern: Incomplete
    stack: Incomplete
    files: Incomplete
    directory: Incomplete
    def __init__(self, directory, pattern: str = "*") -> None: ...
    def __getitem__(self, index): ...
    def filterFiles(self, folder, files):
        """Filter hook, overwrite in subclasses as needed."""

class RestrictedGlobDirectoryWalker(GlobDirectoryWalker):
    """An restricted directory tree iterator."""

    ignorePatterns: Incomplete
    def __init__(self, directory, pattern: str = "*", ignore=None) -> None: ...
    def filterFiles(self, folder, files):
        """Filters all items from files matching patterns to ignore."""

class CVSGlobDirectoryWalker(GlobDirectoryWalker):
    """An directory tree iterator that checks for CVS data."""

    def filterFiles(self, folder, files):
        """Filters files not listed in CVS subfolder.

        This will look in the CVS subfolder of 'folder' for
        a file named 'Entries' and filter all elements from
        the 'files' list that are not listed in 'Entries'.
        """

class SecureTestCase(unittest.TestCase):
    """Secure testing base class with additional pre- and postconditions.

    We try to ensure that each test leaves the environment it has
    found unchanged after the test is performed, successful or not.

    Currently we restore sys.path and the working directory, but more
    of this could be added easily, like removing temporary files or
    similar things.

    Use this as a base class replacing unittest.TestCase and call
    these methods in subclassed versions before doing your own
    business!
    """

    def setUp(self) -> None:
        """Remember sys.path and current working directory."""

    def tearDown(self) -> None:
        """Restore previous sys.path and working directory."""

class NearTestCase(unittest.TestCase):
    @staticmethod
    def assertNear(a, b, accuracy: float = 1e-05) -> None: ...

class ScriptThatMakesFileTest(unittest.TestCase):
    """Runs a Python script at OS level, expecting it to produce a file.

    It CDs to the working directory to run the script.
    """

    scriptDir: Incomplete
    scriptName: Incomplete
    outFileName: Incomplete
    verbose: Incomplete
    def __init__(self, scriptDir, scriptName, outFileName, verbose: int = 0) -> None: ...
    cwd: Incomplete
    def setUp(self) -> None: ...
    def tearDown(self) -> None: ...
    def runTest(self) -> None: ...

def equalStrings(a, b, enc: str = "utf8"): ...
def eqCheck(r, x) -> None: ...
def rlextraNeeded(): ...
def rlSkipIf(cond, reason, __module__=None): ...
def rlSkipUnless(cond, reason, __module__=None): ...
def rlSkip(reason, __module__=None): ...
