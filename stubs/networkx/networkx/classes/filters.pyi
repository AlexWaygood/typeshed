"""Filter factories to hide or show sets of nodes and edges.

These filters return the function used when creating `SubGraph`.
"""

from _typeshed import Incomplete

__all__ = [
    "no_filter",
    "hide_nodes",
    "hide_edges",
    "hide_multiedges",
    "hide_diedges",
    "hide_multidiedges",
    "show_nodes",
    "show_edges",
    "show_multiedges",
    "show_diedges",
    "show_multidiedges",
]

def no_filter(*items):
    """Returns a filter function that always evaluates to True."""

def hide_nodes(nodes):
    """Returns a filter function that hides specific nodes."""

def hide_diedges(edges):
    """Returns a filter function that hides specific directed edges."""

def hide_edges(edges):
    """Returns a filter function that hides specific undirected edges."""

def hide_multidiedges(edges):
    """Returns a filter function that hides specific multi-directed edges."""

def hide_multiedges(edges):
    """Returns a filter function that hides specific multi-undirected edges."""

class show_nodes:
    """Filter class to show specific nodes.

    Attach the set of nodes as an attribute to speed up this commonly used filter

    Note that another allowed attribute for filters is to store the number of nodes
    on the filter as attribute `length` (used in `__len__`). It is a user
    responsibility to ensure this attribute is accurate if present.
    """

    nodes: Incomplete
    def __init__(self, nodes) -> None: ...
    def __call__(self, node): ...

def show_diedges(edges):
    """Returns a filter function that shows specific directed edges."""

def show_edges(edges):
    """Returns a filter function that shows specific undirected edges."""

def show_multidiedges(edges):
    """Returns a filter function that shows specific multi-directed edges."""

def show_multiedges(edges):
    """Returns a filter function that shows specific multi-undirected edges."""
