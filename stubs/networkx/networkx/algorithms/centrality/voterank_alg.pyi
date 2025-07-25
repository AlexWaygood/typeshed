"""Algorithm to select influential nodes in a graph using VoteRank."""

from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["voterank"]

@_dispatchable
def voterank(G: Graph[_Node], number_of_nodes: int | None = None) -> list[Incomplete]:
    """Select a list of influential nodes in a graph using VoteRank algorithm

    VoteRank [1]_ computes a ranking of the nodes in a graph G based on a
    voting scheme. With VoteRank, all nodes vote for each of its in-neighbors
    and the node with the highest votes is elected iteratively. The voting
    ability of out-neighbors of elected nodes is decreased in subsequent turns.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    number_of_nodes : integer, optional
        Number of ranked nodes to extract (default all nodes).

    Returns
    -------
    voterank : list
        Ordered list of computed seeds.
        Only nodes with positive number of votes are returned.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 4)])
    >>> nx.voterank(G)
    [0, 1]

    The algorithm can be used both for undirected and directed graphs.
    However, the directed version is different in two ways:
    (i) nodes only vote for their in-neighbors and
    (ii) only the voting ability of elected node and its out-neighbors are updated:

    >>> G = nx.DiGraph([(0, 1), (2, 1), (2, 3), (3, 4)])
    >>> nx.voterank(G)
    [2, 3]

    Notes
    -----
    Each edge is treated independently in case of multigraphs.

    References
    ----------
    .. [1] Zhang, J.-X. et al. (2016).
        Identifying a set of influential spreaders in complex networks.
        Sci. Rep. 6, 27823; doi: 10.1038/srep27823.
    """
