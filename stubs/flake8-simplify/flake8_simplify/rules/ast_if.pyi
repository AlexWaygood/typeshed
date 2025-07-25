import ast

from flake8_simplify.utils import If

def get_sim102(node: ast.If) -> list[tuple[int, int, str]]:
    """Get a list of all nested if-statements without else-blocks."""

def get_sim103(node: ast.If) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls that wrap a condition to return a bool.

    if cond:
        return True
    else:
        return False

    which is

        If(
            test=Name(id='cond', ctx=Load()),
            body=[
                Return(
                    value=Constant(value=True, kind=None),
                ),
            ],
            orelse=[
                Return(
                    value=Constant(value=False, kind=None),
                ),
            ],
        ),

    """

def get_sim108(node: If) -> list[tuple[int, int, str]]:
    """
    Get a list of all if-elses which could be a ternary operator assignment.

        If(
            test=Name(id='a', ctx=Load()),
            body=[
                Assign(
                    targets=[Name(id='b', ctx=Store())],
                    value=Name(id='c', ctx=Load()),
                    type_comment=None,
                ),
            ],
            orelse=[
                Assign(
                    targets=[Name(id='b', ctx=Store())],
                    value=Name(id='d', ctx=Load()),
                    type_comment=None,
                ),
            ],
        ),
    """

def get_sim114(node: ast.If) -> list[tuple[int, int, str]]:
    """
    Find same bodys.

    Examples
    --------
        If(
            test=Name(id='a', ctx=Load()),
            body=[
                Expr(
                    value=Name(id='b', ctx=Load()),
                ),
            ],
            orelse=[
                If(
                    test=Name(id='c', ctx=Load()),
                    body=[
                        Expr(
                            value=Name(id='b', ctx=Load()),
                        ),
                    ],
                    orelse=[],
                ),
            ],
        ),
    """

def get_sim116(node: ast.If) -> list[tuple[int, int, str]]:
    """
    Find places where 3 or more consecutive if-statements with direct returns.

    * Each if-statement must be a check for equality with the
      same variable
    * Each if-statement must just have a "return"
    * Else must also just have a return
    """

def get_sim908(node: ast.If) -> list[tuple[int, int, str]]:
    """
    Get all if-blocks which only check if a key is in a dictionary.
    """

def get_sim401(node: ast.If) -> list[tuple[int, int, str]]:
    """
    Get all calls that should use default values for dictionary access.

    Pattern 1
    ---------
    if key in a_dict:
        value = a_dict[key]
    else:
        value = "default"

    which is

        If(
            test=Compare(
                left=Name(id='key', ctx=Load()),
                ops=[In()],
                comparators=[Name(id='a_dict', ctx=Load())],
            ),
            body=[
                Assign(
                    targets=[Name(id='value', ctx=Store())],
                    value=Subscript(
                        value=Name(id='a_dict', ctx=Load()),
                        slice=Name(id='key', ctx=Load()),
                        ctx=Load(),
                    ),
                    type_comment=None,
                ),
            ],
            orelse=[
                Assign(
                    targets=[Name(id='value', ctx=Store())],
                    value=Constant(value='default', kind=None),
                    type_comment=None,
                ),
            ],
        ),

    Pattern 2
    ---------

        if key not in a_dict:
            value = 'default'
        else:
            value = a_dict[key]

    which is

        If(
            test=Compare(
                left=Name(id='key', ctx=Load()),
                ops=[NotIn()],
                comparators=[Name(id='a_dict', ctx=Load())],
            ),
            body=[
                Assign(
                    targets=[Name(id='value', ctx=Store())],
                    value=Constant(value='default', kind=None),
                    type_comment=None,
                ),
            ],
            orelse=[
                Assign(
                    targets=[Name(id='value', ctx=Store())],
                    value=Subscript(
                        value=Name(id='a_dict', ctx=Load()),
                        slice=Name(id='key', ctx=Load()),
                        ctx=Load(),
                    ),
                    type_comment=None,
                ),
            ],
        )

    """
