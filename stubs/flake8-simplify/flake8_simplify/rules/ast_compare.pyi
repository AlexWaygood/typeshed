import ast

def get_sim118(node: ast.Compare) -> list[tuple[int, int, str]]:
    """
    Get a list of all usages of "key in dict.keys()"

    Compare(left=Name(id='key', ctx=Load()),
            ops=[In()],
            comparators=[
                Call(
                    func=Attribute(
                        value=Name(id='dict', ctx=Load()),
                        attr='keys',
                        ctx=Load(),
                    ),
                    args=[],
                    keywords=[],
                ),
            ],
        )
    """

def get_sim300(node: ast.Compare) -> list[tuple[int, int, str]]:
    """
    Get a list of all Yoda conditions.

    Compare(
                left=Constant(value='Yoda', kind=None),
                ops=[Eq()],
                comparators=[Name(id='i_am', ctx=Load())],
            )
    """
