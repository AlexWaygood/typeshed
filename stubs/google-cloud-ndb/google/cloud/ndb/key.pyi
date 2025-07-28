"""Provides a :class:`.Key` for Google Cloud Datastore.

.. testsetup:: *

    from google.cloud import ndb

A key encapsulates the following pieces of information, which together
uniquely designate a (possible) entity in Google Cloud Datastore:

* a Google Cloud Platform project (a string)
* a list of one or more ``(kind, id)`` pairs where ``kind`` is a string
  and ``id`` is either a string or an integer
* an optional database (a string)
* an optional namespace (a string)

The application ID must always be part of the key, but since most
applications can only access their own entities, it defaults to the
current application ID and you rarely need to worry about it.

The database is an optional database ID. If unspecified, it defaults
to that of the client.
For usage in Cloud NDB, the default database should always be referred
to as an empty string; please do not use "(default)".

The namespace designates a top-level partition of the key space for a
particular application. If you've never heard of namespaces, you can
safely ignore this feature.

Most of the action is in the ``(kind, id)`` pairs. A key must have at
least one ``(kind, id)`` pair. The last ``(kind, id)`` pair gives the kind
and the ID of the entity that the key refers to, the others merely
specify a "parent key".

The kind is a string giving the name of the model class used to
represent the entity. In more traditional databases this would be
the table name. A model class is a Python class derived from
:class:`.Model`. Only the class name itself is used as the kind. This means
all your model classes must be uniquely named within one application. You can
override this on a per-class basis.

The ID is either a string or an integer. When the ID is a string, the
application is in control of how it assigns IDs. For example, you
could use an email address as the ID for Account entities.

To use integer IDs, it's common to let the datastore choose a unique ID for
an entity when first inserted into the datastore. The ID can be set to
:data:`None` to represent the key for an entity that hasn't yet been
inserted into the datastore. The completed key (including the assigned ID)
will be returned after the entity is successfully inserted into the datastore.

A key for which the ID of the last ``(kind, id)`` pair is set to :data:`None`
is called an **incomplete key** or **partial key**. Such keys can only be used
to insert entities into the datastore.

A key with exactly one ``(kind, id)`` pair is called a top level key or a
root key. Top level keys are also used as entity groups, which play a
role in transaction management.

If there is more than one ``(kind, id)`` pair, all but the last pair
represent the "ancestor path", also known as the key of the "parent entity".

Other constraints:

* Kinds and string IDs must not be empty and must be at most 1500 bytes
  long (after UTF-8 encoding)
* Integer IDs must be at least ``1`` and at most ``2**63 - 1`` (i.e. the
  positive part of the range for a 64-bit signed integer)

In the "legacy" Google App Engine runtime, the default namespace could be
set via the namespace manager (``google.appengine.api.namespace_manager``).
On the gVisor Google App Engine runtime (e.g. Python 3.7), the namespace
manager is not available so the default is to have an unset or empty
namespace. To explicitly select the empty namespace pass ``namespace=""``.
"""

from _typeshed import Incomplete
from typing import Any

UNDEFINED: Any

