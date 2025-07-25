"""Common constants, exceptions and helpe functions"""

from typing import Final

PY3: Final[bool]

class DefusedXmlException(ValueError):
    """Base exception"""

class DTDForbidden(DefusedXmlException):
    """Document type definition is forbidden"""

    name: str
    sysid: str | None
    pubid: str | None
    def __init__(self, name: str, sysid: str | None, pubid: str | None) -> None: ...

class EntitiesForbidden(DefusedXmlException):
    """Entity definition is forbidden"""

    name: str
    value: str | None
    base: str | None
    sysid: str | None
    pubid: str | None
    notation_name: str | None
    def __init__(
        self, name: str, value: str | None, base: str | None, sysid: str | None, pubid: str | None, notation_name: str | None
    ) -> None: ...

class ExternalReferenceForbidden(DefusedXmlException):
    """Resolving an external reference is forbidden"""

    context: str
    base: str | None
    sysid: str | None
    pubid: str | None
    def __init__(self, context: str, base: str | None, sysid: str | None, pubid: str | None) -> None: ...

class NotSupportedError(DefusedXmlException):
    """The operation is not supported"""
