"""Support for Acrobat Forms in ReportLab documents

This module is somewhat experimental at this time.

Includes basic support for
    textfields,
    select fields (drop down lists), and
    check buttons.

The public interface consists of functions at the moment.
At some later date these operations may be made into canvas
methods. (comments?)

The ...Absolute(...) functions position the fields with respect
to the absolute canvas coordinate space -- that is, they do not
respect any coordinate transforms in effect for the canvas.

The ...Relative(...) functions position the ONLY THE LOWER LEFT
CORNER of the field using the coordinate transform in effect for
the canvas.  THIS WILL ONLY WORK CORRECTLY FOR TRANSLATED COORDINATES
-- THE SHAPE, SIZE, FONTSIZE, AND ORIENTATION OF THE FIELD WILL NOT BE EFFECTED
BY SCALING, ROTATION, SKEWING OR OTHER NON-TRANSLATION COORDINATE
TRANSFORMS.

Please note that all field names (titles) in a given document must be unique.
Textfields and select fields only support the "base 14" canvas fonts
at this time.

See individual function docstrings below for more information.

The function test1(...) generates a simple test file.

THIS CONTRIBUTION WAS COMMISSIONED BY REPORTLAB USERS
WHO WISH TO REMAIN ANONYMOUS.
"""

from _typeshed import Incomplete

from reportlab.pdfbase.pdfdoc import PDFObject

def textFieldAbsolute(canvas, title, x, y, width, height, value: str = "", maxlen: int = 1000000, multiline: int = 0):
    """Place a text field on the current page
    with name title at ABSOLUTE position (x,y) with
    dimensions (width, height), using value as the default value and
    maxlen as the maximum permissible length.  If multiline is set make
    it a multiline field.
    """

def textFieldRelative(canvas, title, xR, yR, width, height, value: str = "", maxlen: int = 1000000, multiline: int = 0):
    """same as textFieldAbsolute except the x and y are relative to the canvas coordinate transform"""

def buttonFieldAbsolute(canvas, title, value, x, y, width: float = 16.7704, height: float = 14.907):
    """Place a check button field on the current page
    with name title and default value value (one of "Yes" or "Off")
    at ABSOLUTE position (x,y).
    """

def buttonFieldRelative(canvas, title, value, xR, yR, width: float = 16.7704, height: float = 14.907):
    """same as buttonFieldAbsolute except the x and y are relative to the canvas coordinate transform"""

def selectFieldAbsolute(canvas, title, value, options, x, y, width, height) -> None:
    """Place a select field (drop down list) on the current page
    with name title and
    with options listed in the sequence options
    default value value (must be one of options)
    at ABSOLUTE position (x,y) with dimensions (width, height).
    """

def selectFieldRelative(canvas, title, value, options, xR, yR, width, height):
    """same as textFieldAbsolute except the x and y are relative to the canvas coordinate transform"""

def getForm(canvas):
    """get form from canvas, create the form if needed"""

class AcroForm(PDFObject):
    fields: Incomplete
    def __init__(self) -> None: ...
    def textField(
        self, canvas, title, xmin, ymin, xmax, ymax, value: str = "", maxlen: int = 1000000, multiline: int = 0
    ) -> None: ...
    def selectField(self, canvas, title, value, options, xmin, ymin, xmax, ymax) -> None: ...
    def buttonField(self, canvas, title, value, xmin, ymin, width: float = 16.7704, height: float = 14.907) -> None: ...
    def format(self, document): ...

FormPattern: Incomplete

def FormFontsDictionary(): ...
def FormResources(): ...

ZaDbPattern: Incomplete
FormResourcesDictionaryPattern: Incomplete
FORMFONTNAMES: Incomplete
EncodingPattern: Incomplete
PDFDocEncodingPattern: Incomplete

def FormFont(BaseFont, Name): ...

FormFontPattern: Incomplete

def resetPdfForm() -> None: ...
def TextField(
    title,
    value,
    xmin,
    ymin,
    xmax,
    ymax,
    page,
    maxlen: int = 1000000,
    font: str = "Helvetica-Bold",
    fontsize: int = 9,
    R: int = 0,
    G: int = 0,
    B: float = 0.627,
    multiline: int = 0,
): ...

TextFieldPattern: Incomplete

def SelectField(
    title,
    value,
    options,
    xmin,
    ymin,
    xmax,
    ymax,
    page,
    font: str = "Helvetica-Bold",
    fontsize: int = 9,
    R: int = 0,
    G: int = 0,
    B: float = 0.627,
): ...

SelectFieldPattern: Incomplete

def ButtonField(title, value, xmin, ymin, page, width: float = 16.7704, height: float = 14.907): ...

ButtonFieldPattern: Incomplete

def buttonStreamDictionary(width: float = 16.7704, height: float = 14.907):
    """everything except the length for the button appearance streams"""

def ButtonStream(content, width: float = 16.7704, height: float = 14.907): ...
