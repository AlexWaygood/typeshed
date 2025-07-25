from typing_extensions import deprecated

class StyleProxy:
    """
    Proxy formatting objects so that they cannot be altered
    """

    def __init__(self, target) -> None: ...
    def __getattr__(self, attr: str): ...
    def __setattr__(self, attr: str, value) -> None: ...
    def __copy__(self):
        """
        Return a copy of the proxied object.
        """

    def __add__(self, other):
        """
        Add proxied object to another instance and return the combined object
        """

    @deprecated("Use copy(obj) or cell.obj = cell.obj + other")
    def copy(self, **kw):
        """Return a copy of the proxied object. Keyword args will be passed through"""

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
