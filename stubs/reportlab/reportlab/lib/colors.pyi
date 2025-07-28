"""Defines standard colour-handling classes and colour names.

We define standard classes to hold colours in two models:  RGB and CMYK.
rhese can be constructed from several popular formats.  We also include

- pre-built colour objects for the HTML standard colours

- pre-built colours used in ReportLab's branding

- various conversion and construction functions

These tests are here because doctest cannot find them otherwise.
>>> toColor('rgb(128,0,0)')==toColor('rgb(50%,0%,0%)')
True
>>> toColor('rgb(50%,0%,0%)')!=Color(0.5,0,0,1)
True
>>> toColor('hsl(0,100%,50%)')==toColor('rgb(255,0,0)')
True
>>> toColor('hsl(-120,100%,50%)')==toColor('rgb(0,0,255)')
True
>>> toColor('hsl(120,100%,50%)')==toColor('rgb(0,255,0)')
True
>>> toColor('rgba( 255,0,0,0.5)')==Color(1,0,0,0.5)
True
>>> toColor('cmyk(1,0,0,0 )')==CMYKColor(1,0,0,0)
True
>>> toColor('pcmyk( 100 , 0 , 0 , 0 )')==PCMYKColor(100,0,0,0)
True
>>> toColor('cmyka(1,0,0,0,0.5)')==CMYKColor(1,0,0,0,alpha=0.5)
True
>>> toColor('pcmyka(100,0,0,0,0.5)')==PCMYKColor(100,0,0,0,alpha=0.5)
True
>>> toColor('pcmyka(100,0,0,0)')
Traceback (most recent call last):
    ....
ValueError: css color 'pcmyka(100,0,0,0)' has wrong number of components
"""

from collections.abc import Iterable, Iterator
from typing import Final, Literal, TypeVar, overload
from typing_extensions import Self, TypeAlias

_ColorT = TypeVar("_ColorT", bound=Color)
# NOTE: Reportlab is very inconsistent and sometimes uses the interpretation
#       used in reportlab.pdfgen.textobject instead, so we pick a different name
_ConvertibleToColor: TypeAlias = Color | list[float] | tuple[float, float, float, float] | tuple[float, float, float] | str | int

__version__: Final[str]

class Color:
    """This class is used to represent color.  Components red, green, blue
    are in the range 0 (dark) to 1 (full intensity).
    """

    red: float
    green: float
    blue: float
    alpha: float
    def __init__(self, red: float = 0, green: float = 0, blue: float = 0, alpha: float = 1) -> None:
        """Initialize with red, green, blue in range [0-1]."""

    @property
    def __key__(self) -> tuple[float, ...]:
        """simple comparison by component; cmyk != color ever
        >>> from reportlab import cmp
        >>> cmp(Color(0,0,0),None)
        -1
        >>> cmp(Color(0,0,0),black)
        0
        >>> cmp(Color(0,0,0),CMYKColor(0,0,0,1)),Color(0,0,0).rgba()==CMYKColor(0,0,0,1).rgba()
        (1, True)
        """

    def __hash__(self) -> int: ...
    def __comparable__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool:
        """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""

    def __gt__(self, other: object) -> bool:
        """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""

    def __ge__(self, other: object) -> bool:
        """Return a >= b.  Computed by @total_ordering from (not a < b)."""

    def rgb(self) -> tuple[float, float, float]:
        """Returns a three-tuple of components"""

    def rgba(self) -> tuple[float, float, float, float]:
        """Returns a four-tuple of components"""

    def bitmap_rgb(self) -> tuple[int, int, int]: ...
    def bitmap_rgba(self) -> tuple[int, int, int, int]: ...
    def hexval(self) -> str: ...
    def hexvala(self) -> str: ...
    def int_rgb(self) -> int: ...
    def int_rgba(self) -> int: ...
    def int_argb(self) -> int: ...
    @property
    def cKwds(self) -> Iterator[tuple[str, int]]: ...
    # NOTE: Possible arguments depend on __init__, so this violates LSP
    #       For now we just leave it unchecked
    def clone(self, **kwds) -> Self:
        """copy then change values in kwds"""

    @property
    def normalizedAlpha(self) -> float: ...

