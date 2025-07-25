"""
Algorithm for testing d-separation in DAGs.

*d-separation* is a test for conditional independence in probability
distributions that can be factorized using DAGs.  It is a purely
graphical test that uses the underlying graph and makes no reference
to the actual distribution parameters.  See [1]_ for a formal
definition.

The implementation is based on the conceptually simple linear time
algorithm presented in [2]_.  Refer to [3]_, [4]_ for a couple of
alternative algorithms.

The functional interface in NetworkX consists of three functions:

- `find_minimal_d_separator` returns a minimal d-separator set ``z``.
  That is, removing any node or nodes from it makes it no longer a d-separator.
- `is_d_separator` checks if a given set is a d-separator.
- `is_minimal_d_separator` checks if a given set is a minimal d-separator.

D-separators
------------

Here, we provide a brief overview of d-separation and related concepts that
are relevant for understanding it:

The ideas of d-separation and d-connection relate to paths being open or blocked.

- A "path" is a sequence of nodes connected in order by edges. Unlike for most
  graph theory analysis, the direction of the edges is ignored. Thus the path
  can be thought of as a traditional path on the undirected version of the graph.
- A "candidate d-separator" ``z`` is a set of nodes being considered as
  possibly blocking all paths between two prescribed sets ``x`` and ``y`` of nodes.
  We refer to each node in the candidate d-separator as "known".
- A "collider" node on a path is a node that is a successor of its two neighbor
  nodes on the path. That is, ``c`` is a collider if the edge directions
  along the path look like ``... u -> c <- v ...``.
- If a collider node or any of its descendants are "known", the collider
  is called an "open collider". Otherwise it is a "blocking collider".
- Any path can be "blocked" in two ways. If the path contains a "known" node
  that is not a collider, the path is blocked. Also, if the path contains a
  collider that is not a "known" node, the path is blocked.
- A path is "open" if it is not blocked. That is, it is open if every node is
  either an open collider or not a "known". Said another way, every
  "known" in the path is a collider and every collider is open (has a
  "known" as a inclusive descendant). The concept of "open path" is meant to
  demonstrate a probabilistic conditional dependence between two nodes given
  prescribed knowledge ("known" nodes).
- Two sets ``x`` and ``y`` of nodes are "d-separated" by a set of nodes ``z``
  if all paths between nodes in ``x`` and nodes in ``y`` are blocked. That is,
  if there are no open paths from any node in ``x`` to any node in ``y``.
  Such a set ``z`` is a "d-separator" of ``x`` and ``y``.
- A "minimal d-separator" is a d-separator ``z`` for which no node or subset
  of nodes can be removed with it still being a d-separator.

The d-separator blocks some paths between ``x`` and ``y`` but opens others.
Nodes in the d-separator block paths if the nodes are not colliders.
But if a collider or its descendant nodes are in the d-separation set, the
colliders are open, allowing a path through that collider.

Illustration of D-separation with examples
------------------------------------------

A pair of two nodes, ``u`` and ``v``, are d-connected if there is a path
from ``u`` to ``v`` that is not blocked. That means, there is an open
path from ``u`` to ``v``.

For example, if the d-separating set is the empty set, then the following paths are
open between ``u`` and ``v``:

- u <- n -> v
- u -> w -> ... -> n -> v

If  on the other hand, ``n`` is in the d-separating set, then ``n`` blocks
those paths between ``u`` and ``v``.

Colliders block a path if they and their descendants are not included
in the d-separating set. An example of a path that is blocked when the
d-separating set is empty is:

- u -> w -> ... -> n <- v

The node ``n`` is a collider in this path and is not in the d-separating set.
So ``n`` blocks this path. However, if ``n`` or a descendant of ``n`` is
included in the d-separating set, then the path through the collider
at ``n`` (... -> n <- ...) is "open".

D-separation is concerned with blocking all paths between nodes from ``x`` to ``y``.
A d-separating set between ``x`` and ``y`` is one where all paths are blocked.

D-separation and its applications in probability
------------------------------------------------

D-separation is commonly used in probabilistic causal-graph models. D-separation
connects the idea of probabilistic "dependence" with separation in a graph. If
one assumes the causal Markov condition [5]_, (every node is conditionally
independent of its non-descendants, given its parents) then d-separation implies
conditional independence in probability distributions.
Symmetrically, d-connection implies dependence.

The intuition is as follows. The edges on a causal graph indicate which nodes
influence the outcome of other nodes directly. An edge from u to v
implies that the outcome of event ``u`` influences the probabilities for
the outcome of event ``v``. Certainly knowing ``u`` changes predictions for ``v``.
But also knowing ``v`` changes predictions for ``u``. The outcomes are dependent.
Furthermore, an edge from ``v`` to ``w`` would mean that ``w`` and ``v`` are dependent
and thus that ``u`` could indirectly influence ``w``.

Without any knowledge about the system (candidate d-separating set is empty)
a causal graph ``u -> v -> w`` allows all three nodes to be dependent. But
if we know the outcome of ``v``, the conditional probabilities of outcomes for
``u`` and ``w`` are independent of each other. That is, once we know the outcome
for ``v``, the probabilities for ``w`` do not depend on the outcome for ``u``.
This is the idea behind ``v`` blocking the path if it is "known" (in the candidate
d-separating set).

The same argument works whether the direction of the edges are both
left-going and when both arrows head out from the middle. Having a "known"
node on a path blocks the collider-free path because those relationships
make the conditional probabilities independent.

The direction of the causal edges does impact dependence precisely in the
case of a collider e.g. ``u -> v <- w``. In that situation, both ``u`` and ``w``
influence ``v``. But they do not directly influence each other. So without any
knowledge of any outcomes, ``u`` and ``w`` are independent. That is the idea behind
colliders blocking the path. But, if ``v`` is known, the conditional probabilities
of ``u`` and ``w`` can be dependent. This is the heart of Berkson's Paradox [6]_.
For example, suppose ``u`` and ``w`` are boolean events (they either happen or do not)
and ``v`` represents the outcome "at least one of ``u`` and ``w`` occur". Then knowing
``v`` is true makes the conditional probabilities of ``u`` and ``w`` dependent.
Essentially, knowing that at least one of them is true raises the probability of
each. But further knowledge that ``w`` is true (or false) change the conditional
probability of ``u`` to either the original value or 1. So the conditional
probability of ``u`` depends on the outcome of ``w`` even though there is no
causal relationship between them. When a collider is known, dependence can
occur across paths through that collider. This is the reason open colliders
do not block paths.

Furthermore, even if ``v`` is not "known", if one of its descendants is "known"
we can use that information to know more about ``v`` which again makes
``u`` and ``w`` potentially dependent. Suppose the chance of ``n`` occurring
is much higher when ``v`` occurs ("at least one of ``u`` and ``w`` occur").
Then if we know ``n`` occurred, it is more likely that ``v`` occurred and that
makes the chance of ``u`` and ``w`` dependent. This is the idea behind why
a collider does no block a path if any descendant of the collider is "known".

When two sets of nodes ``x`` and ``y`` are d-separated by a set ``z``,
it means that given the outcomes of the nodes in ``z``, the probabilities
of outcomes of the nodes in ``x`` are independent of the outcomes of the
nodes in ``y`` and vice versa.

Examples
--------
A Hidden Markov Model with 5 observed states and 5 hidden states
where the hidden states have causal relationships resulting in
a path results in the following causal network. We check that
early states along the path are separated from late state in
the path by the d-separator of the middle hidden state.
Thus if we condition on the middle hidden state, the early
state probabilities are independent of the late state outcomes.

>>> G = nx.DiGraph()
>>> G.add_edges_from(
...     [
...         ("H1", "H2"),
...         ("H2", "H3"),
...         ("H3", "H4"),
...         ("H4", "H5"),
...         ("H1", "O1"),
...         ("H2", "O2"),
...         ("H3", "O3"),
...         ("H4", "O4"),
...         ("H5", "O5"),
...     ]
... )
>>> x, y, z = ({"H1", "O1"}, {"H5", "O5"}, {"H3"})
>>> nx.is_d_separator(G, x, y, z)
True
>>> nx.is_minimal_d_separator(G, x, y, z)
True
>>> nx.is_minimal_d_separator(G, x, y, z | {"O3"})
False
>>> z = nx.find_minimal_d_separator(G, x | y, {"O2", "O3", "O4"})
>>> z == {"H2", "H4"}
True

If no minimal_d_separator exists, `None` is returned

>>> other_z = nx.find_minimal_d_separator(G, x | y, {"H2", "H3"})
>>> other_z is None
True


References
----------

.. [1] Pearl, J.  (2009).  Causality.  Cambridge: Cambridge University Press.

.. [2] Darwiche, A.  (2009).  Modeling and reasoning with Bayesian networks.
   Cambridge: Cambridge University Press.

.. [3] Shachter, Ross D. "Bayes-ball: The rational pastime (for
   determining irrelevance and requisite information in belief networks
   and influence diagrams)." In Proceedings of the Fourteenth Conference
   on Uncertainty in Artificial Intelligence (UAI), (pp. 480–487). 1998.

.. [4] Koller, D., & Friedman, N. (2009).
   Probabilistic graphical models: principles and techniques. The MIT Press.

.. [5] https://en.wikipedia.org/wiki/Causal_Markov_condition

.. [6] https://en.wikipedia.org/wiki/Berkson%27s_paradox

"""

