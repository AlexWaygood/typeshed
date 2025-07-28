import ast

def get_sim117(node: ast.With) -> list[tuple[int, int, str]]:
    """
    Find multiple with-statements with same scope.

        With(
            items=[
                withitem(
                    context_expr=Call(
                        func=Name(id='A', ctx=Load()),
                        args=[],
                        keywords=[],
                    ),
                    optional_vars=Name(id='a', ctx=Store()),
                ),
            ],
            body=[
                With(
                    items=[
                        withitem(
                            context_expr=Call(
                                func=Name(id='B', ctx=Load()),
                                args=[],
                                keywords=[],
                            ),
                            optional_vars=Name(id='b', ctx=Store()),
                        ),
                    ],
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id='print', ctx=Load()),
                                args=[Constant(value='hello', kind=None)],
                                keywords=[],
                            ),
                        ),
                    ],
                    type_comment=None,
                ),
            ],
            type_comment=None,
        ),
    """