def opaqueColor(c: object) -> bool:
    """utility to check we have a color that's not fully transparent"""

class CMYKColor(Color):
    """This represents colors using the CMYK (cyan, magenta, yellow, black)
    model commonly used in professional printing.  This is implemented
    as a derived class so that renderers which only know about RGB "see it"
    as an RGB color through its 'red','green' and 'blue' attributes, according
    to an approximate function.

    The RGB approximation is worked out when the object in constructed, so
    the color attributes should not be changed afterwards.

    Extra attributes may be attached to the class to support specific ink models,
    and renderers may look for these.
    """

    cyan: float
    magenta: float
    yellow: float
    black: float
    spotName: str | None
    density: float
    knockout: bool | None
    alpha: float
    def __init__(
        self,
        cyan: float = 0,
        magenta: float = 0,
        yellow: float = 0,
        black: float = 0,
        spotName: str | None = None,
        density: float = 1,
        knockout: bool | None = None,
        alpha: float = 1,
    ) -> None:
        """
        Initialize with four colors in range [0-1]. the optional
        spotName, density & knockout may be of use to specific renderers.
        spotName is intended for use as an identifier to the renderer not client programs.
        density is used to modify the overall amount of ink.
        knockout is a renderer dependent option that determines whether the applied colour
        knocksout (removes) existing colour; None means use the global default.
        """

    def fader(self, n: int, reverse: bool = False) -> list[Self]:
        """return n colors based on density fade
        *NB* note this dosen't reach density zero
        """

    def cmyk(self) -> tuple[float, float, float, float]:
        """Returns a tuple of four color components - syntactic sugar"""

    def cmyka(self) -> tuple[float, float, float, float, float]:
        """Returns a tuple of five color components - syntactic sugar"""

class PCMYKColor(CMYKColor):
    """100 based CMYKColor with density and a spotName; just like Rimas uses"""

    def __init__(
        self,
        cyan: float,
        magenta: float,
        yellow: float,
        black: float,
        density: float = 100,
        spotName: str | None = None,
        knockout: bool | None = None,
        alpha: float = 100,
    ) -> None: ...

class CMYKColorSep(CMYKColor):
    """special case color for making separating pdfs"""

    def __init__(
        self,
        cyan: float = 0,
        magenta: float = 0,
        yellow: float = 0,
        black: float = 0,
        spotName: str | None = None,
        density: float = 1,
        alpha: float = 1,
    ) -> None: ...

class PCMYKColorSep(PCMYKColor, CMYKColorSep):
    """special case color for making separating pdfs"""

    def __init__(
        self,
        cyan: float = 0,
        magenta: float = 0,
        yellow: float = 0,
        black: float = 0,
        spotName: str | None = None,
        density: float = 100,
        alpha: float = 100,
    ) -> None: ...

def cmyk2rgb(cmyk: tuple[float, float, float, float], density: float = 1) -> tuple[float, float, float]:
    """Convert from a CMYK color tuple to an RGB color tuple"""

def rgb2cmyk(r: float, g: float, b: float) -> tuple[float, float, float, float]:
    """one way to get cmyk from rgb"""

def color2bw(colorRGB: Color) -> Color:
    """Transform an RGB color to a black and white equivalent."""

