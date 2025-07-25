"""
.. module:: jenkins.plugins
    :platform: Unix, Windows
    :synopsis: Class for interacting with plugins
"""

from typing import Any

# Any: Union of possible plugin values is too complex
class Plugin(dict[str, Any]):
    """Dictionary object containing plugin metadata."""

    # __init__ wraps dict.__init__  w/o changing the type signature
    def __setitem__(self, key: str, value: Any) -> None:
        """Overrides default setter to ensure that the version key is always
        a PluginVersion class to abstract and simplify version comparisons
        """

class PluginVersion(str):
    """Class providing comparison capabilities for plugin versions."""

    def __init__(self, version: str) -> None:
        """Parse plugin version and store it for comparison."""

    def __le__(self, version: object) -> bool: ...
    def __lt__(self, version: object) -> bool: ...
    def __ge__(self, version: object) -> bool: ...
    def __gt__(self, version: object) -> bool: ...
    def __eq__(self, version: object) -> bool: ...
    def __ne__(self, version: object) -> bool: ...
