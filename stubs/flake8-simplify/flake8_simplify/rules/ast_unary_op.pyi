import ast

from flake8_simplify.utils import UnaryOp

def get_sim201(node: UnaryOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls where an unary 'not' is used for an equality.
    """

def get_sim202(node: UnaryOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls where an unary 'not' is used for an quality.
    """

def get_sim203(node: UnaryOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls where an unary 'not' is used for an in-check.
    """

def get_sim208(node: ast.UnaryOp) -> list[tuple[int, int, str]]:
    """Get a list of all calls of the type "not (not a)"."""
