"""
Various utilities that could not be gathered logically in a specific module.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from collections.abc import Iterable
from typing import Any, AnyStr, Final, Literal, NamedTuple
from typing_extensions import TypeAlias

_Unit: TypeAlias = Literal["pt", "mm", "cm", "in"]

PIL_MEM_BLOCK_SIZE_IN_MIB: Final = 16

class Padding(NamedTuple):
    """Padding(top, right, bottom, left)"""

    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0
    @classmethod
    def new(cls, padding: float | tuple[float, ...] | list[float]):
        """Return a 4-tuple of padding values from a single value or a 2, 3 or 4-tuple according to CSS rules"""

def buffer_subst(buffer: bytearray, placeholder: str, value: str) -> bytearray: ...
def escape_parens(s: AnyStr) -> AnyStr:
    """Add a backslash character before , ( and )"""

def get_scale_factor(unit: _Unit | float) -> float:
    """
    Get how many pts are in a unit. (k)

    Args:
        unit (str, float, int): Any of "pt", "mm", "cm", "in", or a number.
    Returns:
        float: The number of points in that unit (assuming 72dpi)
    Raises:
        ValueError
    """

def convert_unit(
    # to_convert has a recursive type
    to_convert: float | Iterable[float | Iterable[Any]],
    old_unit: str | float,
    new_unit: str | float,
) -> float | tuple[float, ...]:
    """
     Convert a number or sequence of numbers from one unit to another.

     If either unit is a number it will be treated as the number of points per unit.  So 72 would mean 1 inch.

     Args:
        to_convert (float, int, Iterable): The number / list of numbers, or points, to convert
        old_unit (str, float, int): A unit accepted by fpdf.FPDF or a number
        new_unit (str, float, int): A unit accepted by fpdf.FPDF or a number
    Returns:
        (float, tuple): to_convert converted from old_unit to new_unit or a tuple of the same
    """

ROMAN_NUMERAL_MAP: Final[tuple[tuple[str, int], ...]]

def int2roman(n: int | None) -> str:
    """Convert an integer to Roman numeral"""

def int_to_letters(n: int) -> str:
    """Convert an integer to a letter value (A to Z for the first 26, then AA to ZZ, and so on)"""

def print_mem_usage(prefix: str) -> None: ...
def get_mem_usage(prefix: str) -> str: ...
def get_process_rss() -> str: ...
def get_process_rss_as_mib() -> float | None:
    """Inspired by psutil source code"""

def get_process_heap_and_stack_sizes() -> tuple[str, str]: ...
def get_pymalloc_allocated_over_total_size() -> str:
    """
    Get PyMalloc stats from sys._debugmallocstats()
    From experiments, not very reliable
    """

def get_gc_managed_objs_total_size() -> str:
    """From experiments, not very reliable"""

def get_tracemalloc_traced_memory() -> str:
    """Requires python -X tracemalloc"""

def get_pillow_allocated_memory() -> str: ...