def HexColor(val: str | int, htmlOnly: bool = False, hasAlpha: bool = False) -> Color:
    """This function converts a hex string, or an actual integer number,
    into the corresponding color.  E.g., in "#AABBCC" or 0xAABBCC,
    AA is the red, BB is the green, and CC is the blue (00-FF).

    An alpha value can also be given in the form #AABBCCDD or 0xAABBCCDD where
    DD is the alpha value if hasAlpha is True.

    For completeness I assume that #aabbcc or 0xaabbcc are hex numbers
    otherwise a pure integer is converted as decimal rgb.  If htmlOnly is true,
    only the #aabbcc form is allowed.

    >>> HexColor('#ffffff')
    Color(1,1,1,1)
    >>> HexColor('#FFFFFF')
    Color(1,1,1,1)
    >>> HexColor('0xffffff')
    Color(1,1,1,1)
    >>> HexColor('16777215')
    Color(1,1,1,1)

    An '0x' or '#' prefix is required for hex (as opposed to decimal):

    >>> HexColor('ffffff')
    Traceback (most recent call last):
    ValueError: invalid literal for int() with base 10: 'ffffff'

    >>> HexColor('#FFFFFF', htmlOnly=True)
    Color(1,1,1,1)
    >>> HexColor('0xffffff', htmlOnly=True)
    Traceback (most recent call last):
    ValueError: not a hex string
    >>> HexColor('16777215', htmlOnly=True)
    Traceback (most recent call last):
    ValueError: not a hex string

    """

def linearlyInterpolatedColor(c0: _ColorT, c1: _ColorT, x0: float, x1: float, x: float) -> _ColorT:
    """
    Linearly interpolates colors. Can handle RGB, CMYK and PCMYK
    colors - give ValueError if colours aren't the same.
    Doesn't currently handle 'Spot Color Interpolation'.
    """

@overload
def obj_R_G_B(
    c: Color | list[float] | tuple[float, float, float, float] | tuple[float, float, float],
) -> tuple[float, float, float]:
    """attempt to convert an object to (red,green,blue)"""

@overload
def obj_R_G_B(c: None) -> None: ...

transparent: Color
ReportLabBlueOLD: Color
ReportLabBlue: Color
ReportLabBluePCMYK: Color
ReportLabLightBlue: Color
ReportLabFidBlue: Color
ReportLabFidRed: Color
ReportLabGreen: Color
ReportLabLightGreen: Color
aliceblue: Color
antiquewhite: Color
aqua: Color
aquamarine: Color
azure: Color
beige: Color
bisque: Color
black: Color
blanchedalmond: Color
blue: Color
blueviolet: Color
brown: Color
burlywood: Color
cadetblue: Color
chartreuse: Color
chocolate: Color
coral: Color
cornflowerblue: Color
cornflower: Color
cornsilk: Color
crimson: Color
cyan: Color
darkblue: Color
darkcyan: Color
darkgoldenrod: Color
darkgray: Color
darkgrey: Color
darkgreen: Color
darkkhaki: Color
darkmagenta: Color
darkolivegreen: Color
darkorange: Color
darkorchid: Color
darkred: Color
darksalmon: Color
darkseagreen: Color
darkslateblue: Color
darkslategray: Color
darkslategrey: Color
darkturquoise: Color
darkviolet: Color
deeppink: Color
deepskyblue: Color
dimgray: Color
dimgrey: Color
dodgerblue: Color
firebrick: Color
floralwhite: Color
forestgreen: Color
fuchsia: Color
gainsboro: Color
ghostwhite: Color
gold: Color
goldenrod: Color
gray: Color
grey: Color
green: Color
greenyellow: Color
honeydew: Color
hotpink: Color
indianred: Color
indigo: Color
ivory: Color
khaki: Color
lavender: Color
lavenderblush: Color
lawngreen: Color
lemonchiffon: Color
lightblue: Color
lightcoral: Color
lightcyan: Color
lightgoldenrodyellow: Color
lightgreen: Color
lightgrey: Color
lightpink: Color
lightsalmon: Color
lightseagreen: Color
lightskyblue: Color
lightslategray: Color
lightslategrey: Color
lightsteelblue: Color
lightyellow: Color
lime: Color
limegreen: Color
linen: Color
magenta: Color
maroon: Color
mediumaquamarine: Color
mediumblue: Color
mediumorchid: Color
mediumpurple: Color
mediumseagreen: Color
mediumslateblue: Color
mediumspringgreen: Color
mediumturquoise: Color
mediumvioletred: Color
midnightblue: Color
mintcream: Color
mistyrose: Color
moccasin: Color
navajowhite: Color
navy: Color
oldlace: Color
olive: Color
olivedrab: Color
orange: Color
orangered: Color
orchid: Color
palegoldenrod: Color
palegreen: Color
paleturquoise: Color
palevioletred: Color
papayawhip: Color
peachpuff: Color
peru: Color
pink: Color
plum: Color
powderblue: Color
purple: Color
red: Color
rosybrown: Color
royalblue: Color
saddlebrown: Color
salmon: Color
sandybrown: Color
seagreen: Color
seashell: Color
sienna: Color
silver: Color
skyblue: Color
slateblue: Color
slategray: Color
slategrey: Color
snow: Color
springgreen: Color
steelblue: Color
tan: Color
teal: Color
thistle: Color
tomato: Color
turquoise: Color
violet: Color
wheat: Color
white: Color
whitesmoke: Color
yellow: Color
yellowgreen: Color
fidblue: Color
fidred: Color
fidlightblue: Color
ColorType: type[Color]

