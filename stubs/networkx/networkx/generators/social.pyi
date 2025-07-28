"""
Famous social networks.
"""

from networkx.utils.backends import _dispatchable

__all__ = ["karate_club_graph", "davis_southern_women_graph", "florentine_families_graph", "les_miserables_graph"]

@_dispatchable
def karate_club_graph():
    """Returns Zachary's Karate Club graph.

    Each node in the returned graph has a node attribute 'club' that
    indicates the name of the club to which the member represented by that node
    belongs, either 'Mr. Hi' or 'Officer'. Each edge has a weight based on the
    number of contexts in which that edge's incident node members interacted.

    The dataset is derived from the 'Club After Split From Data' column of Table 3 in [1]_.
    This was in turn derived from the 'Club After Fission' column of Table 1 in the
    same paper. Note that the nodes are 0-indexed in NetworkX, but 1-indexed in the
    paper (the 'Individual Number in Matrix C' column of Table 3 starts at 1). This
    means, for example, that ``G.nodes[9]["club"]`` returns 'Officer', which
    corresponds to row 10 of Table 3 in the paper.

    Examples
    --------
    To get the name of the club to which a node belongs::

        >>> G = nx.karate_club_graph()
        >>> G.nodes[5]["club"]
        'Mr. Hi'
        >>> G.nodes[9]["club"]
        'Officer'

    References
    ----------
    .. [1] Zachary, Wayne W.
       "An Information Flow Model for Conflict and Fission in Small Groups."
       *Journal of Anthropological Research*, 33, 452--473, (1977).
    """

@_dispatchable
def davis_southern_women_graph():
    """Returns Davis Southern women social network.

    This is a bipartite graph.

    References
    ----------
    .. [1] A. Davis, Gardner, B. B., Gardner, M. R., 1941. Deep South.
        University of Chicago Press, Chicago, IL.
    """

@_dispatchable
def florentine_families_graph():
    """Returns Florentine families graph.

    References
    ----------
    .. [1] Ronald L. Breiger and Philippa E. Pattison
       Cumulated social roles: The duality of persons and their algebras,1
       Social Networks, Volume 8, Issue 3, September 1986, Pages 215-256
    """

@_dispatchable
def les_miserables_graph():
    """Returns coappearance network of characters in the novel Les Miserables.

    References
    ----------
    .. [1] D. E. Knuth, 1993.
       The Stanford GraphBase: a platform for combinatorial computing,
       pp. 74-87. New York: AcM Press.
    """