class Key:
    """An immutable datastore key.

    For flexibility and convenience, multiple constructor signatures are
    supported.

    The primary way to construct a key is using positional arguments:

    .. testsetup:: *

        from unittest import mock
        from google.cloud.ndb import context as context_module
        client = mock.Mock(
            project="testing",
            database=None,
            namespace=None,
            stub=mock.Mock(spec=()),
            spec=("project", "database", "namespace", "stub"),
        )
        context = context_module.Context(client).use()
        context.__enter__()
        kind1, id1 = "Parent", "C"
        kind2, id2 = "Child", 42

    .. testcleanup:: *

        context.__exit__(None, None, None)

    .. doctest:: key-constructor-primary

        >>> ndb.Key(kind1, id1, kind2, id2)
        Key('Parent', 'C', 'Child', 42)

    This is shorthand for either of the following two longer forms:

    .. doctest:: key-constructor-flat-or-pairs

        >>> ndb.Key(pairs=[(kind1, id1), (kind2, id2)])
        Key('Parent', 'C', 'Child', 42)
        >>> ndb.Key(flat=[kind1, id1, kind2, id2])
        Key('Parent', 'C', 'Child', 42)

    Either of the above constructor forms can additionally pass in another
    key via the ``parent`` keyword. The ``(kind, id)`` pairs of the parent key
    are inserted before the ``(kind, id)`` pairs passed explicitly.

    .. doctest:: key-constructor-parent

        >>> parent = ndb.Key(kind1, id1)
        >>> parent
        Key('Parent', 'C')
        >>> ndb.Key(kind2, id2, parent=parent)
        Key('Parent', 'C', 'Child', 42)

    You can also construct a Key from a "urlsafe" encoded string:

    .. doctest:: key-constructor-urlsafe

        >>> ndb.Key(urlsafe=b"agdleGFtcGxlcgsLEgRLaW5kGLkKDA")
        Key('Kind', 1337, project='example')

    For rare use cases the following constructors exist:

    .. testsetup:: key-constructor-rare

        from google.cloud.datastore import _app_engine_key_pb2
        reference = _app_engine_key_pb2.Reference(
            app="example",
            path=_app_engine_key_pb2.Path(element=[
                _app_engine_key_pb2.Path.Element(type="Kind", id=1337),
            ]),
        )

    .. doctest:: key-constructor-rare

        >>> # Passing in a low-level Reference object
        >>> reference
        app: "example"
        path {
          element {
            type: "Kind"
            id: 1337
          }
        }
        <BLANKLINE>
        >>> ndb.Key(reference=reference)
        Key('Kind', 1337, project='example')
        >>> # Passing in a serialized low-level Reference
        >>> serialized = reference.SerializeToString()
        >>> serialized
        b'j\\x07exampler\\x0b\\x0b\\x12\\x04Kind\\x18\\xb9\\n\\x0c'
        >>> ndb.Key(serialized=serialized)
        Key('Kind', 1337, project='example')
        >>> # For unpickling, the same as ndb.Key(**kwargs)
        >>> kwargs = {"pairs": [("Cheese", "Cheddar")], "namespace": "good"}
        >>> ndb.Key(kwargs)
        Key('Cheese', 'Cheddar', namespace='good')

    The "urlsafe" string is really a websafe-base64-encoded serialized
    ``Reference``, but it's best to think of it as just an opaque unique
    string.

    If a ``Reference`` is passed (using one of the ``reference``,
    ``serialized`` or ``urlsafe`` keywords), the positional arguments and
    ``namespace`` must match what is already present in the ``Reference``
    (after decoding if necessary). The parent keyword cannot be combined with
    a ``Reference`` in any form.

    Keys are immutable, which means that a Key object cannot be modified
    once it has been created. This is enforced by the implementation as
    well as Python allows.

    Keys also support interaction with the datastore; the methods :meth:`get`,
    :meth:`get_async`, :meth:`delete` and :meth:`delete_async` are
    the only ones that engage in any kind of I/O activity.

    Keys may be pickled.

    Subclassing Key is best avoided; it would be hard to get right.

    Args:
        path_args (Union[Tuple[str, ...], Tuple[Dict]]): Either a tuple of
            ``(kind, id)`` pairs or a single dictionary containing only keyword
            arguments.
        reference (Optional[            ~google.cloud.datastore._app_engine_key_pb2.Reference]): A
            reference protobuf representing a key.
        serialized (Optional[bytes]): A reference protobuf serialized to bytes.
        urlsafe (Optional[bytes]): A reference protobuf serialized to bytes. The
            raw bytes are then converted to a websafe base64-encoded string.
        pairs (Optional[Iterable[Tuple[str, Union[str, int]]]]): An iterable
            of ``(kind, id)`` pairs. If this argument is used, then
            ``path_args`` should be empty.
        flat (Optional[Iterable[Union[str, int]]]): An iterable of the
            ``(kind, id)`` pairs but flattened into a single value. For
            example, the pairs ``[("Parent", 1), ("Child", "a")]`` would be
            flattened to ``["Parent", 1, "Child", "a"]``.
        project (Optional[str]): The Google Cloud Platform project (previously
            on Google App Engine, this was called the Application ID).
        app (Optional[str]): DEPRECATED: Synonym for ``project``.
        namespace (Optional[str]): The namespace for the key.
        parent (Optional[Key]): The parent of the key being
            constructed. If provided, the key path will be **relative** to the
            parent key's path.
        database (Optional[str]): The database to use.
            Defaults to that of the client if a parent was specified, and
            to the default database if it was not.

    Raises:
        TypeError: If none of ``reference``, ``serialized``, ``urlsafe``,
            ``pairs`` or ``flat`` is provided as an argument and no positional
            arguments were given with the path.
    """

    def __new__(cls, *path_args, **kwargs): ...
    def __hash__(self) -> int:
        """Hash value, for use in dictionary lookups.

        .. note::

            This ignores ``app``, ``database``, and ``namespace``. Since :func:`hash` isn't
            expected to return a unique value (it just reduces the chance of
            collision), this doesn't try to increase entropy by including other
            values. The primary concern is that hashes of equal keys are
            equal, not the other way around.
        """

    def __eq__(self, other):
        """Equality comparison operation."""

    def __ne__(self, other):
        """The opposite of __eq__."""

    def __lt__(self, other):
        """Less than ordering."""

    def __le__(self, other):
        """Less than or equal ordering."""

    def __gt__(self, other):
        """Greater than ordering."""

    def __ge__(self, other):
        """Greater than or equal ordering."""

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method is provided for backwards compatibility, though it
            isn't needed.

        Returns:
            Tuple[Dict[str, Any]]: A tuple containing a single dictionary of
            state to pickle. The dictionary has four keys: ``pairs``, ``app``,
            ``database`` and ``namespace``.
        """

    def parent(self):
        """Parent key constructed from all but the last ``(kind, id)`` pairs.

        If there is only one ``(kind, id)`` pair, return :data:`None`.

        .. doctest:: key-parent

            >>> key = ndb.Key(
            ...     pairs=[
            ...         ("Purchase", "Food"),
            ...         ("Type", "Drink"),
            ...         ("Coffee", 11),
            ...     ]
            ... )
            >>> parent = key.parent()
            >>> parent
            Key('Purchase', 'Food', 'Type', 'Drink')
            >>>
            >>> grandparent = parent.parent()
            >>> grandparent
            Key('Purchase', 'Food')
            >>>
            >>> grandparent.parent() is None
            True
        """

    def root(self):
        """The root key.

        This is either the current key or the highest parent.

        .. doctest:: key-root

            >>> key = ndb.Key("a", 1, "steak", "sauce")
            >>> root_key = key.root()
            >>> root_key
            Key('a', 1)
            >>> root_key.root() is root_key
            True
        """

    def namespace(self):
        """The namespace for the key, if set.

        .. doctest:: key-namespace

            >>> key = ndb.Key("A", "B")
            >>> key.namespace() is None
            True
            >>>
            >>> key = ndb.Key("A", "B", namespace="rock")
            >>> key.namespace()
            'rock'
        """

    def project(self):
        """The project ID for the key.

        .. warning::

            This **may** differ from the original ``app`` passed in to the
            constructor. This is because prefixed application IDs like
            ``s~example`` are "legacy" identifiers from Google App Engine.
            They have been replaced by equivalent project IDs, e.g. here it
            would be ``example``.

        .. doctest:: key-app

            >>> key = ndb.Key("A", "B", project="s~example")
            >>> key.project()
            'example'
            >>>
            >>> key = ndb.Key("A", "B", project="example")
            >>> key.project()
            'example'
        """
    app: Any
    def database(self) -> str | None:
        """The database ID for the key.

        .. doctest:: key-database

           >>> key = ndb.Key("A", "B", database="mydb")
           >>> key.database()
           'mydb'
        """

    def id(self):
        """The string or integer ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.id()
            37
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.id()
            'B'
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.id() is None
            True
        """

    def string_id(self):
        """The string ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-string-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.string_id() is None
            True
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.string_id()
            'B'
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.string_id() is None
            True
        """

    def integer_id(self):
        """The integer ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-integer-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.integer_id()
            37
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.integer_id() is None
            True
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.integer_id() is None
            True
        """

    def pairs(self):
        """The ``(kind, id)`` pairs for the key.

        .. doctest:: key-pairs

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.pairs()
            (('Satellite', 'Moon'), ('Space', 'Dust'))
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.pairs()
            (('Known', None),)
        """

    def flat(self):
        """The flat path for the key.

        .. doctest:: key-flat

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.flat()
            ('Satellite', 'Moon', 'Space', 'Dust')
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.flat()
            ('Known', None)
        """

    def kind(self):
        """The kind of the entity referenced.

        This comes from the last ``(kind, id)`` pair.

        .. doctest:: key-kind

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.kind()
            'Space'
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.kind()
            'Known'
        """

    def reference(self):
        """The ``Reference`` protobuf object for this key.

        The return value will be stored on the current key, so the caller
        promises not to mutate it.

        .. doctest:: key-reference

            >>> key = ndb.Key("Trampoline", 88, project="xy", database="wv", namespace="zt")
            >>> key.reference()
            app: "xy"
            path {
              element {
                type: "Trampoline"
                id: 88
              }
            }
            name_space: "zt"
            database_id: "wv"
            <BLANKLINE>
        """

    def serialized(self):
        """A ``Reference`` protobuf serialized to bytes.

        .. doctest:: key-serialized

            >>> key = ndb.Key("Kind", 1337, project="example", database="example-db")
            >>> key.serialized()
            b'j\\x07exampler\\x0b\\x0b\\x12\\x04Kind\\x18\\xb9\\n\\x0c\\xba\\x01\\nexample-db'
        """

    def urlsafe(self):
        """A ``Reference`` protobuf serialized and encoded as urlsafe base 64.

        .. doctest:: key-urlsafe

            >>> key = ndb.Key("Kind", 1337, project="example")
            >>> key.urlsafe()
            b'agdleGFtcGxlcgsLEgRLaW5kGLkKDA'
        """

    def to_legacy_urlsafe(self, location_prefix):
        """
        A urlsafe serialized ``Reference`` protobuf with an App Engine prefix.

        This will produce a urlsafe string which includes an App Engine
        location prefix ("partition"), compatible with the Google Datastore
        admin console.

        This only supports the default database. For a named database,
        please use urlsafe() instead.

        Arguments:
            location_prefix (str): A location prefix ("partition") to be
                prepended to the key's `project` when serializing the key. A
                typical value is "s~", but "e~" or other partitions are
                possible depending on the project's region and other factors.

        .. doctest:: key-legacy-urlsafe

            >>> key = ndb.Key("Kind", 1337, project="example")
            >>> key.to_legacy_urlsafe("s~")
            b'aglzfmV4YW1wbGVyCwsSBEtpbmQYuQoM'
        """

    def get(
        self,
        read_consistency: Incomplete | None = ...,
        read_policy: Incomplete | None = ...,
        transaction: Incomplete | None = ...,
        retries: Incomplete | None = ...,
        timeout: Incomplete | None = ...,
        deadline: Incomplete | None = ...,
        use_cache: Incomplete | None = ...,
        use_global_cache: Incomplete | None = ...,
        use_datastore: Incomplete | None = ...,
        global_cache_timeout: Incomplete | None = ...,
        use_memcache: Incomplete | None = ...,
        memcache_timeout: Incomplete | None = ...,
        max_memcache_items: Incomplete | None = ...,
        force_writes: Incomplete | None = ...,
        _options: Incomplete | None = ...,
    ):
        """Synchronously get the entity for this key.

        Returns the retrieved :class:`.Model` or :data:`None` if there is no
        such entity.

        Args:
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
            Union[:class:`.Model`, :data:`None`]
        """

    def get_async(
        self,
        read_consistency: Incomplete | None = ...,
        read_policy: Incomplete | None = ...,
        transaction: Incomplete | None = ...,
        retries: Incomplete | None = ...,
        timeout: Incomplete | None = ...,
        deadline: Incomplete | None = ...,
        use_cache: Incomplete | None = ...,
        use_global_cache: Incomplete | None = ...,
        use_datastore: Incomplete | None = ...,
        global_cache_timeout: Incomplete | None = ...,
        use_memcache: Incomplete | None = ...,
        memcache_timeout: Incomplete | None = ...,
        max_memcache_items: Incomplete | None = ...,
        force_writes: Incomplete | None = ...,
        _options: Incomplete | None = ...,
    ):
        """Asynchronously get the entity for this key.

        The result for the returned future will either be the retrieved
        :class:`.Model` or :data:`None` if there is no such entity.

        Args:
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
            :class:`~google.cloud.ndb.tasklets.Future`
        """

    def delete(
        self,
        retries: Incomplete | None = ...,
        timeout: Incomplete | None = ...,
        deadline: Incomplete | None = ...,
        use_cache: Incomplete | None = ...,
        use_global_cache: Incomplete | None = ...,
        use_datastore: Incomplete | None = ...,
        global_cache_timeout: Incomplete | None = ...,
        use_memcache: Incomplete | None = ...,
        memcache_timeout: Incomplete | None = ...,
        max_memcache_items: Incomplete | None = ...,
        force_writes: Incomplete | None = ...,
        _options: Incomplete | None = ...,
    ):
        """Synchronously delete the entity for this key.

        This is a no-op if no such entity exists.

        Note:
            If in a transaction, the entity can only be deleted at transaction
            commit time. In that case, this function will schedule the entity
            to be deleted as part of the transaction and will return
            immediately, which is effectively the same as calling
            :meth:`delete_async` and ignoring the returned future. If not in a
            transaction, this function will block synchronously until the
            entity is deleted, as one would expect.

        Args:
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
        """

    def delete_async(
        self,
        retries: Incomplete | None = ...,
        timeout: Incomplete | None = ...,
        deadline: Incomplete | None = ...,
        use_cache: Incomplete | None = ...,
        use_global_cache: Incomplete | None = ...,
        use_datastore: Incomplete | None = ...,
        global_cache_timeout: Incomplete | None = ...,
        use_memcache: Incomplete | None = ...,
        memcache_timeout: Incomplete | None = ...,
        max_memcache_items: Incomplete | None = ...,
        force_writes: Incomplete | None = ...,
        _options: Incomplete | None = ...,
    ):
        """Schedule deletion of the entity for this key.

        The result of the returned future becomes available once the
        deletion is complete. In all cases the future's result is :data:`None`
        (i.e. there is no way to tell whether the entity existed or not).

        Args:
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
        """

    @classmethod
    def from_old_key(cls, old_key) -> None:
        """Factory constructor to convert from an "old"-style datastore key.

        The ``old_key`` was expected to be a ``google.appengine.ext.db.Key``
        (which was an alias for ``google.appengine.api.datastore_types.Key``).

        However, the ``google.appengine.ext.db`` module was part of the legacy
        Google App Engine runtime and is not generally available.

        Raises:
            NotImplementedError: Always.
        """

    def to_old_key(self) -> None:
        """Convert to an "old"-style datastore key.

        See :meth:`from_old_key` for more information on why this method
        is not supported.

        Raises:
            NotImplementedError: Always.
        """
