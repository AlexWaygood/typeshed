import ast

def get_sim907(node: ast.Subscript) -> list[tuple[int, int, str]]:
    """

    Subscript(
        value=Name(id='Union', ctx=Load()),
        slice=Tuple(
            elts=[
                Name(id='int', ctx=Load()),
                Name(id='str', ctx=Load()),
                Constant(value=None, kind=None),
            ],
            ...
        )
    )
    """
