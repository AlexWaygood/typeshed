from _typeshed import Incomplete
from collections.abc import Iterable

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["average_degree_connectivity"]

@_dispatchable
def average_degree_connectivity(
    G: Graph[_Node], source="in+out", target="in+out", nodes: Iterable[Incomplete] | None = None, weight: str | None = None
) -> dict[Incomplete, int | float]:
    """Compute the average degree connectivity of graph.

    The average degree connectivity is the average nearest neighbor degree of
    nodes with degree k. For weighted graphs, an analogous measure can
    be computed using the weighted average neighbors degree defined in
    [1]_, for a node `i`, as

    .. math::

        k_{nn,i}^{w} = \\frac{1}{s_i} \\sum_{j \\in N(i)} w_{ij} k_j

    where `s_i` is the weighted degree of node `i`,
    `w_{ij}` is the weight of the edge that links `i` and `j`,
    and `N(i)` are the neighbors of node `i`.

    Parameters
    ----------
    G : NetworkX graph

    source :  "in"|"out"|"in+out" (default:"in+out")
       Directed graphs only. Use "in"- or "out"-degree for source node.

    target : "in"|"out"|"in+out" (default:"in+out"
       Directed graphs only. Use "in"- or "out"-degree for target node.

    nodes : list or iterable (optional)
        Compute neighbor connectivity for these nodes. The default is all
        nodes.

    weight : string or None, optional (default=None)
       The edge attribute that holds the numerical value used as a weight.
       If None, then each edge has weight 1.

    Returns
    -------
    d : dict
       A dictionary keyed by degree k with the value of average connectivity.

    Raises
    ------
    NetworkXError
        If either `source` or `target` are not one of 'in',
        'out', or 'in+out'.
        If either `source` or `target` is passed for an undirected graph.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> G.edges[1, 2]["weight"] = 3
    >>> nx.average_degree_connectivity(G)
    {1: 2.0, 2: 1.5}
    >>> nx.average_degree_connectivity(G, weight="weight")
    {1: 2.0, 2: 1.75}

    See Also
    --------
    average_neighbor_degree

    References
    ----------
    .. [1] A. Barrat, M. Barthélemy, R. Pastor-Satorras, and A. Vespignani,
       "The architecture of complex weighted networks".
       PNAS 101 (11): 3747–3752 (2004).
    """