def colorDistance(col1: Color, col2: Color) -> float:
    """Returns a number between 0 and root(3) stating how similar
    two colours are - distance in r,g,b, space.  Only used to find
    names for things.
    """

def cmykDistance(col1: Color, col2: Color) -> float:
    """Returns a number between 0 and root(4) stating how similar
    two colours are - distance in r,g,b, space.  Only used to find
    names for things.
    """

def getAllNamedColors() -> dict[str, Color]: ...
@overload
def describe(aColor: Color, mode: Literal[0] = 0) -> None:
    """finds nearest colour match to aColor.
    mode=0 print a string desription
    mode=1 return a string description
    mode=2 return (distance, colorName)
    """

@overload
def describe(aColor: Color, mode: Literal[1]) -> str: ...
@overload
def describe(aColor: Color, mode: Literal[2]) -> tuple[str, float]: ...
def hue2rgb(m1: float, m2: float, h: float) -> float: ...
def hsl2rgb(h: float, s: float, l: float) -> tuple[float, float, float]: ...

class _cssParse:
    def pcVal(self, v: str) -> float: ...
    def rgbPcVal(self, v: str) -> float: ...
    def rgbVal(self, v: str) -> float: ...
    def hueVal(self, v: str) -> float: ...
    def alphaVal(self, v: str, c: float = 1, n: str = "alpha") -> float: ...
    s: str
    def __call__(self, s: str) -> Color: ...

cssParse: _cssParse

class _toColor:
    extraColorsNS: dict[str, Color]
    def __init__(self) -> None: ...
    def setExtraColorsNameSpace(self, NS: dict[str, Color]) -> None: ...
    def __call__(self, arg: _ConvertibleToColor, default: Color | None = None) -> Color: ...

toColor: _toColor

@overload
def toColorOrNone(arg: None, default: Color | None) -> None:
    """as above but allows None as a legal value"""

@overload
def toColorOrNone(arg: _ConvertibleToColor, default: Color | None = None) -> Color: ...
def setColors(**kw: _ConvertibleToColor) -> None: ...
def Whiter(c: _ColorT, f: float) -> _ColorT:
    """given a color combine with white as c*f w*(1-f) 0<=f<=1"""

def Blacker(c: _ColorT, f: float) -> _ColorT:
    """given a color combine with black as c*f+b*(1-f) 0<=f<=1"""

def fade(aSpotColor: CMYKColor, percentages: Iterable[float]) -> list[CMYKColor]:
    """Waters down spot colors and returns a list of new ones

    e.g fade(myColor, [100,80,60,40,20]) returns a list of five colors
    """
