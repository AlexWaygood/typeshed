"""Generate ReportLab logo in a variety of sizes and formats.


This module includes some reusable routines for ReportLab's
 'Corporate Image' - the logo, standard page backdrops and
 so on - you are advised to do the same for your own company!
"""

from _typeshed import Incomplete
from typing import Final

from reportlab.graphics.widgetbase import Widget
from reportlab.lib.attrmap import *
from reportlab.lib.validators import *

__version__: Final[str]

class RL_CorpLogo(Widget):
    """Dinu's fat letter logo as hacked into decent paths by Robin"""

    fillColor: Incomplete
    strokeColor: Incomplete
    strokeWidth: float
    background: Incomplete
    border: Incomplete
    borderWidth: int
    shadow: float
    height: int
    width: int
    x: int
    skewX: int
    showPage: int
    oColors: Incomplete
    pageColors: Incomplete
    prec: Incomplete
    def __init__(self) -> None: ...
    def demo(self): ...
    @staticmethod
    def applyPrec(P, prec): ...
    def draw(self): ...

class RL_CorpLogoReversed(RL_CorpLogo):
    background: Incomplete
    fillColor: Incomplete
    def __init__(self) -> None: ...

class RL_CorpLogoThin(Widget):
    """The ReportLab Logo.

    New version created by John Precedo on 7-8 August 2001.
    Based on bitmapped imaged from E-Id.
    Improved by Robin Becker.
    """

    fillColor: Incomplete
    strokeColor: Incomplete
    x: int
    y: int
    height: Incomplete
    width: Incomplete
    def __init__(self) -> None: ...
    def demo(self): ...
    def draw(self): ...

class ReportLabLogo:
    """vector reportlab logo centered in a 250x by 150y rectangle"""

    origin: Incomplete
    dimensions: Incomplete
    powered_by: Incomplete
    def __init__(self, atx: int = 0, aty: int = 0, width=180.0, height=108.0, powered_by: int = 0) -> None: ...
    def draw(self, canvas) -> None: ...

class RL_BusinessCard(Widget):
    """Widget that creates a single business card.
    Uses RL_CorpLogo for the logo.

    For a black border around your card, set self.border to 1.
    To change the details on the card, over-ride the following properties:
    self.name, self.position, self.telephone, self.mobile, self.fax, self.email, self.web
    The office locations are set in self.rh_blurb_top ("London office" etc), and
    self.rh_blurb_bottom ("New York office" etc).
    """

    fillColor: Incomplete
    strokeColor: Incomplete
    altStrokeColor: Incomplete
    x: int
    y: int
    height: Incomplete
    width: Incomplete
    borderWidth: Incomplete
    bleed: Incomplete
    cropMarks: int
    border: int
    name: str
    position: str
    telephone: str
    mobile: str
    fax: str
    email: str
    web: str
    rh_blurb_top: Incomplete
    def __init__(self) -> None: ...
    def demo(self): ...
    def draw(self): ...

def test(formats=["pdf", "eps", "jpg", "gif", "svg"]) -> None:
    """This function produces a pdf with examples."""