from _typeshed import Incomplete

from networkx.classes.digraph import DiGraph
from networkx.classes.graph import _Node
from networkx.utils.backends import _dispatchable

__all__ = ["is_d_separator", "is_minimal_d_separator", "find_minimal_d_separator"]

@_dispatchable
def is_d_separator(G: DiGraph[_Node], x: _Node | set[_Node], y: _Node | set[_Node], z: _Node | set[_Node]) -> bool:
    """Return whether node sets `x` and `y` are d-separated by `z`.

    Parameters
    ----------
    G : nx.DiGraph
        A NetworkX DAG.

    x : node or set of nodes
        First node or set of nodes in `G`.

    y : node or set of nodes
        Second node or set of nodes in `G`.

    z : node or set of nodes
        Potential separator (set of conditioning nodes in `G`). Can be empty set.

    Returns
    -------
    b : bool
        A boolean that is true if `x` is d-separated from `y` given `z` in `G`.

    Raises
    ------
    NetworkXError
        The *d-separation* test is commonly used on disjoint sets of
        nodes in acyclic directed graphs.  Accordingly, the algorithm
        raises a :exc:`NetworkXError` if the node sets are not
        disjoint or if the input graph is not a DAG.

    NodeNotFound
        If any of the input nodes are not found in the graph,
        a :exc:`NodeNotFound` exception is raised

    Notes
    -----
    A d-separating set in a DAG is a set of nodes that
    blocks all paths between the two sets. Nodes in `z`
    block a path if they are part of the path and are not a collider,
    or a descendant of a collider. Also colliders that are not in `z`
    block a path. A collider structure along a path
    is ``... -> c <- ...`` where ``c`` is the collider node.

    https://en.wikipedia.org/wiki/Bayesian_network#d-separation
    """

