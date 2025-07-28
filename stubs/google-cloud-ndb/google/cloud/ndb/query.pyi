"""High-level wrapper for datastore queries.

The fundamental API here overloads the 6 comparison operators to represent
filters on property values, and supports AND and OR operations (implemented as
functions -- Python's 'and' and 'or' operators cannot be overloaded, and the
'&' and '|' operators have a priority that conflicts with the priority of
comparison operators).

For example::

    class Employee(Model):
        name = StringProperty()
        age = IntegerProperty()
        rank = IntegerProperty()

      @classmethod
      def demographic(cls, min_age, max_age):
          return cls.query().filter(AND(cls.age >= min_age,
                                        cls.age <= max_age))

      @classmethod
      def ranked(cls, rank):
          return cls.query(cls.rank == rank).order(cls.age)

    for emp in Employee.seniors(42, 5):
        print(emp.name, emp.age, emp.rank)

The 'in' operator cannot be overloaded, but is supported through the IN()
method. For example::

    Employee.query().filter(Employee.rank.IN([4, 5, 6]))

Sort orders are supported through the order() method; unary minus is
overloaded on the Property class to represent a descending order::

    Employee.query().order(Employee.name, -Employee.age)

Besides using AND() and OR(), filters can also be combined by repeatedly
calling .filter()::

    query1 = Employee.query()  # A query that returns all employees
    query2 = query1.filter(Employee.age >= 30)  # Only those over 30
    query3 = query2.filter(Employee.age < 40)  # Only those in their 30s

A further shortcut is calling .filter() with multiple arguments; this implies
AND()::

  query1 = Employee.query()  # A query that returns all employees
  query3 = query1.filter(Employee.age >= 30,
                         Employee.age < 40)  # Only those in their 30s

And finally you can also pass one or more filter expressions directly to the
.query() method::

  query3 = Employee.query(Employee.age >= 30,
                          Employee.age < 40)  # Only those in their 30s

Query objects are immutable, so these methods always return a new Query object;
the above calls to filter() do not affect query1. On the other hand, operations
that are effectively no-ops may return the original Query object.

Sort orders can also be combined this way, and .filter() and .order() calls may
be intermixed::

    query4 = query3.order(-Employee.age)
    query5 = query4.order(Employee.name)
    query6 = query5.filter(Employee.rank == 5)

Again, multiple .order() calls can be combined::

    query5 = query3.order(-Employee.age, Employee.name)

The simplest way to retrieve Query results is a for-loop::

    for emp in query3:
        print emp.name, emp.age

Some other methods to run a query and access its results::

    :meth:`Query.iter`() # Return an iterator; same as iter(q) but more
        flexible.
    :meth:`Query.fetch`(N) # Return a list of the first N results
    :meth:`Query.get`() # Return the first result
    :meth:`Query.count`(N) # Return the number of results, with a maximum of N
    :meth:`Query.fetch_page`(N, start_cursor=cursor) # Return (results, cursor,
        has_more)

All of the above methods take a standard set of additional query options,
in the form of keyword arguments such as keys_only=True. You can also pass
a QueryOptions object options=QueryOptions(...), but this is deprecated.

The most important query options are:

- keys_only: bool, if set the results are keys instead of entities.
- limit: int, limits the number of results returned.
- offset: int, skips this many results first.
- start_cursor: Cursor, start returning results after this position.
- end_cursor: Cursor, stop returning results after this position.

The following query options have been deprecated or are not supported in
datastore queries:

- batch_size: int, hint for the number of results returned per RPC.
- prefetch_size: int, hint for the number of results in the first RPC.
- produce_cursors: bool, return Cursor objects with the results.

All of the above methods except for iter() have asynchronous variants as well,
which return a Future; to get the operation's ultimate result, yield the Future
(when inside a tasklet) or call the Future's get_result() method (outside a
tasklet)::

    :meth:`Query.fetch_async`(N)
    :meth:`Query.get_async`()
    :meth:`Query.count_async`(N)
    :meth:`Query.fetch_page_async`(N, start_cursor=cursor)

Finally, there's an idiom to efficiently loop over the Query results in a
tasklet, properly yielding when appropriate::

    it = query1.iter()
    while (yield it.has_next_async()):
        emp = it.next()
        print(emp.name, emp.age)
"""

