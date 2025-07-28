"""
This module contains code to translate formulae across cells in a worksheet.

The idea is that if A1 has formula "=B1+C1", then translating it to cell A2
results in formula "=B2+C2". The algorithm relies on the formula tokenizer
to identify the parts of the formula that need to change.

"""

from _typeshed import Incomplete
from re import Pattern
from typing import Final

class TranslatorError(Exception):
    """
    Raised when a formula can't be translated across cells.

    This error arises when a formula's references would be translated outside
    the worksheet's bounds on the top or left. Excel represents these
    situations with a #REF! literal error. E.g., if the formula at B2 is
    '=A1', attempting to translate the formula to B1 raises TranslatorError,
    since there's no cell above A1. Similarly, translating the same formula
    from B2 to A2 raises TranslatorError, since there's no cell to the left of
    A1.

    """

class Translator:
    """
    Modifies a formula so that it can be translated from one cell to another.

    `formula`: The str string to translate. Must include the leading '='
               character.
    `origin`: The cell address (in A1 notation) where this formula was
              defined (excluding the worksheet name).

    """

    tokenizer: Incomplete
    def __init__(self, formula, origin) -> None: ...
    def get_tokens(self):
        """Returns a list with the tokens comprising the formula."""
    ROW_RANGE_RE: Final[Pattern[str]]
    COL_RANGE_RE: Final[Pattern[str]]
    CELL_REF_RE: Final[Pattern[str]]
    @staticmethod
    def translate_row(row_str, rdelta):
        """
        Translate a range row-snippet by the given number of rows.
        """

    @staticmethod
    def translate_col(col_str, cdelta):
        """
        Translate a range col-snippet by the given number of columns
        """

    @staticmethod
    def strip_ws_name(range_str):
        """Splits out the worksheet reference, if any, from a range reference."""

    @classmethod
    def translate_range(cls, range_str, rdelta, cdelta):
        """
        Translate an A1-style range reference to the destination cell.

        `rdelta`: the row offset to add to the range
        `cdelta`: the column offset to add to the range
        `range_str`: an A1-style reference to a range. Potentially includes
                     the worksheet reference. Could also be a named range.

        """

    def translate_formula(self, dest=None, row_delta: int = 0, col_delta: int = 0):
        """
        Convert the formula into A1 notation, or as row and column coordinates

        The formula is converted into A1 assuming it is assigned to the cell
        whose address is `dest` (no worksheet name).

        """
