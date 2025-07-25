"""
Time Series Graphs
"""

from networkx.utils.backends import _dispatchable

__all__ = ["visibility_graph"]

@_dispatchable
def visibility_graph(series):
    """
    Return a Visibility Graph of an input Time Series.

    A visibility graph converts a time series into a graph. The constructed graph
    uses integer nodes to indicate which event in the series the node represents.
    Edges are formed as follows: consider a bar plot of the series and view that
    as a side view of a landscape with a node at the top of each bar. An edge
    means that the nodes can be connected by a straight "line-of-sight" without
    being obscured by any bars between the nodes.

    The resulting graph inherits several properties of the series in its structure.
    Thereby, periodic series convert into regular graphs, random series convert
    into random graphs, and fractal series convert into scale-free networks [1]_.

    Parameters
    ----------
    series : Sequence[Number]
       A Time Series sequence (iterable and sliceable) of numeric values
       representing times.

    Returns
    -------
    NetworkX Graph
        The Visibility Graph of the input series

    Examples
    --------
    >>> series_list = [range(10), [2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3]]
    >>> for s in series_list:
    ...     g = nx.visibility_graph(s)
    ...     print(g)
    Graph with 10 nodes and 9 edges
    Graph with 12 nodes and 18 edges

    References
    ----------
    .. [1] Lacasa, Lucas, Bartolo Luque, Fernando Ballesteros, Jordi Luque, and Juan Carlos Nuno.
           "From time series to complex networks: The visibility graph." Proceedings of the
           National Academy of Sciences 105, no. 13 (2008): 4972-4975.
           https://www.pnas.org/doi/10.1073/pnas.0709247105
    """
