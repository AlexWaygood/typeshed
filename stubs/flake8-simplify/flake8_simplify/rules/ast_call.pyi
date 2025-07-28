import ast
import logging

from flake8_simplify.utils import Call

logger: logging.Logger

def get_sim115(node: Call) -> list[tuple[int, int, str]]:
    """
    Find places where open() is called without a context handler.

    Example AST
    -----------
        Assign(
            targets=[Name(id='f', ctx=Store())],
            value=Call(
                func=Name(id='open', ctx=Load()),
                args=[Constant(value=Ellipsis, kind=None)],
                keywords=[],
            ),
            type_comment=None,
        )
        ...
        Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='f', ctx=Load()),
                    attr='close',
                    ctx=Load(),
                ),
                args=[],
                keywords=[],
            ),
        ),
    """

def get_sim901(node: ast.Call) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "bool(comparison)".

    Call(
        func=Name(id='bool', ctx=Load()),
        args=[
            Compare(
                left=Name(id='a', ctx=Load()),
                ops=[Eq()],
                comparators=[Name(id='b', ctx=Load())],
            ),
        ],
        keywords=[],
    )
    """

def get_sim905(node: ast.Call) -> list[tuple[int, int, str]]: ...
def get_sim906(node: ast.Call) -> list[tuple[int, int, str]]: ...
def get_sim910(node: Call) -> list[tuple[int, int, str]]:
    """
    Get a list of all usages of "dict.get(key, None)"

    Example AST
    -----------
        Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='a_dict', ctx=Load()),
                    attr='get',
                    ctx=Load()
                ),
                args=[
                    Name(id='key', ctx=Load()),
                    Constant(value=None)
                ],
                keywords=[]
            ),
        ),
    """

def get_sim911(node: ast.AST) -> list[tuple[int, int, str]]:
    """
    Find nodes representing the expression "zip(_.keys(), _.values())".

    Returns a list of tuples containing the line number and column offset
    of each identified node.

    Expr(
        value=Call(
            func=Name(id='zip', ctx=Load()),
            args=[
                Call(
                    func=Attribute(
                        value=Name(id='_', ctx=Load()),
                        attr='keys',
                        ctx=Load()),
                    args=[],
                    keywords=[]),
                Call(
                    func=Attribute(
                        value=Name(id='_', ctx=Load()),
                        attr='values',
                        ctx=Load()),
                    args=[],
                    keywords=[])],
            keywords=[
                keyword(
                    arg='strict',
                    value=Constant(value=False))
                ]
            )
        )
    """