from _typeshed import Incomplete
from typing import Any

from google.cloud.ndb import _options

class PropertyOrder:
    """The sort order for a property name, to be used when ordering the
    results of a query.

    Args:
        name (str): The name of the model property to use for ordering.
        reverse (bool): Whether to reverse the sort order (descending)
            or not (ascending). Default is False.
    """

    name: Any
    reverse: Any
    def __init__(self, name, reverse: bool = ...) -> None: ...
    def __neg__(self): ...

class RepeatedStructuredPropertyPredicate:
    """A predicate for querying repeated structured properties.

    Called by ``model.StructuredProperty._compare``. This is used to handle
    queries of the form::

        Squad.query(Squad.members == Member(name="Joe", age=24, rank=5))

    This query should find any squad with a member named "Joe" whose age is 24
    and rank is 5.

    Datastore, on its own, can find all squads with a team member named Joe, or
    a team member whose age is 24, or whose rank is 5, but it can't be queried
    for all 3 in a single subentity. This predicate must be applied client
    side, therefore, to limit results to entities where all the keys match for
    a single subentity.

    Arguments:
        name (str): Name of the repeated structured property being queried
            (e.g. "members").
        match_keys (list[str]): Property names to check on the subentities
            being queried (e.g. ["name", "age", "rank"]).
        entity_pb (google.cloud.datastore_v1.proto.entity_pb2.Entity): A
            partial entity protocol buffer containing the values that must
            match in a subentity of the repeated structured property. Should
            contain a value for each key in ``match_keys``.
    """

    name: Any
    match_keys: Any
    match_values: Any
    def __init__(self, name, match_keys, entity_pb) -> None: ...
    def __call__(self, entity_pb): ...

class ParameterizedThing:
    """Base class for :class:`Parameter` and :class:`ParameterizedFunction`.

    This exists purely for :func:`isinstance` checks.
    """

    def __eq__(self, other): ...
    def __ne__(self, other): ...

class Parameter(ParameterizedThing):
    """Represents a bound variable in a GQL query.

    ``Parameter(1)`` corresponds to a slot labeled ``:1`` in a GQL query.
    ``Parameter('something')`` corresponds to a slot labeled ``:something``.

    The value must be set (bound) separately.

    Args:
        key (Union[str, int]): The parameter key.

    Raises:
        TypeError: If the ``key`` is not a string or integer.
    """

    def __init__(self, key) -> None: ...
    def __eq__(self, other): ...
    @property
    def key(self):
        """Retrieve the key."""

    def resolve(self, bindings, used):
        """Resolve the current parameter from the parameter bindings.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified if the current parameter
                is in ``bindings``.

        Returns:
            Any: The bound value for the current parameter.

        Raises:
            exceptions.BadArgumentError: If the current parameter is not in ``bindings``.
        """

class ParameterizedFunction(ParameterizedThing):
    """Represents a GQL function with parameterized arguments.

    For example, ParameterizedFunction('key', [Parameter(1)]) stands for
    the GQL syntax KEY(:1).
    """

    func: Any
    values: Any
    def __init__(self, func, values) -> None: ...
    def __eq__(self, other): ...
    def is_parameterized(self): ...
    def resolve(self, bindings, used): ...

