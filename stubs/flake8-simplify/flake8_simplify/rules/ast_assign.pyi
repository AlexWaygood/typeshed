import ast

from flake8_simplify.utils import Assign

def get_sim904(node: ast.Assign) -> list[tuple[int, int, str]]:
    """
    Assign values to dictionary directly at initialization.

    Example
    -------
    Code:
        # Bad
        a = { }
        a['b] = 'c'

        # Good
        a = {'b': 'c'}
    Bad AST:
        [
            Assign(
                targets=[Name(id='a', ctx=Store())],
                value=Dict(keys=[], values=[]),
                type_comment=None,
            ),
            Assign(
                targets=[
                    Subscript(
                        value=Name(id='a', ctx=Load()),
                        slice=Constant(value='b', kind=None),
                        ctx=Store(),
                    ),
                ],
                value=Constant(value='c', kind=None),
                type_comment=None,
            ),
        ]
    """

def get_sim909(node: Assign) -> list[tuple[int, int, str]]:
    """
    Avoid reflexive assignments

    Example
    -------
    Code:
        # Bad
        foo = foo

        # Good: Just remove them
    Bad AST:
        [
            Assign(
                targets=[Name(id='foo', ctx=Store())],
                value=Name(id='foo', ctx=Load()),
                type_comment=None,
            ),
        ]
    """
