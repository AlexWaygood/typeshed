from _typeshed import Incomplete

from reportlab.pdfbase.pdfdoc import PDFObject

__all__ = ("AcroForm",)

class PDFFromString(PDFObject):
    def __init__(self, s) -> None: ...
    def format(self, document): ...

class RadioGroup(PDFObject):
    TU: Incomplete
    Ff: Incomplete
    kids: Incomplete
    T: Incomplete
    V: Incomplete
    def __init__(self, name, tooltip: str = "", fieldFlags: str = "noToggleToOff required radio") -> None: ...
    def format(self, doc): ...

class AcroForm(PDFObject):
    formFontNames: Incomplete
    referenceMap: Incomplete
    fonts: Incomplete
    fields: Incomplete
    sigFlags: Incomplete
    extras: Incomplete
    def __init__(self, canv, **kwds) -> None: ...
    @property
    def canv(self): ...
    def fontRef(self, f): ...
    def format(self, doc): ...
    def colorTuple(self, c): ...
    def streamFillColor(self, c): ...
    def streamStrokeColor(self, c): ...
    def checkboxAP(
        self,
        key,
        value,
        buttonStyle: str = "circle",
        shape: str = "square",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        size: int = 20,
        dashLen: int = 3,
    ): ...
    @staticmethod
    def circleArcStream(size, r, arcs=(0, 1, 2, 3), rotated: bool = False): ...
    def zdMark(self, c, size, ds, iFontName): ...
    def getRef(self, obj): ...
    def getRefStr(self, obj): ...
    @staticmethod
    def stdColors(t, b, f): ...
    @staticmethod
    def varyColors(key, t, b, f): ...
    def checkForceBorder(
        self, x, y, width, height, forceBorder, shape, borderStyle, borderWidth, borderColor, fillColor
    ) -> None: ...
    def checkbox(
        self,
        checked: bool = False,
        buttonStyle: str = "check",
        shape: str = "square",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        size: int = 20,
        x: int = 0,
        y: int = 0,
        tooltip=None,
        name=None,
        annotationFlags: str = "print",
        fieldFlags: str = "required",
        forceBorder: bool = False,
        relative: bool = False,
        dashLen: int = 3,
    ) -> None: ...
    def radio(
        self,
        value=None,
        selected: bool = False,
        buttonStyle: str = "circle",
        shape: str = "circle",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        size: int = 20,
        x: int = 0,
        y: int = 0,
        tooltip=None,
        name=None,
        annotationFlags: str = "print",
        fieldFlags: str = "noToggleToOff required radio",
        forceBorder: bool = False,
        relative: bool = False,
        dashLen: int = 3,
    ) -> None: ...
    def makeStream(self, width, height, stream, **D): ...
    def txAP(
        self,
        key,
        value,
        iFontName,
        rFontName,
        fontSize,
        shape: str = "square",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        width: int = 120,
        height: int = 36,
        dashLen: int = 3,
        wkind: str = "textfield",
        labels=[],
        I=[],
        sel_bg: str = "0.600006 0.756866 0.854904 rg",
        sel_fg: str = "0 g",
    ): ...
    def makeFont(self, fontName): ...
    def textfield(
        self,
        value: str = "",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        width: int = 120,
        height: int = 36,
        x: int = 0,
        y: int = 0,
        tooltip=None,
        name=None,
        annotationFlags: str = "print",
        fieldFlags: str = "",
        forceBorder: bool = False,
        relative: bool = False,
        maxlen: int = 100,
        fontName=None,
        fontSize=None,
        dashLen: int = 3,
    ): ...
    def listbox(
        self,
        value: str = "",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        width: int = 120,
        height: int = 36,
        x: int = 0,
        y: int = 0,
        tooltip=None,
        name=None,
        annotationFlags: str = "print",
        fieldFlags: str = "",
        forceBorder: bool = False,
        relative: bool = False,
        fontName=None,
        fontSize=None,
        dashLen: int = 3,
        maxlen=None,
        options=[],
    ): ...
    def choice(
        self,
        value: str = "",
        fillColor=None,
        borderColor=None,
        textColor=None,
        borderWidth: int = 1,
        borderStyle: str = "solid",
        width: int = 120,
        height: int = 36,
        x: int = 0,
        y: int = 0,
        tooltip=None,
        name=None,
        annotationFlags: str = "print",
        fieldFlags: str = "combo",
        forceBorder: bool = False,
        relative: bool = False,
        fontName=None,
        fontSize=None,
        dashLen: int = 3,
        maxlen=None,
        options=[],
    ): ...
    def checkboxRelative(self, **kwds) -> None:
        """same as checkbox except the x and y are relative to the canvas coordinate transform"""

    def radioRelative(self, **kwds) -> None:
        """same as radio except the x and y are relative to the canvas coordinate transform"""

    def textfieldRelative(self, **kwds) -> None:
        """same as textfield except the x and y are relative to the canvas coordinate transform"""

    def listboxRelative(self, **kwds) -> None:
        """same as textfield except the x and y are relative to the canvas coordinate transform"""

    def choiceRelative(self, **kwds) -> None:
        """same as textfield except the x and y are relative to the canvas coordinate transform"""

    @property
    def encRefStr(self): ...

