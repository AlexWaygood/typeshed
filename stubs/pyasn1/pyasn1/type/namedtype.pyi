__all__ = ["NamedType", "OptionalNamedType", "DefaultedNamedType", "NamedTypes"]

class NamedType:
    """Create named field object for a constructed ASN.1 type.

    The |NamedType| object represents a single name and ASN.1 type of a constructed ASN.1 type.

    |NamedType| objects are immutable and duck-type Python :class:`tuple` objects
    holding *name* and *asn1Object* components.

    Parameters
    ----------
    name: :py:class:`str`
        Field name

    asn1Object:
        ASN.1 type object
    """

    isOptional: bool
    isDefaulted: bool
    def __init__(self, name, asn1Object, openType: type | None = None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __hash__(self): ...
    def __getitem__(self, idx): ...
    def __iter__(self): ...
    @property
    def name(self): ...
    @property
    def asn1Object(self): ...
    @property
    def openType(self): ...
    def getName(self): ...
    def getType(self): ...

class OptionalNamedType(NamedType):
    """Create named field object for a constructed ASN.1 type.

    The |NamedType| object represents a single name and ASN.1 type of a constructed ASN.1 type.

    |NamedType| objects are immutable and duck-type Python :class:`tuple` objects
    holding *name* and *asn1Object* components.

    Parameters
    ----------
    name: :py:class:`str`
        Field name

    asn1Object:
        ASN.1 type object
    """

    isOptional: bool

class DefaultedNamedType(NamedType):
    """Create named field object for a constructed ASN.1 type.

    The |NamedType| object represents a single name and ASN.1 type of a constructed ASN.1 type.

    |NamedType| objects are immutable and duck-type Python :class:`tuple` objects
    holding *name* and *asn1Object* components.

    Parameters
    ----------
    name: :py:class:`str`
        Field name

    asn1Object:
        ASN.1 type object
    """

    isDefaulted: bool

class NamedTypes:
    """Create a collection of named fields for a constructed ASN.1 type.

    The NamedTypes object represents a collection of named fields of a constructed ASN.1 type.

    *NamedTypes* objects are immutable and duck-type Python :class:`dict` objects
    holding *name* as keys and ASN.1 type object as values.

    Parameters
    ----------
    *namedTypes: :class:`~pyasn1.type.namedtype.NamedType`

    Examples
    --------

    .. code-block:: python

        class Description(Sequence):
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

    def __init__(self, *namedTypes, **kwargs) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __hash__(self): ...
    def __getitem__(self, idx): ...
    def __contains__(self, key) -> bool: ...
    def __iter__(self): ...
    def __bool__(self) -> bool: ...
    def __len__(self) -> int: ...
    def values(self): ...
    def keys(self): ...
    def items(self): ...
    def clone(self): ...

    class PostponedError:
        def __init__(self, errorMsg) -> None: ...
        def __getitem__(self, item) -> None: ...

    def getTypeByPosition(self, idx):
        """Return ASN.1 type object by its position in fields set.

        Parameters
        ----------
        idx: :py:class:`int`
            Field index

        Returns
        -------
        :
            ASN.1 type

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If given position is out of fields range
        """

    def getPositionByType(self, tagSet):
        """Return field position by its ASN.1 type.

        Parameters
        ----------
        tagSet: :class:`~pysnmp.type.tag.TagSet`
            ASN.1 tag set distinguishing one ASN.1 type from others.

        Returns
        -------
        : :py:class:`int`
            ASN.1 type position in fields set

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If *tagSet* is not present or ASN.1 types are not unique within callee *NamedTypes*
        """

    def getNameByPosition(self, idx):
        """Return field name by its position in fields set.

        Parameters
        ----------
        idx: :py:class:`idx`
            Field index

        Returns
        -------
        : :py:class:`str`
            Field name

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If given field name is not present in callee *NamedTypes*
        """

    def getPositionByName(self, name):
        """Return field position by filed name.

        Parameters
        ----------
        name: :py:class:`str`
            Field name

        Returns
        -------
        : :py:class:`int`
            Field position in fields set

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If *name* is not present or not unique within callee *NamedTypes*
        """

    def getTagMapNearPosition(self, idx):
        """Return ASN.1 types that are allowed at or past given field position.

        Some ASN.1 serialisation allow for skipping optional and defaulted fields.
        Some constructed ASN.1 types allow reordering of the fields. When recovering
        such objects it may be important to know which types can possibly be
        present at any given position in the field sets.

        Parameters
        ----------
        idx: :py:class:`int`
            Field index

        Returns
        -------
        : :class:`~pyasn1.type.tagmap.TagMap`
            Map if ASN.1 types allowed at given field position

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If given position is out of fields range
        """

    def getPositionNearType(self, tagSet, idx):
        """Return the closest field position where given ASN.1 type is allowed.

        Some ASN.1 serialisation allow for skipping optional and defaulted fields.
        Some constructed ASN.1 types allow reordering of the fields. When recovering
        such objects it may be important to know at which field position, in field set,
        given *tagSet* is allowed at or past *idx* position.

        Parameters
        ----------
        tagSet: :class:`~pyasn1.type.tag.TagSet`
           ASN.1 type which field position to look up

        idx: :py:class:`int`
            Field position at or past which to perform ASN.1 type look up

        Returns
        -------
        : :py:class:`int`
            Field position in fields set

        Raises
        ------
        ~pyasn1.error.PyAsn1Error
            If *tagSet* is not present or not unique within callee *NamedTypes*
            or *idx* is out of fields range
        """

    @property
    def minTagSet(self):
        """Return the minimal TagSet among ASN.1 type in callee *NamedTypes*.

        Some ASN.1 types/serialisation protocols require ASN.1 types to be
        arranged based on their numerical tag value. The *minTagSet* property
        returns that.

        Returns
        -------
        : :class:`~pyasn1.type.tagset.TagSet`
            Minimal TagSet among ASN.1 types in callee *NamedTypes*
        """

    @property
    def tagMap(self):
        """Return a *TagMap* object from tags and types recursively.

        Return a :class:`~pyasn1.type.tagmap.TagMap` object by
        combining tags from *TagMap* objects of children types and
        associating them with their immediate child type.

        Example
        -------
        .. code-block:: python

           OuterType ::= CHOICE {
               innerType INTEGER
           }

        Calling *.tagMap* on *OuterType* will yield a map like this:

        .. code-block:: python

           Integer.tagSet -> Choice
        """

    @property
    def tagMapUnique(self):
        """Return a *TagMap* object from unique tags and types recursively.

        Return a :class:`~pyasn1.type.tagmap.TagMap` object by
        combining tags from *TagMap* objects of children types and
        associating them with their immediate child type.

        Example
        -------
        .. code-block:: python

           OuterType ::= CHOICE {
               innerType INTEGER
           }

        Calling *.tagMapUnique* on *OuterType* will yield a map like this:

        .. code-block:: python

           Integer.tagSet -> Choice

        Note
        ----

        Duplicate *TagSet* objects found in the tree of children
        types would cause error.
        """

    @property
    def hasOptionalOrDefault(self): ...
    @property
    def hasOpenTypes(self): ...
    @property
    def namedTypes(self): ...
    @property
    def requiredComponents(self): ...
