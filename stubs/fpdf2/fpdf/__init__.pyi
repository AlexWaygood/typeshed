"""
Root module.
Gives direct access to some classes defined in submodules:

* `fpdf.fpdf.FPDF`
* `fpdf.enums.Align`
* `fpdf.enums.TextMode`
* `fpdf.enums.XPos`
* `fpdf.enums.YPos`
* `fpdf.errors.FPDFException`
* `fpdf.fonts.FontFace`
* `fpdf.fonts.TextStyle`
* `fpdf.prefs.ViewerPreferences`
* `fpdf.template.Template`
* `fpdf.template.FlexTemplate`
"""

from pathlib import Path

from .enums import Align as Align, TextMode as TextMode, XPos as XPos, YPos as YPos
from .fonts import FontFace as FontFace, TextStyle as TextStyle
from .fpdf import FPDF as FPDF, FPDFException as FPDFException, TitleStyle as TitleStyle
from .html import HTML2FPDF as HTML2FPDF, HTMLMixin as HTMLMixin
from .prefs import ViewerPreferences as ViewerPreferences
from .template import FlexTemplate as FlexTemplate, Template as Template
from .util import get_scale_factor as get_scale_factor

__license__: str
__version__: str
FPDF_VERSION: str
FPDF_FONT_DIR: Path

__all__ = [
    "__version__",
    "__license__",
    "FPDF",
    "FPDFException",
    "FontFace",
    "Align",
    "TextMode",
    "XPos",
    "YPos",
    "Template",
    "FlexTemplate",
    "TitleStyle",
    "TextStyle",
    "ViewerPreferences",
    "HTMLMixin",
    "HTML2FPDF",
    "FPDF_VERSION",
    "FPDF_FONT_DIR",
    "get_scale_factor",
]