@_dispatchable
def find_minimal_d_separator(G, x, y, *, included=None, restricted=None) -> set[Incomplete] | None:
    """Returns a minimal d-separating set between `x` and `y` if possible

    A d-separating set in a DAG is a set of nodes that blocks all
    paths between the two sets of nodes, `x` and `y`. This function
    constructs a d-separating set that is "minimal", meaning no nodes can
    be removed without it losing the d-separating property for `x` and `y`.
    If no d-separating sets exist for `x` and `y`, this returns `None`.

    In a DAG there may be more than one minimal d-separator between two
    sets of nodes. Minimal d-separators are not always unique. This function
    returns one minimal d-separator, or `None` if no d-separator exists.

    Uses the algorithm presented in [1]_. The complexity of the algorithm
    is :math:`O(m)`, where :math:`m` stands for the number of edges in
    the subgraph of G consisting of only the ancestors of `x` and `y`.
    For full details, see [1]_.

    Parameters
    ----------
    G : graph
        A networkx DAG.
    x : set | node
        A node or set of nodes in the graph.
    y : set | node
        A node or set of nodes in the graph.
    included : set | node | None
        A node or set of nodes which must be included in the found separating set,
        default is None, which means the empty set.
    restricted : set | node | None
        Restricted node or set of nodes to consider. Only these nodes can be in
        the found separating set, default is None meaning all nodes in ``G``.

    Returns
    -------
    z : set | None
        The minimal d-separating set, if at least one d-separating set exists,
        otherwise None.

    Raises
    ------
    NetworkXError
        Raises a :exc:`NetworkXError` if the input graph is not a DAG
        or if node sets `x`, `y`, and `included` are not disjoint.

    NodeNotFound
        If any of the input nodes are not found in the graph,
        a :exc:`NodeNotFound` exception is raised.

    References
    ----------
    .. [1] van der Zander, Benito, and Maciej Liśkiewicz. "Finding
        minimal d-separators in linear time and applications." In
        Uncertainty in Artificial Intelligence, pp. 637-647. PMLR, 2020.
    """

