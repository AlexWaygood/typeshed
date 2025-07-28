"""Model classes for datastore objects and properties for models.

.. testsetup:: *

    from unittest import mock
    from google.cloud import ndb
    from google.cloud.ndb import context as context_module

    client = mock.Mock(
        project="testing",
        database=None,
        namespace=None,
        stub=mock.Mock(spec=()),
        spec=("project", "namespace", "database", "stub"),
    )
    context = context_module.Context(client).use()
    context.__enter__()

.. testcleanup:: *

    context.__exit__(None, None, None)

A model class represents the structure of entities stored in the datastore.
Applications define model classes to indicate the structure of their entities,
then instantiate those model classes to create entities.

All model classes must inherit (directly or indirectly) from Model. Through
the magic of metaclasses, straightforward assignments in the model class
definition can be used to declare the model's structure::

    class Person(Model):
        name = StringProperty()
        age = IntegerProperty()

We can now create a Person entity and write it to Cloud Datastore::

    person = Person(name='Arthur Dent', age=42)
    key = person.put()

The return value from put() is a Key (see the documentation for
``ndb/key.py``), which can be used to retrieve the same entity later::

    person2 = key.get()
    person2 == person  # Returns True

To update an entity, simply change its attributes and write it back (note that
this doesn't change the key)::

    person2.name = 'Arthur Philip Dent'
    person2.put()

We can also delete an entity (by using the key)::

    key.delete()

The property definitions in the class body tell the system the names and the
types of the fields to be stored in Cloud Datastore, whether they must be
indexed, their default value, and more.

Many different Property types exist.  Most are indexed by default, the
exceptions are indicated in the list below:

- :class:`StringProperty`: a short text string, limited to at most 1500 bytes
  (when UTF-8 encoded from :class:`str` to bytes).
- :class:`TextProperty`: an unlimited text string; unindexed.
- :class:`BlobProperty`: an unlimited byte string; unindexed.
- :class:`IntegerProperty`: a 64-bit signed integer.
- :class:`FloatProperty`: a double precision floating point number.
- :class:`BooleanProperty`: a bool value.
- :class:`DateTimeProperty`: a datetime object. Note: Datastore always uses
  UTC as the timezone.
- :class:`DateProperty`: a date object.
- :class:`TimeProperty`: a time object.
- :class:`GeoPtProperty`: a geographical location, i.e. (latitude, longitude).
- :class:`KeyProperty`: a Cloud Datastore Key value, optionally constrained to
  referring to a specific kind.
- :class:`UserProperty`: a User object (for backwards compatibility only)
- :class:`StructuredProperty`: a field that is itself structured like an
  entity; see below for more details.
- :class:`LocalStructuredProperty`: like StructuredProperty but the on-disk
  representation is an opaque blob; unindexed.
- :class:`ComputedProperty`: a property whose value is computed from other
  properties by a user-defined function. The property value is written to Cloud
  Datastore so that it can be used in queries, but the value from Cloud
  Datastore is not used when the entity is read back.
- :class:`GenericProperty`: a property whose type is not constrained; mostly
  used by the Expando class (see below) but also usable explicitly.
- :class:`JsonProperty`: a property whose value is any object that can be
  serialized using JSON; the value written to Cloud Datastore is a JSON
  representation of that object.
- :class:`PickleProperty`: a property whose value is any object that can be
  serialized using Python's pickle protocol; the value written to the Cloud
  Datastore is the pickled representation of that object, using the highest
  available pickle protocol

Most Property classes have similar constructor signatures.  They
accept several optional keyword arguments:

- name=<string>: the name used to store the property value in the datastore.
  Unlike the following options, this may also be given as a positional
  argument.
- indexed=<bool>: indicates whether the property should be indexed (allowing
  queries on this property's value).
- repeated=<bool>: indicates that this property can have multiple values in
  the same entity.
- write_empty_list<bool>: For repeated value properties, controls whether
  properties with no elements (the empty list) is written to Datastore. If
  true, written, if false, then nothing is written to Datastore.
- required=<bool>: indicates that this property must be given a value.
- default=<value>: a default value if no explicit value is given.
- choices=<list of values>: a list or tuple of allowable values.
- validator=<function>: a general-purpose validation function. It will be
  called with two arguments (prop, value) and should either return the
  validated value or raise an exception. It is also allowed for the function
  to modify the value, but the function should be idempotent. For example: a
  validator that returns value.strip() or value.lower() is fine, but one that
  returns value + '$' is not).
- verbose_name=<value>: A human readable name for this property. This human
  readable name can be used for html form labels.

The repeated and required/default options are mutually exclusive: a repeated
property cannot be required nor can it specify a default value (the default is
always an empty list and an empty list is always an allowed value), but a
required property can have a default.

Some property types have additional arguments.  Some property types do not
support all options.

Repeated properties are always represented as Python lists; if there is only
one value, the list has only one element. When a new list is assigned to a
repeated property, all elements of the list are validated. Since it is also
possible to mutate lists in place, repeated properties are re-validated before
they are written to the datastore.

No validation happens when an entity is read from Cloud Datastore; however
property values read that have the wrong type (e.g. a string value for an
IntegerProperty) are ignored.

For non-repeated properties, None is always a possible value, and no validation
is called when the value is set to None. However for required properties,
writing the entity to Cloud Datastore requires the value to be something other
than None (and valid).

The StructuredProperty is different from most other properties; it lets you
define a sub-structure for your entities. The substructure itself is defined
using a model class, and the attribute value is an instance of that model
class. However, it is not stored in the datastore as a separate entity;
instead, its attribute values are included in the parent entity using a naming
convention (the name of the structured attribute followed by a dot followed by
the name of the subattribute). For example::

    class Address(Model):
      street = StringProperty()
      city = StringProperty()

    class Person(Model):
      name = StringProperty()
      address = StructuredProperty(Address)

    p = Person(name='Harry Potter',
               address=Address(street='4 Privet Drive',
               city='Little Whinging'))
    k = p.put()

This would write a single 'Person' entity with three attributes (as you could
verify using the Datastore Viewer in the Admin Console)::

    name = 'Harry Potter'
    address.street = '4 Privet Drive'
    address.city = 'Little Whinging'

Structured property types can be nested arbitrarily deep, but in a hierarchy of
nested structured property types, only one level can have the repeated flag
set. It is fine to have multiple structured properties referencing the same
model class.

It is also fine to use the same model class both as a top-level entity class
and as for a structured property; however, queries for the model class will
only return the top-level entities.

The LocalStructuredProperty works similar to StructuredProperty on the Python
side. For example::

    class Address(Model):
        street = StringProperty()
        city = StringProperty()

    class Person(Model):
        name = StringProperty()
        address = LocalStructuredProperty(Address)

    p = Person(name='Harry Potter',
               address=Address(street='4 Privet Drive',
               city='Little Whinging'))
    k = p.put()

However, the data written to Cloud Datastore is different; it writes a 'Person'
entity with a 'name' attribute as before and a single 'address' attribute
whose value is a blob which encodes the Address value (using the standard
"protocol buffer" encoding).

The Model class offers basic query support. You can create a Query object by
calling the query() class method. Iterating over a Query object returns the
entities matching the query one at a time. Query objects are fully described
in the documentation for query, but there is one handy shortcut that is only
available through Model.query(): positional arguments are interpreted as filter
expressions which are combined through an AND operator. For example::

    Person.query(Person.name == 'Harry Potter', Person.age >= 11)

is equivalent to::

    Person.query().filter(Person.name == 'Harry Potter', Person.age >= 11)

Keyword arguments passed to .query() are passed along to the Query()
constructor.

It is possible to query for field values of structured properties. For
example::

    qry = Person.query(Person.address.city == 'London')

A number of top-level functions also live in this module:

- :func:`get_multi` reads multiple entities at once.
- :func:`put_multi` writes multiple entities at once.
- :func:`delete_multi` deletes multiple entities at once.

All these have a corresponding ``*_async()`` variant as well. The
``*_multi_async()`` functions return a list of Futures.

There are many other interesting features. For example, Model subclasses may
define pre-call and post-call hooks for most operations (get, put, delete,
allocate_ids), and Property classes may be subclassed to suit various needs.
Documentation for writing a Property subclass is in the docs for the
:class:`Property` class.
"""

