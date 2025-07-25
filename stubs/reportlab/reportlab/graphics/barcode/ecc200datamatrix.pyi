from _typeshed import Incomplete

from reportlab.graphics.barcode.common import Barcode

class ECC200DataMatrix(Barcode):
    """This code only supports a Type 12 (44x44) C40 encoded data matrix.
    This is the size and encoding that Royal Mail wants on all mail from October 1st 2015.
    see https://bitbucket.org/rptlab/reportlab/issues/69/implementations-of-code-128-auto-and-data
    """

    barWidth: int
    row_modules: int
    col_modules: int
    row_regions: int
    col_regions: int
    cw_data: int
    cw_ecc: int
    row_usable_modules: Incomplete
    col_usable_modules: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    valid: int
    validated: Incomplete
    def validate(self) -> None: ...
    encoded: Incomplete
    def encode(self): ...
    def computeSize(self, *args) -> None: ...
    def draw(self) -> None: ...

__all__ = ("ECC200DataMatrix",)
