from _typeshed import ConvertibleToInt, Incomplete, SupportsRichComparison
from collections.abc import Callable, Generator
from typing_extensions import Self

from pyasn1.type import base, constraint, namedtype, namedval
from pyasn1.type.tag import TagSet

__all__ = [
    "Integer",
    "Boolean",
    "BitString",
    "OctetString",
    "Null",
    "ObjectIdentifier",
    "Real",
    "Enumerated",
    "SequenceOfAndSetOfBase",
    "SequenceOf",
    "SetOf",
    "SequenceAndSetBase",
    "Sequence",
    "Set",
    "Choice",
    "Any",
    "NoValue",
    "noValue",
]

NoValue = base.NoValue
noValue: NoValue

class Integer(base.SimpleAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`int` objects.

    Keyword Args
    ------------
    value: :class:`int`, :class:`str` or |ASN.1| object
        Python :class:`int` or :class:`str` literal or |ASN.1| class
        instance. If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    namedValues: :py:class:`~pyasn1.type.namedval.NamedValues`
        Object representing non-default symbolic aliases for numbers

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------

    .. code-block:: python

        class ErrorCode(Integer):
            '''
            ASN.1 specification:

            ErrorCode ::=
                INTEGER { disk-full(1), no-disk(-1),
                          disk-not-formatted(2) }

            error ErrorCode ::= disk-full
            '''
            namedValues = NamedValues(
                ('disk-full', 1), ('no-disk', -1),
                ('disk-not-formatted', 2)
            )

        error = ErrorCode('disk-full')
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    namedValues: namedval.NamedValues
    typeId: int
    def __init__(self, value=..., **kwargs) -> None: ...
    def __and__(self, value): ...
    def __rand__(self, value): ...
    def __or__(self, value): ...
    def __ror__(self, value): ...
    def __xor__(self, value): ...
    def __rxor__(self, value): ...
    def __lshift__(self, value): ...
    def __rshift__(self, value): ...
    def __add__(self, value): ...
    def __radd__(self, value): ...
    def __sub__(self, value): ...
    def __rsub__(self, value): ...
    def __mul__(self, value): ...
    def __rmul__(self, value): ...
    def __mod__(self, value): ...
    def __rmod__(self, value): ...
    # Accepts everything builtins.pow does
    def __pow__(self, value: complex, modulo: int | None = None) -> Self: ...
    def __rpow__(self, value): ...
    def __floordiv__(self, value): ...
    def __rfloordiv__(self, value): ...
    def __truediv__(self, value): ...
    def __rtruediv__(self, value): ...
    def __divmod__(self, value): ...
    def __rdivmod__(self, value): ...
    __hash__ = base.SimpleAsn1Type.__hash__
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __abs__(self): ...
    def __index__(self) -> int: ...
    def __pos__(self): ...
    def __neg__(self): ...
    def __invert__(self): ...
    def __round__(self, n: int = 0): ...
    def __floor__(self): ...
    def __ceil__(self): ...
    def __trunc__(self): ...
    def __lt__(self, value): ...
    def __le__(self, value): ...
    def __eq__(self, value): ...
    def __ne__(self, value): ...
    def __gt__(self, value): ...
    def __ge__(self, value): ...
    def prettyIn(self, value): ...
    def prettyOut(self, value): ...
    def getNamedValues(self): ...

class Boolean(Integer):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`int` objects.

    Keyword Args
    ------------
    value: :class:`int`, :class:`str` or |ASN.1| object
        Python :class:`int` or :class:`str` literal or |ASN.1| class
        instance. If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s).Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    namedValues: :py:class:`~pyasn1.type.namedval.NamedValues`
        Object representing non-default symbolic aliases for numbers

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class RoundResult(Boolean):
            '''
            ASN.1 specification:

            RoundResult ::= BOOLEAN

            ok RoundResult ::= TRUE
            ko RoundResult ::= FALSE
            '''
        ok = RoundResult(True)
        ko = RoundResult(False)
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    namedValues: namedval.NamedValues
    typeId: int

class SizedInteger(int):
    bitLength: int | None
    leadingZeroBits: int | None
    def setBitLength(self, bitLength): ...
    def __len__(self) -> int: ...

