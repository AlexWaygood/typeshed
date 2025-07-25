"""
An algorithm for finding if two undirected trees are isomorphic,
and if so returns an isomorphism between the two sets of nodes.

This algorithm uses a routine to tell if two rooted trees (trees with a
specified root node) are isomorphic, which may be independently useful.

This implements an algorithm from:
The Design and Analysis of Computer Algorithms
by Aho, Hopcroft, and Ullman
Addison-Wesley Publishing 1974
Example 3.2 pp. 84-86.

A more understandable version of this algorithm is described in:
Homework Assignment 5
McGill University SOCS 308-250B, Winter 2002
by Matthew Suderman
http://crypto.cs.mcgill.ca/~crepeau/CS250/2004/HW5+.pdf
"""

from _typeshed import Incomplete

from networkx.classes.graph import Graph, _Node
from networkx.utils.backends import _dispatchable

__all__ = ["rooted_tree_isomorphism", "tree_isomorphism"]

@_dispatchable
def root_trees(t1, root1, t2, root2):
    """Create a single digraph dT of free trees t1 and t2
    #   with roots root1 and root2 respectively
    # rename the nodes with consecutive integers
    # so that all nodes get a unique name between both trees

    # our new "fake" root node is 0
    # t1 is numbers from 1 ... n
    # t2 is numbered from n+1 to 2n
    """

@_dispatchable
def rooted_tree_isomorphism(t1, root1, t2, root2) -> list[tuple[Incomplete, Incomplete]]:
    """
    Return an isomorphic mapping between rooted trees `t1` and `t2` with roots
    `root1` and `root2`, respectively.

    These trees may be either directed or undirected,
    but if they are directed, all edges should flow from the root.

    It returns the isomorphism, a mapping of the nodes of `t1` onto the nodes
    of `t2`, such that two trees are then identical.

    Note that two trees may have more than one isomorphism, and this
    routine just returns one valid mapping.
    This is a subroutine used to implement `tree_isomorphism`, but will
    be somewhat faster if you already have rooted trees.

    Parameters
    ----------
    t1 :  NetworkX graph
        One of the trees being compared

    root1 : node
        A node of `t1` which is the root of the tree

    t2 : NetworkX graph
        The other tree being compared

    root2 : node
        a node of `t2` which is the root of the tree

    Returns
    -------
    isomorphism : list
        A list of pairs in which the left element is a node in `t1`
        and the right element is a node in `t2`.  The pairs are in
        arbitrary order.  If the nodes in one tree is mapped to the names in
        the other, then trees will be identical. Note that an isomorphism
        will not necessarily be unique.

        If `t1` and `t2` are not isomorphic, then it returns the empty list.

    Raises
    ------
    NetworkXError
        If either `t1` or `t2` is not a tree
    """

@_dispatchable
def tree_isomorphism(t1: Graph[_Node], t2: Graph[_Node]) -> list[tuple[Incomplete, Incomplete]]:
    """
    Return an isomorphic mapping between two trees `t1` and `t2`.

    If `t1` and `t2` are not isomorphic, an empty list is returned.
    Note that two trees may have more than one isomorphism, and this routine just
    returns one valid mapping.

    Parameters
    ----------
    t1 : undirected NetworkX graph
        One of the trees being compared

    t2 : undirected NetworkX graph
        The other tree being compared

    Returns
    -------
    isomorphism : list
        A list of pairs in which the left element is a node in `t1`
        and the right element is a node in `t2`.  The pairs are in
        arbitrary order.  If the nodes in one tree is mapped to the names in
        the other, then trees will be identical. Note that an isomorphism
        will not necessarily be unique.

        If `t1` and `t2` are not isomorphic, then it returns the empty list.

    Raises
    ------
    NetworkXError
        If either `t1` or `t2` is not a tree

    Notes
    -----
    This runs in ``O(n*log(n))`` time for trees with ``n`` nodes.
    """