class Node:
    """Base class for filter expression tree nodes.

    Tree nodes are considered immutable, even though they can contain
    Parameter instances, which are not. In particular, two identical
    trees may be represented by the same Node object in different
    contexts.

    Raises:
        TypeError: Always, only subclasses are allowed.
    """

    def __new__(cls): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __le__(self, unused_other): ...
    def __lt__(self, unused_other): ...
    def __ge__(self, unused_other): ...
    def __gt__(self, unused_other): ...
    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        .. note::

            Both ``bindings`` and ``used`` are unused by this base class
            implementation.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified if the current parameter
                is in ``bindings``.

        Returns:
            Node: The current node.
        """

class FalseNode(Node):
    """Tree node for an always-failing filter."""

    def __eq__(self, other):
        """Equality check.

        An instance will always equal another :class:`FalseNode` instance. This
        is because they hold no state.
        """

class ParameterNode(Node):
    """Tree node for a parameterized filter.

    Args:
        prop (~google.cloud.ndb.model.Property): A property describing a value
            type.
        op (str): The comparison operator. One of ``=``, ``!=``, ``<``, ``<=``,
            ``>``, ``>=`` or ``in``.
        param (ParameterizedThing): The parameter corresponding to the node.

    Raises:
        TypeError: If ``prop`` is not a
            :class:`~google.cloud.ndb.model.Property`.
        TypeError: If ``op`` is not one of the accepted operators.
        TypeError: If ``param`` is not a :class:`.Parameter` or
            :class:`.ParameterizedFunction`.
    """

    def __new__(cls, prop, op, param): ...
    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[~google.cloud.ndb.model.Property, str, ParameterizedThing]:
            A tuple containing the internal state: the property, operation and
            parameter.
        """

    def __eq__(self, other): ...
    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters.

        Returns:
            Union[~google.cloud.ndb.query.DisjunctionNode,                 ~google.cloud.ndb.query.FilterNode,                 ~google.cloud.ndb.query.FalseNode]: A node corresponding to
            the value substituted.
        """

class FilterNode(Node):
    """Tree node for a single filter expression.

    For example ``FilterNode("a", ">", 3)`` filters for entities where the
    value ``a`` is greater than ``3``.

    .. warning::

        The constructor for this type may not always return a
        :class:`FilterNode`. For example:

        * The filter ``name in (value1, ..., valueN)`` is converted into
          ``(name = value1) OR ... OR (name = valueN)`` (also a
          :class:`DisjunctionNode`)
        * The filter ``name in ()`` (i.e. a property is among an empty list
          of values) is converted into a :class:`FalseNode`
        * The filter ``name in (value1,)`` (i.e. a list with one element) is
          converted into ``name = value1``, a related :class:`FilterNode`
          with a different ``opsymbol`` and ``value`` than what was passed
          to the constructor

    Args:
        name (str): The name of the property being filtered.
        opsymbol (str): The comparison operator. One of ``=``, ``!=``, ``<``,
            ``<=``, ``>``, ``>=`` or ``in``.
        value (Any): The value to filter on / relative to.
        server_op (bool): Force the operator to use a server side filter.

    Raises:
        TypeError: If ``opsymbol`` is ``"in"`` but ``value`` is not a
            basic container (:class:`list`, :class:`tuple`, :class:`set` or
            :class:`frozenset`)
    """

    def __new__(cls, name, opsymbol, value, server_op: bool = False): ...
    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[str, str, Any]: A tuple containing the
            internal state: the name, ``opsymbol`` and value.
        """

    def __eq__(self, other): ...

