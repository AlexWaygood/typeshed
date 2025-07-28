import ast

def get_sim210(node: ast.IfExp) -> list[tuple[int, int, str]]:
    """Get a list of all calls of the type "True if a else False"."""

def get_sim211(node: ast.IfExp) -> list[tuple[int, int, str]]:
    """Get a list of all calls of the type "False if a else True"."""

def get_sim212(node: ast.IfExp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "b if not a else a".

    IfExp(
        test=UnaryOp(
            op=Not(),
            operand=Name(id='a', ctx=Load()),
        ),
        body=Name(id='b', ctx=Load()),
        orelse=Name(id='a', ctx=Load()),
    )
    """
