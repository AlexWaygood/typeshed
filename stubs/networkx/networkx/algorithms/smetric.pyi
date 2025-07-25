from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["s_metric"]

@_dispatchable
def s_metric(G: Graph[_Node]) -> float:
    """Returns the s-metric [1]_ of graph.

    The s-metric is defined as the sum of the products ``deg(u) * deg(v)``
    for every edge ``(u, v)`` in `G`.

    Parameters
    ----------
    G : graph
        The graph used to compute the s-metric.

    Returns
    -------
    s : float
        The s-metric of the graph.

    References
    ----------
    .. [1] Lun Li, David Alderson, John C. Doyle, and Walter Willinger,
           Towards a Theory of Scale-Free Graphs:
           Definition, Properties, and  Implications (Extended Version), 2005.
           https://arxiv.org/abs/cond-mat/0501169
    """