class PostFilterNode(Node):
    """Tree node representing an in-memory filtering operation.

    This is used to represent filters that cannot be executed by the
    datastore, for example a query for a structured value.

    Args:
        predicate (Callable[[Any], bool]): A filter predicate that
            takes a datastore entity (typically as a protobuf) and
            returns :data:`True` or :data:`False` if the entity matches
            the given filter.
    """

    def __new__(cls, predicate): ...
    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Callable[[Any], bool],]: A tuple containing a single value,
            the ``predicate`` attached to this node.
        """

    def __eq__(self, other): ...

class _BooleanClauses:
    """This type will be used for symbolically performing boolean operations.

    Internally, the state will track a symbolic expression like::

        A or (B and C) or (A and D)

    as a list of the ``OR`` components::

        [A, B and C, A and D]

    When ``combine_or=False``, it will track ``AND`` statements as a list,
    making the final simplified form of our example::

        [[A], [B, C], [A, D]]

    Via :meth:`add_node`, we will ensure that new nodes will be correctly
    combined (via ``AND`` or ``OR``) with the current expression.

    Args:
        name (str): The name of the class that is tracking a
            boolean expression.
        combine_or (bool): Indicates if new nodes will be combined
            with the current boolean expression via ``AND`` or ``OR``.
    """

    name: Any
    combine_or: Any
    or_parts: Any
    def __init__(self, name, combine_or) -> None: ...
    def add_node(self, node) -> None:
        """Update the current boolean expression.

        This uses the distributive law for sets to combine as follows:

        - ``(A or B or C or ...) or  D`` -> ``A or B or C or ... or D``
        - ``(A or B or C or ...) and D`` ->
          ``(A and D) or (B and D) or (C and D) or ...``

        Args:
            node (Node): A node to add to the list of clauses.

        Raises:
            TypeError: If ``node`` is not a :class:`.Node`.
        """

class ConjunctionNode(Node):
    """Tree node representing a boolean ``AND`` operator on multiple nodes.

    .. warning::

        The constructor for this type may not always return a
        :class:`ConjunctionNode`. For example:

        * If the passed in ``nodes`` has only one entry, that single node
          will be returned by the constructor
        * If the resulting boolean expression has an ``OR`` in it, then a
          :class:`DisjunctionNode` will be returned; e.g.
          ``AND(OR(A, B), C)`` becomes ``OR(AND(A, C), AND(B, C))``

    Args:
        nodes (Tuple[Node, ...]): A list of nodes to be joined.

    Raises:
        TypeError: If ``nodes`` is empty.
        RuntimeError: If the ``nodes`` combine to an "empty" boolean
            expression.
    """

    def __new__(cls, *nodes): ...
    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Node, ...]: The list of stored nodes, converted to a
            :class:`tuple`.
        """

    def __iter__(self): ...
    def __eq__(self, other): ...
    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified for each parameter found
                in ``bindings``.

        Returns:
            Node: The current node, if all nodes are already resolved.
            Otherwise returns a modified :class:`ConjunctionNode` with
            each individual node resolved.
        """

class DisjunctionNode(Node):
    """Tree node representing a boolean ``OR`` operator on multiple nodes.

    .. warning::

        This constructor may not always return a :class:`DisjunctionNode`.
        If the passed in ``nodes`` has only one entry, that single node
        will be returned by the constructor.

    Args:
        nodes (Tuple[Node, ...]): A list of nodes to be joined.

    Raises:
        TypeError: If ``nodes`` is empty.
    """

    def __new__(cls, *nodes): ...
    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Node, ...]: The list of stored nodes, converted to a
            :class:`tuple`.
        """

    def __iter__(self): ...
    def __eq__(self, other): ...
    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified for each parameter found
                in ``bindings``.

        Returns:
            Node: The current node, if all nodes are already resolved.
            Otherwise returns a modified :class:`DisjunctionNode` with
            each individual node resolved.
        """

AND = ConjunctionNode
OR = DisjunctionNode

class QueryOptions(_options.ReadOptions):
    project: Any
    namespace: Any
    database: str | None
    def __init__(self, config: Incomplete | None = ..., context: Incomplete | None = ..., **kwargs) -> None: ...

class Query:
    """Query object.

    Args:
        kind (str): The kind of entities to be queried.
        filters (FilterNode): Node representing a filter expression tree.
        ancestor (key.Key): Entities returned will be descendants of
            `ancestor`.
        order_by (list[Union[str, google.cloud.ndb.model.Property]]): The
            model properties used to order query results.
        orders (list[Union[str, google.cloud.ndb.model.Property]]):
            Deprecated. Synonym for `order_by`.
        project (str): The project to perform the query in. Also known as the
            app, in Google App Engine. If not passed, uses the client's value.
        app (str): Deprecated. Synonym for `project`.
        namespace (str): The namespace to which to restrict results.
            If not passed, uses the client's value.
        projection (list[Union[str, google.cloud.ndb.model.Property]]): The
            fields to return as part of the query results.
        keys_only (bool): Return keys instead of entities.
        offset (int): Number of query results to skip.
        limit (Optional[int]): Maximum number of query results to return.
            If not specified, there is no limit.
        distinct_on (list[str]): The field names used to group query
            results.
        group_by (list[str]): Deprecated. Synonym for distinct_on.
        default_options (QueryOptions): Deprecated. QueryOptions object.
            Prefer passing explicit keyword arguments to the relevant method directly.

    Raises:
        TypeError: If any of the arguments are invalid.
    """

    default_options: Any
    kind: Any
    ancestor: Any
    filters: Any
    order_by: Any
    project: Any
    namespace: Any
    limit: Any
    offset: Any
    keys_only: Any
    projection: Any
    distinct_on: Any
    database: str | None
    def __init__(
        self,
        kind: Incomplete | None = ...,
        filters: Incomplete | None = ...,
        ancestor: Incomplete | None = ...,
        order_by: Incomplete | None = ...,
        orders: Incomplete | None = ...,
        project: Incomplete | None = ...,
        app: Incomplete | None = ...,
        namespace: Incomplete | None = ...,
        projection: Incomplete | None = ...,
        distinct_on: Incomplete | None = ...,
        group_by: Incomplete | None = ...,
        limit: Incomplete | None = ...,
        offset: Incomplete | None = ...,
        keys_only: Incomplete | None = ...,
        default_options: Incomplete | None = ...,
    ) -> None: ...
    @property
    def is_distinct(self):
        """True if results are guaranteed to contain a unique set of property
        values.

        This happens when every property in distinct_on is also in projection.
        """

    def filter(self, *filters):
        """Return a new Query with additional filter(s) applied.

        Args:
            filters (list[Node]): One or more instances of Node.

        Returns:
            Query: A new query with the new filters applied.

        Raises:
            TypeError: If one of the filters is not a Node.
        """

    def order(self, *props):
        """Return a new Query with additional sort order(s) applied.

        Args:
            props (list[Union[str, google.cloud.ndb.model.Property]]): One or
                more model properties to sort by.

        Returns:
            Query: A new query with the new order applied.
        """

    def analyze(self):
        """Return a list giving the parameters required by a query.

        When a query is created using gql, any bound parameters
        are created as ParameterNode instances. This method returns
        the names of any such parameters.

        Returns:
            list[str]: required parameter names.
        """

    def bind(self, *positional, **keyword):
        """Bind parameter values.  Returns a new Query object.

        When a query is created using gql, any bound parameters
        are created as ParameterNode instances. This method
        receives values for both positional (:1, :2, etc.) or
        keyword (:something, :other, etc.) bound parameters, then sets the
        values accordingly. This mechanism allows easy reuse of a
        parameterized query, by passing the values to bind here.

        Args:
            positional (list[Any]): One or more positional values to bind.
            keyword (dict[Any]): One or more keyword values to bind.

        Returns:
            Query: A new query with the new bound parameter values.

        Raises:
            google.cloud.ndb.exceptions.BadArgumentError: If one of
                the positional parameters is not used in the query.
        """

    def fetch(self, limit: Incomplete | None = ..., **kwargs):
        """Run a query, fetching results.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[Union[str, google.cloud.ndb.model.Property]]): The
                fields to return as part of the query results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            List[Union[model.Model, key.Key]]: The query results.
        """

    def fetch_async(self, limit: Incomplete | None = ..., **kwargs):
        """Run a query, asynchronously fetching the results.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[Union[str, google.cloud.ndb.model.Property]]): The
                fields to return as part of the query results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            tasklets.Future: Eventual result will be a List[model.Model] of the
                results.
        """

    def run_to_queue(self, queue, conn, options: Incomplete | None = ..., dsquery: Incomplete | None = ...) -> None:
        """Run this query, putting entities into the given queue."""

    def iter(self, **kwargs):
        """Get an iterator over query results.

        Args:
            keys_only (bool): Return keys instead of entities.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            :class:`QueryIterator`: An iterator.
        """
    __iter__: Any
    def map(self, callback, **kwargs):
        """Map a callback function or tasklet over the query results.

        Args:
            callback (Callable): A function or tasklet to be applied to each
                result; see below.
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.
            pass_batch_info_callback: DEPRECATED: No longer implemented.
            merge_future: DEPRECATED: No longer implemented.

        Callback signature: The callback is normally called with an entity as
        argument. However if keys_only=True is given, it is called with a Key.
        The callback can return whatever it wants.

        Returns:
            Any: When the query has run to completion and all callbacks have
                returned, map() returns a list of the results of all callbacks.
        """

    def map_async(self, callback, **kwargs) -> None:
        """Map a callback function or tasklet over the query results.

        This is the asynchronous version of :meth:`Query.map`.

        Returns:
            tasklets.Future: See :meth:`Query.map` for eventual result.
        """

    def get(self, **kwargs):
        """Get the first query result, if any.

        This is equivalent to calling ``q.fetch(1)`` and returning the first
        result, if any.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            Optional[Union[google.cloud.datastore.entity.Entity, key.Key]]:
                A single result, or :data:`None` if there are no results.
        """

    def get_async(self, **kwargs) -> None:
        """Get the first query result, if any.

        This is the asynchronous version of :meth:`Query.get`.

        Returns:
            tasklets.Future: See :meth:`Query.get` for eventual result.
        """

    def count(self, limit: Incomplete | None = ..., **kwargs):
        """Count the number of query results, up to a limit.

        This returns the same result as ``len(q.fetch(limit))``.

        Note that you should pass a maximum value to limit the amount of
        work done by the query.

        Note:
            The legacy GAE version of NDB claims this is more efficient than
            just calling ``len(q.fetch(limit))``. Since Datastore does not
            provide API for ``count``, this version ends up performing the
            fetch underneath hood. We can specify ``keys_only`` to save some
            network traffic, making this call really equivalent to
            ``len(q.fetch(limit, keys_only=True))``. We can also avoid
            marshalling NDB key objects from the returned protocol buffers, but
            this is a minor savings--most applications that use NDB will have
            their performance bound by the Datastore backend, not the CPU.
            Generally, any claim of performance improvement using this versus
            the equivalent call to ``fetch`` is exaggerated, at best.

        Args:
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            Optional[Union[google.cloud.datastore.entity.Entity, key.Key]]:
                A single result, or :data:`None` if there are no results.
        """

    def count_async(self, limit: Incomplete | None = ..., **kwargs):
        """Count the number of query results, up to a limit.

        This is the asynchronous version of :meth:`Query.count`.

        Returns:
            tasklets.Future: See :meth:`Query.count` for eventual result.
        """

    def fetch_page(self, page_size, **kwargs):
        """Fetch a page of results.

        This is a specialized method for use by paging user interfaces.

        To fetch the next page, you pass the cursor returned by one call to the
        next call using the `start_cursor` argument.  A common idiom is to pass
        the cursor to the client using :meth:`_datastore_query.Cursor.urlsafe`
        and to reconstruct that cursor on a subsequent request using the
        `urlsafe` argument to :class:`_datastore_query.Cursor`.

        NOTE:
            This method relies on cursors which are not available for queries
            that involve ``OR``, ``!=``, ``IN`` operators. This feature is not
            available for those queries.

        Args:
            page_size (int): The number of results per page. At most, this many
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            batch_size: DEPRECATED: No longer implemented.
            prefetch_size: DEPRECATED: No longer implemented.
            produce_cursors: Ignored. Cursors always produced if available.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If set then passes the explicit read consistency to
                the server.  May not be set to ``ndb.EVENTUAL`` when a transaction
                is specified.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

               results will be returned.

        Returns:
            Tuple[list, _datastore_query.Cursor, bool]: A tuple
                `(results, cursor, more)` where `results` is a list of query
                results, `cursor` is a cursor pointing just after the last
                result returned, and `more` indicates whether there are
                (likely) more results after that.
        """

    def fetch_page_async(self, page_size, **kwargs) -> None:
        """Fetch a page of results.

        This is the asynchronous version of :meth:`Query.fetch_page`.

        Returns:
            tasklets.Future: See :meth:`Query.fetch_page` for eventual result.
        """

def gql(query_string: str, *args: Any, **kwds: Any) -> Query:
    """Parse a GQL query string.

    Args:
        query_string (str): Full GQL query, e.g. 'SELECT * FROM Kind WHERE
            prop = 1 ORDER BY prop2'.
        args: If present, used to call bind().
        kwds: If present, used to call bind().

    Returns:
        Query: a query instance.

    Raises:
        google.cloud.ndb.exceptions.BadQueryError: When bad gql is passed in.
    """
