"""Gazillions of miscellaneous internal utility functions"""

import datetime
import zipimport
from _typeshed import Incomplete, SupportsItems
from collections.abc import Generator, Iterable
from os import PathLike
from types import TracebackType
from typing import AnyStr, Final, Literal, TypeVar, overload

from reportlab.lib.rltempfile import get_rl_tempdir as get_rl_tempdir, get_rl_tempfile as get_rl_tempfile

from .rl_safe_eval import (
    rl_extended_literal_eval as rl_extended_literal_eval,
    rl_safe_exec as rl_safe_exec,
    safer_globals as safer_globals,
)

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

__version__: Final[str]

class _UNSET_:
    @staticmethod
    def __bool__() -> Literal[False]: ...

__UNSET__: Final[_UNSET_]

isPyPy: bool

def isFunction(v: object) -> bool: ...
def isMethod(v: object, mt=...) -> bool: ...
def isModule(v: object) -> bool: ...
def isSeq(v: object, _st=...) -> bool: ...
def isNative(v: object) -> bool: ...

strTypes: tuple[type[str], type[bytes]]

def asBytes(v: str | bytes, enc: str = "utf8") -> bytes: ...
def asUnicode(v: str | bytes, enc: str = "utf8") -> str: ...
def asUnicodeEx(v: str | bytes, enc: str = "utf8") -> str: ...
def asNative(v: str | bytes, enc: str = "utf8") -> str: ...
def int2Byte(i: int) -> bytes: ...
def isStr(v: object) -> bool: ...
def isBytes(v: object) -> bool: ...
def isUnicode(v: object) -> bool: ...
def isClass(v: object) -> bool: ...
def isNonPrimitiveInstance(x: object) -> bool: ...
def instantiated(v: object) -> bool: ...
def bytestr(x: object, enc: str = "utf8") -> bytes: ...
def encode_label(args) -> str: ...
def decode_label(label: str): ...
def rawUnicode(s: str | bytes) -> str:
    """converts first 256 unicodes 1-1"""

def rawBytes(s: str | bytes) -> bytes:
    """converts first 256 unicodes 1-1"""

rl_exec = exec

def char2int(s: int | str | bytes) -> int: ...
def rl_reraise(t, v: BaseException, b: TracebackType | None = None) -> None: ...
def rl_add_builtins(**kwd) -> None: ...
def zipImported(ldr: zipimport.zipimporter | None = None) -> zipimport.zipimporter | None: ...

class CIDict(dict[_KT, _VT]):
    def __init__(self, *args, **kwds) -> None: ...
    def update(self, D: SupportsItems[_KT, _VT]) -> None: ...  # type:ignore[override]

def markfilename(filename, creatorcode=None, filetype=None): ...

__rl_loader__: Incomplete

def rl_glob(pattern: AnyStr, glob=...) -> list[AnyStr]: ...
def isFileSystemDistro() -> bool:
    """return truth if a file system distribution"""

def isCompactDistro() -> bool:
    """return truth if not a file system distribution"""

def isSourceDistro() -> bool:
    """return truth if a source file system distribution"""

def normalize_path(p: PathLike[AnyStr]) -> PathLike[AnyStr]: ...
def recursiveImport(modulename, baseDir=None, noCWD: int = 0, debug: int = 0):
    """Dynamically imports possible packagized module, or raises ImportError"""

haveImages: Final[bool]

class ArgvDictValue:
    """A type to allow clients of getArgvDict to specify a conversion function"""

    value: Incomplete
    func: Incomplete
    def __init__(self, value, func) -> None: ...

def getArgvDict(**kw):
    """Builds a dictionary from its keyword arguments with overrides from sys.argv.
    Attempts to be smart about conversions, but the value can be an instance
    of ArgDictValue to allow specifying a conversion function.
    """

def getHyphenater(hDict=None): ...
def open_for_read_by_name(name, mode: str = "b"): ...
def rlUrlRead(name): ...
def open_for_read(name, mode: str = "b"): ...
def open_and_read(name, mode: str = "b"): ...
def open_and_readlines(name, mode: str = "t"): ...
def rl_isfile(fn, os_path_isfile=...): ...
def rl_isdir(pn, os_path_isdir=..., os_path_normpath=...): ...
def rl_listdir(pn, os_path_isdir=..., os_path_normpath=..., os_listdir=...): ...
def rl_getmtime(pn, os_path_isfile=..., os_path_normpath=..., os_path_getmtime=..., time_mktime=...): ...
def __rl_get_module__(name, dir): ...
def rl_get_module(name, dir): ...

class ImageReader:
    """Wraps up PIL to get data from bitmaps"""

    fileName: Incomplete
    fp: Incomplete
    def __init__(self, fileName, ident=None) -> None: ...
    def identity(self) -> str:
        """try to return information that will identify the instance"""

    @classmethod
    def check_pil_image_size(cls, im) -> None: ...
    @classmethod
    def set_max_image_size(cls, max_image_size=None) -> None: ...
    def jpeg_fh(self) -> None: ...
    def getSize(self) -> tuple[int, int]: ...
    mode: Incomplete
    def getRGBData(self):
        """Return byte array of RGB data as string"""

    def getImageData(self): ...
    def getTransparent(self): ...

class LazyImageReader(ImageReader): ...

def getImageData(imageFileName):
    """Get width, height and RGB pixels from image file.  Wraps PIL"""

