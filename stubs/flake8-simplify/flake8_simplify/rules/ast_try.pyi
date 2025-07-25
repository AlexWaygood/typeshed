import ast

def get_sim105(node: ast.Try) -> list[tuple[int, int, str]]:
    """
    Get a list of all "try-except-pass" patterns.

    try:
        foo()
    except ValueError:
        pass

    which is

        Try(
            body=[
                Expr(
                    value=Call(
                        func=Name(id='foo', ctx=Load()),
                        args=[],
                        keywords=[],
                    ),
                ),
            ],
            handlers=[
                ExceptHandler(
                    type=Name(id='ValueError', ctx=Load()),
                    name=None,
                    body=[Pass()],
                ),
            ],
            orelse=[],
            finalbody=[],
        ),


    """

def get_sim107(node: ast.Try) -> list[tuple[int, int, str]]:
    """
    Get a list of all calls where try/except and finally have 'return'.
    """
