"""
Exception Classes for the xdg package
"""

debug: bool

class Error(Exception):
    """Base class for exceptions defined here."""

    msg: str
    def __init__(self, msg: str) -> None: ...

class ValidationError(Error):
    """Raised when a file fails to validate.

    The filename is the .file attribute.
    """

    msg: str
    file: str
    def __init__(self, msg: str, file: str) -> None: ...

class ParsingError(Error):
    """Raised when a file cannot be parsed.

    The filename is the .file attribute.
    """

    msg: str
    file: str
    def __init__(self, msg: str, file: str) -> None: ...

class NoKeyError(Error):
    """Raised when trying to access a nonexistant key in an INI-style file.

    Attributes are .key, .group and .file.
    """

    key: str
    group: str
    file: str
    def __init__(self, key: str, group: str, file: str) -> None: ...

class DuplicateKeyError(Error):
    """Raised when the same key occurs twice in an INI-style file.

    Attributes are .key, .group and .file.
    """

    key: str
    group: str
    file: str
    def __init__(self, key: str, group: str, file: str) -> None: ...

class NoGroupError(Error):
    """Raised when trying to access a nonexistant group in an INI-style file.

    Attributes are .group and .file.
    """

    group: str
    file: str
    def __init__(self, group: str, file: str) -> None: ...

class DuplicateGroupError(Error):
    """Raised when the same key occurs twice in an INI-style file.

    Attributes are .group and .file.
    """

    group: str
    file: str
    def __init__(self, group: str, file: str) -> None: ...

class NoThemeError(Error):
    """Raised when trying to access a nonexistant icon theme.

    The name of the theme is the .theme attribute.
    """

    theme: str
    def __init__(self, theme: str) -> None: ...