@_dispatchable
def is_minimal_d_separator(
    G: DiGraph[_Node],
    x: _Node | set[_Node],
    y: _Node | set[_Node],
    z: _Node | set[_Node],
    *,
    included: _Node | set[_Node] | None = None,
    restricted: _Node | set[_Node] | None = None,
) -> bool:
    """Determine if `z` is a minimal d-separator for `x` and `y`.

    A d-separator, `z`, in a DAG is a set of nodes that blocks
    all paths from nodes in set `x` to nodes in set `y`.
    A minimal d-separator is a d-separator `z` such that removing
    any subset of nodes makes it no longer a d-separator.

    Note: This function checks whether `z` is a d-separator AND is
    minimal. One can use the function `is_d_separator` to only check if
    `z` is a d-separator. See examples below.

    Parameters
    ----------
    G : nx.DiGraph
        A NetworkX DAG.
    x : node | set
        A node or set of nodes in the graph.
    y : node | set
        A node or set of nodes in the graph.
    z : node | set
        The node or set of nodes to check if it is a minimal d-separating set.
        The function :func:`is_d_separator` is called inside this function
        to verify that `z` is in fact a d-separator.
    included : set | node | None
        A node or set of nodes which must be included in the found separating set,
        default is ``None``, which means the empty set.
    restricted : set | node | None
        Restricted node or set of nodes to consider. Only these nodes can be in
        the found separating set, default is ``None`` meaning all nodes in ``G``.

    Returns
    -------
    bool
        Whether or not the set `z` is a minimal d-separator subject to
        `restricted` nodes and `included` node constraints.

    Examples
    --------
    >>> G = nx.path_graph([0, 1, 2, 3], create_using=nx.DiGraph)
    >>> G.add_node(4)
    >>> nx.is_minimal_d_separator(G, 0, 2, {1})
    True
    >>> # since {1} is the minimal d-separator, {1, 3, 4} is not minimal
    >>> nx.is_minimal_d_separator(G, 0, 2, {1, 3, 4})
    False
    >>> # alternatively, if we only want to check that {1, 3, 4} is a d-separator
    >>> nx.is_d_separator(G, 0, 2, {1, 3, 4})
    True

    Raises
    ------
    NetworkXError
        Raises a :exc:`NetworkXError` if the input graph is not a DAG.

    NodeNotFound
        If any of the input nodes are not found in the graph,
        a :exc:`NodeNotFound` exception is raised.

    References
    ----------
    .. [1] van der Zander, Benito, and Maciej Liśkiewicz. "Finding
        minimal d-separators in linear time and applications." In
        Uncertainty in Artificial Intelligence, pp. 637-647. PMLR, 2020.

    Notes
    -----
    This function works on verifying that a set is minimal and
    d-separating between two nodes. Uses criterion (a), (b), (c) on
    page 4 of [1]_. a) closure(`x`) and `y` are disjoint. b) `z` contains
    all nodes from `included` and is contained in the `restricted`
    nodes and in the union of ancestors of `x`, `y`, and `included`.
    c) the nodes in `z` not in `included` are contained in both
    closure(x) and closure(y). The closure of a set is the set of nodes
    connected to the set by a directed path in G.

    The complexity is :math:`O(m)`, where :math:`m` stands for the
    number of edges in the subgraph of G consisting of only the
    ancestors of `x` and `y`.

    For full details, see [1]_.
    """
