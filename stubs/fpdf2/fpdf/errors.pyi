from typing import Any

class FPDFException(Exception): ...

class FPDFPageFormatException(FPDFException):
    """Error is thrown when a bad page format is given"""

    argument: Any
    unknown: Any
    one: Any
    def __init__(self, argument, unknown: bool = False, one: bool = False) -> None: ...

class FPDFUnicodeEncodingException(FPDFException):
    """Error is thrown when a character that cannot be encoded by the chosen encoder is provided"""

    def __init__(self, text_index, character, font_name) -> None: ...
