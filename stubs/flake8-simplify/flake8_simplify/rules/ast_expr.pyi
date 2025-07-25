import ast

def get_sim112(node: ast.Expr) -> list[tuple[int, int, str]]:
    """
    Find non-capitalized calls to environment variables.

    os.environ["foo"]
        Expr(
            value=Subscript(
                value=Attribute(
                    value=Name(id='os', ctx=Load()),
                    attr='environ',
                    ctx=Load(),
                ),
                slice=Index(
                    value=Constant(value='foo', kind=None),
                ),
                ctx=Load(),
            ),
        ),
    """