import datetime
from _typeshed import Unused
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Literal, NoReturn
from typing_extensions import Self, TypeAlias

from google.cloud.ndb import exceptions, key as key_module, query as query_module, tasklets as tasklets_module

Key = key_module.Key
Rollback = exceptions.Rollback
BlobKey: object
GeoPt: object

class KindError(exceptions.BadValueError):
    """Raised when an implementation for a kind can't be found.

    May also be raised when the kind is not a byte string.
    """

class InvalidPropertyError(exceptions.Error):
    """Raised when a property is not applicable to a given use.

    For example, a property must exist and be indexed to be used in a query's
    projection or group by clause.
    """

BadProjectionError = InvalidPropertyError

class UnprojectedPropertyError(exceptions.Error):
    """Raised when getting a property value that's not in the projection."""

class ReadonlyPropertyError(exceptions.Error):
    """Raised when attempting to set a property value that is read-only."""

class ComputedPropertyError(ReadonlyPropertyError):
    """Raised when attempting to set or delete a computed property."""

class UserNotFoundError(exceptions.Error):
    """No email argument was specified, and no user is logged in."""

class _NotEqualMixin:
    """Mix-in class that implements __ne__ in terms of __eq__."""

    def __ne__(self, other: object) -> bool:
        """Implement self != other as not(self == other)."""

_Direction: TypeAlias = Literal["asc", "desc"]

class IndexProperty(_NotEqualMixin):
    """Immutable object representing a single property in an index."""

    def __new__(cls, name: str, direction: _Direction) -> Self: ...
    @property
    def name(self) -> str:
        """str: The property name being indexed."""

    @property
    def direction(self) -> _Direction:
        """str: The direction in the index, ``asc`` or ``desc``."""

    def __eq__(self, other: object) -> bool:
        """Compare two index properties for equality."""

    def __hash__(self) -> int: ...

class Index(_NotEqualMixin):
    """Immutable object representing an index."""

    def __new__(cls, kind: str, properties: list[IndexProperty], ancestor: bool) -> Self: ...
    @property
    def kind(self) -> str:
        """str: The kind being indexed."""

    @property
    def properties(self) -> list[IndexProperty]:
        """List[IndexProperty]: The properties being indexed."""

    @property
    def ancestor(self) -> bool:
        """bool: Indicates if this is an ancestor index."""

    def __eq__(self, other) -> bool:
        """Compare two indexes."""

    def __hash__(self) -> int: ...

class IndexState(_NotEqualMixin):
    """Immutable object representing an index and its state."""

    def __new__(cls, definition, state, id): ...
    @property
    def definition(self):
        """Index: The index corresponding to the tracked state."""

    @property
    def state(self):
        """str: The index state.

        Possible values are ``error``, ``deleting``, ``serving`` or
        ``building``.
        """

    @property
    def id(self):
        """int: The index ID."""

    def __eq__(self, other) -> bool:
        """Compare two index states."""

    def __hash__(self) -> int: ...

class ModelAdapter:
    # This actually returns NoReturn, but mypy can't handle that
    def __new__(cls, *args, **kwargs) -> Self: ...

def make_connection(*args, **kwargs) -> NoReturn: ...

class ModelAttribute:
    """Base for classes that implement a ``_fix_up()`` method."""

class _BaseValue(_NotEqualMixin):
    """A marker object wrapping a "base type" value.

    This is used to be able to tell whether ``entity._values[name]`` is a
    user value (i.e. of a type that the Python code understands) or a
    base value (i.e of a type that serialization understands).
    User values are unwrapped; base values are wrapped in a
    :class:`_BaseValue` instance.

    Args:
        b_val (Any): The base value to be wrapped.

    Raises:
        TypeError: If ``b_val`` is :data:`None`.
        TypeError: If ``b_val`` is a list.
    """

    b_val: object
    def __init__(self, b_val) -> None: ...
    def __eq__(self, other) -> bool:
        """Compare two :class:`_BaseValue` instances."""

    def __hash__(self) -> int: ...

