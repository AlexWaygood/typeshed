from typing import Any

from networkx.utils.backends import _dispatchable

__all__ = ["cytoscape_data", "cytoscape_graph"]

# Any: Complex type union
def cytoscape_data(G, name: str = "name", ident: str = "id") -> dict[str, Any]:
    """Returns data in Cytoscape JSON format (cyjs).

    Parameters
    ----------
    G : NetworkX Graph
        The graph to convert to cytoscape format
    name : string
        A string which is mapped to the 'name' node element in cyjs format.
        Must not have the same value as `ident`.
    ident : string
        A string which is mapped to the 'id' node element in cyjs format.
        Must not have the same value as `name`.

    Returns
    -------
    data: dict
        A dictionary with cyjs formatted data.

    Raises
    ------
    NetworkXError
        If the values for `name` and `ident` are identical.

    See Also
    --------
    cytoscape_graph: convert a dictionary in cyjs format to a graph

    References
    ----------
    .. [1] Cytoscape user's manual:
       http://manual.cytoscape.org/en/stable/index.html

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(2)
    >>> cyto_data = nx.cytoscape_data(G)
    >>> pprint(cyto_data, sort_dicts=False)
    {'data': [],
     'directed': False,
     'multigraph': False,
     'elements': {'nodes': [{'data': {'id': '0', 'value': 0, 'name': '0'}},
                            {'data': {'id': '1', 'value': 1, 'name': '1'}}],
                  'edges': [{'data': {'source': 0, 'target': 1}}]}}

    The :mod:`json` package can be used to serialize the resulting data

    >>> import io, json
    >>> with io.StringIO() as fh:  # replace io with `open(...)` to write to disk
    ...     json.dump(cyto_data, fh)
    ...     fh.seek(0)  # doctest: +SKIP
    ...     print(fh.getvalue()[:64])  # View the first 64 characters
    {"data": [], "directed": false, "multigraph": false, "elements":

    """

@_dispatchable
def cytoscape_graph(data, name: str = "name", ident: str = "id"):
    """
    Create a NetworkX graph from a dictionary in cytoscape JSON format.

    Parameters
    ----------
    data : dict
        A dictionary of data conforming to cytoscape JSON format.
    name : string
        A string which is mapped to the 'name' node element in cyjs format.
        Must not have the same value as `ident`.
    ident : string
        A string which is mapped to the 'id' node element in cyjs format.
        Must not have the same value as `name`.

    Returns
    -------
    graph : a NetworkX graph instance
        The `graph` can be an instance of `Graph`, `DiGraph`, `MultiGraph`, or
        `MultiDiGraph` depending on the input data.

    Raises
    ------
    NetworkXError
        If the `name` and `ident` attributes are identical.

    See Also
    --------
    cytoscape_data: convert a NetworkX graph to a dict in cyjs format

    References
    ----------
    .. [1] Cytoscape user's manual:
       http://manual.cytoscape.org/en/stable/index.html

    Examples
    --------
    >>> data_dict = {
    ...     "data": [],
    ...     "directed": False,
    ...     "multigraph": False,
    ...     "elements": {
    ...         "nodes": [
    ...             {"data": {"id": "0", "value": 0, "name": "0"}},
    ...             {"data": {"id": "1", "value": 1, "name": "1"}},
    ...         ],
    ...         "edges": [{"data": {"source": 0, "target": 1}}],
    ...     },
    ... }
    >>> G = nx.cytoscape_graph(data_dict)
    >>> G.name
    ''
    >>> G.nodes()
    NodeView((0, 1))
    >>> G.nodes(data=True)[0]
    {'id': '0', 'value': 0, 'name': '0'}
    >>> G.edges(data=True)
    EdgeDataView([(0, 1, {'source': 0, 'target': 1})])
    """
