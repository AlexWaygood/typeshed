__all__ = [
    "SingleValueConstraint",
    "ContainedSubtypeConstraint",
    "ValueRangeConstraint",
    "ValueSizeConstraint",
    "PermittedAlphabetConstraint",
    "InnerTypeConstraint",
    "ConstraintsExclusion",
    "ConstraintsIntersection",
    "ConstraintsUnion",
]

class AbstractConstraint:
    def __init__(self, *values) -> None: ...
    def __call__(self, value, idx: int | None = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __bool__(self) -> bool: ...
    def __hash__(self): ...
    def getValueMap(self): ...
    def isSuperTypeOf(self, otherConstraint): ...
    def isSubTypeOf(self, otherConstraint): ...

class SingleValueConstraint(AbstractConstraint):
    """Create a SingleValueConstraint object.

    The SingleValueConstraint satisfies any value that
    is present in the set of permitted values.

    Objects of this type are iterable (emitting constraint values) and
    can act as operands for some arithmetic operations e.g. addition
    and subtraction. The latter can be used for combining multiple
    SingleValueConstraint objects into one.

    The SingleValueConstraint object can be applied to
    any ASN.1 type.

    Parameters
    ----------
    *values: :class:`int`
        Full set of values permitted by this constraint object.

    Examples
    --------
    .. code-block:: python

        class DivisorOfSix(Integer):
            '''
            ASN.1 specification:

            Divisor-Of-6 ::= INTEGER (1 | 2 | 3 | 6)
            '''
            subtypeSpec = SingleValueConstraint(1, 2, 3, 6)

        # this will succeed
        divisor_of_six = DivisorOfSix(1)

        # this will raise ValueConstraintError
        divisor_of_six = DivisorOfSix(7)
    """

    def __contains__(self, item) -> bool: ...
    def __iter__(self): ...
    def __add__(self, constraint): ...
    def __sub__(self, constraint): ...

class ContainedSubtypeConstraint(AbstractConstraint):
    """Create a ContainedSubtypeConstraint object.

    The ContainedSubtypeConstraint satisfies any value that
    is present in the set of permitted values and also
    satisfies included constraints.

    The ContainedSubtypeConstraint object can be applied to
    any ASN.1 type.

    Parameters
    ----------
    *values:
        Full set of values and constraint objects permitted
        by this constraint object.

    Examples
    --------
    .. code-block:: python

        class DivisorOfEighteen(Integer):
            '''
            ASN.1 specification:

            Divisors-of-18 ::= INTEGER (INCLUDES Divisors-of-6 | 9 | 18)
            '''
            subtypeSpec = ContainedSubtypeConstraint(
                SingleValueConstraint(1, 2, 3, 6), 9, 18
            )

        # this will succeed
        divisor_of_eighteen = DivisorOfEighteen(9)

        # this will raise ValueConstraintError
        divisor_of_eighteen = DivisorOfEighteen(10)
    """

class ValueRangeConstraint(AbstractConstraint):
    """Create a ValueRangeConstraint object.

    The ValueRangeConstraint satisfies any value that
    falls in the range of permitted values.

    The ValueRangeConstraint object can only be applied
    to :class:`~pyasn1.type.univ.Integer` and
    :class:`~pyasn1.type.univ.Real` types.

    Parameters
    ----------
    start: :class:`int`
        Minimum permitted value in the range (inclusive)

    end: :class:`int`
        Maximum permitted value in the range (inclusive)

    Examples
    --------
    .. code-block:: python

        class TeenAgeYears(Integer):
            '''
            ASN.1 specification:

            TeenAgeYears ::= INTEGER (13 .. 19)
            '''
            subtypeSpec = ValueRangeConstraint(13, 19)

        # this will succeed
        teen_year = TeenAgeYears(18)

        # this will raise ValueConstraintError
        teen_year = TeenAgeYears(20)
    """

class ValueSizeConstraint(ValueRangeConstraint):
    """Create a ValueSizeConstraint object.

    The ValueSizeConstraint satisfies any value for
    as long as its size falls within the range of
    permitted sizes.

    The ValueSizeConstraint object can be applied
    to :class:`~pyasn1.type.univ.BitString`,
    :class:`~pyasn1.type.univ.OctetString` (including
    all :ref:`character ASN.1 types <type.char>`),
    :class:`~pyasn1.type.univ.SequenceOf`
    and :class:`~pyasn1.type.univ.SetOf` types.

    Parameters
    ----------
    minimum: :class:`int`
        Minimum permitted size of the value (inclusive)

    maximum: :class:`int`
        Maximum permitted size of the value (inclusive)

    Examples
    --------
    .. code-block:: python

        class BaseballTeamRoster(SetOf):
            '''
            ASN.1 specification:

            BaseballTeamRoster ::= SET SIZE (1..25) OF PlayerNames
            '''
            componentType = PlayerNames()
            subtypeSpec = ValueSizeConstraint(1, 25)

        # this will succeed
        team = BaseballTeamRoster()
        team.extend(['Jan', 'Matej'])
        encode(team)

        # this will raise ValueConstraintError
        team = BaseballTeamRoster()
        team.extend(['Jan'] * 26)
        encode(team)

    Note
    ----
    Whenever ValueSizeConstraint is applied to mutable types
    (e.g. :class:`~pyasn1.type.univ.SequenceOf`,
    :class:`~pyasn1.type.univ.SetOf`), constraint
    validation only happens at the serialisation phase rather
    than schema instantiation phase (as it is with immutable
    types).
    """

class PermittedAlphabetConstraint(SingleValueConstraint):
    """Create a PermittedAlphabetConstraint object.

    The PermittedAlphabetConstraint satisfies any character
    string for as long as all its characters are present in
    the set of permitted characters.

    Objects of this type are iterable (emitting constraint values) and
    can act as operands for some arithmetic operations e.g. addition
    and subtraction.

    The PermittedAlphabetConstraint object can only be applied
    to the :ref:`character ASN.1 types <type.char>` such as
    :class:`~pyasn1.type.char.IA5String`.

    Parameters
    ----------
    *alphabet: :class:`str`
        Full set of characters permitted by this constraint object.

    Example
    -------
    .. code-block:: python

        class BooleanValue(IA5String):
            '''
            ASN.1 specification:

            BooleanValue ::= IA5String (FROM ('T' | 'F'))
            '''
            subtypeSpec = PermittedAlphabetConstraint('T', 'F')

        # this will succeed
        truth = BooleanValue('T')
        truth = BooleanValue('TF')

        # this will raise ValueConstraintError
        garbage = BooleanValue('TAF')

    ASN.1 `FROM ... EXCEPT ...` clause can be modelled by combining multiple
    PermittedAlphabetConstraint objects into one:

    Example
    -------
    .. code-block:: python

        class Lipogramme(IA5String):
            '''
            ASN.1 specification:

            Lipogramme ::=
                IA5String (FROM (ALL EXCEPT ("e"|"E")))
            '''
            subtypeSpec = (
                PermittedAlphabetConstraint(*string.printable) -
                PermittedAlphabetConstraint('e', 'E')
            )

        # this will succeed
        lipogramme = Lipogramme('A work of fiction?')

        # this will raise ValueConstraintError
        lipogramme = Lipogramme('Eel')

    Note
    ----
    Although `ConstraintsExclusion` object could seemingly be used for this
    purpose, practically, for it to work, it needs to represent its operand
    constraints as sets and intersect one with the other. That would require
    the insight into the constraint values (and their types) that are otherwise
    hidden inside the constraint object.

    Therefore it's more practical to model `EXCEPT` clause at
    `PermittedAlphabetConstraint` level instead.
    """

class ComponentPresentConstraint(AbstractConstraint):
    """Create a ComponentPresentConstraint object.

    The ComponentPresentConstraint is only satisfied when the value
    is not `None`.

    The ComponentPresentConstraint object is typically used with
    `WithComponentsConstraint`.

    Examples
    --------
    .. code-block:: python

        present = ComponentPresentConstraint()

        # this will succeed
        present('whatever')

        # this will raise ValueConstraintError
        present(None)
    """

class ComponentAbsentConstraint(AbstractConstraint):
    """Create a ComponentAbsentConstraint object.

    The ComponentAbsentConstraint is only satisfied when the value
    is `None`.

    The ComponentAbsentConstraint object is typically used with
    `WithComponentsConstraint`.

    Examples
    --------
    .. code-block:: python

        absent = ComponentAbsentConstraint()

        # this will succeed
        absent(None)

        # this will raise ValueConstraintError
        absent('whatever')
    """

class WithComponentsConstraint(AbstractConstraint):
    """Create a WithComponentsConstraint object.

    The `WithComponentsConstraint` satisfies any mapping object that has
    constrained fields present or absent, what is indicated by
    `ComponentPresentConstraint` and `ComponentAbsentConstraint`
    objects respectively.

    The `WithComponentsConstraint` object is typically applied
    to  :class:`~pyasn1.type.univ.Set` or
    :class:`~pyasn1.type.univ.Sequence` types.

    Parameters
    ----------
    *fields: :class:`tuple`
        Zero or more tuples of (`field`, `constraint`) indicating constrained
        fields.

    Notes
    -----
    On top of the primary use of `WithComponentsConstraint` (ensuring presence
    or absence of particular components of a :class:`~pyasn1.type.univ.Set` or
    :class:`~pyasn1.type.univ.Sequence`), it is also possible to pass any other
    constraint objects or their combinations. In case of scalar fields, these
    constraints will be verified in addition to the constraints belonging to
    scalar components themselves. However, formally, these additional
    constraints do not change the type of these ASN.1 objects.

    Examples
    --------

    .. code-block:: python

        class Item(Sequence):  #  Set is similar
            '''
            ASN.1 specification:

            Item ::= SEQUENCE {
                id    INTEGER OPTIONAL,
                name  OCTET STRING OPTIONAL
            } WITH COMPONENTS id PRESENT, name ABSENT | id ABSENT, name PRESENT
            '''
            componentType = NamedTypes(
                OptionalNamedType('id', Integer()),
                OptionalNamedType('name', OctetString())
            )
            withComponents = ConstraintsUnion(
                WithComponentsConstraint(
                    ('id', ComponentPresentConstraint()),
                    ('name', ComponentAbsentConstraint())
                ),
                WithComponentsConstraint(
                    ('id', ComponentAbsentConstraint()),
                    ('name', ComponentPresentConstraint())
                )
            )

        item = Item()

        # This will succeed
        item['id'] = 1

        # This will succeed
        item.reset()
        item['name'] = 'John'

        # This will fail (on encoding)
        item.reset()
        descr['id'] = 1
        descr['name'] = 'John'
    """

class InnerTypeConstraint(AbstractConstraint):
    """Value must satisfy the type and presence constraints"""

class ConstraintsExclusion(AbstractConstraint):
    """Create a ConstraintsExclusion logic operator object.

    The ConstraintsExclusion logic operator succeeds when the
    value does *not* satisfy the operand constraint.

    The ConstraintsExclusion object can be applied to
    any constraint and logic operator object.

    Parameters
    ----------
    *constraints:
        Constraint or logic operator objects.

    Examples
    --------
    .. code-block:: python

        class LuckyNumber(Integer):
            subtypeSpec = ConstraintsExclusion(
                SingleValueConstraint(13)
            )

        # this will succeed
        luckyNumber = LuckyNumber(12)

        # this will raise ValueConstraintError
        luckyNumber = LuckyNumber(13)

    Note
    ----
    The `FROM ... EXCEPT ...` ASN.1 clause should be modeled by combining
    constraint objects into one. See `PermittedAlphabetConstraint` for more
    information.
    """

class AbstractConstraintSet(AbstractConstraint):
    def __getitem__(self, idx): ...
    def __iter__(self): ...
    def __add__(self, value): ...
    def __radd__(self, value): ...
    def __len__(self) -> int: ...

class ConstraintsIntersection(AbstractConstraintSet):
    """Create a ConstraintsIntersection logic operator object.

    The ConstraintsIntersection logic operator only succeeds
    if *all* its operands succeed.

    The ConstraintsIntersection object can be applied to
    any constraint and logic operator objects.

    The ConstraintsIntersection object duck-types the immutable
    container object like Python :py:class:`tuple`.

    Parameters
    ----------
    *constraints:
        Constraint or logic operator objects.

    Examples
    --------
    .. code-block:: python

        class CapitalAndSmall(IA5String):
            '''
            ASN.1 specification:

            CapitalAndSmall ::=
                IA5String (FROM ("A".."Z"|"a".."z"))
            '''
            subtypeSpec = ConstraintsIntersection(
                PermittedAlphabetConstraint('A', 'Z'),
                PermittedAlphabetConstraint('a', 'z')
            )

        # this will succeed
        capital_and_small = CapitalAndSmall('Hello')

        # this will raise ValueConstraintError
        capital_and_small = CapitalAndSmall('hello')
    """

class ConstraintsUnion(AbstractConstraintSet):
    """Create a ConstraintsUnion logic operator object.

    The ConstraintsUnion logic operator succeeds if
    *at least* a single operand succeeds.

    The ConstraintsUnion object can be applied to
    any constraint and logic operator objects.

    The ConstraintsUnion object duck-types the immutable
    container object like Python :py:class:`tuple`.

    Parameters
    ----------
    *constraints:
        Constraint or logic operator objects.

    Examples
    --------
    .. code-block:: python

        class CapitalOrSmall(IA5String):
            '''
            ASN.1 specification:

            CapitalOrSmall ::=
                IA5String (FROM ("A".."Z") | FROM ("a".."z"))
            '''
            subtypeSpec = ConstraintsUnion(
                PermittedAlphabetConstraint('A', 'Z'),
                PermittedAlphabetConstraint('a', 'z')
            )

        # this will succeed
        capital_or_small = CapitalAndSmall('Hello')

        # this will raise ValueConstraintError
        capital_or_small = CapitalOrSmall('hello!')
    """