class DebugMemo:
    """Intended as a simple report back encapsulator

    Typical usages:

    1. To record error data::

        dbg = DebugMemo(fn='dbgmemo.dbg',myVar=value)
        dbg.add(anotherPayload='aaaa',andagain='bbb')
        dbg.dump()

    2. To show the recorded info::

        dbg = DebugMemo(fn='dbgmemo.dbg',mode='r')
        dbg.load()
        dbg.show()

    3. To re-use recorded information::

        dbg = DebugMemo(fn='dbgmemo.dbg',mode='r')
            dbg.load()
        myTestFunc(dbg.payload('myVar'),dbg.payload('andagain'))

    In addition to the payload variables the dump records many useful bits
    of information which are also printed in the show() method.
    """

    fn: Incomplete
    stdout: Incomplete
    store: Incomplete
    def __init__(
        self,
        fn: str = "rl_dbgmemo.dbg",
        mode: str = "w",
        getScript: int = 1,
        modules=(),
        capture_traceback: int = 1,
        stdout=None,
        **kw,
    ) -> None: ...
    def add(self, **kw) -> None: ...
    def dump(self) -> None: ...
    def dumps(self): ...
    def load(self) -> None: ...
    def loads(self, s) -> None: ...
    specials: Incomplete
    def show(self) -> None: ...
    def payload(self, name): ...
    def __setitem__(self, name, value) -> None: ...
    def __getitem__(self, name): ...

def flatten(L):
    """recursively flatten the list or tuple L"""

def find_locals(func, depth: int = 0):
    """apply func to the locals at each stack frame till func returns a non false value"""

class _FmtSelfDict:
    obj: Incomplete
    def __init__(self, obj, overrideArgs) -> None: ...
    def __getitem__(self, k): ...

class FmtSelfDict:
    """mixin to provide the _fmt method"""

def simpleSplit(text: str | bytes, fontName: str | None, fontSize: float, maxWidth: float | None): ...
@overload
def escapeTextOnce(text: None) -> None:
    """Escapes once only"""

@overload
def escapeTextOnce(text: str | bytes) -> str: ...
def fileName2FSEnc(fn): ...
def prev_this_next(items):
    """
    Loop over a collection with look-ahead and look-back.

    From Thomas Guest,
    http://wordaligned.org/articles/zippy-triples-served-with-python

    Seriously useful looping tool (Google "zippy triples")
    lets you loop a collection and see the previous and next items,
    which get set to None at the ends.

    To be used in layout algorithms where one wants a peek at the
    next item coming down the pipe.

    """

def commasplit(s: str | bytes) -> list[str]:
    """
    Splits the string s at every unescaped comma and returns the result as a list.
    To escape a comma, double it. Individual items are stripped.
    To avoid the ambiguity of 3 successive commas to denote a comma at the beginning
    or end of an item, add a space between the item seperator and the escaped comma.

    >>> commasplit(u'a,b,c') == [u'a', u'b', u'c']
    True
    >>> commasplit('a,, , b , c    ') == [u'a,', u'b', u'c']
    True
    >>> commasplit(u'a, ,,b, c') == [u'a', u',b', u'c']
    """

def commajoin(l: Iterable[str | bytes]) -> str:
    """
    Inverse of commasplit, except that whitespace around items is not conserved.
    Adds more whitespace than needed for simplicity and performance.

    >>> commasplit(commajoin(['a', 'b', 'c'])) == [u'a', u'b', u'c']
    True
    >>> commasplit((commajoin([u'a,', u' b ', u'c'])) == [u'a,', u'b', u'c']
    True
    >>> commasplit((commajoin([u'a ', u',b', u'c'])) == [u'a', u',b', u'c']
    """

def findInPaths(fn, paths, isfile: bool = True, fail: bool = False):
    """search for relative files in likely places"""

def annotateException(msg: str, enc: str = "utf8", postMsg: str = "", sep: str = " ") -> None:
    """add msg to the args of an existing exception"""

def escapeOnce(data: str) -> str:
    """Ensure XML output is escaped just once, irrespective of input

    >>> escapeOnce('A & B')
    'A &amp; B'
    >>> escapeOnce('C &amp; D')
    'C &amp; D'
    >>> escapeOnce('E &amp;amp; F')
    'E &amp; F'

    """

class IdentStr(str):
    """useful for identifying things that get split"""

    def __new__(cls, value): ...

class RLString(str):
    """allows specification of extra properties of a string using a dictionary of extra attributes
    eg fontName = RLString('proxima-nova-bold',
                    svgAttrs=dict(family='"proxima-nova"',weight='bold'))
    """

    def __new__(cls, v, **kwds): ...

def makeFileName(s):
    """force filename strings to unicode so python can handle encoding stuff"""

class FixedOffsetTZ(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, h, m, name) -> None: ...
    def utcoffset(self, dt): ...
    def tzname(self, dt): ...
    def dst(self, dt): ...

class TimeStamp:
    tzname: str
    t: Incomplete
    lt: Incomplete
    YMDhms: Incomplete
    dhh: Incomplete
    dmm: Incomplete
    def __init__(self, invariant=None) -> None: ...
    @property
    def datetime(self): ...
    @property
    def asctime(self): ...

def recursiveGetAttr(obj, name, g=None):
    """Can call down into e.g. object1.object2[4].attr"""

def recursiveSetAttr(obj, name, value) -> None:
    """Can call down into e.g. object1.object2[4].attr = value"""

def recursiveDelAttr(obj, name) -> None: ...
def yieldNoneSplits(L) -> Generator[Incomplete, None, None]:
    """yield sublists of L separated by None; the Nones disappear"""

class KlassStore:
    lim: int
    store: dict[str, type]
    def __init__(self, lim: int = 127) -> None: ...
    def add(self, k: str, v: type) -> None: ...
    def __contains__(self, k) -> bool: ...
    def __getitem__(self, k: str) -> type: ...
    def get(self, k, default=None): ...
