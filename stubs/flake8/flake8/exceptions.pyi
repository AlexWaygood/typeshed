"""Exception classes for all of Flake8."""

from _typeshed import Incomplete

class Flake8Exception(Exception):
    """Plain Flake8 exception."""

class EarlyQuit(Flake8Exception):
    """Except raised when encountering a KeyboardInterrupt."""

class ExecutionError(Flake8Exception):
    """Exception raised during execution of Flake8."""

class FailedToLoadPlugin(Flake8Exception):
    """Exception raised when a plugin fails to load."""

    FORMAT: str
    plugin_name: Incomplete
    original_exception: Incomplete
    def __init__(self, plugin_name: str, exception: Exception) -> None:
        """Initialize our FailedToLoadPlugin exception."""

class PluginRequestedUnknownParameters(Flake8Exception):
    """The plugin requested unknown parameters."""

    FORMAT: str
    plugin_name: Incomplete
    original_exception: Incomplete
    def __init__(self, plugin_name: str, exception: Exception) -> None:
        """Pop certain keyword arguments for initialization."""

class PluginExecutionFailed(Flake8Exception):
    """The plugin failed during execution."""

    FORMAT: str
    filename: Incomplete
    plugin_name: Incomplete
    original_exception: Incomplete
    def __init__(self, filename: str, plugin_name: str, exception: Exception) -> None:
        """Utilize keyword arguments for message generation."""