class Property(ModelAttribute):
    """A class describing a typed, persisted attribute of an entity.

    .. warning::

        This is not to be confused with Python's ``@property`` built-in.

    .. note::

        This is just a base class; there are specific subclasses that
        describe properties of various types (and :class:`GenericProperty`
        which describes a dynamically typed property).

    The :class:`Property` does not reserve any "public" names (i.e. names
    that don't start with an underscore). This is intentional; the subclass
    :class:`StructuredProperty` uses the public attribute namespace to refer to
    nested property names (this is essential for specifying queries on
    subproperties).

    The :meth:`IN` attribute is provided as an alias for ``_IN``, but ``IN``
    can be overridden if a subproperty has the same name.

    The :class:`Property` class and its predefined subclasses allow easy
    subclassing using composable (or stackable) validation and
    conversion APIs. These require some terminology definitions:

    * A **user value** is a value such as would be set and accessed by the
      application code using standard attributes on the entity.
    * A **base value** is a value such as would be serialized to
      and deserialized from Cloud Datastore.

    A property will be a member of a :class:`Model` and will be used to help
    store values in an ``entity`` (i.e. instance of a model subclass). The
    underlying stored values can be either user values or base values.

    To interact with the composable conversion and validation API, a
    :class:`Property` subclass can define

    * ``_to_base_type()``
    * ``_from_base_type()``
    * ``_validate()``

    These should **not** call their ``super()`` method, since the methods
    are meant to be composed. For example with composable validation:

    .. code-block:: python

        class Positive(ndb.IntegerProperty):
            def _validate(self, value):
                if value < 1:
                    raise ndb.exceptions.BadValueError("Non-positive", value)


        class SingleDigit(Positive):
            def _validate(self, value):
                if value > 9:
                    raise ndb.exceptions.BadValueError("Multi-digit", value)

    neither ``_validate()`` method calls ``super()``. Instead, when a
    ``SingleDigit`` property validates a value, it composes all validation
    calls in order:

    * ``SingleDigit._validate``
    * ``Positive._validate``
    * ``IntegerProperty._validate``

    The API supports "stacking" classes with ever more sophisticated
    user / base conversions:

    * the user to base conversion goes from more sophisticated to less
      sophisticated
    * the base to user conversion goes from less sophisticated to more
      sophisticated

    For example, see the relationship between :class:`BlobProperty`,
    :class:`TextProperty` and :class:`StringProperty`.

    The validation API distinguishes between "lax" and "strict" user values.
    The set of lax values is a superset of the set of strict values. The
    ``_validate()`` method takes a lax value and if necessary converts it to
    a strict value. For example, an integer (lax) can be converted to a
    floating point (strict) value. This means that when setting the property
    value, lax values are accepted, while when getting the property value, only
    strict values will be returned. If no conversion is needed, ``_validate()``
    may return :data:`None`. If the argument is outside the set of accepted lax
    values, ``_validate()`` should raise an exception, preferably
    :exc:`TypeError` or :exc:`.BadValueError`.

    A class utilizing all three may resemble:

    .. code-block:: python

        class WidgetProperty(ndb.Property):

            def _validate(self, value):
                # Lax user value to strict user value.
                if not isinstance(value, Widget):
                    raise ndb.exceptions.BadValueError(value)

            def _to_base_type(self, value):
                # (Strict) user value to base value.
                if isinstance(value, Widget):
                    return value.to_internal()

            def _from_base_type(self, value):
                # Base value to (strict) user value.'
                if not isinstance(value, _WidgetInternal):
                    return Widget(value)

    There are some things that ``_validate()``, ``_to_base_type()`` and
    ``_from_base_type()`` do **not** need to handle:

    * :data:`None`: They will not be called with :data:`None` (and if they
      return :data:`None`, this means that the value does not need conversion).
    * Repeated values: The infrastructure takes care of calling
      ``_from_base_type()`` or ``_to_base_type()`` for each list item in a
      repeated value.
    * Wrapping "base" values: The wrapping and unwrapping is taken care of by
      the infrastructure that calls the composable APIs.
    * Comparisons: The comparison operations call ``_to_base_type()`` on
      their operand.
    * Distinguishing between user and base values: the infrastructure
      guarantees that ``_from_base_type()`` will be called with an
      (unwrapped) base value, and that ``_to_base_type()`` will be called
      with a user value.
    * Returning the original value: if any of these return :data:`None`, the
      original value is kept. (Returning a different value not equal to
      :data:`None` will substitute the different value.)

    Additionally, :meth:`_prepare_for_put` can be used to integrate with
    datastore save hooks used by :class:`Model` instances.

    .. automethod:: _prepare_for_put

    Args:
        name (str): The name of the property.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (Any): The default value for this property.
        choices (Iterable[Any]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.
    """

    def __init__(
        self,
        name: str | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: object = None,
        choices: Iterable[object] | None = ...,
        validator: Callable[[Property, Any], object] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...
    def __eq__(self, value: object) -> query_module.FilterNode:  # type: ignore[override]
        """FilterNode: Represents the ``=`` comparison."""

    def __ne__(self, value: object) -> query_module.FilterNode:  # type: ignore[override]
        """FilterNode: Represents the ``!=`` comparison."""

    def __lt__(self, value: object) -> query_module.FilterNode:
        """FilterNode: Represents the ``<`` comparison."""

    def __le__(self, value: object) -> query_module.FilterNode:
        """FilterNode: Represents the ``<=`` comparison."""

    def __gt__(self, value: object) -> query_module.FilterNode:
        """FilterNode: Represents the ``>`` comparison."""

    def __ge__(self, value: object) -> query_module.FilterNode:
        """FilterNode: Represents the ``>=`` comparison."""

    def IN(
        self, value: Iterable[object], server_op: bool = False
    ) -> query_module.DisjunctionNode | query_module.FilterNode | query_module.FalseNode:
        """For the ``in`` comparison operator.

        The ``in`` operator cannot be overloaded in the way we want
        to, so we define a method. For example:

        .. code-block:: python

            Employee.query(Employee.rank.IN([4, 5, 6]))

        Note that the method is called ``_IN()`` but may normally be invoked
        as ``IN()``; ``_IN()`` is provided for the case that a
        :class:`.StructuredProperty` refers to a model that has a property
        named ``IN``.

        Args:
            value (Iterable[Any]): The set of values that the property value
                must be contained in.

        Returns:
            Union[~google.cloud.ndb.query.DisjunctionNode,                 ~google.cloud.ndb.query.FilterNode,                 ~google.cloud.ndb.query.FalseNode]: A node corresponding
            to the desired in filter.

            * If ``value`` is empty, this will return a :class:`.FalseNode`
            * If ``len(value) == 1``, this will return a :class:`.FilterNode`
            * Otherwise, this will return a :class:`.DisjunctionNode`

        Raises:
            ~google.cloud.ndb.exceptions.BadFilterError: If the current
                property is not indexed.
            ~google.cloud.ndb.exceptions.BadArgumentError: If ``value`` is not
                a basic container (:class:`list`, :class:`tuple`, :class:`set`
                or :class:`frozenset`).
        """

    def NOT_IN(
        self, value: Iterable[object], server_op: bool = False
    ) -> query_module.DisjunctionNode | query_module.FilterNode | query_module.FalseNode:
        """.FilterNode: Represents the ``not_in`` filter."""

    def __neg__(self) -> query_module.PropertyOrder:
        """Return a descending sort order on this property.

        For example:

        .. code-block:: python

            Employee.query().order(-Employee.rank)
        """

    def __pos__(self) -> query_module.PropertyOrder:
        """Return an ascending sort order on this property.

        Note that this is redundant but provided for consistency with
        :meth:`__neg__`. For example, the following two are equivalent:

        .. code-block:: python

            Employee.query().order(+Employee.rank)
            Employee.query().order(Employee.rank)
        """

    def __set__(self, entity: Model, value: object) -> None:
        """Descriptor protocol: set the value on the entity.

        Args:
            entity (Model): An entity to set a value on.
            value (Any): The value to set.
        """

    def __delete__(self, entity: Model) -> None:
        """Descriptor protocol: delete the value from the entity.

        Args:
            entity (Model): An entity to delete a value from.
        """

class ModelKey(Property):
    """Special property to store a special "key" for a :class:`Model`.

    This is intended to be used as a pseudo-:class:`Property` on each
    :class:`Model` subclass. It is **not** intended for other usage in
    application code.

    It allows key-only queries to be done for a given kind.

    .. automethod:: _validate
    """

    def __init__(self) -> None: ...
    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> key_module.Key | list[key_module.Key] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class BooleanProperty(Property):
    """A property that contains values of type bool.

    .. automethod:: _validate
    """

    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> bool | list[bool] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class IntegerProperty(Property):
    """A property that contains values of type integer.

    .. note::

        If a value is a :class:`bool`, it will be coerced to ``0`` (for
        :data:`False`) or ``1`` (for :data:`True`).

    .. automethod:: _validate
    """

    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> int | list[int] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class FloatProperty(Property):
    """A property that contains values of type float.

    .. note::

        If a value is a :class:`bool` or :class:`int`, it will be
        coerced to a floating point value.

    .. automethod:: _validate
    """

    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> float | list[float] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class _CompressedValue(bytes):
    """A marker object wrapping compressed values.

    Args:
        z_val (bytes): A return value of ``zlib.compress``.
    """

    z_val: bytes
    def __init__(self, z_val: bytes) -> None: ...
    def __eq__(self, other: object) -> bool:
        """Compare two compressed values."""

    def __hash__(self) -> NoReturn: ...

class BlobProperty(Property):
    """A property that contains values that are byte strings.

    .. note::

        Unlike most property types, a :class:`BlobProperty` is **not**
        indexed by default.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate

    Args:
        name (str): The name of the property.
        compressed (bool): Indicates if the value should be compressed (via
            ``zlib``).
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (bytes): The default value for this property.
        choices (Iterable[bytes]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.

    Raises:
        NotImplementedError: If the property is both compressed and indexed.
    """

    def __init__(
        self,
        name: str | None = ...,
        compressed: bool | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: bytes | None = ...,
        choices: Iterable[bytes] | None = ...,
        validator: Callable[[Property, Any], object] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...
    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> bytes | list[bytes] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class CompressedTextProperty(BlobProperty):
    """A version of :class:`TextProperty` which compresses values.

    Values are stored as ``zlib`` compressed UTF-8 byte sequences rather than
    as strings as in a regular :class:`TextProperty`. This class allows NDB to
    support passing `compressed=True` to :class:`TextProperty`. It is not
    necessary to instantiate this class directly.
    """

    def __init__(self, *args, **kwargs) -> None: ...

class TextProperty(Property):
    """An unindexed property that contains UTF-8 encoded text values.

    A :class:`TextProperty` is intended for values of unlimited length, hence
    is **not** indexed. Previously, a :class:`TextProperty` could be indexed
    via:

    .. code-block:: python

        class Item(ndb.Model):
            description = ndb.TextProperty(indexed=True)
            ...

    but this usage is no longer supported. If indexed text is desired, a
    :class:`StringProperty` should be used instead.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate

    Args:
        name (str): The name of the property.
        compressed (bool): Indicates if the value should be compressed (via
            ``zlib``). An instance of :class:`CompressedTextProperty` will be
            substituted if `True`.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (Any): The default value for this property.
        choices (Iterable[Any]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.

    Raises:
        NotImplementedError: If ``indexed=True`` is provided.
    """

    def __new__(cls, *args, **kwargs): ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __get__(self, entity: Model, unused_cls: type[Model] | None = ...) -> str | list[str] | None:
        """Descriptor protocol: get the value from the entity.

        Args:
            entity (Model): An entity to get a value from.
            unused_cls (type): The class that owns this instance.
        """

class StringProperty(TextProperty):
    """An indexed property that contains UTF-8 encoded text values.

    This is nearly identical to :class:`TextProperty`, but is indexed. Values
    must be at most 1500 bytes (when UTF-8 encoded from :class:`str` to bytes).

    Raises:
        NotImplementedError: If ``indexed=False`` is provided.
    """

    def __init__(self, *args, **kwargs) -> None: ...

class GeoPtProperty(Property):
    """A property that contains :attr:`.GeoPt` values.

    .. automethod:: _validate
    """

class PickleProperty(BlobProperty):
    """A property that contains values that are pickle-able.

    .. note::

        Unlike most property types, a :class:`PickleProperty` is **not**
        indexed by default.

    This will use :func:`pickle.dumps` with the highest available pickle
    protocol to convert to bytes and :func:`pickle.loads` to convert **from**
    bytes. The base value stored in the datastore will be the pickled bytes.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    """

class JsonProperty(BlobProperty):
    """A property that contains JSON-encodable values.

    .. note::

        Unlike most property types, a :class:`JsonProperty` is **not**
        indexed by default.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate

    Args:
        name (str): The name of the property.
        compressed (bool): Indicates if the value should be compressed (via
            ``zlib``).
        json_type (type): The expected type of values that this property can
            hold. If :data:`None`, any type is allowed.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (Any): The default value for this property.
        choices (Iterable[Any]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.
    """

    def __init__(
        self,
        name: str | None = ...,
        compressed: bool | None = ...,
        json_type: type | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: object = None,
        choices: Iterable[object] | None = ...,
        validator: Callable[[Property, Any], object] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...

class User:
    """Provides the email address, nickname, and ID for a Google Accounts user.

    .. note::

        This class is a port of ``google.appengine.api.users.User``.
        In the (legacy) Google App Engine standard environment, this
        constructor relied on several environment variables to provide a
        fallback for inputs. In particular:

        * ``AUTH_DOMAIN`` for the ``_auth_domain`` argument
        * ``USER_EMAIL`` for the ``email`` argument
        * ``USER_ID`` for the ``_user_id`` argument
        * ``FEDERATED_IDENTITY`` for the (now removed) ``federated_identity``
          argument
        * ``FEDERATED_PROVIDER`` for the (now removed) ``federated_provider``
          argument

        However in the gVisor Google App Engine runtime (e.g. Python 3.7),
        none of these environment variables will be populated.

    .. note::

        Previous versions of the Google Cloud Datastore API had an explicit
        ``UserValue`` field. However, the ``google.datastore.v1`` API returns
        previously stored user values as an ``Entity`` with the meaning set to
        ``ENTITY_USER=20``.

    .. warning::

        The ``federated_identity`` and ``federated_provider`` are
        decommissioned and have been removed from the constructor. Additionally
        ``_strict_mode`` has been removed from the constructor and the
        ``federated_identity()`` and ``federated_provider()`` methods have been
        removed from this class.

    Args:
        email (str): The user's email address.
        _auth_domain (str): The auth domain for the current application.
        _user_id (str): The user ID.

    Raises:
        ValueError: If the ``_auth_domain`` is not passed in.
        UserNotFoundError: If ``email`` is empty.
    """

    def __init__(self, email: str | None = ..., _auth_domain: str | None = ..., _user_id: str | None = ...) -> None: ...
    def nickname(self) -> str:
        """The nickname for this user.

        A nickname is a human-readable string that uniquely identifies a Google
        user with respect to this application, akin to a username. For some
        users, this nickname is an email address or part of the email address.

        Returns:
            str: The nickname of the user.
        """

    def email(self):
        """Returns the user's email address."""

    def user_id(self) -> str | None:
        """Obtains the user ID of the user.

        Returns:
            Optional[str]: A permanent unique identifying string or
            :data:`None`. If the email address was set explicitly, this will
            return :data:`None`.
        """

    def auth_domain(self) -> str:
        """Obtains the user's authentication domain.

        Returns:
            str: The authentication domain. This method is internal and
            should not be used by client applications.
        """

    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...

class UserProperty(Property):
    """A property that contains :class:`.User` values.

    .. warning::

        This exists for backwards compatibility with existing Cloud Datastore
        schemas only; storing :class:`.User` objects directly in Cloud
        Datastore is not recommended.

    .. warning::

        The ``auto_current_user`` and ``auto_current_user_add`` arguments are
        no longer supported.

    .. note::

        On Google App Engine standard, after saving a :class:`User` the user ID
        would automatically be populated by the datastore, even if it wasn't
        set in the :class:`User` value being stored. For example:

        .. code-block:: python

            >>> class Simple(ndb.Model):
            ...     u = ndb.UserProperty()
            ...
            >>> entity = Simple(u=users.User("user@example.com"))
            >>> entity.u.user_id() is None
            True
            >>>
            >>> entity.put()
            >>> # Reload without the cached values
            >>> entity = entity.key.get(use_cache=False,
            ...     use_global_cache=False)
            >>> entity.u.user_id()
            '...9174...'

        However in the gVisor Google App Engine runtime (e.g. Python 3.7),
        this will behave differently. The user ID will only be stored if it
        is manually set in the :class:`User` instance, either by the running
        application or by retrieving a stored :class:`User` that already has
        a user ID set.

    .. automethod:: _validate
    .. automethod:: _prepare_for_put

    Args:
        name (str): The name of the property.
        auto_current_user (bool): Deprecated flag. When supported, if this flag
            was set to :data:`True`, the property value would be set to the
            currently signed-in user whenever the model instance is stored in
            the datastore, overwriting the property's previous value.
            This was useful for tracking which user modifies a model instance.
        auto_current_user_add (bool): Deprecated flag. When supported, if this
            flag was set to :data:`True`, the property value would be set to
            the currently signed-in user he first time the model instance is
            stored in the datastore, unless the property has already been
            assigned a value. This was useful for tracking which user creates
            a model instance, which may not be the same user that modifies it
            later.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (bytes): The default value for this property.
        choices (Iterable[bytes]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.

    Raises:
        NotImplementedError: If ``auto_current_user`` is provided.
        NotImplementedError: If ``auto_current_user_add`` is provided.
    """

    def __init__(
        self,
        name: str | None = ...,
        auto_current_user: bool | None = ...,
        auto_current_user_add: bool | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: bytes | None = ...,
        choices: Iterable[bytes] | None = ...,
        validator: Callable[[Property, Any], object] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...

class KeyProperty(Property):
    """A property that contains :class:`~google.cloud.ndb.key.Key` values.

    The constructor for :class:`KeyProperty` allows at most two positional
    arguments. Any usage of :data:`None` as a positional argument will
    be ignored. Any of the following signatures are allowed:

    .. testsetup:: key-property-constructor

        from google.cloud import ndb


        class SimpleModel(ndb.Model):
            pass

    .. doctest:: key-property-constructor

        >>> name = "my_value"
        >>> ndb.KeyProperty(name)
        KeyProperty('my_value')
        >>> ndb.KeyProperty(SimpleModel)
        KeyProperty(kind='SimpleModel')
        >>> ndb.KeyProperty(name, SimpleModel)
        KeyProperty('my_value', kind='SimpleModel')
        >>> ndb.KeyProperty(SimpleModel, name)
        KeyProperty('my_value', kind='SimpleModel')

    The type of the positional arguments will be used to determine their
    purpose: a string argument is assumed to be the ``name`` and a
    :class:`type` argument is assumed to be the ``kind`` (and checked that
    the type is a subclass of :class:`Model`).

    .. automethod:: _validate

    Args:
        name (str): The name of the property.
        kind (Union[type, str]): The (optional) kind to be stored. If provided
            as a positional argument, this must be a subclass of :class:`Model`
            otherwise the kind name is sufficient.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (~google.cloud.ndb.key.Key): The default value for this property.
        choices (Iterable[~google.cloud.ndb.key.Key]): A container of allowed values for this
            property.
        validator (Callable[[~google.cloud.ndb.model.Property, ~google.cloud.ndb.key.Key], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.
    """

    def __init__(
        self,
        name: str | None = ...,
        kind: type[Model] | str | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: key_module.Key | None = ...,
        choices: Iterable[key_module.Key] | None = ...,
        validator: Callable[[Property, key_module.Key], key_module.Key] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...

class BlobKeyProperty(Property):
    """A property containing :class:`~google.cloud.ndb.model.BlobKey` values.

    .. automethod:: _validate
    """

class DateTimeProperty(Property):
    """A property that contains :class:`~datetime.datetime` values.

    If ``tzinfo`` is not set, this property expects "naive" datetime stamps,
    i.e. no timezone can be set. Furthermore, the assumption is that naive
    datetime stamps represent UTC.

    If ``tzinfo`` is set, timestamps will be stored as UTC and converted back
    to the timezone set by ``tzinfo`` when reading values back out.

    .. note::

        Unlike Django, ``auto_now_add`` can be overridden by setting the
        value before writing the entity. And unlike the legacy
        ``google.appengine.ext.db``, ``auto_now`` does not supply a default
        value. Also unlike legacy ``db``, when the entity is written, the
        property values are updated to match what was written. Finally, beware
        that this also updates the value in the in-process cache, **and** that
        ``auto_now_add`` may interact weirdly with transaction retries (a retry
        of a property with ``auto_now_add`` set will reuse the value that was
        set on the first try).

    .. automethod:: _validate
    .. automethod:: _prepare_for_put

    Args:
        name (str): The name of the property.
        auto_now (bool): Indicates that the property should be set to the
            current datetime when an entity is created and whenever it is
            updated.
        auto_now_add (bool): Indicates that the property should be set to the
            current datetime when an entity is created.
        tzinfo (Optional[datetime.tzinfo]): If set, values read from Datastore
            will be converted to this timezone. Otherwise, values will be
            returned as naive datetime objects with an implied UTC timezone.
        indexed (bool): Indicates if the value should be indexed.
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (~datetime.datetime): The default value for this property.
        choices (Iterable[~datetime.datetime]): A container of allowed values
            for this property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.

    Raises:
        ValueError: If ``repeated=True`` and ``auto_now=True``.
        ValueError: If ``repeated=True`` and ``auto_now_add=True``.
    """

    def __init__(
        self,
        name: str | None = ...,
        auto_now: bool | None = ...,
        auto_now_add: bool | None = ...,
        tzinfo: datetime.tzinfo | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        required: bool | None = ...,
        default: datetime.datetime | None = ...,
        choices: Iterable[datetime.datetime] | None = ...,
        validator: Callable[[Property, Any], object] | None = ...,
        verbose_name: str | None = ...,
        write_empty_list: bool | None = ...,
    ) -> None: ...

class DateProperty(DateTimeProperty):
    """A property that contains :class:`~datetime.date` values.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate
    """

class TimeProperty(DateTimeProperty):
    """A property that contains :class:`~datetime.time` values.

    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate
    """

class StructuredProperty(Property):
    """A Property whose value is itself an entity.

    The values of the sub-entity are indexed and can be queried.
    """

    def __init__(self, model_class: type, name: str | None = ..., **kwargs) -> None: ...
    def __getattr__(self, attrname: str):
        """Dynamically get a subproperty."""

    def IN(self, value: Iterable[object]) -> query_module.DisjunctionNode | query_module.FalseNode: ...  # type: ignore[override]

class LocalStructuredProperty(BlobProperty):
    """A property that contains ndb.Model value.

    .. note::
        Unlike most property types, a :class:`LocalStructuredProperty`
        is **not** indexed.
    .. automethod:: _to_base_type
    .. automethod:: _from_base_type
    .. automethod:: _validate

    Args:
        model_class (type): The class of the property. (Must be subclass of
            ``ndb.Model``.)
        name (str): The name of the property.
        compressed (bool): Indicates if the value should be compressed (via
            ``zlib``).
        repeated (bool): Indicates if this property is repeated, i.e. contains
            multiple values.
        required (bool): Indicates if this property is required on the given
            model type.
        default (Any): The default value for this property.
        validator (Callable[[~google.cloud.ndb.model.Property, Any], bool]): A
            validator to be used to check values.
        verbose_name (str): A longer, user-friendly name for this property.
        write_empty_list (bool): Indicates if an empty list should be written
            to the datastore.
    """

    def __init__(self, model_class: type[Model], **kwargs) -> None: ...

class GenericProperty(Property):
    """A Property whose value can be (almost) any basic type.
    This is mainly used for Expando and for orphans (values present in
    Cloud Datastore but not represented in the Model subclass) but can
    also be used explicitly for properties with dynamically-typed
    values.

    This supports compressed=True, which is only effective for str
    values (not for unicode), and implies indexed=False.
    """

    def __init__(self, name: str | None = ..., compressed: bool = ..., **kwargs) -> None: ...

class ComputedProperty(GenericProperty):
    """A Property whose value is determined by a user-supplied function.
    Computed properties cannot be set directly, but are instead generated by a
    function when required. They are useful to provide fields in Cloud
    Datastore that can be used for filtering or sorting without having to
    manually set the value in code - for example, sorting on the length of a
    BlobProperty, or using an equality filter to check if another field is not
    empty. ComputedProperty can be declared as a regular property, passing a
    function as the first argument, or it can be used as a decorator for the
    function that does the calculation.

    Example:

    >>> class DatastoreFile(ndb.Model):
    ...   name = ndb.model.StringProperty()
    ...   n_lower = ndb.model.ComputedProperty(lambda self: self.name.lower())
    ...
    ...   data = ndb.model.BlobProperty()
    ...
    ...   @ndb.model.ComputedProperty
    ...   def size(self):
    ...     return len(self.data)
    ...
    ...   def _compute_hash(self):
    ...     return hashlib.sha1(self.data).hexdigest()
    ...   hash = ndb.model.ComputedProperty(_compute_hash, name='sha1')
    """

    def __init__(
        self,
        func: Callable[[Model], object],
        name: str | None = ...,
        indexed: bool | None = ...,
        repeated: bool | None = ...,
        verbose_name: str | None = ...,
    ) -> None:
        """Constructor.

        Args:

        func: A function that takes one argument, the model instance, and
            returns a calculated value.
        """

class MetaModel(type):
    """Metaclass for Model.

    This exists to fix up the properties -- they need to know their name. For
    example, defining a model:

    .. code-block:: python

        class Book(ndb.Model):
            pages = ndb.IntegerProperty()

    the ``Book.pages`` property doesn't have the name ``pages`` assigned.
    This is accomplished by calling the ``_fix_up_properties()`` method on the
    class itself.
    """

    def __init__(cls, name: str, bases, classdict) -> None: ...

class Model(_NotEqualMixin, metaclass=MetaModel):
    """A class describing Cloud Datastore entities.

    Model instances are usually called entities. All model classes
    inheriting from :class:`Model` automatically have :class:`MetaModel` as
    their metaclass, so that the properties are fixed up properly after the
    class is defined.

    Because of this, you cannot use the same :class:`Property` object to
    describe multiple properties -- you must create separate :class:`Property`
    objects for each property. For example, this does not work:

    .. code-block:: python

        reuse_prop = ndb.StringProperty()

        class Wrong(ndb.Model):
            first = reuse_prop
            second = reuse_prop

    instead each class attribute needs to be distinct:

    .. code-block:: python

        class NotWrong(ndb.Model):
            first = ndb.StringProperty()
            second = ndb.StringProperty()

    The "kind" for a given :class:`Model` subclass is normally equal to the
    class name (exclusive of the module name or any other parent scope). To
    override the kind, define :meth:`_get_kind`, as follows:

    .. code-block:: python

        class MyModel(ndb.Model):
            @classmethod
            def _get_kind(cls):
                return "AnotherKind"

    A newly constructed entity will not be persisted to Cloud Datastore without
    an explicit call to :meth:`put`.

    User-defined properties can be passed to the constructor via keyword
    arguments:

    .. doctest:: model-keywords

        >>> class MyModel(ndb.Model):
        ...     value = ndb.FloatProperty()
        ...     description = ndb.StringProperty()
        ...
        >>> MyModel(value=7.34e22, description="Mass of the moon")
        MyModel(description='Mass of the moon', value=7.34e+22)

    In addition to user-defined properties, there are seven accepted keyword
    arguments:

    * ``key``
    * ``id``
    * ``app``
    * ``namespace``
    * ``database``
    * ``parent``
    * ``projection``

    Of these, ``key`` is a public attribute on :class:`Model` instances:

    .. testsetup:: model-key

        from google.cloud import ndb


        class MyModel(ndb.Model):
            value = ndb.FloatProperty()
            description = ndb.StringProperty()

    .. doctest:: model-key

        >>> entity1 = MyModel(id=11)
        >>> entity1.key
        Key('MyModel', 11)
        >>> entity2 = MyModel(parent=entity1.key)
        >>> entity2.key
        Key('MyModel', 11, 'MyModel', None)
        >>> entity3 = MyModel(key=ndb.Key(MyModel, "e-three"))
        >>> entity3.key
        Key('MyModel', 'e-three')

    However, a user-defined property can be defined on the model with the
    same name as one of those keyword arguments. In this case, the user-defined
    property "wins":

    .. doctest:: model-keyword-id-collision

        >>> class IDCollide(ndb.Model):
        ...     id = ndb.FloatProperty()
        ...
        >>> entity = IDCollide(id=17)
        >>> entity
        IDCollide(id=17.0)
        >>> entity.key is None
        True

    In such cases of argument "collision", an underscore can be used as a
    keyword argument prefix:

    .. doctest:: model-keyword-id-collision

        >>> entity = IDCollide(id=17, _id=2009)
        >>> entity
        IDCollide(key=Key('IDCollide', 2009), id=17.0)

    For the **very** special case of a property named ``key``, the ``key``
    attribute will no longer be the entity's key but instead will be the
    property value. Instead, the entity's key is accessible via ``_key``:

    .. doctest:: model-keyword-key-collision

        >>> class KeyCollide(ndb.Model):
        ...     key = ndb.StringProperty()
        ...
        >>> entity1 = KeyCollide(key="Take fork in road", id=987)
        >>> entity1
        KeyCollide(_key=Key('KeyCollide', 987), key='Take fork in road')
        >>> entity1.key
        'Take fork in road'
        >>> entity1._key
        Key('KeyCollide', 987)
        >>>
        >>> entity2 = KeyCollide(key="Go slow", _key=ndb.Key(KeyCollide, 1))
        >>> entity2
        KeyCollide(_key=Key('KeyCollide', 1), key='Go slow')

    The constructor accepts keyword arguments based on the properties
    defined on model subclass. However, using keywords for nonexistent
    or non-:class:`Property` class attributes will cause a failure:

    .. doctest:: model-keywords-fail

        >>> class Simple(ndb.Model):
        ...     marker = 1001
        ...     some_name = ndb.StringProperty()
        ...
        >>> Simple(some_name="Value set here.")
        Simple(some_name='Value set here.')
        >>> Simple(some_name="Value set here.", marker=29)
        Traceback (most recent call last):
          ...
        TypeError: Cannot set non-property marker
        >>> Simple(some_name="Value set here.", missing=29)
        Traceback (most recent call last):
          ...
        AttributeError: type object 'Simple' has no attribute 'missing'

    .. automethod:: _get_kind

    Args:
        key (Key): Datastore key for this entity (kind must match this model).
            If ``key`` is used, ``id`` and ``parent`` must be unset or
            :data:`None`.
        id (str): Key ID for this model. If ``id`` is used, ``key`` must be
            :data:`None`.
        parent (Key): The parent model or :data:`None` for a top-level model.
            If ``parent`` is used, ``key`` must be :data:`None`.
        namespace (str): Namespace for the entity key.
        project (str): Project ID for the entity key.
        app (str): DEPRECATED: Synonym for ``project``.
        database (str): Database for the entity key.
        kwargs (Dict[str, Any]): Additional keyword arguments. These should map
            to properties of this model.

    Raises:
        exceptions.BadArgumentError: If the constructor is called with ``key`` and one
            of ``id``, ``app``, ``namespace``, ``database``, or ``parent`` specified.
    """

    key: ModelKey
    def __init__(_self, **kwargs) -> None: ...
    def __hash__(self) -> NoReturn:
        """Not implemented hash function.

        Raises:
            TypeError: Always, to emphasize that entities are mutable.
        """

    def __eq__(self, other: object) -> bool:
        """Compare two entities of the same class for equality."""

    @classmethod
    def gql(cls: type[Model], query_string: str, *args, **kwargs) -> query_module.Query:
        """Run a GQL query using this model as the FROM entity.

        Args:
            query_string (str): The WHERE part of a GQL query (including the
                WHERE keyword).
            args: if present, used to call bind() on the query.
            kwargs: if present, used to call bind() on the query.

        Returns:
            :class:query.Query: A query instance.
        """

    def put(self, **kwargs):
        """Synchronously write this entity to Cloud Datastore.

        If the operation creates or completes a key, the entity's key
        attribute is set to the new, complete key.

        Args:
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            key.Key: The key for the entity. This is always a complete key.
        """

    def put_async(self, **kwargs) -> tasklets_module.Future:
        """Asynchronously write this entity to Cloud Datastore.

        If the operation creates or completes a key, the entity's key
        attribute is set to the new, complete key.

        Args:
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            tasklets.Future: The eventual result will be the key for the
                entity. This is always a complete key.
        """

    @classmethod
    def query(cls: type[Model], *args, **kwargs) -> query_module.Query:
        """Generate a query for this class.

        Args:
            *filters (query.FilterNode): Filters to apply to this query.
            distinct (Optional[bool]): Setting this to :data:`True` is
                shorthand for setting `distinct_on` to `projection`.
            ancestor (key.Key): Entities returned will be descendants of
                `ancestor`.
            order_by (list[Union[str, google.cloud.ndb.model.Property]]):
                The model properties used to order query results.
            orders (list[Union[str, google.cloud.ndb.model.Property]]):
                Deprecated. Synonym for `order_by`.
            project (str): The project to perform the query in. Also known as
                the app, in Google App Engine. If not passed, uses the
                client's value.
            app (str): Deprecated. Synonym for `project`.
            namespace (str): The namespace to which to restrict results.
                If not passed, uses the client's value.
            projection (list[str]): The fields to return as part of the
                query results.
            distinct_on (list[str]): The field names used to group query
                results.
            group_by (list[str]): Deprecated. Synonym for distinct_on.
            default_options (QueryOptions): QueryOptions object.
        """

    @classmethod
    def allocate_ids(
        cls: type[Model],
        size: int | None = ...,
        max: int | None = ...,
        parent: key_module.Key | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
    ) -> tuple[key_module.Key, key_module.Key]:
        """Allocates a range of key IDs for this model class.

        Args:
            size (int): Number of IDs to allocate. Must be specified.
            max (int): Maximum ID to allocated. This feature is no longer
                supported. You must always specify ``size``.
            parent (key.Key): Parent key for which the IDs will be allocated.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            tuple(key.Key): Keys for the newly allocated IDs.
        """

    @classmethod
    def allocate_ids_async(
        cls: type[Model],
        size: int | None = ...,
        max: int | None = ...,
        parent: key_module.Key | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
    ) -> tasklets_module.Future:
        """Allocates a range of key IDs for this model class.

        Args:
            size (int): Number of IDs to allocate. Must be specified.
            max (int): Maximum ID to allocated. This feature is no longer
                supported. You must always specify ``size``.
            parent (key.Key): Parent key for which the IDs will be allocated.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            tasklets.Future: Eventual result is ``tuple(key.Key)``: Keys for
                the newly allocated IDs.
        """

    @classmethod
    def get_by_id(
        cls: type[Model],
        id: int | str | None,
        parent: key_module.Key | None = ...,
        namespace: str | None = ...,
        project: str | None = ...,
        app: str | None = ...,
        read_consistency: Literal["EVENTUAL"] | None = ...,
        read_policy: Literal["EVENTUAL"] | None = ...,
        transaction: bytes | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
        database: str | None = None,
    ) -> Model | None:
        """Get an instance of Model class by ID.

        This really just a shorthand for ``Key(cls, id, ....).get()``.

        Args:
            id (Union[int, str]): ID of the entity to load.
            parent (Optional[key.Key]): Key for the parent of the entity to
                load.
            namespace (Optional[str]): Namespace for the entity to load. If not
                passed, uses the client's value.
            project (Optional[str]): Project id for the entity to load. If not
                passed, uses the client's value.
            app (str): DEPRECATED: Synonym for `project`.
            read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
                waiting for the Datastore to finish applying changes to all
                returned results, you wish to get possibly-not-current results
                faster. You can't do this if using a transaction.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Any results returned will be consistent with
                the Datastore state represented by this transaction id.
                Defaults to the currently running transaction. Cannot be used
                with ``read_consistency=ndb.EVENTUAL``.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.
            database (Optional[str]): This parameter is ignored. Please set the database on the Client instead.

        Returns:
            Optional[Model]: The retrieved entity, if one is found.
        """

    @classmethod
    def get_by_id_async(
        cls: type[Model],
        id: int | str,
        parent: key_module.Key | None = ...,
        namespace: str | None = ...,
        project: str | None = ...,
        app: str | None = ...,
        read_consistency: Literal["EVENTUAL"] | None = ...,
        read_policy: Literal["EVENTUAL"] | None = ...,
        transaction: bytes | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
        database: str | None = None,
    ) -> tasklets_module.Future:
        """Get an instance of Model class by ID.

        This is the asynchronous version of :meth:`get_by_id`.

        Args:
            id (Union[int, str]): ID of the entity to load.
            parent (Optional[key.Key]): Key for the parent of the entity to
                load.
            namespace (Optional[str]): Namespace for the entity to load. If not
                passed, uses the client's value.
            project (Optional[str]): Project id for the entity to load. If not
                passed, uses the client's value.
            app (str): DEPRECATED: Synonym for `project`.
            read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
                waiting for the Datastore to finish applying changes to all
                returned results, you wish to get possibly-not-current results
                faster. You can't do this if using a transaction.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Any results returned will be consistent with
                the Datastore state represented by this transaction id.
                Defaults to the currently running transaction. Cannot be used
                with ``read_consistency=ndb.EVENTUAL``.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.
            database (Optional[str]): This parameter is ignored. Please set the database on the Client instead.

        Returns:
            tasklets.Future: Optional[Model]: The retrieved entity, if one is
                found.
        """

    @classmethod
    def get_or_insert(
        cls: type[Model],
        _name: str,
        parent: key_module.Key | None = ...,
        namespace: str | None = ...,
        project: str | None = ...,
        app: str | None = ...,
        read_consistency: Literal["EVENTUAL"] | None = ...,
        read_policy: Literal["EVENTUAL"] | None = ...,
        transaction: bytes | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
        **kw_model_args,
    ) -> Model:
        """Transactionally retrieves an existing entity or creates a new one.

        Will attempt to look up an entity with the given ``name`` and
        ``parent``. If none is found a new entity will be created using the
        given ``name`` and ``parent``, and passing any ``kw_model_args`` to the
        constructor the ``Model`` class.

        If not already in a transaction, a new transaction will be created and
        this operation will be run in that transaction.

        Args:
            name (str): Name of the entity to load or create.
            parent (Optional[key.Key]): Key for the parent of the entity to
                load.
            namespace (Optional[str]): Namespace for the entity to load. If not
                passed, uses the client's value.
            project (Optional[str]): Project id for the entity to load. If not
                passed, uses the client's value.
            app (str): DEPRECATED: Synonym for `project`.
            **kw_model_args: Keyword arguments to pass to the constructor of
                the model class if an instance for the specified key name does
                not already exist. If an instance with the supplied ``name``
                and ``parent`` already exists, these arguments will be
                discarded.
            read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
                waiting for the Datastore to finish applying changes to all
                returned results, you wish to get possibly-not-current results
                faster. You can't do this if using a transaction.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Any results returned will be consistent with
                the Datastore state represented by this transaction id.
                Defaults to the currently running transaction. Cannot be used
                with ``read_consistency=ndb.EVENTUAL``.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            Model: The entity that was either just retrieved or created.
        """

    @classmethod
    def get_or_insert_async(
        cls: type[Model],
        _name: str,
        parent: key_module.Key | None = ...,
        namespace: str | None = ...,
        project: str | None = ...,
        app: str | None = ...,
        read_consistency: Literal["EVENTUAL"] | None = ...,
        read_policy: Literal["EVENTUAL"] | None = ...,
        transaction: bytes | None = ...,
        retries: int | None = ...,
        timeout: float | None = ...,
        deadline: float | None = ...,
        use_cache: bool | None = ...,
        use_global_cache: bool | None = ...,
        global_cache_timeout: int | None = ...,
        use_datastore: bool | None = ...,
        use_memcache: bool | None = ...,
        memcache_timeout: int | None = ...,
        max_memcache_items: int | None = ...,
        force_writes: bool | None = ...,
        _options=...,
        **kw_model_args,
    ) -> tasklets_module.Future:
        """Transactionally retrieves an existing entity or creates a new one.

        This is the asynchronous version of :meth:``_get_or_insert``.

        Args:
            name (str): Name of the entity to load or create.
            parent (Optional[key.Key]): Key for the parent of the entity to
                load.
            namespace (Optional[str]): Namespace for the entity to load. If not
                passed, uses the client's value.
            project (Optional[str]): Project id for the entity to load. If not
                passed, uses the client's value.
            app (str): DEPRECATED: Synonym for `project`.
            **kw_model_args: Keyword arguments to pass to the constructor of
                the model class if an instance for the specified key name does
                not already exist. If an instance with the supplied ``name``
                and ``parent`` already exists, these arguments will be
                discarded.
            read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
                waiting for the Datastore to finish applying changes to all
                returned results, you wish to get possibly-not-current results
                faster. You can't do this if using a transaction.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Any results returned will be consistent with
                the Datastore state represented by this transaction id.
                Defaults to the currently running transaction. Cannot be used
                with ``read_consistency=ndb.EVENTUAL``.
            retries (int): Number of times to retry this operation in the case
                of transient server errors. Operation will potentially be tried
                up to ``retries`` + 1 times. Set to ``0`` to try operation only
                once, with no retries.
            timeout (float): Override the gRPC timeout, in seconds.
            deadline (float): DEPRECATED: Synonym for ``timeout``.
            use_cache (bool): Specifies whether to store entities in in-process
                cache; overrides in-process cache policy for this operation.
            use_global_cache (bool): Specifies whether to store entities in
                global cache; overrides global cache policy for this operation.
            use_datastore (bool): Specifies whether to store entities in
                Datastore; overrides Datastore policy for this operation.
            global_cache_timeout (int): Maximum lifetime for entities in global
                cache; overrides global cache timeout policy for this
                operation.
            use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
            memcache_timeout (int): DEPRECATED: Synonym for
                ``global_cache_timeout``.
            max_memcache_items (int): No longer supported.
            force_writes (bool): No longer supported.

        Returns:
            tasklets.Future: Model: The entity that was either just retrieved
                or created.
        """

    def populate(self, **kwargs) -> None:
        """Populate an instance from keyword arguments.

        Each keyword argument will be used to set a corresponding property.
        Each keyword must refer to a valid property name. This is similar to
        passing keyword arguments to the ``Model`` constructor, except that no
        provision for key, id, or parent are made.

        Arguments:
            **kwargs: Keyword arguments corresponding to properties of this
                model class.
        """

    def has_complete_key(self) -> bool:
        """Return whether this entity has a complete key.

        Returns:
            bool: :data:``True`` if and only if entity has a key and that key
                has a name or an id.
        """

    def to_dict(
        self,
        include: list[object] | tuple[object, object] | set[object] | None = ...,
        exclude: list[object] | tuple[object, object] | set[object] | None = ...,
    ):
        """Return a ``dict`` containing the entity's property values.

        Arguments:
            include (Optional[Union[list, tuple, set]]): Set of property names
                to include. Default is to include all names.
            exclude (Optional[Union[list, tuple, set]]): Set of property names
                to exclude. Default is to not exclude any names.
        """

class Expando(Model):
    """Model subclass to support dynamic Property names and types.

    Sometimes the set of properties is not known ahead of time.  In such
    cases you can use the Expando class.  This is a Model subclass that
    creates properties on the fly, both upon assignment and when loading
    an entity from Cloud Datastore.  For example::

        >>> class SuperPerson(Expando):
                name = StringProperty()
                superpower = StringProperty()

        >>> razorgirl = SuperPerson(name='Molly Millions',
                                    superpower='bionic eyes, razorblade hands',
                                    rasta_name='Steppin' Razor',
                                    alt_name='Sally Shears')
        >>> elastigirl = SuperPerson(name='Helen Parr',
                                     superpower='stretchable body')
        >>> elastigirl.max_stretch = 30  # Meters

        >>> print(razorgirl._properties.keys())
            ['rasta_name', 'name', 'superpower', 'alt_name']
        >>> print(elastigirl._properties)
            {'max_stretch': GenericProperty('max_stretch'),
             'name': StringProperty('name'),
             'superpower': StringProperty('superpower')}

    Note: You can inspect the properties of an expando instance using the
    _properties attribute, as shown above. This property exists for plain Model
    instances too; it is just not as interesting for those.
    """

    def __getattr__(self, name: str): ...
    def __setattr__(self, name: str, value) -> None: ...
    def __delattr__(self, name: str) -> None: ...

def get_multi_async(
    keys: Sequence[key_module.Key],
    read_consistency: Literal["EVENTUAL"] | None = ...,
    read_policy: Literal["EVENTUAL"] | None = ...,
    transaction: bytes | None = ...,
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[tasklets_module.Future]:
    """Fetches a sequence of keys.

    Args:
        keys (Sequence[:class:`~google.cloud.ndb.key.Key`]): A sequence of
            keys.
        read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
            waiting for the Datastore to finish applying changes to all
            returned results, you wish to get possibly-not-current results
            faster. You can't do this if using a transaction.
        transaction (bytes): Any results returned will be consistent with
            the Datastore state represented by this transaction id.
            Defaults to the currently running transaction. Cannot be used
            with ``read_consistency=ndb.EVENTUAL``.
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        read_policy: DEPRECATED: Synonym for ``read_consistency``.
        force_writes (bool): No longer supported.

    Returns:
        List[:class:`~google.cloud.ndb.tasklets.Future`]: List of futures.
    """

def get_multi(
    keys: Sequence[key_module.Key],
    read_consistency: Literal["EVENTUAL"] | None = ...,
    read_policy: Literal["EVENTUAL"] | None = ...,
    transaction: bytes | None = ...,
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[Model | None]:
    """Fetches a sequence of keys.

    Args:
        keys (Sequence[:class:`~google.cloud.ndb.key.Key`]): A sequence of
            keys.
        read_consistency: Set this to ``ndb.EVENTUAL`` if, instead of
            waiting for the Datastore to finish applying changes to all
            returned results, you wish to get possibly-not-current results
            faster. You can't do this if using a transaction.
        transaction (bytes): Any results returned will be consistent with
            the Datastore state represented by this transaction id.
            Defaults to the currently running transaction. Cannot be used
            with ``read_consistency=ndb.EVENTUAL``.
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        read_policy: DEPRECATED: Synonym for ``read_consistency``.
        force_writes (bool): No longer supported.

    Returns:
        List[Union[:class:`~google.cloud.ndb.model.Model`, :data:`None`]]: List
            containing the retrieved models or None where a key was not found.
    """

def put_multi_async(
    entities: list[Model],
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[tasklets_module.Future]:
    """Stores a sequence of Model instances.

    Args:
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        entities (List[:class:`~google.cloud.ndb.model.Model`]): A sequence
            of models to store.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        force_writes (bool): No longer supported.

    Returns:
        List[:class:`~google.cloud.ndb.tasklets.Future`]: List of futures.
    """

def put_multi(
    entities: list[Model],
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[key_module.Key]:
    """Stores a sequence of Model instances.

    Args:
        entities (List[:class:`~google.cloud.ndb.model.Model`]): A sequence
            of models to store.
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        force_writes (bool): No longer supported.

    Returns:
        List[:class:`~google.cloud.ndb.key.Key`]: A list with the stored keys.
    """

def delete_multi_async(
    keys: Sequence[key_module.Key],
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[tasklets_module.Future]:
    """Deletes a sequence of keys.

    Args:
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        keys (Sequence[:class:`~google.cloud.ndb.key.Key`]): A sequence of
            keys.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        force_writes (bool): No longer supported.

    Returns:
        List[:class:`~google.cloud.ndb.tasklets.Future`]: List of futures.
    """

def delete_multi(
    keys: Sequence[key_module.Key],
    retries: int | None = ...,
    timeout: float | None = ...,
    deadline: float | None = ...,
    use_cache: bool | None = ...,
    use_global_cache: bool | None = ...,
    global_cache_timeout: int | None = ...,
    use_datastore: bool | None = ...,
    use_memcache: bool | None = ...,
    memcache_timeout: int | None = ...,
    max_memcache_items: int | None = ...,
    force_writes: bool | None = ...,
    _options: object = None,
) -> list[None]:
    """Deletes a sequence of keys.

    Args:
        keys (Sequence[:class:`~google.cloud.ndb.key.Key`]): A sequence of
            keys.
        retries (int): Number of times to retry this operation in the case
            of transient server errors. Operation will potentially be tried
            up to ``retries`` + 1 times. Set to ``0`` to try operation only
            once, with no retries.
        timeout (float): Override the gRPC timeout, in seconds.
        deadline (float): DEPRECATED: Synonym for ``timeout``.
        use_cache (bool): Specifies whether to store entities in in-process
            cache; overrides in-process cache policy for this operation.
        use_global_cache (bool): Specifies whether to store entities in
            global cache; overrides global cache policy for this operation.
        use_datastore (bool): Specifies whether to store entities in
            Datastore; overrides Datastore policy for this operation.
        global_cache_timeout (int): Maximum lifetime for entities in global
            cache; overrides global cache timeout policy for this
            operation.
        use_memcache (bool): DEPRECATED: Synonym for ``use_global_cache``.
        memcache_timeout (int): DEPRECATED: Synonym for
            ``global_cache_timeout``.
        max_memcache_items (int): No longer supported.
        force_writes (bool): No longer supported.

    Returns:
        List[:data:`None`]: A list whose items are all None, one per deleted
            key.
    """

def get_indexes_async(**options: Unused) -> NoReturn:
    """Get a data structure representing the configured indexes."""

def get_indexes(**options: Unused) -> NoReturn:
    """Get a data structure representing the configured indexes."""