class BitString(base.SimpleAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type both Python :class:`tuple` (as a tuple
    of bits) and :class:`int` objects.

    Keyword Args
    ------------
    value: :class:`int`, :class:`str` or |ASN.1| object
        Python :class:`int` or :class:`str` literal representing binary
        or hexadecimal number or sequence of integer bits or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    namedValues: :py:class:`~pyasn1.type.namedval.NamedValues`
        Object representing non-default symbolic aliases for numbers

    binValue: :py:class:`str`
        Binary string initializer to use instead of the *value*.
        Example: '10110011'.

    hexValue: :py:class:`str`
        Hexadecimal string initializer to use instead of the *value*.
        Example: 'DEADBEEF'.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class Rights(BitString):
            '''
            ASN.1 specification:

            Rights ::= BIT STRING { user-read(0), user-write(1),
                                    group-read(2), group-write(3),
                                    other-read(4), other-write(5) }

            group1 Rights ::= { group-read, group-write }
            group2 Rights ::= '0011'B
            group3 Rights ::= '3'H
            '''
            namedValues = NamedValues(
                ('user-read', 0), ('user-write', 1),
                ('group-read', 2), ('group-write', 3),
                ('other-read', 4), ('other-write', 5)
            )

        group1 = Rights(('group-read', 'group-write'))
        group2 = Rights('0011')
        group3 = Rights(0x3)
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    namedValues: namedval.NamedValues
    typeId: int
    defaultBinValue: str | base.NoValue
    defaultHexValue: str | base.NoValue
    def __init__(self, value=..., **kwargs) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __len__(self) -> int: ...
    def __getitem__(self, i): ...
    def __iter__(self): ...
    def __reversed__(self): ...
    def __add__(self, value): ...
    def __radd__(self, value): ...
    def __mul__(self, value): ...
    def __rmul__(self, value): ...
    def __lshift__(self, count): ...
    def __rshift__(self, count): ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def asNumbers(self):
        """Get |ASN.1| value as a sequence of 8-bit integers.

        If |ASN.1| object length is not a multiple of 8, result
        will be left-padded with zeros.
        """

    def asOctets(self):
        """Get |ASN.1| value as a sequence of octets.

        If |ASN.1| object length is not a multiple of 8, result
        will be left-padded with zeros.
        """

    def asInteger(self):
        """Get |ASN.1| value as a single integer value."""

    def asBinary(self):
        """Get |ASN.1| value as a text string of bits."""

    @classmethod
    def fromHexString(cls, value, internalFormat: bool = False, prepend: ConvertibleToInt | None = None):
        """Create a |ASN.1| object initialized from the hex string.

        Parameters
        ----------
        value: :class:`str`
            Text string like 'DEADBEEF'
        """

    @classmethod
    def fromBinaryString(cls, value, internalFormat: bool = False, prepend: ConvertibleToInt | None = None):
        """Create a |ASN.1| object initialized from a string of '0' and '1'.

        Parameters
        ----------
        value: :class:`str`
            Text string like '1010111'
        """

    @classmethod
    def fromOctetString(cls, value, internalFormat: bool = False, prepend: ConvertibleToInt | None = None, padding: int = 0):
        """Create a |ASN.1| object initialized from a string.

        Parameters
        ----------
        value: :class:`bytes`
            Text string like b'\\\\x01\\\\xff'
        """

    def prettyIn(self, value): ...

class OctetString(base.SimpleAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type :class:`bytes`.
    When used in Unicode context, |ASN.1| type
    assumes "|encoding|" serialisation.

    Keyword Args
    ------------
    value: :class:`unicode`, :class:`str`, :class:`bytes` or |ASN.1| object
        :class:`bytes`, alternatively :class:`str`
        representing character string to be serialised into octets
        (note `encoding` parameter) or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    encoding: :py:class:`str`
        Unicode codec ID to encode/decode
        :class:`str` the payload when |ASN.1| object is used
        in text string context.

    binValue: :py:class:`str`
        Binary string initializer to use instead of the *value*.
        Example: '10110011'.

    hexValue: :py:class:`str`
        Hexadecimal string initializer to use instead of the *value*.
        Example: 'DEADBEEF'.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class Icon(OctetString):
            '''
            ASN.1 specification:

            Icon ::= OCTET STRING

            icon1 Icon ::= '001100010011001000110011'B
            icon2 Icon ::= '313233'H
            '''
        icon1 = Icon.fromBinaryString('001100010011001000110011')
        icon2 = Icon.fromHexString('313233')
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    defaultBinValue: str | base.NoValue
    defaultHexValue: str | base.NoValue
    encoding: str
    def __init__(self, value=..., **kwargs) -> None: ...
    def prettyIn(self, value): ...
    def __bytes__(self) -> bytes: ...
    def asOctets(self): ...
    def asNumbers(self): ...
    def prettyOut(self, value): ...
    def prettyPrint(self, scope: int = 0): ...
    @staticmethod
    def fromBinaryString(value):
        """Create a |ASN.1| object initialized from a string of '0' and '1'.

        Parameters
        ----------
        value: :class:`str`
            Text string like '1010111'
        """

    @staticmethod
    def fromHexString(value):
        """Create a |ASN.1| object initialized from the hex string.

        Parameters
        ----------
        value: :class:`str`
            Text string like 'DEADBEEF'
        """

    def __len__(self) -> int: ...
    def __getitem__(self, i): ...
    def __iter__(self): ...
    def __contains__(self, value) -> bool: ...
    def __add__(self, value): ...
    def __radd__(self, value): ...
    def __mul__(self, value): ...
    def __rmul__(self, value): ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __reversed__(self): ...

class Null(OctetString):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`str` objects
    (always empty).

    Keyword Args
    ------------
    value: :class:`str` or |ASN.1| object
        Python empty :class:`str` literal or any object that evaluates to :obj:`False`
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class Ack(Null):
            '''
            ASN.1 specification:

            Ack ::= NULL
            '''
        ack = Ack('')
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    def prettyIn(self, value): ...

class ObjectIdentifier(base.SimpleAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`tuple` objects
    (tuple of non-negative integers).

    Keyword Args
    ------------
    value: :class:`tuple`, :class:`str` or |ASN.1| object
        Python sequence of :class:`int` or :class:`str` literal or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class ID(ObjectIdentifier):
            '''
            ASN.1 specification:

            ID ::= OBJECT IDENTIFIER

            id-edims ID ::= { joint-iso-itu-t mhs-motif(6) edims(7) }
            id-bp ID ::= { id-edims 11 }
            '''
        id_edims = ID('2.6.7')
        id_bp = id_edims + (11,)
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    def __add__(self, other): ...
    def __radd__(self, other): ...
    def asTuple(self): ...
    def __len__(self) -> int: ...
    def __getitem__(self, i): ...
    def __iter__(self): ...
    def __contains__(self, value) -> bool: ...
    def index(self, suboid): ...
    def isPrefixOf(self, other):
        """Indicate if this |ASN.1| object is a prefix of other |ASN.1| object.

        Parameters
        ----------
        other: |ASN.1| object
            |ASN.1| object

        Returns
        -------
        : :class:`bool`
            :obj:`True` if this |ASN.1| object is a parent (e.g. prefix) of the other |ASN.1| object
            or :obj:`False` otherwise.
        """

    def prettyIn(self, value): ...
    def prettyOut(self, value): ...

class Real(base.SimpleAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`float` objects.
    Additionally, |ASN.1| objects behave like a :class:`tuple` in which case its
    elements are mantissa, base and exponent.

    Keyword Args
    ------------
    value: :class:`tuple`, :class:`float` or |ASN.1| object
        Python sequence of :class:`int` (representing mantissa, base and
        exponent) or :class:`float` instance or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class Pi(Real):
            '''
            ASN.1 specification:

            Pi ::= REAL

            pi Pi ::= { mantissa 314159, base 10, exponent -5 }

            '''
        pi = Pi((314159, 10, -5))
    """

    binEncBase: int | None
    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    def prettyIn(self, value): ...
    def prettyPrint(self, scope: int = 0): ...
    @property
    def isPlusInf(self):
        """Indicate PLUS-INFINITY object value

        Returns
        -------
        : :class:`bool`
            :obj:`True` if calling object represents plus infinity
            or :obj:`False` otherwise.

        """

    @property
    def isMinusInf(self):
        """Indicate MINUS-INFINITY object value

        Returns
        -------
        : :class:`bool`
            :obj:`True` if calling object represents minus infinity
            or :obj:`False` otherwise.
        """

    @property
    def isInf(self): ...
    def __add__(self, value): ...
    def __radd__(self, value): ...
    def __mul__(self, value): ...
    def __rmul__(self, value): ...
    def __sub__(self, value): ...
    def __rsub__(self, value): ...
    def __mod__(self, value): ...
    def __rmod__(self, value): ...
    # Accepts everything builtins.pow with a float base does
    def __pow__(self, value: complex, modulo: int | None = None) -> Self: ...
    def __rpow__(self, value): ...
    def __truediv__(self, value): ...
    def __rtruediv__(self, value): ...
    def __divmod__(self, value): ...
    def __rdivmod__(self, value): ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __abs__(self): ...
    def __pos__(self): ...
    def __neg__(self): ...
    def __round__(self, n: int = 0): ...
    def __floor__(self): ...
    def __ceil__(self): ...
    def __trunc__(self): ...
    def __lt__(self, value): ...
    def __le__(self, value): ...
    def __eq__(self, value): ...
    def __ne__(self, value): ...
    def __gt__(self, value): ...
    def __ge__(self, value): ...
    def __bool__(self) -> bool: ...
    __hash__ = base.SimpleAsn1Type.__hash__
    def __getitem__(self, idx): ...
    def isPlusInfinity(self): ...
    def isMinusInfinity(self): ...
    def isInfinity(self): ...

class Enumerated(Integer):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`, its
    objects are immutable and duck-type Python :class:`int` objects.

    Keyword Args
    ------------
    value: :class:`int`, :class:`str` or |ASN.1| object
        Python :class:`int` or :class:`str` literal or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    namedValues: :py:class:`~pyasn1.type.namedval.NamedValues`
        Object representing non-default symbolic aliases for numbers

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------

    .. code-block:: python

        class RadioButton(Enumerated):
            '''
            ASN.1 specification:

            RadioButton ::= ENUMERATED { button1(0), button2(1),
                                         button3(2) }

            selected-by-default RadioButton ::= button1
            '''
            namedValues = NamedValues(
                ('button1', 0), ('button2', 1),
                ('button3', 2)
            )

        selected_by_default = RadioButton('button1')
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    namedValues: namedval.NamedValues

class SequenceOfAndSetOfBase(base.ConstructedAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`list` objects.

    Keyword Args
    ------------
    componentType : :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
        A pyasn1 object representing ASN.1 type allowed within |ASN.1| type

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class LotteryDraw(SequenceOf):  #  SetOf is similar
            '''
            ASN.1 specification:

            LotteryDraw ::= SEQUENCE OF INTEGER
            '''
            componentType = Integer()

        lotteryDraw = LotteryDraw()
        lotteryDraw.extend([123, 456, 789])
    """

    componentType: namedtype.NamedTypes | None
    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    def __init__(
        self,
        *args,
        componentType: namedtype.NamedTypes | None = ...,
        tagSet: TagSet = ...,
        subtypeSpec: constraint.ConstraintsIntersection = ...,
    ) -> None: ...
    def __getitem__(self, idx): ...
    def __setitem__(self, idx, value) -> None: ...
    def append(self, value) -> None: ...
    def count(self, value): ...
    def extend(self, values) -> None: ...
    def index(self, value, start: int = 0, stop: int | None = None): ...
    def reverse(self) -> None: ...
    def sort(self, key: Callable[[Incomplete], SupportsRichComparison] | None = None, reverse: bool = False) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def getComponentByPosition(self, idx, default=..., instantiate: bool = True):
        """Return |ASN.1| type component value by position.

        Equivalent to Python sequence subscription operation (e.g. `[]`).

        Parameters
        ----------
        idx : :class:`int`
            Component index (zero-based). Must either refer to an existing
            component or to N+1 component (if *componentType* is set). In the latter
            case a new component type gets instantiated and appended to the |ASN.1|
            sequence.

        Keyword Args
        ------------
        default: :class:`object`
            If set and requested component is a schema object, return the `default`
            object instead of the requested component.

        instantiate: :class:`bool`
            If :obj:`True` (default), inner component will be automatically instantiated.
            If :obj:`False` either existing component or the :class:`NoValue` object will be
            returned.

        Returns
        -------
        : :py:class:`~pyasn1.type.base.PyAsn1Item`
            Instantiate |ASN.1| component type or return existing component value

        Examples
        --------

        .. code-block:: python

            # can also be SetOf
            class MySequenceOf(SequenceOf):
                componentType = OctetString()

            s = MySequenceOf()

            # returns component #0 with `.isValue` property False
            s.getComponentByPosition(0)

            # returns None
            s.getComponentByPosition(0, default=None)

            s.clear()

            # returns noValue
            s.getComponentByPosition(0, instantiate=False)

            # sets component #0 to OctetString() ASN.1 schema
            # object and returns it
            s.getComponentByPosition(0, instantiate=True)

            # sets component #0 to ASN.1 value object
            s.setComponentByPosition(0, 'ABCD')

            # returns OctetString('ABCD') value object
            s.getComponentByPosition(0, instantiate=False)

            s.clear()

            # returns noValue
            s.getComponentByPosition(0, instantiate=False)
        """

    def setComponentByPosition(
        self, idx, value=..., verifyConstraints: bool = True, matchTags: bool = True, matchConstraints: bool = True
    ):
        """Assign |ASN.1| type component by position.

        Equivalent to Python sequence item assignment operation (e.g. `[]`)
        or list.append() (when idx == len(self)).

        Parameters
        ----------
        idx: :class:`int`
            Component index (zero-based). Must either refer to existing
            component or to N+1 component. In the latter case a new component
            type gets instantiated (if *componentType* is set, or given ASN.1
            object is taken otherwise) and appended to the |ASN.1| sequence.

        Keyword Args
        ------------
        value: :class:`object` or :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
            A Python value to initialize |ASN.1| component with (if *componentType* is set)
            or ASN.1 value object to assign to |ASN.1| component.
            If `value` is not given, schema object will be set as a component.

        verifyConstraints: :class:`bool`
             If :obj:`False`, skip constraints validation

        matchTags: :class:`bool`
             If :obj:`False`, skip component tags matching

        matchConstraints: :class:`bool`
             If :obj:`False`, skip component constraints matching

        Returns
        -------
        self

        Raises
        ------
        ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
            On constraint violation or bad initializer
        IndexError
            When idx > len(self)
        """

    @property
    def componentTagMap(self): ...
    @property
    def components(self): ...
    def clear(self):
        """Remove all components and become an empty |ASN.1| value object.

        Has the same effect on |ASN.1| object as it does on :class:`list`
        built-in.
        """

    def reset(self):
        """Remove all components and become a |ASN.1| schema object.

        See :meth:`isValue` property for more information on the
        distinction between value and schema objects.
        """

    def prettyPrint(self, scope: int = 0): ...
    def prettyPrintType(self, scope: int = 0): ...
    @property
    def isValue(self):
        """Indicate that |ASN.1| object represents ASN.1 value.

        If *isValue* is :obj:`False` then this object represents just ASN.1 schema.

        If *isValue* is :obj:`True` then, in addition to its ASN.1 schema features,
        this object can also be used like a Python built-in object
        (e.g. :class:`int`, :class:`str`, :class:`dict` etc.).

        Returns
        -------
        : :class:`bool`
            :obj:`False` if object represents just ASN.1 schema.
            :obj:`True` if object represents ASN.1 schema and can be used as a normal value.

        Note
        ----
        There is an important distinction between PyASN1 schema and value objects.
        The PyASN1 schema objects can only participate in ASN.1 schema-related
        operations (e.g. defining or testing the structure of the data). Most
        obvious uses of ASN.1 schema is to guide serialisation codecs whilst
        encoding/decoding serialised ASN.1 contents.

        The PyASN1 value objects can **additionally** participate in many operations
        involving regular Python objects (e.g. arithmetic, comprehension etc).
        """

    @property
    def isInconsistent(self):
        """Run necessary checks to ensure |ASN.1| object consistency.

        Default action is to verify |ASN.1| object against constraints imposed
        by `subtypeSpec`.

        Raises
        ------
        :py:class:`~pyasn1.error.PyAsn1tError` on any inconsistencies found
        """

class SequenceOf(SequenceOfAndSetOfBase):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`list` objects.

    Keyword Args
    ------------
    componentType : :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
        A pyasn1 object representing ASN.1 type allowed within |ASN.1| type

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class LotteryDraw(SequenceOf):  #  SetOf is similar
            '''
            ASN.1 specification:

            LotteryDraw ::= SEQUENCE OF INTEGER
            '''
            componentType = Integer()

        lotteryDraw = LotteryDraw()
        lotteryDraw.extend([123, 456, 789])
    """

    typeId: int

class SetOf(SequenceOfAndSetOfBase):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`list` objects.

    Keyword Args
    ------------
    componentType : :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
        A pyasn1 object representing ASN.1 type allowed within |ASN.1| type

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class LotteryDraw(SequenceOf):  #  SetOf is similar
            '''
            ASN.1 specification:

            LotteryDraw ::= SEQUENCE OF INTEGER
            '''
            componentType = Integer()

        lotteryDraw = LotteryDraw()
        lotteryDraw.extend([123, 456, 789])
    """

    typeId: int

class SequenceAndSetBase(base.ConstructedAsn1Type):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`dict` objects.

    Keyword Args
    ------------
    componentType: :py:class:`~pyasn1.type.namedtype.NamedType`
        Object holding named ASN.1 types allowed within this collection

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s).  Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class Description(Sequence):  #  Set is similar
            '''
            ASN.1 specification:

            Description ::= SEQUENCE {
                surname    IA5String,
                first-name IA5String OPTIONAL,
                age        INTEGER DEFAULT 40
            }
            '''
            componentType = NamedTypes(
                NamedType('surname', IA5String()),
                OptionalNamedType('first-name', IA5String()),
                DefaultedNamedType('age', Integer(40))
            )

        descr = Description()
        descr['surname'] = 'Smith'
        descr['first-name'] = 'John'
    """

    componentType: namedtype.NamedTypes

    class DynamicNames:
        """Fields names/positions mapping for component-less objects"""

        def __init__(self) -> None: ...
        def __len__(self) -> int: ...
        def __contains__(self, item) -> bool: ...
        def __iter__(self): ...
        def __getitem__(self, item): ...
        def getNameByPosition(self, idx): ...
        def getPositionByName(self, name): ...
        def addField(self, idx) -> None: ...

    def __init__(self, **kwargs) -> None: ...
    def __getitem__(self, idx): ...
    def __setitem__(self, idx, value) -> None: ...
    def __contains__(self, key) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def values(self) -> Generator[Incomplete, None, None]: ...
    def keys(self): ...
    def items(self) -> Generator[Incomplete, None, None]: ...
    def update(self, *iterValue, **mappingValue) -> None: ...
    def clear(self):
        """Remove all components and become an empty |ASN.1| value object.

        Has the same effect on |ASN.1| object as it does on :class:`dict`
        built-in.
        """

    def reset(self):
        """Remove all components and become a |ASN.1| schema object.

        See :meth:`isValue` property for more information on the
        distinction between value and schema objects.
        """

    @property
    def components(self): ...
    def getComponentByName(self, name, default=..., instantiate: bool = True):
        """Returns |ASN.1| type component by name.

        Equivalent to Python :class:`dict` subscription operation (e.g. `[]`).

        Parameters
        ----------
        name: :class:`str`
            |ASN.1| type component name

        Keyword Args
        ------------
        default: :class:`object`
            If set and requested component is a schema object, return the `default`
            object instead of the requested component.

        instantiate: :class:`bool`
            If :obj:`True` (default), inner component will be automatically
            instantiated.
            If :obj:`False` either existing component or the :class:`NoValue`
            object will be returned.

        Returns
        -------
        : :py:class:`~pyasn1.type.base.PyAsn1Item`
            Instantiate |ASN.1| component type or return existing
            component value
        """

    def setComponentByName(
        self, name, value=..., verifyConstraints: bool = True, matchTags: bool = True, matchConstraints: bool = True
    ):
        """Assign |ASN.1| type component by name.

        Equivalent to Python :class:`dict` item assignment operation (e.g. `[]`).

        Parameters
        ----------
        name: :class:`str`
            |ASN.1| type component name

        Keyword Args
        ------------
        value: :class:`object` or :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
            A Python value to initialize |ASN.1| component with (if *componentType* is set)
            or ASN.1 value object to assign to |ASN.1| component.
            If `value` is not given, schema object will be set as a component.

        verifyConstraints: :class:`bool`
             If :obj:`False`, skip constraints validation

        matchTags: :class:`bool`
             If :obj:`False`, skip component tags matching

        matchConstraints: :class:`bool`
             If :obj:`False`, skip component constraints matching

        Returns
        -------
        self
        """

    def getComponentByPosition(self, idx, default=..., instantiate: bool = True):
        """Returns |ASN.1| type component by index.

        Equivalent to Python sequence subscription operation (e.g. `[]`).

        Parameters
        ----------
        idx: :class:`int`
            Component index (zero-based). Must either refer to an existing
            component or (if *componentType* is set) new ASN.1 schema object gets
            instantiated.

        Keyword Args
        ------------
        default: :class:`object`
            If set and requested component is a schema object, return the `default`
            object instead of the requested component.

        instantiate: :class:`bool`
            If :obj:`True` (default), inner component will be automatically
            instantiated.
            If :obj:`False` either existing component or the :class:`NoValue`
            object will be returned.

        Returns
        -------
        : :py:class:`~pyasn1.type.base.PyAsn1Item`
            a PyASN1 object

        Examples
        --------

        .. code-block:: python

            # can also be Set
            class MySequence(Sequence):
                componentType = NamedTypes(
                    NamedType('id', OctetString())
                )

            s = MySequence()

            # returns component #0 with `.isValue` property False
            s.getComponentByPosition(0)

            # returns None
            s.getComponentByPosition(0, default=None)

            s.clear()

            # returns noValue
            s.getComponentByPosition(0, instantiate=False)

            # sets component #0 to OctetString() ASN.1 schema
            # object and returns it
            s.getComponentByPosition(0, instantiate=True)

            # sets component #0 to ASN.1 value object
            s.setComponentByPosition(0, 'ABCD')

            # returns OctetString('ABCD') value object
            s.getComponentByPosition(0, instantiate=False)

            s.clear()

            # returns noValue
            s.getComponentByPosition(0, instantiate=False)
        """

    def setComponentByPosition(
        self, idx, value=..., verifyConstraints: bool = True, matchTags: bool = True, matchConstraints: bool = True
    ):
        """Assign |ASN.1| type component by position.

        Equivalent to Python sequence item assignment operation (e.g. `[]`).

        Parameters
        ----------
        idx : :class:`int`
            Component index (zero-based). Must either refer to existing
            component (if *componentType* is set) or to N+1 component
            otherwise. In the latter case a new component of given ASN.1
            type gets instantiated and appended to |ASN.1| sequence.

        Keyword Args
        ------------
        value: :class:`object` or :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
            A Python value to initialize |ASN.1| component with (if *componentType* is set)
            or ASN.1 value object to assign to |ASN.1| component.
            If `value` is not given, schema object will be set as a component.

        verifyConstraints : :class:`bool`
             If :obj:`False`, skip constraints validation

        matchTags: :class:`bool`
             If :obj:`False`, skip component tags matching

        matchConstraints: :class:`bool`
             If :obj:`False`, skip component constraints matching

        Returns
        -------
        self
        """

    @property
    def isValue(self):
        """Indicate that |ASN.1| object represents ASN.1 value.

        If *isValue* is :obj:`False` then this object represents just ASN.1 schema.

        If *isValue* is :obj:`True` then, in addition to its ASN.1 schema features,
        this object can also be used like a Python built-in object (e.g.
        :class:`int`, :class:`str`, :class:`dict` etc.).

        Returns
        -------
        : :class:`bool`
            :obj:`False` if object represents just ASN.1 schema.
            :obj:`True` if object represents ASN.1 schema and can be used as a
            normal value.

        Note
        ----
        There is an important distinction between PyASN1 schema and value objects.
        The PyASN1 schema objects can only participate in ASN.1 schema-related
        operations (e.g. defining or testing the structure of the data). Most
        obvious uses of ASN.1 schema is to guide serialisation codecs whilst
        encoding/decoding serialised ASN.1 contents.

        The PyASN1 value objects can **additionally** participate in many operations
        involving regular Python objects (e.g. arithmetic, comprehension etc).

        It is sufficient for |ASN.1| objects to have all non-optional and non-defaulted
        components being value objects to be considered as a value objects as a whole.
        In other words, even having one or more optional components not turned into
        value objects, |ASN.1| object is still considered as a value object. Defaulted
        components are normally value objects by default.
        """

    @property
    def isInconsistent(self):
        """Run necessary checks to ensure |ASN.1| object consistency.

        Default action is to verify |ASN.1| object against constraints imposed
        by `subtypeSpec`.

        Raises
        ------
        :py:class:`~pyasn1.error.PyAsn1tError` on any inconsistencies found
        """

    def prettyPrint(self, scope: int = 0):
        """Return an object representation string.

        Returns
        -------
        : :class:`str`
            Human-friendly object representation.
        """

    def prettyPrintType(self, scope: int = 0): ...
    def setDefaultComponents(self): ...
    def getComponentType(self): ...
    def getNameByPosition(self, idx): ...

class Sequence(SequenceAndSetBase):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`dict` objects.

    Keyword Args
    ------------
    componentType: :py:class:`~pyasn1.type.namedtype.NamedType`
        Object holding named ASN.1 types allowed within this collection

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s).  Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class Description(Sequence):  #  Set is similar
            '''
            ASN.1 specification:

            Description ::= SEQUENCE {
                surname    IA5String,
                first-name IA5String OPTIONAL,
                age        INTEGER DEFAULT 40
            }
            '''
            componentType = NamedTypes(
                NamedType('surname', IA5String()),
                OptionalNamedType('first-name', IA5String()),
                DefaultedNamedType('age', Integer(40))
            )

        descr = Description()
        descr['surname'] = 'Smith'
        descr['first-name'] = 'John'
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    componentType: namedtype.NamedTypes
    typeId: int
    def getComponentTagMapNearPosition(self, idx): ...
    def getComponentPositionNearType(self, tagSet, idx): ...

class Set(SequenceAndSetBase):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`dict` objects.

    Keyword Args
    ------------
    componentType: :py:class:`~pyasn1.type.namedtype.NamedType`
        Object holding named ASN.1 types allowed within this collection

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s).  Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class Description(Sequence):  #  Set is similar
            '''
            ASN.1 specification:

            Description ::= SEQUENCE {
                surname    IA5String,
                first-name IA5String OPTIONAL,
                age        INTEGER DEFAULT 40
            }
            '''
            componentType = NamedTypes(
                NamedType('surname', IA5String()),
                OptionalNamedType('first-name', IA5String()),
                DefaultedNamedType('age', Integer(40))
            )

        descr = Description()
        descr['surname'] = 'Smith'
        descr['first-name'] = 'John'
    """

    tagSet: TagSet
    componentType: namedtype.NamedTypes
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    def getComponent(self, innerFlag: bool = False): ...
    def getComponentByType(self, tagSet, default=..., instantiate: bool = True, innerFlag: bool = False):
        """Returns |ASN.1| type component by ASN.1 tag.

        Parameters
        ----------
        tagSet : :py:class:`~pyasn1.type.tag.TagSet`
            Object representing ASN.1 tags to identify one of
            |ASN.1| object component

        Keyword Args
        ------------
        default: :class:`object`
            If set and requested component is a schema object, return the `default`
            object instead of the requested component.

        instantiate: :class:`bool`
            If :obj:`True` (default), inner component will be automatically
            instantiated.
            If :obj:`False` either existing component or the :class:`noValue`
            object will be returned.

        Returns
        -------
        : :py:class:`~pyasn1.type.base.PyAsn1Item`
            a pyasn1 object
        """

    def setComponentByType(
        self,
        tagSet,
        value=...,
        verifyConstraints: bool = True,
        matchTags: bool = True,
        matchConstraints: bool = True,
        innerFlag: bool = False,
    ):
        """Assign |ASN.1| type component by ASN.1 tag.

        Parameters
        ----------
        tagSet : :py:class:`~pyasn1.type.tag.TagSet`
            Object representing ASN.1 tags to identify one of
            |ASN.1| object component

        Keyword Args
        ------------
        value: :class:`object` or :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
            A Python value to initialize |ASN.1| component with (if *componentType* is set)
            or ASN.1 value object to assign to |ASN.1| component.
            If `value` is not given, schema object will be set as a component.

        verifyConstraints : :class:`bool`
            If :obj:`False`, skip constraints validation

        matchTags: :class:`bool`
            If :obj:`False`, skip component tags matching

        matchConstraints: :class:`bool`
            If :obj:`False`, skip component constraints matching

        innerFlag: :class:`bool`
            If :obj:`True`, search for matching *tagSet* recursively.

        Returns
        -------
        self
        """

    @property
    def componentTagMap(self): ...

class Choice(Set):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.ConstructedAsn1Type`,
    its objects are mutable and duck-type Python :class:`list` objects.

    Keyword Args
    ------------
    componentType: :py:class:`~pyasn1.type.namedtype.NamedType`
        Object holding named ASN.1 types allowed within this collection

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s).  Constraints
        verification for |ASN.1| type can only occur on explicit
        `.isInconsistent` call.

    Examples
    --------

    .. code-block:: python

        class Afters(Choice):
            '''
            ASN.1 specification:

            Afters ::= CHOICE {
                cheese  [0] IA5String,
                dessert [1] IA5String
            }
            '''
            componentType = NamedTypes(
                NamedType('cheese', IA5String().subtype(
                    implicitTag=Tag(tagClassContext, tagFormatSimple, 0)
                ),
                NamedType('dessert', IA5String().subtype(
                    implicitTag=Tag(tagClassContext, tagFormatSimple, 1)
                )
            )

        afters = Afters()
        afters['cheese'] = 'Mascarpone'
    """

    tagSet: TagSet
    componentType: namedtype.NamedTypes
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> bool: ...
    def __iter__(self): ...
    def values(self) -> Generator[Incomplete, None, None]: ...
    def keys(self) -> Generator[Incomplete, None, None]: ...
    def items(self) -> Generator[Incomplete, None, None]: ...
    def checkConsistency(self) -> None: ...
    def getComponentByPosition(self, idx, default=..., instantiate: bool = True): ...
    def setComponentByPosition(
        self, idx, value=..., verifyConstraints: bool = True, matchTags: bool = True, matchConstraints: bool = True
    ):
        """Assign |ASN.1| type component by position.

        Equivalent to Python sequence item assignment operation (e.g. `[]`).

        Parameters
        ----------
        idx: :class:`int`
            Component index (zero-based). Must either refer to existing
            component or to N+1 component. In the latter case a new component
            type gets instantiated (if *componentType* is set, or given ASN.1
            object is taken otherwise) and appended to the |ASN.1| sequence.

        Keyword Args
        ------------
        value: :class:`object` or :py:class:`~pyasn1.type.base.PyAsn1Item` derivative
            A Python value to initialize |ASN.1| component with (if *componentType* is set)
            or ASN.1 value object to assign to |ASN.1| component. Once a new value is
            set to *idx* component, previous value is dropped.
            If `value` is not given, schema object will be set as a component.

        verifyConstraints : :class:`bool`
            If :obj:`False`, skip constraints validation

        matchTags: :class:`bool`
            If :obj:`False`, skip component tags matching

        matchConstraints: :class:`bool`
            If :obj:`False`, skip component constraints matching

        Returns
        -------
        self
        """

    @property
    def effectiveTagSet(self):
        """Return a :class:`~pyasn1.type.tag.TagSet` object of the currently initialized component or self (if |ASN.1| is tagged)."""

    @property
    def tagMap(self):
        """ "Return a :class:`~pyasn1.type.tagmap.TagMap` object mapping
        ASN.1 tags to ASN.1 objects contained within callee.
        """

    def getComponent(self, innerFlag: bool = False):
        """Return currently assigned component of the |ASN.1| object.

        Returns
        -------
        : :py:class:`~pyasn1.type.base.PyAsn1Item`
            a PyASN1 object
        """

    def getName(self, innerFlag: bool = False):
        """Return the name of currently assigned component of the |ASN.1| object.

        Returns
        -------
        : :py:class:`str`
            |ASN.1| component name
        """

    @property
    def isValue(self):
        """Indicate that |ASN.1| object represents ASN.1 value.

        If *isValue* is :obj:`False` then this object represents just ASN.1 schema.

        If *isValue* is :obj:`True` then, in addition to its ASN.1 schema features,
        this object can also be used like a Python built-in object (e.g.
        :class:`int`, :class:`str`, :class:`dict` etc.).

        Returns
        -------
        : :class:`bool`
            :obj:`False` if object represents just ASN.1 schema.
            :obj:`True` if object represents ASN.1 schema and can be used as a normal
            value.

        Note
        ----
        There is an important distinction between PyASN1 schema and value objects.
        The PyASN1 schema objects can only participate in ASN.1 schema-related
        operations (e.g. defining or testing the structure of the data). Most
        obvious uses of ASN.1 schema is to guide serialisation codecs whilst
        encoding/decoding serialised ASN.1 contents.

        The PyASN1 value objects can **additionally** participate in many operations
        involving regular Python objects (e.g. arithmetic, comprehension etc).
        """

    def clear(self): ...
    def getMinTagSet(self): ...

class Any(OctetString):
    """Create |ASN.1| schema or value object.

    |ASN.1| class is based on :class:`~pyasn1.type.base.SimpleAsn1Type`,
    its objects are immutable and duck-type :class:`bytes`.
    When used in Unicode context, |ASN.1| type assumes
    "|encoding|" serialisation.

    Keyword Args
    ------------
    value: :class:`unicode`, :class:`str`, :class:`bytes` or |ASN.1| object
        :class:`bytes`, alternatively :class:`str`
        representing character string to be serialised into octets (note
        `encoding` parameter) or |ASN.1| object.
        If `value` is not given, schema object will be created.

    tagSet: :py:class:`~pyasn1.type.tag.TagSet`
        Object representing non-default ASN.1 tag(s)

    subtypeSpec: :py:class:`~pyasn1.type.constraint.ConstraintsIntersection`
        Object representing non-default ASN.1 subtype constraint(s). Constraints
        verification for |ASN.1| type occurs automatically on object
        instantiation.

    encoding: :py:class:`str`
        Unicode codec ID to encode/decode
        :class:`str` the payload when |ASN.1| object is used
        in text string context.

    binValue: :py:class:`str`
        Binary string initializer to use instead of the *value*.
        Example: '10110011'.

    hexValue: :py:class:`str`
        Hexadecimal string initializer to use instead of the *value*.
        Example: 'DEADBEEF'.

    Raises
    ------
    ~pyasn1.error.ValueConstraintError, ~pyasn1.error.PyAsn1Error
        On constraint violation or bad initializer.

    Examples
    --------
    .. code-block:: python

        class Error(Sequence):
            '''
            ASN.1 specification:

            Error ::= SEQUENCE {
                code      INTEGER,
                parameter ANY DEFINED BY code  -- Either INTEGER or REAL
            }
            '''
            componentType=NamedTypes(
                NamedType('code', Integer()),
                NamedType('parameter', Any(),
                          openType=OpenType('code', {1: Integer(),
                                                     2: Real()}))
            )

        error = Error()
        error['code'] = 1
        error['parameter'] = Integer(1234)
    """

    tagSet: TagSet
    subtypeSpec: constraint.ConstraintsIntersection
    typeId: int
    @property
    def tagMap(self):
        """ "Return a :class:`~pyasn1.type.tagmap.TagMap` object mapping
        ASN.1 tags to ASN.1 objects contained within callee.
        """
