"""Error classes used by simplejson"""

__all__ = ["JSONDecodeError"]

def linecol(doc: str, pos: int) -> tuple[int, int]: ...
def errmsg(msg: str, doc: str, pos: int, end: int | None = None) -> str: ...

class JSONDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The JSON document being parsed
    pos: The start index of doc where parsing failed
    end: The end index of doc where parsing failed (may be None)
    lineno: The line corresponding to pos
    colno: The column corresponding to pos
    endlineno: The line corresponding to end (may be None)
    endcolno: The column corresponding to end (may be None)

    """

    msg: str
    doc: str
    pos: int
    end: int | None
    lineno: int
    colno: int
    endlineno: int | None
    endcolno: int | None
    def __init__(self, msg: str, doc: str, pos: int, end: int | None = None) -> None: ...
    def __reduce__(self) -> tuple[JSONDecodeError, tuple[str, str, int, int | None]]: ...
