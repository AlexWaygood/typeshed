"""JSON token scanner"""

from collections.abc import Callable

from simplejson.decoder import JSONDecoder

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

def make_scanner(context: JSONDecoder) -> Callable[[str, int], tuple[bool, int]]:
    """JSON scanner object"""

__all__ = ["make_scanner", "JSONDecodeError"]
