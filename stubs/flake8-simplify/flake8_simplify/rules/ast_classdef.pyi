import ast

def get_sim120(node: ast.ClassDef) -> list[tuple[int, int, str]]:
    """
    Get a list of all classes that inherit from object.
    """
