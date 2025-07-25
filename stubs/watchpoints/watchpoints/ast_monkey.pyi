import ast

def ast_parse_node(node: ast.expr) -> ast.Module:
    """
    :param ast.Node node: an ast node representing an expression of variable

    :return ast.Node: an ast node for:
        _watchpoints_obj = var
        if <var is a local variable>:
            # watch(a)
            _watchpoints_localvar = "a"
        elif <var is a subscript>:
            # watch(a[3])
            _watchpoints_parent = a
            _watchpoints_subscr = 3
        elif <var is an attribute>:
            # watch(a.b)
            _watchpoints_parent = a
            _watchpoints_attr = "b"
    """
