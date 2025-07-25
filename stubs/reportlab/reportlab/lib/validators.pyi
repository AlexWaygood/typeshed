"""Standard verifying functions used by attrmap."""

from _typeshed import Incomplete
from typing import Final

__version__: Final[str]

class Percentage(float): ...

class Validator:
    """base validator class"""

    def __call__(self, x): ...
    def normalize(self, x): ...
    def normalizeTest(self, x): ...

class _isAnything(Validator):
    def test(self, x): ...

class _isNothing(Validator):
    def test(self, x): ...

class _isBoolean(Validator):
    def test(self, x): ...
    def normalize(self, x): ...

class _isString(Validator):
    def test(self, x): ...

class _isCodec(Validator):
    def test(self, x): ...

class _isNumber(Validator):
    def test(self, x): ...
    def normalize(self, x): ...

class _isInt(Validator):
    def test(self, x): ...
    def normalize(self, x): ...

class _isNumberOrNone(_isNumber):
    def test(self, x): ...
    def normalize(self, x): ...

class _isListOfNumbersOrNone(Validator):
    """ListOfNumbersOrNone validator class."""

    def test(self, x): ...

class isNumberInRange(_isNumber):
    min: Incomplete
    max: Incomplete
    def __init__(self, min, max) -> None: ...
    def test(self, x): ...

class _isListOfShapes(Validator):
    """ListOfShapes validator class."""

    def test(self, x): ...

class _isListOfStringsOrNone(Validator):
    """ListOfStringsOrNone validator class."""

    def test(self, x): ...

class _isTransform(Validator):
    """Transform validator class."""

    def test(self, x): ...

class _isColor(Validator):
    """Color validator class."""

    def test(self, x): ...

class _isColorOrNone(Validator):
    """ColorOrNone validator class."""

    def test(self, x): ...

class _isNormalDate(Validator):
    def test(self, x): ...
    def normalize(self, x): ...

class _isValidChild(Validator):
    """ValidChild validator class."""

    def test(self, x):
        """Is this child allowed in a drawing or group?
        I.e. does it descend from Shape or UserNode?
        """

class _isValidChildOrNone(_isValidChild):
    def test(self, x): ...

class _isCallable(Validator):
    def test(self, x): ...

class OneOf(Validator):
    """Make validator functions for list of choices.

    Usage:
    f = reportlab.lib.validators.OneOf('happy','sad')
    or
    f = reportlab.lib.validators.OneOf(('happy','sad'))
    f('sad'),f('happy'), f('grumpy')
    (1,1,0)
    """

    def __init__(self, enum, *args) -> None: ...
    def test(self, x): ...

class SequenceOf(Validator):
    def __init__(self, elemTest, name=None, emptyOK: int = 1, NoneOK: int = 0, lo: int = 0, hi: int = 2147483647) -> None: ...
    def test(self, x): ...

class EitherOr(Validator):
    def __init__(self, tests, name=None) -> None: ...
    def test(self, x): ...

class NoneOr(EitherOr):
    def test(self, x): ...

class NotSetOr(EitherOr):
    def test(self, x): ...
    @staticmethod
    def conditionalValue(v, a): ...

class _isNotSet(Validator):
    def test(self, x): ...

class Auto(Validator):
    def __init__(self, **kw) -> None: ...
    def test(self, x): ...

class AutoOr(EitherOr):
    def test(self, x): ...

class isInstanceOf(Validator):
    def __init__(self, klass=None) -> None: ...
    def test(self, x): ...

class isSubclassOf(Validator):
    def __init__(self, klass=None) -> None: ...
    def test(self, x): ...

class matchesPattern(Validator):
    """Matches value, or its string representation, against regex"""

    def __init__(self, pattern) -> None: ...
    def test(self, x): ...

class DerivedValue:
    """This is used for magic values which work themselves out.
    An example would be an "inherit" property, so that one can have

      drawing.chart.categoryAxis.labels.fontName = inherit

    and pick up the value from the top of the drawing.
    Validators will permit this provided that a value can be pulled
    in which satisfies it.  And the renderer will have special
    knowledge of these so they can evaluate themselves.
    """

    def getValue(self, renderer, attr) -> None:
        """Override this.  The renderers will pass the renderer,
        and the attribute name.  Algorithms can then backtrack up
        through all the stuff the renderer provides, including
        a correct stack of parent nodes.
        """

class Inherit(DerivedValue):
    def getValue(self, renderer, attr): ...

inherit: Incomplete

class NumericAlign(str):
    """for creating the numeric string value for anchors etc etc
    dp is the character to align on (the last occurrence will be used)
    dpLen is the length of characters after the dp
    """

    def __new__(cls, dp: str = ".", dpLen: int = 0): ...

isAuto: Auto
isBoolean: _isBoolean
isString: _isString
isCodec: _isCodec
isNumber: _isNumber
isInt: _isInt
isNoneOrInt: NoneOr
isNumberOrNone: _isNumberOrNone
isTextAnchor: OneOf
isListOfNumbers: SequenceOf
isListOfNoneOrNumber: SequenceOf
isListOfListOfNoneOrNumber: SequenceOf
isListOfNumbersOrNone: _isListOfNumbersOrNone
isListOfShapes: _isListOfShapes
isListOfStrings: SequenceOf
isListOfStringsOrNone: _isListOfStringsOrNone
isTransform: _isTransform
isColor: _isColor
isListOfColors: SequenceOf
isColorOrNone: _isColorOrNone
isShape: _isValidChild
isValidChild: _isValidChild
isNoneOrShape: _isValidChildOrNone
isValidChildOrNone: _isValidChildOrNone
isAnything: _isAnything
isNothing: _isNothing
isXYCoord: SequenceOf
isBoxAnchor: OneOf
isNoneOrString: NoneOr
isNoneOrListOfNoneOrStrings: SequenceOf
isListOfNoneOrString: SequenceOf
isNoneOrListOfNoneOrNumbers: SequenceOf
isCallable: _isCallable
isNoneOrCallable: NoneOr
isStringOrCallable: EitherOr
isStringOrCallableOrNone: NoneOr
isStringOrNone: NoneOr
isNormalDate: _isNormalDate
isNotSet: _isNotSet
