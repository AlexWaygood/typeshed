"""
Module for parsing/evaluating Microsoft Excel formulas.
"""

from typing import Final
from typing_extensions import Self

from .book import Book, Name
from .timemachine import *

__all__ = [
    "oBOOL",
    "oERR",
    "oNUM",
    "oREF",
    "oREL",
    "oSTRG",
    "oUNK",
    "decompile_formula",
    "dump_formula",
    "evaluate_name_formula",
    "okind_dict",
    "rangename3d",
    "rangename3drel",
    "cellname",
    "cellnameabs",
    "colname",
    "FMLA_TYPE_CELL",
    "FMLA_TYPE_SHARED",
    "FMLA_TYPE_ARRAY",
    "FMLA_TYPE_COND_FMT",
    "FMLA_TYPE_DATA_VAL",
    "FMLA_TYPE_NAME",
    "Operand",
    "Ref3D",
]

FMLA_TYPE_CELL: Final[int]
FMLA_TYPE_SHARED: Final[int]
FMLA_TYPE_ARRAY: Final[int]
FMLA_TYPE_COND_FMT: Final[int]
FMLA_TYPE_DATA_VAL: Final[int]
FMLA_TYPE_NAME: Final[int]
oBOOL: Final[int]
oERR: Final[int]
oNUM: Final[int]
oREF: Final[int]
oREL: Final[int]
oSTRG: Final[int]
oUNK: Final[int]
okind_dict: Final[dict[int, str]]

class FormulaError(Exception): ...

class Operand:
    """
    Used in evaluating formulas.
    The following table describes the kinds and how their values
    are represented.

    .. raw:: html

        <table border="1" cellpadding="7">
        <tr>
        <th>Kind symbol</th>
        <th>Kind number</th>
        <th>Value representation</th>
        </tr>
        <tr>
        <td>oBOOL</td>
        <td align="center">3</td>
        <td>integer: 0 => False; 1 => True</td>
        </tr>
        <tr>
        <td>oERR</td>
        <td align="center">4</td>
        <td>None, or an int error code (same as XL_CELL_ERROR in the Cell class).
        </td>
        </tr>
        <tr>
        <td>oMSNG</td>
        <td align="center">5</td>
        <td>Used by Excel as a placeholder for a missing (not supplied) function
        argument. Should *not* appear as a final formula result. Value is None.</td>
        </tr>
        <tr>
        <td>oNUM</td>
        <td align="center">2</td>
        <td>A float. Note that there is no way of distinguishing dates.</td>
        </tr>
        <tr>
        <td>oREF</td>
        <td align="center">-1</td>
        <td>The value is either None or a non-empty list of
        absolute Ref3D instances.<br>
        </td>
        </tr>
        <tr>
        <td>oREL</td>
        <td align="center">-2</td>
        <td>The value is None or a non-empty list of
        fully or partially relative Ref3D instances.
        </td>
        </tr>
        <tr>
        <td>oSTRG</td>
        <td align="center">1</td>
        <td>A Unicode string.</td>
        </tr>
        <tr>
        <td>oUNK</td>
        <td align="center">0</td>
        <td>The kind is unknown or ambiguous. The value is None</td>
        </tr>
        </table>
    """

    value: float | str | None
    kind: int
    text: str
    rank: int
    def __init__(self, akind: int | None = None, avalue: float | str | None = None, arank: int = 0, atext: str = "?") -> None: ...

class Ref3D(tuple[int, int, int, int, int, int, int, int, int, int, int, int]):
    """
    Represents an absolute or relative 3-dimensional reference to a box
    of one or more cells.

    The ``coords`` attribute is a tuple of the form::

      (shtxlo, shtxhi, rowxlo, rowxhi, colxlo, colxhi)

    where ``0 <= thingxlo <= thingx < thingxhi``.

    .. note::
      It is quite possible to have ``thingx > nthings``; for example
      ``Print_Titles`` could have ``colxhi == 256`` and/or ``rowxhi == 65536``
      irrespective of how many columns/rows are actually used in the worksheet.
      The caller will need to decide how to handle this situation.
      Keyword: :class:`IndexError` :-)

    The components of the coords attribute are also available as individual
    attributes: ``shtxlo``, ``shtxhi``, ``rowxlo``, ``rowxhi``, ``colxlo``, and
    ``colxhi``.

    The ``relflags`` attribute is a 6-tuple of flags which indicate whether
    the corresponding (sheet|row|col)(lo|hi) is relative (1) or absolute (0).

    .. note::
      There is necessarily no information available as to what cell(s)
      the reference could possibly be relative to. The caller must decide what
      if any use to make of ``oREL`` operands.

    .. note:
      A partially relative reference may well be a typo.
      For example, define name ``A1Z10`` as ``$a$1:$z10`` (missing ``$`` after
      ``z``) while the cursor is on cell ``Sheet3!A27``.

      The resulting :class:`Ref3D` instance will have
      ``coords = (2, 3, 0, -16, 0, 26)``
      and ``relflags = (0, 0, 0, 1, 0, 0).<br>

      So far, only one possibility of a sheet-relative component in
      a reference has been noticed: a 2D reference located in the
      "current sheet".

      This will appear as ``coords = (0, 1, ...)`` and
      ``relflags = (1, 1, ...)``.

    .. versionadded:: 0.6.0
    """

    coords: tuple[int, int, int, int, int, int]
    relflags: tuple[int, int, int, int, int, int]
    shtxlo: int
    shtxhi: int
    rowxlo: int
    rowxhi: int
    colxlo: int
    colxhi: int
    def __new__(cls, atuple: tuple[int, int, int, int, int, int, int, int, int, int, int, int]) -> Self: ...
    def __init__(self, atuple: tuple[int, int, int, int, int, int, int, int, int, int, int, int]) -> None: ...

def evaluate_name_formula(bk: Book, nobj: Name, namex: str, blah: int = 0, level: int = 0) -> None: ...
def decompile_formula(
    bk: Book,
    fmla: bytes,
    fmlalen: int,
    fmlatype: int | None = None,
    browx: int | None = None,
    bcolx: int | None = None,
    blah: int = 0,
    level: int = 0,
    r1c1: int = 0,
) -> str | None: ...
def dump_formula(bk: Book, data: bytes, fmlalen: int, bv: int, reldelta: int, blah: int = 0, isname: int = 0) -> None: ...
def cellname(rowx: int, colx: int) -> str:
    """Utility function: ``(5, 7)`` => ``'H6'``"""

def cellnameabs(rowx: int, colx: int, r1c1: int = 0) -> str:
    """Utility function: ``(5, 7)`` => ``'$H$6'``"""

def colname(colx: int) -> str:
    """Utility function: ``7`` => ``'H'``, ``27`` => ``'AB'``"""

def rangename3d(book: Book, ref3d: Ref3D) -> str:
    """
    Utility function:
    ``Ref3D(1, 4, 5, 20, 7, 10)`` =>
    ``'Sheet2:Sheet3!$H$6:$J$20'``
    (assuming Excel's default sheetnames)
    """

def rangename3drel(book: Book, ref3d: Ref3D, browx: int | None = None, bcolx: int | None = None, r1c1: int = 0) -> str:
    """
    Utility function:
    ``Ref3D(coords=(0, 1, -32, -22, -13, 13), relflags=(0, 0, 1, 1, 1, 1))``

    In R1C1 mode => ``'Sheet1!R[-32]C[-13]:R[-23]C[12]'``

    In A1 mode => depends on base cell ``(browx, bcolx)``
    """
