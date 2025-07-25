from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["edge_betweenness_partition", "edge_current_flow_betweenness_partition"]

@_dispatchable
def edge_betweenness_partition(G: Graph[_Node], number_of_sets: int, *, weight: str | None = None) -> list[Incomplete]:
    """Partition created by iteratively removing the highest edge betweenness edge.

    This algorithm works by calculating the edge betweenness for all
    edges and removing the edge with the highest value. It is then
    determined whether the graph has been broken into at least
    `number_of_sets` connected components.
    If not the process is repeated.

    Parameters
    ----------
    G : NetworkX Graph, DiGraph or MultiGraph
      Graph to be partitioned

    number_of_sets : int
      Number of sets in the desired partition of the graph

    weight : key, optional, default=None
      The key to use if using weights for edge betweenness calculation

    Returns
    -------
    C : list of sets
      Partition of the nodes of G

    Raises
    ------
    NetworkXError
      If number_of_sets is <= 0 or if number_of_sets > len(G)

    Examples
    --------
    >>> G = nx.karate_club_graph()
    >>> part = nx.community.edge_betweenness_partition(G, 2)
    >>> {0, 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 19, 21} in part
    True
    >>> {
    ...     2,
    ...     8,
    ...     9,
    ...     14,
    ...     15,
    ...     18,
    ...     20,
    ...     22,
    ...     23,
    ...     24,
    ...     25,
    ...     26,
    ...     27,
    ...     28,
    ...     29,
    ...     30,
    ...     31,
    ...     32,
    ...     33,
    ... } in part
    True

    See Also
    --------
    edge_current_flow_betweenness_partition

    Notes
    -----
    This algorithm is fairly slow, as both the calculation of connected
    components and edge betweenness relies on all pairs shortest
    path algorithms. They could potentially be combined to cut down
    on overall computation time.

    References
    ----------
    .. [1] Santo Fortunato 'Community Detection in Graphs' Physical Reports
       Volume 486, Issue 3-5 p. 75-174
       http://arxiv.org/abs/0906.0612
    """

@_dispatchable
def edge_current_flow_betweenness_partition(
    G: Graph[_Node], number_of_sets: int, *, weight: str | None = None
) -> list[Incomplete]:
    """Partition created by removing the highest edge current flow betweenness edge.

    This algorithm works by calculating the edge current flow
    betweenness for all edges and removing the edge with the
    highest value. It is then determined whether the graph has
    been broken into at least `number_of_sets` connected
    components. If not the process is repeated.

    Parameters
    ----------
    G : NetworkX Graph, DiGraph or MultiGraph
      Graph to be partitioned

    number_of_sets : int
      Number of sets in the desired partition of the graph

    weight : key, optional (default=None)
      The edge attribute key to use as weights for
      edge current flow betweenness calculations

    Returns
    -------
    C : list of sets
      Partition of G

    Raises
    ------
    NetworkXError
      If number_of_sets is <= 0 or number_of_sets > len(G)

    Examples
    --------
    >>> G = nx.karate_club_graph()
    >>> part = nx.community.edge_current_flow_betweenness_partition(G, 2)
    >>> {0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 16, 17, 19, 21} in part
    True
    >>> {8, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33} in part
    True


    See Also
    --------
    edge_betweenness_partition

    Notes
    -----
    This algorithm is extremely slow, as the recalculation of the edge
    current flow betweenness is extremely slow.

    References
    ----------
    .. [1] Santo Fortunato 'Community Detection in Graphs' Physical Reports
       Volume 486, Issue 3-5 p. 75-174
       http://arxiv.org/abs/0906.0612
    """
