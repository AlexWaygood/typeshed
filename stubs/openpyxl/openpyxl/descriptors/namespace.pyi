# 'None' shouldn't be a valid tagname and namespaced should always return str
def namespaced(obj: object, tagname: str, namespace: str | None = None) -> str:
    """
    Utility to create a namespaced tag for an object
    """