class CBMark:
    opNames: Incomplete
    opCount: Incomplete
    ops: Incomplete
    points: Incomplete
    slack: Incomplete
    def __init__(self, ops, points, bounds, slack: float = 0.05) -> None: ...
    def scaledRender(self, size, ds: int = 0):
        """
        >>> print(cbmarks['check'].scaledRender(20))
        12.97075 14.68802 m 15.00139 17.16992 l 15.9039 18.1727 17.93454 18.67409 19.2883 18.67409 c 19.46379 18.27298 l 17.13231 15.51532 l 11.91783 8.62117 l 8.307799 3.030641 l 7.430362 1.526462 l 7.305014 1.275766 7.154596 .97493 6.9039 .824513 c 6.577994 .674095 5.825905 .674095 5.47493 .674095 c 4.672702 .674095 4.497214 .674095 4.321727 .799443 c 4.071031 .97493 3.945682 1.325905 3.770195 1.67688 c 3.218663 2.830084 2.240947 5.337047 2.240947 6.590529 c 2.240947 7.016713 2.491643 7.21727 2.817549 7.442897 c 3.344011 7.818942 4.0961 8.245125 4.747911 8.245125 c 5.249304 8.245125 5.299443 7.818942 5.449861 7.417827 c 5.951253 6.239554 l 6.026462 6.038997 6.252089 5.337047 6.527855 5.337047 c 6.778552 5.337047 7.079387 5.913649 7.179666 6.089136 c 12.97075 14.68802 l h f
        >>> print(cbmarks['cross'].scaledRender(20))
        19.9104 17.43931 m 12.41908 10 l 19.9104 2.534682 l 18.37572 1 l 10.9104 8.491329 l 3.445087 1 l 1.910405 2.534682 l 9.427746 10 l 1.910405 17.46532 l 3.445087 19 l 10.9104 11.50867 l 18.37572 19 l 19.9104 17.43931 l h f
        >>> print(cbmarks['circle'].scaledRender(20))
        1.872576 9.663435 m 1.872576 14.64958 5.936288 18.61357 10.89751 18.61357 c 15.8338 18.61357 19.87258 14.59972 19.87258 9.663435 c 19.87258 4.727147 15.8338 .688366 10.89751 .688366 c 5.936288 .688366 1.872576 4.677285 1.872576 9.663435 c h f
        >>> print(cbmarks['star'].scaledRender(20))
        10.85542 18.3253 m 12.90361 11.84337 l 19.84337 11.84337 l 14.25301 7.650602 l 16.42169 1 l 10.85542 5.096386 l 5.289157 1 l 7.481928 7.650602 l 1.843373 11.84337 l 8.759036 11.84337 l 10.85542 18.3253 l h f
        >>> print(cbmarks['diamond'].scaledRender(20))
        17.43533 9.662031 m 15.63282 7.484006 l 10.85118 .649513 l 8.422809 4.329624 l 5.919332 7.659249 l 4.267038 9.662031 l 6.16968 12.0153 l 10.85118 18.64951 l 12.75382 15.4701 15.00695 12.49096 17.43533 9.662031 c h f
        """
