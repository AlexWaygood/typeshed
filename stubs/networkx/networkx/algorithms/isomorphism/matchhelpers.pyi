"""Functions which help end users define customize node_match and
edge_match functions to use during isomorphism checks.
"""

from _typeshed import Incomplete
from types import FunctionType

from networkx.utils.backends import _dispatchable

__all__ = [
    "categorical_node_match",
    "categorical_edge_match",
    "categorical_multiedge_match",
    "numerical_node_match",
    "numerical_edge_match",
    "numerical_multiedge_match",
    "generic_node_match",
    "generic_edge_match",
    "generic_multiedge_match",
]

def copyfunc(f, name=None) -> FunctionType:
    """Returns a deepcopy of a function."""

def allclose(x, y, rtol: float = 1.0000000000000001e-05, atol=1e-08) -> bool:
    """Returns True if x and y are sufficiently close, elementwise.

    Parameters
    ----------
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    """

@_dispatchable
def categorical_node_match(attr, default):
    """
    Returns a comparison function for a categorical node attribute.

    The value(s) of the attr(s) must be hashable and comparable via the ==
    operator since they are placed into a set([]) object.  If the sets from
    G1 and G2 are the same, then the constructed function returns True.

    Parameters
    ----------
    attr : string | list
        The categorical node attribute to compare, or a list of categorical
        node attributes to compare.
    default : value | list
        The default value for the categorical node attribute, or a list of
        default values for the categorical node attributes.

    Returns
    -------
    match : function
        The customized, categorical `node_match` function.

    Examples
    --------
    >>> import networkx.algorithms.isomorphism as iso
    >>> nm = iso.categorical_node_match("size", 1)
    >>> nm = iso.categorical_node_match(["color", "size"], ["red", 2])

    """

categorical_edge_match: Incomplete

@_dispatchable
def categorical_multiedge_match(attr, default):
    """
    Returns a comparison function for a categorical edge attribute.

    The value(s) of the attr(s) must be hashable and comparable via the ==
    operator since they are placed into a set([]) object.  If the sets from
    G1 and G2 are the same, then the constructed function returns True.

    Parameters
    ----------
    attr : string | list
        The categorical edge attribute to compare, or a list of categorical
        edge attributes to compare.
    default : value | list
        The default value for the categorical edge attribute, or a list of
        default values for the categorical edge attributes.

    Returns
    -------
    match : function
        The customized, categorical `edge_match` function.

    Examples
    --------
    >>> import networkx.algorithms.isomorphism as iso
    >>> nm = iso.categorical_multiedge_match("size", 1)
    >>> nm = iso.categorical_multiedge_match(["color", "size"], ["red", 2])

    """

@_dispatchable
def numerical_node_match(attr, default, rtol: float = 1e-05, atol: float = 1e-08):
    """
    Returns a comparison function for a numerical node attribute.

    The value(s) of the attr(s) must be numerical and sortable.  If the
    sorted list of values from G1 and G2 are the same within some
    tolerance, then the constructed function returns True.

    Parameters
    ----------
    attr : string | list
        The numerical node attribute to compare, or a list of numerical
        node attributes to compare.
    default : value | list
        The default value for the numerical node attribute, or a list of
        default values for the numerical node attributes.
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    Returns
    -------
    match : function
        The customized, numerical `node_match` function.

    Examples
    --------
    >>> import networkx.algorithms.isomorphism as iso
    >>> nm = iso.numerical_node_match("weight", 1.0)
    >>> nm = iso.numerical_node_match(["weight", "linewidth"], [0.25, 0.5])

    """

numerical_edge_match: Incomplete

@_dispatchable
def numerical_multiedge_match(attr, default, rtol: float = 1e-05, atol: float = 1e-08):
    """
    Returns a comparison function for a numerical edge attribute.

    The value(s) of the attr(s) must be numerical and sortable.  If the
    sorted list of values from G1 and G2 are the same within some
    tolerance, then the constructed function returns True.

    Parameters
    ----------
    attr : string | list
        The numerical edge attribute to compare, or a list of numerical
        edge attributes to compare.
    default : value | list
        The default value for the numerical edge attribute, or a list of
        default values for the numerical edge attributes.
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    Returns
    -------
    match : function
        The customized, numerical `edge_match` function.

    Examples
    --------
    >>> import networkx.algorithms.isomorphism as iso
    >>> nm = iso.numerical_multiedge_match("weight", 1.0)
    >>> nm = iso.numerical_multiedge_match(["weight", "linewidth"], [0.25, 0.5])

    """

@_dispatchable
def generic_node_match(attr, default, op):
    """
    Returns a comparison function for a generic attribute.

    The value(s) of the attr(s) are compared using the specified
    operators. If all the attributes are equal, then the constructed
    function returns True.

    Parameters
    ----------
    attr : string | list
        The node attribute to compare, or a list of node attributes
        to compare.
    default : value | list
        The default value for the node attribute, or a list of
        default values for the node attributes.
    op : callable | list
        The operator to use when comparing attribute values, or a list
        of operators to use when comparing values for each attribute.

    Returns
    -------
    match : function
        The customized, generic `node_match` function.

    Examples
    --------
    >>> from operator import eq
    >>> from math import isclose
    >>> from networkx.algorithms.isomorphism import generic_node_match
    >>> nm = generic_node_match("weight", 1.0, isclose)
    >>> nm = generic_node_match("color", "red", eq)
    >>> nm = generic_node_match(["weight", "color"], [1.0, "red"], [isclose, eq])

    """

generic_edge_match: Incomplete

@_dispatchable
def generic_multiedge_match(attr, default, op):
    """Returns a comparison function for a generic attribute.

    The value(s) of the attr(s) are compared using the specified
    operators. If all the attributes are equal, then the constructed
    function returns True. Potentially, the constructed edge_match
    function can be slow since it must verify that no isomorphism
    exists between the multiedges before it returns False.

    Parameters
    ----------
    attr : string | list
        The edge attribute to compare, or a list of node attributes
        to compare.
    default : value | list
        The default value for the edge attribute, or a list of
        default values for the edgeattributes.
    op : callable | list
        The operator to use when comparing attribute values, or a list
        of operators to use when comparing values for each attribute.

    Returns
    -------
    match : function
        The customized, generic `edge_match` function.

    Examples
    --------
    >>> from operator import eq
    >>> from math import isclose
    >>> from networkx.algorithms.isomorphism import generic_node_match
    >>> nm = generic_node_match("weight", 1.0, isclose)
    >>> nm = generic_node_match("color", "red", eq)
    >>> nm = generic_node_match(["weight", "color"], [1.0, "red"], [isclose, eq])

    """
