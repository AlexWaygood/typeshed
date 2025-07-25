from networkx.utils.backends import _dispatchable

__all__ = ["node_link_data", "node_link_graph"]

def node_link_data(
    G,
    *,
    source: str = "source",
    target: str = "target",
    name: str = "id",
    key: str = "key",
    edges: str | None = None,
    nodes: str = "nodes",
    link: str | None = None,
):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in JavaScript documents.

    Parameters
    ----------
    G : NetworkX graph
    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    edges : string
        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.
    nodes : string
        A string that provides the 'nodes' attribute name for storing NetworkX-internal graph data.
    link : string
        .. deprecated:: 3.4

           The `link` argument is deprecated and will be removed in version `3.6`.
           Use the `edges` keyword instead.

        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If the values of 'source', 'target' and 'key' are not unique.

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.Graph([("A", "B")])
    >>> data1 = nx.node_link_data(G, edges="edges")
    >>> pprint(data1)
    {'directed': False,
     'edges': [{'source': 'A', 'target': 'B'}],
     'graph': {},
     'multigraph': False,
     'nodes': [{'id': 'A'}, {'id': 'B'}]}

    To serialize with JSON

    >>> import json
    >>> s1 = json.dumps(data1)
    >>> pprint(s1)
    ('{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, '
     '{"id": "B"}], "edges": [{"source": "A", "target": "B"}]}')


    A graph can also be serialized by passing `node_link_data` as an encoder function.

    >>> s1 = json.dumps(G, default=nx.node_link_data)
    >>> pprint(s1)
    ('{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, '
     '{"id": "B"}], "links": [{"source": "A", "target": "B"}]}')

    The attribute names for storing NetworkX-internal graph data can
    be specified as keyword options.

    >>> H = nx.gn_graph(2)
    >>> data2 = nx.node_link_data(
    ...     H, edges="links", source="from", target="to", nodes="vertices"
    ... )
    >>> pprint(data2)
    {'directed': True,
     'graph': {},
     'links': [{'from': 1, 'to': 0}],
     'multigraph': False,
     'vertices': [{'id': 0}, {'id': 1}]}

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.

    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.

    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """

@_dispatchable
def node_link_graph(
    data,
    directed: bool = False,
    multigraph: bool = True,
    attrs=None,
    *,
    source: str = "source",
    target: str = "target",
    name: str = "id",
    key: str = "key",
    edges: str | None = None,
    nodes: str = "nodes",
    link: str | None = None,
):
    """Returns graph from node-link data format.

    Useful for de-serialization from JSON.

    Parameters
    ----------
    data : dict
        node-link formatted graph data

    directed : bool
        If True, and direction not specified in data, return a directed graph.

    multigraph : bool
        If True, and multigraph not specified in data, return a multigraph.

    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    edges : string
        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.
    nodes : string
        A string that provides the 'nodes' attribute name for storing NetworkX-internal graph data.
    link : string
        .. deprecated:: 3.4

           The `link` argument is deprecated and will be removed in version `3.6`.
           Use the `edges` keyword instead.

        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    G : NetworkX graph
        A NetworkX graph object

    Examples
    --------

    Create data in node-link format by converting a graph.

    >>> from pprint import pprint
    >>> G = nx.Graph([("A", "B")])
    >>> data = nx.node_link_data(G, edges="edges")
    >>> pprint(data)
    {'directed': False,
     'edges': [{'source': 'A', 'target': 'B'}],
     'graph': {},
     'multigraph': False,
     'nodes': [{'id': 'A'}, {'id': 'B'}]}

    Revert data in node-link format to a graph.

    >>> H = nx.node_link_graph(data, edges="edges")
    >>> print(H.edges)
    [('A', 'B')]

    To serialize and deserialize a graph with JSON,

    >>> import json
    >>> d = json.dumps(nx.node_link_data(G, edges="edges"))
    >>> H = nx.node_link_graph(json.loads(d), edges="edges")
    >>> print(G.edges, H.edges)
    [('A', 'B')] [('A', 'B')]


    Notes
    -----
    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.

    See Also
    --------
    node_link_data, adjacency_data, tree_data
    """
