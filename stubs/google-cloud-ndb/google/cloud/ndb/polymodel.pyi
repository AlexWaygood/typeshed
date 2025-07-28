"""Polymorphic models and queries.

The standard NDB Model class only supports 'functional polymorphism'.
That is, you can create a subclass of Model, and then subclass that
class, as many generations as necessary, and those classes will share
all the same properties and behaviors of their base classes.  However,
subclassing Model in this way gives each subclass its own kind.  This
means that it is not possible to do 'polymorphic queries'.  Building a
query on a base class will only return entities whose kind matches
that base class's kind, and exclude entities that are instances of
some subclass of that base class.

The PolyModel class defined here lets you create class hierarchies
that support polymorphic queries.  Simply subclass PolyModel instead
of Model.
"""

from typing import Any

from google.cloud.ndb import model

class _ClassKeyProperty(model.StringProperty):
    """Property to store the 'class key' of a polymorphic class.

    The class key is a list of strings describing a polymorphic entity's
    place within its class hierarchy.  This property is automatically
    calculated.  For example:

    .. testsetup:: class-key-property

        from google.cloud import ndb


        class Animal(ndb.PolyModel):
            pass


        class Feline(Animal):
            pass


        class Cat(Feline):
            pass

    .. doctest:: class-key-property

        >>> Animal().class_
        ['Animal']
        >>> Feline().class_
        ['Animal', 'Feline']
        >>> Cat().class_
        ['Animal', 'Feline', 'Cat']
    """

    def __init__(self, name=..., indexed: bool = ...) -> None:
        """Constructor.

        If you really want to you can give this a different datastore name
        or make it unindexed.  For example:

        .. code-block:: python

            class Foo(PolyModel):
                class_ = _ClassKeyProperty(indexed=False)
        """

class PolyModel(model.Model):
    """Base class for class hierarchies supporting polymorphic queries.

    Use this class to build hierarchies that can be queried based on
    their types.

    Example:

    Consider the following model hierarchy::

        +------+
        |Animal|
        +------+
          |
          +-----------------+
          |                 |
        +------+          +------+
        |Canine|          |Feline|
        +------+          +------+
          |                 |
          +-------+         +-------+
          |       |         |       |
        +---+   +----+    +---+   +-------+
        |Dog|   |Wolf|    |Cat|   |Panther|
        +---+   +----+    +---+   +-------+

    This class hierarchy has three levels.  The first is the `root
    class`.  All models in a single class hierarchy must inherit from
    this root.  All models in the hierarchy are stored as the same
    kind as the root class.  For example, Panther entities when stored
    to Cloud Datastore are of the kind `Animal`.  Querying against the
    Animal kind will retrieve Cats, Dogs and Canines, for example,
    that match your query.  Different classes stored in the `root
    class` kind are identified by their class key.  When loaded from
    Cloud Datastore, it is mapped to the appropriate implementation
    class.

    Polymorphic properties:

    Properties that are defined in a given base class within a
    hierarchy are stored in Cloud Datastore for all subclasses only.
    So, if the Feline class had a property called `whiskers`, the Cat
    and Panther entities would also have whiskers, but not Animal,
    Canine, Dog or Wolf.

    Polymorphic queries:

    When written to Cloud Datastore, all polymorphic objects
    automatically have a property called `class` that you can query
    against.  Using this property it is possible to easily write a
    query against any sub-hierarchy.  For example, to fetch only
    Canine objects, including all Dogs and Wolves:

    .. code-block:: python

        Canine.query()

    The `class` property is not meant to be used by your code other
    than for queries.  Since it is supposed to represent the real
    Python class it is intended to be hidden from view.  Although if
    you feel the need, it is accessible as the `class_` attribute.

    Root class:

    The root class is the class from which all other classes of the
    hierarchy inherits from.  Each hierarchy has a single root class.
    A class is a root class if it is an immediate child of PolyModel.
    The subclasses of the root class are all the same kind as the root
    class. In other words:

    .. code-block:: python

        Animal.kind() == Feline.kind() == Panther.kind() == 'Animal'

    Note:

    All classes in a given hierarchy must have unique names, since
    the class name is used to identify the appropriate subclass.
    """

    class_: Any
