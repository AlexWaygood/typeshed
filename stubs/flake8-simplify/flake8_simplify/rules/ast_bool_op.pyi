import ast

def get_sim101(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """Get a positions where the duplicate isinstance problem appears."""

def get_sim109(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """
    Check if multiple equalities with the same value are combined via "or".

        BoolOp(
                op=Or(),
                values=[
                    Compare(
                        left=Name(id='a', ctx=Load()),
                        ops=[Eq()],
                        comparators=[Name(id='b', ctx=Load())],
                    ),
                    Compare(
                        left=Name(id='a', ctx=Load()),
                        ops=[Eq()],
                        comparators=[Name(id='c', ctx=Load())],
                    ),
                ],
        )
    """

def get_sim220(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "a and not a".

    BoolOp(
        op=And(),
        values=[
            Name(id='a', ctx=Load()),
            UnaryOp(
                op=Not(),
                operand=Name(id='a', ctx=Load()),
            ),
        ],
    )
    """

def get_sim221(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "a or not a".

    BoolOp(
        op=Or(),
        values=[
            Name(id='a', ctx=Load()),
            UnaryOp(
                op=Not(),
                operand=Name(id='a', ctx=Load()),
            ),
        ],
    )
    """

def get_sim222(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "... or True".

    BoolOp(
        op=Or(),
        values=[
            Name(id='a', ctx=Load()),
            UnaryOp(
                op=Not(),
                operand=Name(id='a', ctx=Load()),
            ),
        ],
    )
    """

def get_sim223(node: ast.BoolOp) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls of the type "... and False".

    BoolOp(
        op=And(),
        values=[
            Name(id='a', ctx=Load()),
            UnaryOp(
                op=Not(),
                operand=Name(id='a', ctx=Load()),
            ),
        ],
    )
    """
